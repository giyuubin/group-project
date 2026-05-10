# 🛡️ AI-Based Static API Malware Detection System
**Gachon University - AI Programming Team 05**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-0.24+-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.2+-green.svg)

## 📖 Overview
This project introduces a **Static Analysis Architecture** that detects malware by analyzing API call patterns from Portable Executable (PE) files. It efficiently overcomes the vulnerabilities of traditional signature-based detection and the heavy resource costs of dynamic analysis.

## 🔬 Core Methodology
* **Feature Selection:** Reduced 1,000 raw APIs to the **Top 30 core APIs** using Random Forest's Gini Impurity to prevent the 'curse of dimensionality'.
* **Imbalance Handling:** Shifted the primary evaluation metric from Accuracy to **Recall** to effectively counter the extreme 1:23 (Normal:Malware) data imbalance and avoid the 'accuracy paradox'.
* **Final Model (Random Forest):** Selected for its ability to capture complex non-linear API interactions, resist overfitting via Bagging, and provide built-in OOB (Out-of-Bag) validation.

## 📂 Repository Structure
```text
📦 group-project
 ┣ 📂 code/     # Data splitting, model training, and benchmark notebooks
 ┣ 📂 data/     # Train (SMOTE 1:1) and Test (Original 1:23) datasets
 ┣ 📂 model/    # Saved trained models (.joblib)
 ┣ 📂 report/   # Progress reports and presentations
 ┣ 📂 search/   # Research materials and cross-validation docs
 ┗ 📜 README.md # Project overview
```

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone [https://github.com/giyuubin/group-project.git](https://github.com/giyuubin/group-project.git)
   cd group-project
   ```

2. **Install dependencies**
   ```bash
   pip install pandas scikit-learn imbalanced-learn matplotlib seaborn
   ```

3. **Run the Code**
   * Navigate to the `code/` directory to run data preparation (`Data_Split_and_SMOTE.ipynb`), individual model training (`LR_Model_Training.ipynb`), and final evaluation (`model_benchmark.ipynb`).

---
*Reference: The theoretical basis for our Random Forest Bagging and OOB validation approach is derived from Breiman, L. (2001). Random forests. Machine learning, 45(1), 5-32.*
