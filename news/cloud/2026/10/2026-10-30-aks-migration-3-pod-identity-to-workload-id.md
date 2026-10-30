---
title: pod 관리 ID에서 워크로드 ID로…지원 끝난 구성을 걷어내는 세 가지 경로
slug: 2026-10-30-aks-migration-3-pod-identity-to-workload-id
topic: cloud
published_at: 2026-10-30T01:02:00+09:00
tags:
  - AKS 실전 이전
  - AKS
  - Azure
  - Kubernetes
  - 워크로드 ID
  - Microsoft Entra
summary: AKS 실전 이전 가이드 5회 연재의 3회. AKS의 pod 관리 ID 애드온은 2025년 9월로 지원이 끝났다. 앱의 SDK 버전에 따라 병행 배포, 이전용 사이드카, 코드 수정 가운데 경로를 고르고, 페더레이션 자격 증명을 만들고, 기존 구성을 지우는 순서를 정리한다.
generated_by: claude
model: claude-opus-5-5
---

# pod 관리 ID에서 워크로드 ID로…지원 끝난 구성을 걷어내는 세 가지 경로

## 한눈에 보기

AKS의 pod 관리 ID(pod-managed identity)는 끝까지 preview였고, AKS 애드온은 2025년 9월까지만 패치와 지원을 받았다. 오픈소스 프로젝트 aad-pod-identity는 2022년 10월 deprecated, 2023년 9월 보관(archived)됐다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-azure-ad-pod-identity)). 지금 이 구성을 쓰고 있다면 지원 없이 돌고 있는 셈이다. 대체재인 Microsoft Entra 워크로드 ID는 GA이며 AKS Automatic에는 기본으로 켜져 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview)).

워크로드 ID의 원리는 [AKS 입문 4회](https://now.zeta4.net/a/2026-10-30-aks-104-identity-security)에서 다뤘다. 이번 회는 기존 pod 관리 ID에서 옮기는 절차에 집중한다.

## 경로 고르기: 앱의 SDK 버전이 기준

Microsoft의 [이전 가이드](https://learn.microsoft.com/en-us/azure/aks/workload-identity-migrate-from-pod-identity)는 세 경로를 제시한다.

| 경로 | 맞는 경우 |
|---|---|
| 병행 배포 | 앱이 이미 워크로드 ID를 지원하는 Azure Identity SDK 버전을 쓸 때. pod 관리 ID와 나란히 띄워 검증한 뒤 제거 |
| 이전용 사이드카 | 구버전 SDK라 당장 코드를 못 바꿀 때. 사이드카가 IMDS 요청을 받아 OIDC 토큰 교환으로 대신 처리. Linux 전용, 임시 방편 |
| 코드 수정 | 앱을 최신 Azure Identity로 바꾼 뒤 이전 |

워크로드 ID를 지원하는 최소 SDK 버전은 다음과 같다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview)).

| 언어 | 패키지 | 최소 버전 |
|---|---|---|
| .NET | Azure.Identity | 1.9.0 |
| Java | azure-identity | 1.9.0 |
| Python | azure-identity | 1.13.0 |
| Node.js | @azure/identity | 3.2.0 |
| Go | azidentity | 1.3.0 |
| C++ | azure-identity-cpp | 1.6.0 |

코드에서는 `DefaultAzureCredential`이나 `WorkloadIdentityCredential`을 쓴다. 사이드카는 장기 운영용이 아니라고 Microsoft가 명시했으니, 사이드카로 옮기더라도 SDK 업그레이드 일정을 함께 잡는다.

## 1단계: 클러스터에서 워크로드 ID 켜기

```bash
az aks update --resource-group "${RESOURCE_GROUP}" --name "${CLUSTER_NAME}" \
  --enable-oidc-issuer --enable-workload-identity

export AKS_OIDC_ISSUER="$(az aks show --name "${CLUSTER_NAME}" \
  --resource-group "${RESOURCE_GROUP}" --query "oidcIssuerProfile.issuerUrl" --output tsv)"
```

## 2단계: 기존 관리 ID에 페더레이션 자격 증명 만들기

pod 관리 ID에서 쓰던 사용자 할당 관리 ID를 그대로 재사용할 수 있다. Azure 쪽 역할 할당을 다시 만들 필요가 없다는 뜻이다. 그 ID에 "이 클러스터의 이 서비스 계정이 보낸 토큰을 믿는다"는 페더레이션 자격 증명을 추가한다.

```bash
export USER_ASSIGNED_CLIENT_ID="$(az identity show --resource-group $RESOURCE_GROUP \
  --name $MANAGED_IDENTITY_NAME --query 'clientId' -otsv)"

az identity federated-credential create --name $FEDERATED_IDENTITY_NAME \
  --identity-name $MANAGED_IDENTITY_NAME --resource-group $RESOURCE_GROUP \
  --issuer ${AKS_OIDC_ISSUER} \
  --subject system:serviceaccount:${SERVICE_ACCOUNT_NAMESPACE}:${SERVICE_ACCOUNT_NAME} \
  --audience api://AzureADTokenExchange
```

관리 ID 하나에 페더레이션 자격 증명은 최대 20개다. 반영에 수 초에서 수 분이 걸리므로, 만든 직후의 토큰 요청은 실패할 수 있다.

## 3단계: 서비스 계정과 pod 바꾸기

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: my-app
  annotations:
    azure.workload.identity/client-id: <USER_ASSIGNED_CLIENT_ID>
```

Deployment의 pod 템플릿에는 `serviceAccountName: my-app-sa`와 레이블 `azure.workload.identity/use: "true"`를 넣는다. 값은 문자열이어야 한다. 사이드카 경로라면 어노테이션 `azure.workload.identity/inject-proxy-sidecar: "true"`를 더한다.

자주 걸리는 함정은 다음과 같다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster)).

- 레이블을 빠뜨리면 pod가 재시작된 뒤 인증에 실패한다.
- 서비스 계정 어노테이션을 바꿨다면 pod를 재시작해야 반영된다.
- 토큰 범위는 `https://management.azure.com/.default`처럼 v2 형식으로 준다.
- 토큰 파일 경로를 코드에 박지 말고 `AZURE_FEDERATED_TOKEN_FILE` 환경 변수를 쓴다.
- virtual node에서는 워크로드 ID를 쓸 수 없다.

## 4단계: 검증 후 pod 관리 ID 제거

새 pod가 워크로드 ID로 Azure 자원에 접근하는지 확인했다면, 앱 매니페스트에서 `aadpodidbinding` 레이블을 지우고 pod 관리 ID를 정리한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/workload-identity-migrate-from-pod-identity)).

```bash
az aks pod-identity delete --name <pod-identity-name> --namespace <namespace> \
  --resource-group $RESOURCE_GROUP --cluster-name $CLUSTER_NAME
az aks update --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME --disable-pod-identity
kubectl get azureidentity -A
kubectl get azureidentitybinding -A
```

마지막 두 명령으로 AzureIdentity와 AzureIdentityBinding이 남지 않았는지 확인한다. 애드온이 아니라 Helm으로 직접 aad-pod-identity를 설치했다면, 제거 절차는 Microsoft 문서에 따로 나와 있지 않으니 설치할 때 쓴 방식으로 지운다.

KEDA를 쓰고 있다면 함께 점검한다. KEDA 2.15부터는 pod 관리 ID를 지원하지 않으므로 스케일러 인증도 워크로드 ID로 바꿔야 한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/keda-about)).

## 정리

- 앱별 Azure Identity SDK 버전부터 조사해 경로를 정한다.
- 기존 관리 ID에 페더레이션 자격 증명을 더하면 역할 할당은 그대로 쓸 수 있다.
- 서비스 계정 어노테이션과 pod 레이블, 둘 다 있어야 한다.
- 검증이 끝나면 pod 관리 ID와 `aadpodidbinding` 레이블을 지운다.

다음 회에서는 2027년 6월 1일 시작되는 플랫폼 강제 업그레이드에 대비하는 방법을 다룬다.

## 출처

- [Migrate from pod managed identity to workload identity — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/workload-identity-migrate-from-pod-identity)
- [Microsoft Entra Workload ID with AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview)
- [Deploy and configure workload identity on AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster)
- [Use Microsoft Entra pod-managed identities in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-azure-ad-pod-identity)
- [KEDA add-on for AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/keda-about)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
