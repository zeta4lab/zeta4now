from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from check_content import validate_immutable_media, validate_repository

PNG_BYTES = b"\x89PNG\r\n\x1a\n"
WEBP_BYTES = b"RIFF\x04\x00\x00\x00WEBP"


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
        image.write_bytes(WEBP_BYTES)
        article.write_text(
            self.article(
                "![데이터센터 전경](./2026-08-13-ai-daily/data-center.webp)",
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

    def test_rejects_bare_http_url(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(
            self.article("관련 영상은 http://example.com/video 에서 확인합니다."),
            encoding="utf-8",
        )
        self.assertTrue(any("HTTPS" in error for error in validate_repository(root)))

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
        for source in ("https:///", "https://?", "https://example.com:bad/"):
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
        for filename in ("movie.wmv", "movie.flv", "movie.3gp", "movie.mxf"):
            video = root / "assets" / filename
            video.parent.mkdir(exist_ok=True)
            video.write_bytes(b"video")
        errors = validate_repository(root)
        self.assertEqual(sum("동영상 파일" in error for error in errors), 4)

    def test_rejects_video_content_with_disguised_extensions(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        mp4_header = b"\x00\x00\x00\x18ftypisom\x00\x00\x00\x00isom"
        outside = root / "assets/movie.bin"
        outside.parent.mkdir()
        outside.write_bytes(mp4_header)
        disguised_image = article.parent / "2026-08-13-ai-daily/movie.png"
        disguised_image.parent.mkdir()
        disguised_image.write_bytes(mp4_header)
        errors = validate_repository(root)
        self.assertEqual(sum("동영상 파일" in error for error in errors), 2)

    def test_rejects_disguised_mpeg_transport_stream(self) -> None:
        temporary, root, article = self.repository()
        self.addCleanup(temporary.cleanup)
        article.write_text(self.article(), encoding="utf-8")
        packet = bytearray(377)
        packet[0] = packet[188] = packet[376] = 0x47
        video = root / "assets/movie.bin"
        video.parent.mkdir()
        video.write_bytes(packet)
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


if __name__ == "__main__":
    unittest.main()
