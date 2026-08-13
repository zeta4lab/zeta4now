from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ARTICLE_PATH_RE = re.compile(r"^news/[^/]+/\d{4}/\d{2}/([^/]+)\.md$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n")
SLUG_RE = re.compile(r"^slug:\s*([^\s]+)\s*$", re.MULTILINE)
MARKDOWN_IMAGE_RE = re.compile(r"(?<!\\)!\[([^\]\r\n]*)\]\(([^)\r\n]+)\)")
REFERENCE_IMAGE_RE = re.compile(r"(?<!\\)!\[([^\]\r\n]*)\]\[([^\]\r\n]*)\]")
SHORTCUT_IMAGE_RE = re.compile(r"(?<![\\\]])!\[([^\]\r\n]+)\](?![\[(])")
REFERENCE_DEFINITION_RE = re.compile(
    r"^[ \t]{0,3}\[([^\]\r\n]+)\]:[ \t]*(?:<([^>\r\n]+)>|([^\s]+))"
    r'(?:[ \t]+(?:"[^"\r\n]*"|\'[^\'\r\n]*\'|\([^\)\r\n]*\)))?[ \t]*$',
    re.MULTILINE,
)
IMAGE_ATTRIBUTION_RE = re.compile(
    r"\A[ \t]*\r?\n(?:[ \t]*\r?\n)?[ \t]*\*사진:\s*([^·\r\n]+?)\s*·\s*"
    r"출처:\s*(https://[^\s*]+)\s*·\s*라이선스:\s*([^*\r\n]+?)\*[ \t]*(?:\r?\n|\Z)"
)
RAW_MEDIA_TAG_RE = re.compile(
    r"<\s*/?\s*(?:img|iframe|video|audio|object|embed|source)\b", re.IGNORECASE
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
}
MAX_MARKDOWN_BYTES = 1_000_000


def relative_name(root: Path, candidate: Path) -> str:
    return candidate.relative_to(root).as_posix()


def markdown_images(markdown: str) -> list[tuple[str, str | None, int]]:
    definitions: dict[str, str] = {}
    for match in REFERENCE_DEFINITION_RE.finditer(markdown):
        label = match.group(1).strip().casefold()
        destination = (
            f"<{match.group(2)}>" if match.group(2) is not None else match.group(3)
        )
        if destination:
            definitions[label] = destination

    images = [
        (match.group(1), match.group(2), match.end())
        for match in MARKDOWN_IMAGE_RE.finditer(markdown)
    ]
    for match in REFERENCE_IMAGE_RE.finditer(markdown):
        alt = match.group(1)
        label = match.group(2).strip() or alt.strip()
        images.append((alt, definitions.get(label.casefold()), match.end()))
    for match in SHORTCUT_IMAGE_RE.finditer(markdown):
        alt = match.group(1)
        images.append((alt, definitions.get(alt.strip().casefold()), match.end()))
    return sorted(images, key=lambda image: image[2])


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
    if RAW_MEDIA_TAG_RE.search(markdown):
        errors.append(f"{name}: 원시 미디어 태그나 임베드는 허용하지 않습니다")

    for raw_alt, raw_destination, image_end in markdown_images(markdown):
        alt = raw_alt.strip()
        destination = (raw_destination or "").strip()
        bracketed = destination.startswith("<") and destination.endswith(">")
        if bracketed:
            destination = destination[1:-1]
        if not alt:
            errors.append(f"{name}: 사진 대체 텍스트가 비어 있습니다")
        if not destination:
            errors.append(f"{name}: 참조형 사진의 경로 정의가 없습니다")
            continue
        if (
            not bracketed and any(character.isspace() for character in destination)
        ) or any(marker in destination for marker in ("?", "#")):
            errors.append(
                f"{name}: 사진 경로에 공백, 쿼리 또는 프래그먼트를 사용할 수 없습니다"
            )
            continue

        decoded = unquote(destination)
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
        if not IMAGE_ATTRIBUTION_RE.match(markdown[image_end:]):
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
        if candidate.suffix.lower() in VIDEO_EXTENSIONS and (
            candidate.is_file() or candidate.is_symlink()
        ):
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
        elif suffix in VIDEO_EXTENSIONS:
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
