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
summary: 엔비디아 이사회는 8일 젠슨 황 CEO가 외국 정보기관의 표적이 됐다는 보도에 따라 독립 조사를 열었고, 황은 12일 CEO와 이사직에서 즉시 물러났다. 같은 주 매디슨 황은 배경훈 부총리 면담을 포함한 방한 일정을 취소했고, 정부는 13일 엔비디아에서 GPU 26만 장 공급을 '회사 차원에서' 재확인받았다. 이 글은 스파이 의혹의 진위보다, 한국의 AI 인프라 계획이 한 회사와 한 사람과의 관계 위에 세워져 있었다는 점을 문제로 본다.
generated_by: claude
model: unspecified
updated_at: 2026-11-26T08:40:00+09:00
tracking:
  status: ongoing
  last_update:
    at: 2026-11-18T09:12:00+09:00
    note: 17일 3분기 실적(매출 1,158억 달러)과 이사회의 황 복귀 불가 발언, 한국 언급 부재, 황 하원 증언 12월 1일·상원 청문회 3일 확정 반영
  checkpoints:
    - date: 2026-12-02
      note: 황(1일)·테터 법무책임자(2일)의 하원 3개 위원회 속기 인터뷰 개최 여부와 공개된 내용
    - date: 2026-12-03
      note: 상원 은행위 공개 청문회에 황이 출석하는지, 소환장 발부 여부
    - date: 2026-12-31
      note: 이사회 조사 결과 공개, 정부 GPU 잔여 1만 4천 장 입고와 NPU 검토 결과
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

## 11일 워싱턴: 회신은 확인되지 않았고, 질문은 거취로 넘어갔다

기한인 11일(미국 시각) 오후까지 황이 하원에 회신했다는 확인은 없다. **의회의 질문은 브리핑에 나올지에서 CEO 자리에 남을지로 옮겨 갔다.** 매스트와 몰레나 위원장은 11일 오후 기자들에게 아직 황에게서 답을 듣지 못했고 그날이 끝날 때까지 기다리겠다고 했다. 황이 응하지 않으면 소환장을 보내겠느냐는 질문에 매스트는 "그렇다"고 답했고, 몰레나는 "세 위원회 모두 소환권이 있다", "계속 추진하겠다"고 했다([CNBC](https://www.cnbc.com/2026/11/11/nvidia-jensen-huang-congress-resign-ai-chips.html), [TechCrunch](https://techcrunch.com/2026/11/11/congress-to-call-jensen-huang-in-to-answer-for-alleged-chinese-spy-affair/)). 엔비디아는 언론의 논평 요청에 바로 답하지 않았다.

같은 날 의회에서는 사임 요구가 나왔다. 케빈 크레이머 공화당 상원의원은 "스스로의 양심에 따라 사임해야 한다"며 황이 "협박과 갈취에 매우 취약하다"고 했고, 수하스 수브라마니암 민주당 하원의원과 돈 베이컨 공화당 하원의원도 사임을 요구했다. 엘리자베스 워런·짐 뱅크스 상원의원은 국방수권법(NDAA)에 'AI 오버워치법'을 넣으라고 촉구했고, MATCH법과 칩보안법도 거론됐다([CNBC](https://www.cnbc.com/2026/11/11/nvidia-jensen-huang-congress-resign-ai-chips.html)). 사임 요구가 초당적으로 나왔고, 논의가 한 사람의 처신에서 칩 수출 경로 입법으로 번졌다는 점이 한국에는 더 중요하다.

11일 장 마감 뒤에는 회사 안쪽이 흔들렸다. NYT는 황이 사내 임원인 킴벌리 파월 헬스케어 부사장과도 혼외 관계였다고 보도했고, WSJ는 이사회가 황의 해임을 준비하며 이르면 그날 회의를 열 수 있다고 전했다. 로이터는 소식통을 인용해 이사회가 11일 늦게 회의를 연다고 했고, 블룸버그는 이사회가 외부 업체와 후임 후보를 찾고 있다고 보도했다. 엔비디아와 파월은 논평 요청에 바로 답하지 않았고, 엔비디아 주가는 시간외 거래에서 9% 넘게 내렸다([CNBC](https://www.cnbc.com/2026/11/11/nvidia-jensen-huang-affair-employee.html), [Investing.com(로이터)](https://www.investing.com/news/stock-market-news/nvidia-is-preparing-to-oust-ceo-jensen-huang-wsj-reports-5019991)). 12일 낮(한국 시각)까지 이사회 결정은 발표되지 않았다. 이는 모두 익명 취재원 보도다.

## 12~13일: 사람은 떠났고, 약속은 '회사 차원'으로 옮겨졌다

**이 글이 문제로 본 '한 사람'은 나흘 만에 자리에서 사라졌다. 한국 정부가 그다음 날 한 일은 약속의 주어를 황에서 회사로 바꿔 받아 두는 것이었다.** 방향은 맞다. 다만 아직은 재확인이지 계약 공개가 아니다.

엔비디아는 12일(현지시각) 황이 사장·CEO·이사직에서 즉시 물러났다고 발표했다. 콜레트 크레스 CFO가 CFO를 겸하며 임시 CEO를 맡고, 이사회는 내부와 외부 후보를 놓고 후임을 찾는다. 1993년부터 이사였던 하비 존스가 회사 역사상 첫 이사회 의장이 됐다. 발표문은 조사나 의혹을 언급하지 않았고, 17일 3분기 실적 발표 일정은 그대로 뒀다([엔비디아 8-K](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000082/nvidiaannouncesceotransiti.htm)). CNBC는 이사회가 11일 밤 해임을 결정했다는 소식통 발언을 전했다. 엔비디아 주가는 12일 장 초반 13% 넘게 빠져 시가총액이 한때 4조 달러 아래로 내려갔다가 4.3% 하락으로 마감했다. 이사회는 10일 와크텔 립턴에 정보활동 의혹 조사를 맡겼다([CNBC](https://www.cnbc.com/2026/11/12/nvidia-jensen-huang-ceo-live-updates.html)).

의회 쪽 질문은 황이 물러난 뒤에도 남았다. 매스트 하원 외교위원장은 12일 황이 몇 주 안에 증언하기로 동의했고 추수감사절 전이 될 것으로 본다며 "기본적으로 일주일 안에 보고 싶다"고 했다. 외교위·정보위·중국특위가 함께하는 선서·속기 증언이 될 것이라고 했지만 공개 여부는 정해지지 않았다. 팀 스콧 상원 은행위원장은 황과 러트닉 상무장관에게 12월 증언을 요구했고, 러트닉은 자진 출석에 동의했다([CNBC](https://www.cnbc.com/2026/11/13/nvidia-jensen-huang-washington-congress.html)). 원래 요청한 18일 비공개 브리핑이 그대로 열리는지는 확인되지 않았다.

서울의 대응은 하루 만에 나왔다. 배경훈 부총리는 13일 "오늘 오전 과기정통부 제2차관 주재로 엔비디아 측과 현안점검회의를 열었다"며 "첨단 GPU 26만장 공급과 국내 기업과의 협력을 엔비디아가 회사 차원에서 기존 발표대로 추진할 계획임을 재확인했다"고 밝혔다. 정부는 직접 확보분 약 3만 5천 장 가운데 약 2만 1천 장을 확보했고 나머지 약 1만 4천 장은 내년 초 들어온다고 했으며, 약 1만 5천 장은 국가AI컴퓨팅센터로 따로 확보한다고 했다([전자신문](https://www.etnews.com/20261113000289)). 같은 날 국가인공지능전략위원회는 긴급회의를 열어 엔비디아 협력은 유지하되 국산 NPU 등 다른 AI 컴퓨팅 자원도 검토해 공급 선택지를 넓히기로 했다([데일리한국](https://daily.hankooki.com/news/articleView.html?idxno=1425139)).

이 대응에서 눈여겨볼 것은 두 가지다. 첫째, 정부가 처음으로 정부분 확보 현황을 물량 단위로 내놓았다. 다만 '확보'가 계약인지 반입인지는 밝히지 않았고, 10월 국감 자료의 '협약분 9,704장 중 반입 2,608장'과 기준이 같은지도 알 수 없다. 삼성·SK·현대차·네이버클라우드 몫의 진행 상황은 이번 발표에도 들어 있지 않다. 둘째, 'NPU 검토'는 9일 리벨리온 MOU와 같은 방향이지만, 위기가 터진 뒤에야 공급 다변화를 국가 위원회 의제로 올렸다는 사실은 그동안 대안이 계획이 아니라 구호였다는 뜻이기도 하다. 이는 해석이다.

## 17일: 첫 실적은 기록을 냈고, 실적 자료에 26만 장은 없었다

**크레스 임시 CEO 체제의 첫 실적은 시장 예상을 크게 넘었다. 그러나 엔비디아가 숫자로 말한 한국은 GPU를 사는 나라가 아니라 기판과 패키징을 만드는 나라였다.**

엔비디아는 17일(현지시각) 10월 25일로 끝난 3분기 매출이 1,158억 달러로 1년 전보다 103% 늘었다고 발표했다. 데이터센터 매출은 1,076억 달러였고, 4분기 매출 전망은 1,300억 달러(±3%)였다. 4분기는 14주짜리 분기이고, 중국 데이터센터 연산 매출은 전망에 넣지 않았다. 발표문에서 크레스 임시 CEO 겸 CFO는 "베라 루빈이 폭발적으로 출발했다"고 했다. 황의 이름은 발표문에 없고, 이사회 독립위원회의 조사가 미래예측 고지의 위험 요인으로 들어갔다([엔비디아](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-third-quarter-fiscal-2027)). CNBC에 따르면 매출과 4분기 전망은 LSEG 집계 예상치(1,091억 달러, 1,251억 달러)를 넘었고, 주가는 시간외 거래에서 3% 넘게 올랐다([CNBC](https://www.cnbc.com/2026/11/17/nvidia-nvda-earnings-report-q3-2027.html)).

실적 발표 통화에서 하비 존스 이사회 의장은 "이사회는 만장일치로 그의 사임을 받아들였고 젠슨을 CEO로 복귀시킬 생각이 없다"고 했다. 크레스는 회사가 "평소대로" 움직이고 있으며 고객과 공급사, 파트너가 "100%" 함께하고 있다고 했다. 황은 같은 날 이사회 조사에 협조하겠다며, 이사회가 주주에게 이롭다고 판단하면 CEO로 돌아가는 것을 "영광"으로 여기겠다는 성명을 냈다([CNBC](https://www.cnbc.com/2026/11/17/nvidia-nvda-earnings-report-q3-2027.html), [CNBC](https://www.cnbc.com/2026/11/17/nvidia-stock-earnings-jensen-huang-resignation.html)).

한국과 관련된 숫자는 다른 곳에 있었다. CFO 해설에 따르면 공급 약정은 직전 분기 2,790억 달러에서 3,900억 달러로 늘었고, 회사는 증가분이 "주로 다년 메모리 조달"과 관련된다고 했다([CFO 해설(MarketScreener)](https://www.marketscreener.com/news/nvidia-third-quarter-2027-cfo-commentary-ce785edcdc81f420)). 같은 날 낸 공급망 발표에는 삼성전기가 기판 공급 계약을 고쳤고 앞선 협력이 세종·부산의 기판 생산을 뒷받침했다는 내용, 엔비디아가 앰코의 애리조나·한국 첨단 패키징 증설을 지원한다는 내용이 들어 있다([엔비디아](https://nvidianews.nvidia.com/news/nvidia-expands-commitments-with-supply-chain-partners-to-support-ai-infrastructure-buildout)). 실적 발표문과 CFO 해설, 통화 보도에서 한국 정부의 26만 장, 삼성전자, SK하이닉스를 언급한 대목은 찾지 못했다.

의회 일정은 늦춰졌다. 하원 외교위·정보위·중국특위 위원장들은 황이 12월 1일, 팀 테터 법무책임자가 2일 세 위원회의 속기 인터뷰에 나온다고 밝혔다. 비공개가 될 가능성이 크고, 위원장들은 원래 11월 18일로 잡았었다. 매스트 위원장이 기대한 추수감사절(26일) 전 증언은 무산됐다. 팀 스콧 상원 은행위원장은 황을 12월 3일 공개 청문회에 부르며 소환장을 경고했고, 러트닉 상무장관에게는 10일 증언을 요청했다. 황의 대변인은 상원 출석에 대한 논평을 거절했다([CNBC](https://www.cnbc.com/2026/11/17/nvidia-jensen-huang-house-committee.html)).

이 글은 17일 자료에서 두 가지를 읽는다. 첫째, 이사회가 복귀를 닫으면서 '한 사람'의 문제는 끝났지만, 13일 한국 정부가 받아 둔 '회사 차원의 재확인'은 여전히 정부 발표로만 남아 있다. 엔비디아가 투자자에게 내놓은 자료에는 26만 장이 한 줄도 없다. 둘째, 엔비디아가 계약의 언어로 말하는 한국은 고객 한국이 아니라 공급망 한국이다. 공급 약정 증가분 1,110억 달러의 대부분이 메모리라면, 삼성전자와 SK하이닉스에 실제로 걸린 돈은 이쪽이다. 한국이 협상력을 찾을 곳도 GPU를 받는 쪽보다 HBM과 기판을 대는 쪽이다. 마지막으로, 하원 증언이 비공개로 가면 수출통제 논의의 공개 무대는 12월 3일 상원 청문회가 된다. 이는 해석이다.

## 17~18일: 미국이 허가한 중국 판매를 엔비디아가 스스로 멈췄다

**같은 실적 통화에서 크레스 임시 CEO는 미국 정부 허가를 받은 중국향 호퍼 칩 출하를 멈췄다고 밝혔다. 황이 떠난 뒤 엔비디아가 가장 먼저 줄인 것은 워싱턴의 의심을 살 수 있는 매출이다.**

로이터에 따르면 크레스는 17일 통화에서 "허가받은 호퍼 데이터센터 제품을 더 이상 중국에 출하하지 않는다"고 했다. 10월 25일로 끝난 3분기에 이 제품의 중국 매출은 24억 달러였고, 추가 출하 계획은 없으며 4분기 전망에서도 뺐다. 멈춘 이유와 재개 여부는 말하지 않았다([더 스탠더드(로이터)](https://www.thestandard.com.hk/china/article/348898/Nvidia-stops-shipping-US-approved-AI-chips-to-China), [블룸버그 거번먼트](https://news.bgov.com/bloomberg-government-news/nvidia-stops-selling-ai-chips-to-china-despite-us-approval)). 다음 날인 18일 브렛 거스리 하원 에너지상업위원장은 크레스와 러트닉 상무장관에게 서한을 보내, 엔비디아가 고객사 메가스피드의 수출통제 회피를 도왔는지 다음 달 브리핑하라고 요구했다. 그는 "보도된 사건들은 회사가 현행 연방법을 지키고 있는지 의문을 제기한다"고 썼다([저스트 더 뉴스](https://justthenews.com/government/congress/house-commerce-committee-requests-briefings-lutnick-nvidia-interim-ceo-export)). 12월 1일 하원 3개 위원회 인터뷰와 별개인 네 번째 위원회 조사다. 혐의는 입증되지 않았다.

이 글은 출하 중단을 회사의 방어로 읽는다. 허가는 정부가 내줬지만, 그 허가가 어떻게 나왔는지를 의회가 묻는 상황에서 판매를 이어 가면 다음 청문회의 질문이 된다. 한국에는 두 가지가 걸린다. 첫째, H200에는 SK하이닉스의 HBM3E가 주로 들어가므로, 분기 24억 달러 규모의 판로 하나가 닫힌 셈이다. 다만 엔비디아의 메모리 조달 약정은 오히려 늘었으므로 당장의 물량 감소로 단정할 근거는 없다. 둘째, 16일 상무부의 원격 접근 규칙과 이번 출하 중단은 같은 방향을 가리킨다. 중국과 닿는 연산은 허가가 있어도 회사가 먼저 끊는다. 한국 데이터센터가 중국계 고객에게 연산을 빌려줄 때 공급자의 눈치를 먼저 보게 되는 구조가 이미 시작됐다([관련 기사](https://now.zeta4.net/a/2026-11-18-us-remote-access-rule-compute-kyc-korea)). 이는 해석이다.

## 22~25일: 황은 돌아왔고, 이번에는 백악관이 보증했다

엔비디아 이사회는 22일(미국 시각) 황을 CEO와 이사로 즉시 복귀시켰고 23일 발표했다. 발표문은 이사회가 황과 여러 차례 논의한 뒤 그의 솔직함과 리더십에 만족했다며 만장일치로 결정했다고 적었다. 같은 문서는 이사회가 "미국 정부 고위층으로부터 의견을 받았고, 그 의견에 근거해" 황의 복귀가 국가안보 위험이 아니라고 확신한다고 밝혔다. 이사회 조사는 끝까지 진행하고, 독립이사로만 구성한 국가안보·수출통제위원회를 새로 두고 최고준법책임자 직을 만든다고 했다([엔비디아 SEC 공시](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000090/nov23pressrelease.htm)). 17일 실적 통화에서 황을 복귀시킬 뜻이 없다고 했던 존스 의장은 엿새 뒤 "젠슨이 엔비디아를 이끌 적임자"라는 성명을 냈다.

트럼프 대통령은 CNBC 인터뷰에서 "내가 그들을 설득했다", "내가 거래를 성사시켰다"며 "알고 있는 모든 것에 비춰 우리는 그들에게 보증을 줬다"고 했다. CNBC는 소식통을 인용해 22일 트럼프의 개인적 약속이 결정적이었다고 전했다([CNBC](https://www.cnbc.com/2026/11/23/trump-nvidia-jensen-huang.html)). 트럼프는 수사로 황이 무혐의가 됐다는 취지로 말했지만, 같은 CNBC 보도는 로이터를 인용해 법무부가 복귀 전에 황을 정식으로 수사한 적은 없다고 전했다([CNBC](https://www.cnbc.com/2026/11/25/vance-jensen-huang-nvidia-doj-investigation.html)). 의회는 물러서지 않았다. 하원 3개 위원회 위원장은 황과 테터 법무책임자가 12월 1·2일 비공개 속기 인터뷰에 예정대로 나온다고 밝혔고, 상원 은행위원회는 황을 단독 증인으로 3일 공개 청문회를 연다([NBC](https://www.nbcnews.com/politics/congress/congress-criticism-jensen-huang-nvidia-reinstated-ceo-trump-rcna610926)). 슈머 상원 민주당 원내대표는 24일 X에서 황이 "미국 수출통제법을 위반해" 첨단 칩을 중국에 보냈다고 주장했다. 근거는 밝히지 않았고 입증된 혐의도 아니다([로이터(CP24 게재)](https://www.cp24.com/news/world/2026/11/24/schumer-accuses-nvidia-ceo-of-violating-us-export-control-law/)).

서울의 반응은 안도였다. 과기정통부 고위 관계자는 13일 회의에서 엔비디아로부터 기존 협업 과제를 그대로 이행한다는 답을 받았다며 "일희일비할 문제는 아니지만 젠슨 황 CEO의 복귀 자체는 다행"이라고 했다([머니투데이](https://www.mt.co.kr/tech/2026/11/24/2026112413455223376)). 업계에서는 "사업의 연속성과 예측 가능성이 높아진다"는 평가가 나왔다([연합뉴스(네이트 게재)](https://m.news.nate.com/view/20261124n12433)). 정부의 새 공식 발표나 26만 장 공급에 관한 새 수치는 없었다.

이 글은 이 복귀가 이 기사의 판단을 약하게 하는 것이 아니라 강하게 만든다고 본다. 정부의 "다행"이라는 반응은 한국의 AI 인프라 약속이 여전히 한 사람의 거취에 걸려 있다는 고백이다. 그리고 그 한 사람의 자리는 이제 이사회의 판단만이 아니라 미국 대통령의 보증 위에 서 있다. 이사회가 발표문에 정부 의견을 근거로 적었고, 대통령이 거래를 성사시켰다고 말했다. 한국이 기대는 사슬에 고리가 하나 늘었다. 젠슨 황 개인에서 젠슨 황과 백악관의 관계로. 12월 의회 증언과 내년 1월 민주당의 위원장직 인수는 그 고리를 다시 흔들 수 있다. 이는 해석이다.

## 서울: 창구가 닫힌 주말

젠슨 황의 딸 매디슨 황 엔비디아 수석이사는 8일 서울 콘래드호텔에서 배경훈 부총리 겸 과기정통부 장관을 만나고, 9~10일 코엑스 'AI 데이 서울'에 참석하며, 9일 류제명 2차관과 스타트업 포럼을 공동 주재하고 리벨리온 본사를 찾을 예정이었다. 엔비디아는 7일 그가 "부득이한 사정으로" 참석하지 못한다고 알렸고, 연합뉴스는 소식통을 인용해 "가족 문제"라고 전했다. 과기정통부는 "면담 불발은 아쉽지만 예정된 협력과 간담회는 차질 없이 진행한다"고 했다([ZDNet Korea](https://zdnet.co.kr/view/?no=20261108115633), [코리아타임스(연합)](https://www.koreatimes.co.kr/business/companies/20261107/nvidia-ceos-daughter-cancels-planned-visit-to-korea-sources), [한국일보](https://www.hankookilbo.com/news/article/A2026110810050001381)). 취소와 의혹의 연관은 어느 보도도 확인하지 못했다. 행사는 다른 임원들이 대신 나와 예정대로 열린다.

매디슨 황은 올해만 세 번 방한해 삼성, SK하이닉스, LG, 현대차, 두산로보틱스와 피지컬 AI 협력을 논의한 사실상의 창구였다. 이번이 네 번째가 될 예정이었다. **한 사람의 일정이 바뀌자 부총리 면담과 차관 포럼 공동 주재가 같이 사라졌다.** 이것이 이 글이 보는 문제다. 협력의 통로가 제도가 아니라 사람이었다.

## 의존의 크기

지난해 10월 경주 APEC에서 엔비디아는 한국 전체에 26만 장 넘는 GPU를 공급하겠다고 발표했다. 정부 최대 5만, 삼성 5만 이상, SK 5만 이상, 현대차 5만, 네이버클라우드 6만 이상이다([엔비디아](https://nvidianews.nvidia.com/news/south-korea-ai-infrastructure)). 올해 6월 황이 방한했을 때 배 부총리는 "모든 정책적 지원을 아끼지 않겠다"고 했다([뉴시스](https://mobile.newsis.com/view/NISX20260608_0003661166)). 국감 자료에 따르면 정부분 가운데 실제 서비스 중인 것은 지난해 추경분 1만 3,100장이고, 올해 협약분 9,704장 중 10월 8일까지 반입은 2,608장이다([ZDNet Korea](https://zdnet.co.kr/view/?no=20261014164011)). 나머지는 약속이다.

반대 방향의 의존도 크다. 삼성전자와 SK하이닉스의 HBM 매출은 엔비디아 발주에 좌우되고, 지난주 코스피는 데이터센터 규제 우려로 사흘간 10% 넘게 빠졌다. 엔비디아 주가는 5일 9.26% 떨어졌다가 6일 2.78% 반등했는데, 그날의 하락을 의혹과 연결한 주요 보도는 없다([StockAnalysis](https://stockanalysis.com/stocks/nvda/history/)). 시장은 아직 이 사건을 가격에 넣지 않았다.

그러나 위험은 있다. 엔비디아는 연차보고서에서 통제 품목의 전용(diversion) 보도는 "근거가 없고 사실이 아니더라도 사업에 부정적 영향을 줄 수 있다"고 적었고, 수출통제가 "파트너, 공급업체, 고객에게 복잡하고 부담스러운 준수 의무"를 지운다고 썼다([엔비디아 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)). 그 고객과 공급업체에 한국 기업이 있다. 의회가 황의 증언에서 메가스피드 경로를 파고들면 다음 단계는 아시아 데이터센터와 재판매 경로에 대한 더 촘촘한 통제다. 한국 기업은 그 통제의 대상이 아니라 준수 비용을 떠안는 쪽이 된다. 이는 해석이다.

## 9일 서울: 행사는 열렸고, 질문엔 답이 없었다

'AI 데이 서울'은 매디슨 황 없이 열렸다. 엔비디아, SK텔레콤, 리벨리온은 과기정통부 지원 아래 NVLink Fusion으로 엔비디아 GPU와 리벨리온 NPU를 한 시스템에 묶는 MOU를 맺었다. 프리필은 GPU가, 디코드는 NPU가 맡는 구조로 SKT AI 데이터센터에 2028년 도입이 목표다. 이도규 과기정통부 정보통신정책실장은 "오늘의 MOU가 선언에 그치지 않고 글로벌 시장 진출이라는 가시적인 성과로 이어지는 것이 중요하다"고 했다([파이낸셜뉴스](https://www.fnnews.com/news/202611091444371881)). 과기정통부는 다른 국산 NPU 기업으로도 넓히겠다고 했다. 엔비디아는 매디슨 황의 불참 사유와 의혹 관련성에 답하지 않았고, GPU·HBM 영향 질문에는 "행사와 무관하다"고 했다([재경일보](https://news.jkn.co.kr/post/1080731)). 엔비디아 주가는 9일 프리마켓에서 5.2% 내렸고 중국 외교부는 "이른바 중국 스파이 서사"에 근거가 없다고 했다([CNBC](https://www.cnbc.com/2026/11/09/nvidia-jensen-huang-chinese-spy-investigation.html)).

이 MOU는 이 글이 말한 방향과 겹친다. 엔비디아 플랫폼 안에서 국산 NPU에 자리를 만드는 것은 의존을 끊는 일이 아니라 의존의 조건을 바꾸는 일이다. 2028년이라는 시점과 '확대 방침'이 계약으로 이어지는지가 다음 확인 지점이다. 이는 해석이다.

9일 미국 시장에서 엔비디아는 4.27% 내린 178.67달러로 마감했고 거래량은 3개월 평균의 3.7배였다. 같은 날 나스닥은 2.74% 올랐다([Motley Fool](https://www.fool.com/coverage/stock-market-today/2026/11/09/stock-market-today-nov-9-nvidia-stock-plunges-4-on-jensen-huang-investigation-as-nasdaq-surges-nearly-3/)). 시장 전체가 반등하는 날 이 종목만 빠졌다는 것은 하락 이유가 거시가 아니라 이 회사라는 뜻이다. 하원이 요구한 11일 회신 여부는 기한 당일까지도 확인되지 않았다.

## 영향 평가

| 대상 | 영향 | 판단 |
|---|---|---|
| 엔비디아 경영 | 12일 황 사임, 크레스 임시 CEO 체제. 17일 이사회 의장이 황 복귀 불가를 밝혔으나 22일 미국 정부 의견을 근거로 황 복귀. 12월 1일 하원 인터뷰, 3일 상원 청문회는 예정대로 | CEO 교체 위험은 한 번 현실이 됐다가 되돌려졌다. 한국과의 약속을 지킬 책임자는 돌아왔지만, 그 자리는 이제 미국 정부의 보증에 기대고 있다 |
| 한국 정부 GPU 계획 | 13일 엔비디아가 26만 장 공급을 '회사 차원에서' 재확인. 정부분 3만 5천 장 중 2만 1천 장 확보 발표 | 주어가 사람에서 회사로 옮겨진 것은 진전이다. 그래도 '확보'의 기준과 민간 몫의 계약·납기는 여전히 공개되지 않았다 |
| 삼성·SK하이닉스 | 단기 발주 영향 없음. 수출통제 강화 시 준수 비용 증가 | 고객 다변화가 다시 과제가 된다 |
| 피지컬 AI 협력 | 창구였던 인물의 방한 취소 | 기업 간 실무 채널로 옮겨야 한다. 리벨리온 같은 국산 NPU 기업과의 협력은 엔비디아 일정과 무관하게 진행돼야 한다 |
| 과기정통부 | 부총리·차관 일정이 한 회사 임원 방문에 맞춰 짜임 | 국가 AI 전략의 대외 일정이 특정 기업의 가족 행사가 돼서는 안 된다 |

## 한국이 해야 할 일

1. **약속을 계약으로 바꾼다.** 26만 장 가운데 계약, 발주, 반입을 구분해 공개하고, 2027년 베라루빈 1만 장 도입의 조건을 명시해야 한다.
2. **창구를 제도로 바꾼다.** 엔비디아 코리아와 과기정통부, 산업부 사이의 정례 협의체를 두면 임원 한 사람의 일정에 따라 부총리 면담이 생기고 사라지는 일은 줄어든다.
3. **의회 쪽을 본다.** 황의 하원 증언, 12월 상원 은행위 증언과 그 뒤의 수출통제 논의는 한국 기업의 준수 비용을 바꾼다. 워싱턴의 의회 접촉은 백악관 접촉과 별개로 필요하다. 지난주 중간선거 기사에서 말한 것과 같은 결론이다.
4. **사생활을 쟁점으로 만들지 않는다.** 황의 고백은 개인의 일이다. 한국이 물을 것은 그 일이 아니라 거래의 구조다.

## 확인할 점

- 정보당국 메모는 공개되지 않았고 어느 정부 기관도 존재나 내용을 확인하지 않았다. NYT와 FT 보도는 익명 취재원에 기댄다. FT 원문은 접속이 막혀 2차 보도로 확인했다. 기소된 사람은 없다.
- 황의 이메일은 외도 상대를 특정하지 않았다. 이메일과 FT 보도의 인물을 같은 사람으로 단정할 근거는 없다.
- 매디슨 황의 방한 취소 사유는 엔비디아가 밝히지 않았고, '가족 문제'는 연합뉴스가 소식통을 인용한 표현이다. 의혹과의 연관은 확인되지 않았다.
- 26만 장 GPU 가운데 계약으로 확정된 물량은 공개 자료에서 확인하지 못했다. 삼성·SK하이닉스의 엔비디아 매출 의존도 수치는 넣지 않았다.
- 황의 사임과 크레스 임시 CEO 선임은 엔비디아 발표와 SEC 공시로 확인했다. 사임 사유는 발표문에 없고, 이사회가 11일 밤 해임을 결정했다는 것은 소식통 보도다. 두 번째 외도 보도는 NYT의 익명 취재원 보도다.
- 황의 하원 일정(12월 1일)과 테터 법무책임자 일정(2일)은 CNBC가 전한 세 위원장 성명으로 확인했다. 위원장 성명 원문은 보지 못했다. CNBC는 형식을 '속기 인터뷰'로 쓰고 선서 여부는 밝히지 않았다. 황의 상원 청문회 출석 여부는 확인되지 않았다.
- (갱신) 존스 의장의 발언은 실적 발표 통화를 전한 CNBC 보도로 확인했고, 통화 녹취록 원문은 보지 못했다. 공급 약정 직전 분기 수치는 일부 국내 보도가 2,780억 달러로 썼지만 엔비디아 CFO 해설의 2,790억 달러를 따랐다.
- 정부가 밝힌 '2만 1천 장 확보'가 계약 기준인지 반입 기준인지는 보도에서 확인하지 못했다. 엔비디아가 '회사 차원에서' 재확인했다는 것은 정부 발표이며, 엔비디아의 별도 공식 입장은 찾지 못했다.
- (갱신) 크레스의 출하 중단 발언은 로이터 보도로, 거스리 위원장 서한은 저스트 더 뉴스 보도로 확인했고 서한 원문은 보지 못했다. H200에 SK하이닉스 HBM3E가 주로 쓰인다는 것은 2025년 국내 보도에 근거한다. 출하 중단 뒤 한국 정부의 26만 장 계획에 관한 새 발표는 찾지 못했다.
- 의존 구조에 대한 판단, 수출통제 강화 전망, 영향 평가와 제안은 이 글의 해석이다.
- (갱신) 법무부가 황을 정식 수사한 적 없다는 내용은 로이터 보도를 인용한 CNBC 기사로 확인했고 로이터 원문은 보지 못했다. 상원 은행위 공식 페이지는 열지 못해 청문회 일정은 CNBC·NBC 보도로 확인했다. 슈머의 X 게시물 전문은 확인하지 못했다.

## 갱신 기록

- 2026-11-09: 9일 AI 데이 서울 MOU와 엔비디아의 무응답, 프리마켓 주가 반영
- 2026-11-10: 9일 엔비디아 주가와 거래량 반영
- 2026-11-11: 매스트 하원 외교위원장의 10일 "회신 못 받았다" 발언 반영, 확인 일정을 11월 12일로 변경
- 2026-11-12: 11일 회신 기한 당일 상황(회신 미확인, 소환장 준비, 사임 요구, NDAA 수출통제 법안)과 두 번째 외도·이사회 해임 논의 보도 반영, 확인 일정을 11월 13일로 변경
- 2026-11-14: 12일 황 CEO·이사 사임과 크레스 임시 CEO 선임, 황의 하원 증언 동의와 상원 은행위 12월 증언 요구, 13일 정부·엔비디아 현안점검회의와 국가AI전략위 긴급회의 반영, 확인 일정을 11월 18일·27일로 조정
- 2026-11-18: 17일 3분기 실적과 전망, 존스 의장의 복귀 불가 발언과 황 성명, 공급 약정 증가와 공급망 발표의 한국 관련 내용, 황 하원 인터뷰 12월 1일·상원 청문회 3일 일정 반영. 11월 18·27일 확인 일정을 12월 2·3일로 변경
- 2026-11-21: 크레스 임시 CEO의 중국향 허가 호퍼 칩 출하 중단 발언(3분기 24억 달러)과 하원 에너지상업위의 메가스피드 관련 브리핑 요구 반영
- 2026-11-26: 22일 황 CEO 복귀(이사회가 미국 정부 고위층 의견을 근거로 명시), 트럼프의 '거래 성사' 발언과 법무부 수사 여부 엇갈림, 하원 인터뷰·상원 청문회 예정대로 진행, 슈머의 수출통제법 위반 주장, 과기정통부·업계 반응 반영

## 출처

- [NVIDIA Board reinstates Jensen Huang as CEO — 엔비디아 SEC 공시 첨부 보도자료 (2026-11-23)](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000090/nov23pressrelease.htm)
- [NVIDIA Form 8-K — SEC (2026-11-23)](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000090/nvda-20261122.htm)
- [Trump says he convinced Nvidia board to bring back Huang — CNBC (2026-11-23)](https://www.cnbc.com/2026/11/23/trump-nvidia-jensen-huang.html)
- [Vance says DOJ told him Huang was under no investigation — CNBC (2026-11-25)](https://www.cnbc.com/2026/11/25/vance-jensen-huang-nvidia-doj-investigation.html)
- [Congress criticism of Huang reinstatement — NBC News (2026-11-23)](https://www.nbcnews.com/politics/congress/congress-criticism-jensen-huang-nvidia-reinstated-ceo-trump-rcna610926)
- [Schumer accuses Nvidia CEO of violating US export control law — 로이터(CP24 게재, 2026-11-24)](https://www.cp24.com/news/world/2026/11/24/schumer-accuses-nvidia-ceo-of-violating-us-export-control-law/)
- [과기정통부, 젠슨 황 복귀 예의주시 — 머니투데이 (2026-11-24)](https://www.mt.co.kr/tech/2026/11/24/2026112413455223376)
- [젠슨 황 복귀에 국내 업계 반응 — 연합뉴스(네이트 게재, 2026-11-24)](https://m.news.nate.com/view/20261124n12433)
- [Nvidia stops shipping US-approved AI chips to China — The Standard(Reuters) (2026-11-18)](https://www.thestandard.com.hk/china/article/348898/Nvidia-stops-shipping-US-approved-AI-chips-to-China)
- [Nvidia stops selling AI chips to China despite US approval — Bloomberg Government (2026-11-18)](https://news.bgov.com/bloomberg-government-news/nvidia-stops-selling-ai-chips-to-china-despite-us-approval)
- [House Commerce Committee requests briefings from Lutnick, Nvidia interim CEO — Just The News (2026-11-18)](https://justthenews.com/government/congress/house-commerce-committee-requests-briefings-lutnick-nvidia-interim-ceo-export)
- [NVIDIA Announces Financial Results for Third Quarter Fiscal 2027 — 엔비디아 (2026-11-17)](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-third-quarter-fiscal-2027)
- [NVIDIA Third Quarter 2027 CFO Commentary — MarketScreener (2026-11-17)](https://www.marketscreener.com/news/nvidia-third-quarter-2027-cfo-commentary-ce785edcdc81f420)
- [NVIDIA Expands Commitments With Supply Chain Partners — 엔비디아 (2026-11-17)](https://nvidianews.nvidia.com/news/nvidia-expands-commitments-with-supply-chain-partners-to-support-ai-infrastructure-buildout)
- [Nvidia Q3 2027 earnings: live updates — CNBC (2026-11-17)](https://www.cnbc.com/2026/11/17/nvidia-nvda-earnings-report-q3-2027.html)
- [Nvidia stock ahead of earnings after Jensen Huang resignation — CNBC (2026-11-17)](https://www.cnbc.com/2026/11/17/nvidia-stock-earnings-jensen-huang-resignation.html)
- [Jensen Huang to sit for House committee interviews Dec. 1 — CNBC (2026-11-17)](https://www.cnbc.com/2026/11/17/nvidia-jensen-huang-house-committee.html)
- [NVIDIA Announces CEO Transition — 엔비디아 8-K (2026-11-12)](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000082/nvidiaannouncesceotransiti.htm)
- [Nvidia CEO Jensen Huang resigns: Live updates — CNBC (2026-11-12)](https://www.cnbc.com/2026/11/12/nvidia-jensen-huang-ceo-live-updates.html)
- [Nvidia is done with Jensen Huang. The fallout in Washington is just beginning — CNBC (2026-11-13)](https://www.cnbc.com/2026/11/13/nvidia-jensen-huang-washington-congress.html)
- [젠슨 황 사임에도 韓 GPU 26만장 공급 유지…정부 점검회의서 재확인 — 전자신문 (2026-11-13)](https://www.etnews.com/20261113000289)
- [젠슨 황 떠나도 韓 GPU 26만장 공급 유지…정부, 국산 AI반도체 활용 검토 — 데일리한국 (2026-11-13)](https://daily.hankooki.com/news/articleView.html?idxno=1425139)

- [Jensen Huang affair in D.C.: Resignation calls and moves to tighten Nvidia China exports — CNBC (2026-11-11)](https://www.cnbc.com/2026/11/11/nvidia-jensen-huang-congress-resign-ai-chips.html)
- [Congress to call Jensen Huang in to answer for alleged Chinese spy affair — TechCrunch (2026-11-11)](https://techcrunch.com/2026/11/11/congress-to-call-jensen-huang-in-to-answer-for-alleged-chinese-spy-affair/)
- [Nvidia prepares to oust Jensen Huang, WSJ reports — CNBC (2026-11-11)](https://www.cnbc.com/2026/11/11/nvidia-jensen-huang-affair-employee.html)
- [Nvidia board meets to decide CEO Huang's future, source says — Investing.com(로이터) (2026-11-11)](https://www.investing.com/news/stock-market-news/nvidia-is-preparing-to-oust-ceo-jensen-huang-wsj-reports-5019991)
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
