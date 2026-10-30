---
title: 모바일 앱에 AI 붙이는 네 갈래 길…iOS 27과 Android의 기기 내 모델, 클라우드, 하이브리드, 에이전트 연결
slug: 2026-10-31-mobile-ai-integration-android-ios
topic: ai
published_at: 2026-10-31T06:00:00+09:00
tags:
  - 모바일 AI
  - iOS 27
  - Android
  - Foundation Models
  - Gemini Nano
  - AppFunctions
  - Firebase AI Logic
summary: 2026년 가을 기준 Android와 iOS 앱이 AI를 붙이는 방법은 기기 안 모델, 클라우드 모델, 둘을 섞는 하이브리드, 운영체제 에이전트에게 앱 기능을 여는 방식의 네 갈래다. 두 플랫폼의 공식 문서로 각 방식의 현재 상태와 제약을 정리한다.
generated_by: claude
model: unspecified
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-11-02
      note: Firebase AI Logic의 App Check 적용 의무화 시행 확인
---

# 모바일 앱에 AI 붙이는 네 갈래 길…iOS 27과 Android의 기기 내 모델, 클라우드, 하이브리드, 에이전트 연결

## 한눈에 보기

2026년 가을 기준으로 스마트폰 앱이 AI를 쓰는 방법은 크게 네 가지다. 휴대폰 안에 든 모델을 부르거나, 클라우드의 대형 모델을 부르거나, 둘을 섞어 기기에서 되면 기기에서 안 되면 클라우드에서 돌리거나, 앱이 직접 AI를 부르는 대신 Siri나 Gemini 같은 운영체제 에이전트가 앱 기능을 쓸 수 있게 열어 두는 방식이다. 9월 14일 정식 배포된 iOS 27과 올해 Google I/O에서 발표된 Android의 AI 기능으로 네 갈래 모두 공식 API를 갖췄지만, 상당수는 아직 베타나 실험 단계다.

| 방식 | iOS | Android | 상태(10월 말 기준) |
|---|---|---|---|
| 기기 안 모델 | Foundation Models(시스템 모델), Core AI, MLX | ML Kit GenAI API(Gemini Nano), LiteRT-LM | iOS 정식, Android Prompt API 베타 |
| 클라우드 모델 | Foundation Models에 Claude·Gemini 연결, Private Cloud Compute | Firebase AI Logic | Claude 패키지 베타, Firebase 경유 Gemini 프리뷰 |
| 하이브리드 | Firebase AI Logic(Apple 시스템 모델 + Gemini) | Firebase AI Logic(Gemini Nano + Gemini) | 두 플랫폼 모두 실험 기능 |
| 에이전트에게 앱 열기 | App Intents(Siri) | AppFunctions, Gemini UI 자동화 | Android는 실험 프리뷰 |

## 1. 기기 안 모델: 무료이고 오프라인에서도 되지만 작다

iOS의 출발점은 Foundation Models 프레임워크다. Apple Intelligence가 쓰는 기기 안 모델을 Swift API로 직접 부른다. Apple은 iOS 27에서 이 시스템 언어 모델을 처음부터 다시 만들어 지시를 더 잘 따르고 프롬프트에 이미지를 바로 넣을 수 있게 했으며, OCR·바코드 판독 같은 Vision 프레임워크 도구를 모델이 기기 안에서 직접 호출할 수 있다고 밝혔다([Apple](https://developer.apple.com/ios/whats-new/)). 직접 고른 모델을 넣으려면 새 프레임워크 Core AI를 쓴다. Apple은 Core AI를 "서버 의존도 토큰 비용도 없이" 모델을 기기에서 불러와 실행하는 Swift API라고 설명한다. Hugging Face의 MLX 커뮤니티 모델도 같은 방식으로 부를 수 있다([WWDC26 세션](https://developer.apple.com/videos/play/wwdc2026/339/)).

Android에서는 ML Kit의 GenAI API가 기기 안 모델 Gemini Nano를 부른다. 요약·교정·재작성·이미지 설명처럼 용도가 정해진 API와, 자유 형식 요청을 보내는 Prompt API가 있다. Google은 Gemini Nano가 1억 4,000만 대가 넘는 기기에서 돌고 있으며, 차세대 Gemini Nano 4는 올해 안에 플래그십 기기에 탑재되고 지금은 AICore 개발자 프리뷰로 시험할 수 있다고 밝혔다([Android 개발자 블로그](https://android-developers.googleblog.com/2026/07/android-on-device-inference.html), [I/O 26 정리](https://android-developers.googleblog.com/2026/05/android-ai-intelligence-system.html)). 직접 미세 조정한 소형 모델은 LiteRT-LM으로 올린다.

제약도 분명하다. Firebase 문서에 따르면 Android의 Prompt API는 아직 베타이고 일부 기기에서만 되며, 기기 안 모델은 단일 턴 텍스트 생성 중심이고 품질 검증 언어는 영어와 한국어다([Firebase](https://firebase.google.com/docs/ai-logic/hybrid/android/get-started)). 어느 플랫폼이든 지원 기종이 아니면 기능 자체가 없으므로 대체 경로를 함께 설계해야 한다.

## 2. 클라우드 모델: iOS는 '한 가지 호출 방식'으로 묶었다

iOS 27의 가장 큰 변화는 Foundation Models가 Apple 모델 전용이 아니게 된 점이다. LanguageModel 프로토콜을 따르는 모델이면 기기 모델, Private Cloud Compute 모델, Core AI 모델, MLX 모델, 외부 회사 모델을 같은 `LanguageModelSession` 호출로 바꿔 쓸 수 있다([WWDC26 세션](https://developer.apple.com/videos/play/wwdc2026/339/)).

- **Private Cloud Compute**: Apple 서버의 차세대 모델로 추론 기능과 3만 2,000토큰 문맥을 지원한다. App Store Small Business Program에 가입했고 첫 다운로드가 200만 회 미만인 앱은 클라우드 API 비용 없이 쓸 수 있다([Apple](https://developer.apple.com/ios/whats-new/)).
- **Claude**: Anthropic은 6월 8일 Swift 패키지 'Claude for Foundation Models'를 발표했다([Anthropic](https://claude.com/blog/claude-for-foundation-models)). 문서상 아직 베타이며, 인증은 App Attest로 설치본마다 1시간짜리 토큰을 받는 방식, 자체 중계 서버가 키를 붙이는 방식, 개발용 API 키 세 가지다. 앱에 API 키를 넣으면 배포된 바이너리에서 추출될 수 있다고 문서가 경고한다([Claude 문서](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models)).
- **Gemini**: Google은 Firebase AI Logic 라이브러리(firebase-ios-sdk 12.19.0 이상)로 Foundation Models에서 Gemini를 부르는 기능을 프리뷰로 내놨다. 첫 지원 대상은 iOS와 macOS다([Firebase](https://firebase.google.com/docs/ai-logic/apple-foundation-models-framework/get-started)).

Android와 그 밖의 플랫폼에서는 Firebase AI Logic이 표준 경로다. Swift, Kotlin·Java, JavaScript, Flutter, Unity용 클라이언트 SDK가 있고, Firebase 프록시가 중간에서 Gemini API 키를 서버에만 두게 해 준다([Firebase](https://firebase.google.com/docs/ai-logic)). 앱에 키를 심지 않는 것이 핵심이다. Firebase는 **2026년 11월 2일부터 Firebase AI Logic을 쓰려면 App Check 적용이 필수**라고 공지했으므로, 이미 앱을 낸 개발자는 운영용 기기 인증(Android는 Play Integrity, iOS는 App Attest 등) 등록 여부를 바로 확인해야 한다.

## 3. 하이브리드: 되면 기기에서, 안 되면 클라우드에서

Firebase AI Logic은 두 플랫폼 모두에 하이브리드 추론을 실험 기능으로 제공한다. Android는 Gemini Nano와 클라우드 Gemini 사이를 `PREFER_ON_DEVICE`(기기 우선, 안 되면 클라우드), `PREFER_IN_CLOUD`(클라우드 우선, 오프라인이면 기기), `ONLY_ON_DEVICE`, `ONLY_IN_CLOUD` 네 모드로 고른다([Android 개발자 블로그](https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html)). iOS는 기기 쪽에 Apple의 Foundation Models를, 클라우드 쪽에 Gemini를 쓴다([Firebase](https://firebase.google.com/docs/ai-logic/hybrid/ios/get-started)).

기기 쪽 제약은 크다. iOS는 텍스트 입출력만 되고 요청은 약 4,096토큰까지이며, 앱이 화면 맨 앞에 있을 때만 돌고 이미지 입력과 검색 그라운딩은 안 된다. Android 문서는 여러 턴 대화가 클라우드로 넘어가지 않으니 대화와 도구 사용에는 `ONLY_IN_CLOUD`를 권한다. 결국 하이브리드는 짧고 개인정보가 민감한 작업은 기기에서, 길고 무거운 작업은 클라우드에서 처리하도록 나누는 장치다.

## 4. 에이전트에게 앱을 연다: App Intents와 AppFunctions

네 번째 방식은 앱이 모델을 부르지 않는다. 운영체제의 AI 비서가 앱의 데이터와 기능을 쓸 수 있게 열어 둔다.

iOS 27에서는 App Intents가 그 통로다. 엔티티 스키마로 앱 콘텐츠를 Spotlight 의미 색인에 올리면 Siri가 출처를 밝혀 보여 주고, 인텐트 스키마로 정해진 문구 없이 자연어로 기능을 실행하게 할 수 있다. 새 View Annotations API는 화면 속 요소를 엔티티에 연결해 사용자가 "이거"처럼 화면을 가리켜 말해도 알아듣게 한다([Apple](https://developer.apple.com/ios/whats-new/)).

Android의 대응물은 AppFunctions다. Google은 이를 "앱을 기기 안 MCP 서버처럼 동작하게 하는" 플랫폼 API라고 설명한다. 함수에 `@AppFunction` 주석을 달면 Gemini 같은 에이전트가 찾아 실행할 수 있다. Android 16 이상에서 동작하고 호출하는 쪽은 `EXECUTE_APP_FUNCTIONS` 권한이 있어야 한다. 아직 실험 프리뷰이며 Gemini 연동은 일부 테스터 대상 비공개 프리뷰다([Android 개발자 문서](https://developer.android.com/ai/appfunctions)).

별도로 Gemini가 앱 화면을 직접 조작하는 UI 자동화도 있다. 개발자가 할 일은 없다. Google은 2월 Galaxy S26 시리즈와 일부 Pixel 10에서 미국과 한국의 음식 배달·장보기·차량 호출 앱 일부를 대상으로 베타를 시작했고, 결제처럼 민감한 단계 앞에서는 사용자에게 먼저 알린다고 밝혔다([Android 개발자 블로그](https://android-developers.googleblog.com/2026/02/the-intelligent-os-making-ai-agents.html)). 앱 입장에서는 AppFunctions로 기능을 직접 열지 않아도 화면 조작으로 쓰일 수 있다는 뜻이므로, 어떤 동작을 어떤 조건에서 허용할지 정하려면 명시적으로 여는 편이 낫다.

## 무엇부터 고를까

- 요약·교정·분류처럼 개인정보가 민감하고 짧은 작업은 기기 안 모델이 맞다. 지원 기종이 아닐 때의 대체 경로를 함께 만든다.
- 긴 문맥, 이미지·검색 그라운딩, 최신 대형 모델이 필요하면 클라우드를 쓰되 API 키를 앱에 넣지 않는다. 프록시와 App Check·App Attest가 사실상 필수가 됐다.
- 두 플랫폼을 한 코드 구조로 다루려면 Firebase AI Logic의 하이브리드 모드가 가장 가깝지만, 아직 실험 단계다.
- Siri와 Gemini에서 앱이 쓰이길 원하면 iOS는 App Intents 스키마를 채우고, Android는 AppFunctions 프리뷰를 준비해 둔다.

## 출처

- [What's New - iOS (Apple Developer)](https://developer.apple.com/ios/whats-new/)
- [Bring an LLM provider to the Foundation Models framework - WWDC26](https://developer.apple.com/videos/play/wwdc2026/339/)
- [Apple Announces iOS 27 Release Date (MacRumors, 2026-09-09)](https://macrumors.com/2026/09/09/apple-announces-ios-27-release-date/)
- [Building intelligent apps for Apple platforms with Claude in the Foundation Models framework (Anthropic, 2026-06-08)](https://claude.com/blog/claude-for-foundation-models)
- [Apple Foundation Models - Claude 문서](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models)
- [Access Gemini API via Apple's Foundation Models framework (Firebase)](https://firebase.google.com/docs/ai-logic/apple-foundation-models-framework/get-started)
- [Firebase AI Logic 개요](https://firebase.google.com/docs/ai-logic)
- [Firebase AI Logic 하이브리드 - iOS](https://firebase.google.com/docs/ai-logic/hybrid/ios/get-started)
- [Firebase AI Logic 하이브리드 - Android](https://firebase.google.com/docs/ai-logic/hybrid/android/get-started)
- [Top AI on Android updates from Google I/O '26 (2026-05-26)](https://android-developers.googleblog.com/2026/05/android-ai-intelligence-system.html)
- [Build intelligent Android apps: On-device inference (2026-07-21)](https://android-developers.googleblog.com/2026/07/android-on-device-inference.html)
- [Build intelligent Android apps: Cloud and hybrid inference (2026-07-21)](https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html)
- [Overview of AppFunctions (Android Developers)](https://developer.android.com/ai/appfunctions)
- [The Intelligent OS: Making AI agents more helpful for Android apps (2026-02-25)](https://android-developers.googleblog.com/2026/02/the-intelligent-os-making-ai-agents.html)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
