---
title: AKS 앱 배포와 확장…ACR 연결부터 HPA·KEDA·VPA, GitOps, 스토리지와 GPU까지
slug: 2026-10-30-aks-105-deploy-and-scale
topic: cloud
published_at: 2026-10-30T00:34:00+09:00
tags:
  - AKS 입문
  - AKS
  - Azure
  - Kubernetes
  - 오토스케일링
  - GitOps
summary: AKS 입문 6회 연재의 5회. ACR에서 이미지를 받는 원리, HPA·KEDA·VPA를 언제 어떻게 섞어 쓰는지, Flux 기반 GitOps와 Automated Deployments, Azure Disk·Files CSI 스토리지, GPU 노드풀과 KAITO를 정리한다.
generated_by: claude
model: claude-opus-5-5
---

# AKS 앱 배포와 확장…ACR 연결부터 HPA·KEDA·VPA, GitOps, 스토리지와 GPU까지

## 한눈에 보기

클러스터가 준비됐으면 앱을 올릴 차례다. 이번 회는 이미지를 받아 오는 길, 부하에 맞춰 늘리고 줄이는 세 가지 오토스케일러, 배포를 자동화하는 GitOps, 상태를 저장하는 스토리지, AI 워크로드를 위한 GPU 노드를 차례로 본다. 핵심은 각 도구가 무엇을 조절하는지 구분하는 것이다. pod 수를 바꾸는 HPA·KEDA, pod 크기를 바꾸는 VPA, 노드 수를 바꾸는 클러스터 오토스케일러는 서로 겹치지 않게 써야 한다.

## 이미지 받기: ACR 연결

Azure Container Registry(ACR)에 올린 이미지를 AKS가 받으려면, [4회](https://now.zeta4.net/a/2026-10-30-aks-104-identity-security)에서 본 kubelet ID에 레지스트리의 `AcrPull` 역할이 있어야 한다. `--attach-acr`가 이 역할 할당을 대신 해 준다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/cluster-container-registry-integration)).

```bash
az aks update -g $RG -n $CLUSTER --attach-acr myacr
az aks check-acr -g $RG -n $CLUSTER --acr myacr.azurecr.io
```

역할 할당은 명령을 실행한 사람의 권한으로 이뤄지므로, 실행자에게 Owner처럼 역할을 할당할 수 있는 권한이 필요하다. 이미지 풀이 실패하면 `check-acr`로 원인을 먼저 본다. 레지스트리를 "RBAC Registry + ABAC Repository Permissions" 모드로 쓰면 `--attach-acr`가 지원되지 않으므로 Container Registry Repository Reader 역할을 직접 할당한다.

## 세 가지 오토스케일러

| 도구 | 무엇을 바꾸나 | 기준 | 켜는 법(기본형) |
|---|---|---|---|
| HPA | pod 개수 | CPU·메모리 사용률 | Kubernetes 기본 기능 |
| KEDA | pod 개수(0까지) | 큐 길이, 이벤트 등 외부 지표 | `--enable-keda` |
| VPA | pod의 CPU·메모리 요청 | 실제 사용 이력 | `--enable-vpa` |

AKS Automatic에는 셋 모두 기본으로 켜져 있다.

**KEDA**는 Azure Service Bus 큐 길이나 Kafka 지연처럼 CPU로는 드러나지 않는 부하에 맞춰 pod를 늘리고, 일이 없으면 0까지 줄인다. 주의할 점이 있다. 같은 워크로드에 HPA와 KEDA의 ScaledObject를 함께 걸면 안 된다. HPA가 먼저 있으면 ScaledObject 생성이 실패한다. 외부 메트릭 서버는 클러스터에 하나뿐이라 KEDA를 따로 또 설치할 수도 없다. KEDA 2.15부터는 pod 관리 ID를 지원하지 않으니 인증은 워크로드 ID로 한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/keda-about)).

**VPA**는 pod가 실제로 쓰는 CPU·메모리를 보고 요청값을 추천하거나 고친다. 모드는 `Off`(추천만), `Initial`(pod 생성 때만 적용), `Recreate`(pod를 다시 만들어 적용), `InPlaceOrRecreate`(AKS 1.34 이상, 가능하면 재시작 없이 적용)다. 예전 `Auto` 모드는 deprecated되어 `Recreate`처럼 동작한다. 같은 CPU·메모리 지표로 HPA와 함께 쓰는 것은 권장하지 않고, JVM 워크로드와 Windows는 지원하지 않는다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/vertical-pod-autoscaler)).

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Off"
```

처음에는 `Off`로 두고 추천값을 본 뒤 Deployment의 요청값에 반영하는 방식이 무난하다. pod가 늘어 노드가 모자라면 [2회](https://now.zeta4.net/a/2026-10-30-aks-102-cluster-and-node-pools)의 클러스터 오토스케일러나 노드 자동 프로비저닝이 노드를 추가한다.

## 배포 자동화: GitOps와 Automated Deployments

**GitOps(Flux)**는 Git 저장소의 매니페스트를 정답으로 두고 클러스터를 그 상태로 맞추는 방식이다. AKS에서는 `microsoft.flux` 클러스터 확장으로 제공되며 **AKS에서는 무료**다. 첫 Flux 구성을 만들면 확장이 자동 설치된다. 멀티테넌시가 기본으로 켜져 있어 다른 네임스페이스의 소스를 참조하는 구성은 막힌다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-arc/kubernetes/conceptual-gitops-flux2)).

구성은 `az k8s-configuration flux create` 명령이나 포털에서 만든다.

**Automated Deployments**는 포털에서 저장소를 고르면 Dockerfile과 Kubernetes 매니페스트(Deployment, Service, ConfigMap)를 만들고, GitHub Actions나 Azure DevOps 배포 파이프라인을 구성해 저장소에 PR로 올려 준다. 생성되는 매니페스트에는 배포 안전장치 권장 사항이 반영된다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/automated-deployments)). 첫 배포 틀을 잡을 때 쓰고, 이후에는 생성된 파일을 직접 관리하면 된다.

## 스토리지: CSI 드라이버

AKS는 Kubernetes 1.21부터 CSI 스토리지 드라이버를 기본으로 쓰고, 1.26부터는 예전 in-tree 드라이버로 볼륨을 만들 수 없다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/csi-storage-drivers)).

- **Azure Disk**(`disk.csi.azure.com`): 노드 하나가 읽고 쓰는 블록 스토리지(ReadWriteOnce). 데이터베이스처럼 한 pod가 쓰는 데이터에 맞다. 영역 중복(ZRS), Premium SSD v2, 스냅샷, 복제, 무중단 확장을 지원한다.
- **Azure Files**(`file.csi.azure.com`): 여러 노드가 함께 쓰는 SMB 공유. 업로드 파일처럼 여러 pod가 같이 읽는 데이터에 맞다.
- **Blob CSI**: `--enable-blob-driver`로 따로 켠다.

Azure Disk는 노드와 같은 가용 영역에 있어야 붙는다. 영역 분산 노드풀에서 pod가 다른 영역으로 옮겨 가면 디스크가 따라가지 못하는 문제가 생기니, 영역 장애에 대비해야 하면 ZRS 디스크를 고려한다. 로컬 NVMe나 Elastic SAN을 쓰는 Azure Container Storage v2도 있지만, v2는 Azure Disk를 지원하지 않는다는 점에 유의한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/storage/container-storage/container-storage-introduction)).

## GPU와 KAITO

GPU 노드풀을 추가하면 AKS는 기본으로 NVIDIA 드라이버를 자동 설치한다. 드라이버를 직접 관리하려면 `--gpu-driver none`을 쓴다(예전 `--skip-gpu-driver-install`은 은퇴했다). 드라이버, device plugin, DCGM 모니터링까지 AKS가 관리하는 GPU 노드풀은 아직 preview다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-nvidia-gpu), [Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/aks-managed-gpu-nodes)).

오픈 모델을 서빙하려면 **KAITO**(AI toolchain operator) 애드온을 볼 만하다. `--enable-ai-toolchain-operator --enable-oidc-issuer`로 켜고, 모델을 지정하면 GPU 노드를 준비하고 vLLM으로 OpenAI 호환 API를 띄운다. Ampere 이후 세대 NVIDIA GPU만 지원하며 T4와 V100은 쓸 수 없다. Windows와 AMD GPU도 지원하지 않는다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/ai-toolchain-operator)).

## 정리

- 이미지 풀 문제는 대부분 kubelet ID의 `AcrPull` 권한 문제다. `check-acr`부터 본다.
- 한 워크로드에는 HPA와 KEDA 중 하나만 건다. VPA는 `Off`로 추천값부터 본다.
- 배포는 GitOps로 Git을 정답으로 둔다.
- Azure Disk는 영역에 묶인다는 점을 기억한다.

마지막 회에서는 모니터링, 업그레이드, 비용, 백업 등 클러스터를 오래 운영하는 데 필요한 것들을 다룬다.

## 출처

- [Authenticate with ACR from AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/cluster-container-registry-integration)
- [KEDA add-on for AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/keda-about)
- [Vertical Pod Autoscaling in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/vertical-pod-autoscaler)
- [GitOps Flux v2 configurations with AKS and Azure Arc — Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-arc/kubernetes/conceptual-gitops-flux2)
- [Automated deployments for AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/automated-deployments)
- [CSI storage drivers on AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/csi-storage-drivers)
- [What is Azure Container Storage? — Microsoft Learn](https://learn.microsoft.com/en-us/azure/storage/container-storage/container-storage-introduction)
- [Use NVIDIA GPUs on AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-nvidia-gpu)
- [AKS-managed GPU nodes — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/aks-managed-gpu-nodes)
- [AI toolchain operator (KAITO) add-on — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/ai-toolchain-operator)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
