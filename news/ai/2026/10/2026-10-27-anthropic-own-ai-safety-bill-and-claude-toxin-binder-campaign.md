---
title: Anthropic이 직접 쓴 연방 AI 안전 법안 초안 유출…나흘 뒤엔 Claude가 64시간 자율 캠페인으로 전갈 독소 결합체 17개 확인
slug: 2026-10-27-anthropic-own-ai-safety-bill-and-claude-toxin-binder-campaign
topic: ai
published_at: 2026-10-27T14:17:00+09:00
tags:
  - Anthropic
  - Claude
  - AI 규제
  - 단백질 설계
  - 바이오 안보
  - 자율 에이전트
summary: Politico가 10월 16일(현지시각) Anthropic이 의원들에게 돌린 비공개 연방 AI 안전 법안 초안을 공개했다. 모델 차단 요건을 피해 10억 달러 초과 또는 50명 초과 사망·중상의 '예견 가능하고 임박한' 위험으로 좁히고 주법을 선점하는 내용이어서, 회사가 6월에 낸 공개 프레임워크와 어긋난다는 비판이 나왔다. 나흘 뒤 Anthropic은 내부 연구 모델이 64시간 동안 대체로 자율적으로 전갈 신경독소 결합체 318,484개를 설계했고 외부 실험실에서 211개를 시험해 17개가 기준을 충족했다고 밝혔다. 회사는 "해독제를 만들었다고 주장하지 않는다"고 적었다.
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-11-04
      note: 미국 중간선거 직후. Anthropic이 예고한 선점 조항 수정 문안과 평가자 요건 후속 제안이 공개되는지, 법안이 실제 발의되는지 확인
    - date: 2026-12-22
      note: 전갈 독소 결합체 211개 설계·실험 데이터의 Hugging Face 공개 여부와 독립 연구진의 재현·검증 보고 확인
    - date: 2027-02-01
      note: Anthropic이 다음 단계로 든 천연 독소 결합 확인, 패치클램프 기능 시험, 생쥐 보호 실험 결과가 나오는지 확인
---

# Anthropic이 직접 쓴 연방 AI 안전 법안 초안 유출…나흘 뒤엔 Claude가 64시간 자율 캠페인으로 전갈 독소 결합체 17개 확인

## 한눈에 보기

Anthropic이 10월 셋째 주 미국 의회에 두 가지 얼굴을 보였다. 10월 16일(현지시각) Politico는 Anthropic이 의원들에게 비공개로 돌리던 연방 프런티어 AI 안전 법안 초안을 공개했다. 정부가 모델의 출시나 사용을 막을 수 있는 경우를 10억 달러를 넘는 피해 또는 50명을 넘는 사망·중상의 '예견 가능하고 임박한' 위험으로 좁히고, 생물무기·통제 상실·사이버 공격을 대상 위험으로 꼽으며, 상무부가 연방법원에 제소하는 방식만 허용하고 주(州)의 프런티어 AI 법을 선점하는 구조다. 안전 쪽 인사들은 이 문턱이 회사가 6월에 공개한 'Anthropic's Advanced AI Framework'보다 약하다고 비판했고, 회사는 선점 문안이 "충분히 정밀하지 않다"며 고치겠다고 했다.

나흘 뒤인 10월 20일 Anthropic은 공식 연구 블로그에 'Claude가 전갈 신경독소 결합 단백질을 어떻게 설계했나'를 올렸다. 내부 연구 모델이 Claude Science 환경에서 약 64시간 동안 대체로 자율적으로 작동하며 설계 도구 12종으로 후보 318,484개를 만들고 설계-독소 쌍 553,052개를 공동접힘(co-folding)으로 선별했으며, 자신이 고른 180개에 연구진이 31개를 더한 211개를 외부 수탁 실험실 두 곳에서 시험한 결과 17개가 결합 기준을 충족했다는 내용이다. 회사는 같은 글에서 "우리는 해독제를 만들었다고 주장하지 않는다"고 못 박았다.

두 건은 같은 날이 아니고 같은 주의 일이지만 같은 영역을 가리킨다. 법안 초안이 정부 개입 대상으로 못 박은 세 위험 가운데 하나가 생물무기이고, 같은 회사의 모델은 그 생물학 설계 역량으로 독소 대응 단백질을 만들어 실험실에 보냈다. 규제의 바닥을 회사가 직접 쓰는 동안, 그 규제가 다룰 능력의 실측값도 회사 발표로만 공개되고 있다.

## 10월 16일: 회사가 쓴 법안의 문턱

Politico는 10월 16일 Anthropic 관계자들이 의원실에 돌린 비공개 논의용 초안(discussion draft)을 보도하며 전문을 공개했다. 보도된 핵심은 정부가 모델을 막을 수 있는 요건이다. 10억 달러를 넘는 피해나 50명을 넘는 사람의 사망 또는 중상을 일으킬 '예견 가능하고 임박한' 위험이 있을 때만 차단이 가능하고, 대상 위험은 생물무기, 개발사가 모델 통제를 잃는 경우, 사이버 공격 세 갈래다. 집행은 상무부만 할 수 있고, 상무부가 직접 중단시키는 대신 연방법원에 차단을 청구해야 하며 다른 기관이나 공직자는 모델을 정지시킬 수 없다. 공개 공시, 제3자 평가, 사고 보고를 다루는 주법은 선점된다. Anthropic 대변인은 이 초안이 "6월부터 연방·주 의원들에게 주창해 온 Anthropic's Advanced AI Framework에 담긴 제안을 담은 것"이라고 밝혔다. 법안은 아직 발의되지 않았고 법이 된 것도 아니다([TNW](https://thenextweb.com/news/anthropic-leaked-ai-safety-bill-backlash-frontier), [Interesting Engineering](https://interestingengineering.com/ai-robotics/anthropic-confidential-congress-draft-bill)). Politico 원문은 이 저장소의 조사 도구로 직접 열리지 않아, 초안 조항은 원문을 인용한 복수 매체 보도로만 확인했다.

## 회사의 공개 프레임워크와 어긋난 지점

비판의 근거는 Anthropic이 6월에 스스로 낸 문서다. 'Anthropic's Advanced AI Framework'(2026년 6월)는 대상 개발사를 훈련 연산 10^25 FLOP 초과에 연 AI 매출 5억 달러 초과 또는 연 AI 연구개발 지출 10억 달러 초과를 함께 만족하는 곳으로 정하고, 생물무기·공격적 사이버 작전·통제 상실·자동화된 연구개발 네 범주를 '열거된 위험'으로 둔다. 선점에 대해서는 "미국에서는, 의회가 이 프레임워크가 제시한 가장 강한 조치에 이르거나 그것을 넘어서는 엄격한 연방 체제를 제정하지 않는 한 주법을 선점해서는 안 된다"(Congress should not preempt state law unless it enacts a rigorous federal regime that meets or exceeds the strongest measures proposed in this framework)고 썼고, 선점하더라도 "의회가 명시적으로 점유하기로 택한 특정 프런티어 거버넌스 기능"에 한정하고 모호한 부분은 주 권한을 보존하는 쪽으로 해석해야 한다고 적었다. 강한 연방법이 없으면 주가 완전한 입법 권한을 가져야 한다는 문장도 있다([Anthropic Advanced AI Framework PDF](https://www-cdn.anthropic.com/files/4zrzovbb/website/0a58d567024a8b448ff15158ebc3625328dfcc1f.pdf)).

프레임워크는 차단 권한도 다르게 설계했다. 기관이 시스템 카드·리스크 보고서·독립 평가를 검토해 네 가지 위반(보고서 미공개, 평가자의 자격·중립성 결여, 평가자의 시간·접근 부족, 안전조치를 감안해도 중대한 재앙적 위험이 확인된 경우) 가운데 하나를 확인하면 벌금, 후속 모델 배포 금지, 극단적인 경우 이미 배포된 모델의 사용·접근 제한까지 할 수 있게 하는 안을 담았다. 과도한 권한을 막는 장치로 법원 집행, 재량 제한, 신속 사법심사를 선택지로 제시했을 뿐, 금전 피해액이나 인명 피해 숫자를 차단의 전제로 깔지는 않았다. 독립 평가에 대해서도 평가자 기준 공개와 면허제 검토, 공적·공동 기금, 평가자 등급제와 고위험 사안의 무작위 배정 같은 '평가자 쇼핑' 방지책을 권고했다.

유출된 초안은 이 가운데 상당 부분을 덜어 냈다는 것이 비판의 요지다. Transformer는 10월 19일 분석에서 초안이 제3자 평가를 요구하면서도 평가자에게 기준이나 면허를 요구하지 않고 자기 인증을 허용한다는 점, 법원이 상무부와 평가자의 판단에 "존중 없이"(without deference) 판단하고 차단이 개발사·이용자·공중에 끼칠 피해를 따지도록 하면서 차단하지 않아 생길 피해는 따지라고 하지 않는다는 점, 캘리포니아 SB 53과 뉴욕 RAISE법, 일리노이 SB 315가 선점되고 주 의회·법원이 재앙적 위험을 이유로 모델을 정지시키는 길까지 막힌다는 점을 짚었다. LawAI의 찰리 불럭은 이런 구조에서 감사인들이 "가장 싼 값에 가장 성가시지 않은 감사"를 두고 경쟁하게 된다고 했고, 옹호단체 Encode의 법률 고문 네이선 캘빈은 초안이 "본능적으로 화가 났다"(viscerally angry)고 말했다([Transformer](https://www.transformernews.ai/p/anthropic-leaked-ai-bill-undermines-safety-first-approach)).

Anthropic의 연방 담당 책임자 앤서니 시미노(Anthony Cimino)는 10월 18일 X에 올린 글에서 선점 문안이 "충분히 정밀하지 않다"(not precise enough)며 Advanced AI Framework에 맞게 고치겠다고 했고, 피해 문턱에 대해서는 "문턱을 재평가할 시점이 맞을 것"이라고 했다. 그는 문턱 숫자가 캘리포니아 주법에서 가져온 것이라고 설명했지만 그것이 왜 연방 기준이 되어야 하는지는 밝히지 않았다. 캘리포니아 주상원의원 스콧 위너는 이 제안이 "공중 보건과 안전을 지키기에 한참 모자란다"고 했다. 비교 기준으로 거론되는 FRONTIER Act는 제이 오버놀테·로리 트래한 하원의원이 7월에 발의한 초당적 법안이다([TNW](https://thenextweb.com/news/anthropic-leaked-ai-safety-bill-backlash-frontier)). 시미노의 글은 원문을 직접 확인하지 못해 TNW 보도로 인용한다.

## 10월 20일: 64시간 캠페인의 숫자와 한계

Anthropic Science 팀은 10월 20일 블로그에서 멕시코·브라질·북아프리카·중동 지역 전갈의 신경독소 다섯 종을 표적으로 한 미니바인더(minibinder) 설계 캠페인을 공개했다. 모델은 "Claude Science 안에서 작동하는 내부 연구 모델"로만 소개됐고 모델명이나 버전은 밝히지 않았다. 캠페인은 약 64시간 동안 "대체로 자율적"으로 진행됐다. 첫 프롬프트 뒤 24시간은 사람의 개입 없이 혼자 일했고, 연구진은 네 번의 후속 프롬프트를 줬다. 선정된 설계 180개 가운데 대부분과 가장 강한 결합체는 세 번째 후속 프롬프트 뒤에 나왔다. 모델은 설계 도구 12종을 쓰면서 독소나 알려진 단백질을 닮은 설계는 걸러 냈고, 후보 318,484개를 만들어 설계-독소 쌍 553,052개를 복합체로 공동접힘해 선별했다. 연산은 약 1만 GPU 시간이 들었다. 프롬프트 작성에는 금융 리서치 회사 Citrini Research가 참여했다([Anthropic](https://www.anthropic.com/research/claude-scorpion-toxin-binder-design)).

실험은 수탁 실험실 두 곳이 맡았다. Adaptyv Bio는 무세포 발현계로, Twist Bioscience는 사람 신장세포에서 Fc 융합 단백질로 발현해 각각 표면플라스몬공명(SPR)으로 결합을 측정했다. 211개 가운데 17개가 기준을 충족했고, 기준은 두 실험실에서 모두 양성, 해리상수 1 µM 이하, 비표적 대조 단백질 CLEC12A에는 신호 없음이었다. 충족한 17개는 각각 단일 독소에만 결합했다. 독소별로는 Cn2 7개, AaH II 4개, AaH I 4개, LqhIII 2개다. 단일 독소를 겨냥한 설계는 60개 중 11개(18%)가 결합했고, 여러 독소를 동시에 겨냥한 설계 가운데 둘 이상에 결합 기준을 충족한 것은 없었다. 가장 강한 Cn2-B1과 Cn2-B2는 한 자릿수 나노몰 수준의 친화도를 보였고, 경쟁 실험에서는 생쥐에서 Cn2를 중화한다고 보고된 LR 항체와 같거나 가까운 부위에 붙는 것으로 나타났다([Anthropic](https://www.anthropic.com/research/claude-scorpion-toxin-binder-design)).

회사가 직접 적은 한계가 결과만큼 중요하다. 결합은 재조합(실험실에서 만든) 독소에만 시험했고 독에서 정제한 천연 독소로는 확인하지 않았다. 어떤 설계도 시험관 내 중화나 살아 있는 동물에서의 효능을 시험하지 않았다. 그래서 "해독제를 만들었다고 주장하지 않는다"는 문장이 들어갔다. 다음 단계로는 천연 독소 결합 확인, 패치클램프 기록으로 기능 확인, 생쥐 보호 실험을 들었고, 안전성·안정성·가격과 접근성 문제도 남았다고 했다. 시험한 211개의 서열과 실험 측정값은 Hugging Face에 공개하겠다고 밝혔다. 외부 전문가로는 스페인 CNIO의 수사나 바스케스 토레스와 덴마크공대의 티모시 P. 젠킨스가 "유망한 첫걸음"이라고 평가했다고 적혔다([Anthropic](https://www.anthropic.com/research/claude-scorpion-toxin-binder-design)).

이 캠페인은 처음이 아니다. Anthropic은 8월 18일 자 프리프린트에서 Claude Opus 4.8과 Mythos Preview가 표적 16개에 대해 사람의 설계 개입 없이 결합체를 설계했고, 해석 가능한 표적 15개 가운데 14개에서 결합체를 찾았다고 보고했다([Anthropic PDF](https://www-cdn.anthropic.com/30bf50e22a01388bb29bf077ee3f244531594b7a.pdf)). 두 보고 모두 실험 자체는 외부 수탁 기관이 했지만, 설계·선별·결과 해석과 공개 범위는 회사가 정했다. 현재까지 제3자가 같은 실험을 독립적으로 재현해 공개한 기록은 확인되지 않았다.

## 두 건을 같이 봐야 하는 이유

Anthropic의 6월 프레임워크 2부는 '사회적 복원력' 항목에서 "AI로 가속한 대응수단 개발"을 권고한다. AI 기반 신약 발굴과 단백질 설계로 새로운 대응수단의 개발 기간을 줄이고, AI 개발사와 생물방어 연구기관의 협력에 자금을 대 "필요해지기 전에" 역량을 갖추라는 내용이다. 10월 20일 캠페인은 회사가 스스로 쓴 정책 권고의 한 항목을 자사 모델로 시연한 사례에 가깝다. 같은 프레임워크 1부는 생물무기 역량을 정부가 개입해야 할 재앙적 위험으로 분류한다. 생물학 설계 능력은 두 문서에서 각각 규제 대상과 공공재로 등장하고, 그 능력의 수준을 보여 주는 수치는 아직 회사 발표가 거의 유일한 출처다.

그래서 법안 초안의 설계가 중요해진다. 초안대로면 연방 차원의 개입은 10억 달러·50명이라는 사후적 피해 규모를 '예견 가능하고 임박한' 수준으로 입증할 수 있을 때만 작동하고, 그 사이 공시·제3자 평가·사고 보고를 자체적으로 강화한 주법은 선점된다. 평가자에게 자격 요건이 없다면, 318,484개 설계와 553,052번의 선별 같은 숫자를 외부에서 검증할 주체도 회사가 고른 평가자 또는 회사가 고른 수탁 실험실에 머문다. 유출된 초안이 Anthropic의 최종 입장이 아니라는 점은 회사도 인정했고, 수정 문안은 아직 나오지 않았다.

## 확인할 점

- 법안은 발의되지 않았고 법도 아니다. 조항은 Politico가 공개한 비공개 논의용 초안 기준이며, 이 기사에서는 Politico 원문을 직접 열지 못해 복수의 인용 보도로 확인했다.
- 피해 문턱(10억 달러, 50명 초과)과 선점 범위는 회사가 수정하겠다고 예고한 부분이다. 수정 문안이 나오기 전 조항으로 평가해야 한다.
- 전갈 독소 결합체 수치 318,484개, 553,052쌍, 211개 시험, 17개 적합은 모두 Anthropic 공식 발표 수치다. 실험은 외부 수탁 실험실이 했지만 독립적인 제3자 재현 결과는 아직 없다.
- 17개는 모두 단일 독소 결합체이고 중화 실험과 동물 실험을 거치지 않았다. 해독제가 됐다는 뜻이 아니다.
- 캠페인에 쓰인 모델은 "내부 연구 모델"로만 공개됐다. 공개 모델로 같은 결과가 나오는지는 알 수 없다.

## 출처

- [Anthropic, How Claude designed protein binders against scorpion neurotoxins (2026-10-20)](https://www.anthropic.com/research/claude-scorpion-toxin-binder-design)
- [Anthropic's Advanced AI Framework (2026년 6월, PDF)](https://www-cdn.anthropic.com/files/4zrzovbb/website/0a58d567024a8b448ff15158ebc3625328dfcc1f.pdf)
- [Anthropic, Autonomous de novo protein binder design with Claude (PDF)](https://www-cdn.anthropic.com/30bf50e22a01388bb29bf077ee3f244531594b7a.pdf)
- [TNW, Anthropic to rewrite part of its leaked AI bill after safety backlash (2026-10-20)](https://thenextweb.com/news/anthropic-leaked-ai-safety-bill-backlash-frontier)
- [Transformer, Anthropic's weak AI bill undermines its 'safety first' approach (2026-10-19)](https://www.transformernews.ai/p/anthropic-leaked-ai-bill-undermines-safety-first-approach)
- [Interesting Engineering, Anthropic's confidential draft bill to Congress](https://interestingengineering.com/ai-robotics/anthropic-confidential-congress-draft-bill)
- [Anthropic AI policy](https://www.anthropic.com/policy)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
