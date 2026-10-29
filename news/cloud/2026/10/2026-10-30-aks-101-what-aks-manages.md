---
title: AKS가 맡는 것과 내가 맡는 것…컨트롤 플레인은 Microsoft, 노드와 업그레이드 결정은 사용자
slug: 2026-10-30-aks-101-what-aks-manages
topic: cloud
published_at: 2026-10-30T00:30:00+09:00
tags:
  - AKS 입문
  - AKS
  - Azure
  - Kubernetes
summary: Azure Kubernetes Service(AKS)를 처음 쓰는 개발자를 위한 6회 연재의 첫 편. AKS가 대신 운영하는 부분과 사용자가 끝까지 책임지는 부분, Free·Standard·Premium 티어와 AKS Automatic의 차이, 버전 지원 정책과 2027년 6월부터 시작되는 강제 업그레이드를 정리한다.
generated_by: claude
model: claude-opus-5-5
---

# AKS가 맡는 것과 내가 맡는 것…컨트롤 플레인은 Microsoft, 노드와 업그레이드 결정은 사용자

## 한눈에 보기

AKS(Azure Kubernetes Service)는 "Kubernetes를 대신 운영해 주는 서비스"로 흔히 소개되지만, 실제로 Microsoft가 맡는 범위는 생각보다 좁다. API server와 etcd 같은 컨트롤 플레인은 Microsoft가 운영하지만, 노드를 어떻게 구성하고 언제 업그레이드하며 워크로드와 데이터를 어떻게 지킬지는 사용자 몫이다. 이 연재는 Kubernetes를 조금 아는 개발자를 위해 AKS를 6회에 걸쳐 정리한다. 첫 편은 책임 분담, 가격 티어, 버전 정책이라는 세 가지 기본 틀을 다룬다.

연재 순서는 다음과 같다. 1회 AKS가 맡는 것과 내가 맡는 것, [2회 클러스터와 노드풀](https://now.zeta4.net/a/2026-10-30-aks-102-cluster-and-node-pools), [3회 네트워킹](https://now.zeta4.net/a/2026-10-30-aks-103-networking), [4회 ID와 보안](https://now.zeta4.net/a/2026-10-30-aks-104-identity-security), [5회 앱 배포와 확장](https://now.zeta4.net/a/2026-10-30-aks-105-deploy-and-scale), [6회 운영과 비용](https://now.zeta4.net/a/2026-10-30-aks-106-operations-and-cost).

## 세 칸으로 나뉘는 책임

Microsoft의 지원 정책 문서는 책임을 세 칸으로 나눈다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/support-policies)).

| 구분 | 내용 |
|---|---|
| Microsoft | 컨트롤 플레인(API server, etcd, scheduler, controller)과 그 고가용성, etcd 자동 백업(30분마다), 노드 자동 복구, 노드의 containerd·kubelet·kube-proxy |
| 공동 | Kubernetes 버전 업그레이드(버전 제공은 Microsoft, 실행과 일정은 사용자), 노드 OS 패치(이미지 제공은 Microsoft, 채널 선택과 적용은 사용자), 노드 자동 확장(도구 제공은 Microsoft, 최소·최대 정책은 사용자), 관리형 애드온과 CNI |
| 사용자 | 노드풀 구성(VM 크기, 개수, 레이블, taint), VNet과 NSG, RBAC, 시크릿, 워크로드, 데이터, 백업과 재해 복구 |

눈여겨볼 점이 둘 있다. 첫째, etcd 백업은 Microsoft가 하지만 사용자는 그 백업에 접근하거나 복원할 수 없다. 내 앱과 데이터의 백업은 따로 챙겨야 한다(6회에서 다룬다). 둘째, 노드 이미지는 매주 나오고, 90일보다 오래된 이미지는 지원 대상이 아니다. "관리형"이라도 업데이트를 적용하지 않으면 지원 범위 밖으로 밀려난다.

## 노드는 내 구독에 있지만 마음대로 고치면 안 된다

AKS 노드는 사용자의 구독에서 돌아가는 가상 머신 확장 집합(VMSS)이다. 이 VM들은 클러스터 리소스와 별도로 `MC_` 접두사가 붙은 노드 리소스 그룹에 만들어진다. 클러스터를 지우면 이 그룹도 함께 지워진다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-system-pools)).

노드가 내 구독에 보인다고 해서 Azure 포털이나 IaaS API로 VM을 직접 고치면 안 된다. 지원 정책은 이렇게 하면 클러스터가 지원할 수 없는(unsupportable) 상태가 된다고 경고한다. 노드에 설정을 더해야 하면 DaemonSet처럼 Kubernetes 방식으로 한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/support-policies)).

## 가격 티어: 컨트롤 플레인에 무엇을 보장받을 것인가

AKS의 "티어"는 노드 요금이 아니라 컨트롤 플레인에 붙는 요금과 보장 수준이다. 노드 VM 요금은 티어와 별개로 낸다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/free-standard-pricing-tiers)).

| 티어 | 용도 | 노드 한도 | 가동 시간 SLA |
|---|---|---|---|
| Free | 개발·테스트, 10노드 미만 권장 | 1,000 | 금전 보상 SLA 없음 |
| Standard | 운영 | 5,000 | 포함 |
| Premium | 운영 + 장기 지원(LTS) | 5,000 | 포함 |

Standard와 Premium의 API server SLA는 가용 영역을 쓰면 99.95%, 쓰지 않으면 99.9%다. Azure 소매 가격 API의 미국 동부·달러 기준으로 Standard는 클러스터당 시간당 0.10달러, Premium(장기 지원 포함)은 0.60달러다. 리전과 계약에 따라 다를 수 있으니 실제 비용은 [가격 페이지](https://azure.microsoft.com/pricing/details/kubernetes-service/)와 계산기로 확인해야 한다.

```bash
az aks create --resource-group $RG --name $CLUSTER --tier standard --generate-ssh-keys
```

## AKS Automatic: 결정을 미리 내려 둔 AKS

AKS에는 두 가지 형태가 있다. 지금까지 설명한 기본형(Standard)과, 2025년 8월 GA된 AKS Automatic이다. Automatic은 운영에 필요한 선택 대부분을 Microsoft 권장값으로 미리 정해 둔 형태다. Standard 티어, Azure CNI Overlay와 Cilium, Microsoft Entra 기반 Azure RBAC, 워크로드 ID, 노드 자동 프로비저닝(Karpenter), HPA·KEDA·VPA, 배포 안전장치(Deployment Safeguards), Managed Prometheus와 Container Insights가 처음부터 켜져 있다. 시스템 노드풀도 AKS가 관리하며 사용자의 구독이 아닌 AKS 쪽에 호스팅된다. 업그레이드는 stable 채널과 NodeImage 채널로 고정된다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/intro-aks-automatic)).

Automatic에는 API server SLA 외에 pod 준비 SLA가 붙는다. 적격 작업의 99.9%가 5분 안에 Ready가 된다는 약속이다. 요금 구조도 다르다. 같은 가격 API 기준으로 컨트롤 플레인 시간당 0.16달러에 더해 vCPU 시간당 요금이 붙는다(범용 VM 기준 0.007841달러). 이 연재의 3~6회에서 다룰 기능 상당수가 Automatic에서는 기본으로 켜져 있으므로, 각 회에서 "Automatic이면 이미 되어 있는 것"을 함께 표시한다.

## 버전 정책: 1년마다 올려야 하고, 안 올리면 강제로 올라간다

AKS는 Kubernetes 마이너 버전 세 개(N, N-1, N-2)를 지원하고, 각 버전은 AKS에서 GA된 날부터 12개월 지원한다. 새 클러스터의 기본 버전은 N-1이다. 2026년 10월 현재 1.37이 최신 GA이고 1.36이 기본이다. 1.34는 2026년 11월에 지원이 끝난다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions)).

| 버전 | AKS GA | 지원 종료 |
|---|---|---|
| 1.34 | 2025-11 | 2026-11 |
| 1.35 | 2026-03 | 2027-03 |
| 1.36 | 2026-06 | 2027-06 |
| 1.37 | 2026-10 | 2027-10 |

입문자가 꼭 기억해야 할 변화가 있다. 2027년 6월 1일부터 AKS는 지원이 끝난 버전에 60일 넘게 머문 클러스터를 플랫폼이 직접 업그레이드한다. 이 업그레이드는 유지보수 시간대를 따르지 않고, 더는 쓸 수 없는(deprecated) API가 남아 있어도 멈추지 않으며, PodDisruptionBudget을 무시할 수 있다. 끌 수 있는 옵션은 없다. 업그레이드를 미루면 원하지 않는 시점에 장애를 겪을 수 있다는 뜻이다.

더 길게 머물러야 하면 Premium 티어의 장기 지원(LTS)을 켠다. 커뮤니티 지원 1년에 LTS 1년을 더해 약 24개월을 한 버전에 머물 수 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/long-term-support)).

## 정리: 첫 클러스터 전에 정할 것

- 이 클러스터는 운영용인가? 운영용이면 Free가 아니라 Standard 이상을 쓴다.
- 직접 고를 것인가, Automatic의 기본값을 받을 것인가? 처음이라면 Automatic이 실수를 줄인다.
- 1년에 한 번 이상 마이너 버전을 올릴 사람과 절차가 있는가? 없다면 2027년 6월부터는 플랫폼이 대신 올린다.

다음 회에서는 실제로 클러스터와 노드풀을 만들며 VM 크기, 가용 영역, 노드 OS, 자동 확장을 고른다.

## 출처

- [Support policies for AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/support-policies)
- [Free, Standard, and Premium pricing tiers for AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/free-standard-pricing-tiers)
- [What is AKS Automatic? — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/intro-aks-automatic)
- [Supported Kubernetes versions in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions)
- [Long-term support for AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/long-term-support)
- [Use system node pools in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-system-pools)
- [Azure Kubernetes Service pricing — Microsoft Azure](https://azure.microsoft.com/pricing/details/kubernetes-service/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
