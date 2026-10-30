---
title: AKS 노드 OS 이전…Azure Linux 2.0은 10월 31일 이미지 삭제, Ubuntu 22.04는 2027년 6월 지원 종료
slug: 2026-10-30-aks-migration-5-node-os
topic: cloud
published_at: 2026-10-30T01:04:00+09:00
tags:
  - AKS 실전 이전
  - AKS
  - Azure
  - Kubernetes
  - Azure Linux
  - Ubuntu
summary: AKS 실전 이전 가이드 5회 연재의 마지막 회. 노드 OS는 명령 한 줄로 제자리에서 바꾸거나, 새 노드풀을 만들어 옮기는 두 방법이 있다. Azure Linux 2.0과 Ubuntu 20.04·22.04의 은퇴 일정, OS SKU와 Kubernetes 버전의 관계, 두 이전 방법의 절차와 주의점을 정리한다.
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-11-02
      note: Azure Linux 2.0 노드 이미지 삭제(10월 31일) 실행과 영향 확인
---

# AKS 노드 OS 이전…Azure Linux 2.0은 10월 31일 이미지 삭제, Ubuntu 22.04는 2027년 6월 지원 종료

## 한눈에 보기

[AKS 입문 2회](https://now.zeta4.net/a/2026-10-30-aks-102-cluster-and-node-pools)에서 노드 OS의 은퇴 일정을 표로 봤다. 가장 급한 것은 Azure Linux 2.0이다. 지원은 2025년 11월 30일에 끝났고, 이미지는 `202512.06.0`에서 멈췄으며, **2026년 10월 31일부터 노드 이미지가 삭제되어 노드풀을 확장할 수 없다**([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-os-version)). 다음은 Ubuntu 20.04(2027-03-17)와 22.04(2027-06-30)다. 이번 회는 노드 OS를 옮기는 두 방법, 곧 제자리 변경과 새 노드풀 교체를 다룬다.

## 은퇴 일정 다시 보기

| OS | 지원 종료 | 이미지 삭제 | 삭제 후 |
|---|---|---|---|
| Azure Linux 2.0 | 2025-11-30 | 2026-10-31 | 노드풀 확장 불가 |
| Ubuntu 20.04 | 2027-03-17 | 2027-03-17 | 확장 불가 |
| Ubuntu 22.04 | 2027-06-30(새 풀·이미지·패치 중단) | 2028-04-30 | 확장·복구 실패 |
| Azure Linux with OS Guard(preview) | 2026-12-10 | 2027-03-10 | — |

Azure Linux 2.0이 이미지 삭제 뒤 확장 말고 업그레이드나 재이미지에서도 실패하는지는 문서에 나와 있지 않다. 확장이 막히는 것만으로도 부하가 몰릴 때 노드를 늘릴 수 없다는 뜻이니 기다릴 이유가 없다. Azure Linux 2.0을 지원하는 마지막 AKS 버전은 1.31이므로, 이 노드풀이 남아 있다면 Kubernetes 버전도 뒤처져 있을 가능성이 크다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-linux/aks-support-cycle)). [4회](https://now.zeta4.net/a/2026-10-30-aks-migration-4-upgrade-before-2027)의 강제 업그레이드는 OS SKU를 바꿔 주지 않는다는 점도 기억한다.

## 0단계: 노드풀 현황 보기

```bash
az aks nodepool list -g $RG --cluster-name $CLUSTER \
  --query "[].{Name:name,OsSku:osSku,Version:orchestratorVersion,Image:nodeImageVersion}" -o table
```

## OS SKU와 Kubernetes 버전의 관계

OS를 고르는 값(OS SKU)에는 버전이 고정된 것과 Kubernetes 버전을 따라 바뀌는 것이 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-os-version)).

- `Ubuntu`: Kubernetes 버전에 따라 기본 버전이 바뀐다. 1.34까지는 22.04이고, 문서에 따르면 1.35부터 24.04로 바뀐다. Kubernetes를 올리면 OS도 따라 바뀐다.
- `Ubuntu2204`: 1.25~1.36에서 쓸 수 있다. `Ubuntu2404`: 1.32~1.38.
- `AzureLinux`: 1.32 이상에서 Azure Linux 3.0이 기본이다. `AzureLinux3`는 1.28~1.36에서 쓸 수 있다.

다만 Microsoft 문서 안에서 1.35의 기본 Ubuntu 버전이 엇갈린다. 같은 페이지의 다른 행과 버전 지원 문서의 구성 요소 표에는 1.35에 22.04가 적혀 있다. 1.35 클러스터라면 위 명령으로 실제 노드 이미지를 확인하는 것이 확실하다. `Ubuntu2204`처럼 버전을 고정한 SKU를 쓰면 Kubernetes를 올려도 OS가 바뀌지 않으니, 은퇴 일정에 맞춰 직접 바꿔야 한다.

## 방법 1: 제자리 변경

지원되는 Linux OS SKU끼리는 `az aks nodepool update`로 제자리에서 바꿀 수 있다. GA 기능이다. OS가 바뀌면 노드가 다시 만들어진다(reimage). 대상 노드 이미지가 없으면 실패할 수 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-os-version)).

```bash
az aks nodepool update --resource-group $RG --cluster-name $CLUSTER \
  --name $NODE_POOL_NAME --os-sku AzureLinux
```

Ubuntu에서 Azure Linux로, 또는 그 반대로 바꿀 때는 Azure CLI 2.61.0 이상이 필요하고 포털과 PowerShell에서는 할 수 없다. Windows, Kata, GPU 전용 이미지(`UseGPUDedicatedVHD`), 기밀 VM의 20.04 노드풀은 제자리 변경이 안 된다. 바꾼 뒤 `kubectl get nodes -o wide`에서 이미지가 "Microsoft Azure Linux 3.0"이고 커널 버전이 `.azl3`로 끝나면 성공이다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-linux/tutorial-migrate-azure-linux-aks)).

Azure Linux 2.0에서 3.0으로 옮길 때는 주의가 필요하다. 문서는 1.28~1.36에서 쓸 수 있는 `AzureLinux3` SKU를 2.0→3.0 이전에 쓸 수 있다고 적었지만, `--os-sku AzureLinux3`를 넣은 명령 예시는 따로 싣지 않았다. `AzureLinux` SKU는 1.32 이상에서 3.0이 기본이고, Azure Linux 2.0을 지원하는 마지막 버전은 1.31이다. 스테이징에서 SKU 변경을 먼저 시험하고, 안 되면 아래 방법 2(새 노드풀 교체)로 간다. Kubernetes 버전이 뒤처져 있다면 [4회](https://now.zeta4.net/a/2026-10-30-aks-migration-4-upgrade-before-2027)의 업그레이드도 함께 계획한다.

제자리 변경은 노드 업그레이드처럼 노드를 차례로 바꾼다. [AKS 입문 6회](https://now.zeta4.net/a/2026-10-30-aks-106-operations-and-cost)의 surge·drain 설정과 앱의 PDB가 그대로 적용된다.

## 방법 2: 새 노드풀로 교체

더 조심스럽게 옮기고 싶거나 제자리 변경이 안 되는 경우에는 새 노드풀을 만들고 워크로드를 옮긴다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-conceptual)).

1. 새 OS로 노드풀을 추가한다. 시스템 풀을 바꾸는 경우라면 `--mode System`으로 만든다. 시스템 모드 풀이 하나 이상 있어야 기존 시스템 풀을 지울 수 있다.
2. 기존 노드를 `kubectl cordon`으로 새 pod를 받지 않게 막는다.
3. `kubectl drain`으로 기존 노드의 pod를 내보낸다. pod는 새 노드풀로 옮겨 간다.
4. 앱이 정상인지 확인한다.
5. 기존 노드풀을 지운다.

```bash
az aks nodepool add --resource-group $RG --cluster-name $CLUSTER \
  --name newsys --mode System --os-sku AzureLinux
kubectl cordon -l agentpool=<기존 풀 이름>
kubectl drain -l agentpool=<기존 풀 이름> --ignore-daemonsets --delete-emptydir-data
az aks nodepool delete --resource-group $RG --cluster-name $CLUSTER --name <기존 풀 이름>
```

문제가 생기면 기존 노드를 `kubectl uncordon`으로 되살리고 새 노드풀을 비우면 된다. 기존 노드풀을 지우기 전까지는 언제든 되돌릴 수 있다는 것이 이 방법의 장점이다. 워크로드가 노드 선택자(nodeSelector)나 어피니티로 기존 노드풀 이름을 가리키고 있다면 새 노드풀로 옮겨 가지 못하니 미리 확인한다.

AKS가 관리하는 블루-그린 노드풀 업그레이드(`--upgrade-strategy bluegreen`)도 있지만 preview이고, Kubernetes 버전과 노드 이미지 업그레이드만 지원해 **OS SKU 변경에는 쓸 수 없다**([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/blue-green-node-pool-upgrade)).

## 어느 방법을 고를까

| 상황 | 권장 |
|---|---|
| 사용자 노드풀, 앱이 PDB와 레플리카를 갖춤 | 제자리 변경 |
| 시스템 풀, 또는 확인하며 천천히 옮기고 싶을 때 | 새 노드풀 교체 |
| Windows·GPU 전용 이미지 등 제자리 변경 불가 | 새 노드풀 교체 |
| Ubuntu 22.04에서 LTS 1.33 이상을 켜야 할 때 | 먼저 24.04로 변경 |

## 연재를 마치며: 이전 일정표

| 마감 | 할 일 | 회차 |
|---|---|---|
| 2026-10-31 | Azure Linux 2.0 노드풀 이전 | 5회 |
| 2026-11 | 관리형 NGINX를 Gateway API 또는 AGC로 | 1회 |
| 이미 지남 | pod 관리 ID를 워크로드 ID로 | 3회 |
| 2027-03-17 | Ubuntu 20.04 이전 | 5회 |
| 2027-06-01 | 1.35 이하 클러스터 업그레이드 | 4회 |
| 2027-06-30 | Ubuntu 22.04 이전 | 5회 |
| 2028-03-31 | kubenet을 Azure CNI Overlay로 | 2회 |
| 2028-09-30 | Azure NPM(Linux)을 Cilium으로 | 2회 |

## 출처

- [Upgrade the OS version for AKS node pools — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-os-version)
- [Azure Linux support cycle on AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-linux/aks-support-cycle)
- [Migrate to Azure Linux on AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-linux/tutorial-migrate-azure-linux-aks)
- [Upgrade options for AKS clusters — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-conceptual)
- [Blue-green node pool upgrade — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/blue-green-node-pool-upgrade)
- [Supported Kubernetes versions in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
