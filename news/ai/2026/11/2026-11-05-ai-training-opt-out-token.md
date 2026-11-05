---
title: "'AI 학습 거부' 한 줄의 값…구글에서는 답변 노출까지 걸리고, 이미 가져간 데이터는 돌아오지 않는다"
slug: 2026-11-05-ai-training-opt-out-token
topic: ai
published_at: 2026-11-05T11:30:00+09:00
tags:
  - AI
  - 저작권
  - robots.txt
  - 옵트아웃
  - 언론
  - 구글
summary: 구글, 오픈AI, 앤트로픽, MS가 robots.txt 토큰 하나로 AI 학습 거부를 받기로 했다. 이는 권리가 아니라 의사표시이고 공식 표준도 아니다. 그래도 한국 사이트 운영자는 거부 기록을 남기는 수단으로 지금 적어 두는 편이 낫다.
generated_by: claude
model: unspecified
updated_at: 2026-11-05T22:25:00+09:00
tracking:
  status: ongoing
  last_update:
    at: 2026-11-05T22:25:00+09:00
    note: 지상파·네이버 8차 변론 공방과 12월 1일 9차 변론 종결 예정 반영
  checkpoints:
    - date: 2026-12-01
      note: 지상파·네이버 9차 변론 종결 여부와 선고 일정
    - date: 2026-12-15
      note: Bing 임시 그라운딩 설정 개시 여부
    - date: 2027-02-01
      note: Bing의 학습·그라운딩 선호 반영 시작 여부
    - date: 2027-03-31
      note: 구글의 토큰 지원 시작 여부와 Google-Extended 해석 방식 변경 여부
    - date: 2027-05-03
      note: 초안 만료 시점의 표준화 진행 상황과 오픈AI·메타 등의 실제 지원 여부
---

# 'AI 학습 거부' 한 줄의 값…구글에서는 답변 노출까지 걸리고, 이미 가져간 데이터는 돌아오지 않는다

## 판단: 스위치가 아니라 의사표시다

"4사 합의"라는 보도와 달리 4사 공동 문서는 찾지 못했다. 10월 30일 나온 것은 Anthropic의 케빈 켈리가 쓴 개인 초안과 회사별 글이다. 초안은 IETF의 공식 표준이 아니고, 집행과 감사는 관련 작업반의 범위 밖이다([초안](https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/), [IETF](https://datatracker.ietf.org/wg/aipref/about/)).

이 글의 판단은 이렇다. **이 토큰은 저작권을 보호하지 않는다. 다만 "나는 거부했다"는 기록을 싸게 남기는 수단으로는 쓸모가 있으니 지금 적어야 한다. 대신 그것으로 해결됐다고 생각하면 안 된다.** 진짜 싸움은 대가와 소급, 그리고 한국법상 효력이다.

*이 글은 Anthropic의 AI 모델인 Claude로 작성했다. 초안 저자가 Anthropic 소속이라 이해관계가 있음을 밝힌다.*

## 한 줄이 실제로 하는 일

```text
User-Agent: __usage_ai-training
Disallow: /
```

| 회사 | 시기 | 주의할 점 |
|---|---|---|
| Anthropic | 인식 시작, 전 서비스 적용은 진행 중 | `ClaudeBot`을 따로 적으면 그 규칙이 우선한다 |
| 구글 | 2027년 초 | `Google-Extended` 차단으로 해석한다. 이 설정은 Gemini 학습과 그라운딩을 모두 관장한다 |
| MS | 2027년 2월 1일 | 학습과 그라운딩을 분리. "대가나 노출을 보장하지 않는다" |
| 오픈AI | "수개월 내", 날짜 없음 | 공식 글은 읽지 못해 보도로 확인했다 |
| 메타, 애플, 아마존, 커먼크롤 | 약속 확인 안 됨 | 메타는 공통 신호가 중요하다고만 했다 |

**다들 놓친 함정은 구글이다.** 구글은 토큰을 `Google-Extended` 차단으로 해석한다. 구글은 이 설정을 명시적으로 허용한 사이트가 Gemini 앱의 그라운딩 응답에 나오고 클릭을 받을 수 있다고 안내한다([구글](https://developers.google.com/search/blog/2026/10/ai-training-control), [구글 크롤러 문서](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)). 학습은 거부하고 답변 노출은 유지하려는 사이트에는 곤란한 구조다. 구글 검색 순위와는 별개라고 안내하지만, AI 답변이 트래픽 입구가 되는 시대에 이는 작은 비용이 아닐 수 있다. 반면 MS는 학습과 그라운딩을 나눴다([Bing](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/)). 같은 토큰이어도 회사별 값이 다르다.

**또 하나의 함정은 와일드카드다.** 초안에 따르면 `User-agent: *` 차단은 이 토큰 신호로 인정되지 않는다. 지금까지 전체 차단을 해 둔 사이트도 AI 학습 거부 의사로는 기록되지 않는 셈이다.

## 막지 못하는 것

- **이미 수집된 데이터.** 초안은 수집 당시의 `robots.txt`를 기준으로 삼고, 읽은 1차 자료에서 기존 데이터 삭제 약속은 찾지 못했다.
- **비준수 크롤러.** TollBit은 2026년 상반기 220억 건 이상의 AI 스크레이프 가운데 19억 건 이상이 `robots.txt`를 우회·무시했다고 집계했다([TollBit](https://tollbit.com/web-access/)). TollBit은 봇 과금 사업자여서 이해관계가 있다.
- **검색·RAG·사용자 주도 조회.** 대가도 포함되지 않는다. Courtney Radsch는 "이는 통제가 아니라 선호"라고 했다([Radsch](https://courtneyradsch.substack.com/p/big-ai-firms-coalesce-around-a-new)).

IETF 안에서는 절차 비판도 나온다. Alissa Cooper는 초안이 "IETF에서 공식 지위가 없다"고 지적했고, Laurent Le Meur는 기정사실화라고 했다([Tech Policy Press](https://www.techpolicy.press/what-the-new-ai-training-optout-really-means), [IETF 메일](https://mailarchive.ietf.org/arch/msg/ai-control/fb32reD933_7PHlogKWCaLAVtD8/)). **규칙의 대상이 될 쪽이 아니라 규칙을 지킬 쪽이 먼저 문구를 정했다**는 점이 이 논란의 핵심이다. 비판의 절반은 옳다. 다만 작업반 표준을 무작정 기다리는 동안 수집은 계속되므로, 임시로라도 쓸 수 있는 신호가 생긴 것 자체는 사이트 운영자에게 이득이다. 이는 해석이다.

## 한국에 주는 영향

**언론사.** 기자협회보 6월 조사에서 10개 주요 매체의 대응은 제각각이었고, 구글 '뉴스 AI 랩' 참여 조건에는 `Google-Extended` 허용이 들어 있었다([기자협회보](https://journalist.or.kr/news/article.html?no=61015)). 토큰을 적기 전에 이 계약부터 확인해야 한다. 초안은 사적 계약이 신호보다 우선할 수 있다고 한다.

**소송.** 지상파 3사와 네이버의 소송은 5일 8차 변론을 거쳐 12월 1일 9차에서 변론을 끝낼 예정이다. 네이버는 언급된 기사 대부분이 시사보도로 저작권 보호를 받을 수 없다고 했고, 지상파는 AI 학습이 기사의 표현을 반복 학습하는 무단 이용이라고 맞섰다([뉴스임팩트](https://www.newsimpact.co.kr/news/articleView.html?idxno=4002330), [디지털데일리](https://www.ddaily.co.kr/page/view/2026110516552569126)). 재판부는 구체적 침해를 개별 저작물로 판단해야 한다고 했다([기자협회보](https://journalist.or.kr/news/article.html?no=61621)). 국내에는 AI 학습 적법성을 직접 판단한 판례가 없다([세계일보](https://www.segye.com/newsView/20261018513255)). 문체부 안내서는 공정이용 판단에서 "저작권자가 AI 학습을 명확히 거부한 경우"를 예시로 들었다([김앤장](https://www.kimchang.com/ko/insights/detail.kc?sch_section=4&idx=34407)). **토큰이 '명확한 거부'로 인정된다는 근거는 아직 없지만, 기계가 읽을 수 있고 날짜가 남는 거부 기록은 다툼에서 없는 것보다 낫다.** 이는 법률 자문이 아니라 해석이다.

**정부.** 국가AI전략위는 공개 게시물에 옵트아웃 제도가 핵심이라고 밝혔다([엠에스투데이](https://www.mstoday.co.kr/news/articleView.html?idxno=100288)). 해외 회사들이 사실상의 양식을 정하면 한국 입법도 이를 따라갈 압력을 받는다. 네이버와 독자 AI 모델 사업자들이 이 신호를 존중하는지는 확인되지 않았다. 정부는 이 토큰을 그대로 받아들일지, 그리고 국내 사업자에게 어떤 수준의 준수와 공개를 요구할지 먼저 정해야 한다.

**AI 회사.** 비용은 작지 않을 수 있지만 측정된 자료는 없다. 구글이 학습과 답변 노출을 묶어 둔 것은 경쟁 측면에서도 봐야 한다. 이는 해석이다. Cloudflare의 2025년 8월 자료에서는 Anthropic의 수집 대비 유입 비율이 약 5만 대 1로 가장 높았다는 점도 함께 밝혀 둔다([Cloudflare](https://blog.cloudflare.com/ai-crawler-traffic-by-purpose-and-industry)).

## 그래서 무엇을 해야 하나

| 대상 | 권고 |
|---|---|
| 일반 사이트·창작자 | 토큰을 지금 적고 회사별 규칙도 유지한다. 예: `GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended`, `meta-externalagent`, `CCBot` |
| 언론사 | 먼저 계약을 확인하고, 구글 노출 손익을 따져 정한다. `robots.txt` 변경 이력을 보관한다 |
| 실제 차단이 필요한 곳 | CDN 수준 차단을 쓴다. Cloudflare도 `robots.txt` 준수는 자율이라고 안내한다([Cloudflare](https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/)) |
| 협회 | 대가, 소급, 감사 요구를 토큰과 별도로 협상한다 |
| 정부 | 저작권법 개정에서 기계 판독 거부의 효력을 명시한다 |

## 확인할 점

- 오픈AI 공식 글은 접속이 막혀 보도로 확인했다.
- 구글 `Google-Extended` 허용과 토큰 차단을 함께 쓸 때 학습까지 허용되는지는 구글 확인이 필요하다.
- 토큰에 대한 한국 언론사, 협회, 정부, 네이버의 입장은 찾지 못했다. 저작권법 개정안의 제출 여부와 옵트아웃 조문도 확인하지 못했다.
- 한국어 데이터 비중과 독자 모델에 미칠 영향의 수치는 찾지 못해 다루지 않았다. 비준수율은 집계 기관과 기간에 따라 차이가 크다.
- 지상파·네이버 8차 변론에서 재판부가 한 발언은 보도에서 확인하지 못했다.

## 갱신 기록

- 2026-11-05: 지상파·네이버 8차 변론 공방과 9차 일정 반영

## 출처

- [지상파·네이버 8차 변론 — 뉴스임팩트](https://www.newsimpact.co.kr/news/articleView.html?idxno=4002330)
- [지상파·네이버 8차 변론 — 디지털데일리](https://www.ddaily.co.kr/page/view/2026110516552569126)
- [Machine-Readable Training Preference Signal — IETF 초안](https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/)
- [AI Preferences 작업반 — IETF](https://datatracker.ietf.org/wg/aipref/about/)
- [AI training control — Google Search Central](https://developers.google.com/search/blog/2026/10/ai-training-control)
- [Google common crawlers — Google](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)
- [Your content, your choice — Bing](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/)
- [Does Anthropic crawl data from the web — Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Anthropic, OpenAI, Google and Microsoft will make it easier for publishers to opt out — Nieman Lab](https://www.niemanlab.org/2026/11/anthropic-openai-google-and-microsoft-will-make-it-easier-for-publishers-to-opt-out-of-being-scraped/)
- [Web access report — TollBit](https://tollbit.com/web-access/)
- [Big AI firms coalesce around a new signal — Courtney Radsch](https://courtneyradsch.substack.com/p/big-ai-firms-coalesce-around-a-new)
- [What the new AI training opt-out really means — Tech Policy Press](https://www.techpolicy.press/what-the-new-ai-training-optout-really-means)
- [ai-control 메일링리스트 — IETF](https://mailarchive.ietf.org/arch/msg/ai-control/fb32reD933_7PHlogKWCaLAVtD8/)
- [구글 뉴스 AI 랩과 언론사 봇 현황 — 기자협회보](https://journalist.or.kr/news/article.html?no=61015)
- [변론 종결 가까워진 지상파-네이버 AI 저작권 소송 — 기자협회보](https://journalist.or.kr/news/article.html?no=61621)
- [AI 학습 적법성 국내 판례 — 세계일보](https://www.segye.com/newsView/20261018513255)
- [생성형 AI 저작권 안내서 — 김앤장](https://www.kimchang.com/ko/insights/detail.kc?sch_section=4&idx=34407)
- [국가AI전략위 옵트아웃 — 엠에스투데이](https://www.mstoday.co.kr/news/articleView.html?idxno=100288)
- [AI crawler traffic by purpose and industry — Cloudflare](https://blog.cloudflare.com/ai-crawler-traffic-by-purpose-and-industry)
- [Managed robots.txt — Cloudflare](https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
