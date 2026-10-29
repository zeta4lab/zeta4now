---
title: AKS 운영과 비용…로그 비용 조절, 무중단 업그레이드, 비용 분석, 백업까지
slug: 2026-10-30-aks-106-operations-and-cost
topic: cloud
published_at: 2026-10-30T00:35:00+09:00
tags:
  - AKS 입문
  - AKS
  - Azure
  - Kubernetes
  - 모니터링
  - 클라우드 비용
summary: AKS 입문 6회 연재의 마지막 회. Managed Prometheus와 Container Insights의 로그 비용 조절, maxSurge·드레인 시간으로 무중단 업그레이드 하기, 2027년 6월부터의 강제 업그레이드 대비, 비용 분석 애드온·Spot·클러스터 정지, Azure Backup으로 워크로드 백업하기를 정리한다.
generated_by: claude
model: claude-opus-5-5
---

# AKS 운영과 비용…로그 비용 조절, 무중단 업그레이드, 비용 분석, 백업까지

## 한눈에 보기

클러스터는 만든 날보다 운영하는 날이 훨씬 길다. 마지막 회는 오래 운영할 때 반복해서 부딪히는 네 가지를 다룬다. 무엇을 얼마나 관측할지(그리고 그 로그 비용), 업그레이드를 어떻게 무중단으로 할지, 돈이 어디로 새는지, 사고가 났을 때 무엇으로 되돌릴지다.

## 모니터링: 지표는 Prometheus, 로그는 비용부터

AKS 모니터링은 두 갈래다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/containers/kubernetes-monitoring-enable)).

- **Azure Monitor managed Prometheus**: 노드·pod·컨테이너 지표를 수집한다. `--enable-azure-monitor-metrics`로 켜고, 컨트롤 플레인 지표(API server, etcd 등)는 `--enable-control-plane-metrics`를 더한다.
- **Container Insights**: 컨테이너 로그와 Kubernetes 이벤트를 Log Analytics로 보낸다.

로그는 비용이 빠르게 불어나는 곳이다. Container Insights는 수집 범위를 프리셋으로 고를 수 있다.

| 프리셋 | 수집 주기 | 수집 대상 |
|---|---|---|
| Logs and Events(기본) | 1분 | 컨테이너 로그, Kubernetes 이벤트, pod 목록 |
| Standard | 1분 | 표준 테이블 전체 |
| Syslog | 1분 | 표준 테이블 전체 + 노드 Syslog |
| Cost-optimized | 5분 | kube-system 등 시스템 네임스페이스 제외 |

수집 주기는 1~30분 사이에서 조정할 수 있고 네임스페이스별로 거를 수 있다. 개발 클러스터는 Cost-optimized로 시작하고, 꼭 필요한 네임스페이스만 자세히 보는 것이 비용을 아끼는 첫걸음이다. 대시보드는 Azure 포털 안에서 바로 열리는 "Dashboards with Grafana"의 AKS 템플릿으로 시작할 수 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/visualize-use-grafana-dashboards)).

## 업그레이드: 노드를 하나씩 바꾸는 원리

AKS의 노드 업그레이드는 새 노드를 먼저 추가하고(surge), 기존 노드의 pod를 내보낸 뒤(drain), 기존 노드를 지우는 과정을 반복한다. 이 속도와 안전성을 몇 가지 값으로 조절한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-node-pools-rolling)).

| 설정 | 기본값 | 의미 |
|---|---|---|
| `maxSurge` | 1 | 한 번에 더 만드는 노드 수. 운영 환경 권장 33% |
| `maxUnavailable` | 0 | 한 번에 비워도 되는 노드 수. 시스템 풀에는 설정 불가 |
| `drain-timeout` | 30분 | pod 내보내기를 기다리는 최대 시간(5분~24시간) |
| `node-soak-duration` | 0 | 노드 하나를 바꾼 뒤 다음 노드로 가기 전 대기 시간(0~30분) |

```bash
az aks nodepool update -g $RG --cluster-name $CLUSTER -n np1 --max-surge 33% --drain-timeout 45
```

무중단 업그레이드의 진짜 열쇠는 앱 쪽에 있다. 레플리카가 2개 이상이고, PodDisruptionBudget으로 동시에 내려가도 되는 pod 수를 정해 두고, readiness probe가 제대로 동작해야 노드가 바뀌는 동안 트래픽이 끊기지 않는다. PDB가 너무 엄격하면 drain이 진행되지 못해 `drain-timeout`에 걸린다는 점도 기억한다.

블루-그린 방식의 노드풀 업그레이드(`--upgrade-strategy bluegreen`)도 있지만 아직 preview이고, 업그레이드하는 동안 용량이 두 배 필요하다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/blue-green-node-pool-upgrade)).

## 지원 종료 버전에 머물면 생기는 일

[1회](https://now.zeta4.net/a/2026-10-30-aks-101-what-aks-manages)에서 짚었듯 **2027년 6월 1일부터 AKS는 지원 종료 후 60일이 지난 클러스터를 플랫폼이 강제로 업그레이드한다.** 이 업그레이드는 유지보수 시간대를 따르지 않고, deprecated API가 있어도 멈추지 않으며, PDB를 무시할 수 있다. 지원이 끝난 버전의 클러스터는 Resource Health에 Degraded로 표시된다. 당장 다음 차례는 1.34로, 2026년 11월에 지원이 끝난다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions)).

대비책은 [2회](https://now.zeta4.net/a/2026-10-30-aks-102-cluster-and-node-pools)의 자동 업그레이드 채널과 유지보수 시간대다. 한 버전에 오래 머물러야 하는 사정이 있다면 Premium 티어의 장기 지원(LTS)을 쓴다. 업그레이드 전에는 Azure Advisor가 알려 주는 deprecated API 사용 여부를 확인한다.

## 비용: 어디에 쓰는지부터 본다

**비용 분석 애드온**(`--enable-cost-analysis`)은 OpenCost 기반으로 Azure 비용 관리 화면에서 네임스페이스·워크로드 단위 비용을 보여 준다. Standard 이상 티어가 필요하고, EA·MCA 계약에서만 볼 수 있으며, Azure Disk CSI 드라이버가 켜져 있어야 한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/cost-analysis)).

```bash
az aks update -g $RG -n $CLUSTER --enable-azure-monitor-metrics --enable-cost-analysis
```

비용을 줄이는 대표적인 방법은 다음과 같다.

- **요청값 바로잡기**: [5회](https://now.zeta4.net/a/2026-10-30-aks-105-deploy-and-scale)의 VPA 추천값으로 과하게 잡힌 CPU·메모리 요청을 줄이면 같은 노드에 더 많은 pod가 들어간다.
- **Spot 노드풀**: 중단돼도 되는 작업을 할인된 Spot 노드로 보낸다.
- **클러스터 정지**: 개발 클러스터는 `az aks stop`으로 밤과 주말에 멈춘다. 상태는 최대 12개월 보존되지만, 컨트롤러 없이 단독으로 만든 pod는 지워지고 API server IP가 바뀔 수 있다. 노드 자동 프로비저닝을 쓰는 클러스터는 정지할 수 없고, 다시 시작할 때 용량이 부족하면 실패할 수 있어 중요한 클러스터에는 권장하지 않는다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/start-stop-cluster)).
- **로그 수집 범위 줄이기**: 앞서 본 Container Insights 프리셋을 조정한다.

## 백업: etcd 백업은 내 것이 아니다

1회에서 본 것처럼 Microsoft의 etcd 백업은 사용자가 복원할 수 없다. 워크로드와 데이터를 되돌리려면 **Azure Backup for AKS**를 쓴다. 클러스터에 백업 확장을 설치하고 신뢰할 수 있는 액세스(Trusted Access)를 켜며, 백업 자격 증명 모음은 클러스터와 같은 리전·구독에 둔다. Azure Disk와 Azure Files(SMB) 볼륨을 지원한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-backup-overview)).

| 저장 위치 | 특징 |
|---|---|
| Operational tier | 내 테넌트 안의 스냅샷, 최소 4시간 간격 |
| Vault tier | 하루 1개 복구 지점, 다른 리전 복원 지원, Azure Disk 전용 |

요금은 보호하는 네임스페이스 수에 따른 요금과 스냅샷 저장 요금으로 이뤄진다. 백업은 복원해 보기 전까지는 백업이 아니다. 분기에 한 번은 다른 네임스페이스로 복원 연습을 해 두자.

## 연재를 마치며: AKS 운영 점검표

- 운영 클러스터는 Standard 이상 티어, 가용 영역 분산 (1·2회)
- System 풀 분리, Azure Linux 2.0 등 은퇴 OS 없음 (2회)
- 자동 업그레이드 채널과 유지보수 시간대 설정 (2회)
- Azure CNI Overlay, 네트워크 정책 적용, 관리형 NGINX 이전 계획 (3회)
- Entra ID + Azure RBAC, 로컬 계정 끔, 워크로드 ID, Key Vault (4회)
- 레플리카 2개 이상, PDB, readiness probe, 적절한 요청값 (5·6회)
- 로그 수집 범위 조정, 비용 분석 켬 (6회)
- 워크로드 백업과 복원 연습 (6회)

이 점검표의 상당 부분은 AKS Automatic에서 기본으로 채워진다. 처음 시작한다면 Automatic으로 시작해 기본값을 이해하고, 꼭 필요한 곳만 바꾸는 것이 가장 빠른 길이다.

## 출처

- [Enable monitoring for AKS clusters — Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/containers/kubernetes-monitoring-enable)
- [Use Grafana dashboards in Azure Monitor — Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/visualize-use-grafana-dashboards)
- [Upgrade AKS node pools with rolling upgrades — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-node-pools-rolling)
- [Blue-green node pool upgrade — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/blue-green-node-pool-upgrade)
- [Supported Kubernetes versions in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions)
- [AKS cost analysis — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/cost-analysis)
- [Stop and start an AKS cluster — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/start-stop-cluster)
- [Azure Kubernetes Service backup overview — Microsoft Learn](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-backup-overview)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
