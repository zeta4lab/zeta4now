---
title: 구글이 Workspace에 MCP를 의무화한 것은 표준을 따르려는 것이 아니라 'AI가 부르는 요청'에 따로 값을 매기려는 것이다…규모가 커지면 같은 Gmail 호출도 일반 앱은 하루 수천만 건까지 무료, 에이전트는 첫 요청부터 유료다
slug: 2026-11-25-google-workspace-mcp-mandate-agent-toll
topic: ai
published_at: 2026-11-25T22:50:00+09:00
summary: 구글은 24일 Workspace MCP 서버를 정식 출시하며 AI 에이전트는 2027년 2월 1일부터 REST API 대신 MCP로만 Workspace 데이터에 접근하라고 정했다. 이 글은 이것을 기술 표준화가 아니라 호출자 분류로 본다. 같은 데이터라도 부르는 쪽이 AI면 다른 문, 다른 요금, 다른 약관을 거친다. 열린 표준이 플랫폼에게는 AI를 식별하고 계량하는 장치가 됐고, 권한의 경계도 고객의 프록시에서 구글의 도구 정의로 옮겨 간다.
tags:
  - AI 에이전트
  - MCP
  - 구글
  - Google Workspace
  - API
  - 플랫폼
tracking:
  status: ongoing
  checkpoints:
    - date: 2027-02-01
      note: Workspace 에이전트의 REST 접근 제한 기술 집행 시작, 판별 방식과 개발자 반응 확인
generated_by: claude
model: claude-opus-5-5
---

# 구글이 Workspace에 MCP를 의무화한 것은 표준을 따르려는 것이 아니라 'AI가 부르는 요청'에 따로 값을 매기려는 것이다…규모가 커지면 같은 Gmail 호출도 일반 앱은 하루 수천만 건까지 무료, 에이전트는 첫 요청부터 유료다

> **이해관계 고지**: Zeta4 Now의 기사는 앤트로픽의 Claude로 초안을 작성하고 사람이 검토해 발행한다. 앤트로픽은 MCP를 처음 만든 회사이며, 이 기사는 MCP를 둘러싼 구글의 정책을 다룬다.

## 판단: MCP는 이제 통로가 아니라 검문소다

구글은 24일 Gmail, Drive, Docs, Sheets, Slides, Calendar, Chat, Tasks용 Workspace MCP 서버와 공식 명령줄 도구를 정식 출시하고, 사용량 등급과 'Workspace AI 도구 부속 약관'을 함께 내놨다. 핵심 문장은 이것이다. "AI 에이전트나 이와 유사한 접근 도구는 Workspace REST API를 직접 부르지 말고 MCP로 Workspace 데이터에 접근해야 한다. 기술적 집행은 2027년 2월 1일에 시작한다"([구글 Workspace 업데이트](https://workspaceupdates.googleblog.com/2026/11/mcp-servers-cli-standardized-usage-tiers-now-available.html)).

일부 보도는 이를 'AI 에이전트의 REST 접근 종료'로 전했다. 구글 개발자 문서의 실제 내용은 차단이 아니라 제한이다. 2월 1일부터 MCP 대신 REST를 직접 부르는 에이전트는 어떤 등급을 골랐든 무료 등급인 Standard의 한도에 묶인다([구글 개발자 문서](https://developers.google.com/workspace/tools-safety)).

이 글의 판단은 세 가지다. **첫째, 이번 조치의 본질은 기술 표준화가 아니라 호출자 분류다.** 같은 메일, 같은 파일이라도 부르는 쪽이 AI면 다른 문을 지나고 다른 요금표와 다른 약관을 따른다. **둘째, 열린 표준이 그 분류를 가능하게 했다.** MCP는 앤트로픽이 만들어 리눅스재단 산하 에이전틱AI재단에 넘긴 공개 규약이지만, 구글에게는 AI 호출을 한 곳으로 모아 식별하고 계량하는 장치가 됐다. **셋째, 권한의 경계가 고객에게서 구글로 옮겨 간다.** 기업이 REST 경로별로 걸어 둔 통제는 MCP의 단일 엔드포인트 앞에서 쓸모가 줄고, 에이전트가 할 수 있는 일은 구글이 정의한 도구 목록이 정한다. 세 가지 모두 해석이다.

## 같은 데이터, 두 개의 요금표

구글은 Standard와 Scaled 두 등급을 만들었다. Standard는 무료이고 결제 계정이 필요 없다. MCP는 "프로젝트별, 제품별로 하루 최대 5,000건"이다. 구글은 활성 개발자의 99% 이상이 이 등급 안에 있다고 했다. 더 쓰려면 Scaled로 가야 하고, 과금은 2027년 4월 1일부터다([구글 요금 문서](https://developers.google.com/workspace/guides/quota-pricing)).

차이는 규모가 커질 때 드러난다.

| | REST API(에이전트가 아닌 앱) | MCP(에이전트) |
|---|---|---|
| Scaled 등급 하루 무료 한도 | Gmail Light 요청 7,000만 건, Drive Light 2,000만 건 등(결제 계정 기준) | 없음. Gmail·Calendar·Drive MCP는 첫 요청부터 과금 |
| 단가(1,000건당) | 0.10~0.50달러 | 0.10~0.50달러. 일부 MCP 도구는 여러 건으로 계산 |
| 에이전트의 직접 호출 | 2027년 2월 1일부터 Standard 한도로 제한 | 유일하게 규모를 키울 수 있는 경로 |

출처: [구글 요금 문서](https://developers.google.com/workspace/guides/quota-pricing), [구글 개발자 문서](https://developers.google.com/workspace/tools-safety).

에이전트가 아닌 앱은 MCP로 옮길 필요가 없다. 구글은 "Standard 한도 안에서 운영하는 REST API 프로젝트는 지금처럼 계속 돌아간다"고 했다. 정리하면 이렇다. 사람이 쓰는 앱이 Gmail을 대량으로 읽으면 하루 수천만 건까지 무료이고, 같은 일을 에이전트가 하려면 MCP로 옮겨 첫 요청부터 돈을 내야 한다. 기술적으로 같은 요청이 호출자가 AI인지에 따라 다른 상품이 된 것이다. 이는 해석이다.

## 누가 AI인지는 신고와 약관이 정한다

그렇다면 구글은 호출자가 AI인지 어떻게 아는가. 구글이 공개한 방법은 자기 신고다. 개발자는 OAuth 클라이언트를 만들 때 'AI 에이전트용 클라이언트'에 표시해야 하고, 에이전트가 아닌 기능은 별도 클라이언트를 쓰라고 했다. Workspace MCP 서버는 이 표시가 있는 클라이언트의 호출만 받는다([구글 클라우드 도움말](https://support.google.com/cloud/answer/15549257)). 기술적 판별 방법은 어디에도 공개되지 않았다.

빈자리는 약관이 메운다. 부속 약관은 'AI 에이전트'를 "감독을 받거나 자율적으로 사용자를 대신해 행동하거나 작업을 수행하는 목표 지향적 AI 시스템이나 워크플로"로 정의하고, 접근 도구가 AI로 분류되는 것을 "피하게 해서는 안 된다"고 적었다([Workspace AI 도구 부속 약관](https://workspace.google.com/terms/ai-tools)). 같은 약관은 벡터 임베딩, 메모리 색인, 사용자 프로필, 조직 관계도를 30일 넘게 저장하지 못하게 하고, 사용자 데이터를 모델 학습, 미세조정, 평가 데이터셋 구축, 증류에 쓰지 못하게 했다. Workspace 서비스와 비슷한 제품을 만드는 것도 금지했고, 구글은 접근을 "즉시" 제한하거나 없앨 수 있다.

이 글은 약관의 이 부분이 요금표보다 중요하다고 본다. 회사 메일과 문서를 읽어 조직의 기억을 쌓는 에이전트는 지금 AI 업무 도구 시장의 중심 상품이다. 30일 보관 제한은 그 기억을 구글 바깥에 오래 쌓지 말라는 뜻이고, '비슷한 제품 금지'는 그 기억으로 구글과 겨루지 말라는 뜻이다. 데이터는 고객의 것이지만, 그 데이터를 AI가 읽는 조건은 플랫폼이 정한다. 이는 해석이다.

## 2023년의 트위터·레딧, 2025년의 슬랙

플랫폼이 API 값을 바꾸는 것은 처음이 아니다. 트위터는 2023년 2월 무료 API를 끊겠다고 발표했고 3월에 월 100달러짜리 기본 등급을 내놨다([더버지](https://www.theverge.com/2023/3/30/23662832/twitter-api-tiers-free-bot-novelty-accounts-basic-enterprice-monthly-price)). 레딧은 같은 해 4월 유료 접근을 예고했고, 인기 앱 아폴로의 개발자는 연 2,000만 달러쯤 내야 한다며 6월 30일 문을 닫았다([더버지](https://www.theverge.com/2023/6/8/23754616/apollo-reddit-app-shutting-down-api)). 슬랙은 2025년 5월 마켓플레이스 밖 상용 앱의 대화 기록 조회를 분당 1회로 줄이며 이유로 "AI 시스템이 강력해지면서" 승인받지 않은 데이터 수집을 막아야 한다는 점을 들었다([슬랙 개발자 문서](https://docs.slack.dev/changelog/2025/05/29/rate-limit-changes-for-non-marketplace-apps)).

구글의 방식은 한 단계 더 나갔다. 트위터와 레딧은 모든 호출자에게 값을 올렸고, 슬랙은 외부 앱을 막았다. 구글은 호출자를 'AI냐 아니냐'로 나눠 AI에만 다른 문을 만들었다. 막지는 않되 따로 세고 따로 받는다. 이 방식이 통하면 다른 플랫폼도 따라올 유인이 크다. 사람의 트래픽은 그대로 두고, 늘어나는 AI 트래픽만 새 수익원으로 만들 수 있기 때문이다. 이는 해석이다.

## 권한의 경계가 구글 쪽으로 옮겨 간다

해커뉴스에서 한 개발자는 자기 회사가 직접 운영하는 에이전트의 권한을 REST 경로와 메서드 단위의 프록시 규칙으로 막아 왔다고 썼다. Drive 파일 수정·삭제 금지, Gmail 발송 금지 같은 식이다. 그는 "MCP에서는 모든 호출이 하나의 엔드포인트로 가서 그걸 다시 다 만들어야 한다"고 했다([해커뉴스](https://news.ycombinator.com/item?id=50637725)).

이 지적은 작아 보이지만 핵심을 짚는다. REST에서는 고객이 요청 하나하나를 경로로 구분해 통제할 수 있었다. MCP에서는 에이전트가 할 수 있는 일이 구글이 서버에 정의한 도구 목록으로 정해지고, 고객의 통제는 그 도구 단위를 따라가야 한다. 이 사이트는 오늘 앤트로픽의 시렌 시험을 다루며 에이전트의 경계가 점점 운영체제가 아니라 모델에게 주는 말과 도구에서 정해진다고 썼다([관련 기사](https://now.zeta4.net/a/2026-11-25-anthropic-siren-sandbox-escape-tempter-is-the-prompt)). 구글의 의무화는 그 경계를 정하는 주체를 플랫폼으로 옮긴다. 보안상 이점이 없는 것은 아니다. 구글은 도구 단위로 위험한 동작을 막을 수 있다. 다만 그 판단을 고객이 아니라 구글이 내린다.

## 한국: 카카오는 같은 계산을 하고 있고, 네이버는 다른 문으로 같은 곳에 간다

한국에서도 같은 흐름이 보인다. 카카오는 2025년 8월 국내 첫 MCP 기반 개방형 플랫폼이라며 플레이MCP를 열었고([카카오](https://www.kakaocorp.com/page/detail/11674)), 2026년 8월 실적 발표에서 등록 도구가 3,400개를 넘고 하루 도구 호출이 약 10만 건이라며 "AI 시대 앱스토어"라고 불렀다고 머니투데이 계열 보도는 전했다([서플](https://supple.kr/news/cmsguqnbw00bbexbtap7ax8fa)). 앱스토어라는 말은 곧 통행료를 받는 자리라는 뜻이다. 네이버는 MCP가 아니라 다른 길로 같은 곳에 간다. 검색 API를 네이버클라우드의 API 허브로 옮기며 옛 키는 2027년 6월 30일 끊고, 허브는 "한시적으로 무료"이며 유료 요금제를 낼 계획이라고 공지했다. 쇼핑·책·학술 검색 API는 7월 31일 대체 없이 끝났다([네이버 개발자센터](https://developers.naver.com/notice/article/32530)).

이 글은 한국 기업에 두 가지를 권한다. 첫째, Workspace 위에서 에이전트를 만드는 스타트업은 2월 1일 전에 비용 구조와 함께 30일 보관 제한이 자기 제품의 기억 기능에 걸리는지부터 따져야 한다. 둘째, 정부가 지금 쓰는 '마이 AI 에이전트' 마이데이터 계획은 에이전트가 금융 데이터에 닿는 권리를 다루지만([뉴스핌](https://www.newspim.com/news/view/20260825000822)), 플랫폼이 AI 호출만 따로 값을 매기거나 막는 것에 대한 규칙은 없다. 데이터 이동권을 법으로 보장해도 그 데이터를 부르는 문에 AI 전용 통행료가 붙으면 권리는 비용으로 바뀐다. 이는 해석이다.

## 확인하지 못한 것

- 구글 블로그는 Scaled 등급이 "하루 무료 한도를 넘는 사용량만" 과금된다고 썼지만, 개발자 문서는 Gmail·Calendar·Drive MCP에 무료 한도가 없고 첫 요청부터 과금한다고 적었다. 이 글은 더 구체적인 개발자 문서를 따랐다.
- 구글이 자기 신고 외에 에이전트를 기술적으로 판별하는지는 공개 자료에서 찾지 못했다.
- 일반 Gmail 계정(Workspace가 아닌 개인 계정)이 MCP 서버를 쓸 수 있는지는 확인하지 못했다.
- 같은 주 커서가 공식 플러그인 규격을 발표했다는 일부 보도는 1차 자료로 확인되지 않아 쓰지 않았다.
- 개발자 반응은 해커뉴스의 소수 의견으로만 확인했다. 카카오 플레이MCP의 실적 수치는 2차 보도로 확인했다.
- 호출자 분류, 권한 경계의 이동, 한국에 대한 제안은 이 글의 판단이다.

## 출처

- [MCP servers, CLI, and standardized usage tiers now available — Google Workspace Updates (2026-11-24)](https://workspaceupdates.googleblog.com/2026/11/mcp-servers-cli-standardized-usage-tiers-now-available.html)
- [Workspace tools safety — Google for Developers](https://developers.google.com/workspace/tools-safety)
- [Quota and pricing — Google for Developers](https://developers.google.com/workspace/guides/quota-pricing)
- [Configure MCP servers — Google for Developers](https://developers.google.com/workspace/guides/configure-mcp-servers)
- [Workspace AI Tools Addendum — Google (2026-11-24)](https://workspace.google.com/terms/ai-tools)
- [AI agent OAuth clients — Google Cloud Help](https://support.google.com/cloud/answer/15549257)
- [Agent tools and security updates for Workspace developers — Google Workspace Updates (2026-05-01)](https://workspaceupdates.googleblog.com/2026/05/agent-tools-and-security-updates-for-workspace-developers.html)
- [Skills over MCP, Tasks, and more — Claude (2026-11-24)](https://claude.com/resources/articles/skills-over-mcp-tasks-and-more)
- [Donating the Model Context Protocol and establishing the Agentic AI Foundation — Anthropic (2025-12-09)](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [Google mandates MCP for AI agents accessing Workspace — Hacker News (2026-11-24)](https://news.ycombinator.com/item?id=50637725)
- [Twitter API tiers — The Verge (2023-03-30)](https://www.theverge.com/2023/3/30/23662832/twitter-api-tiers-free-bot-novelty-accounts-basic-enterprice-monthly-price)
- [Apollo Reddit app shutting down — The Verge (2023-06-08)](https://www.theverge.com/2023/6/8/23754616/apollo-reddit-app-shutting-down-api)
- [Rate limit changes for non-Marketplace apps — Slack (2025-05-29)](https://docs.slack.dev/changelog/2025/05/29/rate-limit-changes-for-non-marketplace-apps)
- [카카오, MCP 기반 개방형 플랫폼 플레이MCP 공개 — 카카오 (2025-08-13)](https://www.kakaocorp.com/page/detail/11674)
- [카카오 플레이MCP 실적 보도 — 서플 (2026-08)](https://supple.kr/news/cmsguqnbw00bbexbtap7ax8fa)
- [검색 API의 NAVER API HUB 이전 안내 — 네이버 개발자센터](https://developers.naver.com/notice/article/32530)
- [금융위, '마이 AI 에이전트' 마이데이터 추진 — 뉴스핌 (2026-08-25)](https://www.newspim.com/news/view/20260825000822)
- [Claude를 샌드박스 밖으로 이끈 것은 '철저히 찾아라'는 한 줄이었다 — Zeta4 Now (2026-11-25)](https://now.zeta4.net/a/2026-11-25-anthropic-siren-sandbox-escape-tempter-is-the-prompt)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
