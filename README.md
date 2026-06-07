# 🛡️ ML-Based Static API Malware Detection System (Pre-filter)
**Gachon University — AI Programming Team 05**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-3.3+-green.svg?style=flat-square)
![SMOTE](https://img.shields.io/badge/Imbalance-SMOTE_1:4-orange.svg?style=flat-square)
![XAI](https://img.shields.io/badge/XAI-SHAP-lightblue.svg?style=flat-square)

## 📖 Overview
This project introduces an ultra-lightweight **1st-line of defense (Pre-filter)** machine learning pipeline. It statically parses the **Import Address Table (IAT)** from the Portable Executable (PE) structure of Windows files (`.exe`) to pre-determine maliciousness without executing them.

It is designed to complement the evasion vulnerabilities of traditional signature-based detection and drastically reduce the resource bottlenecks and analysis delays introduced to dynamic analysis (Sandbox) systems through high-speed screening.

## 🔬 Core Methodology
* **Feature Selection:** Conducted 5-Fold grid experiments on the initial 1,000 API features, significantly reducing the dimensionality to the **Top 50 core APIs** where diminishing returns begin, thereby minimizing inference costs and preventing overfitting.
* **Imbalance Handling:** Applied **SMOTE 1:4 resampling** to overcome the extreme 1:23.7 imbalance between normal and malicious samples. This optimal threshold recovered the normal file recognition rate to 82.8% while minimizing integrity loss from synthetic data.
* **Model & Threshold:** Adopted **LightGBM**, which is highly optimized for real-time inference. To suppress False Positives for the pre-filter purpose, the classification threshold was **raised from 0.5 to 0.85**. This successfully maintained a high malware detection rate (95.1%) while cutting the False Positive Rate (FPR) nearly in half to 8.5%.
* **Explainable AI (SHAP):** SHAP analysis proved that the model learned a "Dual-Signal" approach. It detects not only the presence of malicious APIs but also identifies the **'complete absence of normal indicators'** (e.g., `_cexit`, a standard C runtime exit function) as the strongest malicious signal.

## 📂 Repository Structure
```text
📦 ai-based-static-api-malware-detection-system
 ┣ 📂 code/      # Data preprocessing, feature selection, model training, and evaluation
 ┣ 📂 data/      # Raw and processed datasets (Original 1:23 and SMOTE applied)
 ┣ 📂 model/     # Saved trained models (.pkl, .joblib)
 ┣ 📂 report/    # Progress reports, presentations, and visual analytics
 ┣ 📂 search/    # Research materials and cross-validation docs
 ┗ 📜 README.md  # Project overview
```

## 📊 Final Test Set Performance
The following metrics are based on a single evaluation of 9,516 external test data samples completely isolated during the training phase.

| Metrics | Value | Operational Impact |
| :--- | :---: | :--- |
| **Balanced Accuracy** | `0.9330` | Robust detection of both malware and normal files without imbalance distortion. |
| **Malware Recall** | `0.9515` | Strongly maintains the defense line against fatal malware misses. |
| **Normal Recall** | `0.9145` | Protects user experience by minimizing false positives (FP). |
| **False Positive Rate** | `0.0855` | **44% reduction in system FP burden** by applying the 0.85 threshold. |

🚨 **[Overcoming Static Analysis Blind Spots]**: For highly packed or obfuscated malicious samples (`njRAT`, `Remcos`) where 0 matching features are extracted, traditional AVs often misclassify them as normal. However, our model successfully blocked them with **94.92% probability** by leveraging the 'absence of normal indicators' pattern.

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/giyuubin/ai-based-static-api-malware-detection-system.git
cd ai-based-static-api-malware-detection-system
```

**2. Install dependencies**
```bash
pip install pandas scikit-learn lightgbm imbalanced-learn matplotlib seaborn shap
```

**3. Run the Code**
Navigate to the `code/` directory to run the Jupyter notebooks for data preparation, individual model training, and final evaluation.

---
*Reference: The foundational dataset for top-1000 PE imports was acquired via Kaggle (Angelo Oliveira).*
