from __future__ import annotations

import mimetypes
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ARTICLE_PATH_RE = re.compile(r"^news/[^/]+/\d{4}/\d{2}/([^/]+)\.md$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n")
SLUG_RE = re.compile(r"^slug:\s*([^\s]+)\s*$", re.MULTILINE)
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]\r\n]*)\]\(([^)\r\n]+)\)")
IMAGE_OPEN_RE = re.compile(r"!\[")
IMAGE_ATTRIBUTION_RE = re.compile(
    r"\A[ \t]*\r?\n(?:[ \t]*\r?\n)?[ \t]*\*사진:\s*([^·\r\n]+?)\s*·\s*"
    r"출처:\s*(https://[^\s*]+)\s*·\s*라이선스:\s*([^*\r\n]+?)\*[ \t]*(?:\r?\n|\Z)"
)
RAW_MEDIA_TAG_RE = re.compile(
    r"<\s*/?\s*(?:img|iframe|video|audio|object|embed|source|svg|image|use|foreignObject)\b",
    re.IGNORECASE,
)
ALLOWED_IMAGE_EXTENSIONS = {".webp", ".jpg", ".jpeg", ".png"}
UNSUPPORTED_IMAGE_EXTENSIONS = {".svg", ".gif", ".avif", ".bmp", ".tif", ".tiff"}
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
}
MAX_MARKDOWN_BYTES = 1_000_000
BLOCKQUOTE_PREFIX_RE = re.compile(r"^[ ]{0,3}>[ ]?")
LIST_MARKER_RE = re.compile(r"^[ ]{0,3}(?:[-+*]|\d{1,9}[.)])([ \t]+)")


def mask_range(characters: list[str], start: int, end: int) -> None:
    for index in range(start, end):
        if characters[index] not in {"\r", "\n"}:
            characters[index] = " "


def strip_blockquote_prefixes(content: str) -> tuple[str, int]:
    depth = 0
    while match := BLOCKQUOTE_PREFIX_RE.match(content):
        content = content[match.end() :]
        depth += 1
    return content, depth


def fence_view(
    content: str, list_indent: int, *, update_list: bool
) -> tuple[str, int, int]:
    view, blockquote_depth = strip_blockquote_prefixes(content)
    if update_list:
        marker = LIST_MARKER_RE.match(view)
        if marker:
            return view[marker.end() :], marker.end(), blockquote_depth
    leading_spaces = len(view) - len(view.lstrip(" "))
    if list_indent and leading_spaces >= list_indent:
        return view[list_indent:], list_indent, blockquote_depth
    if update_list and view.strip():
        list_indent = 0
    return view, list_indent, blockquote_depth


def without_markdown_code(markdown: str) -> str:
    characters = list(markdown)
    offset = 0
    fence_character = ""
    fence_length = 0
    list_indent = 0
    fence_blockquote_depth = 0
    fence_list_indent = 0
    for line in markdown.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        container_view, blockquote_depth = strip_blockquote_prefixes(content)
        container_indentation = len(container_view) - len(container_view.lstrip(" "))
        left_container = bool(fence_character) and (
            blockquote_depth < fence_blockquote_depth
            or (
                fence_list_indent
                and bool(container_view.strip())
                and container_indentation < fence_list_indent
            )
        )
        if left_container:
            fence_character = ""
            fence_length = 0
            fence_blockquote_depth = 0
            fence_list_indent = 0
        view, list_indent, blockquote_depth = fence_view(
            content, list_indent, update_list=not fence_character
        )
        stripped = view.lstrip(" ")
        indentation = len(view) - len(stripped)
        backtick_opening = (
            re.fullmatch(r"(`{3,})[^`]*", stripped) if indentation <= 3 else None
        )
        tilde_opening = (
            re.fullmatch(r"(~{3,}).*", stripped) if indentation <= 3 else None
        )
        opening = backtick_opening or tilde_opening
        closing = (
            re.fullmatch(
                rf"{re.escape(fence_character)}{{{fence_length},}}[ \t]*", stripped
            )
            if fence_character and indentation <= 3
            else None
        )
        if fence_character:
            mask_range(characters, offset, offset + len(line))
            if closing:
                fence_character = ""
                fence_length = 0
                fence_blockquote_depth = 0
                fence_list_indent = 0
        elif opening:
            fence = opening.group(1)
            fence_character = fence[0]
            fence_length = len(fence)
            fence_blockquote_depth = blockquote_depth
            fence_list_indent = list_indent
            mask_range(characters, offset, offset + len(line))
        offset += len(line)

    masked = "".join(characters)
    characters = list(masked)
    index = 0
    while index < len(masked):
        if masked[index] != "`" or is_escaped(masked, index):
            index += 1
            continue
        end = index
        while end < len(masked) and masked[end] == "`":
            end += 1
        delimiter_length = end - index
        search = end
        closing_index = -1
        closing_end = -1
        while search < len(masked):
            candidate = masked.find("`", search)
            if candidate < 0:
                break
            candidate_end = candidate
            while candidate_end < len(masked) and masked[candidate_end] == "`":
                candidate_end += 1
            if candidate_end - candidate == delimiter_length:
                closing_index = candidate
                closing_end = candidate_end
                break
            search = candidate_end
        if closing_index < 0:
            index = end
            continue
        mask_range(characters, index, closing_end)
        index = closing_end
    return "".join(characters)


def is_escaped(markdown: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and markdown[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def relative_name(root: Path, candidate: Path) -> str:
    return candidate.relative_to(root).as_posix()


def markdown_images(markdown: str) -> tuple[list[tuple[str, str, int]], list[int]]:
    images = [
        (match.group(1), match.group(2), match.end())
        for match in MARKDOWN_IMAGE_RE.finditer(markdown)
        if not is_escaped(markdown, match.start())
    ]
    valid_starts = {
        match.start()
        for match in MARKDOWN_IMAGE_RE.finditer(markdown)
        if not is_escaped(markdown, match.start())
    }
    unsupported = [
        match.start()
        for match in IMAGE_OPEN_RE.finditer(markdown)
        if not is_escaped(markdown, match.start()) and match.start() not in valid_starts
    ]
    return images, unsupported


def is_video_file(candidate: Path) -> bool:
    media_type, _encoding = mimetypes.guess_type(candidate.name)
    return candidate.suffix.lower() in VIDEO_EXTENSIONS or bool(
        media_type and media_type.startswith("video/")
    )


def validate_article(root: Path, article: Path) -> list[str]:
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
    media_markdown = without_markdown_code(markdown)
    if RAW_MEDIA_TAG_RE.search(media_markdown):
        errors.append(f"{name}: 원시 미디어 태그나 임베드는 허용하지 않습니다")

    images, unsupported_images = markdown_images(media_markdown)
    if unsupported_images:
        errors.append(f"{name}: 사진은 한 줄 inline Markdown 문법만 사용할 수 있습니다")

    for raw_alt, raw_destination, image_end in images:
        alt = raw_alt.strip()
        destination = raw_destination.strip()
        bracketed = destination.startswith("<") and destination.endswith(">")
        if bracketed:
            destination = destination[1:-1]
        if not alt:
            errors.append(f"{name}: 사진 대체 텍스트가 비어 있습니다")
        if (
            not bracketed and any(character.isspace() for character in destination)
        ) or any(marker in destination for marker in ("?", "#")):
            errors.append(
                f"{name}: 사진 경로에 공백, 쿼리 또는 프래그먼트를 사용할 수 없습니다"
            )
            continue

        if re.search(r"%(?![0-9A-Fa-f]{2})", destination):
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
        if image.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            errors.append(f"{name}: 사진 형식은 webp, jpg, jpeg 또는 png여야 합니다")
        elif not image.is_file() or image.is_symlink():
            errors.append(
                f"{name}: 참조한 사진 파일이 없거나 심볼릭 링크입니다: {decoded}"
            )
        attribution = IMAGE_ATTRIBUTION_RE.match(media_markdown[image_end:])
        if (
            not attribution
            or not attribution.group(1).strip()
            or not attribution.group(3).strip()
        ):
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

    for candidate in news.rglob("*"):
        if candidate.is_symlink():
            errors.append(
                f"{relative_name(root, candidate)}: 심볼릭 링크는 허용하지 않습니다"
            )
            continue
        if not candidate.is_file():
            continue
        suffix = candidate.suffix.lower()
        if suffix == ".md":
            errors.extend(validate_article(root, candidate))
        elif is_video_file(candidate):
            continue
        elif suffix in UNSUPPORTED_IMAGE_EXTENSIONS:
            errors.append(
                f"{relative_name(root, candidate)}: 지원하지 않는 사진 형식입니다"
            )
        elif suffix in ALLOWED_IMAGE_EXTENSIONS:
            article = candidate.parent.parent / f"{candidate.parent.name}.md"
            if not article.is_file():
                errors.append(
                    f"{relative_name(root, candidate)}: 대응하는 기사 파일이 없습니다"
                )

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve(strict=True)
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("공개 콘텐츠 계약 검증을 통과했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
