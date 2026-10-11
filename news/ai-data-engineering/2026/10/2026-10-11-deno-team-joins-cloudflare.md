---
title: "Deno 팀 전원 Cloudflare로…Deno 런타임은 1년 뒤 개발 종료, Deno Deploy는 6개월 뒤 문 닫는다"
slug: 2026-10-11-deno-team-joins-cloudflare
topic: ai-data-engineering
published_at: 2026-10-11T18:35:00+09:00
tags:
  - Deno
  - Cloudflare
  - Workers
  - JavaScript
  - 런타임
  - 오픈소스
summary: "Node.js를 만든 라이언 달의 Deno 팀이 통째로 Cloudflare에 합류한다. Deno 런타임은 1년간 보안·버그 수정만 받은 뒤 공식 개발을 끝내고, 호스팅 서비스 Deno Deploy는 6개월 뒤 종료된다. 두 팀은 Workers를 자기 서버에서 돌리게 하는 기술을 합칠 계획이다."
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2027-04-09
      note: Deno Deploy 종료(발표 기준 6개월)와 유료 고객 이전 지원 결과
    - date: 2027-10-09
      note: Deno 런타임 공식 지원 종료와 커뮤니티 이어받기 여부
---

# Deno 팀 전원 Cloudflare로…Deno 런타임은 1년 뒤 개발 종료, Deno Deploy는 6개월 뒤 문 닫는다

## 한눈에 보기

Node.js를 만든 라이언 달이 2018년 "Node.js의 실수를 바로잡겠다"며 시작한 Deno가 독립 프로젝트로서는 사실상 막을 내린다. Deno 팀 전원이 Cloudflare로 옮기고, Deno 런타임은 1년 뒤 공식 개발이 끝나며, 호스팅 서비스 Deno Deploy는 6개월 뒤 종료된다. 대신 두 팀은 Cloudflare의 서버리스 플랫폼 Workers를 클라우드뿐 아니라 자기 서버에서도 돌릴 수 있게 만드는 데 힘을 모은다.

## 무엇이 발표됐나

10월 9일 Cloudflare와 Deno는 각자의 블로그에 같은 제목("Deno is joining Cloudflare")으로 소식을 알렸다. Cloudflare 글은 Workers 기술 책임자 켄턴 바르다와 라이언 달이 함께 썼다. 두 글 모두 본문에서는 "Deno 팀이 합류한다"고 표현했고, 거래 금액은 밝히지 않았다. Cloudflare 블로그는 이 글을 '인수(Acquisitions)' 분류로 묶었다.

## celld와 workerd를 합친다

이번 합류의 중심은 Deno 팀이 만들어 온 `celld`다. Workers와 Durable Objects를 오픈소스로 다시 구현한 것으로, Rust로 만든 실행 파일 하나에 외부 의존은 오브젝트 스토리지뿐이다. 이 안에서 연산, 관계형 데이터베이스, 큐, 실시간 통신을 함께 제공해 자기 인프라에서 운영하고 확장하도록 설계됐다.

Cloudflare는 이를 자사의 오픈소스 Workers 런타임 `workerd`와 합치겠다고 밝혔다. 라이언 달과 Deno 공동 창업자 버트 벨더가 이 작업을 이끈다. 지금의 workerd는 Durable Objects를 한 인스턴스로만 실행할 수 있어 로컬 테스트에는 쓸 만해도 운영 규모로 늘릴 수 없었다. Cloudflare는 통합이 끝나면 workerd로 직접 운영하는 것을 "Workers 방식으로 앱을 만들고 돌리는 1급 지원 방법"으로 만들겠다고 했다. 세부 일정은 앞으로 몇 달 안에 발표한다.

## Deno 사용자에게 바뀌는 것

**Deno 런타임**은 앞으로 1년 동안 버그 수정과 보안 업데이트를 담은 월간 릴리스만 나오고, 그 뒤 공식 개발이 끝난다. 코드는 오픈소스로 남으며, Deno는 개발을 이어갈 사람을 환영한다고 밝혔다.

**Deno Deploy**는 6개월 더 운영한 뒤 종료된다. 정확한 종료일은 아직 공지되지 않았다. 유료 고객이 Cloudflare Workers로 옮길 때 이전을 지원한다.

**JSR**(Deno가 만든 자바스크립트 패키지 저장소)은 계속 운영되고 인프라만 Cloudflare로 옮긴다. V8 엔진을 Rust에서 쓰게 해 주는 `rusty_v8` 지원도 계속하며, workerd와의 통합을 추진한다.

## 왜 이런 선택을 했나

라이언 달은 별도의 런타임과 호스팅 서비스를 각각 키우는 대신 공동 플랫폼에 힘을 모으겠다고 설명했다. 그는 Durable Objects가 서버리스 실행, 상태 저장, 웹소켓을 저렴하게 제공해 AI 에이전트를 돌리는 기반으로 잘 맞는다고 보고, 이 프로그래밍 모델을 Cloudflare 네트워크든 자기 인프라든 "서버를 만드는 기본 방식"으로 만들겠다는 목표를 내걸었다.

Cloudflare는 Workers가 고객을 묶어 두려는 플랫폼이라는 비판에 정면으로 답했다. 켄턴 바르다는 이 주장이 틀렸다며, 오히려 고객이 못 떠난다는 인식이 회사에 손해라고 썼다. 오픈소스 런타임을 요구한 고객 때문에 workerd를 공개했고, 실제로 workerd를 이용해 떠난 고객도 있었다고 했다. celld 통합으로 자기 서버 운영이 쉬워지면 이 논리를 기술로 뒷받침하는 셈이다.

## 개발자 반응

해커뉴스에서 이 소식은 1,350점과 댓글 703개를 받았다. 1년 지원 종료 소식이 글 맨 아래에 묻혀 있었다는 지적, 벤처 투자로 운영되는 오픈소스 런타임의 한계를 짚는 의견이 많았다. Deno의 권한 모델과 내장 도구(타입 검사, 린터, 테스트 실행기)가 Node.js의 변화를 이끌었다는 평가도 함께 나왔다. 이전 부담은 Deno 고유 기능을 얼마나 썼느냐에 달렸다. 표준 API 위주라면 Node.js나 Workers로 옮기기 쉽지만, Deno KV 같은 고유 API를 쓴 서비스는 손이 더 간다.

## 맥락: Cloudflare의 개발자 생태계 영입

Cloudflare는 지난 6월 프런트엔드 빌드 도구 Vite를 만든 VoidZero(에반 유 창업)를 인수했다. 그때는 Vite, Vitest 등을 MIT 라이선스 오픈소스로 유지하겠다고 약속했다. 넉 달 만에 자바스크립트 런타임 팀까지 데려오면서, 빌드 도구에서 실행 환경까지 자바스크립트 개발 흐름 전반을 Workers 쪽으로 끌어당기고 있다. Deno는 2022년 세쿼이아캐피털 주도로 2,100만 달러를 투자받은 바 있다.

## 확인할 점

- Deno Deploy의 정확한 종료일과 유료 고객 이전 지원 내용
- 1년 뒤 Deno 런타임을 커뮤니티가 이어받을지(포크 여부)
- celld와 workerd 통합 일정, 그리고 Deno KV 사용자를 위한 이전 경로

## 출처

- [Cloudflare 블로그 — Deno is joining Cloudflare](https://blog.cloudflare.com/deno-joins-cloudflare/) · 2026-10-09
- [Deno 블로그 — Deno is joining Cloudflare](https://deno.com/blog/cloudflare) · 2026-10-09
- [Hacker News — Deno Is Joining Cloudflare (토론)](https://news.ycombinator.com/item?id=50019911)
- [Intelligent CIO — Cloudflare acquires VoidZero](https://www.intelligentcio.com/me/2026/06/05/cloudflare-acquires-voidzero/) · 2026-06-05
- [Deno 블로그 — Deno raises $21M](https://deno.com/blog/series-a) · 2022-06-21

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
