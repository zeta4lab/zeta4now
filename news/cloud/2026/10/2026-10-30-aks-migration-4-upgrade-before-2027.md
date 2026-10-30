---
title: AKS 2027년 6월 강제 업그레이드 대비…취소도 롤백도 없는 업그레이드를 피하는 법
slug: 2026-10-30-aks-migration-4-upgrade-before-2027
topic: cloud
published_at: 2026-10-30T01:03:00+09:00
tags:
  - AKS 실전 이전
  - AKS
  - Azure
  - Kubernetes
  - 업그레이드
summary: AKS 실전 이전 가이드 5회 연재의 4회. 2027년 6월 1일부터 AKS는 지원이 끝난 클러스터를 유지보수 시간대도, deprecated API 검사도, 롤백도 없이 강제로 업그레이드한다. 위험 클러스터 찾기, deprecated API 점검, 컨트롤 플레인과 노드풀 순서, 자동 업그레이드 루틴을 정리한다.
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-12-01
      note: Kubernetes 1.34 지원 종료(11월) 반영과 1.38 preview 출시 여부 확인
---

# AKS 2027년 6월 강제 업그레이드 대비…취소도 롤백도 없는 업그레이드를 피하는 법

## 한눈에 보기

[AKS 입문 1회](https://now.zeta4.net/a/2026-10-30-aks-101-what-aks-manages)에서 2027년 6월부터 강제 업그레이드가 시작된다고 짚었다. Microsoft는 이를 "플랫폼 주도 업그레이드(platform-initiated upgrade)"라는 별도 문서로 정리했다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/platform-initiated-upgrades)). 2027년 5월 31일까지는 사용자가 직접 올리는 기간이고, 6월 1일부터는 AKS가 지원이 끝난 클러스터를 직접 올린다. 그 뒤로는 각 버전의 지원 종료 다음 날부터 60일 유예가 지나면 같은 일이 반복된다. 이번 회는 이 업그레이드를 맞지 않는 방법, 곧 스스로 먼저 올리는 루틴을 다룬다.

## 강제 업그레이드는 무엇을 무시하나

| 평소 업그레이드 | 플랫폼 주도 업그레이드 |
|---|---|
| 유지보수 시간대를 따른다 | 따르지 않는다 |
| deprecated API를 쓰면 멈춘다 | 검사를 건너뛴다 |
| PDB와 surge 설정을 지킨다 | 최선 노력. drain이 실패하면 PDB를 무시하고, surge 노드를 못 만들면 노드를 하나씩 비우며 진행 |
| 업그레이드 채널 설정을 따른다 | `none`, `patch`를 포함해 무시 |
| 취소·롤백 | 끄기, 취소, 롤백 모두 불가 |

마이너 버전은 한 번에 하나씩 올리고, 컨트롤 플레인 다음에 노드풀 순서로 진행한다. 노드 OS 종류(OS SKU)는 바꾸지 않는다. 2027년 6월 시점에 기대하는 버전은 일반 클러스터 1.36 이상, LTS 클러스터 1.33 LTS 이상이다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/platform-initiated-upgrades)).

알림은 Resource Health(Degraded 표시), 포털 배너, Azure Advisor, AKS Communication Manager 이메일, 진단 및 문제 해결 화면으로 온다. 실제로 일어났는지는 활동 로그에서 `upgradeTrigger=PlatformInitiatedUnsupportedVersion`으로 확인한다.

## 1단계: 위험한 클러스터 찾기

구독이 여러 개라면 Azure Resource Graph로 한 번에 본다. 아래는 문서에 나온 쿼리다.

```bash
az graph query -q "resources | where type =~ 'microsoft.containerservice/managedclusters' | project clusterName = name, resourceGroup, subscriptionId, kubernetesVersion = properties.kubernetesVersion, tier = properties.sku.tier, supportPlan = properties.supportPlan | order by kubernetesVersion asc" --output table
```

버전별 일정과 맞춰 본다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions)).

| 버전 | 지원 종료 | 플랫폼 주도 업그레이드 |
|---|---|---|
| 1.32~1.35 | 1.34는 2026-11, 1.35는 2027-03 | 2027-06 |
| 1.36 | 2027-06 | 2027-09 |
| 1.37 | 2027-10 | 2028-01 |

일반(비 LTS) 클러스터는 마이너 버전을 건너뛸 수 없다. 1.33에서 1.36으로 가려면 1.34, 1.35를 거쳐야 하므로, 오래된 클러스터일수록 일찍 시작해야 한다.

```bash
az aks get-upgrades --resource-group $RG --name $CLUSTER --output table
```

## 2단계: deprecated API 점검

AKS는 기본으로 **deprecated API를 쓰는 클러스터의 업그레이드를 멈춘다.** 대상 버전이 1.26 이상인 마이너 업그레이드에서, 최근 12시간 안에 제거될 API를 호출한 기록이 있으면 `UpgradeBlockedOnDeprecatedAPIUsage` 오류로 막는다. 조회(get, list, watch)는 세지 않는다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/stop-cluster-upgrade-api-breaking-changes)).

어떤 API를 쓰는지는 포털의 **진단 및 문제 해결 → Create, Upgrade, Delete, and Scale → Kubernetes API deprecations**에서 본다. Container Insights의 감사 로그로도 확인할 수 있다. 컨트롤 플레인 업그레이드 문서는 오픈소스 도구 kubent로 매니페스트를 점검하라고 권한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-control-plane)).

이 검사를 우회하는 `--enable-force-upgrade`도 있지만 권장하지 않는다. 우회한다는 것은 강제 업그레이드와 같은 위험을 스스로 지는 것이다. 무엇보다 6월 이후 플랫폼 주도 업그레이드는 이 검사 자체를 건너뛴다. 막혀 있을 때 고쳐 두지 않으면, 나중에 막아 줄 장치가 없다.

참고로 Kubernetes 공식 deprecation 가이드는 1.32까지만 정리돼 있고 1.33 이후 항목이 없다. 그렇다고 "제거되는 API가 없다"고 볼 수는 없다. 각 버전 릴리스 노트와 AKS의 점검 화면을 함께 본다. AKS 쪽에서는 1.37부터 ServiceMonitor·PodMonitor의 basicAuth 비밀 접근 방식이 바뀐다는 공지가 있다.

## 3단계: 순서대로 올리기

업그레이드는 컨트롤 플레인이 먼저다. 노드풀을 컨트롤 플레인보다 먼저 올릴 수는 없다. 1.28부터는 컨트롤 플레인이 노드풀보다 최대 세 마이너 버전까지 앞설 수 있어, 컨트롤 플레인만 먼저 올리고 노드풀은 나눠서 올리는 것도 가능하다.

```bash
az aks upgrade --resource-group $RG --name $CLUSTER --kubernetes-version <버전> --control-plane-only
az aks nodepool list --resource-group $RG --cluster-name $CLUSTER \
  --query "[].{Name:name,Version:orchestratorVersion}" --output table
```

자동 업그레이드 채널이 켜져 있으면 `--control-plane-only`는 오류가 난다. 이미 지원이 끝난 클러스터를 되살릴 때는 컨트롤 플레인만 따로 올릴 수 없고 전체 업그레이드만 된다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-control-plane)). 노드풀 업그레이드의 surge·drain 설정은 [AKS 입문 6회](https://now.zeta4.net/a/2026-10-30-aks-106-operations-and-cost)를 참고한다.

## 4단계: 다시는 밀리지 않게, 자동 업그레이드 루틴

한 번 따라잡았다면 다시 밀리지 않게 만든다. Microsoft의 권장은 `stable` 채널과 4시간 이상의 유지보수 시간대 조합이다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-cluster)).

```bash
az aks update --resource-group $RG --name $CLUSTER --auto-upgrade-channel stable
az aks maintenanceconfiguration add --resource-group $RG --cluster-name $CLUSTER \
  --name aksManagedAutoUpgradeSchedule --schedule-type Weekly --day-of-week Sunday \
  --interval-weeks 1 --duration 4 --utc-offset +09:00 --start-time 02:00
```

`patch` 채널은 패치 버전만 올리고 마이너 버전은 그대로 두므로, 이것만으로는 강제 업그레이드를 피할 수 없다. 클러스터가 여러 개면 Azure Kubernetes Fleet Manager로 테스트 클러스터를 먼저, 운영 클러스터를 나중에 올리는 단계를 둘 수 있다. 다만 지원이 끝난 클러스터에는 Fleet의 순서가 적용되지 않는다.

한 버전에 오래 머물러야 할 사정이 있으면 Premium 티어의 장기 지원(LTS)을 켠다. 단, Ubuntu 22.04 노드풀로는 1.33 이상 LTS를 켤 수 없어 노드 OS부터 옮겨야 한다. 이 내용은 다음 회에서 다룬다.

## 정리

- Resource Graph로 모든 클러스터의 버전을 뽑고, 2027-06 대상인 1.35 이하부터 계획한다.
- deprecated API 차단은 막아 주는 장치다. 우회하지 말고 고친다.
- 컨트롤 플레인 → 노드풀 순서, 마이너 버전은 하나씩.
- 따라잡은 뒤에는 `stable` 채널과 유지보수 시간대로 자동화한다.

마지막 회에서는 노드 OS 이전, 특히 10월 31일 이미지가 삭제되는 Azure Linux 2.0과 Ubuntu 버전 전환을 다룬다.

## 출처

- [Platform-initiated upgrades for unsupported AKS clusters — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/platform-initiated-upgrades)
- [Supported Kubernetes versions in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions)
- [Stop cluster upgrades on API breaking changes — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/stop-cluster-upgrade-api-breaking-changes)
- [Upgrade the AKS control plane — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-control-plane)
- [Automatically upgrade an AKS cluster — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-cluster)
- [Deprecated API migration guide — Kubernetes](https://kubernetes.io/docs/reference/using-api/deprecation-guide/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
