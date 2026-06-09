# 🛡️ ML-Based Static API Malware Detection System (Pre-filter)
**Gachon University — AI Programming Team 05**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-3.3+-green.svg?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-Web_Demo-black.svg?style=flat-square)

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

### 2. Run Real-time Web Scanner (UI)
```bash
python app.py
```
* Open your web browser and navigate to `http://127.0.0.1:5000`.
* Upload any `.exe` file. The system will instantly parse the PE IAT and display the maliciousness probability.

### 3. Run Batch Prediction (Packed Malware Defense)
This script demonstrates our model's capability to detect highly packed or obfuscated malware (e.g., `njRAT`, `Remcos`) where 0 API features are extracted.
```bash
python batch_predict.py
```
* The console will output the prediction logs, showing how the model successfully blocks them with a **94.92% probability** by leveraging the "absence of normal indicators".

<br>

## 🔬 Core Achievements
Our deployed model (`lightgbm_final.pkl`) was built through the following optimizations:

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
