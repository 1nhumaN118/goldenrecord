# GoldenRecord

GoldenRecord is an intelligent entity resolution and deduplication tool that helps users identify and merge duplicate records in structured datasets. It combines feature similarity, ML prediction, user feedback, and explainability in a seamless interface.

---

## Project Structure

```
goldenrecord/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── logic/
│   │   ├── pairgen.py
│   │   ├── predict.py
│   │   ├── feedback.py
│   │   ├── cluster.py
│   │   └── report.py
│   ├── model/
│   │   ├── trained_model.pkl
│   │   └── shap_explainer.pkl
│   ├── data/
│   │   ├── uploads/
│   │   └── session/
├── frontend/
│   ├── pages/
│   │   ├── index.tsx
│   │   ├── confirm.tsx
│   │   └── report.tsx
│   ├── components/
│   │   ├── FileUpload.tsx
│   │   ├── DupConf.tsx
│   │   └── ReportView.tsx
│   └── lib/api.ts
```

---

## Features

- Upload Excel files with structured entity records
- Generate pairwise similarity using TF-IDF & SBERT
- Predict duplicate probability with XGBoost
- Let user confirm/reject suggestions with feedback loop
- Visualize SHAP feature importance and export golden record clusters

---

## How to Run (Development)

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Open: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open: [http://localhost:3000](http://localhost:3000)

---

## Version

- Phase 1 MVP (May 2025)
- Includes UI/UX, model prediction, feedback, SHAP and report export

---

## Contact

**Author**: tranvu.812  
**GitHub**: [github.com/1nhumaN118](https://github.com/1nhumaN118)  
**Email**: [tranvu.812@gmail.com](tranvu.812@gmail.com)