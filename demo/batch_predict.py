# sample/ 폴더의 모든 .exe를 일괄 예측해서 CSV로 저장
#
# 폴더 구조 예:
#   sample/LockBit/xxx.exe
#   sample/Lumma/yyy.exe
#   sample/normal/notepad.exe
# → family 컬럼은 sample 바로 아래 하위 폴더명으로 채움 (없으면 "(root)")

import csv
import joblib
import pandas as pd
import pefile
from pathlib import Path

BASE_DIR   = Path(__file__).parent
MODEL_PATH = BASE_DIR / "model" / "lightgbm_final.pkl"
SAMPLE_DIR = BASE_DIR / "sample"
OUTPUT_CSV = BASE_DIR / "batch_results.csv"

bundle    = joblib.load(MODEL_PATH)
model     = bundle["model"]
features  = bundle["features"]
threshold = bundle["threshold"]


def extract_apis(path):
    try:
        pe = pefile.PE(str(path))
        apis = set()
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name:
                        apis.add(imp.name.decode("utf-8", errors="ignore"))
        pe.close()
        return apis, None
    except Exception as e:
        return None, str(e)


rows = []
exe_paths = sorted(SAMPLE_DIR.rglob("*.exe"))
print(f"Found {len(exe_paths)} .exe files under {SAMPLE_DIR}")

for path in exe_paths:
    rel    = path.relative_to(SAMPLE_DIR)
    family = rel.parts[0] if len(rel.parts) > 1 else "(root)"
    apis, err = extract_apis(path)

    if err:
        rows.append({
            "family": family,
            "file": rel.name,
            "prediction": "ERROR",
            "raw_proba": "",
            "confidence_pct": "",
            "total_imported_apis": "",
            "matched_features": "",
            "error": err,
        })
        continue

    vector     = [1 if f in apis else 0 for f in features]
    X          = pd.DataFrame([vector], columns=features)
    proba      = float(model.predict_proba(X)[0, 1])
    is_malware = proba >= threshold
    confidence = proba if is_malware else (1 - proba)

    rows.append({
        "family": family,
        "file": rel.name,
        "prediction": "악성" if is_malware else "정상",
        "raw_proba": round(proba, 4),
        "confidence_pct": round(confidence * 100, 2),
        "total_imported_apis": len(apis),
        "matched_features": sum(vector),
        "error": "",
    })

fieldnames = ["family", "file", "prediction", "raw_proba", "confidence_pct",
              "total_imported_apis", "matched_features", "error"]

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

total   = len(rows)
errors  = sum(1 for r in rows if r["prediction"] == "ERROR")
malware = sum(1 for r in rows if r["prediction"] == "악성")
normal  = sum(1 for r in rows if r["prediction"] == "정상")

print(f"\n=== Summary ===")
print(f"Total:   {total}")
print(f"Malware: {malware}")
print(f"Normal:  {normal}")
print(f"Errors:  {errors}")
print(f"\nResults saved to: {OUTPUT_CSV}")
