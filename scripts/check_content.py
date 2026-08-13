from __future__ import annotations

import mimetypes
import re
import sys
from filecmp import cmp
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token

ARTICLE_PATH_RE = re.compile(r"^news/[^/]+/\d{4}/\d{2}/([^/]+)\.md$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n")
SLUG_RE = re.compile(r"^slug:\s*([^\s]+)\s*$", re.MULTILINE)
SINGLE_LINE_IMAGE_RE = re.compile(r"^!\[(?:\\.|[^\]\\\r\n])*\]\(((?:\\.|[^\r\n])*)\)$")
ATTRIBUTION_TEXT_RE = re.compile(
    r"^사진:\s*(.*?)\s*·\s*출처:\s*(https://\S+)\s*·\s*라이선스:\s*(.*?)$"
)
BARE_EXTERNAL_URL_RE = re.compile(r"(?i)(?<![\w])(?:(?:https?|ftp):)?//[^\s<]+")
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
COMMONMARK = MarkdownIt("commonmark")


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
        raise ValueError("본문의 bare 외부 URL은 HTTPS를 사용해야 합니다")

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


def is_video_file(candidate: Path) -> bool:
    media_type, _encoding = mimetypes.guess_type(candidate.name)
    if candidate.suffix.lower() in VIDEO_EXTENSIONS or bool(
        media_type and media_type.startswith("video/")
    ):
        return True
    if candidate.is_symlink() or not candidate.is_file():
        return False
    try:
        with candidate.open("rb") as stream:
            header = stream.read(512)
    except OSError:
        return False
    return (
        (len(header) >= 12 and header[4:8] == b"ftyp")
        or (header.startswith(b"RIFF") and header[8:12] == b"AVI ")
        or header.startswith(
            (
                b"\x1a\x45\xdf\xa3",
                b"FLV",
                b"OggS",
                b".RMF",
                b"\x30\x26\xb2\x75\x8e\x66\xcf\x11",
                b"\x00\x00\x01\xba",
                b"\x00\x00\x01\xb3",
                b"\x06\x0e\x2b\x34\x02\x05\x01\x01\x0d\x01\x02",
            )
        )
        or (len(header) > 376 and header[0] == header[188] == header[376] == 0x47)
        or (len(header) > 388 and header[4] == header[196] == header[388] == 0x47)
    )


def is_valid_image_file(candidate: Path) -> bool:
    try:
        with candidate.open("rb") as stream:
            header = stream.read(16)
    except OSError:
        return False
    suffix = candidate.suffix.lower()
    if suffix == ".png":
        return header.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix in {".jpg", ".jpeg"}:
        return header.startswith(b"\xff\xd8\xff")
    return suffix == ".webp" and header.startswith(b"RIFF") and header[8:12] == b"WEBP"


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

        if re.search(r"%(?![0-9A-Fa-f]{2})", raw_destination):
            errors.append(f"{name}: 사진 경로의 percent encoding이 잘못됐습니다")
            continue
        try:
            decoded = unquote(destination, encoding="utf-8", errors="strict")
        except UnicodeDecodeError:
            errors.append(
                f"{name}: 사진 경로는 올바른 UTF-8 percent encoding을 사용해야 합니다"
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


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    news = root / "news"
    if not news.is_dir() or news.is_symlink():
        return ["news 디렉터리가 없거나 심볼릭 링크입니다"]

    for candidate in root.rglob("*"):
        relative = candidate.relative_to(root)
        if ".git" in relative.parts:
            continue
        if is_video_file(candidate) and (candidate.is_file() or candidate.is_symlink()):
            errors.append(f"{relative.as_posix()}: 동영상 파일은 저장할 수 없습니다")

    referenced_images: set[Path] = set()
    for article in news.rglob("*.md"):
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
            elif candidate not in referenced_images:
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
        if (
            proposed.is_file()
            and not proposed.is_symlink()
            and not cmp(existing, proposed, shallow=False)
        ):
            errors.append(
                f"{relative.as_posix()}: 발행된 사진은 같은 경로에서 덮어쓸 수 없습니다"
            )
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve(strict=True)
    errors = validate_repository(root)
    if len(sys.argv) > 2:
        base = Path(sys.argv[2]).resolve(strict=True)
        errors.extend(validate_immutable_media(base, root))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("공개 콘텐츠 계약 검증을 통과했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
