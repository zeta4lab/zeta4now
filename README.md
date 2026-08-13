# zeta4now

`zeta4now`는 [Zeta4 Now](https://now.zeta4.net)가 공개하는 소식 문서의 원본 저장소다.
문서는 Markdown과 YAML front matter로 관리한다.

## 문서 위치

```text
news/<topic>/<YYYY>/<MM>/<slug>.md
```

자동 생성 문서는 다음 값을 반드시 포함한다.

- `title`: 제목
- `slug`: 저장소 전체에서 고유한 문서 식별자
- `topic`: 검색·분류에 사용하는 영문 소문자 또는 한글 식별자
- `published_at`: 시간대가 포함된 ISO 8601 발행 시각
- `summary`: 목록에 표시할 요약
- `tags`: 선택 태그 목록
- `generated_by`: 생성 자동화 식별자
- `model`: 생성 모델

본문 끝에는 `## 출처`와 원문 링크, AI 자동 생성 고지를 둔다. 구체적인 형식은
[`templates/article.md`](templates/article.md)를 따른다.

## 사진과 동영상

사진은 기사 파일 옆의 `<slug>/` 디렉터리에 저장하고 Markdown 상대경로로 참조한다.

```text
news/ai/2026/08/2026-08-13-ai-daily.md
news/ai/2026/08/2026-08-13-ai-daily/data-center.webp
```

```markdown
![데이터센터 전경](./2026-08-13-ai-daily/data-center.webp)
```

동영상 파일은 저장하지 않으며 공식 원문으로 연결되는 HTTPS 링크만 사용한다. 사진의 사용 조건과
세부 규칙은 [`MEDIA_POLICY.md`](MEDIA_POLICY.md)를 따른다.

## 발행 흐름

1. 비공개 `zeta4s`가 정해진 시각에 생성 작업을 실행한다.
2. 비공개 자동화가 Gemini Google Search grounding 결과를 Markdown으로 만들고 검증한다.
3. 검증된 파일만 이 저장소의 `main` 브랜치에 발행한다.
4. GitHub webhook이 조회·검색 서비스에 변경을 알리고 D1 검색 색인을 갱신한다.

이 저장소에는 API 키, 토큰, 실행 로그를 저장하지 않는다.
