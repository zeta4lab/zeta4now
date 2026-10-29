---
title: 에이전트는 모델이 아니라 시스템이다…ChatGPT Work·Claude Duet·GPT-6.1 Terra로 본 '모델·실행 틀·작업 공간' 3층 구조
slug: 2026-10-29-building-ai-agents-system-not-model
topic: ai
published_at: 2026-10-29T20:00:00+09:00
tags:
  - 에이전트 만들기
  - AI 에이전트
  - 하네스
  - ChatGPT Work
  - Claude Duet
  - Codex
summary: AI 에이전트를 만드는 7회 연재의 첫 편. 10월 26일 공개된 서베이 논문 'Work Agents'는 에이전트를 기반 모델, 실행 틀(harness), 상태가 남는 작업 공간의 결합으로 정리했다. ChatGPT Work, Claude Duet, GPT-6.1 Terra를 이 틀로 뜯어 보고, 에이전트를 만드는 사람이 차례로 내려야 할 결정을 정리한다.
generated_by: claude
model: unspecified
---

# 에이전트는 모델이 아니라 시스템이다…ChatGPT Work·Claude Duet·GPT-6.1 Terra로 본 '모델·실행 틀·작업 공간' 3층 구조

## 한눈에 보기

"어떤 모델이 제일 똑똑한가"는 에이전트를 만드는 사람에게 첫 질문이 아니다. 같은 모델이라도 어떤 도구를 쥐여 주고, 어디서 일하게 하고, 언제 사람에게 묻게 하느냐에 따라 결과가 달라진다. 10월 26일 arXiv에 올라온 서베이 논문 'Work Agents: Systems, Capabilities, and Optimization'은 이 점을 정면으로 짚는다. 저자 16명은 에이전트를 "기반 모델과 실행 틀(runtime harness)을 결합해, 상태가 남는 작업 공간(stateful workspace)에서 과제를 수행하고 검증 가능한 결과를 내는 시스템"으로 본다([arXiv](https://arxiv.org/abs/2610.35845)).

이 글은 AI 에이전트를 만드는 7회 연재의 첫 편이다. 올해 나온 대표 제품 세 가지를 이 3층 구조로 나눠 보고, 이후 6회에 걸쳐 다룰 결정(모델 고르기, 도구 연결, 기억, 평가, 보안, 운영)의 지도를 그린다.

## 세 층: 모델, 실행 틀, 작업 공간

**기반 모델**은 판단을 맡는다. 다음에 무엇을 할지 정하고, 도구 호출을 만들고, 결과를 읽고 고친다. **실행 틀**은 모델 바깥의 프로그램이다. 모델에 어떤 도구를 보여 줄지, 도구 호출을 실제로 실행할지, 실패하면 다시 시킬지, 언제 사람 승인을 받을지, 대화가 길어지면 무엇을 버리고 무엇을 남길지 정한다. Codex나 Claude Code 같은 코딩 에이전트에서 모델을 감싼 그 프로그램이 실행 틀이다. **작업 공간**은 일이 실제로 벌어지는 곳이다. 파일 시스템, 브라우저, 클라우드 가상 머신, 연결된 업무 앱이 여기에 들어가고, 한 단계의 결과가 다음 단계의 입력으로 남는다는 점이 채팅과 다르다.

논문은 작업 조건을 두 축으로 나눈다. 일이 얼마나 오래 이어지는가(작업 지속성, work persistence)와 환경이 얼마나 열려 있는가(작업 개방성, work openness)다. 디지털 업무는 과제 범위와 조직 방식에 따라 다섯 형태로, 안정적으로 일을 끝내는 데 필요한 능력은 다섯 계열로 정리했다. 성능을 끌어올리는 길도 셋으로 나눴다. 모델을 고치는 것, 실행 틀을 고치는 것, 둘을 함께 고치는 것이다. 실험 결과를 내는 논문은 아니고, 흩어진 연구를 "맡긴 일을 믿을 만하게 끝내는가"라는 기준으로 다시 묶은 지도에 가깝다([arXiv](https://arxiv.org/abs/2610.35845)).

## 사례 1: ChatGPT Work, 코딩 에이전트의 실행 틀을 사무 업무로

OpenAI가 7월 9일 내놓은 ChatGPT Work는 이 구조를 가장 노골적으로 보여 준다. OpenAI는 "Codex 기술이 내장되어" ChatGPT가 질문에 답하는 것을 넘어 실제 업무를 처리한다고 설명했다. 매주 500만 명 넘게 쓰는 Codex는 코딩 에이전트로 시작했지만 100만 명 넘는 사용자가 소프트웨어 개발 밖의 일에도 쓰고 있었고, 그 실행 틀을 스프레드시트·슬라이드·문서·웹 앱을 만드는 일로 넓힌 것이 Work다([OpenAI](https://openai.com/index/chatgpt-for-your-most-ambitious-work/)).

세 층으로 나누면 이렇다. 모델은 출시 당시 GPT-5.6이었다. 작업 공간은 플러그인으로 연결한 Slack·Teams·Google Drive·SharePoint·이메일·캘린더·CRM, 데스크톱 앱의 로컬 파일과 내장 브라우저, 그리고 화면을 직접 조작하는 컴퓨터 사용이다. 실행 틀에는 큰 일을 작은 단계로 나눠 몇 시간씩 이어 가는 기능, 일정이나 이벤트에 맞춰 다시 도는 예약 작업, 사용자가 진행을 보며 방향을 바꾸고 중요한 작업을 승인하는 지점, 연결된 도구로 중요한 작업을 실행하기 전에 다른 모델이 검토하는 '자동 검토'가 들어 있다. 사용량도 채팅이 아니라 Codex와 같은 구조로 센다. 일의 양에 따라 비용이 달라지는 시스템이라는 뜻이다([OpenAI](https://openai.com/index/chatgpt-for-your-most-ambitious-work/)).

## 사례 2: Claude Duet, 기다리지 않고 먼저 오는 에이전트

Anthropic은 10월 21일(현지시각) Claude Duet 연구 프리뷰를 열었다. Anthropic은 공식 계정에서 Duet을 "Claude가 능동적인 에이전트로 일하는 새 앱"이라고 소개하며, 사용자가 신경 써야 할 일을 먼저 가져오고, 맡긴 일을 끝내고, 자리를 비워도 계속 일하고, 사용자를 대신해 행동하기 전에 확인한다고 설명했다([Claude 공식 X](https://x.com/claudeai/status/2112984664256241837)).

여러 보도에 따르면 Duet은 Claude Opus 5.5로 돌고, 사용자의 기기가 꺼져 있어도 일하도록 자체 클라우드 가상 머신과 브라우저에서 작업한다. 메시지 발송, 결제, 문서 서명, 삭제는 실행 전에 할 일을 보여 주고 승인을 기다린다. 미국의 Pro·Max 구독자를 대상으로 대기자 명단을 받는다([Yahoo Tech](https://tech.yahoo.com/ai/claude/articles/anthropic-unveils-claude-duet-answer-002554435.html), [BetaNews](https://betanews.com/article/proactive-ai-agent-claude-duet/)). 3층으로 보면 Duet의 새로움은 모델이 아니라 실행 틀에 있다. 사용자가 부를 때만 도는 루프가 아니라, 스스로 깨어나 확인하고 보고하는 루프를 짰다.

## 사례 3: GPT-6.1 Terra, 같은 일을 더 적은 토큰으로

10월 26일 나온 GPT-6.1 Terra는 거꾸로 모델 쪽 변화가 에이전트 비용을 바꾸는 사례다. OpenAI는 Terra가 컴퓨터 사용 벤치마크 Agents' Last Exam에서 추론 수준 '최대'일 때 Claude Opus 5.5보다 토큰 효율이 3배 넘게 높아 작업당 비용이 약 9분의 1이라고 주장했다. 비교 대상은 토큰당 가격이 아니라 과제 하나를 끝내는 데 드는 돈이다([OpenAI](https://openai.com/index/introducing-gpt-6-1-terra/)). 자세한 수치와 안전 평가는 [GPT-6.1 Terra 출시 기사](https://now.zeta4.net/a/2026-10-27-openai-gpt-6-1-terra-computer-use)에 정리돼 있다.

여기서 읽을 것은 성능 순위가 아니다. 에이전트는 한 번 답하고 끝나는 게 아니라 수십, 수백 번 도구를 부르며 돈다. 그래서 토큰을 얼마나 아껴 쓰는지, 얼마나 빨리 다음 단계로 가는지가 모델 선택의 핵심 기준이 된다. 이 문제는 2회에서 따로 다룬다.

## 만드는 사람이 내려야 할 결정

세 사례를 겹쳐 보면 에이전트를 만드는 일은 세 층마다 결정을 내리는 일이다.

| 층 | 결정할 것 | 다룰 회차 |
|---|---|---|
| 모델 | 어떤 모델을 어떤 일에 쓸까, 작업당 비용과 속도는 | 2회 (10월 30일) |
| 실행 틀·작업 공간 | 도구를 함수 호출로 줄까, MCP로 붙일까, 화면을 조작하게 할까 | 3회 (10월 31일) |
| 실행 틀 | 긴 일을 할 때 무엇을 기억하고 무엇을 버릴까, '스킬'은 어떻게 쌓을까 | 4회 (11월 1일) |
| 전체 | 잘 만들었는지 어떻게 측정할까 | 5회 (11월 2일) |
| 실행 틀·작업 공간 | 권한, 샌드박스, 프롬프트 인젝션을 어떻게 막을까 | 6회 (11월 3일) |
| 전체 | 사람은 어디서 승인하고, 비용과 로그는 어떻게 볼까 | 7회 (11월 4일) |

한 가지 원칙을 먼저 적어 둔다. 실행 틀에서 고칠 수 있는 문제를 모델 교체로 풀려 하지 않는 것이다. 에이전트가 엉뚱한 파일을 고친다면 더 큰 모델보다 작업 공간의 권한을 좁히는 편이 빠르고 싸다. 에이전트가 같은 실수를 반복한다면 모델보다 실행 틀의 재시도·검증 단계를 먼저 본다. 반대로 실행 틀을 아무리 다듬어도 모델이 화면을 못 읽으면 소용이 없다. 어느 층의 문제인지 가르는 것이 에이전트를 만드는 첫 기술이다.

올해 에이전트가 빨라진 흐름은 [AI는 왜 이렇게 빨라졌나](https://now.zeta4.net/a/2026-10-09-ai-race-eleven-months)에, 에이전트가 실제로 일으킨 사고는 [현실로 나타나는 AI 에이전트 위험](https://now.zeta4.net/a/2026-10-10-ai-agent-risks-become-real)에 정리돼 있다.

## 확인할 점

- 'Work Agents' 논문의 다섯 업무 형태와 다섯 능력 계열의 세부 정의는 초록과 논문 소개 페이지 기준으로 정리했다. 저자 소속은 소개 페이지에 표시되지 않았다.
- Claude Duet의 Opus 5.5 사용, 클라우드 가상 머신, 승인 대상, 미국 대기자 명단은 Anthropic 공식 계정 게시물이 아니라 보도로 확인했다. Anthropic의 제품 공지 원문은 직접 열지 못했다.
- ChatGPT Work의 출시 모델은 7월 기준 GPT-5.6이다. 이후 GPT-6 계열로 바뀌었다는 보도가 있지만 OpenAI 원문으로 확인하지 못했다.
- GPT-6.1 Terra의 작업당 비용 비교는 OpenAI 자체 측정이다.

## 출처

- [Work Agents: Systems, Capabilities, and Optimization — arXiv](https://arxiv.org/abs/2610.35845)
- [ChatGPT for your most ambitious work — OpenAI](https://openai.com/index/chatgpt-for-your-most-ambitious-work/)
- [Claude Duet 연구 프리뷰 공지 — Claude 공식 X](https://x.com/claudeai/status/2112984664256241837)
- [Anthropic unveils Claude Duet — Yahoo Tech](https://tech.yahoo.com/ai/claude/articles/anthropic-unveils-claude-duet-answer-002554435.html)
- [Claude Duet: Anthropic opens proactive AI agent preview — BetaNews](https://betanews.com/article/proactive-ai-agent-claude-duet/)
- [Introducing GPT-6.1 Terra — OpenAI](https://openai.com/index/introducing-gpt-6-1-terra/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
