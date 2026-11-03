---
title: 100만 토큰 컨텍스트는 기억이 아니다…압축은 완수율 뒤에 도구 호출 3배를 숨기고, 스스로 고친 스킬이 사람이 쓴 스킬을 60.7% 대 56.4%로 넘었다
slug: 2026-11-01-building-ai-agents-memory-context-skills
topic: ai
published_at: 2026-11-01T20:00:00+09:00
tags:
  - 에이전트 만들기
  - AI 에이전트
  - 컨텍스트 엔지니어링
  - 에이전트 메모리
  - Agent Skills
  - SkillsBench
summary: AI 에이전트를 만드는 7회 연재의 네 번째 편. 주요 모델의 컨텍스트가 100만 토큰이 됐지만 긴 컨텍스트는 정확도를 떨어뜨리고 매 단계 비용을 키운다. 도구 결과 비우기, 서버 압축, 파일 기반 외부 메모리의 공식 API를 비교하고, 압축이 완수율 대신 도구 호출을 늘린다는 측정, 파일과 grep이 그래프 메모리를 이긴 결과, 반복 작업을 '스킬'로 쌓을 때 자동 생성 스킬이 사람 큐레이션을 넘어선 Skill∞ 논문을 바탕으로 무엇을 기억하고 무엇을 버릴지 판단 기준을 정리한다.
generated_by: claude
model: unspecified
---

# 100만 토큰 컨텍스트는 기억이 아니다…압축은 완수율 뒤에 도구 호출 3배를 숨기고, 스스로 고친 스킬이 사람이 쓴 스킬을 60.7% 대 56.4%로 넘었다

## 한눈에 보기

[1회](https://now.zeta4.net/a/2026-10-29-building-ai-agents-system-not-model)에서 에이전트를 모델, 실행 틀, 작업 공간의 세 층으로 나눴고, [2회](https://now.zeta4.net/a/2026-10-30-building-ai-agents-cost-per-task)에서 에이전트 비용의 큰 몫이 매 단계 다시 넣는 입력이라는 점을 봤으며, [3회](https://now.zeta4.net/a/2026-10-31-building-ai-agents-function-calling-mcp-computer-use)에서 함수 호출·MCP·화면 조작으로 손발을 달았다. 이번 회는 그 입력, 곧 컨텍스트를 다루는 법이다. 질문은 셋이다. 컨텍스트가 100만 토큰이면 기억 문제가 사라지는가. 긴 과제에서 무엇을 버리고 무엇을 남기는가. 반복되는 작업 방법은 어디에 쌓는가.

결론부터 적는다. 첫째, 큰 컨텍스트는 기억을 대신하지 못한다. Anthropic 공식 문서가 "대화가 길어질수록 응답 품질이 떨어진다"고 직접 적고, OpenAI도 긴 대화에서 품질·비용·지연을 맞추는 수단으로 압축을 권하며, 100만 토큰을 쓰면 비용도 그만큼 든다. 둘째, 버리는 방법은 비우기, 압축, 외부 메모리 셋이고, 두 회사 API가 모두 이를 서버 기능으로 제공한다. 다만 8월 arXiv 논문은 압축이 완수율을 유지하면서도 에이전트가 잃어버린 상태를 다시 찾느라 도구 호출을 3배로 늘린 사례를 보고했다([arXiv](https://arxiv.org/abs/2608.16370)). 셋째, 작업 방법은 '스킬'이라는 파일 묶음으로 쌓는 것이 업계 표준이 됐다. 2월 벤치마크는 모델이 스스로 쓴 스킬이 평균적으로 도움이 안 된다고 했는데, 10월 26일 나온 Skill∞ 논문은 검증기로 돌린 자동 개선 스킬이 83개 과제에서 60.7%로 사람이 만든 스킬 56.4%를 넘었다고 보고했다([arXiv](https://arxiv.org/abs/2610.35434)). 두 결과의 차이가 만드는 사람에게 주는 교훈이 이 글의 마지막이다.

## 100만 토큰이 기본값이 됐지만

올해 주요 모델의 컨텍스트 창은 100만 토큰이 기본이 됐다. Anthropic 문서는 Opus 5.5, Sonnet 5.5, Haiku 5.5를 포함한 현행 모델 전부가 100만 토큰 컨텍스트를 갖고, 베타 헤더 없이 기본값이며, Haiku 5.5의 10만 토큰 초과 프롬프트를 빼면 표준 요금이라고 적었다([Claude Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)). OpenAI의 GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra 모델 페이지는 컨텍스트 창 105만 토큰, 최대 입력 92만 2천 토큰, 최대 출력 12만 8천 토큰을 적고, 입력이 27만 2천 토큰을 넘는 요청은 요청 전체에 입력·캐시 요금 2배, 출력 요금 1.5배를 매긴다고 밝혔다([OpenAI](https://developers.openai.com/api/docs/models/gpt-6.1-terra)).

| | Claude Opus 5.5·Sonnet 5.5·Haiku 5.5 | GPT-6 Astra·GPT-6.1 Sol·GPT-6.1 Terra |
|---|---|---|
| 컨텍스트 창 | 100만 토큰(기본값) | 105만 토큰(최대 입력 92만 2천) |
| 최대 출력 | 12만 8천 토큰 | 12만 8천 토큰 |
| 긴 컨텍스트 요금 | 표준 요금. Haiku 5.5만 10만 토큰 초과 시 할증 | 입력 27만 2천 토큰 초과 시 입력·캐시 2배, 출력 1.5배 |
| 공식 문서가 권하는 기본 전략 | 서버 압축(compaction) | 서버 압축(compaction) |

그런데 같은 문서들이 큰 컨텍스트를 채우지 말라고 말한다. Anthropic의 컨텍스트 창 문서는 "더 많은 컨텍스트가 자동으로 더 낫지는 않다"고 적고, 압축 문서는 "대화가 길어질수록 응답 품질이 떨어지므로" 활성 컨텍스트를 작게 유지하라고 설명한다([Claude Docs](https://platform.claude.com/docs/en/build-with-claude/compaction)). 근거는 두 가지다. 하나는 정확도다. Chroma가 2025년 7월 낸 기술 보고서는 GPT-4.1, Claude 4, Gemini 2.5, Qwen3 등 18개 모델을 시험해 "입력이 길어질수록 성능이 점점 신뢰하기 어려워진다"고 결론지었고([Chroma](https://research.trychroma.com/context-rot)), Anthropic 엔지니어링 블로그는 이를 '컨텍스트 부패(context rot)'라고 부르며 컨텍스트를 "한계 효용이 줄어드는 유한한 자원", 모델의 '주의 예산'으로 보라고 했다([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)). 다른 하나는 비용이다. 에이전트는 매 단계 지금까지의 컨텍스트 전부를 다시 입력으로 넣는다. 50만 토큰짜리 컨텍스트로 30단계를 돌면 입력만 1,500만 토큰이고, OpenAI 모델이라면 27만 2천 토큰을 넘는 순간부터 요금이 2배가 된다. 2회에서 본 과제당 비용이 여기서 결정된다.

그래서 큰 컨텍스트는 '한 번에 많이 읽어야 하는 일'에 쓰는 여유분이지, 긴 과제의 기억 장치가 아니다. 기억은 따로 설계해야 한다.

## 버리는 법 셋: 비우기, 압축, 외부 메모리

긴 과제에서 컨텍스트를 관리하는 방법은 결국 세 가지다. 오래된 도구 결과를 지우는 **비우기**, 앞부분을 요약으로 바꾸는 **압축**, 컨텍스트 밖 파일에 적어 두고 필요할 때 읽는 **외부 메모리**다. 두 회사 API가 셋을 어떻게 제공하는지 정리하면 이렇다.

| 방법 | Anthropic Claude API | OpenAI Responses API |
|---|---|---|
| 비우기 | 컨텍스트 편집(베타). `clear_tool_uses_20250919`가 임계값을 넘으면 오래된 도구 결과부터 자리 표시자로 바꾸고, `clear_thinking_20251015`가 이전 턴의 사고 블록을 정리한다 | 별도 기능 없음. 압축 항목 이전의 입력을 클라이언트가 버릴 수 있다 |
| 압축 | 서버 압축(베타). 요청형은 `compact-2026-09-04` 헤더로 원할 때 요약을 받아 교체하고, 임계값형은 `compact-2026-01-12` 헤더로 입력 토큰이 기본 15만(최소 5만)에 닿으면 요청 중간에 요약한다. 요약 프롬프트를 직접 쓸 수 있다 | `context_management`에 `compact_threshold`를 넣으면 서버가 임계값에서 압축 항목을 만들어 같은 스트림에 넣는다. 별도 `/responses/compact` 호출도 가능. 압축 항목은 암호화돼 사람이 읽을 수 없다 |
| 외부 메모리 | 메모리 도구 `memory_20250818`. 모델이 `/memories` 아래 파일의 생성·읽기·수정·삭제를 요청하고 실행은 내 애플리케이션이 한다. 경로 탈출 차단은 내 책임 | 별도 기능 없음. 함수 호출로 직접 만든다 |
| 캐시와의 관계 | 도구 결과를 지우면 그 지점부터 프롬프트 캐시가 깨진다. `clear_at_least`로 한 번에 충분히 지우라고 권한다 | 압축 항목 이전을 버리면 요청이 작아져 지연이 준다 |

출처: [컨텍스트 편집](https://platform.claude.com/docs/en/build-with-claude/context-editing), [압축 개요](https://platform.claude.com/docs/en/build-with-claude/compaction), [임계값 압축](https://platform.claude.com/docs/en/build-with-claude/compaction-threshold), [메모리 도구](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool), [OpenAI 압축 안내](https://developers.openai.com/api/docs/guides/compaction)

효과에 대한 숫자는 Anthropic이 2025년 9월 29일 컨텍스트 편집과 메모리 도구를 내며 낸 것이 있다. 에이전트 검색 내부 평가에서 메모리 도구와 컨텍스트 편집을 함께 쓰면 기준선보다 39%, 컨텍스트 편집만 쓰면 29% 성능이 올랐고, 100턴짜리 웹 검색 평가에서는 컨텍스트 편집 덕에 컨텍스트 고갈로 실패했을 작업을 끝내면서 토큰 사용을 84% 줄였다고 한다([Anthropic](https://www.anthropic.com/news/context-management)). 내부 평가 세트의 자체 측정이라 다른 업무에서 같은 폭이 나온다는 보장은 없다.

만드는 사람 입장에서 셋의 차이는 '무엇을 잃는가'다. 비우기는 도구 결과의 원문을 잃지만 대화 흐름과 모델의 결정은 남는다. Anthropic 블로그가 이를 "가장 안전하고 가벼운 압축"이라고 부르는 이유다. 압축은 모델이 쓴 요약만 남으므로 요약에서 빠진 것은 사라진다. 두 회사 모두 요약을 서버가 만들고, OpenAI 쪽은 그 내용을 들여다볼 수도 없다. 외부 메모리는 아무것도 잃지 않는 대신 모델이 언제 적고 언제 읽을지 스스로 정해야 하고, 그 판단이 틀리면 적어 둔 것을 안 읽는다.

## 압축의 숨은 비용: 완수율은 그대로, 도구 호출은 3배

압축을 평가할 때 흔히 과제 완수율만 본다. 8월 17일 arXiv에 올라온 단독 저자 논문 'What Does Context Compression Cost an Agent?'는 그 지표가 놓치는 것을 쟀다. 24턴으로 제한한 결정론적 계획 환경에서 압축 강도를 바꿔 가며 세 모델을 돌리고, 도구 호출을 '다시 찾기(retrieval)'와 '실행'으로 나눠 셌다. 결과는 여섯 가지 모델·과제 조합 모두에서 다시 찾기 호출이 늘었고, 늘어난 상호작용의 거의 전부가 그것이었다. GPT-5.5가 가장 분명한 사례였다. 완수율은 80%에서 85%로 통계적으로 차이가 없었지만(p = 1.0), 다시 찾기 호출은 21.0회에서 63.9회로 3배가 됐다(p = .002). 남긴 상태를 의미 없는 내용으로 바꿔치기하자 완수율은 그대로인데 다시 찾기가 57% 늘었다. 반면 ALFWorld 환경에서는 같은 압축을 해도 다시 찾기가 늘지 않아, 이 현상은 환경에 따라 다르다고 저자는 적었다([arXiv](https://arxiv.org/abs/2608.16370)).

2회의 계산으로 옮기면 이렇다. 압축으로 단계당 입력 토큰을 줄였는데 단계 수가 3배가 되면 과제당 비용은 오히려 늘 수 있고, 과제 완수율만 보는 대시보드에는 아무것도 안 보인다. 압축을 평가하려면 완수율 옆에 '과제당 도구 호출 수'와 '과제당 총 토큰'을 같이 둬야 한다.

반대로 잘 고른 압축은 비용과 정확도를 함께 올린다. 6월 arXiv 논문은 Microsoft Dynamics 365의 MCP 도구로 호텔 경비 항목을 처리하는 50개 과제에서 GPT-5 설정 네 가지를 비교했다. 대화 기록 전부를 유지하면 완수율 71.0%에 벤치마크당 148만 996토큰과 14.56시간이 들었고, 최근 도구 호출 5쌍만 남기면 79.0%에 53만 5,274토큰과 5.39시간, 여기에 자동 요약을 더하면 91.6%에 55만 3,374토큰과 5.79시간이었다([arXiv](https://arxiv.org/abs/2606.10209)). 장황한 기업 시스템 응답을 그대로 쌓는 것이 가장 비싸고 가장 부정확했다는 뜻이다. 7월 논문 ACM은 한 걸음 더 가서, 압축 시점을 규칙이 아니라 에이전트가 정하게 하고 버린 내용을 외부 메모리로 옮겨 필요할 때 다시 조회하게 하는 구조를 제안했다([arXiv](https://arxiv.org/abs/2607.23809)). 두 논문 모두 저자들의 벤치마크 기준이다.

세 논문을 겹치면 원칙이 하나 나온다. 버려도 되는 것은 '이미 처리한 원문'이고, 버리면 안 되는 것은 '다음 행동에 필요한 상태'다. 파일 내용, 검색 결과, API 응답 원문은 모델이 읽고 결론을 낸 뒤에는 지워도 된다. 하지만 지금 어떤 파일을 고치고 있는지, 어떤 시도가 실패했는지, 사용자가 무엇을 승인했는지는 요약에서 빠지면 에이전트가 다시 찾거나 같은 실수를 반복한다. 압축 프롬프트를 직접 쓸 수 있는 API라면 이 '상태' 항목을 명시적으로 남기라고 적어 두는 것이 첫 번째 할 일이다.

## 외부 메모리: 파일과 grep으로 시작한다

컨텍스트 밖에 두는 기억의 저장소로 무엇을 쓸지는 올해 결론이 꽤 분명해졌다. [10월 17일 기사](https://now.zeta4.net/a/2026-10-17-agent-memory-graph-db-mem0-drops-graph-drivers)에서 정리했듯, Letta는 대화 기록을 파일 하나에 넣고 grep과 검색 도구만 준 에이전트가 LoCoMo 벤치마크에서 74.0%로 Mem0의 그래프 메모리 변형 68.5%를 앞섰다고 보고했고, 에이전트 메모리 분야 최대 투자를 받은 Mem0는 오픈소스에서 그래프 DB 드라이버를 걷어냈다. 그래프는 추출과 검색에 2~4배의 비용을 요구하면서 일관된 이득을 보여 주지 못했다.

두 회사의 공식 구현도 파일이다. Anthropic 메모리 도구는 모델이 `/memories` 디렉터리의 파일을 만들고 읽고 고치고 지우는 요청을 보내면 내 애플리케이션이 실행하는 구조이고, 모델은 과제를 시작하기 전에 메모리 디렉터리를 먼저 확인한다([Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)). Claude Code는 사람이 쓰는 `CLAUDE.md`(또는 `AGENTS.md`)와 모델이 스스로 적는 '자동 메모리' 두 층을 두고 매 세션 시작 때 읽는데, 자동 메모리는 처음 200줄 또는 25KB까지만 올린다. 문서는 둘 다 "강제되는 설정이 아니라 컨텍스트"이며, 어떤 행동을 반드시 막아야 하면 메모리가 아니라 훅을 쓰라고 적었다([Claude Code Docs](https://code.claude.com/docs/en/memory)). Anthropic 엔지니어링 블로그는 이 방식을 '구조화된 메모 쓰기'라고 부르며, 에이전트가 `NOTES.md` 같은 파일에 진행 상황을 적고 나중에 다시 읽는 단순한 패턴이 "최소한의 부담으로 지속되는 기억"을 준다고 했다([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

만드는 사람이 정할 것은 저장소보다 '무엇을 적게 할 것인가'다. 메모리에 들어갈 내용은 세 가지로 나뉜다. 사람이 준 교정과 선호(같은 지적을 두 번 받지 않기 위한 것), 코드나 문서에서 다시 끌어낼 수 없는 결정과 그 이유, 그리고 지금 진행 중인 과제의 상태다. 반대로 코드에서 읽을 수 있는 사실, 한 번 쓰고 끝나는 중간 결과, 비밀 값은 적지 않는다. 그리고 메모리에 적힌 내용은 언제나 '데이터'로 다뤄야 한다. 에이전트가 읽은 웹페이지나 문서의 지시문이 메모리에 들어가면 다음 세션에서 명령처럼 작동할 수 있다. 이 문제는 6회에서 다시 본다.

## 스킬: 작업 방법을 파일로 쌓는다

기억이 '이 프로젝트에서 무엇이 참인가'라면, 스킬은 '이런 일은 이렇게 한다'는 절차다. Anthropic이 2025년 10월 16일 소개하고 12월 18일 공개 표준으로 내놓은 Agent Skills는 `SKILL.md` 파일 하나와 선택적인 스크립트·참고 문서를 담은 디렉터리다. 사양은 `name`(64자 이하 소문자·숫자·하이픈)과 `description`(1,024자 이하)만 필수로 요구한다([Agent Skills 사양](https://agentskills.io/specification)). OpenAI의 ChatGPT와 Codex도 같은 표준을 따른다([OpenAI](https://developers.openai.com/codex/skills)).

핵심 설계는 '점진적 공개'다. 에이전트는 시작할 때 설치된 모든 스킬의 이름과 설명만 시스템 프롬프트에 올리고, 과제가 설명과 맞을 때만 `SKILL.md` 본문을 읽고, 본문이 가리키는 참고 파일과 스크립트는 그때그때 연다. Anthropic 문서는 1단계 메타데이터가 스킬당 약 100토큰, 2단계 본문이 5천 토큰 미만, 3단계 파일은 열기 전까지 0토큰이라고 적고, 스크립트는 코드가 아니라 실행 결과만 컨텍스트에 들어온다고 설명한다([Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)). Codex는 이 초기 목록에 컨텍스트 창의 최대 2%(창 크기를 모르면 8,000자)를 쓰고, 스킬이 많으면 설명을 먼저 줄이며, 설정으로 1만 토큰까지 늘릴 수 있다([OpenAI](https://developers.openai.com/codex/skills)). 앞 절에서 본 컨텍스트 예산 문제를 스킬 구조 자체로 푸는 셈이다.

스킬이 실제로 도움이 되는지는 올해 측정이 시작됐다. 2월 13일 공개된 SkillsBench 초판은 11개 분야 86개 과제를 스킬 없음, 사람이 만든 스킬, 모델이 스스로 만든 스킬 세 조건으로 돌렸다. 사람이 만든 스킬은 평균 통과율을 16.2%포인트 올렸지만 분야별 편차가 컸고(소프트웨어 공학 +4.5%포인트, 의료 +51.9%포인트) 84개 과제 중 16개는 오히려 떨어졌다. 모델이 스스로 만든 스킬은 "평균적으로 이득이 없었다"며 저자들은 "모델은 자기가 소비해서 이득을 보는 절차 지식을 스스로 믿을 만하게 쓰지는 못한다"고 적었다. 2~3개 모듈로 집중한 스킬이 포괄적 문서보다 나았고, 스킬을 받은 작은 모델이 스킬 없는 큰 모델과 맞먹었다([arXiv v1](https://arxiv.org/abs/2602.12670v1)). 현재 판은 87개 과제, 18개 모델·실행 틀 조합으로 늘어 평균 통과율 33.9%에서 50.5%로 16.6%포인트 상승을 보고하고 있다([arXiv](https://arxiv.org/abs/2602.12670)).

그로부터 8개월 뒤인 10월 26일 arXiv에 올라온 Skill∞ 논문은 반대 결과를 냈다. 메타 에이전트가 '메타 스킬'을 따라 과제 스킬을 고치고, 같은 절차로 메타 스킬 자신도 고치는 재귀 구조다. 실행 흔적을 진단하고, 후보를 제안하고, 독립 검토를 요청하고, 탐색 예산을 배분하는 단계가 모두 메타 스킬에 적혀 있어 자기 개선이 그 단계 자체를 다시 쓸 수 있다. Codex CLI와 GPT-6 Luna로 SkillsBench 83개 과제를 돌린 주 비교에서 Skill∞는 60.7%, 사람이 만든 스킬은 56.4%, 기존 자동 개선 기법 SkillEvolver는 54.5%였다. 메타 스킬의 자기 개선을 빼면 55.9%로 떨어졌다. 스킬은 프롬프트에 주입하지 않고 실제 배포와 같이 이름과 설명만 보고 에이전트가 스스로 불러오게 했다. 비용은 과제 스킬 하나를 최적화하는 데 평균 입력 870만 토큰과 출력 6만 6천 토큰이 들었고, 메타 스킬 자기 개선은 과제 스킬 11개 분량의 토큰을 써서 83개에 나누면 건당 15% 미만이 더해진다고 했다([arXiv](https://arxiv.org/abs/2610.35434)). 저자들은 한계도 적었다. 두 수준의 최적화가 모두 자동 검증기에 기대므로, 자동으로 채점할 수 있는 분야에만 적용된다.

두 논문을 나란히 놓으면 만드는 사람이 가져갈 것이 분명해진다. 모델에게 "이 일을 하는 스킬을 써 줘"라고 한 번 시키면 도움이 안 된다. 그러나 스킬을 쓰고, 돌려 보고, 채점하고, 고치는 루프를 돌릴 수 있으면 사람보다 나은 스킬이 나올 수 있다. 차이는 모델이 아니라 검증기의 유무다. 우리 업무에 결정론적 채점기가 있는가가 스킬 자동 개선의 전제 조건이고, 그 채점기를 만드는 일이 다음 회(평가)의 주제다.

## 무엇을 기억하고 무엇을 버리나: 판단 기준

| 내용 | 어디에 두나 | 이유 |
|---|---|---|
| 이미 읽고 결론을 낸 파일·검색·API 원문 | 비운다(도구 결과 비우기) | 다시 볼 일이 거의 없고, 남기면 주의 예산과 입력 비용을 먹는다 |
| 지금 과제의 상태(고치는 파일, 실패한 시도, 받은 승인) | 압축 요약에 명시적으로 남기거나 메모 파일에 적는다 | 빠지면 다시 찾느라 도구 호출이 늘고 같은 실수를 반복한다 |
| 사용자의 교정·선호, 코드에서 못 끌어내는 결정과 이유 | 외부 메모리(파일) | 세션을 넘어 남아야 하고, 그래프 DB까지 갈 근거는 약하다 |
| 반복되는 작업의 절차, 도구 사용법, 검사 스크립트 | 스킬(`SKILL.md`와 스크립트) | 필요할 때만 불러와 컨텍스트를 아끼고, 검증기가 있으면 자동으로 개선할 수 있다 |
| 비밀 값, 외부 문서 속 지시문 | 어디에도 적지 않는다 | 메모리에 들어가면 다음 세션에서 명령처럼 작동한다 |

긴 과제를 맡기기 전에 확인할 것을 체크리스트로 정리하면 이렇다.

- 과제당 평균 컨텍스트 크기와 최대 크기를 재고 있는가. OpenAI 모델이라면 27만 2천 토큰, Haiku 5.5라면 10만 토큰을 넘는 순간 요금이 바뀐다.
- 도구 결과 비우기나 압축을 켰다면 완수율 옆에 과제당 도구 호출 수와 총 토큰을 함께 보고 있는가. 완수율만 보면 숨은 비용이 안 보인다.
- 압축 요약에 반드시 남을 항목(진행 중인 파일, 실패한 시도, 받은 승인, 남은 할 일)을 요약 프롬프트에 적었는가. 기본 요약이 무엇을 버리는지 확인했는가.
- 비우기와 압축이 프롬프트 캐시를 언제 깨뜨리는지 알고, 한 번에 충분히 지우도록 임계값을 잡았는가.
- 외부 메모리는 파일로 시작했는가. 메모리 경로 밖으로 나가는 요청을 막고 있는가. 메모리에 들어간 내용을 지시가 아니라 데이터로 다루는가.
- 반복되는 절차를 프롬프트가 아니라 스킬로 뺐는가. 스킬 설명에 '무엇을, 언제'가 들어 있는가. 스킬 본문은 5천 토큰 아래이고 2~3개 모듈로 집중돼 있는가.
- 스킬을 자동으로 고치고 싶다면 결정론적으로 채점할 방법이 있는가. 없다면 사람이 쓴 집중된 스킬이 지금의 최선이다.

기억과 스킬을 갖춘 에이전트가 정말 나아졌는지는 결국 재 봐야 안다. 공개 벤치마크의 한계와 우리 업무용 평가 세트를 만드는 법은 5회에서 다룬다.

## 확인할 점

- Anthropic의 '39%·29% 성능 향상'과 '84% 토큰 절감'은 2025년 9월 내부 평가 세트의 자체 측정이며, 당시 대상 모델은 Claude Sonnet 4.5였다. 현행 모델에서 같은 폭이 나오는지는 확인하지 못했다.
- 'What Does Context Compression Cost an Agent?'는 단독 저자의 arXiv 논문이며 동료 심사 여부는 확인하지 못했다. 24턴 제한의 계획 환경이라는 특수한 조건에서 잰 결과이고, 저자 스스로 ALFWorld에서는 같은 현상이 없었다고 적었다.
- 호텔 경비 벤치마크(71.0%→91.6%)와 ACM의 결과는 각 저자들이 만든 벤치마크 기준이다.
- SkillsBench 초판의 '모델이 만든 스킬은 평균적으로 이득이 없다'는 결론은 2월 13일 v1 초록에 있고, 현재 판 초록에는 그 조건의 수치가 적혀 있지 않다. 초판은 86개 과제라고 쓰면서 음의 효과를 '84개 중 16개'로 세었는데 그 차이의 이유는 초록에서 확인하지 못했다.
- Skill∞의 60.7%는 Codex CLI와 GPT-6 Luna로 돌린 저자들의 측정이며 SkillsBench의 83개 과제 부분집합 기준이다. 논문은 모델이나 실행 틀을 바꿔도 사람이 만든 스킬을 앞섰다고 적었지만 그 수치는 이 글에서 확인하지 않았다. 저자 소속은 초록 페이지에 표시되지 않아 적지 않았다.
- 컨텍스트 창 크기, 요금, 베타 헤더 이름은 11월 1일 기준 각 회사 공식 문서다. 압축과 컨텍스트 편집은 두 회사 모두 변경이 잦은 기능이라 적용 전에 문서를 다시 확인해야 한다.

## 출처

- [Context windows — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Compaction overview — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/compaction)
- [Compaction at a token threshold — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/compaction-threshold)
- [Context editing — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/context-editing)
- [Memory tool — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Agent Skills overview — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [How Claude remembers your project — Claude Code Docs](https://code.claude.com/docs/en/memory)
- [Managing context on the Claude Developer Platform — Anthropic](https://www.anthropic.com/news/context-management)
- [Effective context engineering for AI agents — Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Equipping agents for the real world with Agent Skills — Anthropic Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [GPT-6.1 Terra model page — OpenAI API](https://developers.openai.com/api/docs/models/gpt-6.1-terra)
- [Compaction — OpenAI API](https://developers.openai.com/api/docs/guides/compaction)
- [Build skills — OpenAI Codex Docs](https://developers.openai.com/codex/skills)
- [Agent Skills Specification — agentskills.io](https://agentskills.io/specification)
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance — Chroma](https://research.trychroma.com/context-rot)
- [What Does Context Compression Cost an Agent? — arXiv](https://arxiv.org/abs/2608.16370)
- [Less Context, Better Agents — arXiv](https://arxiv.org/abs/2606.10209)
- [ACM: Agentic Context Management for Long Horizon Tasks — arXiv](https://arxiv.org/abs/2607.23809)
- [SkillsBench v1 (2026-02-13) — arXiv](https://arxiv.org/abs/2602.12670v1)
- [SkillsBench (현재 판) — arXiv](https://arxiv.org/abs/2602.12670)
- [Skill∞: Recursive Self-Improvement for Agent Skill Optimization — arXiv](https://arxiv.org/abs/2610.35434)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
