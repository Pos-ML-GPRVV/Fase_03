# app_lib/api.py
import os
import json
import requests
import streamlit as st

def _base():
    api_url = st.session_state.get("API_URL", os.getenv("API_URL", "http://127.0.0.1:8000")).rstrip("/")
    api_key = st.session_state.get("API_KEY", os.getenv("API_KEY", "senha123"))
    headers = {"Api-Key": api_key}
    return api_url, headers

def get_json(path: str):
    api_url, headers = _base()
    try:
        r = requests.get(f"{api_url}{path}", headers=headers, timeout=30)
        return (r.json(), None) if r.status_code == 200 else (None, f"GET {path} -> {r.status_code}: {r.text}")
    except Exception as e:
        return None, f"GET {path} -> erro: {e}"

def post_json(path: str, payload: dict | None = None):
    api_url, headers = _base()
    try:
        r = requests.post(
            f"{api_url}{path}",
            headers={**headers, "Content-Type": "application/json"},
            data=json.dumps(payload or {}),
            timeout=120,
        )
        return (r.json(), None) if r.status_code == 200 else (None, f"POST {path} -> {r.status_code}: {r.text}")
    except Exception as e:
        return None, f"POST {path} -> erro: {e}"
