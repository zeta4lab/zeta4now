---
title: "Cloudflare, Vite 팀의 Void 1.0을 플랫폼까지 MIT로 공개…바이브코딩 사내 앱을 IT가 관리하는 자체 호스팅 도구"
slug: 2026-10-17-cloudflare-void-1-0-open-source
topic: ai-data-engineering
published_at: 2026-10-17T10:31:00+09:00
tags:
  - Cloudflare
  - Vite
  - VoidZero
  - Workers
  - 오픈소스
  - 바이브코딩
summary: "Cloudflare가 10월 15일 Vite 팀(VoidZero)이 만든 Void 1.0을 SDK·CLI·자체 호스팅 플랫폼까지 MIT 라이선스로 공개했다. 원래 유료 서비스로 기획했던 비공개 플랫폼을 '직원들이 AI로 만든 사내 앱을 IT가 통제하는 환경'으로 다시 짰다. 자체 호스팅에는 월 25달러부터인 Workers for Platforms와 R2, 별도 PostgreSQL이 필요하고, 배포 전 보안 검토 단계는 없다."
generated_by: claude
model: claude-fable-5-1
---

# Cloudflare, Vite 팀의 Void 1.0을 플랫폼까지 MIT로 공개…바이브코딩 사내 앱을 IT가 관리하는 자체 호스팅 도구

## 한눈에 보기

Cloudflare가 10월 15일 Vite 개발사 VoidZero의 배포 플랫폼 Void를 1.0으로 내놓으면서 SDK, CLI, 그리고 자체 호스팅 플랫폼까지 소스 전체를 공개했다. 저장소는 GitHub `voidzero-dev/void`이고 라이선스는 MIT다. SDK와 CLI는 이미 npm에 MIT로 올라와 있었고, 이번에 플랫폼 코드까지 공개됐다는 점이 핵심이다([Cloudflare 블로그](https://blog.cloudflare.com/deploy-with-void/), [The New Stack](https://thenewstack.io/cloudflare-voidzero-void-vibe-coding/)).

Void는 Vite 프로젝트에 서버 라우트와 타입이 붙은 데이터 접근을 더하고, `void deploy` 한 명령으로 D1 같은 Cloudflare 자원을 만들어 Workers에 올리는 도구다. VoidZero는 원래 이것을 비공개 유료 서비스로 키우려 했지만, 6월 Cloudflare에 합류한 뒤 "회사가 직원들의 바이브코딩 사내 앱을 장려하면서도 보안을 걱정하고, 모든 직원에게 클라우드 계정을 주고 싶지는 않다"는 수요에 맞춰 누구나 자기 Cloudflare 계정에 설치하는 오픈소스 플랫폼으로 방향을 바꿨다.

다만 자체 호스팅에는 월 25달러부터인 Workers for Platforms 유료 플랜과 R2, 별도 PostgreSQL이 필요하고, 문서화된 배포 절차에 IT 보안 검토 단계는 없다. 관리형 서비스도 아직 없다. Deno 팀 합류, Birthday Week의 Basin·K2 출시에 이어 Cloudflare 개발자 플랫폼이 빠르게 두꺼워지는 흐름 속의 발표다.

## 무엇이 공개됐나: SDK, CLI, Platform

Cloudflare 블로그는 Void를 "풀스택 Vite 앱을 만들어 Cloudflare에 배포하는 오픈소스 SDK, CLI, 자체 호스팅 플랫폼"으로 소개하고, 세 제품이 하나의 JavaScript 패키지이자 Vite 플러그인으로 묶여 있다고 설명했다([Cloudflare 블로그](https://blog.cloudflare.com/deploy-with-void/)).

**Void SDK**는 파일 기반 API 라우팅, 프리렌더링, 캐싱, 아일랜드, 데이터베이스에서 UI까지 이어지는 타입 안전성을 제공한다. API는 Hono, 인증은 Better Auth를 쓰고 React와 Vue 어댑터가 있으며 React Router, SvelteKit, Nuxt, Astro와도 함께 쓸 수 있다. `void/db`를 가져오면 개발 중에는 로컬 데이터베이스가 생기고 배포 때 D1이 만들어지며, `void/ai`를 가져오면 Cloudflare AI Gateway가 자동으로 설정된다. 블로그는 배포 시 "데이터베이스, 큐, AI 바인딩 같은 자원을 추론해 프로비저닝한다"고 썼다. 공식 문서의 프로젝트 구조는 `pages/`에 UI와 `.server.ts` 로더·액션, `routes/`에 서버 라우트(`routes/api/hello.ts`가 `/api/hello`가 되는 식), `db/schema.ts`에 Drizzle 스키마를 두는 형태다([Void 문서 — Quick Start](https://void.cloud/guide/quickstart)).

**Void CLI**는 Birthday Week에 공개된 새 `cf` CLI 위에 만들어졌고, 코딩 에이전트와 함께 쓰는 것을 염두에 뒀다. `void deploy`는 첫 실행 때 Cloudflare 로그인을 띄우고 Vite 빌드, 마이그레이션 적용, 자원 프로비저닝, 배포를 한 번에 처리한다. 사용자·프로젝트 권한 관리, 배포·로그·롤백 조회, 사용량 모니터링 같은 플랫폼 관리도 같은 CLI로 한다.

**Void Platform**은 Workers for Platforms 위에 올라가는 팀 공용 배포 환경이다. 관리자가 접근 권한과 자원 한도를 정하고 배포와 사용량을 CLI나 대시보드에서 살핀다. 개발자는 `void connect https://api.orange-company.dev`처럼 회사 플랫폼 주소를 연결한 뒤 `void deploy`만 치면 된다.

```sh
npm install -D void && npx void init && npm run dev && npx void deploy
```

저장소 README 기준 Node.js 24.21.0 이상이 필요하고, 모노레포 `packages/`에는 `void`, `create-void`, `platform`, `deploy-cloudflare`, `deploy-core`, `react`, `vue`, `svelte`, `solid`, `edge`, `isr`, `md` 12개 패키지가 있다([GitHub — voidzero-dev/void](https://github.com/voidzero-dev/void)). npm의 `void` 패키지는 10월 15일 1.0.3이 올라간 뒤 같은 날 1.1.11까지 올라갔다([npm 레지스트리 — void](https://registry.npmjs.org/void)).

## 비공개 유료 서비스에서 오픈소스로 돌아선 이유

Cloudflare 블로그는 "원래는 모든 사용자가 앱을 배포하는 하나의 비공개 플랫폼을 만들려 했다"고 인정했다. VoidZero가 Cloudflare에 합류한 뒤 플랫폼을 오픈소스로 바꿔 누구나 설치할 수 있게 했다는 설명이다. 그 배경으로 든 것이 사내 바이브코딩이다. 회사들은 직원들이 AI로 내부 앱을 만드는 것을 장려하고 싶지만 보안이 걱정되고, 모든 직원에게 클라우드 접근 권한을 주고 싶지는 않다. Void Platform은 디자이너가 인터랙티브 프로토타입을, 운영 담당자가 내부 대시보드를 만들어 공유하되 관리자가 울타리를 치는 환경을 겨냥한다([Cloudflare 블로그](https://blog.cloudflare.com/deploy-with-void/)).

에반 유는 발표 당일 X에 "인수 전부터 Void를 만들었고 원래는 상용 제품으로 만들 생각이었지만, 이제는 그럴 필요가 없어져 오픈소스로 공개했다"고 썼다. The New Stack에 따르면 VoidZero는 올해 3월 Vite+를 MIT로 공개하면서 같은 달 Void를 오픈소스 생태계의 수익원이 될 얼리 액세스 배포 서비스로 소개했었다. VoidZero에서 Cloudflare로 옮겨 전략 리드를 맡은 마이클 동은 "인수 뒤 누구나 자기 Cloudflare 계정에 설치해 호스팅할 수 있는 플랫폼으로 밑바닥부터 다시 만들었다"고 했고, 기존 Void Cloud 서비스는 자체 팀과 초대받은 소수 테스터만 쓰는 비공개 상태로 남아 있다. 엔지니어링 디렉터 크리스토프 나카자와는 "공개된 적이 없다"고 확인했다. 동은 100명 넘는 베타 사용자가 Void SDK로 앱을 배포했다고 밝혔지만 Void Cloud를 거쳤는지 Cloudflare에 직접 배포했는지는 구분하지 않았다([The New Stack](https://thenewstack.io/cloudflare-voidzero-void-vibe-coding/)).

6월 합류 발표 때 Cloudflare는 Void를 Vite용 배포 플랫폼이자 풀스택 아이디어의 "테스트베드"라 부르며 장기 과제로 "Void 플랫폼 오픈소스화"를 적어 두었고, 9월 28일 Birthday Week의 VoidZero 4개월 보고에서도 "몇 달 안에 자체 호스팅 가능한 오픈소스 Void"를 예고했다([Cloudflare 블로그 — VoidZero is joining Cloudflare](https://blog.cloudflare.com/voidzero-joins-cloudflare/), [Cloudflare 블로그 — VoidZero 업데이트](https://blog.cloudflare.com/voidzero-update/)).

## 쟁점: 비용, 보안 검토 부재, Cloudflare 종속

자체 호스팅 요건은 명확하다. Workers for Platforms와 R2가 켜진 Cloudflare 계정, PostgreSQL 데이터베이스, 로그인 제공자 계정, 앱에 쓸 도메인이다([Cloudflare 블로그](https://blog.cloudflare.com/deploy-with-void/)). Workers for Platforms 유료 플랜은 월 25달러이며 월 2,000만 요청과 6,000만 CPU 밀리초, 스크립트 1,000개가 포함되고 초과분은 종량 과금이다([Cloudflare 문서 — Workers for Platforms 요금](https://developers.cloudflare.com/cloudflare-for-platforms/workers-for-platforms/platform/pricing/)). 문서상 로그인 제공자는 GitHub, Google, 일반 OIDC, Cloudflare Access를 지원한다([Void 문서 — Self-hosted Platform](https://void.cloud/guide/self-hosted-platform)). 동은 SDK로 Cloudflare에 직접 배포하는 개발자는 유료 플랜이 필요 없다고 했지만, Cloudflare가 대신 운영해 주는 관리형 Void Platform은 현재 없다.

The New Stack은 보안 측면의 한계를 짚었다. Void 문서에 따르면 관리자는 새 앱을 기본 공개로 설정할 수 있고 프로젝트 소유자도 자기 앱을 공개로 바꿀 수 있다. 문서화된 배포 절차에는 앱이 올라가기 전 IT 보안 검토 단계가 없다. 배포 전 승인이 가능한지 묻자 나카자와는 기존 접근 제어와 "오픈소스이므로 회사가 필요에 맞게 고칠 수 있다"는 답을 내놓았다. 승인 절차나 더 엄격한 정책은 조직이 직접 구현해야 한다는 뜻이다. 동은 Cloudflare 사내에도 직원만 접근하는 Void Platform이 있어 "바이브코딩 앱을 통한 데이터 유출을 기본적으로 막는다"고 했지만, 매체는 접근을 제한해도 앱이 민감 정보를 가져다 외부로 보내는 것까지 막지는 못한다고 지적했다([The New Stack](https://thenewstack.io/cloudflare-voidzero-void-vibe-coding/)).

종속성도 남는다. Cloudflare는 Vite 등 기존 도구는 벤더 중립을 약속했지만 Void의 자동 프로비저닝은 Cloudflare 전용이다. 공식 배포 문서도 D1, KV, R2, Workers AI 바인딩은 Node.js·Bun·Deno 타깃에서 쓸 수 없다고 적는다([Void 문서 — Deployment](https://void.cloud/guide/deployment)). 나카자와는 "같은 기본 기능을 제공하는 다른 제공자 지원을 커뮤니티와 함께 하길 기대한다"고 했을 뿐 경쟁 클라우드 지원을 약속하지는 않았다.

## 한국 개발자 관점: Wrangler 기반 개발과 무엇이 다른가

지금까지 Workers 개발은 `wrangler.jsonc`에 D1·KV·R2 바인딩을 손으로 적고, 대시보드나 CLI로 자원을 먼저 만든 뒤 ID를 설정에 붙여 넣는 방식이었다. Void는 코드에서 `void/db`를 가져오는 것만으로 바인딩을 추론해 배포 때 자원을 만든다. 기존 Worker가 있으면 `void deploy`가 루트의 `wrangler.jsonc`를 연결해 자원을 보존할 수 있고, 운영 비밀은 `void secret put`으로 넣으며 로컬 `.env`는 절대 올라가지 않는다. 마이그레이션은 `db/migrations/`에서 적용되는데, 스키마가 바뀌었는데 마이그레이션이 없으면 `void db generate`를 요구하며 배포를 멈추고, 롤백은 마이그레이션을 되돌리지 않는다([Void 문서 — Deployment](https://void.cloud/guide/deployment)). D1과 R2로 돌아가는 소규모 서비스라면 Workers Free 한도 안에서 바로 쓸 수 있고(샌드박스만 Workers Paid 필요), Vite 프런트엔드와 Hono API를 한 저장소에서 타입을 공유하며 만드는 흐름이 생긴다. 반대로 Durable Objects나 세밀한 라우팅 규칙처럼 Void가 추상화하지 않은 기능은 여전히 Wrangler 쪽 지식이 필요하다. `cf` CLI 글에서 Cloudflare는 오픈 베타가 끝나면 Wrangler에 마지막 메이저 버전을 내고 18개월 유지보수만 하겠다고 밝혔으니, Wrangler 설정 파일 중심의 워크플로 자체가 Vite 플러그인과 `cf`·`void` 쪽으로 옮겨 가는 과정으로 읽을 수 있다([Cloudflare 블로그 — cf CLI](https://blog.cloudflare.com/cloudflare-cf-cli-launch/)).

## 맥락: Astro, VoidZero, Deno…그리고 Birthday Week

The New Stack은 Cloudflare가 1월 Astro 팀, 6월 VoidZero, 그리고 지난주 Deno까지 JavaScript 생태계의 핵심 팀을 잇달아 영입했다고 정리했다. Deno 합류의 내용은 본지 기사 [Deno 팀 전원 Cloudflare로](https://now.zeta4.net/a/2026-10-11-deno-team-joins-cloudflare)에서 다뤘다. 9월 28일부터 10월 2일까지 Birthday Week에는 `cf` CLI, Vinext 1.0(Next.js를 Vite로), Iceberg·R2 기반 데이터 플랫폼 Basin 정식 출시, R2 위의 이벤트 스트림 K2 공개 베타 등 46건이 쏟아졌다([Cloudflare 블로그 — Birthday Week 정리](https://blog.cloudflare.com/birthday-week-2026-wrap-up/), [Cloudflare 블로그 — Basin](https://blog.cloudflare.com/cloudflare-basin/), [Cloudflare 블로그 — K2](https://blog.cloudflare.com/cloudflare-k2-streams/)).

## 의미

Void의 진짜 의미는 "Vite용 풀스택 프레임워크 하나 더"가 아니라 Cloudflare가 Workers for Platforms를 사내 PaaS 키트로 포장해 무료로 나눠 준다는 데 있다. 소프트웨어는 공짜지만 플랫폼을 돌리는 회사는 Workers, R2, D1 사용량을 Cloudflare에 지불한다. The New Stack이 지적했듯 채택이 늘수록 Cloudflare 인프라 매출이 따라온다. 다만 접근 제어가 곧 보안 검토는 아니며, 승인 워크플로가 필요한 조직은 포크해서 직접 넣어야 한다. 1.0 당일 npm 버전이 1.1.11까지 올라간 것을 보면 아직 빠르게 움직이는 코드이기도 하다.

## 확인할 점

- Cloudflare 블로그 본문은 라이선스 이름을 적지 않았다. MIT는 GitHub 저장소 LICENSE 파일(저작권자 Cloudflare, Inc.)과 npm 메타데이터, The New Stack 보도로 확인했다.
- 자동 프로비저닝 대상으로 블로그는 "데이터베이스, 큐, AI 바인딩"을 예로 들었고 D1과 AI Gateway만 코드 예시로 보여 줬다. KV·R2·Queues가 `void/kv` 같은 import로 자동 생성되는지는 공식 문서에서 직접 확인하지 못했다.
- Cloudflare 블로그는 "VoidZero에서 지난 몇 달간 프로덕션으로 썼다"고 했고, The New Stack은 동의 말을 빌려 Cloudflare 사내 직원 전용 플랫폼이 있다고 전했다. 두 설명은 같은 인스턴스인지 불분명하다.
- 블로그에 저자 표기가 없었고, "100명 이상 베타 사용자" 수치는 The New Stack 인터뷰에만 있다.
- 다른 클라우드 제공자 지원, Bundled Dev의 실험 단계 해제, 관리형 Void Platform 제공 여부는 모두 날짜 없는 약속이라 tracking을 두지 않았다.
- GitHub 스타 수(조회 시점 310개)는 빠르게 바뀌어 본문에 넣지 않았다.

## 출처

- [Deploy with Void — Cloudflare 블로그](https://blog.cloudflare.com/deploy-with-void/) · 2026-10-15
- [Employees are vibe-coding their own apps. Cloudflare open-sources Void to give IT a handle on them — The New Stack](https://thenewstack.io/cloudflare-voidzero-void-vibe-coding/) · 2026-10-16
- [voidzero-dev/void — GitHub](https://github.com/voidzero-dev/void)
- [void 패키지 메타데이터 — npm 레지스트리](https://registry.npmjs.org/void)
- [Quick Start — Void 문서](https://void.cloud/guide/quickstart)
- [Deployment — Void 문서](https://void.cloud/guide/deployment)
- [Self-hosted Platform — Void 문서](https://void.cloud/guide/self-hosted-platform)
- [Workers for Platforms Pricing — Cloudflare 문서](https://developers.cloudflare.com/cloudflare-for-platforms/workers-for-platforms/platform/pricing/)
- [VoidZero is joining Cloudflare — Cloudflare 블로그](https://blog.cloudflare.com/voidzero-joins-cloudflare/) · 2026-06-04
- [VoidZero at Cloudflare: four months in — Cloudflare 블로그](https://blog.cloudflare.com/voidzero-update/) · 2026-09-28
- [Introducing cf, the agentic CLI for Cloudflare — Cloudflare 블로그](https://blog.cloudflare.com/cloudflare-cf-cli-launch/) · 2026-09-28
- [Birthday Week 2026 wrap-up — Cloudflare 블로그](https://blog.cloudflare.com/birthday-week-2026-wrap-up/) · 2026-10-05
- [Cloudflare Basin is now generally available — Cloudflare 블로그](https://blog.cloudflare.com/cloudflare-basin/) · 2026-10-01
- [Cloudflare K2 — Cloudflare 블로그](https://blog.cloudflare.com/cloudflare-k2-streams/) · 2026-10-01
- [Deno 팀 전원 Cloudflare로 — Zeta4 Now](https://now.zeta4.net/a/2026-10-11-deno-team-joins-cloudflare) · 2026-10-11

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
