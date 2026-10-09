# zeta4now

`zeta4now`는 [Zeta4 Now](https://now.zeta4.net)가 공개하는 소식 문서의 원본 저장소다.
문서는 Markdown과 YAML front matter로 관리한다.

## 문서 위치

```text
news/<topic>/<YYYY>/<MM>/<slug>.md
```

모든 문서는 다음 값을 반드시 포함한다.

- `title`: 제목
- `slug`: 저장소 전체에서 고유한 문서 식별자
- `topic`: 검색·분류에 사용하는 영문 소문자 또는 한글 식별자
- `published_at`: 기사 경로의 연·월과 일치하며 시간대가 포함된 ISO 8601 발행 시각
- `summary`: 목록에 표시할 요약
- `tags`: 선택 태그 목록
- `generated_by`: 작성 주체(`claude`, `codex`, `gemini`, `manual` 또는 자동 생성기 `zeta4s`, `zeta4now-mcp`)
- `model`: 사용한 모델(`manual`이면 `none`)

본문 끝에는 `## 출처`와 원문 링크를 둔다. AI가 작성한 문서는 그 뒤에 고지를 붙인다. 데스크 발행 문서는
"검토해 발행" 고지를, 검토 없이 발행한 자동 생성 문서는 자동 생성 고지를 사용한다. 구체적인 형식은
[`templates/article.md`](templates/article.md)와 [`AGENTS.md`](AGENTS.md)를 따른다.

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

기본은 **데스크 발행**이다.

1. 사용자가 Claude, Codex, Gemini 같은 대화형 에이전트에게 기사를 지시한다.
2. 에이전트가 공개 출처를 조사해 초안을 대화로 제시하고, 사용자가 데스크(검토·수정)한다.
3. 승인된 초안만 파일로 만들어 검증하고 `desk/<slug>` 브랜치의 PR로 올린다.
4. 사용자가 PR을 승인하면 `Public content contract` 검사 통과 후 `main`에 merge한다.
5. GitHub webhook이 조회·검색 서비스에 변경을 알리고 D1 검색 색인을 갱신한다.

에이전트가 따르는 세부 절차는 [`AGENTS.md`](AGENTS.md)에 있다.

**자동 발행은 옵션**이다. 사용자가 지시한 경우에만 `zeta4now-mcp`나 비공개 `zeta4s` 정기 작업이 생성부터
발행까지 자동으로 수행한다.

이 저장소에는 API 키, 토큰, 실행 로그를 저장하지 않는다.
