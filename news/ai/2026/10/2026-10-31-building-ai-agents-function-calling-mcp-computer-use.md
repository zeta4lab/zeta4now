---
title: 에이전트의 손발은 함수 호출·MCP·화면 조작 셋뿐이다…도구는 20개 아래로, 화면 조작은 최고 모델도 1.6시간짜리 과제 5건 중 1건만 끝낸다
slug: 2026-10-31-building-ai-agents-function-calling-mcp-computer-use
topic: ai
published_at: 2026-10-31T20:00:00+09:00
tags:
  - 에이전트 만들기
  - AI 에이전트
  - 함수 호출
  - MCP
  - 컴퓨터 사용
  - OSWorld
summary: AI 에이전트를 만드는 7회 연재의 세 번째 편. 모델에 손발을 다는 길은 함수 호출, MCP, 화면 조작 세 가지다. OpenAI와 Anthropic의 공식 문서가 말하는 도구 수의 한계, 7월에 상태 없는 구조로 바뀐 MCP 사양, OSWorld 2.0과 Agents' Last Exam이 보여 주는 화면 조작의 현재 성공률을 바탕으로 언제 무엇을 쓸지 판단 기준을 정리한다.
generated_by: claude
model: unspecified
---

# 에이전트의 손발은 함수 호출·MCP·화면 조작 셋뿐이다…도구는 20개 아래로, 화면 조작은 최고 모델도 1.6시간짜리 과제 5건 중 1건만 끝낸다

## 한눈에 보기

[1회](https://now.zeta4.net/a/2026-10-29-building-ai-agents-system-not-model)에서 에이전트를 모델, 실행 틀, 작업 공간의 세 층으로 나눴고, [2회](https://now.zeta4.net/a/2026-10-30-building-ai-agents-cost-per-task)에서 모델을 '과제 1건 비용'으로 고르는 법을 다뤘다. 이번 회는 고른 모델에 손발을 다는 일이다. 모델이 바깥세상에 영향을 주는 길은 결국 세 가지뿐이다. 내가 만든 함수를 모델이 부르게 하는 **함수 호출**, 남이 만든 도구를 표준 규격으로 꽂는 **MCP**, 그리고 사람처럼 화면을 보고 클릭하는 **화면 조작(컴퓨터 사용)**이다.

세 가지는 상위·하위 관계가 아니라 쓰임이 다르다. 결론을 먼저 적으면 이렇다. API가 있는 일은 함수 호출로 한다. 같은 도구를 여러 에이전트와 여러 제품에서 써야 하면 MCP로 감싼다. 화면 조작은 API가 없는 소프트웨어를 다룰 때만 쓰되, 가장 좋은 모델도 긴 과제를 다섯 번에 한 번 끝내는 수준이라는 점을 전제로 설계한다. 이 글에서 인용하는 수치 가운데 OpenAI·Anthropic이 자사 모델에 대해 낸 것은 모두 자체 측정이다.

## 세 가지 길, 무엇이 다른가

| | 함수 호출 | MCP | 화면 조작 |
|---|---|---|---|
| 모델에 주는 것 | 내가 정의한 함수의 이름·설명·JSON 스키마 | MCP 서버가 내놓는 도구 목록 | 스크린샷과 클릭·입력·스크롤 동작 |
| 누가 실행하나 | 내 코드 | MCP 서버(원격 또는 로컬) | 내 코드가 가상 머신·브라우저를 조작 |
| 장점 | 가장 빠르고 싸고 통제가 쉽다 | 한 번 만들면 여러 클라이언트에서 재사용, 생태계가 크다 | API가 없어도 된다 |
| 약점 | 통합마다 코드를 짠다 | 서버를 믿어야 하고, 도구 수가 쉽게 불어난다 | 느리고 비싸고 성공률이 낮다 |
| 쓸 때 | API가 있고 내가 만드는 단일 앱 | 도구를 여러 에이전트·제품이 공유 | API가 없는 레거시·전문 소프트웨어 |

Anthropic 문서는 "도구 사용(함수 호출이라고도 한다)"이라고 적어 둘을 같은 것으로 본다([Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)). MCP도 결국 모델 입장에서는 도구 목록이 늘어난 함수 호출이다. 차이는 그 도구를 누가 정의하고 누가 실행하느냐에 있다. 화면 조작은 또 다른 층이다. Anthropic의 컴퓨터 사용 도구는 `computer_toolset_20260801` 항목 하나를 넣으면 `screenshot`, `left_click`, `type`, `zoom` 같은 17개 동작이 모델에 열리고, 모델이 고른 동작을 내 애플리케이션이 내가 통제하는 환경에서 실행하는 구조다([Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). 모델이 직접 컴퓨터를 만지는 것이 아니라, 모델은 "어디를 클릭하라"고 말하고 실행은 내 코드가 한다.

## 함수 호출: 도구는 적게, 스키마는 엄격하게

함수 호출의 기본은 두 회사가 같다. 함수마다 이름, 설명, 매개변수의 JSON 스키마를 적어 모델에 보내면 모델이 호출할 함수와 인자를 골라 돌려주고, 내 코드가 실행한 결과를 다시 넣는다. 여기서 만드는 사람이 가장 자주 놓치는 것이 두 가지다. 도구 수와 스키마 엄격성이다.

OpenAI 함수 호출 안내서는 "처음에 쓸 수 있는 함수의 수를 작게 유지하라"며 "한 턴이 시작될 때 20개 미만을 목표로 하라, 다만 이것은 느슨한 제안"이라고 적었다. 자주 쓰지 않는 도구는 '도구 검색'으로 미뤄 두고, 함수 수를 바꿔 가며 성능을 직접 재라고도 했다([OpenAI](https://developers.openai.com/api/docs/guides/function-calling)). Anthropic은 더 구체적인 숫자를 냈다. 도구 검색 문서는 GitHub·Slack·Sentry·Grafana·Splunk를 함께 붙인 전형적인 다중 서버 구성이 일을 시작하기도 전에 정의만으로 약 5만 5천 토큰을 쓰고, 도구가 30~50개를 넘으면 모델이 맞는 도구를 고르는 정확도가 떨어진다고 적었다. 도구 검색을 쓰면 요청마다 필요한 3~5개만 불러와 정의 토큰을 85% 넘게 줄인다고 한다. 도구가 10개 이상이거나 정의가 1만 토큰을 넘거나 MCP 서버 여러 개를 모아 쓸 때 도구 검색을 권하고, 10개 미만이고 매번 다 쓰는 작은 도구 집합이면 그냥 보내라고 했다([Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)). 도구 정의는 입력 토큰으로 과금되므로, 이 수치는 2회에서 본 과제당 비용과 바로 이어진다.

스키마 엄격성은 모델이 돌려준 인자가 내 스키마와 어긋나는 사고를 막는 장치다. OpenAI는 함수마다 `strict` 값을 두고 "항상 엄격 모드를 켜라"고 권하며, 엄격 모드에서는 모든 속성을 `required`에 넣고 `additionalProperties`를 `false`로 둬야 한다. Anthropic도 `strict: true`를 붙이면 "도구 호출이 항상 스키마와 정확히 일치"한다고 적었다([OpenAI](https://developers.openai.com/api/docs/guides/function-calling), [Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)). OpenAI의 함수 설계 모범 사례는 소프트웨어 설계 원칙과 거의 같다. 함수와 매개변수의 목적을 설명에 명시하고, 언제 쓰고 언제 쓰지 말지는 시스템 프롬프트에 적고, 열거형과 객체 구조로 잘못된 상태를 막고, 모델이 이미 아는 값을 다시 채우게 하지 말고, 항상 순서대로 불리는 함수는 하나로 합치라는 것이다. 다만 "예시를 넣는 것이 추론 모델에서는 성능을 해칠 수 있다"는 단서도 달았다.

병렬 호출도 결정 사항이다. 두 회사 모두 모델이 한 턴에 여러 함수를 부를 수 있고, 이를 끌 수 있다. 읽기 전용 조회라면 병렬이 빠르지만, 쓰기 동작이 섞여 있으면 "한 턴에 많아야 하나"로 제한하는 편이 승인 지점을 넣기 쉽다. OpenAI는 `allowed_tools`로 쓸 수 있는 도구를 좁히면서도 전체 도구 목록은 그대로 두면 프롬프트 캐시가 유지된다고 적었다. 도구 목록을 요청마다 바꾸면 캐시가 깨진다는 뜻이고, 이것 역시 비용 문제다.

## MCP: 한 번 만들어 여러 곳에, 대신 서버를 믿어야 한다

MCP는 Anthropic이 2024년 말 공개한 도구 연결 규격이다. 2025년 12월 9일 Anthropic은 MCP를 리눅스 재단 산하에 새로 만든 Agentic AI Foundation에 기부했고, Block의 goose와 OpenAI의 AGENTS.md가 함께 창립 프로젝트가 됐다([Anthropic](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)). 지금은 두 회사 API가 모두 MCP 서버를 직접 붙인다.

규격은 올해 크게 바뀌었다. 7월 28일 안정판으로 나온 2026-07-28 사양은 연결을 시작할 때 주고받던 `initialize` 교환과 세션 ID를 없애고, 요청마다 프로토콜 버전·클라이언트 정보·기능을 `_meta`에 실어 보내는 '상태 없는' 구조로 갔다. 유지 관리자들은 이것이 "개발자들이 가장 많이 요청한 기능"이었고, 어떤 요청이든 공유 저장소 없이 부하 분산기 뒤의 아무 서버 인스턴스에나 떨어질 수 있게 됐다고 설명했다. 서버가 클라이언트에 되묻던 기능은 열린 스트림 대신 '여러 왕복 요청'으로 바꿨고, `tools/list` 응답에 `ttlMs`를 붙여 클라이언트가 도구 목록을 캐시하고 상위 프롬프트 캐시를 안정적으로 유지하게 했다. 오래 걸리는 작업은 Tasks 확장으로 분리했고, Roots·Sampling·Logging과 HTTP+SSE 전송은 최소 12개월 유예를 두고 폐기 예정으로 표시했다. 상위 SDK 네 개(TypeScript·Python·Go·C#)의 월간 다운로드는 5억 회에 가깝고 TypeScript·Python SDK는 누적 10억 회를 넘었다([MCP 블로그](https://blog.modelcontextprotocol.io/posts/2026-07-28/)). 만드는 사람에게 중요한 변화는 두 가지다. 서버를 상태 없이 짤 수 있게 되어 운영이 쉬워졌고, 도구 목록 캐시가 규격에 들어와 2회에서 본 캐시 적중률 문제를 프로토콜 차원에서 돕는다.

두 회사 API에 MCP 서버를 붙이는 방식은 비슷하면서 다르다. OpenAI Responses API는 `type: "mcp"` 도구에 서버 주소를 넣고, 기본값으로 "커넥터나 원격 MCP 서버에 데이터가 공유되기 전에 승인을 요청"한다. 승인은 "호출 하나마다" 하고, 믿는 도구만 `require_approval`에서 빼거나 `allowed_tools`로 가져올 도구를 좁힐 수 있다. 문서는 "악성 서버는 모델 컨텍스트에 들어온 무엇이든 유출할 수 있다"며 "MCP 서버는 도구 동작을 예고 없이 바꿀 수 있다"고 경고한다([OpenAI](https://developers.openai.com/api/docs/guides/tools-remote-mcp)). Anthropic MCP 커넥터는 아직 베타이고 "MCP 사양 가운데 도구 호출만 지원"하며, 서버는 HTTPS로 공개돼 있어야 하고 로컬 STDIO 서버는 직접 못 붙인다. 쓰기·파괴 도구를 거부 목록에 올려 사람 확인 단계를 두라고 권하고, 서버가 도구 목록을 바꿔도 대화 중간에 모델이 받는 도구가 달라지지 않도록 목록을 고정하는 '핀 고정' 기능을 베타로 넣었다([Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)). 요약하면 두 회사 모두 MCP의 편리함과 함께 "서버를 믿을 수 있는가"를 만드는 사람의 책임으로 넘긴다. 이 문제는 6회에서 다룬다.

MCP는 클라우드 API 밖으로도 퍼지고 있다. 구글은 안드로이드의 AppFunctions를 앱이 "기기 안의 MCP 서버처럼" 동작하게 하는 API로 설명하고, 애플은 시스템이 정한 스키마에 앱을 맞추게 하는 반대 방향을 택했다. 두 플랫폼의 비교는 [아이폰은 '스키마', 안드로이드는 'MCP'](https://now.zeta4.net/a/2026-10-11-on-device-ai-app-integration-ios-android)에 있다.

## 화면 조작: 길이 없을 때 쓰는 마지막 수단

화면 조작은 가장 범용이지만 가장 약한 길이다. 숫자가 그렇게 말한다. 홍콩대 XLANG Lab이 6월 말 공개한 OSWorld 2.0은 108개의 긴 컴퓨터 작업으로 구성된 벤치마크다. 숙련된 사람도 과제당 중앙값 약 1.6시간이 걸리고, Claude Opus 4.7이 최대 추론으로 풀면 과제당 평균 318번 도구를 부른다. OSWorld 1.0의 약 30번과 비교해 10배다. 500단계 안에 과제를 끝냈는지를 보는 기본 지표에서 가장 좋은 Claude Opus 4.8이 20.6%만 완수했고 부분 점수는 54.8%였다. GPT-5.5는 출력 토큰 3만 9천 개로 약 14%에 닿아 토큰 효율은 훨씬 좋았지만 거기서 멈췄고, Opus 4.8은 24만 4천 토큰을 썼다([arXiv](https://arxiv.org/abs/2606.29537), [OSWorld 2.0](https://osworld-v2.xlang.ai/)). 과제가 163분을 넘기면 모든 모델의 완수율이 0으로 떨어진다는 것도 사이트의 핵심 결과다.

그 뒤 나온 모델은 더 나아졌지만 수치는 회사 발표다. Anthropic은 9월 22일 Claude Opus 5.5를 내며 OSWorld 2.1 부분 점수 81.8%(Fable 5.1 80.7%, Opus 5 74.0%)를 적었고, OpenAI는 GPT-6.1 Terra가 OSWorld 2.1에서 GPT-5.6 Terra의 최고 점수를 넘었다고만 밝히고 숫자는 적지 않았다([Anthropic](https://www.anthropic.com/news/claude-opus-5-5), [OpenAI](https://openai.com/index/introducing-gpt-6-1-terra/)). 이 글을 쓰는 시점에 OSWorld 공식 사이트에는 '2.1'에 대한 설명이 없고, Anthropic 표에는 '부분 점수'라는 표시 외에 채점 방법이 없다. 부분 점수 81.8%와 논문의 완수율 20.6%는 같은 자가 아니다.

전문 소프트웨어로 가면 더 떨어진다. UC 버클리 돈 송 교수 연구실이 주도하고 250명 넘는 현업 전문가가 참여한 Agents' Last Exam은 13개 산업군 55개 분야에서 1,490개 과제를 모았다. 과제는 재무제표 재구성, 사출 성형 시뮬레이션, 임상 변이 주석 같은 실제 직무이고, 채점은 LLM 심판 대신 숨겨진 정답과 결정론적 채점기를 쓴다. 10월 25일 갱신된 4판에서 가장 쉬운 '단기' 등급도 가장 좋은 에이전트(Codex, GPT-5.5)가 38.1%였고, 가장 어려운 '최종 시험' 등급은 최고가 2.6%, 대부분 0%였다. 논문은 "주류 실행 틀과 모델 조합 전체에서 완전 통과율 평균이 1% 미만"이라고 적었다([arXiv](https://arxiv.org/abs/2606.05405)). 1회에서 본 Terra의 'Agents' Last Exam' 점수는 바로 이 벤치마크다.

그래도 화면 조작을 버릴 수는 없다. 기업 소프트웨어의 많은 부분에 API가 없기 때문이다. OpenAI가 10월 6일 공개한 Ironclad 협력이 그 현실을 보여 준다. 계약 관리 소프트웨어 안에서 비밀유지계약 설정, 조달 승인 절차 생성, 관할권별 조항 수정 같은 11개 과제를 골라 과제마다 8~50개 기준으로 채점했다. 숙련 사용자가 30~40분 걸릴 일에서 GPT-6 Astra(최대 추론)는 평균 55.0%를 맞혔고 GPT-5.6 Sol(높은 추론)은 41.6%였으며, 시도당 추정 시간은 37.0분에서 19.2분으로 줄었다. OpenAI는 이 시간이 "모델의 처리·생성 속도를 가정해 시뮬레이션한 추정치이며 고객의 실제 시간 절감을 잰 값이 아니다"라고 각주에 밝혔고, 본문에서 "사람의 감독이 여전히 중요하다"고 적었다([OpenAI](https://openai.com/index/advancing-computer-use-with-ironclad/)). 절반을 맞히는 에이전트는 사람을 대체하지 못하지만, 사람이 검토할 초안을 20분 만에 만드는 데는 쓸 수 있다. 화면 조작 에이전트를 설계할 때 목표를 '완수'가 아니라 '검토 가능한 진행'으로 잡아야 하는 이유다.

Anthropic 컴퓨터 사용 문서가 권하는 안전장치는 화면 조작을 쓸 때의 최소 조건이다. 최소 권한의 전용 가상 머신이나 컨테이너에서 돌리고, 로그인 정보 같은 민감한 데이터를 주지 말고, 인터넷은 허용 도메인 목록으로 제한하고, 쿠키 동의·금전 거래·약관 동의처럼 실제 결과가 따르는 결정은 사람이 확인하게 하라는 것이다. 문서는 "어떤 상황에서는 Claude가 당신의 지시와 충돌하더라도 콘텐츠 안에서 발견한 명령을 따른다"고 인정하고, 스크린샷을 자동으로 검사하는 분류기가 있어도 "앞의 예방 조치는 여전히 중요하다"고 적었다([Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

## 언제 무엇을 쓰나: 판단 기준

| 상황 | 선택 | 이유 |
|---|---|---|
| 대상 시스템에 API가 있고, 이 에이전트 하나만 쓴다 | 함수 호출 | 가장 싸고 빠르고, 스키마와 권한을 내 코드가 쥔다 |
| 같은 도구를 여러 에이전트·제품·모델에서 쓴다 | MCP 서버로 감싼다 | 한 번 만들어 재사용, 두 회사 API 모두 지원 |
| 남의 MCP 서버를 붙인다 | MCP, 단 승인·허용 목록 필수 | 서버가 도구를 바꾸거나 데이터를 빼낼 수 있다 |
| 도구가 10개를 넘거나 정의가 1만 토큰을 넘는다 | 도구 검색·지연 로딩 | 선택 정확도와 비용을 함께 지킨다 |
| API가 없고 화면만 있다 | 화면 조작, 사람 검토 전제 | 긴 과제 완수율이 가장 좋은 모델도 20% 안팎 |
| API도 있고 화면도 있다 | API | 화면 조작은 느리고 비싸고 깨지기 쉽다 |

손발을 달기 전에 확인할 것을 체크리스트로 정리하면 이렇다.

- 도구마다 '언제 쓰고 언제 쓰지 않는가'를 설명이나 시스템 프롬프트에 적었는가. 이름과 스키마만 있는 도구는 모델이 엉뚱하게 부른다.
- 엄격 모드(`strict`)를 켰는가. 인자가 스키마에 맞지 않을 때 어떻게 할지 정했는가.
- 한 턴에 쓸 수 있는 도구가 20개 아래인가. 넘으면 도구 검색이나 네임스페이스로 미뤘는가.
- 쓰기·삭제·결제 도구는 읽기 도구와 분리했는가. 그 도구에 사람 승인 지점이 있는가.
- 도구 목록이 요청마다 바뀌지 않는가. 바뀌면 프롬프트 캐시가 깨진다.
- 남의 MCP 서버라면 누가 운영하고, 도구 목록이 바뀌면 어떻게 알며, 어떤 데이터가 그 서버로 가는지 적어 뒀는가.
- 화면 조작이라면 전용 가상 머신, 도메인 허용 목록, 민감 정보 차단, 결과가 따르는 동작의 사람 확인 네 가지를 갖췄는가.
- 화면 조작의 성공 기준을 '완수'가 아니라 '사람이 검토할 수 있는 진행'으로 잡았는가. 과제가 길어질수록 완수율은 0에 가까워진다.

손발을 달았다면 다음 문제는 기억이다. 과제가 길어지면 도구 결과가 컨텍스트를 채우고, 캐시와 비용과 정확도가 함께 흔들린다. 100만 토큰 컨텍스트와 외부 메모리, 그리고 반복되는 작업을 '스킬'로 쌓는 법은 4회에서 다룬다.

## 확인할 점

- Claude Opus 5.5의 OSWorld 2.1 부분 점수 81.8%와 GPT-6.1 Terra의 OSWorld 2.1 우위는 각 회사의 자체 측정이다. OSWorld 공식 사이트에는 이 글을 쓰는 시점에 2.1에 대한 설명이나 리더보드가 보이지 않았고, 부분 점수의 채점 방법은 Anthropic 발표에 없다.
- OSWorld 2.0의 완수율 20.6%와 부분 점수 54.8%는 논문 저자들의 측정이며, 측정 대상은 Claude Opus 4.8과 GPT-5.5다. 그 뒤 나온 모델의 공식 OSWorld 2.0 결과는 확인하지 못했다.
- Agents' Last Exam의 통과율은 10월 25일 4판 기준이다. 6월 초판은 평균 완전 통과율을 2.6%로 적었다가 4판에서 1% 미만으로 바꿨는데, 두 수치의 계산 기준 차이는 논문에서 확인하지 못했다.
- Ironclad 과제 11개의 점수와 소요 시간은 OpenAI 자체 연구 평가이고, 소요 시간은 시뮬레이션 추정치다.
- Anthropic 도구 검색 문서의 '약 5만 5천 토큰', '30~50개 넘으면 정확도 하락', '85% 넘게 절감'은 Anthropic의 설명이며 독립 측정은 확인하지 못했다.
- 벤치마크 자체의 오류도 있다. 7월 arXiv 논문은 OSWorld 등 5개 벤치마크의 실패 판정 150건을 다시 봐 15.3%가 틀린 판정(채점기 오판 10.7%, 깨진 과제 4.7%)이었다고 보고했다([arXiv](https://arxiv.org/abs/2607.28367)). 이 글의 완수율 수치에도 그만한 오차가 있을 수 있다.

## 출처

- [Function calling — OpenAI API](https://developers.openai.com/api/docs/guides/function-calling)
- [Remote MCP servers — OpenAI API](https://developers.openai.com/api/docs/guides/tools-remote-mcp)
- [Tool use overview — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Tool search tool — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
- [Computer use tool — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- [MCP connector — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)
- [The 2026-07-28 Specification — Model Context Protocol Blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [Donating the Model Context Protocol and establishing of the Agentic AI Foundation — Anthropic](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks — arXiv](https://arxiv.org/abs/2606.29537)
- [OSWorld 2.0 — XLANG Lab](https://osworld-v2.xlang.ai/)
- [Agents' Last Exam — arXiv](https://arxiv.org/abs/2606.05405)
- [Introducing Claude Opus 5.5 — Anthropic](https://www.anthropic.com/news/claude-opus-5-5)
- [Introducing GPT-6.1 Terra — OpenAI](https://openai.com/index/introducing-gpt-6-1-terra/)
- [Advancing computer use with Ironclad — OpenAI](https://openai.com/index/advancing-computer-use-with-ironclad/)
- [How Benchmarks Mis-Score Computer-Use Agents — arXiv](https://arxiv.org/abs/2607.28367)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
