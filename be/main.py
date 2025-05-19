from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import pandas as pd

from config import UPLOAD_DIR, SESSION_DIR, OUTPUT_REPORT
from logic.pairgen import generate_pairs
from logic.predict import run_prediction
from logic.feedback import save_feedback
from logic.report import generate_report, get_report_stats, get_shap_beeswarm_plot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...), identifier: str = Form(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(SESSION_DIR, exist_ok=True)
    save_path = os.path.join(UPLOAD_DIR, "customers.xlsx")
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    with open(os.path.join(SESSION_DIR, "identifier.txt"), "w") as f:
        f.write(identifier)
    return {"status": "uploaded", "identifier": identifier}

@app.get("/predict")
def predict_pairs():
    df = pd.read_excel(os.path.join(UPLOAD_DIR, "customers.xlsx"))
    with open(os.path.join(SESSION_DIR, "identifier.txt")) as f:
        identifier = f.read().strip()
    generate_pairs(df, identifier)
    return run_prediction()

@app.post("/feedback")
def receive_feedback(data: dict):
    feedback = data.get("feedback", [])
    save_feedback(feedback)
    return {"status": "feedback saved", "count": len(feedback)}

@app.get("/report")
def download_report():
    path = generate_report()
    return FileResponse(path, filename="golden_record.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.get("/report/stats")
def report_stats():
    stats = get_report_stats()
    return JSONResponse(content=stats)

@app.get("/report/shap")
def report_shap():
    path = get_shap_beeswarm_plot()
    return FileResponse(path, media_type="image/png")