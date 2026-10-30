---
title: Secret의 base64는 암호화가 아니다…ConfigMap·Secret과 Pod이 사라져도 남는 볼륨
slug: 2026-10-30-k8s-hands-on-5-config-storage
topic: cloud
published_at: 2026-10-30T10:54:00+09:00
tags:
  - 쿠버네티스 손으로 익히기
  - Kubernetes
  - 스토리지
summary: 「쿠버네티스 손으로 익히기」 5회. 이미지와 설정을 분리하는 ConfigMap, 기본 상태로는 암호화되지 않는 Secret을 안전하게 다루는 법, PersistentVolume·PersistentVolumeClaim·StorageClass로 Pod보다 오래 사는 데이터를 만드는 법을 kind 클러스터에서 실습한다.
generated_by: claude
model: claude-opus-5-5
---

# Secret의 base64는 암호화가 아니다…ConfigMap·Secret과 Pod이 사라져도 남는 볼륨

## 한눈에 보기

같은 이미지를 개발·스테이징·운영에 그대로 올리려면 환경마다 달라지는 설정을 이미지 밖에 두어야 한다. 쿠버네티스에서는 일반 설정을 ConfigMap에, 비밀번호와 토큰을 Secret에 둔다. 그런데 Secret은 이름과 달리 기본 상태로는 암호화되지 않는다. 또 컨테이너 안의 파일은 Pod이 사라지면 함께 사라지므로, 남아야 하는 데이터는 볼륨으로 따로 관리한다. 이번 회는 설정, 비밀값, 데이터 세 가지를 Pod 밖으로 꺼내는 법을 다룬다.

연재 순서: [1회 선언형과 조정 루프](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-1-declarative-reconcile), [2회 클러스터 해부도](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-2-cluster-anatomy), [3회 워크로드 고르기](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-3-workloads), [4회 네트워킹](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-4-networking), 5회 설정과 저장소, [6회 운영과 디버깅](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-6-operations-debugging), [7회 보안과 배포 파이프라인](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-7-security-delivery).

## ConfigMap: 설정을 이미지 밖으로

ConfigMap은 키-값 형태의 설정을 담는 객체다. Pod에 넣는 방법은 두 가지다([Kubernetes 문서](https://kubernetes.io/docs/concepts/configuration/configmap/)).

- **환경 변수로**: 앱이 `LOG_LEVEL` 같은 환경 변수를 읽는 경우. 컨테이너가 시작할 때 한 번 읽히므로, ConfigMap을 바꿔도 Pod을 다시 띄우기 전에는 반영되지 않는다.
- **파일(볼륨)로**: 앱이 설정 파일을 읽는 경우. ConfigMap을 바꾸면 마운트된 파일이 시간 차를 두고 갱신된다. 다만 앱이 파일을 다시 읽어야 효과가 있고, `subPath`로 마운트한 파일은 갱신되지 않는다.

```bash
kubectl create configmap web-config --from-literal=LOG_LEVEL=info --from-literal=FEATURE_X=on
kubectl get configmap web-config -o yaml
```

설정을 바꾼 뒤 Pod을 다시 띄우고 싶으면 `kubectl rollout restart deployment/web`을 쓴다. 3회의 롤링 업데이트 규칙대로 하나씩 교체된다.

## Secret: 이름만 비밀이다

Secret은 ConfigMap과 거의 같은 방식으로 쓰지만, 비밀값을 위한 객체다. 매니페스트에서 값이 base64로 적혀 있어 암호화된 것처럼 보이지만, base64는 인코딩일 뿐이다.

```bash
kubectl create secret generic db-cred --from-literal=password='s3cr3t-for-lab'
kubectl get secret db-cred -o jsonpath='{.data.password}' | base64 -d; echo
```

Secret을 읽을 권한만 있으면 누구나 원문을 볼 수 있다. 공식 문서도 Secret은 기본적으로 API 서버의 저장소(etcd)에 암호화되지 않은 채 저장되며, API 접근 권한이 있는 사람이나 etcd에 접근할 수 있는 사람은 값을 읽거나 바꿀 수 있다고 경고한다. 그리고 네임스페이스에 Pod을 만들 수 있는 사람은 그 네임스페이스의 Secret을 간접적으로 읽을 수 있다고 덧붙인다([Kubernetes 문서](https://kubernetes.io/docs/concepts/configuration/secret/)).

공식 문서가 권하는 최소한의 조치는 다음과 같다.

- etcd 저장 시 암호화(encryption at rest)를 켠다. 관리형 쿠버네티스는 대개 기본으로 켜져 있거나 옵션으로 제공한다.
- RBAC로 Secret을 읽고 쓸 수 있는 사람과 서비스 계정을 최소한으로 줄인다(7회).
- 클라우드의 비밀 관리 서비스(Azure Key Vault, AWS Secrets Manager 등)를 외부 저장소로 연결하는 방법을 검토한다.
- Secret 매니페스트를 Git에 그대로 커밋하지 않는다. base64는 누구나 풀 수 있다.

## 볼륨: 컨테이너가 바뀌어도 남는 데이터

컨테이너의 파일 시스템은 컨테이너가 다시 시작되면 초기화된다. Pod 안에서만 공유하면 되는 임시 공간은 `emptyDir` 볼륨을 쓰고, Pod이 사라져도 남아야 하는 데이터는 영구 볼륨을 쓴다. 영구 볼륨은 세 객체가 나눠 맡는다([Kubernetes 문서](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)).

| 객체 | 비유 | 누가 만드나 |
|---|---|---|
| StorageClass | 디스크 상품 목록(SSD, HDD, 성능 등급) | 클러스터 운영자 |
| PersistentVolumeClaim(PVC) | "10GiB SSD 하나 주세요"라는 신청서 | 앱 개발자 |
| PersistentVolume(PV) | 실제로 할당된 디스크 | 대개 StorageClass가 자동으로(동적 프로비저닝) |

PVC의 접근 모드도 알아 둔다. `ReadWriteOnce`는 한 노드에서만 읽고 쓰고, `ReadWriteMany`는 여러 노드에서 동시에 읽고 쓴다. 클라우드 블록 디스크는 대부분 `ReadWriteOnce`만 지원하므로, 여러 Pod이 같은 파일을 써야 한다면 파일 스토리지 계열을 골라야 한다. 동적으로 만든 볼륨의 회수 정책은 보통 `Delete`여서 PVC를 지우면 디스크도 지워진다. 지우면 안 되는 데이터라면 회수 정책을 `Retain`으로 두거나 따로 백업한다.

## 실습: Pod을 지워도 남는 파일

kind에는 기본 StorageClass가 들어 있다. 먼저 확인한다.

```bash
kubectl get storageclass
```

`(default)` 표시가 붙은 StorageClass가 보이면, PVC와 그것을 쓰는 Pod을 만든다. 아래를 `data.yaml`로 저장한다.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: notes
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: writer
spec:
  containers:
    - name: app
      image: busybox:1.37
      command: ["sh", "-c", "date >> /data/log.txt; cat /data/log.txt; sleep 3600"]
      env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-cred
              key: password
      envFrom:
        - configMapRef:
            name: web-config
      volumeMounts:
        - name: notes
          mountPath: /data
  volumes:
    - name: notes
      persistentVolumeClaim:
        claimName: notes
```

```bash
kubectl apply -f data.yaml
kubectl get pvc notes
kubectl logs writer
kubectl exec writer -- sh -c 'echo $LOG_LEVEL $FEATURE_X'
```

PVC가 `Bound`가 되고, 로그에 시각이 한 줄 찍힌다. 환경 변수에는 ConfigMap 값이 들어 있다. 이제 Pod만 지우고 다시 만든다.

```bash
kubectl delete pod writer
kubectl apply -f data.yaml
kubectl logs writer
```

로그에 시각이 두 줄 나온다. Pod은 새로 만들어졌지만 PVC에 묶인 볼륨은 그대로 남아 있었기 때문이다. 실습이 끝나면 `kubectl delete -f data.yaml`로 PVC까지 지운다. 이때 회수 정책이 `Delete`이므로 데이터도 함께 사라진다.

StatefulSet은 이 과정을 자동화한다. `volumeClaimTemplates`를 쓰면 `db-0`, `db-1`마다 PVC를 따로 만들고, Pod이 다시 만들어져도 같은 번호의 PVC에 다시 붙인다([Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)).

## 정리

- 환경마다 바뀌는 값은 ConfigMap으로 이미지 밖에 둔다. 환경 변수로 넣었다면 바꾼 뒤 `rollout restart`가 필요하다.
- Secret은 기본으로 암호화되지 않는다. 저장 시 암호화, RBAC, 외부 비밀 저장소를 함께 쓴다.
- 남아야 하는 데이터는 PVC로 신청한다. 회수 정책이 `Delete`인지 먼저 확인한다.

다음 회에서는 지금까지 만든 앱이 실제 운영에서 버티도록 자원 요청량과 헬스 체크를 걸고, 일부러 고장 낸 클러스터를 고친다.

## 출처

- [ConfigMaps — Kubernetes 문서](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Secrets — Kubernetes 문서](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Good practices for Kubernetes Secrets — Kubernetes 문서](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)
- [Encrypting Confidential Data at Rest — Kubernetes 문서](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
- [Persistent Volumes — Kubernetes 문서](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Storage Classes — Kubernetes 문서](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- [StatefulSets — Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
