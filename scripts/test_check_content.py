from __future__ import annotations

import tempfile
import unittest
from base64 import b64decode
from io import BytesIO
from pathlib import Path

from check_content import validate_immutable_media, validate_repository
from PIL import Image

PNG_BYTES = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)
WEBP_BYTES = b64decode("UklGRiIAAABXRUJQVlA4IBYAAAAwAQCdASoBAAEADsD+JaQAA3AAAAAA")
VIDEO_BMFF_BYTES = (
    b"\x00\x00\x00\x14ftypisom\x00\x00\x00\x00isom"
    b"\x00\x00\x00\x14hdlr\x00\x00\x00\x00\x00\x00\x00\x00vide"
)


def mpeg_ts(packet_size: int, stream_type: int = 0x1B) -> bytes:
    packets = bytearray(b"\xff" * (packet_size * 5))

    def write_packet(index: int, pid: int, payload: bytes) -> None:
        offset = packet_size * index
        packets[offset : offset + 4] = bytes(
            (0x47, 0x40 | (pid >> 8), pid & 0xFF, 0x10)
        )
        packets[offset + 4 : offset + 5 + len(payload)] = b"\x00" + payload

    pat = b"\x00\xb0\x0d\x00\x01\xc1\x00\x00\x00\x01\xe1\x00\x00\x00\x00\x00"
    pmt = (
        b"\x02\xb0\x12\x00\x01\xc1\x00\x00\xe1\x01\xf0\x00"
        + bytes((stream_type, 0xE1, 0x01, 0xF0, 0x00))
        + b"\x00\x00\x00\x00"
    )
    write_packet(0, 0, pat)
    write_packet(1, 0x100, pmt)
    for index in range(2, 5):
        offset = packet_size * index
        packets[offset : offset + 4] = b"\x47\x01\x01\x10"
    return bytes(packets)


class ContentContractTest(unittest.TestCase):
    def repository(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        article = root / "news/ai/2026/08/2026-08-13-ai-daily.md"
        article.parent.mkdir(parents=True)
        return temporary, root, article

    def article(self, image: str = "", attribution: str = "") -> str:
        return f"""---
title: 오늘의 AI 소식
slug: 2026-08-13-ai-daily
topic: ai
published_at: 2026-08-13T06:00:00+09:00
summary: 요약
generated_by: manual
model: none
---
# 오늘의 AI 소식

{image}

{attribution}

## 출처

- [원문](https://example.com/source)
"""

    def test_accepts_local_image_with_attribution(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/data-center.webp"
        image.parent.mkdir()
        image.write_bytes(WEBP_BYTES)
        article.write_text(
            self.article(
                "![데이터센터 전경](./2026-08-13-ai-daily/data-center.webp)",
                "*사진: 직접 제작 · 출처: https://example.com/photo · 라이선스: CC BY 4.0*",
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_accepts_quoted_slug_with_yaml_comment(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article().replace(
                "slug: 2026-08-13-ai-daily",
                'slug: "2026-08-13-ai-daily" # 공개 식별자',
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_rejects_duplicate_slugs_across_articles(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        duplicate = root / "news/security/2026/08/2026-08-13-ai-daily.md"
        duplicate.parent.mkdir(parents=True)
        duplicate.write_text(
            self.article().replace("topic: ai", "topic: security"),
            encoding="utf-8",
        )
        self.assertTrue(any("중복" in error for error in validate_repository(root)))

    def test_accepts_uppercase_https_image_attribution(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/data-center.webp"
        image.parent.mkdir()
        image.write_bytes(WEBP_BYTES)
        article.write_text(
            self.article(
                "![데이터센터 전경](./2026-08-13-ai-daily/data-center.webp)",
                "*사진: 직접 제작 · 출처: HTTPS://example.com/photo · 라이선스: CC BY 4.0*",
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_accepts_jpeg_with_structurally_parsed_end_marker(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/photo.jpg"
        image.parent.mkdir()
        Image.new("RGB", (1, 1)).save(image, format="JPEG")
        article.write_text(
            self.article(
                "![사진](./2026-08-13-ai-daily/photo.jpg)",
                "*사진: 직접 제작 · 출처: https://example.com/photo · 라이선스: CC BY 4.0*",
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_accepts_bracketed_image_path_with_parentheses(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/photo(1).png"
        image.parent.mkdir()
        image.write_bytes(PNG_BYTES)
        article.write_text(
            self.article(
                "![데이터센터 전경](<./2026-08-13-ai-daily/photo(1).png>)",
                "*사진: 직접 제작 · 출처: https://example.com/photo · 라이선스: CC BY 4.0*",
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_accepts_image_title_separate_from_path(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/data-center.webp"
        image.parent.mkdir()
        image.write_bytes(WEBP_BYTES)
        article.write_text(
            self.article(
                '![데이터센터 전경](./2026-08-13-ai-daily/data-center.webp "캡션")',
                "*사진: 직접 제작 · 출처: https://example.com/photo · 라이선스: CC BY 4.0*",
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_rejects_entity_encoded_path_traversal(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article(
                "![사진](./2026-08-13-ai-daily/dummy&#47;..&#47;..&#47;other.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("사진 경로" in error for error in validate_repository(root))
        )

    def test_rejects_every_unlisted_media_extension(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        media = article.parent / "2026-08-13-ai-daily/photo.heic"
        media.parent.mkdir()
        media.write_bytes(b"image")
        self.assertTrue(
            any(
                "webp, jpg, jpeg 또는 png" in error
                for error in validate_repository(root)
            )
        )

    def test_rejects_nested_article_media(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        nested = article.parent / "2026-08-13-ai-daily/archive/photo.svg"
        nested.parent.mkdir(parents=True)
        nested.write_bytes(b"<svg></svg>")
        self.assertTrue(
            any(
                "webp, jpg, jpeg 또는 png" in error
                for error in validate_repository(root)
            )
        )

    def test_rejects_non_image_bytes_with_allowed_extension(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/photo.png"
        image.parent.mkdir()
        image.write_bytes(b"<svg xmlns='http://www.w3.org/2000/svg'></svg>")
        article.write_text(
            self.article(
                "![사진](./2026-08-13-ai-daily/photo.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("유효한 사진" in error for error in validate_repository(root))
        )

    def test_rejects_png_prefix_followed_by_non_image_data(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/photo.png"
        image.parent.mkdir()
        image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x18ftypisom")
        article.write_text(
            self.article(
                "![사진](./2026-08-13-ai-daily/photo.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("유효한 사진" in error for error in validate_repository(root))
        )

    def test_rejects_valid_image_with_appended_video(self) -> None:
        jpeg = BytesIO()
        Image.new("RGB", (1, 1)).save(jpeg, format="JPEG")
        video = VIDEO_BMFF_BYTES
        for extension, payload in (
            ("png", PNG_BYTES),
            ("jpg", jpeg.getvalue() + video + b"\xff\xd9"),
            ("webp", WEBP_BYTES),
        ):
            with self.subTest(extension=extension):
                temporary, root, article = self.repository()
                try:
                    image = article.parent / f"2026-08-13-ai-daily/polyglot.{extension}"
                    image.parent.mkdir()
                    image.write_bytes(payload + (b"" if extension == "jpg" else video))
                    article.write_text(
                        self.article(
                            f"![사진](./2026-08-13-ai-daily/polyglot.{extension})",
                            "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
                        ),
                        encoding="utf-8",
                    )
                    self.assertTrue(
                        any(
                            "유효한 사진" in error
                            for error in validate_repository(root)
                        )
                    )
                finally:
                    temporary.cleanup()

    def test_rejects_image_over_pixel_limit_before_full_decode(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/oversized.png"
        image.parent.mkdir()
        Image.new("1", (5_000, 5_000)).save(image)
        article.write_text(
            self.article(
                "![대형 사진](./2026-08-13-ai-daily/oversized.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("유효한 사진" in error for error in validate_repository(root))
        )

    def test_rejects_animated_png(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/animated.png"
        image.parent.mkdir()
        frames = [Image.new("RGBA", (1, 1), color) for color in ("red", "blue")]
        frames[0].save(
            image,
            format="PNG",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
        )
        article.write_text(
            self.article(
                "![애니메이션](./2026-08-13-ai-daily/animated.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("유효한 사진" in error for error in validate_repository(root))
        )

    def test_rejects_animated_image_outside_news(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        image = root / "assets/animated.webp"
        image.parent.mkdir()
        frames = [Image.new("RGBA", (1, 1), color) for color in ("red", "blue")]
        frames[0].save(
            image,
            format="WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
        )
        self.assertTrue(
            any(
                "assets/animated.webp" in error and "정적 사진" in error
                for error in validate_repository(root)
            )
        )

    def test_rejects_unreferenced_image(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/unused.png"
        image.parent.mkdir()
        image.write_bytes(PNG_BYTES)
        article.write_text(self.article(), encoding="utf-8")
        self.assertTrue(
            any("참조하지 않은" in error for error in validate_repository(root))
        )

    def test_rejects_external_reference_style_image(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article(
                "![외부 사진][hero]",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*\n\n"
                "[hero]: https://example.com/photo.png",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("inline Markdown" in error for error in validate_repository(root))
        )

    def test_uses_first_duplicate_reference_definition(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/local.webp"
        image.parent.mkdir()
        image.write_bytes(b"image")
        article.write_text(
            self.article(
                "![외부 사진][hero]",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*\n\n"
                "[hero]: https://example.com/photo.png\n"
                "[hero]: ./2026-08-13-ai-daily/local.webp",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("inline Markdown" in error for error in validate_repository(root))
        )

    def test_collapses_reference_label_whitespace(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/local.webp"
        image.parent.mkdir()
        image.write_bytes(b"image")
        article.write_text(
            self.article(
                "![외부 사진][hero image]",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*\n\n"
                "[hero  image]: https://example.com/photo.png\n"
                "[hero image]: ./2026-08-13-ai-daily/local.webp",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("inline Markdown" in error for error in validate_repository(root))
        )

    def test_rejects_multiline_inline_image(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article("![외부 사진](\nhttps://example.com/photo.png\n)"),
            encoding="utf-8",
        )
        self.assertTrue(
            any("inline Markdown" in error for error in validate_repository(root))
        )

    def test_rejects_non_https_video_link(self) -> None:
        for url in (
            "http://www.youtube.com/watch?v=example",
            "//www.youtube.com/watch?v=example",
            "ftp://example.com/video.mp4",
        ):
            with self.subTest(url=url):
                temporary, root, article = self.repository()
                try:
                    article.write_text(
                        self.article(f"[관련 영상]({url})"), encoding="utf-8"
                    )
                    self.assertTrue(
                        any("HTTPS" in error for error in validate_repository(root))
                    )
                finally:
                    temporary.cleanup()

    def test_rejects_unsafe_gfm_bare_url(self) -> None:
        for url in ("http://example.com/video", "www.example.com/video"):
            with self.subTest(url=url):
                temporary, root, article = self.repository()
                try:
                    article.write_text(
                        self.article(f"관련 영상은 {url} 에서 확인합니다."),
                        encoding="utf-8",
                    )
                    self.assertTrue(
                        any("HTTPS" in error for error in validate_repository(root))
                    )
                finally:
                    temporary.cleanup()

    def test_rejects_bare_email_autolink(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article("문의: editor@example.com"), encoding="utf-8")
        self.assertTrue(any("HTTPS" in error for error in validate_repository(root)))

    def test_rejects_uppercase_markdown_extension(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        uppercase = article.with_suffix(".MD")
        uppercase.write_text(self.article(), encoding="utf-8")
        self.assertTrue(
            any("기사 경로" in error for error in validate_repository(root))
        )

    def test_allows_document_anchor(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article("[현재 문서의 출처로 이동](#출처)"), encoding="utf-8"
        )
        self.assertEqual(validate_repository(root), [])

    def test_ignores_reference_definitions_inside_html_blocks(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article(
                "<!-- [hero]: ./2026-08-13-ai-daily/local.webp -->\n"
                "![외부 사진][hero]\n"
                "[hero]: https://example.com/photo.png"
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("원시 HTML" in error for error in validate_repository(root))
        )

    def test_rejects_external_image_after_even_backslashes(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article(
                r"\\![외부 사진](https://example.com/photo.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("문단에서 단독" in error for error in validate_repository(root))
        )

    def test_rejects_image_without_attribution(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/data-center.webp"
        image.parent.mkdir()
        image.write_bytes(b"image")
        article.write_text(
            self.article("![데이터센터 전경](./2026-08-13-ai-daily/data-center.webp)"),
            encoding="utf-8",
        )
        self.assertTrue(any("제작자" in error for error in validate_repository(root)))

    def test_rejects_whitespace_only_attribution(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/data-center.webp"
        image.parent.mkdir()
        image.write_bytes(b"image")
        article.write_text(
            self.article(
                "![데이터센터 전경](./2026-08-13-ai-daily/data-center.webp)",
                "*사진:   · 출처: https://example.com/photo · 라이선스:   *",
            ),
            encoding="utf-8",
        )
        self.assertTrue(any("제작자" in error for error in validate_repository(root)))

    def test_rejects_attribution_without_valid_https_host(self) -> None:
        for source in (
            "https:///",
            "https://?",
            "https://example.com:bad/",
            "https://%ZZ/",
            "https://bad_host.example/",
            "https://user@example.com/",
        ):
            with self.subTest(source=source):
                temporary, root, article = self.repository()
                try:
                    image = article.parent / "2026-08-13-ai-daily/photo.png"
                    image.parent.mkdir()
                    image.write_bytes(PNG_BYTES)
                    article.write_text(
                        self.article(
                            "![사진](./2026-08-13-ai-daily/photo.png)",
                            f"*사진: 제공자 · 출처: {source} · 라이선스: 허가됨*",
                        ),
                        encoding="utf-8",
                    )
                    self.assertTrue(
                        any(
                            "제작자" in error or "HTTPS" in error
                            for error in validate_repository(root)
                        )
                    )
                finally:
                    temporary.cleanup()

    def test_rejects_semantically_empty_alt(self) -> None:
        for alt in ("&#32;", "&nbsp;"):
            with self.subTest(alt=alt):
                temporary, root, article = self.repository()
                try:
                    image = article.parent / "2026-08-13-ai-daily/data-center.webp"
                    image.parent.mkdir()
                    image.write_bytes(b"image")
                    article.write_text(
                        self.article(
                            f"![{alt}](./2026-08-13-ai-daily/data-center.webp)",
                            "*사진: 직접 제작 · 출처: https://example.com/photo · 라이선스: CC BY 4.0*",
                        ),
                        encoding="utf-8",
                    )
                    self.assertTrue(
                        any(
                            "대체 텍스트" in error
                            for error in validate_repository(root)
                        )
                    )
                finally:
                    temporary.cleanup()

    def test_excludes_frontmatter_from_markdown_parsing(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        markdown = self.article(
            "![외부 사진](https://example.com/photo.png)",
            "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*\n\n`",
        ).replace("title: 오늘의 AI 소식", 'title: "`"')
        article.write_text(markdown, encoding="utf-8")
        self.assertTrue(
            any("사진 경로" in error for error in validate_repository(root))
        )

    def test_ignores_media_examples_in_code(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article(
                '`<img src="example.png">`\n\n```html\n<video src="example.mp4"></video>\n```'
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_does_not_mask_after_escaped_backtick(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article('\\`<img src="./photo.png">`'),
            encoding="utf-8",
        )
        self.assertTrue(
            any("원시 HTML" in error for error in validate_repository(root))
        )

    def test_keeps_four_space_fence_inside_code(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article('```html\n    ```\n<img src="./photo.png">\n```'),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_masks_fenced_code_inside_containers(self) -> None:
        for body in (
            '> ```html\n> <img src="./photo.png">\n> ```',
            '- 기술 예제\n\n    ```html\n    <video src="./video.mp4"></video>\n    ```',
        ):
            with self.subTest(body=body):
                temporary, root, article = self.repository()
                try:
                    article.write_text(self.article(body), encoding="utf-8")
                    self.assertEqual(validate_repository(root), [])
                finally:
                    temporary.cleanup()

    def test_stops_fence_after_leaving_container(self) -> None:
        for body in (
            '> ```html\n> 코드 예제\n<img src="./photo.png">',
            '- 기술 예제\n\n    ```html\n    코드 예제\n<img src="./photo.png">',
        ):
            with self.subTest(body=body):
                temporary, root, article = self.repository()
                try:
                    article.write_text(self.article(body), encoding="utf-8")
                    self.assertTrue(
                        any("원시 HTML" in error for error in validate_repository(root))
                    )
                finally:
                    temporary.cleanup()

    def test_rejects_media_after_invalid_fence_opener(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article("``` bad`\n![외부 사진](https://example.com/photo.png)\n```"),
            encoding="utf-8",
        )
        self.assertTrue(
            any("문단에서 단독" in error for error in validate_repository(root))
        )

    def test_rejects_media_after_unclosed_code_span(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article("`unclosed ![외부 사진](https://example.com/photo.png) ``"),
            encoding="utf-8",
        )
        self.assertTrue(
            any("문단에서 단독" in error for error in validate_repository(root))
        )

    def test_checks_indented_list_image(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article(
                "- 관련 사진\n    ![외부 사진](https://example.com/photo.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("문단에서 단독" in error for error in validate_repository(root))
        )

    def test_rejects_invalid_percent_encoding(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article(
                "![사진](./2026-08-13-ai-daily/photo%ZZ.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("percent encoding" in error for error in validate_repository(root))
        )

    def test_rejects_entity_encoded_invalid_percent_encoding(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article(
                "![사진](./2026-08-13-ai-daily/photo&#37;ZZ.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(
            any("percent encoding" in error for error in validate_repository(root))
        )

    def test_rejects_raw_svg_media(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article('<svg><image href="https://example.com/photo.png"/></svg>'),
            encoding="utf-8",
        )
        self.assertTrue(
            any("원시 HTML" in error for error in validate_repository(root))
        )

    def test_ignores_indented_code_media(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article(
                '    <img src="./photo.png">\n\n'
                "    ![외부 사진](https://example.com/photo.png)"
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_rejects_indented_attribution(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/data-center.webp"
        image.parent.mkdir()
        image.write_bytes(b"image")
        article.write_text(
            self.article(
                "![데이터센터 전경](./2026-08-13-ai-daily/data-center.webp)",
                "    *사진: 직접 제작 · 출처: https://example.com/photo · 라이선스: CC BY 4.0*",
            ),
            encoding="utf-8",
        )
        self.assertTrue(any("제작자" in error for error in validate_repository(root)))

    def test_rejects_all_raw_html(self) -> None:
        for body in (
            '<input type="image" src="./2026-08-13-ai-daily/photo.png">',
            '<div style="background-image: url(./photo.png)">사진</div>',
            '<span data-label="`example`">![사진](https://example.com/photo.png)</span>',
        ):
            with self.subTest(body=body):
                temporary, root, article = self.repository()
                try:
                    article.write_text(self.article(body), encoding="utf-8")
                    self.assertTrue(
                        any("원시 HTML" in error for error in validate_repository(root))
                    )
                finally:
                    temporary.cleanup()

    def test_rejects_video_outside_news(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        video = root / "assets/movie.mpg"
        video.parent.mkdir()
        video.write_bytes(b"video")
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_additional_video_extensions(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        for filename in (
            "movie.wmv",
            "movie.flv",
            "movie.mpg",
            "movie.mxf",
            "movie.h264",
            "movie.264",
            "movie.avc",
            "movie.h265",
            "movie.265",
            "movie.hevc",
            "movie.m4v",
            "movie.mjpeg",
            "movie.mjpg",
        ):
            video = root / "assets" / filename
            video.parent.mkdir(exist_ok=True)
            video.write_bytes(b"video")
        errors = validate_repository(root)
        self.assertEqual(sum("동영상 파일" in error for error in errors), 13)

    def test_rejects_animated_gif_outside_news(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        image = root / "assets/animated.gif"
        image.parent.mkdir()
        frames = [Image.new("RGB", (1, 1), color) for color in ("red", "blue")]
        frames[0].save(
            image,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
        )
        self.assertTrue(
            any(
                "assets/animated.gif" in error and "사진 형식" in error
                for error in validate_repository(root)
            )
        )

    def test_rejects_video_content_with_disguised_extensions(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        mp4_header = VIDEO_BMFF_BYTES
        outside = root / "assets/movie.bin"
        outside.parent.mkdir()
        outside.write_bytes(mp4_header)
        disguised_image = article.parent / "2026-08-13-ai-daily/movie.png"
        disguised_image.parent.mkdir()
        disguised_image.write_bytes(mp4_header)
        errors = validate_repository(root)
        self.assertEqual(sum("동영상 파일" in error for error in errors), 2)

    def test_rejects_non_fast_start_bmff_video_after_large_media_box(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")

        def box(kind: bytes, payload: bytes) -> bytes:
            return (len(payload) + 8).to_bytes(4, "big") + kind + payload

        leading_free = box(b"free", b"metadata")
        ftyp = box(b"ftyp", b"isom\x00\x00\x00\x00isom")
        mdat = box(b"mdat", bytes(1_100_000))
        hdlr = box(b"hdlr", bytes(8) + b"vide")
        moov = box(b"moov", box(b"trak", box(b"mdia", hdlr)))
        video = root / "assets/movie.bin"
        video.parent.mkdir()
        video.write_bytes(leading_free + ftyp + mdat + moov)
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_legacy_quicktime_video_without_ftyp(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")

        def box(kind: bytes, payload: bytes) -> bytes:
            return (len(payload) + 8).to_bytes(4, "big") + kind + payload

        hdlr = box(b"hdlr", bytes(8) + b"vide")
        video = root / "assets/movie.mov"
        video.parent.mkdir()
        video.write_bytes(box(b"moov", box(b"trak", box(b"mdia", hdlr))))
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_disguised_mpeg_transport_stream(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        video = root / "assets/movie.bin"
        video.parent.mkdir()
        video.write_bytes(mpeg_ts(188))
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_disguised_204_byte_mpeg_transport_stream(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        video = root / "assets/movie.bin"
        video.parent.mkdir()
        video.write_bytes(mpeg_ts(204))
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_allows_audio_only_mpeg_transport_stream(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        audio = root / "assets/podcast.ts"
        audio.parent.mkdir()
        audio.write_bytes(mpeg_ts(188, stream_type=0x0F))
        self.assertFalse(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_does_not_classify_three_sync_like_packets_as_transport_stream(
        self,
    ) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        binary = root / "assets/data.bin"
        binary.parent.mkdir()
        binary.write_bytes(mpeg_ts(188)[: 188 * 3])
        self.assertFalse(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_transport_stream_beyond_large_id3_metadata(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        metadata_size = 1_100_000
        synchsafe_size = bytes(
            (
                (metadata_size >> 21) & 0x7F,
                (metadata_size >> 14) & 0x7F,
                (metadata_size >> 7) & 0x7F,
                metadata_size & 0x7F,
            )
        )
        video = root / "assets/movie.bin"
        video.parent.mkdir()
        video.write_bytes(
            b"ID3\x04\x00\x00" + synchsafe_size + bytes(metadata_size) + mpeg_ts(188)
        )
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_disguised_ivf_video(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        video = root / "assets/movie.bin"
        video.parent.mkdir()
        video.write_bytes(b"DKIF" + bytes(28))
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_distinguishes_ogg_audio_from_disguised_ogg_video(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        assets = root / "assets"
        assets.mkdir()

        def ogg_page(packet: bytes) -> bytes:
            return b"OggS\x00\x02" + bytes(20) + b"\x01" + bytes([len(packet)]) + packet

        (assets / "podcast.ogg").write_bytes(ogg_page(b"OpusHead"))
        (assets / "movie.bin").write_bytes(ogg_page(b"\x80theora"))
        (assets / "multiplexed.dat").write_bytes(
            ogg_page(b"OpusHead") + ogg_page(b"\x80theora")
        )
        errors = validate_repository(root)
        self.assertEqual(sum("동영상 파일" in error for error in errors), 2)
        self.assertTrue(any("movie.bin" in error for error in errors))
        self.assertTrue(any("multiplexed.dat" in error for error in errors))

    def test_reassembles_continued_ogg_identification_packet(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        video = root / "assets/movie.bin"
        video.parent.mkdir()

        def ogg_page(
            header_type: int, sequence: int, lacing: bytes, body: bytes
        ) -> bytes:
            return (
                b"OggS\x00"
                + bytes([header_type])
                + bytes(8)
                + (7).to_bytes(4, "little")
                + sequence.to_bytes(4, "little")
                + bytes(4)
                + bytes([len(lacing)])
                + lacing
                + body
            )

        first = b"\x80theora" + bytes(248)
        second = b"continued packet"
        video.write_bytes(
            ogg_page(0x02, 0, b"\xff", first)
            + ogg_page(0x01, 1, bytes([len(second)]), second)
        )
        self.assertTrue(
            any("movie.bin" in error for error in validate_repository(root))
        )

    def test_distinguishes_audio_and_video_in_ebml_and_asf(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        assets = root / "assets"
        assets.mkdir()

        def ebml_element(identifier: bytes, payload: bytes) -> bytes:
            size = len(payload)
            length = 1
            while size >= (1 << (7 * length)) - 1:
                length += 1
            encoded_size = (size | (1 << (7 * length))).to_bytes(length, "big")
            return identifier + encoded_size + payload

        def ebml_file(track_type: bytes, codec_private: bytes = b"") -> bytes:
            track = ebml_element(b"\x83", track_type)
            if codec_private:
                track += ebml_element(b"\x63\xa2", codec_private)
            entry = ebml_element(b"\xae", track)
            tracks = ebml_element(b"\x16\x54\xae\x6b", entry)
            segment = ebml_element(b"\x18\x53\x80\x67", tracks)
            return ebml_element(b"\x1a\x45\xdf\xa3", b"") + segment

        asf = b"\x30\x26\xb2\x75\x8e\x66\xcf\x11\xa6\xd9\x00\xaa\x00\x62\xce\x6c"
        stream_properties = (
            b"\x91\x07\xdc\xb7\xb7\xa9\xcf\x11\x8e\xe6\x00\xc0\x0c\x20\x53\x65"
        )
        audio_guid = b"\x40\x9e\x69\xf8\x4d\x5b\xcf\x11\xa8\xfd\x00\x80\x5f\x5c\x44\x2b"
        video_guid = b"\xc0\xef\x19\xbc\x4d\x5b\xcf\x11\xa8\xfd\x00\x80\x5f\x5c\x44\x2b"

        def asf_object(identifier: bytes, payload: bytes) -> bytes:
            return identifier + (len(payload) + 24).to_bytes(8, "little") + payload

        def asf_file(objects: list[bytes]) -> bytes:
            payload = (
                len(objects).to_bytes(4, "little") + b"\x01\x02" + b"".join(objects)
            )
            return asf + (len(payload) + 24).to_bytes(8, "little") + payload

        (assets / "podcast.webm").write_bytes(
            ebml_file(b"\x02", b"arbitrary\x83\x81\x01metadata")
        )
        (assets / "movie.bin").write_bytes(ebml_file(b"\x00\x01"))
        (assets / "podcast.asf").write_bytes(
            asf_file(
                [
                    asf_object(stream_properties, audio_guid),
                    asf_object(bytes(16), b"cover" + video_guid),
                ]
            )
        )
        (assets / "recording.dat").write_bytes(
            asf_file([asf_object(stream_properties, video_guid)])
        )
        errors = validate_repository(root)
        self.assertEqual(sum("동영상 파일" in error for error in errors), 2)
        self.assertTrue(any("movie.bin" in error for error in errors))
        self.assertTrue(any("recording.dat" in error for error in errors))

    def test_rejects_missing_or_invalid_required_front_matter(self) -> None:
        cases = {
            "title": "title: 오늘의 AI 소식\n",
            "topic": "topic: ai\n",
            "summary": "summary: 요약\n",
            "generated_by": "generated_by: manual\n",
            "model": "model: none\n",
            "published_at": "published_at: 2026-08-13T06:00:00+09:00\n",
        }
        source = self.article()
        for field, line in cases.items():
            with self.subTest(field=field):
                temporary, root, article = self.repository()
                try:
                    article.write_text(source.replace(line, ""), encoding="utf-8")
                    self.assertTrue(
                        any(field in error for error in validate_repository(root))
                    )
                finally:
                    temporary.cleanup()

    def test_rejects_uppercase_topic_identifier(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article().replace("topic: ai", "topic: AI"), encoding="utf-8"
        )
        self.assertTrue(any("topic" in error for error in validate_repository(root)))

    def test_rejects_topic_that_differs_from_path(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article().replace("topic: ai", "topic: security"), encoding="utf-8"
        )
        self.assertTrue(
            any("topic과 news" in error for error in validate_repository(root))
        )

    def test_rejects_invalid_year_and_month_directories(self) -> None:
        for year, month in (("0000", "08"), ("2026", "00"), ("2026", "13")):
            with self.subTest(year=year, month=month):
                temporary = tempfile.TemporaryDirectory()
                try:
                    root = Path(temporary.name)
                    article = (
                        root / "news" / "ai" / year / month / "2026-08-13-ai-daily.md"
                    )
                    article.parent.mkdir(parents=True)
                    article.write_text(self.article(), encoding="utf-8")
                    self.assertTrue(
                        any(
                            "기사 경로 계약" in error
                            for error in validate_repository(root)
                        )
                    )
                finally:
                    temporary.cleanup()

    def test_rejects_missing_source_footer(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article().replace(
                "\n## 출처\n\n- [원문](https://example.com/source)\n", "\n"
            ),
            encoding="utf-8",
        )
        self.assertTrue(any("## 출처" in error for error in validate_repository(root)))

    def test_rejects_generated_article_without_ai_disclosure(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article().replace("generated_by: manual", "generated_by: generator"),
            encoding="utf-8",
        )
        self.assertTrue(any("## 출처" in error for error in validate_repository(root)))

    def test_accepts_crlf_source_footer_and_ai_disclosure(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        markdown = self.article().replace(
            "generated_by: manual", "generated_by: generator"
        )
        markdown += (
            "\n---\n\n이 글은 공개 출처를 바탕으로 AI가 자동 생성했으며, "
            "중요한 판단 전에는 연결된 원문을 확인해야 합니다.\n"
        )
        article.write_bytes(markdown.replace("\n", "\r\n").encode())
        self.assertEqual(validate_repository(root), [])

    def test_rejects_content_after_source_footer(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article() + "\n## 뒤늦은 본문\n\n추가 내용\n", encoding="utf-8"
        )
        self.assertTrue(any("## 출처" in error for error in validate_repository(root)))

    def test_rejects_body_content_nested_inside_source_item(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article().replace(
                "- [원문](https://example.com/source)",
                "- [원문](https://example.com/source)\n\n  ## 숨긴 본문\n\n  추가 내용",
            ),
            encoding="utf-8",
        )
        self.assertTrue(any("## 출처" in error for error in validate_repository(root)))

    def test_ignores_source_heading_text_inside_fenced_code(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article("```markdown\n## 출처\n```"), encoding="utf-8")
        self.assertEqual(validate_repository(root), [])

    def test_accepts_nested_brackets_in_image_alt(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/data-center.webp"
        image.parent.mkdir()
        image.write_bytes(WEBP_BYTES)
        article.write_text(
            self.article(
                "![데이터 [센터]](./2026-08-13-ai-daily/data-center.webp)",
                "*사진: 직접 제작 · 출처: https://example.com/photo · 라이선스: CC BY 4.0*",
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

    def test_rejects_blockquoted_source_heading(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article().replace("## 출처", "> ## 출처"), encoding="utf-8"
        )
        self.assertTrue(any("## 출처" in error for error in validate_repository(root)))

    def test_parses_ebml_tracks_beyond_bounded_signature_scan(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")

        def element(identifier: bytes, payload: bytes) -> bytes:
            size = len(payload)
            length = 1
            while size >= (1 << (7 * length)) - 1:
                length += 1
            encoded_size = (size | (1 << (7 * length))).to_bytes(length, "big")
            return identifier + encoded_size + payload

        track_type = element(b"\x83", b"\x01")
        entry = element(b"\xae", track_type)
        tracks = element(b"\x16\x54\xae\x6b", entry)
        segment = element(
            b"\x18\x53\x80\x67", element(b"\xec", bytes(1_100_000)) + tracks
        )
        video = root / "assets/movie.bin"
        video.parent.mkdir()
        video.write_bytes(element(b"\x1a\x45\xdf\xa3", b"") + segment)
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_yuv4mpeg_stream(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        video = root / "assets/movie.bin"
        video.parent.mkdir()
        video.write_bytes(b"YUV4MPEG2 W1 H1 F1:1 Ip A1:1 Cmono\nFRAME\n\x00")
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_allows_non_video_iso_bmff_brands_outside_news(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        assets = root / "assets"
        assets.mkdir()
        (assets / "audio.bin").write_bytes(
            b"\x00\x00\x00\x18ftypM4A \x00\x00\x00\x00M4A mp42"
        )
        (assets / "image.bin").write_bytes(
            b"\x00\x00\x00\x18ftypavif\x00\x00\x00\x00avifmif1"
        )
        (assets / "generic-audio.bin").write_bytes(
            b"\x00\x00\x00\x14ftypisom\x00\x00\x00\x00isom"
            b"\x00\x00\x00\x14hdlr\x00\x00\x00\x00\x00\x00\x00\x00soun"
        )
        (assets / "podcast.mp4").write_bytes(
            b"\x00\x00\x00\x14ftypisom\x00\x00\x00\x00isom"
            b"\x00\x00\x00\x14hdlr\x00\x00\x00\x00\x00\x00\x00\x00soun"
        )
        self.assertFalse(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_allows_incidental_annex_b_parameter_set_bytes(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        binary = root / "assets/data.bin"
        binary.parent.mkdir()
        binary.write_bytes(b"metadata\x00\x00\x00\x01\x67\x64\x00\x1f")
        self.assertFalse(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_coherent_raw_h264_stream(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        video = root / "assets/movie.bin"
        video.parent.mkdir()
        video.write_bytes(
            b"\x00\x00\x00\x01\x09\xf0"
            b"\x00\x00\x00\x01\x67\x64\x00\x1f"
            b"\x00\x00\x00\x01\x68\xee\x3c\x80"
            b"\x00\x00\x00\x01\x65\x88\x84"
        )
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_overwriting_published_image(self) -> None:
        base_temporary, base, base_article = self.repository()
        candidate_temporary, candidate, candidate_article = self.repository()
        self.addCleanup(base_temporary.cleanup)
        self.addCleanup(candidate_temporary.cleanup)
        relative = Path("news/ai/2026/08/2026-08-13-ai-daily/photo.png")
        base_image = base / relative
        candidate_image = candidate / relative
        base_image.parent.mkdir()
        candidate_image.parent.mkdir()
        base_image.write_bytes(PNG_BYTES + b"old")
        candidate_image.write_bytes(PNG_BYTES + b"new")
        base_article.write_text(self.article(), encoding="utf-8")
        candidate_article.write_text(self.article(), encoding="utf-8")
        self.assertTrue(
            any(
                "덮어쓸 수 없습니다" in error
                for error in validate_immutable_media(base, candidate)
            )
        )

    def test_rejects_deleting_published_image(self) -> None:
        base_temporary, base, _base_article = self.repository()
        candidate_temporary, candidate, candidate_article = self.repository()
        self.addCleanup(base_temporary.cleanup)
        self.addCleanup(candidate_temporary.cleanup)
        relative = Path("news/ai/2026/08/2026-08-13-ai-daily/photo.png")
        base_image = base / relative
        base_image.parent.mkdir()
        base_image.write_bytes(PNG_BYTES)
        candidate_article.write_text(self.article(), encoding="utf-8")
        self.assertTrue(
            any(
                "삭제할 수 없습니다" in error
                for error in validate_immutable_media(base, candidate)
            )
        )

    def test_allows_retiring_published_image_from_article(self) -> None:
        base_temporary, base, base_article = self.repository()
        candidate_temporary, candidate, candidate_article = self.repository()
        self.addCleanup(base_temporary.cleanup)
        self.addCleanup(candidate_temporary.cleanup)
        relative = Path("news/ai/2026/08/2026-08-13-ai-daily/photo.png")
        base_image = base / relative
        candidate_image = candidate / relative
        base_image.parent.mkdir()
        candidate_image.parent.mkdir()
        base_image.write_bytes(PNG_BYTES)
        candidate_image.write_bytes(PNG_BYTES)
        base_article.write_text(
            self.article(
                "![사진](./2026-08-13-ai-daily/photo.png)",
                "*사진: 제공자 · 출처: https://example.com/photo · 라이선스: 허가됨*",
            ),
            encoding="utf-8",
        )
        candidate_article.write_text(self.article(), encoding="utf-8")
        self.assertEqual(validate_repository(candidate, base), [])
        self.assertEqual(validate_immutable_media(base, candidate), [])


if __name__ == "__main__":
    unittest.main()
