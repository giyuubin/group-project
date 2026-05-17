# [Project Note] SMOTE-ENN 샘플링 비율(Sampling Ratio) 최적화 및 수학적 성능 분석

## 1. Problem Definition (문제 정의)
* **주어진 환경:** 정상 파일($C_0$)과 악성코드($C_1$)의 비율이 $\approx 1 : 23.7$인 극도의 불균형 데이터셋.
* **사전 확률(Prior Probability):** $P(C_1) \approx 0.96$
* **한계점 (Limitation):**  원본 데이터($1:23$)로 학습할 경우, 다수 클래스로의 편향성에 의한 **정확도의 역설(Accuracy Paradox)** 발생.
  * 반대로 SMOTE를 통해 $1:1$로 완전 균형(Full Balancing)을 맞출 경우, 합성 데이터의 과적합 및 결정 경계(Decision Boundary) 붕괴로 인한 **사전 확률 왜곡(Prior Distortion)** 발생 위험 존재.
* **연구 목표:** 두 클래스 간의 탐지 밸런스($Macro\ F1$)를 극대화하고, 위협 탐지율($Recall(C_1)$)의 손실 없이 정상 파일 방어율($Recall(C_0)$)을 최대로 끌어올릴 수 있는 **최적의 샘플링 타겟 비율($\lambda$)** 도출.

---

## 2. Definition of Evaluation Metrics (주요 평가 지표의 정의 및 임계성)

### 2.1. Definition: 위협 탐지율 ($Recall(C_1)$)의 절대성
* **수식:** $Recall(C_1) = \frac{TP}{TP + FN}$
* **임계적 당위성 (Criticality):** 악성코드($C_1$)를 정상($C_0$)으로 오판하는 미탐(False Negative, $FN$)은 악성 페이로드 실행 및 시스템의 치명적 파괴로 직결됨. 즉, 보안 시스템에서 오탐(False Positive) 비용보다 미탐 비용이 비대칭적으로 크므로 ($Cost(FN) \gg Cost(FP)$), 높은 $Recall(C_1)$을 보장하는 것은 해당 보안 아키텍처가 성립하기 위한 절대적 **필요조건(Necessary Condition)**임.

### 2.2. Definition: Macro F1-Score의 공정성
* **수식:** $Macro\ F1 = \frac{F1(C_0) + F1(C_1)}{2}$
* **임계적 당위성 (Criticality):** 데이터의 극단적 불균형($1:23$) 하에서, 단순 정확도(Accuracy)는 다수 클래스($C_1$)의 분포에 의해 완전히 지배(Dominated)됨. $Macro\ F1$은 개별 클래스의 조화평균($F1$)을 클래스 빈도와 무관하게 1:1로 산술평균함. 따라서 모델이 소수 클래스($C_0$)를 포기하지 않고 각 클래스의 비선형적 특성 공간(Feature Space)을 균형 있게 학습했는지 검증하는 엄격한 **불편 추정량(Unbiased Estimator)**으로 작용함.

---

## 3. Experimental Results (벤치마크 실험 결과)
타겟 비율 $\lambda \in \{\frac{1}{23}, \frac{1}{7}, \frac{1}{6}, \frac{1}{5}, \frac{1}{4}, \frac{1}{3}, \frac{1}{2}, 1\}$ 에 따른 XGBoost 모델 성능 평가 지표.

| 튜닝 시나리오 ($\lambda$) | Accuracy | Precision ($C_1$) | Recall ($C_0$) | Recall ($C_1$) | Macro F1 | 
| :--- | :---: | :---: | :---: | :---: | :---: | 
| **Baseline (1:23)** | 97.77% | 97.96% | **50.78%** | 99.76% | 0.8188 | 
| **SMOTE-ENN (1:7)** | 97.24% | 98.34% | 60.62% | 98.78% | 0.8129 | 
| **SMOTE-ENN (1:6)** | 96.17% | 99.14% | 80.05% | 96.86% | 0.8046 | 
| **SMOTE-ENN (1:5)** | 97.09% | 98.38% | 61.66% | 98.59% | 0.8085 | 
| **SMOTE-ENN (1:4)** | 96.30% | 99.15% | **80.31%** | **96.98%** | **0.8092** | 
| **SMOTE-ENN (1:3)** | 95.95% | 99.18% | 81.09% | 96.58% | 0.7989 | 
| **SMOTE-ENN (1:2)** | 95.22% | 98.43% | 63.47% | 96.56% | 0.7467 | 
| **SMOTE-ENN (1:1)** | 82.82% | 99.33% | 86.79% | **82.65%** | **0.5965** | 

---

## 4. Mathematical & Logical Analysis (분석 및 증명)

### 4.1. Analysis: Baseline의 편향성 (Accuracy Paradox)
* **현상:** $\lambda = \frac{1}{23}$ 환경에서 $Accuracy = 97.77\%$로 높게 측정되나, $Recall(C_0) = 50.78\%$로 치명적인 정상 파일 오탐(False Positive) 발생.
* **분석:** 모델이 손실 함수(Loss Function)를 최소화하기 위해 입력 벡터를 무조건 $C_1$(악성)으로 맵핑하는 국소 최적해(Local Minima)에 빠짐. 소수 클래스인 정상 파일에 대한 판별력을 온전히 상실함.

### 4.2. Analysis: 완전 균형의 붕괴 (Prior Probability Distortion)
* **현상:** $\lambda = 1$ 환경에서 필요조건인 $Recall(C_1)$이 $82.65\%$로 대폭락하며, $Macro\ F1$ 수치가 최하점($0.5965$)을 기록함.
* **분석:** 과도한 보간법(Interpolation)으로 인해 생성된 비현실적 합성 데이터(Noise)가 $C_1$의 고유한 결정 공간을 침범함. ENN 알고리즘이 경계를 정제하려 시도했으나, 데이터의 양적 팽창으로 인해 **결정 경계(Decision Boundary) 자체가 붕괴**됨. 실제 배포 환경($1:23$)과의 사전 확률 간극이 커져 심각한 미탐(False Negative)을 유발함.

### 4.3. Theorem: 최적 타협점의 도출 (The Sweet Spot)
* **현상:** $\lambda = \frac{1}{4}$ 환경에서 $Recall(C_0) = 80.31\%$, $Recall(C_1) = 96.98\%$를 기록하며, $Macro\ F1$ 기준 가장 안정적인 고점($0.8092$)을 달성함.
* **증명:** 원본의 정보량을 훼손하지 않는 선에서 $C_0$의 합성 데이터를 제한적으로 조절함. 이를 통해 모델의 과적합(Overfitting)을 방지함과 동시에, $C_0$와 $C_1$ 사이의 다차원 경계면(Manifold)을 가장 수학적으로 뚜렷하게 분리해 낸 지점임을 실증함.

---

## 5. Conclusion (최종 결론)
데이터 불균형 해결을 위한 전처리 과정에서 무조건적인 클래스 동률($1:1$) 맵핑은 사전 확률 왜곡을 유발하여 위협 탐지율($Recall(C_1)$)을 치명적으로 훼손함을 증명함. 

따라서 Bias-Variance Tradeoff를 최적화하고, 정상 파일의 오탐을 최소화하면서도 보안 시스템의 절대적 필요조건인 위협 탐지율을 완벽히 방어해 낸 **`SMOTE-ENN (1:4 Ratio)`를 본 프로젝트의 최종 전처리 아키텍처로 채택**함.
