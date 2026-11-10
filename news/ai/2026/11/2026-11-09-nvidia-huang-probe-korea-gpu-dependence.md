---
title: 젠슨 황 한 사람에게 걸어 둔 한국의 AI 인프라…엔비디아 이사회 조사와 매디슨 황 방한 취소가 드러낸 것
slug: 2026-11-09-nvidia-huang-probe-korea-gpu-dependence
topic: ai
published_at: 2026-11-09T07:46:00+09:00
tags:
  - 엔비디아
  - 젠슨 황
  - GPU
  - HBM
  - 수출통제
  - 과기정통부
  - 한국
summary: 엔비디아 이사회는 8일 젠슨 황 CEO가 외국 정보기관의 표적이 됐다는 보도에 따라 독립 조사를 열었고, 황은 직원들에게 "아내에게 부정했다"고 인정했다. 미 하원 3개 위원회는 18일 비공개 브리핑을 요구한다. 같은 주말 젠슨 황의 딸 매디슨 황은 배경훈 부총리 면담을 포함한 방한 일정을 취소했다. 이 글은 스파이 의혹의 진위보다, 한국의 AI 인프라 계획이 한 회사와 한 사람과의 관계 위에 세워져 있다는 점을 문제로 본다.
generated_by: claude
model: unspecified
updated_at: 2026-11-11T08:48:00+09:00
tracking:
  status: ongoing
  last_update:
    at: 2026-11-11T08:48:00+09:00
    note: 하원 외교위 매스트 위원장 10일 "아직 답을 들었다고 말할 수 없다". 회신 기한 11일(미국 시각) 결과 미확인
  checkpoints:
    - date: 2026-11-12
      note: 젠슨 황의 하원 3개 위원회 브리핑(18일) 회신 기한(11일, 미국 시각) 결과와 의회 후속 조치
    - date: 2026-11-18
      note: 엔비디아 3분기 실적 발표(17일)와 하원 비공개 브리핑(18일) 결과
    - date: 2026-12-31
      note: 엔비디아 이사회 독립 조사 결과 공개 여부, 한국 정부의 엔비디아 협력 일정 재조정 여부
---

# 젠슨 황 한 사람에게 걸어 둔 한국의 AI 인프라…엔비디아 이사회 조사와 매디슨 황 방한 취소가 드러낸 것

## 판단: 문제는 의혹이 아니라 의존의 구조다

엔비디아 이사회는 8일(현지시각) "창업자이자 CEO인 젠슨 황이 외국 정보활동의 표적이 됐다는 최근 보도에 따라" 독립 조사를 시작한다고 밝혔다. 사외이사 위원회가 외부 독립 법률대리인의 지원을 받아 조사를 맡고, 이사회는 "국가안보나 엔비디아의 기밀이 침해됐다고 볼 이유는 없지만 모든 정보를 검토할 것"이라고 했다. 같은 날 황은 전 직원에게 보낸 이메일에서 "나는 아내에게 부정했다. 내 행동은 아내와 아이들에게 상처를 줬다. 변명의 여지가 없다"고 썼다. 회사는 "오늘의 소식이 엔비디아를 늦추지 않을 것"이며 황이 "중단 없이" CEO직을 수행한다고 했다([CNBC](https://www.cnbc.com/2026/11/08/nvidia-jensen-huang-email-board-of-directors-statement.html), [CNBC](https://www.cnbc.com/2026/11/08/nvidia-jensen-huang-investigation-china-spy.html)).

이 글의 판단은 이렇다. **한국에 중요한 질문은 젠슨 황이 무엇을 했느냐가 아니라, 한국의 AI 인프라 계획이 왜 이 한 사람의 거취에 흔들리는 구조인가다.** 26만 장 GPU 계획도, 피지컬 AI 협력도, 부총리 면담도 엔비디아라는 한 회사와 황 일가라는 창구에 걸려 있다. 이번 주말 그 창구가 닫혔을 때 한국이 가진 대안이 무엇인지가 드러났다.

## 확인된 것과 보도된 것을 나눠 보면

확인된 사실과 익명 취재원 보도, 그리고 회사의 주장은 무게가 다르다. 이 사건은 그 셋이 뒤섞여 있다.

| 구분 | 내용 | 출처 |
|---|---|---|
| 공식 문서 | 하원 외교위·중국특위·정보위 위원장이 11월 4일자 서한으로 11월 18일 비공개 합동 브리핑을 요청. 앨리스 황을 "공개 보도된 중국 정보자산"이라고만 쓰고 출처는 적지 않음. 11월 11일까지 회신 요구 | [하원 외교위](https://foreignaffairs.house.gov/sites/evo-subsites/republicans-foreignaffairs.house.gov/files/evo-media-document/11.4.26nvidialetter.pdf) |
| 본인 인정 | 황이 8일 이메일에서 외도를 인정. 상대는 특정하지 않았고 스파이 의혹은 언급하지 않음 | [CNBC](https://www.cnbc.com/2026/11/08/nvidia-jensen-huang-email-board-of-directors-statement.html) |
| 회사 조치 | 이사회 독립 조사 개시. "기밀 침해를 믿을 이유 없음" | [CNBC](https://www.cnbc.com/2026/11/08/nvidia-jensen-huang-email-board-of-directors-statement.html) |
| 익명 보도 | NYT(10월 29일): 미 당국이 메가스피드 임원 앨리스 황을 중국에 정보를 넘기는 자산으로 결론, 감시 과정에서 황과의 "가까운 관계" 파악, 트럼프는 1년 전 보고받고 조치하지 않음. FT(7일): 정보당국 메모가 두 사람을 연인 관계로 보고 앨리스 황이 국가안전부에 포섭됐다고 평가. NYT(8일): 루비오 국무장관이 메모 작성을 주도 | [NYT(GV Wire 전재)](https://gvwire.com/2026/10/29/nvidia-chief-seen-as-target-of-chinese-spy-plot/), [Investing.com(FT 인용)](https://ca.investing.com/news/stock-market-news/us-intelligence-memo-ties-nvidias-huang-to-alleged-chinese-spy-ft-reports-4941137), [CNBC](https://www.cnbc.com/2026/11/08/jensen-huang-nvidia-china-spy-congress.html) |
| 정부 확인 | 없음. 백악관·CIA·국무부는 논평을 거부했고 메모는 공개되지 않았다. 기소된 사람은 없다 | [CNBC](https://www.cnbc.com/2026/11/08/jensen-huang-nvidia-china-spy-congress.html) |
| 부인 | 중국 외교부 "근거 없는 추측", 싱가포르 내무부는 자국 당국이 두 사람 관계를 우려했다는 보도를 부인 | [타이베이타임스(AFP)](https://taipeitimes.com/News/world/archives/2026/10/31/2003866928) |

황 본인은 10월 29일 "우리의 관계와 교류는 메가스피드와 관련된 것이었고 완전히 정상적이었다"고 했고, 엔비디아는 밀반입 의혹이 "지난해 철저히 조사돼 반박됐다"고 했다([디칸 크로니클(블룸버그)](https://www.deccanchronicle.com/amp/technology/nvidia-ceo-jensen-huang-says-ties-to-company-in-spy-probe-were-normal-2000242)). 열흘 뒤 나온 이메일은 '정상적인 교류'라는 설명과 '부정'이라는 고백 사이의 거리를 남겼다. 다만 이메일이 FT 보도의 특정 인물이나 스파이 평가를 확인한 것은 아니다.

메가스피드는 싱가포르 경찰의 수사 대상이고, NYT는 말레이시아 자매사가 2024년 6월부터 2026년 2월까지 엔비디아 칩을 포함한 AI 장비를 최소 48억 달러어치 샀으며 미 상무부 조사가 법무부로 넘어갔다고 전했다. 트럼프 대통령은 10월 31일 "젠슨을 매우 존경한다", "아주 면밀히 살펴보겠다"고 했다([ARY(AFP)](https://arynews.tv/trump-us-looking-closely-report-nvidia-ceo-target-china-spy-plot)).

회신 기한을 하루 앞둔 10일(현지시각) 브라이언 매스트 하원 외교위원장은 "아직 답을 들었다고 말할 수 없다"고 했다([CNBC](https://www.cnbc.com/2026/11/10/moolenaar-nvidia-jensen-huang-affair-chinese-spy.html)). 세 위원장은 5일 보도자료에서 11일까지 18일 브리핑을 수락하거나 다른 날짜를 제안하라고 요구했다([하원 외교위](https://foreignaffairs.house.gov/news/press-releases/chairmen-mast-moolenaar-and-crawford-request-jensen-huang-brief-congress-on-link-to-chinese-intelligence-asset)).

## 서울: 창구가 닫힌 주말

젠슨 황의 딸 매디슨 황 엔비디아 수석이사는 8일 서울 콘래드호텔에서 배경훈 부총리 겸 과기정통부 장관을 만나고, 9~10일 코엑스 'AI 데이 서울'에 참석하며, 9일 류제명 2차관과 스타트업 포럼을 공동 주재하고 리벨리온 본사를 찾을 예정이었다. 엔비디아는 7일 그가 "부득이한 사정으로" 참석하지 못한다고 알렸고, 연합뉴스는 소식통을 인용해 "가족 문제"라고 전했다. 과기정통부는 "면담 불발은 아쉽지만 예정된 협력과 간담회는 차질 없이 진행한다"고 했다([ZDNet Korea](https://zdnet.co.kr/view/?no=20261108115633), [코리아타임스(연합)](https://www.koreatimes.co.kr/business/companies/20261107/nvidia-ceos-daughter-cancels-planned-visit-to-korea-sources), [한국일보](https://www.hankookilbo.com/news/article/A2026110810050001381)). 취소와 의혹의 연관은 어느 보도도 확인하지 못했다. 행사는 다른 임원들이 대신 나와 예정대로 열린다.

매디슨 황은 올해만 세 번 방한해 삼성, SK하이닉스, LG, 현대차, 두산로보틱스와 피지컬 AI 협력을 논의한 사실상의 창구였다. 이번이 네 번째가 될 예정이었다. **한 사람의 일정이 바뀌자 부총리 면담과 차관 포럼 공동 주재가 같이 사라졌다.** 이것이 이 글이 보는 문제다. 협력의 통로가 제도가 아니라 사람이었다.

## 의존의 크기

지난해 10월 경주 APEC에서 엔비디아는 한국 전체에 26만 장 넘는 GPU를 공급하겠다고 발표했다. 정부 최대 5만, 삼성 5만 이상, SK 5만 이상, 현대차 5만, 네이버클라우드 6만 이상이다([엔비디아](https://nvidianews.nvidia.com/news/south-korea-ai-infrastructure)). 올해 6월 황이 방한했을 때 배 부총리는 "모든 정책적 지원을 아끼지 않겠다"고 했다([뉴시스](https://mobile.newsis.com/view/NISX20260608_0003661166)). 국감 자료에 따르면 정부분 가운데 실제 서비스 중인 것은 지난해 추경분 1만 3,100장이고, 올해 협약분 9,704장 중 10월 8일까지 반입은 2,608장이다([ZDNet Korea](https://zdnet.co.kr/view/?no=20261014164011)). 나머지는 약속이다.

반대 방향의 의존도 크다. 삼성전자와 SK하이닉스의 HBM 매출은 엔비디아 발주에 좌우되고, 지난주 코스피는 데이터센터 규제 우려로 사흘간 10% 넘게 빠졌다. 엔비디아 주가는 5일 9.26% 떨어졌다가 6일 2.78% 반등했는데, 그날의 하락을 의혹과 연결한 주요 보도는 없다([StockAnalysis](https://stockanalysis.com/stocks/nvda/history/)). 시장은 아직 이 사건을 가격에 넣지 않았다.

그러나 위험은 있다. 엔비디아는 연차보고서에서 통제 품목의 전용(diversion) 보도는 "근거가 없고 사실이 아니더라도 사업에 부정적 영향을 줄 수 있다"고 적었고, 수출통제가 "파트너, 공급업체, 고객에게 복잡하고 부담스러운 준수 의무"를 지운다고 썼다([엔비디아 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)). 그 고객과 공급업체에 한국 기업이 있다. 의회가 18일 브리핑에서 메가스피드 경로를 파고들면 다음 단계는 아시아 데이터센터와 재판매 경로에 대한 더 촘촘한 통제다. 한국 기업은 그 통제의 대상이 아니라 준수 비용을 떠안는 쪽이 된다. 이는 해석이다.

## 9일 서울: 행사는 열렸고, 질문엔 답이 없었다

'AI 데이 서울'은 매디슨 황 없이 열렸다. 엔비디아, SK텔레콤, 리벨리온은 과기정통부 지원 아래 NVLink Fusion으로 엔비디아 GPU와 리벨리온 NPU를 한 시스템에 묶는 MOU를 맺었다. 프리필은 GPU가, 디코드는 NPU가 맡는 구조로 SKT AI 데이터센터에 2028년 도입이 목표다. 이도규 과기정통부 정보통신정책실장은 "오늘의 MOU가 선언에 그치지 않고 글로벌 시장 진출이라는 가시적인 성과로 이어지는 것이 중요하다"고 했다([파이낸셜뉴스](https://www.fnnews.com/news/202611091444371881)). 과기정통부는 다른 국산 NPU 기업으로도 넓히겠다고 했다. 엔비디아는 매디슨 황의 불참 사유와 의혹 관련성에 답하지 않았고, GPU·HBM 영향 질문에는 "행사와 무관하다"고 했다([재경일보](https://news.jkn.co.kr/post/1080731)). 엔비디아 주가는 9일 프리마켓에서 5.2% 내렸고 중국 외교부는 "이른바 중국 스파이 서사"에 근거가 없다고 했다([CNBC](https://www.cnbc.com/2026/11/09/nvidia-jensen-huang-chinese-spy-investigation.html)).

이 MOU는 이 글이 말한 방향과 겹친다. 엔비디아 플랫폼 안에서 국산 NPU에 자리를 만드는 것은 의존을 끊는 일이 아니라 의존의 조건을 바꾸는 일이다. 2028년이라는 시점과 '확대 방침'이 계약으로 이어지는지가 다음 확인 지점이다. 이는 해석이다.

9일 미국 시장에서 엔비디아는 4.27% 내린 178.67달러로 마감했고 거래량은 3개월 평균의 3.7배였다. 같은 날 나스닥은 2.74% 올랐다([Motley Fool](https://www.fool.com/coverage/stock-market-today/2026/11/09/stock-market-today-nov-9-nvidia-stock-plunges-4-on-jensen-huang-investigation-as-nasdaq-surges-nearly-3/)). 시장 전체가 반등하는 날 이 종목만 빠졌다는 것은 하락 이유가 거시가 아니라 이 회사라는 뜻이다. 하원이 요구한 11일 회신 여부는 10일 밤까지 공개되지 않았다.

## 영향 평가

| 대상 | 영향 | 판단 |
|---|---|---|
| 엔비디아 경영 | 이사회 조사, 의회 브리핑, 17일 실적이 2주 안에 몰림 | 애널리스트 댄 아이브스는 조사 결과에 따라 CEO 교체 위험이 있다고 봤다([Yahoo Finance](https://finance.yahoo.com/markets/article/nvidias-jensen-huang-admits-to-affair-after-allegations-of-romance-with-chinese-spy-report-205122263.html)). 회사는 부인한다 |
| 한국 정부 GPU 계획 | 발표된 26만 장 중 계약으로 묶인 비중이 공개되지 않음 | 계약과 납기를 공개해야 한다. 약속의 상대가 흔들릴 때 약속의 형식이 중요해진다 |
| 삼성·SK하이닉스 | 단기 발주 영향 없음. 수출통제 강화 시 준수 비용 증가 | 고객 다변화가 다시 과제가 된다 |
| 피지컬 AI 협력 | 창구였던 인물의 방한 취소 | 기업 간 실무 채널로 옮겨야 한다. 리벨리온 같은 국산 NPU 기업과의 협력은 엔비디아 일정과 무관하게 진행돼야 한다 |
| 과기정통부 | 부총리·차관 일정이 한 회사 임원 방문에 맞춰 짜임 | 국가 AI 전략의 대외 일정이 특정 기업의 가족 행사가 돼서는 안 된다 |

## 한국이 해야 할 일

1. **약속을 계약으로 바꾼다.** 26만 장 가운데 계약, 발주, 반입을 구분해 공개하고, 2027년 베라루빈 1만 장 도입의 조건을 명시해야 한다.
2. **창구를 제도로 바꾼다.** 엔비디아 코리아와 과기정통부, 산업부 사이의 정례 협의체를 두면 임원 한 사람의 일정에 따라 부총리 면담이 생기고 사라지는 일은 줄어든다.
3. **의회 쪽을 본다.** 18일 브리핑과 그 뒤의 수출통제 논의는 한국 기업의 준수 비용을 바꾼다. 워싱턴의 의회 접촉은 백악관 접촉과 별개로 필요하다. 지난주 중간선거 기사에서 말한 것과 같은 결론이다.
4. **사생활을 쟁점으로 만들지 않는다.** 황의 고백은 개인의 일이다. 한국이 물을 것은 그 일이 아니라 거래의 구조다.

## 확인할 점

- 정보당국 메모는 공개되지 않았고 어느 정부 기관도 존재나 내용을 확인하지 않았다. NYT와 FT 보도는 익명 취재원에 기댄다. FT 원문은 접속이 막혀 2차 보도로 확인했다. 기소된 사람은 없다.
- 황의 이메일은 외도 상대를 특정하지 않았다. 이메일과 FT 보도의 인물을 같은 사람으로 단정할 근거는 없다.
- 매디슨 황의 방한 취소 사유는 엔비디아가 밝히지 않았고, '가족 문제'는 연합뉴스가 소식통을 인용한 표현이다. 의혹과의 연관은 확인되지 않았다.
- 26만 장 GPU 가운데 계약으로 확정된 물량은 공개 자료에서 확인하지 못했다. 삼성·SK하이닉스의 엔비디아 매출 의존도 수치는 넣지 않았다.
- 의존 구조에 대한 판단, 수출통제 강화 전망, 영향 평가와 제안은 이 글의 해석이다.

## 갱신 기록

- 2026-11-09: 9일 AI 데이 서울 MOU와 엔비디아의 무응답, 프리마켓 주가 반영
- 2026-11-10: 9일 엔비디아 주가와 거래량 반영
- 2026-11-11: 매스트 하원 외교위원장의 10일 "회신 못 받았다" 발언 반영, 확인 일정을 11월 12일로 변경

## 출처

- [CNBC, Moolenaar on Nvidia and Jensen Huang (2026-11-10)](https://www.cnbc.com/2026/11/10/moolenaar-nvidia-jensen-huang-affair-chinese-spy.html)
- [하원 외교위 보도자료 (2026-11-05)](https://foreignaffairs.house.gov/news/press-releases/chairmen-mast-moolenaar-and-crawford-request-jensen-huang-brief-congress-on-link-to-chinese-intelligence-asset)
- [Nvidia stock plunges 4% on Huang investigation — Motley Fool](https://www.fool.com/coverage/stock-market-today/2026/11/09/stock-market-today-nov-9-nvidia-stock-plunges-4-on-jensen-huang-investigation-as-nasdaq-surges-nearly-3/)
- [엔비디아·SKT·리벨리온 NVLink Fusion MOU — 파이낸셜뉴스](https://www.fnnews.com/news/202611091444371881)
- [AI 데이 서울, 매디슨 황 불참 질문에 답 없어 — 재경일보](https://news.jkn.co.kr/post/1080731)
- [Nvidia shares fall premarket after Huang admission — CNBC](https://www.cnbc.com/2026/11/09/nvidia-jensen-huang-chinese-spy-investigation.html)
- [Nvidia board opens investigation; Huang email — CNBC](https://www.cnbc.com/2026/11/08/nvidia-jensen-huang-email-board-of-directors-statement.html)
- [Nvidia CEO Jensen Huang says he had affair, board investigates — CNBC](https://www.cnbc.com/2026/11/08/nvidia-jensen-huang-investigation-china-spy.html)
- [Jensen Huang asked to brief Congress — CNBC](https://www.cnbc.com/2026/11/08/jensen-huang-nvidia-china-spy-congress.html)
- [Letter to Jensen Huang, November 4, 2026 — House Foreign Affairs Committee](https://foreignaffairs.house.gov/sites/evo-subsites/republicans-foreignaffairs.house.gov/files/evo-media-document/11.4.26nvidialetter.pdf)
- [Nvidia Chief Seen as Target of Chinese Spy Plot — NYT(GV Wire 전재)](https://gvwire.com/2026/10/29/nvidia-chief-seen-as-target-of-chinese-spy-plot/)
- [US memo alleges Nvidia CEO romantically linked to suspected spy, FT reports — Investing.com](https://ca.investing.com/news/stock-market-news/us-intelligence-memo-ties-nvidias-huang-to-alleged-chinese-spy-ft-reports-4941137)
- [Nvidia CEO says ties to company in spy probe were normal — 디칸 크로니클(블룸버그)](https://www.deccanchronicle.com/amp/technology/nvidia-ceo-jensen-huang-says-ties-to-company-in-spy-probe-were-normal-2000242)
- [China rejects report on Nvidia spy plot — 타이베이타임스(AFP)](https://taipeitimes.com/News/world/archives/2026/10/31/2003866928)
- [Trump: looking closely at report on Nvidia CEO — ARY News(AFP)](https://arynews.tv/trump-us-looking-closely-report-nvidia-ceo-target-china-spy-plot)
- [Nvidia's Jensen Huang admits to affair — Yahoo Finance](https://finance.yahoo.com/markets/article/nvidias-jensen-huang-admits-to-affair-after-allegations-of-romance-with-chinese-spy-report-205122263.html)
- [매디슨 황 방한 취소, 과기정통부 입장 — ZDNet Korea](https://zdnet.co.kr/view/?no=20261108115633)
- [Nvidia CEO's daughter cancels planned visit to Korea — 코리아타임스(연합)](https://www.koreatimes.co.kr/business/companies/20261107/nvidia-ceos-daughter-cancels-planned-visit-to-korea-sources)
- [매디슨 황 방한 취소, 리벨리온 방문 무산 — 한국일보](https://www.hankookilbo.com/news/article/A2026110810050001381)
- [NVIDIA, South Korea Government and Industrial Giants Build AI Infrastructure — 엔비디아](https://nvidianews.nvidia.com/news/south-korea-ai-infrastructure)
- [배경훈 부총리, 젠슨 황 면담 — 뉴시스](https://mobile.newsis.com/view/NISX20260608_0003661166)
- [GPU 26만장 중 실제 서비스 1.3만장 — ZDNet Korea](https://zdnet.co.kr/view/?no=20261014164011)
- [NVIDIA Form 10-K FY2026 — SEC](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- [NVDA stock price history — StockAnalysis](https://stockanalysis.com/stocks/nvda/history/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
