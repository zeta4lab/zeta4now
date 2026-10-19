---
title: OpenCode 콘솔 침해로 사용자 1.4%의 Anthropic·OpenAI·Google 키 노출…회사는 "대규모 증류 공격", 개발자는 키부터 바꿔야
slug: 2026-10-19-opencode-breach-provider-api-keys-distillation-attack
topic: ai-data-engineering
published_at: 2026-10-19T23:42:00+09:00
tags:
  - OpenCode
  - API 키 유출
  - 증류 공격
  - Anthropic
  - OpenAI
  - 보안 사고
  - 코딩 에이전트
summary: 오픈소스 AI 코딩 에이전트 OpenCode가 10월 17일(현지시각) 퇴역 중이던 legacy 시스템에 무단 접근이 있었고 OpenCode Console 사용자 1.4%가 워크스페이스에 저장한 Anthropic·OpenAI·Google API 키가 노출됐을 수 있다고 밝혔다. 회사는 이를 "대규모 distillation 공격"과 연결했지만 근거는 내놓지 않았고, 사용자들은 수백~1,700달러의 무단 과금을 보고했다.
generated_by: claude
model: claude-fable-5-1
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-10-24
      note: OpenCode의 사후 분석(post-mortem) 공개 여부와 진입 경로·피해 계정 수·보상 방침 발표 여부
    - date: 2026-10-31
      note: OpenAI의 공식 입장 표명 여부, 무단 과금 환불 처리 사례, GitHub 이슈 #56833 보상 요구 결과
---

# OpenCode 콘솔 침해로 사용자 1.4%의 Anthropic·OpenAI·Google 키 노출…회사는 "대규모 증류 공격", 개발자는 키부터 바꿔야

## 한눈에 보기

GitHub 별 21만 개가 넘는 오픈소스 AI 코딩 에이전트 OpenCode를 만드는 Anomaly(옛 SST)는 10월 17일 18시 08분(UTC, 한국시각 18일 새벽 3시 08분) 공식 X 계정에 "우리는 지난밤 대규모 distillation 공격과 관련된 보안 침해를 겪었고, 이는 OpenCode Console 사용자의 1.4%에 영향을 미쳤다"(We had a security breach last night related to a large scale distillation attack that impacted 1.4% of OpenCode Console users)고 썼다. 회사는 "오늘 아침 이메일로 모두에게 알렸다"(We have notified them all this morning via email)며, 이메일을 받지 않았다면 영향이 없고, 피해 대상은 "외부 제공자를 연결해 둔 사용자의 일부"(a subset of users who had external providers linked)라고 했다. "사건이 진행 중이어서 지금은 더 자세한 내용을 공유할 수 없다"(The incident is ongoing so we cannot share more details at this point)면서 Anthropic, OpenAI, Google과 함께 수습하고 있다고 덧붙였다([OpenCode X](https://x.com/opencode/status/2111519637049319818)).

피해 사용자에게 간 이메일은 "우리는 폐기 절차를 진행 중이던 legacy 시스템에 대한 무단 접근을 확인했다"(We identified unauthorized access to a legacy system that we were in the process of decommissioning), "당신의 워크스페이스에 저장된 서드파티 제공자 키(예: OpenAI, Anthropic)가 노출됐을 수 있다"(Third party provider keys (eg OpenAI, Anthropic) saved in your workspace may have been exposed)고 썼다. 제목은 "Action Required: Potential provider key breach"였다([DEV Community](https://dev.to/gabrielanhaia/opencode-told-14-of-console-users-to-revoke-their-openai-and-anthropic-keys-561), [Hacker News](https://news.ycombinator.com/item?id=50133401)). 노출된 것은 OpenCode 프로그램 자체가 아니라, 팀 단위로 모델 접근을 공유하는 유료 호스팅 서비스 OpenCode Console의 워크스페이스에 사용자가 직접 붙여 넣은 제공자 키다. 공동창업자 Dax Raad는 "이것은 OpenCode Console이지 OpenCode 자체가 아니다. 그 키들은 우리에게 오지 않는다"(note this is the OpenCode Console, not OpenCode itself, those keys never come to us)고 썼다([Dax Raad X](https://x.com/thdxr/status/2111572618340188393)).

회사는 공격자가 어떻게 들어왔는지, 얼마나 오래 머물렀는지, 1.4%가 몇 명인지, 키가 실제로 복사돼 쓰였는지는 밝히지 않았다. 그 사이 X와 Reddit에서는 OpenAI·Anthropic·Google 잔액이 밤사이 빠져나갔다는 보고가 잇따랐고, Anthropic과 Google은 영향을 받은 것으로 보이는 키를 직접 폐기·차단했다고 밝혔다. 이 글은 보도 간 날짜 차이를 정리하고, distillation이 무엇이며 훔친 키가 왜 거기에 쓰이는지, 개발자가 지금 할 일을 순서대로 정리한다.

## 무슨 일이: 16~17일 밤의 침입과 17일 저녁의 공개

OpenCode의 X 게시물은 침해 시점을 "지난밤"(last night)이라고만 썼다. 게시물이 17일 18시(UTC)에 올라왔으므로 미국 시각 기준 16일 밤에서 17일 새벽 사이다. 한 피해 사용자가 공개한 통지에는 노출이 시작됐을 수 있는 가장 이른 시각이 17일 0시 30분(UTC, 한국시각 17일 오전 9시 30분)으로 적혀 있었다고 XenoSpectrum이 전했으나, 이것이 모든 키에 해당하는 확정 시각은 아니다([XenoSpectrum](https://xenospectrum.com/en/opencode-console-breach-api-key-management/)). The Hacker News도 "침입자가 10월 16일 밤 legacy 시스템에 도달했다"고 정리했다([The Hacker News](https://thehackernews.com/2026/10/opencode-console-breach-may-have.html)).

공개는 이메일보다 외부 폭로가 앞섰다. 보안 연구자 Matt Johansen은 17일 15시 30분(UTC, 한국시각 18일 0시 30분) 고객 이메일 화면을 올리며 "확인됨. OpenCode 해킹. 키 도난"(Confirmed. OpenCode hacked. Keys stolen.)이라고 썼고([Matt Johansen X](https://x.com/mattjay/status/2111480005435719885)), 시장조사 업체 Creative Strategies의 분석가 Max Weinbach는 18시 01분 "확인한다. 내 OpenAI와 Anthropic 잔액이 빠져나갔다"(Can confirm. My OpenAI and Anthropic balances got drained)며 Google 계정도 제한되고 일부 소진됐다고 했다([Max Weinbach X](https://x.com/mweinbach/status/2111518053662064829)). OpenCode 공식 계정의 첫 게시물은 17시 56분, 널리 인용된 두 번째 게시물은 18시 08분에 올라왔다([OpenCode X(첫 게시물)](https://x.com/opencode/status/2111516673953935833)). Raad는 18시 41분 "내 개인 계정들도 지금 공격받고 있다. AI 기반 해킹의 완전히 새로운 세상"(my personal accounts are being attacked now too, whole new world with ai powered hacking)이라고 썼다([Dax Raad X](https://x.com/thdxr/status/2111528031072461114)).

보도마다 날짜가 다른 이유는 대부분 시간대다. StepSecurity는 X 공지와 이메일 통지를 모두 10월 18일로 적었고([StepSecurity](https://www.stepsecurity.io/blog/opencode-security-breach)), Cyera와 CyPro, The Hacker News는 17일로 적었다([Cyera](https://www.cyera.com/research/opencode-breach-what-happened-and-how-to-rotate-exposed-ai-api-keys), [CyPro](https://cypro.co.uk/insights/cyber-bulletins/opencode-breach-may-have-exposed-provider-api-keys/)). X 게시물의 원본 타임스탬프는 17일 18시 08분(UTC)이므로 미국·유럽에서는 17일, 한국·일본에서는 18일 새벽이다. 회사가 "오늘 아침"이라고 한 이메일 발송 시각은 공개되지 않았고, Startup Fortune은 "이메일이 17일에 나갔는지 18일에 나갔는지 출처가 엇갈린다"고 썼다([Startup Fortune](https://startupfortune.com/opencode-breach-exposes-stored-openai-and-anthropic-keys-prompts-urgent-key-rotation/)).

18일 12시 04분(UTC, 한국시각 18일 밤 9시 04분) Raad는 "그들은 지난 48시간 동안 쉬지 않고 우리 시스템을 공격하고 있다. 부작용으로 모든 것이 강화되고 있지만, 우리도 에이전트를 24시간 돌려야 한다. 그들이 그렇게 하기 때문"(they've been non stop trying to attack our systems for the past 48 hours, a side effect is everything is getting hardened but damn we basically need agents going 24/7 because that's what they have)이라고 썼다([Dax Raad X](https://x.com/thdxr/status/2111790511409258796)). 그는 조사에 쓴 프런티어 모델이 "꽤 많이 하다가 거부하기 시작했다"(they did quite a bit and then started refusing)며 사이버 보안 가드레일에 막혔다고도 했다([OfficeChai](https://officechai.com/ai/getting-blocked-by-ai-agent-cyber-safeguards-while-fighting-malicious-ai-agents-says-opencode-co-founder-dax-raad-after-hack/)). 19일 밤 현재 OpenCode 블로그나 GitHub에는 별도의 공식 공지나 사후 분석이 없고, OpenCode 상태 페이지에는 16~18일의 보안 사건이 등재돼 있지 않다([OpenCode 상태 페이지](https://status.opencode.ai/)).

## 무엇이 노출됐나: Console 워크스페이스에 저장한 "내 키"

OpenCode는 터미널·에디터·데스크톱에서 돌아가는 코딩 에이전트로, 75개가 넘는 제공자의 모델에 연결된다. 명령줄에서 `/connect`로 넣은 제공자 API 키는 사용자 PC의 `~/.local/share/opencode/auth.json`에 저장된다고 공식 문서가 밝히고 있다([OpenCode 문서 - Providers](https://opencode.ai/docs/providers/)). 반면 OpenCode Console(이전 이름 Zen)은 회사가 운영하는 유료 AI 게이트웨이로, 워크스페이스 소유자와 관리자가 "자기 제공자를 연결"(connect their own providers)해 팀원과 모델을 공유하고 예산을 정할 수 있다([OpenCode 문서 - Console](https://opencode.ai/docs/zen/)). 이 '내 키 가져오기'(BYOK) 구조에서는 제공자 키가 OpenCode 서버에 저장되고, 팀원은 키를 보지 않고도 모델을 쓴다. 이번에 노출됐을 수 있다는 것이 바로 이 서버 저장 키다.

그래서 OpenCode는 피해 범위를 "Console 사용자의 1.4%" 가운데 "외부 제공자를 연결한 사용자"로 한정했다. 다만 1.4%의 분모가 Console 가입자 전체인지, 외부 제공자를 연결한 사용자인지는 보도마다 다르게 읽혔다. 회사는 Console 사용자 수도, 노출된 키 수도 공개하지 않았다. Startup Fortune은 회사가 "현재까지의 조사 결과 다른 데이터가 유출된 증거는 없다"는 취지로 밝혔다고 전했다([Startup Fortune](https://startupfortune.com/opencode-breach-exposes-stored-openai-and-anthropic-keys-prompts-urgent-key-rotation/)).

한편 제공자 키를 연결한 적이 없는 Console·Go 구독자들도 17일 밤부터 자신의 OpenCode 키가 `401 api_key_expired` 오류로 막혔다고 GitHub에 보고했다. 만료일을 "Never"로 둔 키가 모두 17일을 마지막 사용일로 "Expired" 상태가 됐다는 화면도 올라왔다. 한 Go 구독자는 "내 워크스페이스에는 OpenAI, Anthropic, Google 키가 전혀 없었고 유일한 자격 증명은 내 Go 키였는데 그래도 폐기됐다"며 공식 보상 방침을 요구했다([GitHub 이슈 #56833](https://github.com/anomalyco/opencode/issues/56833), [GitHub 이슈 #56556](https://github.com/anomalyco/opencode/issues/56556)). 또 다른 사용자는 17일부터 모든 워크스페이스가 "접근 제한" 상태인데 침해 이메일은 받지 못했다고 썼다([GitHub 이슈 #56703](https://github.com/anomalyco/opencode/issues/56703)). OpenCode의 GitHub 자동 응답 봇은 이들에게 계정 문의는 `help@anoma.ly`로 보내라고 안내하고 이슈를 닫았으며, 회사는 자사 키를 일괄 폐기했는지, 그 이유가 무엇인지 설명하지 않았다.

## 피해 보고와 제공자 대응: Anthropic·Google은 키 폐기, OpenAI는 침묵

무단 과금 보고는 모두 사용자 개인의 주장이며 OpenCode나 제공자가 확인한 수치는 없다. Dealroom은 Colin Parsons가 OpenAI 키에서 281달러, Anthropic 키에서 168달러가 빠져나갔고, Preston Zeller는 1,700달러, Francisco Giancarelli는 키를 끄기 전까지 700달러 이상의 OpenAI 사용료가 발생했다고 X에 썼다고 전했다([Dealroom](https://dealroom.co/news/163473-opencode-breach-drains-users-ai-keys-as-platforms-holding-customer-crede/)). Notebookcheck 보도를 인용한 The Hacker News, GIGAZINE, AI매터스는 Reddit 사용자가 Anthropic에서 약 400달러, Google에서 약 200유로의 무단 사용 뒤 프로젝트가 정지됐다고 보고했다고 썼다([The Hacker News](https://thehackernews.com/2026/10/opencode-console-breach-may-have.html), [GIGAZINE](https://gigazine.net/gsc_news/en/20261019-opencode-leak/), [AI매터스](https://aimatters.co.kr/news-report/55672/)). r/ClaudeAI에는 저장해 둔 Anthropic 키로 하룻밤 사이 약 158달러가 소진됐다는 글이 올라왔고([promppy(r/ClaudeAI 게시글 요약)](https://www.promppy.com/item/2447090)), Hacker News에서는 Anthropic 월 20달러 API 크레딧을 다 썼다는 통지를 받았다는 사용자도 있었다([Hacker News](https://news.ycombinator.com/item?id=50133401)). Crypto Briefing은 "수백 달러에 이르는 청구서"가 보고됐으며 이 과금을 누가 책임질지는 불분명하다고 썼다([Crypto Briefing](https://cryptobriefing.com/opencode-distillation-attack-api-key-breach/)).

제공자 쪽 대응은 두 곳이 공개됐다. Anthropic의 Claude Code 팀 Lydia Hallie는 17일 21시 04분(UTC) OpenCode 게시물을 인용해 "OpenCode와 함께 작업했고 영향을 받은 것으로 보이는 Claude API 키를 폐기했다"며 "OpenCode에 키를 저장했고 더 조심하고 싶다면 새 키를 만들라"(If you saved a key in OpenCode and want to be extra careful, please create a new one!)고 썼다([Lydia Hallie X](https://x.com/lydiahallie/status/2111563956666110287)). Google DeepMind·AI Studio의 Evan Otero는 22시 53분 "OpenCode에 저장된 Gemini API 키와 관련된 OpenCode 보안 사건을 인지하고 있다"(We are aware of the OpenCode security incident involving Gemini API keys stored in OpenCode)며 노출된 키를 차단했고, "OpenCode에 API 키를 썼다면 AI Studio에서 새 키를 만들고 옛 키를 삭제한 뒤 사용량을 검토하라", "본인이 만들지 않은 과금이 보이면 Google Cloud Billing 지원에 연락하라"고 안내했다([Evan Otero X](https://x.com/EvanOtero/status/2111591525876474100)). OpenAI의 공개 입장은 19일 밤까지 확인되지 않았다. OpenCode는 환불이나 보상 방침을 내놓지 않았고, Anthropic의 API 키 관리 안내 문서도 유출된 키로 발생한 사용료의 환불 여부는 다루지 않는다([Anthropic 지원 문서](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-keys-safe-and-secure)).

## distillation이 무엇이고 훔친 키가 왜 거기에 쓰이나

Anthropic은 올해 2월 23일 글에서 distillation을 "덜 유능한 모델을 더 강한 모델의 출력으로 훈련하는 것"(training a less capable model on the outputs of a stronger one)으로 정의했다. 자기 모델의 작은 버전을 만들 때 쓰는 정당한 기법이지만, 다른 회사 모델의 답변을 대량으로 수집해 자기 모델을 학습시키면 이용 약관 위반이자 '능력 탈취'가 된다. 당시 Anthropic은 DeepSeek, Moonshot AI, MiniMax가 약 2만 4,000개의 가짜 계정으로 1,600만 건 넘는 대화를 수집했다고 주장했고, 하나의 프록시 네트워크가 2만 개 이상의 가짜 계정을 동시에 굴렸다고 썼다([Anthropic](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)). 9월 10일 위협 정보 보고서에서는 Alibaba, Moonshot, DeepSeek, Zhipu, Xiaomi, SenseTime, MiniMax 등 중국 기반 7개 연구소를 지목했다. Alibaba 연계 클러스터만 5~7월 1억 5,100만 건, 하루 최대 300만 건의 대화를 3,500개 이상의 가짜 계정으로 수집했다는 것이다. 이 보고서는 접근 방식을 이렇게 설명했다. 이들 연구소는 대체로 프록시 서비스를 거쳐 요청을 보내며, 프록시 서비스는 "거짓 신원, 가짜 또는 훔친 신용카드, 훔친 API 키로 수천 개의 새 계정을 만들고"(create thousands of new accounts using false identities, fake or stolen credit cards, and stolen API keys), "정당한 기업이나 개인에게 속한 훔친 API 자격 증명"(stolen API credentials belonging to legitimate companies or individuals)을 쓴다([Anthropic 위협 정보 보고서(2026년 9월)](https://www.anthropic.com/threat-intelligence-report-september-2026)).

10월 12일 Anthropic은 방어 강화 글에서 초기 방어를 뚫은 distiller들이 "수십만 개의 가짜 계정을 통제하는 프록시 네트워크"(proxy networks that control hundreds of thousands of fraudulent accounts)로 규모를 키웠고, 이 네트워크는 Claude가 제공되지 않는 지역에 접근을 재판매했다고 밝혔다. 새 분류기와 지문 기법으로 distiller가 수집하는 데이터를 90~99% 줄였고, 수만 개의 계정을 캠페인 시작 두 시간 안에 차단하는 경우가 많다고도 했다([Anthropic 연구 블로그](https://www.anthropic.com/research/distillation-defenses)). 이 구조에 비춰 보면 훔친 키의 쓸모는 분명하다. 가짜 계정은 만들기 어려워지고 빨리 막히지만, 결제 수단과 사용 이력이 있는 정당한 고객의 키는 제공자 입장에서 평소와 같은 트래픽으로 보이고, 비용은 키 주인에게 청구된다. Crypto Briefing은 공격자가 "비밀번호나 카드 번호를 노린 것이 아니라"(The attackers were not after passwords or credit card numbers) 고급 모델에 반복 질의해 답변을 긁어 가려 했다고 해석했다([Crypto Briefing](https://cryptobriefing.com/opencode-distillation-attack-api-key-breach/)).

다만 OpenCode가 이번 사건을 distillation과 연결한 근거는 공개되지 않았다. Hacker News 댓글에서는 "공개된 증거가 없다"며 키가 단순 재판매에 쓰였을 수도 있다는 반론이 나왔고([Hacker News](https://news.ycombinator.com/item?id=50133401)), Rescana는 "이 침해를 특정 행위자와 연결하는 직접 증거는 없다"고 썼다([Rescana](https://www.rescana.com/post/opencode-console-breach-exposes-openai-anthropic-and-google-api-keys-in-credential-theft-and-distillation-attack-october)). The Hacker News는 범죄 시장에서 AI 토큰과 키가 재판매된다는 점도 함께 짚었다. 'distillation 공격'이라는 이름이 키가 어떻게 빠져나갔는지를 설명하지는 않는다는 점은 기억해야 한다.

## 개발자가 지금 할 일

첫째, 내가 해당되는지 확인한다. OpenCode Console(또는 옛 Zen) 워크스페이스에 Anthropic·OpenAI·Google 등 제공자 키를 붙여 넣은 적이 있다면 OpenCode의 통지 이메일을 찾는다. 회사 설명대로라면 이메일이 없으면 대상이 아니다. 다만 Console 키 폐기와 워크스페이스 제한이 통지 없이 일어난 사례가 GitHub에 올라와 있으므로, Console에 키를 넣은 적이 있다면 이메일 유무와 관계없이 교체하는 쪽이 안전하다. 명령줄에서만 `/connect`로 키를 넣어 `~/.local/share/opencode/auth.json`에 둔 사용자는 이번 사건의 대상이 아니라는 것이 회사 설명이다. 그래도 같은 키를 Console에도 넣었다면 교체 대상이다. StepSecurity는 조직 관리자가 각 개발자 PC에서 `which opencode`, `~/.config/opencode`, `~/.local/share/opencode/auth.json` 존재 여부로 OpenCode 사용자를 찾고, `auth.json`에 제공자가 적혀 있으면 이메일이 올 때까지 잠재 피해자로 다루라고 권했다([StepSecurity](https://www.stepsecurity.io/blog/opencode-security-breach)).

둘째, 키는 OpenCode가 아니라 제공자 대시보드에서 폐기한다. Console에서 키를 지우는 것은 제공자 쪽 키를 무효화하지 않는다([The Hacker News](https://thehackernews.com/2026/10/opencode-console-breach-may-have.html)). Anthropic은 Console의 API keys 페이지에서 해당 키의 메뉴를 열어 "Delete API Key"를 선택하면 즉시 무효화된다고 안내한다([Anthropic 지원 문서](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-keys-safe-and-secure)). OpenAI는 platform.openai.com의 API keys 페이지, Google은 AI Studio에서 처리하되 Google은 새 키를 먼저 만들고 옛 키를 삭제하라고 안내했다. Cyera는 침해 이메일 안의 링크를 통하지 말고 대시보드 주소를 직접 입력하라고 권했다([Cyera](https://www.cyera.com/research/opencode-breach-what-happened-and-how-to-rotate-exposed-ai-api-keys)). 폐기가 끝났는지는 옛 키로 각 제공자의 models 엔드포인트(`https://api.anthropic.com/v1/models`, `https://api.openai.com/v1/models`)를 호출해 401이 돌아오는지로 확인할 수 있다([DEV Community](https://dev.to/gabrielanhaia/opencode-told-14-of-console-users-to-revoke-their-openai-and-anthropic-keys-561)).

셋째, 새 키를 쓰는 곳을 모두 바꾼다. Console 워크스페이스, CI 시크릿, `.env` 파일, LiteLLM 같은 게이트웨이, 서버의 환경 변수가 해당된다. OpenCode 자체 키가 `api_key_expired`로 막힌 경우에는 Console에서 새 키를 만들고 `opencode auth logout` 뒤 `opencode auth login`으로 다시 넣는다. 그래도 옛 키가 계속 전송되면 `OPENCODE_API_KEY` 환경 변수, `opencode.json`의 `apiKey`, `auth.json`에 남은 옛 `opencode` 항목이 새 자격 증명보다 우선 적용되는 것이 아닌지 확인한다. 한 사용자는 `auth.json`의 옛 항목을 지우고 서비스 프로세스를 재시작해 해결했다고 썼다([GitHub 이슈 #56556](https://github.com/anomalyco/opencode/issues/56556)).

넷째, 사용량과 청구서를 본다. 검토 시작점은 미국 시각 10월 16일, 한국시각 17일이다. 내가 쓰지 않은 모델, 낯선 시간대의 급증, 평소보다 큰 토큰 수가 단서다. Anthropic은 Console의 usage와 logs 페이지, Google은 Cloud Billing 지원 창구를 각각 안내했다. 무단 과금의 환불 여부는 제공자별로 개별 문의해야 하며, 현재까지 공개된 환불 정책은 없다.

다섯째, 같은 일을 다시 겪지 않게 구조를 바꾼다. 외부 서비스마다 전용 키를 발급해 한 곳이 뚫려도 다른 곳으로 번지지 않게 하고, 지출 상한과 사용량 알림을 켠다. Anthropic은 90일마다 키를 교체하고 Console에서 지출 한도나 자동 충전 임계값을 설정하라고 권한다. Console의 월 예산은 Console을 거친 요청만 세므로, 노출된 키가 제공자에 직접 호출되는 것을 막지 못한다는 점도 기억해야 한다([XenoSpectrum](https://xenospectrum.com/en/opencode-console-breach-api-key-management/)). 서드파티 서비스에 제공자 키를 맡기는 일 자체를 줄이는 것, 맡길 때는 그 서비스의 키 보관 방식과 사고 대응 약속을 먼저 확인하는 것이 근본 대책이다.

## 의미

이번 사건은 코딩 에이전트의 편의 기능이 새로운 공격면이 됐음을 보여 준다. 사용자는 팀과 모델을 공유하려고 제공자 키를 서비스에 맡겼고, 서비스는 퇴역 중이던 옛 시스템에 그 키를 남겨 뒀다. 키 보관 방식이 무엇이었는지, 암호화됐는지, 왜 옛 시스템이 아직 키에 접근할 수 있었는지는 회사가 답하지 않았다. Raad의 "그 키들은 우리에게 오지 않는다"는 말은 명령줄 사용자에게는 맞지만, Console 사용자에게는 정반대였다. 두 제품이 같은 이름을 쓰는 탓에 사용자가 자신이 어느 쪽인지 알기 어려웠다는 점은 GitHub에서 CLI·GUI·문서·사이트 사이의 이름(Console, OpenCode, OpenCode Go, OpenCode Zen) 불일치 이슈로도 제기됐다([GitHub 이슈 #56754](https://github.com/anomalyco/opencode/issues/56754)).

두 번째 의미는 distillation 경제가 바뀌고 있다는 점이다. Anthropic이 2월과 9월, 10월에 연이어 공개한 대로 가짜 계정은 빠르게 막히고 비싸졌다. 정당한 고객의 키는 그 비용을 피해자에게 떠넘기면서 탐지도 피하는 수단이 된다. 이번 사건에서 실제로 키가 distillation에 쓰였는지는 입증되지 않았지만, 9월 보고서가 "정당한 기업이나 개인의 훔친 API 자격 증명"을 공격 인프라로 명시한 이상 개발자 키는 이제 자원이자 표적이다. 지출 상한 없는 키를 외부 서비스에 맡기는 관행은 이 사건 이후에도 그대로 둘 이유가 없다.

## 확인할 점

- OpenCode는 X 게시물과 이메일 외에 블로그, GitHub, 상태 페이지에 공식 공지를 올리지 않았다. 침입 경로, 접근 기간, 피해 계정 수, 키 저장·암호화 방식, 사후 분석 공개 일정은 모두 미공개다.
- 침해 시각은 "지난밤"(미국 시각 16~17일 밤)으로만 확인됐다. 한 사용자 통지에 적힌 "17일 0시 30분(UTC)"은 XenoSpectrum 보도에 기댄 것으로, 회사가 공식으로 밝힌 시각은 아니다.
- StepSecurity는 공지와 이메일을 18일, 다른 매체는 17일로 적었다. X 게시물 원본 타임스탬프(17일 18시 08분 UTC)를 기준으로 하면 시간대 차이로 보이지만, 이메일 발송 시각 자체는 회사가 밝히지 않았다.
- 1.4%의 분모가 Console 가입자 전체인지, 외부 제공자를 연결한 사용자인지 보도가 엇갈린다. 본문은 회사의 문장("Console 사용자의 1.4%", "외부 제공자를 연결한 사용자의 일부")을 그대로 옮겼다.
- 무단 과금 금액(158·168·281·400달러, 200유로, 700달러 이상, 1,700달러 등)은 모두 X·Reddit의 개인 보고를 Dealroom, Notebookcheck, promppy 등이 전한 것이다. Notebookcheck 원문은 접근 차단으로 직접 확인하지 못해 The Hacker News, GIGAZINE, AI매터스의 인용을 따랐다. Reddit 원문도 직접 열지 못했다.
- Anthropic(Lydia Hallie)과 Google(Evan Otero)의 입장은 각 직원의 개인 X 계정 게시물이며, 두 회사의 공식 채널 성명은 확인하지 못했다. OpenAI의 입장은 어떤 형태로도 확인되지 않았다.
- 제공자 키를 연결하지 않은 Console·Go 구독자의 키 일괄 폐기와 워크스페이스 접근 제한이 이번 사건의 예방 조치인지는 회사가 설명하지 않았다. 한 사용자는 상태 페이지가 16일 9시 34분(UTC)부터 Console 관련 구성 요소를 "degraded"로 표시했다고 주장했으나, 19일 현재 상태 페이지에서는 16~18일 항목을 확인하지 못했다.
- distillation 공격과의 연관성은 OpenCode의 주장이며 독립적으로 검증되지 않았다. Anthropic 9월 보고서의 중국 7개 연구소 관련 내용도 Anthropic의 주장이고, 해당 기업들은 공개적으로 답하지 않았거나 부인했다.

## 출처

- [OpenCode 공식 X 게시물(2026-10-17 18:08 UTC)](https://x.com/opencode/status/2111519637049319818)
- [OpenCode 공식 X 첫 게시물(2026-10-17 17:56 UTC)](https://x.com/opencode/status/2111516673953935833)
- [Confirmed. OpenCode hacked. Keys stolen. — Matt Johansen(X)](https://x.com/mattjay/status/2111480005435719885)
- [Can confirm. My OpenAI and Anthropic balances got drained — Max Weinbach(X)](https://x.com/mweinbach/status/2111518053662064829)
- [my personal accounts are being attacked now too — Dax Raad(X)](https://x.com/thdxr/status/2111528031072461114)
- [note this is the OpenCode Console, not OpenCode itself — Dax Raad(X)](https://x.com/thdxr/status/2111572618340188393)
- [they've been non stop trying to attack our systems for the past 48 hours — Dax Raad(X)](https://x.com/thdxr/status/2111790511409258796)
- [Anthropic이 영향받은 Claude API 키를 폐기했다는 게시물 — Lydia Hallie(X)](https://x.com/lydiahallie/status/2111563956666110287)
- [We are aware of the OpenCode security incident involving Gemini API keys — Evan Otero(X)](https://x.com/EvanOtero/status/2111591525876474100)
- [OpenCode Hacked: User credentials leaked — Hacker News](https://news.ycombinator.com/item?id=50133401)
- [Go subscriber: key revoked with no expiry date set; no formal compensation policy published — GitHub 이슈 #56833](https://github.com/anomalyco/opencode/issues/56833)
- [The API keys disappear from the account, and the agent stops working — GitHub 이슈 #56556](https://github.com/anomalyco/opencode/issues/56556)
- [Console: all workspaces restricted since Oct 17, no breach email received — GitHub 이슈 #56703](https://github.com/anomalyco/opencode/issues/56703)
- [Inconsistent provider naming across CLI, GUI, docs and site — GitHub 이슈 #56754](https://github.com/anomalyco/opencode/issues/56754)
- [OpenCode 상태 페이지 — OpenCode](https://status.opencode.ai/)
- [There are reports of a potential API key leak involving the AI programming tool 'OpenCode' — GIGAZINE](https://gigazine.net/gsc_news/en/20261019-opencode-leak/)
- [Providers — OpenCode 문서](https://opencode.ai/docs/providers/)
- [Console — OpenCode 문서](https://opencode.ai/docs/zen/)
- [OpenCode Console Breach May Have Exposed OpenAI, Anthropic, and Google API Keys — The Hacker News](https://thehackernews.com/2026/10/opencode-console-breach-may-have.html)
- [OpenCode Security Breach: Distillation Attack Hit Console Users With Linked AI Providers — StepSecurity](https://www.stepsecurity.io/blog/opencode-security-breach)
- [OpenCode Breach: What Happened and How to Rotate Exposed AI API Keys — Cyera](https://www.cyera.com/research/opencode-breach-what-happened-and-how-to-rotate-exposed-ai-api-keys)
- [OpenCode Told 1.4% of Console Users to Revoke Their OpenAI and Anthropic Keys — DEV Community](https://dev.to/gabrielanhaia/opencode-told-14-of-console-users-to-revoke-their-openai-and-anthropic-keys-561)
- [OpenCode Breach May Have Exposed Provider API Keys — CyPro](https://cypro.co.uk/insights/cyber-bulletins/opencode-breach-may-have-exposed-provider-api-keys/)
- [OpenCode Console Breach Affects 1.4% of Users, May Have Exposed OpenAI and Claude API Keys — XenoSpectrum](https://xenospectrum.com/en/opencode-console-breach-api-key-management/)
- [OpenCode breach drains users' AI keys as platforms holding customer credentials become targets — Dealroom](https://dealroom.co/news/163473-opencode-breach-drains-users-ai-keys-as-platforms-holding-customer-crede/)
- [OpenCode discloses distillation attack that hit 1.4% of Console users — Crypto Briefing](https://cryptobriefing.com/opencode-distillation-attack-api-key-breach/)
- [OpenCode breach exposes stored OpenAI and Anthropic keys, prompts urgent key rotation — Startup Fortune](https://startupfortune.com/opencode-breach-exposes-stored-openai-and-anthropic-keys-prompts-urgent-key-rotation/)
- [Getting Blocked By AI Agent Cyber Safeguards While Fighting Malicious AI Agents, Says OpenCode Co-Founder Dax Raad — OfficeChai](https://officechai.com/ai/getting-blocked-by-ai-agent-cyber-safeguards-while-fighting-malicious-ai-agents-says-opencode-co-founder-dax-raad-after-hack/)
- [OpenCode Console Breach Exposes OpenAI, Anthropic, and Google API Keys in Credential Theft and Distillation Attack — Rescana](https://www.rescana.com/post/opencode-console-breach-exposes-openai-anthropic-and-google-api-keys-in-credential-theft-and-distillation-attack-october)
- [AI 코딩 도구 오픈코드 해킹…이용자 AI 서비스 키 유출 우려 — AI매터스](https://aimatters.co.kr/news-report/55672/)
- [OpenCode 콘솔 해킹으로 저장된 Anthropic 키 탈취…하룻밤 사이 $158 소진(r/ClaudeAI 게시글 요약) — promppy](https://www.promppy.com/item/2447090)
- [Detecting and preventing distillation attacks — Anthropic](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)
- [Threat Intelligence Report: September 2026 — Anthropic](https://www.anthropic.com/threat-intelligence-report-september-2026)
- [Strengthening our defenses against distillation attacks — Anthropic](https://www.anthropic.com/research/distillation-defenses)
- [API key best practices: Keeping keys safe and secure — Anthropic 지원 문서](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-keys-safe-and-secure)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
