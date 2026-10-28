<!--
=====================================================================
 📸 SCREENSHOT CHECKLIST  (save every image in docs/screenshots/)
=====================================================================
 [ ] 1.  hero.png              Streamlit app with a high-risk alert
 [ ] 2.  architecture.png      Architecture diagram
 [ ] 3.  training-output.png   Terminal: python -m logiai.train
 [ ] 4.  swagger-ui.png        Full /docs page, routes collapsed
 [ ] 5.  predict-200.png       Swagger: valid request + 200 response
 [ ] 6.  predict-422.png       Swagger: invalid request + 422 response
 [ ] 7.  predict-503.png       Swagger: 503 when models/ is missing
 [ ] 8.  streamlit-alert.png   Streamlit: high-risk delivery + alert
 [ ] 9.  streamlit-ok.png      Streamlit: easy delivery + green message
 [ ] 10. streamlit-api-down.png Streamlit: "API injoignable" error
 [ ] 11. pytest.png            Terminal: python -m pytest (all passed)
 [ ] 12. pull-request.png       GitHub pull request page

 TIP: if you skip a screenshot, delete its <img ... /> line, otherwise
 GitHub shows a broken-image icon. Delete this whole comment at the end.
=====================================================================
-->

<div align="center">

# 🚚 LogiAI

### Predict delivery delay risk and serve it through a REST API

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-validation-E92063?logo=pydantic&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-client-FF4B4B?logo=streamlit&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)

<!--
  📸 SCREENSHOT 1 — hero.png
  WHAT : The Streamlit app after clicking "Évaluer" with worst-case settings
         (long distance, heavy rain, traffic 10, camion). The probability and
         the "Alerte : livraison à risque" message must be visible.
  HOW  : streamlit run streamlit_app.py (API must be running). Crop tightly.
         You can simply copy streamlit-alert.png and rename it.
  SAVE : docs/screenshots/hero.png
-->
<img src="docs/screenshots/hero.png" alt="LogiAI hero screenshot" width="800"/>

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Architecture](#-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Streamlit Client](#-streamlit-client)
- [Testing](#-testing)
- [Design Decisions](#-design-decisions)
- [Extensions & Roadmap](#-extensions--roadmap)
- [Git Workflow](#-git-workflow)
- [Authors](#-authors)
- [Acknowledgements](#-acknowledgements)

---

## 🎯 About the Project

A transport company wants to warn its dispatchers when a delivery is likely to arrive **late**. A machine learning model already exists, but it is locked inside a Python script: only the person who owns the script can use it.

**LogiAI turns that model into a service.** A dashboard, a mobile app or a Streamlit interface sends the characteristics of a delivery over the network and receives back the **probability of delay**, along with an **alert** if it exceeds the threshold (**0.4**).

```
Before :  [ script + model ]                  → a single user

After  :  [ Streamlit ] --\
          [ Mobile    ] ----HTTP/JSON--> [ FastAPI API + model ]
          [ Dashboard ] --/
```

> This project was built as part of **Atelier 3 – REST API with FastAPI** for the module *Développement et déploiement d'applications intelligentes* at **EMSI** (École Marocaine des Sciences de l'Ingénieur), academic year 2026–2027.

---

## 🏗 Architecture

<!--
  📸 SCREENSHOT 2 — architecture.png
  WHAT : A diagram showing: clients (browser, curl, Streamlit, mobile) →
         port 8000 → uvicorn → FastAPI app → model loaded in memory
         (model.joblib read from disk once at startup).
  HOW  : Use the diagram from your course PDF (crop it), or redraw it with
         draw.io / Excalidraw / Canva and export as PNG.
  SAVE : docs/screenshots/architecture.png
-->
<img src="docs/screenshots/architecture.png" alt="LogiAI architecture" width="800"/>

| Layer | Role |
|-------|------|
| **uvicorn** | Launches the app and listens on port `8000` |
| **FastAPI application** | Defines the routes: `/health`, `/v1/predict`, `/docs` |
| **Model (`model.joblib`)** | Loaded **once at startup** and kept in memory for fast responses |
| **Clients** | Browser (`/docs`), `curl`, Streamlit, mobile apps, Java… |

---

## ✨ Features

- 🔮 **Delay prediction** – returns the probability of delay for a delivery and an alert flag
- ✅ **Strict input validation** with Pydantic: types, physical bounds and documented fields
- 📚 **Auto-generated documentation** (Swagger UI) at `/docs`
- ⚡ **Model loaded once** at startup through FastAPI's `lifespan`
- 🚦 **Meaningful HTTP status codes**: `200`, `422` (invalid input), `503` (model not loaded)
- ❤️ **Health endpoint** reporting whether the model is loaded
- 🧪 **Automated test suite** with `pytest` (`TestClient`)
- 🖥 **Streamlit client** that contains *no model*, only HTTP calls to the API

---

## 🛠 Tech Stack

| Category | Technology |
|----------|-----------|
| Language | Python |
| API framework | FastAPI |
| ASGI server | uvicorn |
| Validation | Pydantic |
| Machine learning | scikit-learn, joblib |
| Client UI | Streamlit, requests |
| Testing | pytest |
| Version control | Git / GitHub |

---

## 📂 Project Structure

```
LogiAI/
├── logiai/
│   ├── config.py          # settings: paths, alert threshold (0.4), variable names
│   ├── dataset.py         # generates the deliveries dataset
│   ├── train.py           # trains the model and saves it
│   ├── predict.py         # loads the model and predicts for one delivery
│   └── api/
│       ├── schemas.py     # Pydantic schemas (input "Livraison" / output "PredictionOut")
│       └── main.py        # FastAPI app and routes
├── tests/
│   └── test_api.py        # API test suite
├── docs/
│   └── screenshots/       # images used in this README
├── data/
│   └── livraisons.csv     # generated dataset (not tracked by Git)
├── models/
│   └── model.joblib       # trained model (not tracked by Git)
├── streamlit_app.py       # Streamlit client
├── requirements.txt
├── COMPTE_RENDU.md        # lab report
└── README.md
```

> ⚠️ `.venv/`, `data/*.csv`, `models/` and `.env` are **never committed** (see `.gitignore`).

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/anaskoukham49/LogiAI.git
cd LogiAI

# 2. Switch to the working branch
git switch tp-api

# 3. Create and activate a virtual environment
python -m venv .venv

# Windows (cmd)
.venv\Scripts\activate.bat
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Generate the data and train the model
python -m logiai.dataset      # writes data/livraisons.csv
python -m logiai.train        # writes models/model.joblib
```

<!--
  📸 SCREENSHOT 3 — training-output.png
  WHAT : Your terminal right after `python -m logiai.train`, showing the
         baseline accuracy, the model accuracy and the recall.
  HOW  : Run the command, then capture only the terminal text (no desktop).
         Use a readable font size.
  SAVE : docs/screenshots/training-output.png
-->
<img src="docs/screenshots/training-output.png" alt="Training output" width="700"/>

---

## ▶️ Usage

### Start the API

```bash
python -m uvicorn logiai.api.main:app --reload
```

The API is now available at **http://localhost:8000** and the interactive documentation at **http://localhost:8000/docs**.

<!--
  📸 SCREENSHOT 4 — swagger-ui.png
  WHAT : The whole Swagger page at http://localhost:8000/docs with the
         routes visible (GET /health, POST /v1/predict) and the Schemas
         section at the bottom (Livraison, PredictionOut).
  HOW  : Open /docs, collapse each route by clicking its arrow so everything
         fits on one screen. Zoom the browser to ~90%.
  SAVE : docs/screenshots/swagger-ui.png
-->
<img src="docs/screenshots/swagger-ui.png" alt="Swagger UI" width="800"/>

### Quick test with `curl`

```bash
curl http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d @livraison.json
```

> 💡 On Windows (cmd / PowerShell) use `curl.exe` and **do not** wrap the JSON in single quotes: pass it from a file with `-d @livraison.json`.

---

## 📡 API Reference

### `GET /health`

Checks that the service is running and whether the model is loaded.

```json
{ "status": "ok", "model_loaded": true }
```

### `POST /v1/predict`

Predicts the risk of delay for a single delivery.

**Request body (the API "contract")**

| Field | Type | Description |
|-------|------|-------------|
| `distance_km` | float | Trip distance in km |
| `poids_kg` | float | Transported weight in kg |
| `heure_depart` | int | Departure hour, from 0 to 23 |
| `pluie_mm` | float | Forecast rainfall along the route (mm) |
| `trafic_index` | float | Traffic index: 0 = free-flowing, 10 = saturated |
| `nb_arrets` | int | Number of delivery stops |
| `type_vehicule` | string | `"moto"`, `"fourgon"` or `"camion"` |

**Example request**

```json
{
  "distance_km": 120,
  "poids_kg": 450,
  "heure_depart": 17,
  "pluie_mm": 8.0,
  "trafic_index": 7.5,
  "nb_arrets": 4,
  "type_vehicule": "camion"
}
```

**Response body**

| Field | Type | Description |
|-------|------|-------------|
| `probabilite_retard` | float | Probability that the delivery is late (0 to 1) |
| `alerte` | bool | `true` when the probability reaches the threshold |
| `seuil` | float | Alert threshold used (0.4, defined in `config.py`) |
| `model_version` | string | Version of the model that produced the prediction |

**Example response** (`200 OK`)

```json
{
  "probabilite_retard": 0.73,
  "alerte": true,
  "seuil": 0.4,
  "model_version": "1.0"
}
```

> The `probabilite_retard` value above is illustrative; replace it with a real value from your API if you like.

<!--
  📸 SCREENSHOT 5 — predict-200.png
  WHAT : Swagger "Try it out" with a REALISTIC valid request (e.g. 120 km,
         450 kg, 17h, 8 mm, traffic 7.5, 4 stops, camion) and the
         "Server response" showing code 200 + the JSON body.
  HOW  : /docs → POST /v1/predict → Try it out → edit values → Execute →
         capture the curl / request URL / Server response area.
  SAVE : docs/screenshots/predict-200.png
-->
<img src="docs/screenshots/predict-200.png" alt="Successful prediction" width="800"/>

### Status codes

| Code | Meaning | When it happens in LogiAI |
|------|---------|---------------------------|
| `200` | Success | Prediction returned |
| `404` | Unknown route | Typo in the URL (e.g. `/v1/predcit`) |
| `422` | Invalid input | Out-of-range or malformed value (e.g. 500 mm of rain, `distance_km = -5`, `type_vehicule = "avion"`) |
| `500` | Server error | Bug in the code |
| `503` | Service unavailable | Model not loaded |

<!--
  📸 SCREENSHOT 6 — predict-422.png
  WHAT : Swagger "Server response" showing code 422 and the "detail" block
         that names the faulty field (e.g. pluie_mm too large).
  HOW  : POST /v1/predict → Try it out → set "pluie_mm": 500 (or
         "distance_km": -5) → Execute → capture the response part.
  SAVE : docs/screenshots/predict-422.png
-->
<img src="docs/screenshots/predict-422.png" alt="Validation error 422" width="800"/>

<!--
  📸 SCREENSHOT 7 — predict-503.png
  WHAT : Swagger "Server response" showing code 503 and the error message
         saying the model is missing and what to do.
  HOW  : Stop the server, delete the models/ folder, restart uvicorn, call
         /v1/predict and capture the response. Afterwards run
         `python -m logiai.train` to restore the model.
         (Optional bonus: also capture /health with model_loaded: false.)
  SAVE : docs/screenshots/predict-503.png
-->
<img src="docs/screenshots/predict-503.png" alt="Service unavailable 503" width="800"/>

---

## 🖥 Streamlit Client

A web interface that calls the API through `POST /v1/predict`. It does **not** import scikit-learn or the model: the API is the single source of truth.

Open **two terminals**:

```bash
# Terminal 1: the API
python -m uvicorn logiai.api.main:app --reload

# Terminal 2: the interface
streamlit run streamlit_app.py
```

<!--
  📸 SCREENSHOT 8 — streamlit-alert.png
  WHAT : Streamlit with worst-case settings (long distance, heavy rain,
         traffic 10, camion, hour 17), showing the high probability metric
         and the yellow "Alerte : livraison à risque." banner.
  HOW  : Set the sliders, click "Évaluer", capture the whole app.
  SAVE : docs/screenshots/streamlit-alert.png
-->
<img src="docs/screenshots/streamlit-alert.png" alt="Streamlit high risk alert" width="700"/>

<!--
  📸 SCREENSHOT 9 — streamlit-ok.png
  WHAT : Streamlit with an easy delivery showing a very low probability
         (about 2%) and the green "Livraison probablement à l'heure."
  HOW  : Set moto, 5 km, 3 kg, rain 0, traffic 1, 0 stops, hour 11 →
         click "Évaluer" → capture the whole app.
  SAVE : docs/screenshots/streamlit-ok.png
-->
<img src="docs/screenshots/streamlit-ok.png" alt="Streamlit low risk" width="700"/>

<!--
  📸 SCREENSHOT 10 — streamlit-api-down.png
  WHAT : Streamlit showing the red error "API injoignable : lancez uvicorn
         dans un autre terminal."
  HOW  : Press Ctrl+C in the uvicorn terminal, then click "Évaluer" in
         Streamlit and capture the error message.
  SAVE : docs/screenshots/streamlit-api-down.png
-->
<img src="docs/screenshots/streamlit-api-down.png" alt="Streamlit API unreachable" width="700"/>

---

## 🧪 Testing

```bash
python -m pytest
```

The test suite uses `TestClient(app)` inside a `with` block, so the application's startup (and therefore the model loading) runs exactly as on a real server.

<!--
  📸 SCREENSHOT 11 — pytest.png
  WHAT : Terminal showing the pytest session with all tests passing
         (green "passed" summary line at the bottom, e.g. 15 passed
         including your 2 personal tests).
  HOW  : Run `python -m pytest` and capture the terminal output.
  SAVE : docs/screenshots/pytest.png
-->
<img src="docs/screenshots/pytest.png" alt="pytest results" width="700"/>

---

## 🧠 Design Decisions

**Why a schema?** One Pydantic class is written once and used for three things: it **validates** requests (automatic `422`), **documents** the API (`/docs`), and provides a **typed Python object** inside the route.

**Why load the model at startup?** Loading from disk on every request would be slow and wasteful. The model is read once in `lifespan` and reused from memory.

**Why `503` and not `500` when the model is missing?** A missing model is not a bug in the code but a temporary unavailability of the service, so `503 Service Unavailable` with a message explaining what to do is the correct signal for clients.

**Physical bounds, not data bounds.** Field limits reflect what a real trip can look like, not the min/max of `livraisons.csv`, otherwise a slightly longer real delivery would be wrongly rejected.

---

## 🔭 Extensions & Roadmap

- [ ] **Batch prediction**: `POST /v1/predict-batch` accepting a list of deliveries
- [ ] **Model info route**: `GET /v1/model-info` (version, features, metrics)
- [ ] **API key protection** via an `X-API-Key` header (`401` if missing/invalid)
- [ ] **Image prediction** route (`UploadFile`) for the MNIST model
- [ ] **Threshold tuning**: study the precision/recall trade-off of `ALERT_THRESHOLD`
- [ ] Containerization and deployment

---

## 🌿 Git Workflow

The project is developed on the **`tp-api`** branch and merged through a **pull request** reviewed by the other team member.

```bash
git switch -c tp-api
git add .
git commit -m "TP API: schema, predict, tests, Streamlit client"
git pull        # always pull before pushing
git push -u origin tp-api
```

<!--
  📸 SCREENSHOT 12 — pull-request.png
  WHAT : The GitHub pull request page (from tp-api) showing the title,
         the commits / files changed and your partner's review if any.
  HOW  : On GitHub → Pull requests → open yours → capture the top of the page.
  SAVE : docs/screenshots/pull-request.png
-->
<img src="docs/screenshots/pull-request.png" alt="Pull request" width="800"/>

---

## 👥 Authors

| Name | GitHub |
|------|--------|
| **Anas Koukham** | [@anaskoukham49](https://github.com/anaskoukham49) |
| *Partner name* | [@partner-username](https://github.com/partner-username) |

---

## 🙏 Acknowledgements

- **Pr. Soukaina Gouraguine** – module supervisor
- **EMSI – École Marocaine des Sciences de l'Ingénieur**
- [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/), [Streamlit](https://streamlit.io/), [scikit-learn](https://scikit-learn.org/)

---

<div align="center">

Made with ❤️ at EMSI · 2026–2027

</div>
