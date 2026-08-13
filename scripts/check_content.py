from __future__ import annotations

import mimetypes
import re
import sys
import warnings
from filecmp import cmp
from pathlib import Path
from typing import BinaryIO
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token
from PIL import Image, UnidentifiedImageError

ARTICLE_PATH_RE = re.compile(r"^news/[^/]+/\d{4}/\d{2}/([^/]+)\.md$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n")
SLUG_RE = re.compile(r"^slug:\s*([^\s]+)\s*$", re.MULTILINE)
SINGLE_LINE_IMAGE_RE = re.compile(r"^!\[(?:\\.|[^\]\\\r\n])*\]\(((?:\\.|[^\r\n])*)\)$")
ATTRIBUTION_TEXT_RE = re.compile(
    r"^사진:\s*(.*?)\s*·\s*출처:\s*(https://\S+)\s*·\s*라이선스:\s*(.*?)$",
    re.IGNORECASE,
)
BARE_EXTERNAL_URL_RE = re.compile(
    r"(?i)(?<![\w])(?:(?:(?:https?|ftp):)?//[^\s<]+|www\.[^\s<]+)"
)
BARE_EMAIL_RE = re.compile(
    r"(?i)(?<![\w.+-])[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9.-]+\.[a-z]{2,}"
)
ALLOWED_IMAGE_EXTENSIONS = {".webp", ".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {
    ".mp4",
    ".webm",
    ".mov",
    ".mkv",
    ".avi",
    ".m4v",
    ".mpeg",
    ".mpg",
    ".ogv",
    ".wmv",
    ".flv",
    ".3gp",
    ".3g2",
    ".m2ts",
    ".mts",
    ".vob",
    ".f4v",
    ".asf",
    ".rm",
    ".rmvb",
    ".mxf",
}
MAX_MARKDOWN_BYTES = 1_000_000
MAX_IMAGE_BYTES = 10_000_000
MAX_IMAGE_PIXELS = 20_000_000
MAX_IMAGE_DIMENSION = 8_000
MAX_VIDEO_SCAN_BYTES = 1_000_000
COMMONMARK = MarkdownIt("commonmark")
EBML_HEADER = b"\x1a\x45\xdf\xa3"
ASF_HEADER = b"\x30\x26\xb2\x75\x8e\x66\xcf\x11"
ASF_VIDEO_MEDIA = b"\xc0\xef\x19\xbc\x4d\x5b\xcf\x11\xa8\xfd\x00\x80\x5f\x5c\x44\x2b"

def contains_html(tokens: list[Token]) -> bool:
    return any(
        token.type in {"html_block", "html_inline"}
        or contains_html(token.children or [])
        for token in tokens
    )


def plain_alt(image: Token) -> str:
    return "".join(
        token.content
        for token in image.children or []
        if token.type in {"text", "text_special", "code_inline"}
    )


def valid_https_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        _port = parsed.port
    except ValueError:
        return False
    return parsed.scheme == "https" and bool(parsed.hostname)


def valid_article_link(value: str) -> bool:
    return value.startswith("#") or valid_https_url(value)


def has_invalid_bare_link(tokens: list[Token]) -> bool:
    for parent in tokens:
        link_depth = 0
        for token in parent.children or []:
            if token.type == "link_open":
                link_depth += 1
            elif token.type == "link_close":
                link_depth -= 1
            elif token.type == "text" and link_depth == 0:
                if BARE_EMAIL_RE.search(token.content):
                    return True
                for match in BARE_EXTERNAL_URL_RE.finditer(token.content):
                    if not valid_article_link(match.group(0).rstrip(".,;:!?)]}")):
                        return True
    return False


def attribution_after(tokens: list[Token], inline_index: int) -> re.Match[str] | None:
    expected = ("paragraph_close", "paragraph_open", "inline", "paragraph_close")
    following = tokens[inline_index + 1 : inline_index + 5]
    if (
        len(following) != len(expected)
        or tuple(token.type for token in following) != expected
    ):
        return None
    inline = tokens[inline_index]
    attribution = following[2]
    if attribution.level != inline.level:
        return None
    children = attribution.children or []
    if [child.type for child in children] != ["em_open", "text", "em_close"]:
        return None
    return ATTRIBUTION_TEXT_RE.fullmatch(children[1].content)


def article_images(markdown: str) -> list[tuple[str, str, str, bool]]:
    tokens = COMMONMARK.parse(markdown)
    if contains_html(tokens):
        raise ValueError("원시 HTML은 허용하지 않습니다")
    if any(
        token.type == "link_open"
        and not valid_article_link(str(token.attrGet("href") or ""))
        for parent in tokens
        for token in (parent.children or [])
    ):
        raise ValueError("링크는 문서 내부 앵커 또는 유효한 HTTPS URL이어야 합니다")
    if has_invalid_bare_link(tokens):
        raise ValueError(
            "bare 외부 URL과 이메일 주소는 허용하지 않으며 HTTPS 링크를 사용해야 합니다"
        )

    images: list[tuple[str, str, str, bool]] = []
    for index, token in enumerate(tokens):
        if token.type != "inline":
            continue
        children = token.children or []
        image_tokens = [child for child in children if child.type == "image"]
        if not image_tokens:
            continue
        visible_children = [
            child for child in children if child.type != "text" or child.content.strip()
        ]
        if len(image_tokens) != 1 or visible_children != image_tokens:
            raise ValueError("사진은 문단에서 단독으로 사용해야 합니다")
        syntax = SINGLE_LINE_IMAGE_RE.fullmatch(token.content.strip())
        if not syntax:
            raise ValueError("사진은 한 줄 inline Markdown 문법만 사용할 수 있습니다")
        alt = plain_alt(image_tokens[0]).strip()
        if not alt:
            raise ValueError("사진 대체 텍스트가 비어 있습니다")
        attribution = attribution_after(tokens, index)
        attribution_valid = bool(
            attribution
            and attribution.group(1).strip()
            and valid_https_url(attribution.group(2))
            and attribution.group(3).strip()
        )
        images.append(
            (
                alt,
                (image_tokens[0].attrGet("src") or "").strip(),
                syntax.group(1).strip(),
                attribution_valid,
            )
        )
    return images


def relative_name(root: Path, candidate: Path) -> str:
    return candidate.relative_to(root).as_posix()


def has_annex_b_video(header: bytes) -> bool:
    for marker in (b"\x00\x00\x01", b"\x00\x00\x00\x01"):
        start = 0
        while (index := header.find(marker, start)) >= 0:
            nal_index = index + len(marker)
            if nal_index < len(header):
                nal = header[nal_index]
                if nal & 0x1F in {5, 7, 8} or (nal >> 1) & 0x3F in {19, 20, 32, 33, 34}:
                    return True
            start = nal_index + 1
    return False


def has_ogg_video(candidate: Path, offset: int = 0) -> bool:
    try:
        with candidate.open("rb") as stream:
            stream.seek(offset)
            while header := stream.read(27):
                if len(header) != 27 or not header.startswith(b"OggS"):
                    return False
                segment_table = stream.read(header[26])
                if len(segment_table) != header[26]:
                    return False
                body_size = sum(segment_table)
                body = stream.read(body_size)
                if len(body) != body_size:
                    return False
                if header[5] & 0x02 and body.startswith(
                    (b"\x80theora", b"OVP80", b"BBCD")
                ):
                    return True
    except OSError:
        return False
    return False


def leading_id3_size(header: bytes) -> int:
    if len(header) < 10 or not header.startswith(b"ID3"):
        return 0
    size_bytes = header[6:10]
    if any(value & 0x80 for value in size_bytes):
        return 0
    size = sum(value << shift for value, shift in zip(size_bytes, (21, 14, 7, 0)))
    return 10 + size + (10 if header[5] & 0x10 else 0)


def has_mpeg_transport_stream(data: bytes) -> bool:
    for packet_size in (188, 192, 204, 208):
        offset = data.find(b"\x47")
        while offset >= 0 and offset + packet_size * 4 + 4 <= len(data):
            valid = True
            for index in range(5):
                packet = offset + packet_size * index
                if data[packet] != 0x47 or data[packet + 1] & 0x80:
                    valid = False
                    break
                adaptation_control = (data[packet + 3] >> 4) & 0x03
                if adaptation_control == 0:
                    valid = False
                    break
                if adaptation_control in {2, 3} and data[packet + 4] > packet_size - 5:
                    valid = False
                    break
            if valid:
                return True
            offset = data.find(b"\x47", offset + 1)
    return False


def has_ebml_video_track(data: bytes) -> bool:
    def read_vint(offset: int, *, identifier: bool) -> tuple[int, int] | None:
        if offset >= len(data):
            return None
        first = data[offset]
        marker = 0x80
        length = 1
        while length <= 8 and not first & marker:
            marker >>= 1
            length += 1
        if length > 8 or offset + length > len(data):
            return None
        value = first if identifier else first & (marker - 1)
        for byte in data[offset + 1 : offset + length]:
            value = (value << 8) | byte
        return value, length

    segment_id = 0x18538067
    tracks_id = 0x1654AE6B
    track_entry_id = 0xAE
    track_type_id = 0x83

    def scan(start: int, end: int, context: int = 0) -> bool:
        offset = start
        while offset < end:
            identifier = read_vint(offset, identifier=True)
            if not identifier:
                return False
            element_id, id_length = identifier
            size_field = read_vint(offset + id_length, identifier=False)
            if not size_field:
                return False
            size, size_length = size_field
            payload_start = offset + id_length + size_length
            payload_end = (
                end
                if size == (1 << (7 * size_length)) - 1
                else payload_start + size
            )
            if payload_end > end:
                return False
            if (
                context == track_entry_id
                and element_id == track_type_id
                and 1 <= size <= 8
                and int.from_bytes(data[payload_start:payload_end], "big") == 1
            ):
                return True
            child_context = (
                element_id
                if element_id in {segment_id, tracks_id, track_entry_id}
                else 0
            )
            if child_context and scan(payload_start, payload_end, child_context):
                return True
            offset = payload_end
        return False

    return scan(0, len(data))


def has_exact_jpeg_container(payload: bytes) -> bool:
    if not payload.startswith(b"\xff\xd8"):
        return False
    offset = 2
    in_scan = False
    while offset < len(payload):
        if in_scan:
            marker_start = payload.find(b"\xff", offset)
            if marker_start < 0 or marker_start + 1 >= len(payload):
                return False
            marker_end = marker_start + 1
            while marker_end < len(payload) and payload[marker_end] == 0xFF:
                marker_end += 1
            if marker_end >= len(payload):
                return False
            marker = payload[marker_end]
            if marker == 0x00 or 0xD0 <= marker <= 0xD7:
                offset = marker_end + 1
                continue
            offset = marker_start
            in_scan = False
            continue

        if payload[offset] != 0xFF:
            return False
        marker_end = offset + 1
        while marker_end < len(payload) and payload[marker_end] == 0xFF:
            marker_end += 1
        if marker_end >= len(payload):
            return False
        marker = payload[marker_end]
        offset = marker_end + 1
        if marker == 0xD9:
            return offset == len(payload)
        if marker == 0x01 or marker == 0xD8 or 0xD0 <= marker <= 0xD7:
            continue
        if marker == 0x00 or offset + 2 > len(payload):
            return False
        segment_length = int.from_bytes(payload[offset : offset + 2], "big")
        if segment_length < 2 or offset + segment_length > len(payload):
            return False
        offset += segment_length
        if marker == 0xDA:
            in_scan = True
    return False


def has_video_iso_bmff_track(candidate: Path, start: int = 0) -> bool:
    containers = {b"moov", b"trak", b"mdia"}

    def scan_boxes(stream: BinaryIO, offset: int, end: int, depth: int) -> bool:
        while offset + 8 <= end:
            stream.seek(offset)
            header = stream.read(16)
            if len(header) < 8:
                return False
            size = int.from_bytes(header[:4], "big")
            box_type = header[4:8]
            header_size = 8
            if size == 1:
                if len(header) < 16:
                    return False
                size = int.from_bytes(header[8:16], "big")
                header_size = 16
            elif size == 0:
                size = end - offset
            if size < header_size or offset + size > end:
                return False
            payload_start = offset + header_size
            if box_type == b"hdlr" and size >= header_size + 12:
                stream.seek(payload_start + 8)
                if stream.read(4) == b"vide":
                    return True
            if box_type in containers and depth < 4 and scan_boxes(
                stream, payload_start, offset + size, depth + 1
            ):
                return True
            offset += size
        return False

    try:
        file_size = candidate.stat().st_size
        with candidate.open("rb") as stream:
            stream.seek(start)
            first_header = stream.read(8)
            if len(first_header) < 8 or first_header[4:8] != b"ftyp":
                return False
            return scan_boxes(stream, start, file_size, 0)
    except OSError:
        return False


def is_video_file(candidate: Path) -> bool:
    media_type, _encoding = mimetypes.guess_type(candidate.name)
    if candidate.suffix.lower() in VIDEO_EXTENSIONS or bool(
        media_type and media_type.startswith("video/")
    ):
        return True
    if candidate.is_symlink() or not candidate.is_file():
        return False
    if candidate.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS and is_valid_image_file(
        candidate
    ):
        return False
    try:
        with candidate.open("rb") as stream:
            prefix = stream.read(10)
            scan_offset = leading_id3_size(prefix)
            stream.seek(scan_offset)
            header = stream.read(MAX_VIDEO_SCAN_BYTES + 416)
    except OSError:
        return False
    if header.startswith(b"OggS"):
        return has_ogg_video(candidate, scan_offset)
    if header.startswith(EBML_HEADER):
        return has_ebml_video_track(header)
    if header.startswith(ASF_HEADER):
        return ASF_VIDEO_MEDIA in header
    return (
        has_video_iso_bmff_track(candidate, scan_offset)
        or (header.startswith(b"RIFF") and header[8:12] == b"AVI ")
        or header.startswith(
            (
                b"DKIF",
                b"FLV",
                b".RMF",
                b"\x00\x00\x01\xba",
                b"\x00\x00\x01\xb3",
                b"\x06\x0e\x2b\x34\x02\x05\x01\x01\x0d\x01\x02",
            )
        )
        or has_annex_b_video(header[:512])
        or has_mpeg_transport_stream(header)
    )


def is_valid_image_file(candidate: Path) -> bool:
    expected = {
        ".png": "PNG",
        ".jpg": "JPEG",
        ".jpeg": "JPEG",
        ".webp": "WEBP",
    }
    try:
        if candidate.stat().st_size > MAX_IMAGE_BYTES:
            return False
        payload = candidate.read_bytes()
        suffix = candidate.suffix.lower()
        if suffix == ".png":
            offset = 8
            if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
                return False
            while offset + 12 <= len(payload):
                chunk_length = int.from_bytes(payload[offset : offset + 4], "big")
                chunk_type = payload[offset + 4 : offset + 8]
                offset += 12 + chunk_length
                if offset > len(payload):
                    return False
                if chunk_type == b"IEND":
                    if chunk_length != 0 or offset != len(payload):
                        return False
                    break
            else:
                return False
        elif suffix in {".jpg", ".jpeg"}:
            if not has_exact_jpeg_container(payload):
                return False
        elif suffix == ".webp":
            if (
                len(payload) < 12
                or payload[:4] != b"RIFF"
                or payload[8:12] != b"WEBP"
                or int.from_bytes(payload[4:8], "little") + 8 != len(payload)
            ):
                return False
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(candidate) as image:
                width, height = image.size
                if (
                    width > MAX_IMAGE_DIMENSION
                    or height > MAX_IMAGE_DIMENSION
                    or width * height > MAX_IMAGE_PIXELS
                ):
                    return False
                image.load()
                return image.format == expected.get(candidate.suffix.lower())
    except (
        OSError,
        UnidentifiedImageError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ):
        return False


def validate_article(
    root: Path, article: Path, referenced_images: set[Path] | None = None
) -> list[str]:
    errors: list[str] = []
    name = relative_name(root, article)
    path_match = ARTICLE_PATH_RE.fullmatch(name)
    if not path_match:
        return [f"{name}: 기사 경로 계약을 따르지 않습니다"]
    if article.is_symlink():
        return [f"{name}: 기사 심볼릭 링크는 허용하지 않습니다"]
    if article.stat().st_size > MAX_MARKDOWN_BYTES:
        return [f"{name}: Markdown 크기가 {MAX_MARKDOWN_BYTES}바이트를 초과합니다"]

    try:
        markdown = article.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{name}: Markdown은 UTF-8이어야 합니다"]
    frontmatter_match = FRONTMATTER_RE.match(markdown)
    slug_match = (
        SLUG_RE.search(frontmatter_match.group(1)) if frontmatter_match else None
    )
    slug = slug_match.group(1) if slug_match else ""
    if slug != path_match.group(1):
        errors.append(f"{name}: front matter slug와 파일명이 일치하지 않습니다")
    try:
        body = markdown[frontmatter_match.end() :] if frontmatter_match else markdown
        images = article_images(body)
    except ValueError as error:
        return [*errors, f"{name}: {error}"]

    for _alt, destination, raw_destination, attribution_valid in images:
        bracketed = raw_destination.startswith("<") and raw_destination.endswith(">")
        if (
            not bracketed and any(character.isspace() for character in raw_destination)
        ) or any(marker in destination for marker in ("?", "#")):
            errors.append(
                f"{name}: 사진 경로에 공백, 쿼리 또는 프래그먼트를 사용할 수 없습니다"
            )
            continue

        if re.search(r"%(?![0-9A-Fa-f]{2})", raw_destination) or re.search(
            r"%(?![0-9A-Fa-f]{2})", destination
        ):
            errors.append(f"{name}: 사진 경로의 percent encoding이 잘못됐습니다")
            continue
        try:
            decoded = unquote(destination, encoding="utf-8", errors="strict")
        except UnicodeDecodeError:
            errors.append(
                f"{name}: 사진 경로는 올바른 UTF-8 percent encoding을 사용해야 합니다"
            )
            continue
        if re.search(r"%(?![0-9A-Fa-f]{2})", decoded):
            errors.append(
                f"{name}: 정규화한 사진 경로의 percent encoding이 잘못됐습니다"
            )
            continue
        parts = decoded.split("/")
        if (
            len(parts) != 3
            or parts[:2] != [".", slug]
            or not parts[-1]
            or "\\" in decoded
            or "\0" in decoded
        ):
            errors.append(f"{name}: 사진 경로는 ./{slug}/<file> 형식이어야 합니다")
            continue
        image = article.parent / slug / parts[-1]
        if referenced_images is not None:
            referenced_images.add(image)
        if image.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            errors.append(f"{name}: 사진 형식은 webp, jpg, jpeg 또는 png여야 합니다")
        elif not image.is_file() or image.is_symlink():
            errors.append(
                f"{name}: 참조한 사진 파일이 없거나 심볼릭 링크입니다: {decoded}"
            )
        elif not is_valid_image_file(image):
            errors.append(
                f"{relative_name(root, image)}: 확장자와 일치하는 유효한 사진 파일이 아닙니다"
            )
        if not attribution_valid:
            errors.append(
                f"{name}: 각 사진 바로 다음에 제작자·HTTPS 출처·라이선스를 표시해야 합니다"
            )

    return errors


def validate_repository(root: Path, base: Path | None = None) -> list[str]:
    errors: list[str] = []
    news = root / "news"
    if not news.is_dir() or news.is_symlink():
        return ["news 디렉터리가 없거나 심볼릭 링크입니다"]
    previously_published_images = {
        existing.relative_to(base)
        for existing in (base / "news").rglob("*")
        if existing.is_file()
        and not existing.is_symlink()
        and existing.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS
    } if base and (base / "news").is_dir() else set()

    for candidate in root.rglob("*"):
        relative = candidate.relative_to(root)
        if ".git" in relative.parts:
            continue
        if is_video_file(candidate) and (candidate.is_file() or candidate.is_symlink()):
            errors.append(f"{relative.as_posix()}: 동영상 파일은 저장할 수 없습니다")

    referenced_images: set[Path] = set()
    for article in news.rglob("*"):
        if article.suffix.lower() != ".md":
            continue
        if article.is_file() and not article.is_symlink():
            errors.extend(validate_article(root, article, referenced_images))

    for candidate in news.rglob("*"):
        if candidate.is_symlink():
            errors.append(
                f"{relative_name(root, candidate)}: 심볼릭 링크는 허용하지 않습니다"
            )
            continue
        if not candidate.is_file():
            continue
        suffix = candidate.suffix.lower()
        if suffix == ".md" or is_video_file(candidate):
            continue
        elif suffix in ALLOWED_IMAGE_EXTENSIONS:
            media_parts = candidate.relative_to(news).parts
            if len(media_parts) != 5:
                errors.append(
                    f"{relative_name(root, candidate)}: 사진은 기사 slug와 같은 이름의 디렉터리 바로 아래에 저장해야 합니다"
                )
                continue
            if not is_valid_image_file(candidate):
                errors.append(
                    f"{relative_name(root, candidate)}: 확장자와 일치하는 유효한 사진 파일이 아닙니다"
                )
            article = candidate.parent.parent / f"{candidate.parent.name}.md"
            if not article.is_file():
                errors.append(
                    f"{relative_name(root, candidate)}: 대응하는 기사 파일이 없습니다"
                )
            elif (
                candidate not in referenced_images
                and candidate.relative_to(root) not in previously_published_images
            ):
                errors.append(
                    f"{relative_name(root, candidate)}: 대응하는 기사에서 참조하지 않은 사진입니다"
                )
        else:
            errors.append(
                f"{relative_name(root, candidate)}: 기사 미디어 디렉터리에는 webp, jpg, jpeg 또는 png만 저장할 수 있습니다"
            )

    return list(dict.fromkeys(errors))


def validate_immutable_media(base: Path, candidate: Path) -> list[str]:
    errors: list[str] = []
    base_news = base / "news"
    if not base_news.is_dir():
        return errors
    for existing in base_news.rglob("*"):
        if not existing.is_file() or existing.is_symlink():
            continue
        if existing.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            continue
        relative = existing.relative_to(base)
        proposed = candidate / relative
        if not proposed.is_file() or proposed.is_symlink():
            errors.append(f"{relative.as_posix()}: 발행된 사진은 삭제할 수 없습니다")
        elif not cmp(existing, proposed, shallow=False):
            errors.append(
                f"{relative.as_posix()}: 발행된 사진은 같은 경로에서 덮어쓸 수 없습니다"
            )
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve(strict=True)
    base = Path(sys.argv[2]).resolve(strict=True) if len(sys.argv) > 2 else None
    errors = validate_repository(root, base)
    if base:
        errors.extend(validate_immutable_media(base, root))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("공개 콘텐츠 계약 검증을 통과했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
