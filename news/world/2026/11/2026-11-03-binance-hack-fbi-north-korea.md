---
title: FBI "바이낸스 63억 달러 탈취는 북한 소행"…역대 최대 해킹에 김여정은 "진부한 도발", 금융위는 국내 거래소 긴급 점검
slug: 2026-11-03-binance-hack-fbi-north-korea
topic: world
published_at: 2026-11-03T12:57:00+09:00
tags:
  - 바이낸스
  - 북한
  - 해킹
  - 가상자산
  - FBI
  - 금융위원회
summary: 10월 29일(UTC) 바이낸스에서 63억~64억 달러 규모의 가상자산이 빠져나간 사건을 FBI가 북한 해킹 조직 트레이더트레이터의 소행으로 지목했다. 바이낸스는 손실을 회사 자금으로 메우겠다고 했지만 공격자가 쥔 약 32억 달러는 동결이 어렵고, 한국 금융위는 2일 국내 거래소를 긴급 점검했다.
generated_by: claude
model: claude-opus-5-5
updated_at: 2026-11-05T09:14:00+09:00
tracking:
  status: ongoing
  last_update:
    at: 2026-11-05T09:14:00+09:00
    note: 금융위 5일 전 금융권 간담회 결과(37개사 40건, 약 580개사 전수점검, CEO 책임 강조) 반영
  checkpoints:
    - date: 2026-11-30
      note: 바이낸스 최종 조사 결과와 남은 자산 출금 재개, 국회 정무위 디지털자산기본법 논의와 거래소 배상책임 반영 여부
---

# FBI "바이낸스 63억 달러 탈취는 북한 소행"…역대 최대 해킹에 김여정은 "진부한 도발", 금융위는 국내 거래소 긴급 점검

## 한눈에 보기

세계 최대 가상자산 거래소 바이낸스에서 10월 29일(UTC, 한국시각 30일 새벽) 가상자산이 대량으로 빠져나갔다. 바이낸스는 피해를 약 63억 달러(약 8조 원대)로 추정했고, 블록체인 분석업체 Elliptic은 64억 3,000만 달러로 집계해 역사상 가장 큰 절도라고 평가했다. 2025년 2월 바이비트 해킹(14억 6,000만 달러)의 4배가 넘는다([Elliptic](https://www.elliptic.co/insights/binance-largest-hack-in-history/)).

미국 연방수사국(FBI)은 31일(현지시각) 북한 해킹 조직 '트레이더트레이터'(TraderTraitor)를 배후로 지목했고, 김정은 국무위원장의 여동생 김여정은 3일 "진부한 도발"이라고 반발했다. 바이낸스는 이용자 손실을 회사가 떠안겠다며 1일부터 출금을 단계적으로 재개했다. 지금까지 보도된 내용에서 국내 이용자의 직접 피해는 확인되지 않지만, 금융위원회는 2일 국내 거래소를 긴급 점검했다.

## 어떻게 털렸나: 키를 훔치지 않고 바이낸스 시스템이 서명하게 했다

Elliptic에 따르면 29일 오후 8시 5분(UTC)께 XRP 원장의 바이낸스 지갑 5개가 XRP 2억 3,300만 개를 공격자 주소 한 곳으로 보냈다. 이후 30분 동안 솔라나, 비트코인, 트론, 이더리움 등의 핫월렛이 잇따라 비워졌고, 오후 11시 넘어 2차 유출이 이어져 모두 11개 블록체인이 영향을 받았다. 이더리움에서만 186개 토큰, 38억 달러어치가 나갔다.

바이낸스는 초기에 "개발·운영(DevOps) 엔지니어의 노트북이 침해돼 공격자가 서비스 컨테이너에 접근해 승인되지 않은 출금 거래를 제출했을 수 있다"고 설명했다. 리처드 텡 공동 CEO는 이후 더 복잡한 공격이었다며 흔적을 지우는 악성 소프트웨어가 쓰였다고 했다([NBC News(로이터)](https://www.nbcnews.com/business/business-news/fbi-says-north-korea-was-6-billion-binance-crypto-hack-rcna606758), [CNBC](https://www.cnbc.com/2026/10/31/binance-hack-asset-coverage-withdrawals.html)). Elliptic은 온체인 기록을 근거로 공격자가 개인 키를 훔친 것이 아니라 "바이낸스 자체 시스템이 거래에 서명하게 만들었다"고 분석했다.

바이낸스는 11월 3일 초기 조사 결과를 공개하며 침입 경로를 처음 구체적으로 밝혔다([바이낸스](https://www.binance.com/en/blog/community/3229153443759566763)). 첫 고리는 6월이었다. 엔지니어 A가 검색엔진에서 찾은 AI 코딩 도구를 설치하려다 변조된 Homebrew 설치본을 내려받았다. 바이낸스는 이를 탐지해 기기를 교체하고 자격증명을 바꿨지만, A와 지갑 인프라 동료들의 정보는 이미 노출된 뒤였다. 9월에는 구직 플랫폼에서 프로젝트 책임자를 사칭한 인물이 엔지니어 B에게 접근했고, 화상 면접과 CEO 사칭자 면접을 거쳐 '과제'라며 악성 코드 저장소를 내려받게 했다. 공격자는 10월 20일 B의 컴퓨터와 사내 AI 도구를 이용해 엔지니어 A와 C를 장악했고, A에게 컨테이너 배포 권한 토큰이 있다는 것을 파악했다.

29일 오후 5시 15분(UTC)부터 공격자는 C의 컴퓨터에 로그인해 A의 자격증명으로 컨테이너를 배포하고 악성 스크립트를 실행했다. 오후 8시 5분부터 9분 사이 핫월렛 5개에서 XRP 2억 3,346만 개가 나갔고, EIP-7702로 악성 컨트랙트에 핫월렛 일부의 실행 권한도 넘겼다. 마지막 이체는 오후 11시 56분에 확정됐고, 바이낸스는 30일 0시 10분에 위임 코드를 제거했다.

## FBI "북한 책임"…김여정 "터무니없는 수사"

FBI는 성명에서 "북한이 2026년 10월 29일경 가상자산 거래소 바이낸스에서 60억 달러가 넘는 가상자산을 탈취한 책임이 있다"고 밝혔다([CBS News](https://www.cbsnews.com/news/binance-crypto-heist-withdrawals/)). 비밀경호국(USSS), 국세청 범죄수사국(IRS-CI)과 함께 트레이더트레이터가 탈취 자산을 주로 이더리움으로 바꾸는 것을 관찰했고, 탈중앙금융(DeFi)과 즉시 교환 서비스로 추가 세탁을 시도할 것으로 내다봤다. 또 이더리움 주소 600여 개, 비트코인 주소 20개 미만, 솔라나 주소 1개를 공개하며 민간 사업자에 관련 거래 차단을 요청했다([AP(ABC News)](https://abcnews.com/Business/wireStory/fbi-blames-north-korea-stolen-billions-binance-biggest-137741287), [CoinDesk](https://www.coindesk.com/policy/2026/10/31/fbi-confirms-north-korea-s-role-in-usd6-billion-binance-hack-asks-defi-community-to-block-btc-eth-sol-addresses)). Elliptic에 따르면 FBI는 앞서 바이비트와 DMM 비트코인 해킹도 같은 조직의 소행으로 지목했다. 블록체인 분석업체 TRM Labs도 사전 준비 방식과 서명을 미리 받아 한꺼번에 실행한 수법이 과거 북한 연계 사건과 닮았다고 분석했다.

북한은 3일 조선중앙통신으로 낸 김여정 담화에서 FBI 발표를 "진부한 도발"(a trite provocation), "터무니없는 수사"(an absurd rhetoric)라고 불렀다. 담화는 미국이 "세계 곳곳의 사이버 범죄를 모두 우리 소행인 것처럼 국제 여론을 오도한다"며 "심각한 정치적 도발"이라고 했고, 미국의 적대적 태도와 관련해 "여러 측면에서 재고할 문제가 있다"고 덧붙였다([AP(ABC News)](https://abcnews.com/International/wireStory/north-korea-denies-involvement-binance-hack-criticizes-fbi-137788208), [France 24](https://www.france24.com/en/asia-pacific/20261102-north-korea-rejects-us-allegations-over-6-billion-binance-crypto-heist), [ABC Australia](https://www.abc.net.au/news/2026-11-03/north-korea-denies-binance-heist-customers-withdraw-billions/107340330)).

트럼프 대통령은 FBI 발표 당일 밤 "걱정하지 않는다. 파악 중이다"라며 "북한인지 모른다"고 말했다. AP는 그가 북한 소행으로 확인될 수도 있다고 덧붙였다고 전했고, Fox Business는 "그렇다면 그들과 이야기하겠다"는 발언을 전했다([Fox Business](https://www.foxbusiness.com/technology/north-korea-responsible-6-billion-binance-cryptocurrency-hack-fbi-says)).

## 돈은 어디로: 절반 가까이 동결, 나머지는 800여 개 주소에

Elliptic은 11월 1일 오전(UTC) 기준으로 전체 탈취액의 44%인 28억 5,000만 달러가 동결·압수된 것을 확인했고, 거의 전부가 테더(USDT)와 USD코인(USDC)이라고 밝혔다. 이런 스테이블코인은 발행사가 동결할 수 있다. 다만 공격자는 동결 전에 스테이블코인 약 7억 8,600만 달러를 이더리움과 트론으로 바꿨고, 발행사가 동결할 수 없는 자산 약 32억 5,000만 달러(이더리움 약 58만 4,000개, 비트코인 1만 8,327개, XRP 2억 3,300만 개)를 800개가 넘는 주소에 나눠 들고 있다. 동결액은 집계마다 달라 CoinDesk는 24억 달러 이상, VOA는 약 30억 달러로 전했다([VOA](https://www.voakorea.com/a/8217883.html)).

Elliptic은 북한 연계 세력이 최근 몇 년간 훔친 가상자산이 65억 달러가 넘는다며, 이번 한 건으로 그 누적액이 거의 두 배가 된다고 평가했다. 다만 동결분을 뺀 실제 수익은 이보다 적다.

## 바이낸스의 대응: 회사가 부담, 출금 재개 첫날 순유출 36억 달러

바이낸스는 사고 뒤 출금을 멈췄고, 회사 자금 약 63억 4,000만 달러를 손실 보전용으로 따로 잡았다고 밝혔다. 재원은 이용자자산보호기금(SAFU), 선물 보험기금, 회사 자산이다. 텡 CEO는 "이용자가 이번 사건의 재정적 영향을 부담하지 않을 것"이라며 31일 도난 자산의 90%를 다시 채웠다고 했고, 이후 95%까지 메웠다는 설명도 나왔다. 바이낸스는 3일 게시물에서 10월 31일 기준 영향받은 토큰 자산의 98%를 채웠다고 밝혔다. CNBC는 이 수치가 공격자에게서 90%를 되찾았다는 뜻은 아니라고 짚었다.

출금은 1일 오전 6시(UTC, 한국시각 오후 3시) 비트코인 네트워크부터 다시 열렸다. 이후 이더리움, BNB, XRP 등으로 넓어졌고 3일에는 이더리움·솔라나 자산 51개가 추가됐다. BNB 스마트체인, XRP 원장, 트론 등의 일부 자산은 3일 시점에 아직 열리지 않았고, 완료 시점은 제시되지 않았다([crypto.news](https://crypto.news/binance-restores-withdrawals-for-more-ethereum-solana-tokens-after-6-3b-hack/)). 바이낸스가 밝힌 첫 9시간 30분(06:00~15:30 UTC) 출금은 46억 4,900만 달러, 입금은 10억 1,000만 달러로 순유출은 약 36억 4,000만 달러다. VOA는 로이터를 인용해 순유출을 47억 2,000만 달러로 전했는데, 두 수치의 차이는 설명되지 않았다.

## 한국: 직접 피해 보도는 없지만 '배상 공백'이 드러났다

금융위원회는 2일 오전 유영준 디지털금융정책관 주재로 금융감독원, 금융보안원, 디지털자산거래소 공동협의체(DAXA), 주요 가상자산사업자와 긴급 점검회의를 열었다. 전산 접근통제, 핫월렛 출고 승인·서명 체계, 관리자 권한 관리를 점검했고, 콜드월렛 비중 상향, 입출고 상시 모니터링과 대응 인력 확보, 비정상 접근 시도의 보고·공유, 준비금 추가 적립을 요청했다. 5일에는 금융감독원, 금융보안원, 전 금융권 협회를 불러 대책회의를 연다([뉴시스](https://newsis.com/view/NISX20261102_0003851302), [허프포스트코리아](https://www.huffingtonpost.kr/article/261746)). 블루밍비트에 따르면 업계는 외부 거래소 해킹 같은 긴급 상황에서도 출금을 빨리 멈출 수 있도록 제도적 근거를 달라고 건의했고, 금융위는 검토하기로 했다([블루밍비트](https://bloomingbit.io/feed/news/123502)).

금융위는 5일 전 금융권 간담회에서 9월 30일부터 11월 3일까지 37개사에서 40건의 침해가 신고됐고, 정보 유출 약 47만 3,000건, 자금 탈취 약 10억 원이 신고됐다고 밝혔다. 약 580개사의 IT 자산과 내부통제를 연말까지 전수 점검한다. 이억원 위원장은 보안을 "최고경영자가 직접 책임져야 할 핵심 경영과제"라고 했다([헤럴드경제](https://biz.heraldcorp.com/article/10926424)). 전수 점검은 필요하지만 배상 책임은 이 발표에서 정리되지 않았으므로, 본문이 지적한 공백은 그대로다. 이는 해석이다.

현행 가상자산이용자보호법은 이용자 자산의 80% 이상을 콜드월렛에 두도록 한다. 핫월렛 자산 가치의 5% 이상을 보상할 보험이나 준비금도 요구하며, 최소 금액은 원화마켓 거래소 30억 원, 코인마켓 거래소 등 5억 원이다. 그러나 거래소가 모든 손실을 배상할 의무는 명확하지 않다. 해킹 피해를 원칙적으로 무과실 배상하게 한 전자금융거래법은 가상자산 거래소에 적용되지 않는다. 금융위 가상자산위원회는 3월 무과실 배상책임 부과 방안을 논의했고, 금융위 관계자는 6월 도입을 검토 중이라고 말했다([헤럴드경제](https://biz.heraldcorp.com/article/10922679)). 서나윤 금융위 가상자산과장은 2일 국회 토론회에서 사고 시 책임 소재 등이 "현재 법안에서 검토하고 있는 사항"이라고 했다([헤럴드경제](https://biz.heraldcorp.com/article/10923236)).

국내 거래소의 보안 사고도 별개로 이어졌다. 헤럴드경제에 따르면 10월 고팍스와 프라뱅이 공격을 받았고 프라뱅에서는 1억 원 규모의 고객 자산이 탈취됐으며, 빗썸에서는 고객 844명의 주민등록번호와 계좌번호, 신분증 사본 등이 노출됐다.

## 의미

이번 사건의 교훈은 금액보다 경로에 있다. Elliptic의 분석대로라면 공격자는 키를 빼내지 않고 정상 서명 시스템을 움직였다. 지갑 비율 규제와 키 보관만으로는 막기 어렵고, 승인 절차와 내부 권한, 개발자 단말까지 함께 봐야 한다는 뜻이다. 금융위가 콜드월렛 비중과 함께 서명 체계와 권한 관리를 점검한 것도 같은 맥락으로 읽힌다.

바이낸스의 조사 결과는 이 판단을 뒷받침하면서 더 불편한 사실을 보탠다. 바이낸스는 넉 달 전 첫 침해를 잡아냈고 기기와 자격증명도 바꿨다. 그래도 이미 나간 동료 정보까지 되돌릴 수는 없었고, 공격자는 그 정보로 다음 표적을 고를 수 있었다. 한 번 막은 사고를 끝난 사고로 다루면 안 되는 이유다. 시작점이 금고 근처가 아니라 개발자가 AI 코딩 도구를 찾아 설치하고 이직 제안에 응한 일상적인 순간이었다는 점도 금고 규제로는 닿지 않는 영역이다. 이는 해석이며, 바이낸스의 설명은 자체 초기 조사 결과로 외부 검증을 거치지 않았다.

이용자 입장에서 '손실 전액 보전'은 바이낸스의 재무 여력과 결정에 따른 것이다. 같은 규모의 사고가 국내 거래소에서 나면 법이 요구하는 준비금으로는 감당하기 어렵고 배상 의무도 불분명하다. 디지털자산기본법 논의에 배상책임이 어떻게 담기느냐가 다음 쟁점이다. 이는 해석이다.

## 확인할 점

- FBI 성명 원문은 접속이 막혀 직접 열지 못했고 AP, CBS, CoinDesk, Fox Business의 인용으로 확인했다.
- 피해액은 바이낸스 약 63억 달러, TRM Labs 약 63억 6,000만 달러(헤럴드경제 인용), Elliptic 64억 3,000만 달러로 다르다. Elliptic 수치는 도난 시점 기준 온체인 집계다.
- 공격 경로는 바이낸스가 3일 공개한 초기 조사 결과와 Elliptic의 분석에 기댄 것이다. 바이낸스 게시물은 최종 보고서가 아니며 외부 감사 결과도 아니다. 게시물은 배후를 FBI 정보를 인용해 전한다.
- 보전 비율(90%, 95%, 98%)은 시점과 매체마다 다르고 공격자에게서 되찾은 비율이 아니다. 순유출 36억 4,000만 달러는 바이낸스 자체 수치이며, VOA가 전한 47억 2,000만 달러와의 차이는 확인하지 못했다.
- AP와 France 24 등은 김여정 담화를 '부인'으로 보도했지만, 인용된 담화 문장에는 관여를 직접 부인하는 표현이 확인되지 않는다. 담화 문장은 영문 보도를 옮긴 것으로 조선중앙통신 원문과 다를 수 있다.
- 가격 급락과 시장 영향은 CBS와 NBC가 금요일(30일) 주요 가상자산이 떨어졌다고 전했지만 날짜가 분명한 수치를 찾지 못해 넣지 않았다.
- 국내 이용자·거래소의 직접 피해가 없다는 공식 발표를 확인한 것은 아니며, 읽은 보도에 직접 피해 내용이 없다는 뜻이다. 업비트와 빗썸의 공지 원문도 확인하지 못했다.

## 갱신 기록

- 2026-11-04: 바이낸스 초기 조사 결과(변조된 설치본과 가짜 면접에서 컨테이너 배포까지의 경로, 98% 보충)와 3일 출금 추가 재개 반영
- 2026-11-05: 금융위 5일 전 금융권 간담회 결과 반영, 11월 5일 확인 일정 제거

## 출처

- [금융위 전 금융권 간담회 — 헤럴드경제](https://biz.heraldcorp.com/article/10926424)
- [29 October 2026 Binance Security Incident: Initial Findings and Response Update — 바이낸스](https://www.binance.com/en/blog/community/3229153443759566763)
- [Binance restores withdrawals for more Ethereum, Solana tokens after $6.3B hack — crypto.news](https://crypto.news/binance-restores-withdrawals-for-more-ethereum-solana-tokens-after-6-3b-hack/)
- [The largest theft in history: North Korea likely behind the $6.4 billion Binance hack — Elliptic](https://www.elliptic.co/insights/binance-largest-hack-in-history/)
- [FBI says North Korea was behind the $6.3 billion Binance crypto hack — NBC News(로이터)](https://www.nbcnews.com/business/business-news/fbi-says-north-korea-was-6-billion-binance-crypto-hack-rcna606758)
- [FBI blames North Korea for stolen billions from Binance — AP(ABC News)](https://abcnews.com/Business/wireStory/fbi-blames-north-korea-stolen-billions-binance-biggest-137741287)
- [FBI confirms North Korea's role in $6 billion Binance hack — CoinDesk](https://www.coindesk.com/policy/2026/10/31/fbi-confirms-north-korea-s-role-in-usd6-billion-binance-hack-asks-defi-community-to-block-btc-eth-sol-addresses)
- [FBI says North Korea stole over $6 billion in Binance crypto hack — Fox Business](https://www.foxbusiness.com/technology/north-korea-responsible-6-billion-binance-cryptocurrency-hack-fbi-says)
- [Binance resumes withdrawals following $6.3 billion hack — CNBC](https://www.cnbc.com/2026/10/31/binance-hack-asset-coverage-withdrawals.html)
- [Binance resumes withdrawals for some major cryptocurrencies after $6 billion heist — CBS News](https://www.cbsnews.com/news/binance-crypto-heist-withdrawals/)
- [North Korea denies involvement in Binance hack — AP(ABC News)](https://abcnews.com/International/wireStory/north-korea-denies-involvement-binance-hack-criticizes-fbi-137788208)
- [North Korea rejects US allegations over $6 billion Binance crypto heist — France 24](https://www.france24.com/en/asia-pacific/20261102-north-korea-rejects-us-allegations-over-6-billion-binance-crypto-heist)
- [North Korea dismisses Binance heist allegations as 'absurd' US rhetoric — ABC Australia](https://www.abc.net.au/news/2026-11-03/north-korea-denies-binance-heist-customers-withdraw-billions/107340330)
- [바이낸스 출금 재개…FBI "사상 최대 가상자산 탈취, 북한 소행" — VOA](https://www.voakorea.com/a/8217883.html)
- [美 FBI "바이낸스 8조원대 해킹, 북한 소행" — 헤럴드경제](https://biz.heraldcorp.com/article/10921477)
- [금융위, '바이낸스 해킹' 관련 코인거래소 소집해 긴급 회의 — 뉴시스](https://newsis.com/view/NISX20261102_0003851302)
- [금융위 긴급회의 열고 국내 가상자산사업자 점검 — 허프포스트코리아](https://www.huffingtonpost.kr/article/261746)
- [금융위, 바이낸스 해킹에 국내 거래소 긴급 점검…출금 제한 확대 검토 — 블루밍비트](https://bloomingbit.io/feed/news/123502)
- [바이낸스, 손실 다 책임진다는데…한국은 배상책임 '공백' — 헤럴드경제](https://biz.heraldcorp.com/article/10922679)
- [금융위 "가상자산 해킹 사고 책임 소재, 2단계 법안 제정되면 검토" — 헤럴드경제](https://biz.heraldcorp.com/article/10923236)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
