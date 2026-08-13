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


if __name__ == "__main__":
    unittest.main()
