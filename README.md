# 🛡️ ML-Based Static API Malware Detection System (Pre-filter)
**Gachon University — AI Programming Team 05**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-3.3+-green.svg?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-Web_Demo-black.svg?style=flat-square)

[📄 Detailed Technical Report (Notion)](https://app.notion.com/p/36de8de0e4a380a0b9d9e985358df481?assetsVersion=23.13.20260609.0651#36de8de0e4a380fcbb6ff752cead1b66)

This project introduces an ultra-lightweight **1st-line of defense (Pre-filter)** machine learning pipeline. It statically parses the **Import Address Table (IAT)** from the Portable Executable (PE) structure of Windows files (`.exe`) to pre-determine maliciousness in milliseconds, without executing them. 

It is designed to complement the evasion vulnerabilities of traditional signature-based detection and drastically reduce the resource bottlenecks introduced to dynamic analysis (Sandbox) systems.

<br>

## 🚀 Quick Start (Demo Evaluation)
For a seamless evaluation, we provide a fully functional Web Scanner and a Batch Testing script using our final trained model.

### 1. Environment Setup
Clone the repository and navigate to the `demo/` directory to install dependencies.
```bash
git clone https://github.com/giyuubin/ml-based-static-api-malware-detection-system.git
cd ml-based-static-api-malware-detection-system/demo
pip install -r requirements.txt
```
*(Note: If you encounter module errors or if `pip`/`python` commands are not recognized in Windows, please consistently use the `py` launcher for all commands. e.g., `py -m pip install -r requirements.txt` and `py app.py`)*

### 2. Run Real-time Web Scanner (UI)
```bash
python app.py
```
* Open your web browser and navigate to `http://127.0.0.1:5000`.
* Upload any `.exe` file. The system will instantly parse the PE IAT and display the maliciousness probability.

### 3. Run Batch Prediction (Packed Malware Defense)
This script demonstrates our model's capability to detect highly packed or obfuscated malware (e.g., `njRAT`, `Remcos`) where 0 API features are extracted.

* **Preparation:** Place the `.exe` files you want to test inside the `sample/` directory (e.g., `sample/malware/test.exe`).
* **Execution:**
```bash
python batch_predict.py
```
* The console will output the prediction logs, showing how the model successfully blocks them with a **94.92% probability** by leveraging the "absence of normal indicators". The results are also saved in `batch_results.csv`.

<br>

## 📊 Final Test Set Performance
Based on a completely isolated test dataset.

| Metrics | Score | Operational Impact |
| :--- | :---: | :--- |
| **Balanced Accuracy** | `0.93` | Robust detection of both malware and normal files. |
| **Malware Recall** | `0.95` | Strongly maintains the defense line against fatal misses. |
| **Normal Recall** | `0.91` | Protects user experience by minimizing false positives. |
| **False Positive Rate** | `8.6%` | Drastically reduces system FP burden. |

<br>

## 🔬 Core Achievements & Methodology
Our deployed model (`lightgbm_final.pkl`) was built using a dataset of **47,580 PE samples** (1,929 Normal / 45,651 Malware) through the following optimizations:

* **Feature Optimization:** Reduced the initial 1,000 APIs to the **Top 50 core APIs** where diminishing returns begin, maximizing inference speed and preventing overfitting.
* **Imbalance Handling:** Applied **SMOTE 1:4 resampling** to overcome the extreme 1:23.7 data imbalance, recovering the normal file recognition rate to 82.8%.
* **False Positive Control:** Raised the classification threshold from 0.5 to **0.85**. This successfully maintained a high malware detection rate (95.1%) while cutting the False Positive Rate (FPR) nearly in half to 8.5%.
* **Explainable AI (SHAP):** Proven that the model learns a "Dual-Signal" approach. It detects not only the presence of malicious APIs but also identifies the critical **absence of normal indicators** (e.g., `_cexit`, a standard C runtime exit function) to bypass structural blind spots.

<br>

## 📂 Repository Structure
This repository contains both the final demonstration application and the complete research pipeline.

```text
📦 ml-based-static-api-malware-detection-system
 ┣ 📂 demo/      # 🚀 [Demo] Flask web app, parser script, and final model (lightgbm_final.pkl)
 ┣ 📂 code/      # [Research] Jupyter notebooks for data prep, SMOTE, and model tuning
 ┣ 📂 data/      # [Research] Train/Test matrices and optimization records
 ┣ 📂 model/     # [Research] Checkpoint models and previous iterations (LR, RF)
 ┣ 📂 report/    # Weekly meeting minutes, performance reports, and markdown logs
 ┗ 📂 search/    # Presentation scripts, final PPT drafts, and domain research docs
```
