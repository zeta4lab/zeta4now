---
title: "GPT-6.1 Sol 'COBOL 이관 97.9%'는 OpenAI 비공개 테스트 수치…5.4%는 낮은 추론 강도 비교값이고 태스크 수는 미공개, 공개 저장소에는 SQLite 구현 평가만 있다"
slug: 2026-10-27-openai-gpt-6-1-sol-cobol-migration-vendor-eval-vs-practice
topic: ai-data-engineering
published_at: 2026-10-27T14:17:00+09:00
tags:
  - COBOL
  - 레거시 이관
  - 메인프레임
  - 벤치마크
  - OpenAI
  - IBM
  - AWS
summary: "OpenAI는 미국 시각 10월 19일 GPT-6.1 Sol이 자체 COBOL 이관 평가에서 낮은 추론 강도 86.6%(GPT-5.6 Sol 5.4%), 추론 강도를 높이면 97.9%를 기록했다고 밝혔다. 채점은 비공개 숨은 테스트의 출력 일치 여부이고 태스크 수는 공개되지 않았으며, OpenAI가 GitHub에 공개한 것은 SQLite 구현 평가 MultiLangBench뿐이다. 독립 COBOL 벤치마크와 은행·공공 이관 사례는 코드 번역보다 업무 규칙 검증과 이관 운영이 병목이라는 점을 보여 준다."
generated_by: claude
model: claude-opus-5-5
---

# GPT-6.1 Sol 'COBOL 이관 97.9%'는 OpenAI 비공개 테스트 수치…5.4%는 낮은 추론 강도 비교값이고 태스크 수는 미공개, 공개 저장소에는 SQLite 구현 평가만 있다

## 한눈에 보기

- OpenAI는 미국 시각 2026년 10월 19일 '저자원 프로그래밍 언어' 성능 글을 내고, GPT-6.1 Sol이 COBOL 프로그램을 C++, Java, Kotlin, Python, Rust로 옮기는 자체 평가에서 낮은 추론 강도 기준 86.6%, 추론 강도를 높였을 때 97.9%를 기록했다고 밝혔다. 같은 낮은 추론 강도에서 GPT-5.6 Sol은 5.4%였다.
- 일부 요약 보도의 "최대 추론 강도 97.9% 대 GPT-5.6 Sol 5.4%"는 서로 다른 설정을 붙인 비교다. 5.4%와 짝을 이루는 수치는 86.6%다. 97.9%가 어느 추론 강도 단계(high, xhigh 등)인지는 확인한 보도에서 특정되지 않았다.
- 채점은 이관한 프로그램이 OpenAI가 설계한 숨은 테스트를 모두 통과하고 관찰 가능한 출력이 원본과 같아야 성공으로 친다. 태스크·프로그램 수와 테스트 내용은 공개되지 않았다. OpenAI가 같은 날 GitHub에 공개한 MultiLangBench는 SQLite 구현 평가이고 COBOL 이관 평가는 포함하지 않는다.
- OpenAI 스스로 이 수치가 자사 테스트 묶음에서의 성능이며 오류 없는 이관을 보장하지 않고, 실제 운영 전에는 전문가 검토와 실제 업무 부하·문서화되지 않은 의존성에 대한 검증이 필요하다고 밝혔다.
- 독립 측정은 아직 이 모델을 다루지 않는다. 2026년 4월 COBOL 특화 모델 논문은 GPT-4o의 COBOLEval Pass@1을 16.4로 측정했다. 실무에서는 미 GAO가 2025년 7월 연방 핵심 레거시 시스템 11개 가운데 재무부 시스템 2개가 COBOL·어셈블리로 돈다고 보고했고, 2019년 목록 10개 중 이관을 마친 것은 3개였다.

## OpenAI가 발표한 것

OpenAI는 COBOL, Fortran, OCaml, Visual Basic처럼 학습 데이터가 적은 언어에서의 코딩 성능을 두 가지 평가로 제시했다([OpenAI](https://openai.com/index/low-resource-programming-languages/)). 이 글은 OpenAI 원문이 자동 접근을 막아 직접 열지 못했고, 원문을 인용한 BleepingComputer, The Decoder, Interesting Engineering 보도와 OpenAI가 공개한 GitHub 저장소로 내용을 대조했다.

첫째는 COBOL 이관 평가다. COBOL 프로그램을 C++, Java, Kotlin, Python, Rust 중 하나로 동작을 바꾸지 않고 옮기는 과제로, GPT-6.1 Sol은 낮은 추론 강도에서 86.6%, 추론 강도를 높이면 97.9%를 기록했고 GPT-5.6 Sol은 낮은 추론 강도에서 5.4%였다. OpenAI는 97.9%를 포화에 가깝다고 표현했다([BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/openai-says-gpt-61-sol-is-dramatically-better-at-migrating-legacy-code/)). 비용은 이 평가 실행에서 GPT-5.6 Sol API 비용의 61% 수준이었다고 보도됐다([Interesting Engineering](https://interestingengineering.com/ai-robotics/openai-coding-models-software-modernization)).

둘째는 MultiLangBench다. 모델이 20개 언어 각각으로 SQLite 호환 데이터베이스 엔진을 처음부터 만드는 과제이며, 최대 추론 강도의 GPT-6 Astra가 평균 통과율 87.4%로 GPT-5.6 Sol 26.8%를 앞섰다. 언어별로 COBOL은 10.9%에서 72.1%, Fortran은 21.4%에서 83.5%로 올랐고 COBOL이 여전히 가장 어려운 언어였다([BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/openai-says-gpt-61-sol-is-dramatically-better-at-migrating-legacy-code/), [The Decoder](https://the-decoder.com/openai-says-gpt-6-is-much-better-with-legacy-programming-languages-such-as-cobol-and-fortran/)). 이 표의 72.1%는 GPT-6 Astra의 'COBOL로 SQLite 만들기' 점수이고, GPT-6.1 Sol의 'COBOL에서 다른 언어로 옮기기' 점수와는 다른 과제다.

## 평가가 재는 것과 재지 않는 것

COBOL 이관 평가의 성공 기준은 숨은 테스트 전부에서 관찰 가능한 출력이 원본 프로그램과 같은지다. Runtime Wire는 이 테스트를 OpenAI가 설계한 숨은 테스트로 설명했다([Runtime Wire](https://runtimewire.com/article/openai-low-resource-language-coding-benchmarks)). 확인한 보도 어디에도 COBOL 프로그램 수, 프로그램 규모, CICS·DB2 같은 메인프레임 런타임 의존 여부, 목표 언어별 점수는 나오지 않는다. 외부에서 같은 조건으로 재현할 방법이 없다는 뜻이다.

공개된 것은 MultiLangBench다. OpenAI는 10월 19일(UTC) GitHub에 Apache 2.0 라이선스로 저장소를 열었다. README에 따르면 SQLite 3.40.1의 TCL 테스트 5만 1천 개 중 변환 가능한 2만 4천 개를 테스트로 만들었고, 비용 때문에 평가는 해시가 `00`·`01`·`02`로 시작하는 272개만 쓰도록 권고한다. 점수는 API 비용과 테스트 통과율의 쌍이며, 요청한 언어로 쓰지 않으면 통과율을 0으로 둔다([GitHub](https://github.com/openai/MultiLangBench)). 즉 독립적으로 다시 돌려 볼 수 있는 것은 '새로 짓기' 평가이고, 기사 제목이 된 '옮기기' 평가는 아니다.

출력 일치 기준 자체의 한계도 있다. Interesting Engineering은 이관된 프로그램이 오류 없이 돌아가면서도 다른 결과를 낼 수 있다고 지적하며, 초과 소수 자릿수를 다루는 COBOL 방식을 예로 들었다. 숨은 테스트가 그런 경계 사례를 얼마나 덮는지는 공개되지 않았다. OpenAI도 97.9%가 자사 테스트 묶음 기준이며 "오류 없는 이관의 보장이 아니다"라고 밝혔다([Interesting Engineering](https://interestingengineering.com/ai-robotics/openai-coding-models-software-modernization)).

## 독립 벤치마크: 아직 이 모델에 닿지 않았다

COBOL용 공개 벤치마크는 있지만 GPT-6 계열을 측정한 독립 결과는 찾지 못했다. Bloop가 만든 COBOLEval은 HumanEval을 COBOL로 옮긴 코드 생성 평가로, GnuCOBOL 3.2.0으로 컴파일해 Pass@k를 잰다([GitHub](https://github.com/BloopAI/COBOLEval)). 2026년 4월 arXiv에 올라온 COBOL-Coder 논문은 이 벤치마크에서 GPT-4o의 Pass@1을 16.4, 저자들이 미세조정한 COBOL-Coder를 49.33으로 측정했고, Java에서 COBOL로 옮기는 과제에서는 범용 LLM이 0에 가까웠다고 보고했다([arXiv 2604.03986](https://arxiv.org/abs/2604.03986)). 이 논문도 자기 모델을 평가한 연구이고 대상 모델이 GPT-4o 세대라, GPT-6.1 Sol 수치와 직접 비교할 수 없다.

## 실무의 병목: 번역보다 규칙과 이관 운영

공공 부문의 그림은 미 회계감사원(GAO) 보고서에 있다. GAO는 2025년 7월 연방 레거시 시스템 69개를 검토해 현대화가 가장 시급한 11개를 꼽았고, 이 중 8개가 낡은 언어를 쓰며 재무부 시스템 2개는 COBOL과 어셈블리로 돈다고 밝혔다. 2019년에 꼽은 10개 중 2025년 2월까지 현대화를 마친 것은 3개였고, 핵심 관행을 모두 갖춘 현대화 계획을 문서화한 기관은 3곳뿐이었다([GAO](https://www.gao.gov/products/GAO-25-107795)). 지연의 원인으로 지목된 것은 계획과 거버넌스다.

은행 사례도 비슷하다. 호주 Commonwealth Bank는 2008년 SAP 기반 코어뱅킹 교체를 4년, 5억 8천만 호주달러 규모로 시작해 계좌군을 나눠 단계적으로 옮겼고, 범위가 늘면서 사업비는 약 11억 호주달러로, 기간은 약 9개월 더 늘었다([iTWire](https://itwire.com/business-it-news/business-technology/cba-core-project-balloons-to-%2411-billion)). 영국 TSB는 2018년 4월 새 IT 플랫폼으로 이관한 뒤 지점·전화·온라인·모바일 뱅킹 장애가 그해 12월까지 이어졌고, 영국 FCA와 PRA는 2022년 12월 이관 계획과 위험 관리 실패를 이유로 합계 4,865만 파운드의 벌금을 매겼다([FCA](https://www.fca.org.uk/news/press-releases/tsb-fined-48m-operational-resilience-failings)). 두 사례 모두 COBOL 번역 문제가 아니라 코어 시스템 교체 사례지만, 비용과 위험을 키운 것은 범위 관리, 단계 설계, 이관 계획과 운영 위험 관리였다.

## 경쟁 도구 맥락

COBOL 이관은 이미 여러 벤더가 겨루는 시장이다. IBM은 2023년 8월 watsonx Code Assistant for Z를 발표하며 COBOL 비즈니스 서비스를 골라 Java로 단계적으로 옮기고 자동 테스트로 검증하는 흐름을 내세웠다([IBM](https://newsroom.ibm.com/2023-08-22-IBM-Unveils-watsonx-Generative-AI-Capabilities-to-Accelerate-Mainframe-Application-Modernization)). AWS는 2025년 5월 IBM z/OS 애플리케이션 분석·문서화·리팩터링을 다루는 AWS Transform for mainframe을 정식 출시했고([AWS](https://aws.amazon.com/about-aws/whats-new/2025/05/aws-transform-mainframe-generally-available)), 2026년 6월에는 COBOL·PL/I 코드에서 뽑은 요구사항을 원본 코드에 연결해 변환 결정을 추적하게 하는 기능을 더했다([AWS](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-transform-mainframe-traceable-reimagine-workflow/)).

Anthropic은 2026년 2월 23일 Claude Code가 COBOL 현대화에서 노력이 가장 많이 드는 탐색·분석 단계를 자동화할 수 있다는 글을 냈고, 경계가 분명한 구성 요소 하나부터 단계마다 검증하며 옮기라고 권했다([Claude](https://claude.com/blog/how-ai-helps-break-cost-barrier-cobol-modernization)). 같은 날 IBM 주가는 약 13% 떨어졌다([CNBC](https://www.cnbc.com/2026/02/23/ibm-is-the-latest-ai-casualty-shares-are-tanking-on-anthropic-cobol-threat.html)). 세 회사가 내세우는 공통 구조는 분석·문서화·단계적 이관·테스트 검증이다. 확인한 공개 자료 범위에서 어느 벤더도 실제 고객 시스템의 이관 성공률을 같은 기준으로 공개하지 않았다.

## 의미

- 86.6%와 5.4%의 격차는 같은 낮은 추론 강도에서의 비교이므로, 세대 간 개선 폭을 보여 주는 수치로는 유효하다. 97.9%는 설정이 다른 상한값이다.
- 평가의 핵심 정보인 태스크 수, 프로그램 규모, 테스트 범위가 공개되지 않아 이 수치는 OpenAI 내부 지표로 읽어야 한다. 재현 가능한 공개 저장소는 다른 과제를 다룬다.
- 은행·공공 이관의 실패와 지연은 코드 번역보다 업무 규칙 검증, 데이터 이관, 단계 설계, 거버넌스에서 나왔다. 번역 정확도가 높아지면 병목은 그쪽으로 더 옮겨 간다.
- 도입을 검토하는 조직은 벤더 수치보다 자기 시스템의 대표 프로그램과 실제 업무 데이터로 출력 비교 테스트를 먼저 만들고, 그 위에서 모델을 비교하는 편이 증거에 부합한다.

## 확인할 점

- OpenAI 원문은 자동 접근이 차단돼 직접 확인하지 못했다. 수치는 원문을 인용한 복수 보도로 교차 확인했으며, 97.9%의 정확한 추론 강도 단계와 비용 61%가 어느 설정 기준인지는 보도 간 서술이 갈린다.
- COBOL 이관 평가의 태스크 수, 목표 언어별 점수, 숨은 테스트 내용은 공개되지 않았다.
- GPT-6.1 Sol을 측정한 독립 COBOL 벤치마크 결과는 찾지 못했다.
- Commonwealth Bank 사업비는 2010년대 초 보도 기준이며 최종 집행액은 확인하지 못했다.

## 출처

- [OpenAI, Low-resource programming languages (2026-10-19)](https://openai.com/index/low-resource-programming-languages/)
- [BleepingComputer, OpenAI says GPT-6.1 Sol is dramatically better at migrating legacy code (2026-10-20)](https://www.bleepingcomputer.com/news/artificial-intelligence/openai-says-gpt-61-sol-is-dramatically-better-at-migrating-legacy-code/)
- [The Decoder, OpenAI says GPT-6 is much better with legacy programming languages such as COBOL and Fortran (2026-10-20)](https://the-decoder.com/openai-says-gpt-6-is-much-better-with-legacy-programming-languages-such-as-cobol-and-fortran/)
- [Interesting Engineering, OpenAI models hit 97.9% accuracy in tests to modernize old software (2026-10-19)](https://interestingengineering.com/ai-robotics/openai-coding-models-software-modernization)
- [Runtime Wire, OpenAI reports benchmark gains for COBOL and other legacy-language coding (2026-10-19)](https://runtimewire.com/article/openai-low-resource-language-coding-benchmarks)
- [OpenAI, MultiLangBench (GitHub)](https://github.com/openai/MultiLangBench)
- [BloopAI, COBOLEval (GitHub)](https://github.com/BloopAI/COBOLEval)
- [Dau et al., COBOL-Coder (arXiv 2604.03986, 2026-04)](https://arxiv.org/abs/2604.03986)
- [GAO, Agencies Need to Plan for Modernizing Critical Decades-Old Legacy Systems (GAO-25-107795, 2025-07-17)](https://www.gao.gov/products/GAO-25-107795)
- [iTWire, CBA core project balloons to $1.1 billion](https://itwire.com/business-it-news/business-technology/cba-core-project-balloons-to-%2411-billion)
- [FCA, TSB fined £48.65m for operational resilience failings (2022-12)](https://www.fca.org.uk/news/press-releases/tsb-fined-48m-operational-resilience-failings)
- [IBM, IBM Unveils watsonx Generative AI Capabilities to Accelerate Mainframe Application Modernization (2023-08-22)](https://newsroom.ibm.com/2023-08-22-IBM-Unveils-watsonx-Generative-AI-Capabilities-to-Accelerate-Mainframe-Application-Modernization)
- [AWS, AWS Transform for mainframe is now generally available (2025-05-15)](https://aws.amazon.com/about-aws/whats-new/2025/05/aws-transform-mainframe-generally-available)
- [AWS, AWS Transform for mainframe traceable reimagine workflow (2026-06-16)](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-transform-mainframe-traceable-reimagine-workflow/)
- [Anthropic, How AI helps break the cost barrier to COBOL modernization (2026-02-23)](https://claude.com/blog/how-ai-helps-break-cost-barrier-cobol-modernization)
- [CNBC, IBM is the latest AI casualty (2026-02-23)](https://www.cnbc.com/2026/02/23/ibm-is-the-latest-ai-casualty-shares-are-tanking-on-anthropic-cobol-threat.html)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
