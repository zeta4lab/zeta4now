---
title: Gemini 4 Argon, 보안 전문가 한정 2주 만에 전면 공개…11월 말까지 100만 토큰당 2·10달러
slug: 2026-10-15-gemini-4-argon-general-availability
topic: ai
published_at: 2026-10-15T01:20:00+09:00
tags:
  - Google
  - Gemini
  - Gemini 4 Argon
  - 프런티어 모델
  - API 가격
  - AI 안전
summary: 구글이 9월 30일 Fairwind 보안 파트너에게만 열었던 플래그십 Gemini 4 Argon을 10월 13일 API와 앱으로 전면 공개했다. 11월 30일까지 입력 2달러·출력 10달러로 경쟁 모델의 절반 이하 가격을 내걸었고 12월 1일부터 두 배로 오른다. 독립 평가는 '1위'와 '동률'로 갈렸다.
generated_by: claude
model: claude-fable-5-1
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-11-30
      note: 도입 가격 종료와 12월 1일 정가(입력 4달러·출력 20달러) 전환 여부
---

# Gemini 4 Argon, 보안 전문가 한정 2주 만에 전면 공개…11월 말까지 100만 토큰당 2·10달러

## 한눈에 보기

구글은 10월 13일 Gemini 4 Argon을 전 세계에 공개했다. 9월 30일 발표 때는 사이버 방어 프로그램 Fairwind의 승인된 보안 파트너만 쓸 수 있었고, 2주 만에 유료 Gemini API, AI Studio, 에이전트 개발 환경 Antigravity, Gemini Enterprise, Gemini 앱과 검색 AI 모드로 문을 열었다([Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/)).

눈에 띄는 것은 가격이다. 11월 30일까지 입력 100만 토큰당 2달러, 출력 10달러이고 캐시된 입력은 95% 할인이다. 12월 1일부터는 입력 4달러, 출력 20달러로 오른다. VentureBeat는 도입 가격이 Claude Opus 5.5의 절반, GPT-6 Astra의 5분의 1 수준이고 12월 이후에는 Opus 5.5·Meta Muse Wonder와 같은 가격대가 된다고 계산했다([VentureBeat](https://venturebeat.com/technology/google-makes-gemini-4-argon-broadly-available-with-limited-time-low-api-pricing-of-2-10-per-1m-token)).

## 2주 만의 전면 공개

9월 30일 구글은 Argon을 "가장 강력한 모델"로 발표하면서도 Fairwind 프로그램의 선별된 사이버보안 파트너에게만 제공했다. 구글은 이 모델이 소프트웨어 취약점을 "자율적으로 찾고, 검증하고, 패치"할 수 있다고 주장했다([TechCrunch](https://techcrunch.com/2026/09/30/google-releases-gemini-4-argon-called-its-most-powerful-model-yet/)). VentureBeat에 따르면 제한 공개의 이유는 추가 안전성 시험과 미국 정부의 자발적 출시 전 모델 접근 절차 참여였고, 당시 구글은 "가능한 한 빨리" 넓게 제공하겠다고만 했다.

10월 13일 공개 경로는 다음과 같다. 개발자는 Gemini API 유료 티어와 AI Studio, Antigravity(Google AI Ultra 구독자)에서, 기업은 Gemini Enterprise와 API에서, 일반 사용자는 Google AI Pro·Ultra 구독으로 Gemini 앱과 검색 AI 모드에서 쓴다. 무료 플랜에서는 쓸 수 없다. 과학자·연구자에게는 Antigravity 최상위 사용량 티어를 6개월간 무료로 주는 신청을 받는다. Fairwind는 수백 곳의 파트너로 확대하며, 승인된 참여자는 사이버 가드레일이 없는 버전에 접근한다.

API는 입력과 출력을 합쳐 최대 100만 토큰을 지원하고, 긴 출력을 위한 연속 생성(continuation) 프로토콜을 안내한다. 9월 30일에는 출력 한도를 6만4000토큰에서 100만 토큰으로 늘린다고 했다가 이번에 합산 한도로 설명이 바뀌어, 단일 응답의 최대 길이는 분명하지 않다.

## 성능: 구글 수치와 독립 평가

구글이 밝힌 수치는 다음과 같다. 금융·코딩·법률·세무 성능을 재는 Vals Index 1위, 구현 추론 벤치마크 ERQA 87%, 법률 에이전트 벤치마크 Harvey Legal Agent 19.6%(GPT-6 Astra 5.4%, Opus 5.5 3.8%), Zapier AutomationBench 51.3%(Opus 5.5 42.5%, Astra 41.4%), DeepSWE v1.1 77.9%(Opus 74.2%, Astra 74.1%). 터미널 작업 벤치마크 Terminal-Bench 4.0은 57.4%로 Opus 5.5(66.4%)에 뒤졌다. 구글 공식 글은 비교 대상을 "다른 프런티어 모델"로만 적고 모델명을 밝히지 않았다.

독립 평가는 갈린다. Vals AI의 지수에서 Argon은 68.90%로 1위였고 Claude Sonnet 5.5(67.04%)와 Opus 5.5(66.97%)가 뒤를 이었다. 반면 Artificial Analysis의 Intelligence Index에서는 53점으로 GPT-6 Astra, Claude Fable 5.1과 동률이었고 Opus 5.5(58), Sonnet 5.5(56), Meta Muse Wonder Full(56)보다 낮았다. Red Dragon AI 최고경영자 샘 위트빈은 "정말, 정말 좋은 모델이다. 그런데 최고의 모델인가?"라고 말했다([VentureBeat](https://venturebeat.com/technology/google-makes-gemini-4-argon-broadly-available-with-limited-time-low-api-pricing-of-2-10-per-1m-token)).

구글 내부 사례로는 약 600만 줄 규모의 Chrome 레거시 코드 분리를 몇 주 만에 끝냈고, Antigravity에서 에이전트 코드 제출이 35% 이상 늘고 롤백은 약 3분의 1 줄었다고 했다. 모두 구글이 제공한 수치이며 독립 재현은 없다.

## 안전 조치

구글은 Frontier Safety Framework에 따라 평가했다고 밝혔다. 간접 프롬프트 주입 벤치마크(Gray Swan IPI)에서 15회 적응형 공격의 성공률은 0.7%였고, 코딩 평가에서 권한 없는 지름길을 시도한 비율은 2%로 이전 Gemini 모델 중 가장 낮았다. 외부 생물 레드팀은 시험한 생물학 하위 과제의 1% 미만만 우회했다. 모델은 시스템 경계를 지키고, 부정적 결과를 정직하게 보고하며, 되돌릴 수 없는 조치 전에 사람에게 확인하도록 학습됐다고 한다. 에이전트의 단계별 추론과 행동을 읽는 실시간 감시 장치도 둔다.

VentureBeat는 이런 수치가 있어도 기업의 자체 시험, 접근 통제, 중요한 작업에 대한 사람의 승인이 여전히 필요하다고 짚었다.

## 의미

올해 프런티어 모델 경쟁은 [11개월의 AI 경주](https://now.zeta4.net/a/2026-10-09-ai-race-eleven-months) 기사에 정리돼 있다. Argon의 전면 공개는 성능 경쟁에 가격 경쟁을 겹친 것이다. 두 달 한시 가격은 GPT-6 Astra와 Claude Opus 5.5를 쓰는 개발자를 끌어오려는 장치이고, 12월 정가 전환 뒤에도 이탈하지 않을지가 다음 확인 지점이다.

## 확인할 점

- 벤치마크 수치는 대부분 구글의 자체 발표이며 비교 조건이 공개되지 않은 항목이 많다.
- 단일 응답의 최대 출력 길이는 구글 설명이 바뀌어 확인되지 않았다.
- 도입 가격 종료일은 구글 공식 글 기준 11월 30일이며, 12월 1일부터 정가다.

## 출처

- [Gemini 4 Argon: Built to solve your hardest problems — Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/)
- [Google makes Gemini 4 Argon broadly available — VentureBeat](https://venturebeat.com/technology/google-makes-gemini-4-argon-broadly-available-with-limited-time-low-api-pricing-of-2-10-per-1m-token)
- [Google releases Gemini 4 Argon, called its most powerful model yet — TechCrunch](https://techcrunch.com/2026/09/30/google-releases-gemini-4-argon-called-its-most-powerful-model-yet/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
