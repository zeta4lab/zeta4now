from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from check_content import validate_repository


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
---
# 오늘의 AI 소식

{image}

{attribution}
"""

    def test_accepts_local_image_with_attribution(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        image = article.parent / "2026-08-13-ai-daily/data-center.webp"
        image.parent.mkdir()
        image.write_bytes(b"image")
        article.write_text(
            self.article(
                "![데이터센터 전경](./2026-08-13-ai-daily/data-center.webp)",
                "*사진: 직접 제작 · 출처: https://example.com/photo · 라이선스: CC BY 4.0*",
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(root), [])

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
            any("inline Markdown" in error for error in validate_repository(root))
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
            any("사진 경로" in error for error in validate_repository(root))
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
            any("미디어 태그" in error for error in validate_repository(root))
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

    def test_rejects_media_after_invalid_fence_opener(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article("``` bad`\n![외부 사진](https://example.com/photo.png)\n```"),
            encoding="utf-8",
        )
        self.assertTrue(
            any("사진 경로" in error for error in validate_repository(root))
        )

    def test_rejects_media_after_unclosed_code_span(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article("`unclosed ![외부 사진](https://example.com/photo.png) ``"),
            encoding="utf-8",
        )
        self.assertTrue(
            any("사진 경로" in error for error in validate_repository(root))
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
            any("사진 경로" in error for error in validate_repository(root))
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

    def test_rejects_raw_svg_media(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article('<svg><image href="https://example.com/photo.png"/></svg>'),
            encoding="utf-8",
        )
        self.assertTrue(
            any("미디어 태그" in error for error in validate_repository(root))
        )

    def test_rejects_video_outside_news(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        video = root / "assets/movie.mp4"
        video.parent.mkdir()
        video.write_bytes(b"video")
        self.assertTrue(
            any("동영상 파일" in error for error in validate_repository(root))
        )

    def test_rejects_additional_video_extensions(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        for filename in ("movie.wmv", "movie.flv", "movie.3gp"):
            video = root / "assets" / filename
            video.parent.mkdir(exist_ok=True)
            video.write_bytes(b"video")
        errors = validate_repository(root)
        self.assertEqual(sum("동영상 파일" in error for error in errors), 3)


if __name__ == "__main__":
    unittest.main()
