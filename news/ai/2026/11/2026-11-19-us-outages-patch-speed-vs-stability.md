---
title: 미국을 닷새 동안 멈춘 것은 AI가 아니라 '변경'이었다…AI가 취약점을 기계 속도로 찾자 '즉시 고쳐라'와 '충분히 시험하라'가 부딪치기 시작했다
slug: 2026-11-19-us-outages-patch-speed-vs-stability
topic: ai
published_at: 2026-11-19T11:43:00+09:00
summary: 11월 12~17일 마이크로소프트, 미 연방항공청(FAA), 체이스, 국가안보국(NSA)이 잇따라 멈췄다. 'AI가 찾은 취약점을 급히 고치다 생긴 장애'라는 설명은 NSA 한 곳에서만 실명으로 확인되고, 마이크로소프트·FAA·체이스는 AI와의 관련을 부인했다. 이 글은 공통점이 AI가 아니라 공격 없이 일어난 변경이라고 본다. 그리고 AI가 취약점 발견 속도를 바꾼 지금, 패치 속도만 재는 규정이 그 변경을 더 위험하게 만든다고 판단한다.
tags:
  - 시스템 장애
  - 보안 패치
  - AI 취약점 발견
  - 변경관리
  - NSA
  - 마이크로소프트
  - FAA
  - 전자금융감독규정
  - CISA
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-11-20
      note: 마이크로소프트 365 장애 최종 사후 보고서(11월 20일 예정)의 근본 원인과 재발 방지책
---

# 미국을 닷새 동안 멈춘 것은 AI가 아니라 '변경'이었다…AI가 취약점을 기계 속도로 찾자 '즉시 고쳐라'와 '충분히 시험하라'가 부딪치기 시작했다

## 판단: 공격은 없었고, 바꾸다가 무너졌다

11월 12일부터 17일까지 미국에서 마이크로소프트 365, 연방항공청(FAA) 관제 통신망, 인사관리 서비스 워크데이, 체이스·웰스파고 은행, 국가안보국(NSA) 기밀망이 차례로 멈췄다. 17일 저녁 워싱턴선은 익명 소식통 3명을 인용해 월가 임원들과 NSA가 의회에 장애 원인을 'AI가 찾은 취약점을 고치려는 패치'로 설명했다고 보도했다. 한 의회 관계자는 "한꺼번에 너무 많은 패치를 밀어 넣고 있다. 시스템이 설계된 한도 이상으로"라고 했다([워싱턴선](https://www.washingtonsun.com/technology/bank-ceos-nsa-tell-congress-ai-driven-patches-behind-outages)).

이 글의 판단은 세 가지다. **첫째, 닷새의 장애를 'AI 패치' 하나로 묶는 것은 틀렸다.** 실명으로 확인되는 AI 패치 사례는 NSA 하나이고, 마이크로소프트·FAA·체이스는 AI와의 관련을 직접 부인했다. **둘째, 그래도 이 장애들에는 공통점이 있다. 공격이 없었는데 시스템을 바꾸는 과정에서 무너졌다는 점이다.** 그리고 AI는 지금 그 '바꿔야 할 양'을 전례 없이 키우고 있다. **셋째, 규정은 패치 속도만 잰다.** 미국과 한국의 규정 모두 '빨리 고쳐라'는 시한은 점점 짧게 적는데, 고친 뒤 시스템이 다시 올라오는지는 따로 묻지 않는다. 둘째와 셋째는 해석이다.

## 닷새, 다섯 개의 원인

| 날짜 | 장애 | 공식 설명 | AI 관련 |
|---|---|---|---|
| 11월 12~13일 | 마이크로소프트 365(아웃룩·팀즈 등) | 7월부터 배포한 네트워킹 게이트웨이 수정본의 잠복 결함, 팀즈 트래픽 이동, 용량 약 14% 감소가 겹침 | 회사가 공격·AI 에이전트 관여 징후 없다고 밝힘 |
| 11월 13일 | FAA 전국 지상정지(약 5시간) | 아칸소 원격 사이트에서 계약업체가 구리선을 광케이블로 바꾸고 새 라우터를 달던 중 낡은 통신망이 과부하 | FAA 청장 "AI 관련 증거 전혀 없다" |
| 11월 13일 | 워크데이 | 회사는 조사 중이라며 사과. 원인은 공식 보고서 없음 | 확인 안 됨 |
| 11월 16일 | 체이스·웰스파고 | 체이스는 "온프레미스 하드웨어 시스템의 소프트웨어 버그", 웰스파고는 원인 미공개 | 체이스는 AI로 찾거나 고친 버그가 아니라고 밝힘 |
| 11월 17일 | NSA 기밀망 | NSA는 "예정된 정기 점검 중 일시적 성능 저하" | 국가정보장이 패치 탓이라고 발언 |

마이크로소프트는 예비 사후 보고서에서 문제의 변경이 7월에 배포돼 자동 롤백이 통하지 않았고, 시험이 저사양 장비 위주여서 코어가 많은 신형 장비에서 생기는 결함을 놓쳤다고 설명했다([사이버시큐리티뉴스](https://cybersecuritynews.com/microsoft-outage-incident-report/)). FAA는 낡은 시분할(TDM) 통신망이 불안정해졌다고 했고, 브라이언 베드퍼드 청장은 "악의적인 것의 증거도, AI와 관련된 것의 증거도 전혀 없다"고 했다. 더피 교통장관은 "아주 외딴 곳에서 한 꽤 단순한 작업"이었다고 했다([테크크런치](https://techcrunch.com/2026/11/14/transportation-secretary-blames-routine-equipment-upgrade-for-grounding-flights-nationwide/), [더스택](https://www.thestack.technology/faa-blames-legacy-tdm-network-for-nationwide-flight-grounding)). 체이스는 포춘에 이번 버그가 AI로 찾거나 고친 것이 아니라고 밝혔다([포춘](https://fortune.com/2026/11/18/ai-played-a-major-role-in-the-nsa-banking-outages-but-not-in-the-way-you-may-think)).

NSA만 다르다. 제이 클레이턴 국가정보장은 17일 폭스비즈니스 인터뷰에서 "이 취약점들이 확인됐기 때문에 많은 기관이 패치하고 있다"며 "그 뒤 진행된 패치 때문에 일부 시스템이 패치 후 예상대로 다시 올라오지 않았다. 오늘 NSA에서 일어난 일이 그것"이라고 했다. 그는 "조직적 사이버공격의 징후는 보이지 않는다"고 덧붙였다([폭스비즈니스](https://www.foxbusiness.com/technology/jay-clayton-addresses-concerns-amid-widespread-tech-outages)). 더레코드는 이 패치가 연구자들이 AI 도구의 도움으로 찾은 PHP 취약점을 막기 위한 것이라고 전했다([더레코드](https://therecord.media/nsa-net-disruptions)). 클레이턴은 다음 날 하원 국토안보위원회에서 장애들을 "유지보수와 기술 변경과 관련된 별개의 서비스 장애"라고 정리했다([PBS](https://www.pbs.org/newshour/politics/watch-intelligence-official-pressed-to-explain-cause-of-national-security-agency-outage)).

워싱턴선 보도는 제목에 '은행 CEO들'을 넣었지만 본문은 '월가 임원들'이고 실명 인용은 없다. 독일 IT 매체 하이제는 의원들이 말한 범위가 NSA와 JP모건 장애였고 마이크로소프트와 FAA는 포함되지 않았다고 짚었다. 마크 워너 상원의원실은 포춘에 "엉성한 패치 적용"이 NSA와 은행 장애에 연결돼 있다고 했지만, 체이스의 부인과 맞지 않는다([포춘](https://fortune.com/2026/11/18/ai-played-a-major-role-in-the-nsa-banking-outages-but-not-in-the-way-you-may-think)). 지금 확인된 것은 여기까지다.

## 그래도 압력은 실재한다

장애 하나하나를 AI 탓으로 돌릴 수는 없지만, AI가 방어자에게 지운 짐은 숫자로 보인다. 마이크로소프트는 10월 정기 보안 업데이트에서 1,400건이 넘는 취약점을 고쳐 9월의 종전 최대 기록(964건)을 46% 넘었다([비카리우스](https://www.vicarius.io/articles/microsoft-october-2026-patch-tuesday), [PC월드](https://www.pcworld.com/article/3260668/microsoft-breaks-record-fixing-1416-security-flaws-update-windows-now.html)). 더스택은 9월에 이미 마이크로소프트가 2026년 들어 낸 패치가 2024년과 2025년을 합친 것보다 많다고 썼다([더스택](https://www.thestack.technology/runtime-the-smallest-patch-tuesday-of-the-rest-of-your-life/)). 공개 취약점(CVE) 발행 건수는 10월 말까지 약 9만 건으로, 2025년 한 해(약 5만 건)를 크게 넘었다([NVD 월별 집계](https://github.com/jgamblin/monthlyCVEStats)).

10월에는 AI 모델의 도움으로 찾은 PHP 인터프리터 원격 코드 실행 취약점이 공개됐다. 크리스 크렙스 전 미국 사이버보안·인프라보안청(CISA) 국장은 CNBC에 "지금까지 발견된 치명적 취약점 전체의 3%가 지난 한 달 사이에 나왔다"고 했다([CNBC](https://www.cnbc.com/2026/10/23/php-vulnerabilities-ai-cybersecurity.html)). 뱅크오브아메리카의 브라이언 모이니핸 CEO는 10월 AI 모델이 드러낸 결함을 고치려고 외부 계약직 약 1,000명을 추가했다고 밝혔다([IT프로](https://www.itpro.com/technology/artificial-intelligence/bank-of-america-hired-1-000-security-consultants-to-address-mythos-spotted-flaws)). 한 보안업체 CEO는 포춘에 "AI는 이제 기계 속도로 취약점을 찾는데, 우리의 시험·배포 안전장치는 여전히 사람 속도에 묶여 있다"고 했다. 반대 의견도 있다. 래피드7의 크리스티안 베크는 복잡한 시스템은 적대 세력보다 "지루한 이유로" 훨씬 자주 실패한다며, 서두른 보안 업데이트가 이번 장애를 일으켰다는 공개 증거는 없다고 했다([TNW](https://thenextweb.com/news/us-outages-patches-ai-found-flaws-nsa-banks-washington-sun)).

이 글은 두 말이 모두 맞다고 본다. 이번 장애 대부분은 지루한 이유로 일어났다. 그러나 지루한 실패의 확률은 바꾸는 횟수에 비례한다. 1년 사이 고쳐야 할 취약점이 두 배가 되면, 시험과 배포를 사람 속도로 하는 조직에서는 같은 확률의 실수가 두 배로 일어난다. 이는 해석이다.

## 2년 전의 교훈과 지금의 시한이 부딪친다

2024년 7월 19일 크라우드스트라이크의 보안 업데이트 하나가 윈도 기기 약 850만 대를 멈췄다([마이크로소프트](https://blogs.microsoft.com/blog/2024/07/20/helping-our-customers-through-the-crowdstrike-outage/)). 크라우드스트라이크가 내놓은 재발 방지책은 소수 기기에 먼저 배포한 뒤 문제가 없을 때만 배포 범위를 차례로 넓히고 문제가 생기면 되돌리는 단계 배포였다([크라우드스트라이크](https://www.crowdstrike.com/blog/falcon-content-update-preliminary-post-incident-report/)). 업계가 그 사고에서 배운 것은 보안 업데이트일수록 천천히 넓히라는 것이었다.

2년 뒤의 규정은 반대 방향을 가리킨다. CISA는 6월 구속력 있는 운영지침(BOD 26-04)으로 외부에 노출돼 있고, 완전 자동화 공격이 가능하며, 시스템 장악이 가능하고, 실제 악용 증거가 있는 취약점을 3일 안에 조치하라고 연방기관에 요구했다. CISA는 AI가 새 취약점 발견 속도를 "크게 높이고" 있고 방어자들이 "이미 따라가기 벅차다"고 설명했다([사이버스쿱](https://cyberscoop.com/cisa-vulnerability-remediation-directive-bod-26-04/)). 지침은 패치의 시한을 정하지만, 패치가 시스템을 멈출 위험을 어떻게 관리할지는 다루지 않는다. 클레이턴 국가정보장의 말로는 FBI와 NSA가 "내리고, 패치를 넣으라"고 말해 왔다. 단계 배포는 시간을 들이는 방식이고, 3일 시한은 그 시간을 줄이라는 압력이다.

```mermaid
flowchart LR
    A[AI가 취약점을 기계 속도로 발견] --> B[고쳐야 할 패치 급증]
    B --> C{규정의 요구}
    C --> D[즉시 고쳐라 3일 시한]
    C --> E[충분히 시험하고 단계 배포하라]
    D --> F[시험 생략 압력]
    E --> G[노출 시간 증가]
    F --> H[공격 없는 장애]
    G --> I[공격 위험]
```

## 한국의 규정은 한 문서 안에서 부딪친다

한국 금융권 규정은 이 충돌을 한 고시 안에 담고 있다. 전자금융감독규정 제14조는 금융회사가 "정보처리시스템의 긴급하고 중요한 보정(patch)사항에 대하여는 즉시 보정 작업을 할 것"을, 제15조는 해킹에 대비한 긴급하고 중요한 보정사항에 대해 "즉시 보정작업 실시"를 요구한다. 같은 규정 제29조는 프로그램의 등록·변경·폐기 절차를 세우라고 하고, 개정 전 조문은 운영시스템 적용은 "충분한 테스트 및 관련 책임자 승인 후 실시할 것"이라고 적었다([전자금융감독규정 제2025-4호](https://ko.wikisource.org/wiki/%EC%A0%84%EC%9E%90%EA%B8%88%EC%9C%B5%EA%B0%90%EB%8F%85%EA%B7%9C%EC%A0%95_%28%EC%A0%9C2025-4%ED%98%B8%29)). 패치가 1년에 몇 번이던 시절에는 '즉시'와 '충분한 시험'이 함께 지켜질 수 있었다. 한 회사의 패치가 한 달에 1,000건을 넘기 시작한 지금은 둘 중 하나를 고르게 된다.

정부도 같은 말을 한다. 과기정통부와 한국인터넷진흥원(KISA)은 10월 22일 PHP 취약점에 대해 사이버위기 경보를 '주의'로 올리며 "최신 버전으로 즉시 업데이트해야 한다"고 당부했다([정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148974113)). KISA에 들어온 취약점 신고는 2025년 2,525건으로 제도 시행 이후 가장 많았고 10년 새 3.6배가 됐다([국민일보](https://v.daum.net/v/20260616185248854)). 한국은 유지보수 작업 하나가 국가 전산망을 멈춘 경험도 이미 했다. 2025년 9월 국가정보자원관리원 대전센터에서 배터리 이설 작업 중 불이 나 정부 시스템 709개가 멈췄고, 전면 복구까지 약 95일이 걸렸다([경향신문](https://www.khan.co.kr/article/202512301118001)). FAA의 이번 장애도 '꽤 단순한' 정기 작업에서 시작됐다.

전날 이 사이트는 한국 은행을 뚫은 AI 침투 도구가 외부에 열린 주변 시스템을 노렸다고 썼다([관련 기사](https://now.zeta4.net/a/2026-11-18-fbi-artex-flash-korean-banks-perimeter)). 공격 쪽은 AI로 빨라졌고, 방어 쪽은 AI가 찾은 구멍을 메우느라 스스로 넘어지고 있다. 둘은 같은 현상의 양면이다. 이는 해석이다.

## 무엇을 바꿔야 하나

1. **패치 속도와 장애율을 함께 보고하게 한다.** 지금 규정과 평가는 '얼마나 빨리 고쳤나'를 잰다. 같은 보고서에 '고친 뒤 몇 번 시스템이 멈췄나'(변경 실패율)를 넣지 않으면, 기관은 시한을 지키려고 시험을 줄인다.
2. **'즉시'의 범위를 좁히고 순서를 정한다.** CISA 지침이 외부 노출과 실제 악용 같은 기준을 둔 것처럼, 전자금융감독규정의 '긴급하고 중요한'을 구체적 기준으로 바꾸고 그 밖의 패치는 단계 배포를 의무로 해야 한다. 외부에 노출된 시스템부터 고치는 것이 공격 쪽 교훈과도 맞는다.
3. **되돌리기를 먼저 확인한다.** 마이크로소프트의 이번 장애가 길어진 이유 하나는 몇 달 전 배포한 변경이라 자동 롤백이 안 됐다는 점이다. 패치 계획에 '어떻게 되돌릴지'가 없으면 즉시 패치는 즉시 장애가 될 수 있다.

## 확인하지 못한 것

- 'AI가 찾은 취약점 패치가 장애 원인'이라는 워싱턴선 보도는 익명 소식통 3명에 기댄다. NSA는 워싱턴선 질의에 답하지 않았고, 공식 성명은 '정기 점검'이라고만 했다. NSA 장애를 처음 보도한 CNN 기사는 열지 못했다.
- 웰스파고와 워크데이는 공식 원인을 밝히지 않았다. 워크데이의 재해복구 시험 관련 설명은 2차 보도뿐이다.
- FAA 장애로 인한 결항은 금요일 하루 약 9,000~1만 2,000편, 주말 포함 1만 7,000편 안팎으로 집계마다 다르다. 일부 보도의 '2만 편 이상'은 원문을 확인하지 못했다.
- 마이크로소프트 10월 패치 건수는 업체마다 1,407~1,416건으로 다르다. CVE 연간 건수도 집계 방식에 따라 차이가 있다.
- 전자금융감독규정은 2025년 2월 시행본으로 확인했고, 2026년 7월 개정 고시와 시행세칙 원문은 대조하지 못했다. '충분한 테스트' 문구는 개정 전 조문이며 현재는 세칙으로 옮겨진 것으로 보인다.
- 2026년 국내 금융권에서 보안 패치가 직접 원인이 된 전산장애 사례는 찾지 못했다.

## 출처

- [Bank CEOs, NSA Tell Congress That AI-Driven Patches Are Behind Outages — 워싱턴선 (2026-11-17)](https://www.washingtonsun.com/technology/bank-ceos-nsa-tell-congress-ai-driven-patches-behind-outages)
- [Jay Clayton addresses concerns amid widespread tech outages — 폭스비즈니스 (2026-11-17)](https://www.foxbusiness.com/technology/jay-clayton-addresses-concerns-amid-widespread-tech-outages)
- [NSA network disruptions — 더레코드 (2026-11-17)](https://therecord.media/nsa-net-disruptions)
- [Intelligence official pressed to explain cause of NSA outage — PBS (2026-11-18)](https://www.pbs.org/newshour/politics/watch-intelligence-official-pressed-to-explain-cause-of-national-security-agency-outage)
- [AI played a major role in the NSA, banking outages — but not in the way you may think — 포춘 (2026-11-18)](https://fortune.com/2026/11/18/ai-played-a-major-role-in-the-nsa-banking-outages-but-not-in-the-way-you-may-think)
- [Chase, Wells Fargo, Capital One bank outages — 포춘 (2026-11-16)](https://fortune.com/2026/11/16/chase-bank-wells-fargo-capital-one-bank-outages/)
- [US outages, patches and AI-found flaws — TNW (2026-11-18)](https://thenextweb.com/news/us-outages-patches-ai-found-flaws-nsa-banks-washington-sun)
- [Microsoft outage incident report — 사이버시큐리티뉴스 (2026-11-16)](https://cybersecuritynews.com/microsoft-outage-incident-report/)
- [Transportation secretary blames routine equipment upgrade for grounding flights nationwide — 테크크런치 (2026-11-14)](https://techcrunch.com/2026/11/14/transportation-secretary-blames-routine-equipment-upgrade-for-grounding-flights-nationwide/)
- [FAA blames legacy TDM network for nationwide flight grounding — 더스택 (2026-11-16)](https://www.thestack.technology/faa-blames-legacy-tdm-network-for-nationwide-flight-grounding)
- [Microsoft October 2026 Patch Tuesday — 비카리우스](https://www.vicarius.io/articles/microsoft-october-2026-patch-tuesday)
- [Microsoft breaks record fixing 1,416 security flaws — PC월드](https://www.pcworld.com/article/3260668/microsoft-breaks-record-fixing-1416-security-flaws-update-windows-now.html)
- [The smallest Patch Tuesday of the rest of your life — 더스택 (2026-09-10)](https://www.thestack.technology/runtime-the-smallest-patch-tuesday-of-the-rest-of-your-life/)
- [Monthly CVE statistics — 제리 갬블린 NVD 집계](https://github.com/jgamblin/monthlyCVEStats)
- [PHP vulnerabilities and AI cybersecurity — CNBC (2026-10-23)](https://www.cnbc.com/2026/10/23/php-vulnerabilities-ai-cybersecurity.html)
- [Bank of America hired 1,000 security consultants — IT프로](https://www.itpro.com/technology/artificial-intelligence/bank-of-america-hired-1-000-security-consultants-to-address-mythos-spotted-flaws)
- [CISA vulnerability remediation directive BOD 26-04 — 사이버스쿱 (2026-06-10)](https://cyberscoop.com/cisa-vulnerability-remediation-directive-bod-26-04/)
- [Helping our customers through the CrowdStrike outage — 마이크로소프트 (2024-07-20)](https://blogs.microsoft.com/blog/2024/07/20/helping-our-customers-through-the-crowdstrike-outage/)
- [Falcon content update preliminary post incident report — 크라우드스트라이크](https://www.crowdstrike.com/blog/falcon-content-update-preliminary-post-incident-report/)
- [전자금융감독규정(금융위원회고시 제2025-4호) — 위키문헌](https://ko.wikisource.org/wiki/%EC%A0%84%EC%9E%90%EA%B8%88%EC%9C%B5%EA%B0%90%EB%8F%85%EA%B7%9C%EC%A0%95_%28%EC%A0%9C2025-4%ED%98%B8%29)
- [PHP 취약점 사이버위기 경보 '주의' 상향 — 대한민국 정책브리핑 (2026-10-22)](https://www.korea.kr/news/policyNewsView.do?newsId=148974113)
- [KISA 취약점 신고 역대 최다 — 국민일보 (2026-06-16)](https://v.daum.net/v/20260616185248854)
- [국정자원 화재 시스템 전면 복구 — 경향신문 (2025-12-30)](https://www.khan.co.kr/article/202512301118001)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
