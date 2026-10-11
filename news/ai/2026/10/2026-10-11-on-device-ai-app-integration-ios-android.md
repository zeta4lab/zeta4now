---
title: 아이폰은 '스키마', 안드로이드는 'MCP'…온디바이스 AI가 앱을 부르는 두 가지 방식
slug: 2026-10-11-on-device-ai-app-integration-ios-android
topic: ai
published_at: 2026-10-11T12:15:00+09:00
tags:
  - 온디바이스 AI
  - Apple Intelligence
  - Gemini Nano
  - App Intents
  - AppFunctions
  - 모바일 개발
summary: iOS 27과 안드로이드 17이 나오면서 온디바이스 AI는 '앱 안의 기능'에서 '앱을 부리는 운영체제'로 바뀌고 있다. 애플은 Foundation Models와 App Intents 스키마로, 구글은 Gemini Nano와 MCP식 AppFunctions로 길을 냈다. 두 플랫폼의 구조와 개발 방법, 차이를 정리했다.
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-10-31
      note: iOS 27.2 정식 배포와 시리 AI 한국어 지원 여부
---

# 아이폰은 '스키마', 안드로이드는 'MCP'…온디바이스 AI가 앱을 부르는 두 가지 방식

## 한눈에 보기

애플은 9월 14일 iOS 27과 함께 새 시리 'Siri AI'를 영어 베타로 내놓았고, 한국어 등 5개 언어는 10월에 추가한다고 밝혔다([Apple](https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/)). 구글은 6월 16일 안드로이드 17을 내놓으며 "지능형 시스템으로 전환하는 시작"이라고 했다([Android Developers](https://developer.android.com/blog/posts/android-17-is-here)).

두 회사 모두 연동을 두 방향으로 나눈다. 하나는 **앱이 기기 안의 모델을 호출하는 방향**(애플 Foundation Models, 구글 ML Kit GenAI API)이고, 다른 하나는 **시스템 AI가 앱의 기능을 호출하는 방향**(애플 App Intents, 구글 AppFunctions)이다. 큰 틀은 닮았지만 설계 철학은 다르다. 애플은 시스템이 정한 '스키마'에 앱을 맞추게 하고, 구글은 앱을 기기 안의 MCP 서버처럼 만들어 자유롭게 도구를 내놓게 한다. 개발자가 지금 바로 쓸 수 있는 범위도 다르다. 애플 쪽은 정식 API지만, 구글의 AppFunctions–Gemini 연동은 아직 비공개 프리뷰다.

## 연동 구조: 두 방향, 네 개의 층

| 층 | iOS 27 | 안드로이드 17 |
|---|---|---|
| 시스템 모델 | AFM 3 Core(약 30억 파라미터) 등 애플 온디바이스 모델 | Gemini Nano(v2·v3·v4, 기기별 상이) |
| 앱 → 모델 API | Foundation Models 프레임워크(Swift) | ML Kit GenAI API(AICore 기반) |
| 자체 모델 실행 | Core AI(신규) | LiteRT 등, NPU 직접 접근 시 매니페스트 선언 |
| 모델 → 앱 API | App Intents + App Schemas + View Annotations | AppFunctions(Android MCP), UI 자동화 |
| 시스템 에이전트 | Siri AI | Gemini, Gemini Intelligence |
| 클라우드 확장 | Private Cloud Compute, LanguageModel 프로토콜로 Claude·Gemini 등 | (온디바이스 API와 별도) |

표는 각 사 발표와 개발자 문서를 바탕으로 정리했다.

## iOS: 하나의 시스템 모델, 정해진 문법

**앱이 모델을 부르는 길: Foundation Models.** 애플은 2025년 이 프레임워크를 처음 공개하며 "세 줄의 코드"로 Apple Intelligence의 온디바이스 모델을 쓸 수 있고, 오프라인에서도 동작하며 추론 비용이 무료라고 소개했다. 구조화 출력(guided generation)과 도구 호출도 기본 기능이다([Apple](https://www.apple.com/newsroom/2025/06/apple-intelligence-gets-even-more-powerful-with-new-capabilities-across-apple-devices/)).

```swift
import FoundationModels

let session = LanguageModelSession()
let response = try await session.respond(to: "이 메모를 세 줄로 요약해 줘")
```

iOS 27에서 이 프레임워크는 크게 넓어졌다. 이미지를 텍스트와 함께 넣을 수 있고, OCR·바코드 같은 Vision 도구를 모델이 기기 안에서 직접 호출한다. 모델·도구·지시문을 세션 도중에 바꾸는 'Dynamic Profiles'와 AI 기능을 검증하는 Evaluations 프레임워크도 생겼다([Apple Developer](https://developer.apple.com/wwdc26/guides/ios/)). 가장 큰 변화는 개방이다. 애플은 이제 "Apple Foundation Models, Claude·Gemini 같은 클라우드 모델, 또는 Language Model 프로토콜을 따르는 어떤 제공자의 모델"도 같은 API로 쓸 수 있다고 밝혔다. 앱스토어 소상공인 프로그램에 가입했고 최초 다운로드가 200만 건 미만인 앱은 Private Cloud Compute에서 차세대 애플 모델을 클라우드 API 비용 없이 쓸 수 있다([Apple](https://www.apple.com/newsroom/2026/06/apple-aids-app-development-with-new-intelligence-frameworks-and-advanced-tools/)).

기기 안의 모델은 3세대로 바뀌었다. 애플은 30억 파라미터 밀집 모델의 후속인 'AFM 3 Core'와, 전체 200억 파라미터 가운데 요청마다 10억~40억 개만 쓰는 희소 구조의 'AFM 3 Core Advanced'를 공개했다. Core Advanced는 모델 전체를 플래시 메모리(NAND)에 두고 필요한 전문가(expert)만 DRAM으로 올린다([Apple Machine Learning Research](https://machinelearning.apple.com/research/introducing-third-generation-of-apple-foundation-models)). 다만 서드파티 앱이 Foundation Models로 어느 모델까지 쓸 수 있는지는 공개 자료에서 확인하지 못했다. Core Advanced가 도는 기기는 아이폰 17 프로·에어·18 프로, M4 이상 12GB 아이패드, M3 이상 12GB 맥 등으로 제한된다([Apple](https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/)).

**자체 모델은 Core AI로.** 새 Core AI는 애플 실리콘에 맞춰 모델을 "불러오고, 특화하고, 전적으로 기기에서 실행"하는 프레임워크로, 사전(AOT) 컴파일을 지원하며 "서버 의존성과 토큰 비용이 0"이라고 애플은 설명한다([Apple Developer](https://developer.apple.com/wwdc26/guides/ios/)).

**모델이 앱을 부르는 길: App Intents와 스키마.** 시리가 서드파티 앱 안에서 일하게 하는 통로는 App Intents다. iOS 27의 핵심은 'App Schemas'다. 앱의 콘텐츠(`AppEntity`)와 동작(`AppIntent`)을 메시지·메일·사진 같은 시스템 도메인의 스키마에 맞추면, 시리는 그것이 무엇이고 어떻게 다뤄야 하는지 미리 안다. 애플은 스키마를 "여전히 App Intents지만 시리가 처리할 줄 아는 형태"라고 설명한다([WWDC26](https://developer.apple.com/videos/play/wwdc2026/240/)).

```swift
@AppEntity(schema: .messages.message)
struct MessageEntity: IndexedEntity {
    @Property(indexingKey: \.textContent)
    var body: AttributedString?
}
```

엔티티 스키마를 따르면 앱 콘텐츠가 Spotlight 의미 색인에 들어가 시리가 출처를 밝히며 찾아 준다. 인텐트 스키마를 따르면 별도 호출 문구를 정의하지 않아도 자연어로 실행되고, 시리가 새 언어로 넓어져도 코드를 고칠 필요가 없다. View Annotations API는 화면의 뷰를 엔티티와 연결해 "이거 보내 줘" 같은 화면 기반 요청을 처리하게 한다([Apple Developer](https://developer.apple.com/wwdc26/guides/ios/)). 애플은 시리가 쓰는 Spotlight 색인과 'App Toolbox'가 "전적으로 기기에서" 동작한다고 밝혔다([Apple](https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/)).

## 안드로이드: 기기마다 다른 모델, 열린 도구

**앱이 모델을 부르는 길: AICore와 ML Kit GenAI.** Gemini Nano는 앱이 아니라 시스템 서비스 AICore가 내려받고 갱신한다. 앱은 ML Kit GenAI API로 이를 공유해 쓴다. 요약·교정·재작성·이미지 설명 API는 베타, 자유 프롬프트를 넣는 Prompt API도 베타(일부 기능은 알파), 음성 인식은 알파다. 정식(GA) 단계인 API는 아직 없다([Google for Developers](https://developers.google.com/ml-kit/genai)).

제약도 iOS보다 분명하게 문서화돼 있다. 추론은 앱이 화면 맨 앞에 있을 때만 허용되며, 백그라운드나 포그라운드 서비스에서 호출하면 `BACKGROUND_USE_BLOCKED` 오류가 난다. 앱별 추론 할당량과 일일 배터리 할당량도 있다. 모델 버전은 기기에 따라 nano-v2·v3·v4로 갈리고, 같은 프롬프트에도 결과가 다를 수 있어 `getBaseModelName()`으로 버전을 확인하라고 안내한다(같은 문서).

**자체 모델은 NPU 선언부터.** 안드로이드 17을 타깃으로 NPU에 직접 접근하는 앱은 매니페스트에 `FEATURE_NEURAL_PROCESSING_UNIT`을 선언해야 한다. LiteRT NPU 델리게이트, 제조사 SDK, 지원 중단된 NNAPI가 모두 해당한다([Android Developers](https://developer.android.com/blog/posts/android-17-is-here)).

**모델이 앱을 부르는 길: AppFunctions.** 구글은 AppFunctions를 앱이 "기기 안의 MCP 서버처럼" 동작하게 하는 API라고 설명한다. 앱이 내놓은 함수는 'Android MCP'의 도구가 되고, Gemini 같은 에이전트가 이를 찾아 실행한다. 일반 MCP 서버와 달리 네트워크 왕복 없이 기기 안에서 실행된다([Android Developers](https://developer.android.com/ai/appfunctions)). 함수에 어노테이션을 달고 KDoc 주석을 쓰면, 주석이 곧 LLM이 읽는 도구 설명이 된다.

```kotlin
@AppFunction(isDescribedByKDoc = true)
suspend fun createNote(
    appFunctionContext: AppFunctionContext,
    title: String,
    content: String
): Note = noteRepository.createNote(title, content)
```

AppFunctions는 안드로이드 16 이상에서 동작하며, 호출하는 쪽은 `EXECUTE_APP_FUNCTIONS` 권한이 필요하다. 다만 API 전체가 아직 '실험적 프리뷰'이고, Jetpack 라이브러리는 알파이며, Gemini 연동은 "신뢰할 수 있는 테스터 대상 비공개 프리뷰"다([Android Developers](https://developer.android.com/ai/appfunctions)).

**코드 없는 연동: UI 자동화.** 구글은 AppFunctions를 붙이지 않은 앱도 Gemini가 화면을 대신 조작해 일을 처리하는 UI 자동화 프레임워크를 갖췄다. 갤럭시 S26과 일부 픽셀 10에서 조기 프리뷰로 시작했고, 미국과 **한국**의 일부 음식 배달·장보기·차량 호출 앱이 첫 대상이다. 결제 같은 민감한 작업 전에는 사용자에게 알리고, 사용자가 언제든 직접 조작을 넘겨받을 수 있다([Android Developers Blog](https://android-developers.googleblog.com/2026/02/the-intelligent-os-making-ai-agents.html)).

**고급 기능은 고급 기기에만.** 구글이 5월 발표한 'Gemini Intelligence'는 플래그십 칩, 12GB 이상 RAM, Gemini Nano v3 이상, 5회 이상의 OS 업그레이드와 6년 보안 업데이트를 요구한다. 2025년 모델인 픽셀 9이나 갤럭시 Z 폴드7도 Nano v2라 조건을 채우지 못할 가능성이 있다([9to5Google](https://9to5google.com/2026/05/15/gemini-intelligence-android-spec-requirements/)).

## 무엇이 다른가

**1. '정해진 문법' 대 '자유로운 도구'.** 애플은 도메인별 스키마를 정해 두고 앱이 거기에 맞추게 한다. 시리의 이해 품질을 애플이 책임지는 대신, 스키마가 없는 영역은 시리가 깊이 다루기 어렵다. 구글은 MCP처럼 함수 이름과 설명만으로 도구를 노출해 범위 제약이 적지만, 도구 설명을 잘 쓰는 책임이 개발자에게 넘어온다. 구글이 KDoc을 "LLM 도구 호출에 맞게 최적화"해 주는 에이전트 스킬까지 내놓은 이유다([Android Developers](https://developer.android.com/blog/posts/android-17-is-here)).

**2. 모델 일관성.** iOS에서 개발자가 상대할 시스템 모델은 사실상 애플 모델 하나이며 Apple Intelligence 지원 기기(아이폰 15 프로 이상 등)면 같은 API가 열린다. 안드로이드에서는 같은 API라도 제조사·기종에 따라 Nano 버전과 지원 여부가 갈린다. 실제 서비스에서는 기기 지원 확인과 미지원 기기용 대체 경로(클라우드 모델 등)가 사실상 필수다.

**3. 지금 쓸 수 있는가.** 애플의 Foundation Models와 App Intents는 iOS 27 정식 API로, 지금 앱스토어에 내보낼 수 있다. 구글의 ML Kit GenAI는 베타, AppFunctions는 실험 단계이고 Gemini가 실제로 서드파티 앱 함수를 부르려면 조기 접근 프로그램을 거쳐야 한다.

**4. 클라우드와의 경계.** 애플은 같은 Foundation Models API 안에서 온디바이스 모델, Private Cloud Compute, Claude·Gemini 같은 외부 모델을 바꿔 끼울 수 있게 했다. 안드로이드의 ML Kit GenAI는 온디바이스 전용이며, 문서상 같은 API로 클라우드 모델을 바꿔 쓰는 구조는 아니다.

**5. 개입 방식.** 구글은 개발자가 아무것도 하지 않아도 Gemini가 화면을 조작하는 UI 자동화를 병행한다. 애플은 앱이 App Intents를 채택하지 않으면 시리가 앱 안에서 행동할 수 없는 구조다. 앱 입장에서 보면 구글 쪽은 '참여하지 않아도 불려 갈 수 있는' 플랫폼이다.

## 개발자 체크리스트

- **iOS:** 핵심 콘텐츠를 `AppEntity`로, 주요 동작을 `AppIntent`로 정의하고, 해당 도메인 스키마가 있으면 채택한다. 화면 기반 요청이 중요하면 View Annotations를 붙인다. 생성 기능은 Foundation Models로 시작하되, 모델 교체가 가능한 구조라 프롬프트 평가(Evaluations)를 함께 갖춘다.
- **안드로이드:** 요약·교정 같은 정형 작업은 ML Kit 기능별 API를, 자유 생성은 Prompt API를 쓰고, 기기 지원과 Nano 버전 확인, 할당량 초과 시 재시도, 포그라운드 전용 제약을 반드시 처리한다. 에이전트 연동은 AppFunctions로 미리 준비하고, ADB 명령과 테스트 에이전트 앱으로 검증한다.
- **공통:** 한국어 품질은 따로 검증해야 한다. 시리 AI 한국어는 iOS 27.2 베타에 들어갔고 애플은 10월 확대를 예고했지만, 11일 현재 정식 배포는 확인되지 않았다([MacRumors](https://www.macrumors.com/2026/09/16/siri-ai-new-languages-ios-27-2/)). 시리 AI는 EU의 iOS·아이패드OS와 중국에서는 당분간 제공되지 않는다.

## 남은 변수

애플이 시리와 서드파티 에이전트 사이에 MCP 같은 공개 프로토콜을 둘지는 아직 발표되지 않았다. 구글은 AppFunctions의 정식 출시 일정과 Gemini 연동을 모든 개발자에게 열 시점을 밝히지 않았다. 국내에서는 이달 말 전후 시리 AI 한국어 정식 지원이 첫 시험대가 된다.

## 출처

- [Siri AI, a profoundly more capable and personal assistant, is here — Apple](https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/)
- [Apple accelerates app development with new intelligence frameworks and advanced tools — Apple](https://www.apple.com/newsroom/2026/06/apple-aids-app-development-with-new-intelligence-frameworks-and-advanced-tools/)
- [Apple Intelligence gets even more powerful — Apple (2025)](https://www.apple.com/newsroom/2025/06/apple-intelligence-gets-even-more-powerful-with-new-capabilities-across-apple-devices/)
- [What's new in iOS 27 — Apple Developer](https://developer.apple.com/wwdc26/guides/ios/)
- [Build intelligent Siri experiences with App Schemas — WWDC26](https://developer.apple.com/videos/play/wwdc2026/240/)
- [Introducing the third generation of Apple Foundation Models — Apple Machine Learning Research](https://machinelearning.apple.com/research/introducing-third-generation-of-apple-foundation-models)
- [Android 17 is here — Android Developers](https://developer.android.com/blog/posts/android-17-is-here)
- [The Intelligent OS: Making AI agents more helpful for Android apps — Android Developers Blog](https://android-developers.googleblog.com/2026/02/the-intelligent-os-making-ai-agents.html)
- [Overview of AppFunctions — Android Developers](https://developer.android.com/ai/appfunctions)
- [Overview of the ML Kit GenAI APIs — Google for Developers](https://developers.google.com/ml-kit/genai)
- [Gemini Intelligence Android spec requirements — 9to5Google](https://9to5google.com/2026/05/15/gemini-intelligence-android-spec-requirements/)
- [iOS 27.2 Adds Siri AI in New Languages — MacRumors](https://www.macrumors.com/2026/09/16/siri-ai-new-languages-ios-27-2/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
