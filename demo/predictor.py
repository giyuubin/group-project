# 저장된 LightGBM 번들로 단일 .exe 파일의 악성 여부 예측
#
# 동작: .exe의 IAT(Import Address Table)를 파싱 → import하는 Windows API 이름 수집
#       → 모델이 쓰는 피처를 0/1 벡터로 변환 → LightGBM 예측 → threshold 적용

import os
import joblib
import pandas as pd
import pefile

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "lightgbm_final.pkl")

_bundle    = joblib.load(MODEL_PATH)
_model     = _bundle["model"]
_features  = _bundle["features"]
_threshold = _bundle["threshold"]


def _extract_imported_apis(source):
    """PE 파일의 IAT에서 import하는 API 이름 집합을 추출. source는 파일 경로(str) 또는 바이트(bytes)."""
    if isinstance(source, (bytes, bytearray)):
        pe = pefile.PE(data=source)
    else:
        pe = pefile.PE(source)
    apis = set()
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                if imp.name:
                    apis.add(imp.name.decode("utf-8", errors="ignore"))
    pe.close()
    return apis


def predict(source):
    apis   = _extract_imported_apis(source)
    vector = [1 if f in apis else 0 for f in _features]
    X      = pd.DataFrame([vector], columns=_features)

    proba      = float(_model.predict_proba(X)[0, 1])
    is_malware = proba >= _threshold
    confidence = proba if is_malware else (1 - proba)

    return {
        "prediction": "악성파일" if is_malware else "정상파일",
        "confidence": round(confidence * 100, 2),
    }
