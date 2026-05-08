# 🛡️ AI-Based Static API Malware Detection System
**Gachon University - AI Programming Team 05**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-0.24+-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.2+-green.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626.svg)

## 📖 Project Overview
This project introduces a **Static Analysis Architecture** that detects malware by analyzing API call patterns extracted from the Import Address Table (IAT) of Portable Executable (PE) files. 

By analyzing the "behavioral intent" of combinations of APIs without actually executing the files, this system overcomes the limitations of traditional signature-based detection (vulnerable to zero-day attacks) and dynamic analysis (susceptible to sandbox evasion and heavy resource consumption).

## 🔬 Core Methodology

### 1. Feature Selection (Dimensionality Reduction)
* **Challenge:** Processing 1,000 raw API features causes computational bottlenecks and overfitting (the Curse of Dimensionality).
* **Solution:** Utilized the **Gini Impurity** metric from a preliminary Random Forest model to identify the **Top 30 core APIs** at the elbow point of the information gain curve, maximizing efficiency without losing critical behavioral patterns.

### 2. Overcoming Extreme Data Imbalance (1:23 Ratio)
* **Challenge:** The test dataset has a severe imbalance of Normal (1) to Malware (23). In this environment, relying on 'Accuracy' creates a paradox where a model can simply guess 'Malware' for everything and score 96%.
* **Solution:** Shifted the primary evaluation metric to **Recall**, focusing on minimizing False Negatives (missing actual malware) while maintaining a stable defense against noise.

### 3. Model Selection: Random Forest
After extensive cross-validation against Logistic Regression, SVM, XGBoost, and DNNs, **Random Forest** was selected as the final architecture due to:
* **Non-linear Interaction:** Effectively captures complex, conditional combinations of the 30 core APIs.
* **Overfitting Resistance:** Uses **Bagging (Bootstrap Aggregating)** to maintain high Recall even with noisy, imbalanced data.
* **Explainability:** Provides clear **Feature Importance** metrics to security analysts.
* **OOB Validation:** Leverages Out-of-Bag samples for robust internal validation without wasting training data.

## 📂 Repository Structure

```text
📦 group-project
 ┣ 📂 code/     # Source code including feature selection, model training, and benchmark tests
 ┣ 📂 report/   # Weekly progress reports, presentation materials, and project documentation
 ┣ 📂 search/   # Research materials, academic references, and cross-validation analysis docs
 ┗ 📜 README.md # Project overview and guide
```

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone [https://github.com/giyuubin/group-project.git](https://github.com/giyuubin/group-project.git)
   cd group-project
   ```

2. **Install dependencies**
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn xgboost pefile
   ```

3. **Run the Code**
   * Navigate to the `code/` directory to run the Jupyter notebooks for feature extraction and model benchmarking.

---
*Reference: The theoretical basis for our Random Forest Bagging and OOB validation approach is derived from Breiman, L. (2001). Random forests. Machine learning, 45(1), 5-32.*
