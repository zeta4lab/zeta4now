---
title: 구글 Gemini 4 Carbon 공개…독립 지수 1위는 확인됐지만 나머지는 구글 발표뿐
slug: 2026-10-30-gemini-4-carbon-cyber-defenders-first
topic: ai
published_at: 2026-10-30T00:05:00+09:00
tags:
  - Google
  - Gemini
  - Gemini 4 Carbon
  - 프런티어 모델
  - 사이버보안
  - AI 안전
summary: 구글이 Argon 전면 공개 2주 만에 후속 플래그십 Gemini 4 Carbon을 발표했다. Artificial Analysis 지수 v5.0의 59점 1위는 독립 평가로 확인되지만, 보안·안전성 수치는 구글 자체 발표다. 당분간은 Fairwind 보안 방어자만 쓸 수 있다.
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-11-13
      note: Gemini 4 Carbon 일반 공개 여부와 v5.0 기준 타 모델 재평가 결과 확인
---

# 구글 Gemini 4 Carbon 공개…독립 지수 1위는 확인됐지만 나머지는 구글 발표뿐

## 한눈에 보기

구글은 10월 28일(미국 시간) 새 플래그십 모델 Gemini 4 Carbon을 발표했다. 10월 13일 [Gemini 4 Argon](https://now.zeta4.net/a/2026-10-15-gemini-4-argon-general-availability)을 전면 공개한 지 2주 만이다. 구글은 Carbon을 지금까지 만든 모델 가운데 가장 강하다고 소개하며 사이버보안과 장시간 작업을 강점으로 내세웠다. 이 가운데 외부에서 독립적으로 확인되는 것은 Artificial Analysis 종합 지수 점수 하나뿐이다. 이번 주부터는 일부 사이버 방어자만 쓸 수 있고, 일반 공개 날짜는 정해지지 않았다.

## 무엇이 검증됐고 무엇이 구글의 주장인가

독립적으로 확인되는 것은 종합 지수 점수다. 외부 평가 기관 Artificial Analysis는 자체 Intelligence Index v5.0에서 Carbon(High)에 59점을 매겼고, 자신들이 독립적으로 측정한 결과라고 밝힌다. 다만 v5.0은 최근 개편된 지수다. 발표 시점에 Artificial Analysis의 다른 모델 페이지에는 아직 이전 버전인 v4.3.2 점수가 많이 남아 있다. Argon은 v4.3.2에서 53점이고, 같은 v5.0 기준 점수는 확인되지 않는다. 그래서 "1위"가 얼마나 앞선 것인지는 다른 모델들이 새 지수로 다시 평가된 뒤에야 판단할 수 있다.

나머지 수치는 모두 구글의 자체 발표다. 보안 벤치마크, 안전성 수치, Chrome 팀의 비교, 보안 기업 Wiz의 평가는 구글 블로그에만 실렸고, 독립 재현 결과는 아직 없다. 구글은 외부 벤치마크를 안전장치(guardrail)를 끈 상태에서 쟀다고 밝혔다. 일반 사용자가 받게 될 모델과는 조건이 다를 수 있다는 뜻이다. Argon 때도 구글은 1위를 내세웠지만, 독립 평가는 '1위'와 '동률'로 갈렸다.

## 성능 수치

| 항목 | 결과 | 출처 |
|---|---|---|
| Artificial Analysis Intelligence Index v5.0 | 59점, 1위 | Artificial Analysis(독립 측정) |
| SEC-bench Pro(취약점 찾기) | 88.2% | 구글 발표 |
| ExploitGym(취약점 악용) | 54.8% | 구글 발표 |
| CWE-bench(패치) | 71.0% | 구글 발표 |
| WebDev Arena | 1768점, 4위(+89 Elo) | 구글 발표 |

구글은 내부 평가에서 안전한 코드를 만드는 성공률이 Argon보다 2배 넘게 높아졌다고 했다. Chrome 팀은 품질 좋은 패치를 만드는 능력에서 Carbon이 "다른 연구소의 대형 프런티어 모델"보다 10배 넘게 앞섰다고 밝혔지만, 비교한 모델의 이름은 공개하지 않았다.

## 안전성: 구글이 제시한 내부 수치

구글은 다음 수치를 제시했다. 모두 자체 평가다.

- Terminal-Bench 4.0 부정행위율: 0.0%
- 내부 코딩 환경의 심각한 정렬 이탈 경보: 80% 가까이 감소
- Gray Swan 간접 프롬프트 주입 공격 성공률: Argon의 0.7%에서 0%로
- 근거 없는 주장: Argon의 절반 수준

## 누가 언제 쓸 수 있나

Carbon도 Argon과 같은 순서로 공개된다. 먼저 Fairwind 프로그램으로 보안 방어자에게 열고, 신뢰할 수 있는 파트너로 범위를 차츰 넓힌다. Fairwind는 정부, 국가 사이버 당국, 핵심 기반시설 운영자, 주요 기술 플랫폼을 우선하는 조기 접근 프로그램이다. 구글은 신청 기관을 모두 심사하며, 현재 전 세계 650곳이 넘는 파트너와 일한다고 밝혔다. 미국 정부의 자발적 출시 전 모델 시험 절차에도 참여하고 있다고 했다. 일반 공개는 안전장치에 대한 피드백을 더 모은 뒤 "가능한 한 빨리" 하겠다고만 했다.

Argon은 9월 30일 Fairwind로 먼저 열렸고, 13일 뒤인 10월 13일 전면 공개됐다. Carbon이 같은 간격을 따를지는 정해지지 않았다. 일반 사용자가 직접 써 볼 수 없는 동안에는 구글의 성능 주장을 외부에서 검증할 길도 좁다.

## 가격

API 도입 가격은 Argon과 같다. 100만 토큰당 입력 2달러, 출력 10달러이고, 캐시된 입력은 95% 할인된다. 도입 기간이 끝나면 입력 4달러, 출력 20달러로 오른다. 구글은 Carbon의 도입 가격이 언제 끝나는지 밝히지 않았다(Argon은 11월 30일까지다).

## 출처

- [Gemini 4 Carbon: our next frontier model — Google 공식 블로그(2026-10-28)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/)
- [Gemini 4 Carbon — Artificial Analysis](https://artificialanalysis.ai/models/gemini-4-carbon)
- [Gemini 4 Argon — Artificial Analysis](https://artificialanalysis.ai/ko/models/gemini-4-argon)
- [Fairwind Program — Google DeepMind](https://deepmind.google/fairwind-program)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
