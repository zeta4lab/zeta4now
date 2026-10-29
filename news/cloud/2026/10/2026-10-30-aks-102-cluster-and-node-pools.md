---
title: AKS 클러스터와 노드풀 만들기…시스템 풀 분리, 가용 영역, 노드 OS, 자동 확장
slug: 2026-10-30-aks-102-cluster-and-node-pools
topic: cloud
published_at: 2026-10-30T00:31:00+09:00
tags:
  - AKS 입문
  - AKS
  - Azure
  - Kubernetes
  - 노드풀
summary: AKS 입문 6회 연재의 2회. 시스템 노드풀과 사용자 노드풀을 나누는 이유, 만든 뒤에는 바꿀 수 없는 가용 영역, Ubuntu·Azure Linux 노드 OS와 은퇴 일정, 클러스터 오토스케일러와 노드 자동 프로비저닝, Spot 노드풀, 업그레이드 채널과 유지보수 시간대를 정리한다.
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-11-02
      note: Azure Linux 2.0 노드 이미지 삭제(10월 31일) 실행과 영향 확인
---

# AKS 클러스터와 노드풀 만들기…시스템 풀 분리, 가용 영역, 노드 OS, 자동 확장

## 한눈에 보기

[1회](https://now.zeta4.net/a/2026-10-30-aks-101-what-aks-manages)에서 봤듯 AKS에서 노드풀 구성은 사용자의 책임이다. 이번 회는 `az aks create` 한 줄 뒤에 숨은 결정을 하나씩 꺼낸다. 시스템 풀과 사용자 풀을 나누고, 가용 영역을 처음부터 정하고, 노드 OS의 은퇴 일정을 확인하고, 자동 확장 방식과 업그레이드 시간대를 고른다. AKS Automatic을 쓰면 이 가운데 상당수가 이미 정해져 있다.

## 노드풀은 두 종류다: System과 User

AKS 노드풀은 System 모드와 User 모드로 나뉜다. System 풀은 CoreDNS, metrics-server 같은 클러스터 핵심 구성 요소를 돌린다. 조건이 까다롭다. Linux만 되고, B 시리즈 VM은 쓸 수 없으며, 최소 4 vCPU·4GB 메모리, 최소 2노드(권장 3노드)여야 한다. User 풀은 앱을 돌리는 곳으로 노드 0개까지 줄일 수 있고 Windows도 쓸 수 있다. `az aks nodepool add`로 만든 풀은 기본이 User 모드다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-system-pools)).

운영 클러스터라면 시스템 풀에 앱 pod가 올라가지 않도록 taint를 거는 것이 좋다. 앱이 메모리를 다 써서 CoreDNS가 밀려나는 사고를 막는다.

```bash
az aks nodepool add -g $RG --cluster-name $CLUSTER --name systempool \
  --node-count 3 --node-taints CriticalAddonsOnly=true:NoSchedule --mode System
```

노드풀 이름은 Linux가 1~12자, Windows가 1~6자로 짧다. 이름 규칙을 미리 정해 두자.

## 가용 영역은 만들 때 정한다

`--zones 1 2 3`을 주면 노드풀의 노드가 세 가용 영역에 나뉘어 배치된다. 영역 분산 자체에는 추가 비용이 없다. 중요한 제약은 **노드풀을 만든 뒤에는 영역 구성을 바꿀 수 없다**는 것이다. 영역 없이 만든 풀을 나중에 영역 분산으로 바꾸려면 새 풀을 만들고 옮겨야 한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/reliability/reliability-aks)). 가용 영역을 지원하는 리전이라면 운영 풀은 처음부터 영역을 지정하는 편이 낫다. 1회에서 본 99.95% API server SLA도 가용 영역을 쓸 때의 수치다.

## 노드 OS: 기본은 Ubuntu, 은퇴 일정을 꼭 확인

`--os-sku`를 지정하지 않으면 Ubuntu 노드가 만들어진다. Kubernetes 1.35 이상에서 `Ubuntu`는 24.04를 가리킨다. 다른 선택지로 Microsoft의 Azure Linux(`AzureLinux3`)와 1.34부터 GA된 Azure Container Linux가 있다. Linux 노드 이미지는 매주, Windows 이미지는 매월 나온다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/node-images)).

| OS | 상태 |
|---|---|
| Azure Linux 2.0 | 2025-11-30 지원 종료, **2026-10-31 이미지 삭제** |
| Ubuntu 20.04 | 2027-03-17 지원 종료 |
| Ubuntu 22.04 | 2027-06-30 지원 종료 |
| Windows Server 2019 | 2026-03-01 은퇴 |
| Windows Server 2022 | 2028-06-30 은퇴, Kubernetes 1.37 이상에서 미지원 |
| Windows Server 2025 | GA |

Azure Linux 2.0 노드풀이 남아 있다면 지금 바로 확인해야 한다. 이미지가 삭제된 뒤에는 그 노드풀을 확장할 수 없다. `AzureLinux3`로 옮기는 것이 안내된 경로다.

## 자동 확장: 클러스터 오토스케일러와 노드 자동 프로비저닝

pod가 늘어 노드가 모자랄 때 노드를 늘리는 방법은 두 가지다.

- **클러스터 오토스케일러**: 노드풀마다 최소·최대 노드 수를 정하면 그 범위 안에서 같은 VM 크기의 노드를 늘리고 줄인다. 기본은 꺼져 있다(`--enable-cluster-autoscaler --min-count 1 --max-count 5`).
- **노드 자동 프로비저닝(NAP)**: 오픈소스 Karpenter 기반으로 2025년 7월 GA됐다. 대기 중인 pod의 요구에 맞는 VM 크기를 골라 노드를 만든다. `NodePool`과 `AKSNodeClass` CRD로 설정한다. Windows 노드, IPv6, 서비스 주체 인증은 지원하지 않고, NAP를 쓰는 클러스터는 정지(stop)할 수 없다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/node-autoprovision)).

AKS Automatic은 NAP를 기본으로 쓴다. 기본형에서 처음 시작한다면 클러스터 오토스케일러가 동작을 예측하기 쉽다.

## Spot 노드풀: 싸지만 언제든 회수된다

Spot 노드풀은 Azure의 남는 용량을 할인된 값에 쓰는 노드풀이다. 대신 Azure가 용량이 필요하면 노드를 회수(축출)한다. SLA가 없고, 시스템 풀이나 클러스터의 기본 노드풀로는 만들 수 없으며, 업그레이드할 때 surge 노드도 없다. Spot 노드에는 `kubernetes.azure.com/scalesetpriority=spot:NoSchedule` taint가 자동으로 붙어, 이를 허용(toleration)한 pod만 올라간다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/spot-node-pool)).

```bash
az aks nodepool add -g $RG --cluster-name $CLUSTER --name spotpool \
  --priority Spot --eviction-policy Delete --spot-max-price -1 \
  --enable-cluster-autoscaler --min-count 1 --max-count 3
```

`--spot-max-price -1`은 "가격 때문에는 축출하지 말라"는 뜻이다. 용량 부족으로 인한 축출은 여전히 일어난다. 배치 작업, CI 러너처럼 중단돼도 다시 돌릴 수 있는 일에 쓴다.

## 업그레이드 채널과 유지보수 시간대

업그레이드는 두 갈래다. **Kubernetes 버전 업그레이드**는 컨트롤 플레인과 노드의 버전을 올리고 노드 이미지도 함께 최신으로 바꾼다. **노드 이미지 업그레이드**는 Kubernetes 버전은 그대로 두고 OS 보안 패치만 반영한다.

각각 자동 채널을 고를 수 있다. 클러스터 채널은 `none`(기본형의 기본값), `patch`, `stable`, `rapid`가 있다. 노드 OS 채널은 `None`, `Unmanaged`, `SecurityPatch`, `NodeImage`이며 기본값은 `NodeImage`다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-cluster), [Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-node-os-image)).

자동 업그레이드를 켰다면 유지보수 시간대를 정해 둔다. 4시간 이상을 권장한다. 다만 실행은 최선 노력(best-effort)이고, 긴급 보안 조치는 시간대를 무시할 수 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/planned-maintenance)).

```bash
az aks update -g $RG -n $CLUSTER --auto-upgrade-channel stable --node-os-upgrade-channel NodeImage
az aks maintenanceconfiguration add -g $RG --cluster-name $CLUSTER \
  --name aksManagedAutoUpgradeSchedule --schedule-type Weekly --day-of-week Sunday \
  --interval-weeks 1 --duration 4 --utc-offset +09:00 --start-time 02:00
```

위 예시는 매주 일요일 한국 시간 새벽 2시부터 4시간 동안 클러스터 업그레이드를 허용한다. 노드 OS 업그레이드 시간대는 `aksManagedNodeOSUpgradeSchedule`이라는 이름으로 따로 만든다.

## 정리

- 운영 클러스터는 System 풀과 User 풀을 나누고, System 풀에 taint를 건다.
- 가용 영역은 노드풀을 만들 때만 정할 수 있다.
- Azure Linux 2.0 노드풀이 있다면 10월 31일 이미지 삭제 전에 옮긴다.
- 자동 업그레이드를 켜고 유지보수 시간대를 정한다. 1회에서 본 2027년 6월 강제 업그레이드를 피하는 가장 쉬운 방법이다.

다음 회에서는 pod가 어떤 IP를 받고 트래픽이 어떻게 들어오고 나가는지, AKS 네트워킹을 다룬다.

## 출처

- [Use system node pools in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-system-pools)
- [Reliability in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/reliability/reliability-aks)
- [AKS node images — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/node-images)
- [Node auto-provisioning — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/node-autoprovision)
- [Add a spot node pool to an AKS cluster — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/spot-node-pool)
- [Automatically upgrade an AKS cluster — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-cluster)
- [Autoupgrade node OS images — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-node-os-image)
- [Use planned maintenance to schedule upgrades — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/planned-maintenance)
- [az aks — Azure CLI reference](https://learn.microsoft.com/en-us/cli/azure/aks)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
