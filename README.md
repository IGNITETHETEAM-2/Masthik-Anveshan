# Masthik Anveshan: Advanced Brain Tumor Segmentation & Diagnostic Intelligence

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Showcase-22c55e.svg?logo=githubpages&logoColor=white)](https://IGNITETHETEAM-2.github.io/Masthik-Anveshan/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14-EE4C2C.svg?logo=pytorch)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg?logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](Dockerfile)
[![BraTS 2020](https://img.shields.io/badge/Dataset-BraTS%202020-00f2fe.svg)](https://www.med.upenn.edu/cbica/brats2020/)
[![Jun Cheng Figshare](https://img.shields.io/badge/Dataset-Jun%20Cheng%20Figshare-8b5cf6.svg)](https://figshare.com/articles/brain_tumor_dataset/1512427)
[![Kaggle 4-Class](https://img.shields.io/badge/Dataset-Kaggle%204--Class-10b981.svg)](https://www.kaggle.com/)

> 🌐 **Public Live Showcase & Interactive Simulator (GitHub Pages)**: [https://IGNITETHETEAM-2.github.io/Masthik-Anveshan/](https://IGNITETHETEAM-2.github.io/Masthik-Anveshan/)
>
> 🚀 **Dynamic Flask AI Workstation**: Turn-key cloud deployment ready for **Render**, **Railway**, **Fly.io**, or any Linux **VPS / Docker** server via included `render.yaml`, `railway.json`, `fly.toml`, `Dockerfile`, and `docker-compose.yml`.

**Masthik Anveshan** (Brain Exploration & Investigation) is a clinical-grade neuro-oncology AI diagnostic workstation. It unifies deep learning brain tumor segmentation (inspired by and extending [Muvva-Radhika/Brain_Tumor_Segmentation](https://github.com/Muvva-Radhika/Brain_Tumor_Segmentation)) with multi-class diagnostic classification across all major benchmark datasets.

---

## 🌟 Dual Deployment Architecture

| Component | Target Platform | Purpose | Link / Config |
| :--- | :--- | :--- | :--- |
| **Static Front-End & Docs** | **GitHub Pages** | High-availability showcase, interactive client-side MRI segmentation simulator, BraTS multi-sequence laboratory, architecture visualizer, and technical documentation. | [Live Site](https://IGNITETHETEAM-2.github.io/Masthik-Anveshan/) (`docs/`) |
| **Dynamic AI Backend** | **Render / Railway / Fly.io / VPS** | Full PyTorch neural engine, SQLite clinician authentication, live multipart MRI scan uploads, real-time segmentation inference, and automated PDF clinical reporting. | [`render.yaml`](render.yaml), [`railway.json`](railway.json), [`fly.toml`](fly.toml), [`Dockerfile`](Dockerfile), [`docker-compose.yml`](docker-compose.yml) |
| **Local Workstation** | **Windows Desktop** | Offline standalone clinical diagnostic platform on localhost port 5000. | [`run_app.bat`](../run_app.bat) / [`run.bat`](run.bat) |

---

## 🚀 Quick Launch & Cloud Deployment

### 1. View Public Showcase on GitHub Pages
Visit [https://IGNITETHETEAM-2.github.io/Masthik-Anveshan/](https://IGNITETHETEAM-2.github.io/Masthik-Anveshan/) to explore the live interactive client-side lesion segmentation simulator, compare scan before/after split sliders, and inspect BraTS 4-sequence modalities without needing a backend server.

### 2. Deploy Dynamic Flask App to Render
1. Go to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** &rarr; **Blueprint**.
3. Connect repository `IGNITETHETEAM-2/Masthik-Anveshan`.
4. Render automatically detects [`render.yaml`](render.yaml) and provisions the service with Gunicorn on HTTPS.

### 3. Deploy to Railway
Deploy with one command via the Railway CLI, or import the GitHub repo in Railway Dashboard:
```bash
railway login
railway init
railway up
```
Configuration is automatically read from [`railway.json`](railway.json).

### 4. Deploy to Fly.io
Launch a containerized micro-instance with global edge routing:
```bash
fly launch --now --copy-config
```
Uses the pre-configured [`fly.toml`](fly.toml) and production [`Dockerfile`](Dockerfile).

### 5. Deploy to Any Linux VPS / Docker Host
Run a single command on your Ubuntu/Debian/CentOS VPS:
```bash
git clone https://github.com/IGNITETHETEAM-2/Masthik-Anveshan.git
cd Masthik-Anveshan/neuralBlack
docker compose up -d --build
```
The server will start on port `5000` with volume persistence for SQLite clinician accounts.

### 6. Local Windows 1-Click Launch
Double-click `run_app.bat` in the project root or `run.bat` in this folder:
```bat
run_app.bat
```
The server will initialize and automatically open **`http://localhost:5000`** in your default web browser.

---

## 🌟 Key Capabilities

1. **PyTorch U-Net Lesion Segmentation**:
   - Replicates and enhances the U-Net architecture from `Muvva-Radhika/Brain_Tumor_Segmentation` (3 Encoder levels, Bottleneck, 3 Decoder levels with skip concatenations).
   - Generates pixel-level tumor probability heatmaps, adjustable threshold binary masks (0.10 to 0.90), and glowing contour overlays.
   - BraTS multi-region segmentation breakdown: Necrotic Core (NCR), Enhancing Tumor (ET), and Peritumoral Vasogenic Edema (ED).
   - Interactive **Split Screen Comparison Slider** to swipe and inspect Raw MRI vs. Segmentation Mask side-by-side.

2. **Multi-Class Diagnostic Classification**:
   - Classifies brain MRI scans into 4 clinical categories:
     - **Glioma** (WHO Grade II - IV Astrocytoma / Glioblastoma)
     - **Meningioma** (WHO Grade I - II Dural-based neoplasm)
     - **Pituitary Tumor** (Sellar / Suprasellar Macroadenoma)
     - **No Tumor** (Normal / Healthy Control MRI)
   - Real-time softmax probability distribution with animated confidence meters.

3. **Combined Training Datasets Hub**:
   - **BraTS 2020 (MICCAI)**: 369 training volumes, 57,195 slices, 4 co-registered MRI sequences (FLAIR, T1, T1ce, T2).
   - **Jun Cheng Figshare Benchmark**: 3,064 T1-weighted contrast-enhanced images across 233 patients.
   - **Kaggle Unified Benchmark (Sartaj Bhuvaji & Masoud Nickparvar)**: 7,023+ MRI images across 4 balanced categories.
   - In-app dataset statistics, volume breakdowns, and 1-click preset case loader.

4. **BraTS 4-Sequence Multi-Modal Laboratory**:
   - View co-registered **T1**, **T1-CE**, **T2**, and **FLAIR** sequences in a synchronized 4-quadrant layout.
   - Explore how different pulse sequences reveal distinct biophysical tumor tissue characteristics.

5. **Quantitative Morphometrics & Diagnostic Report**:
   - Computes total positive tumor pixels, estimated surface area ($mm^2$ at 1.0mm isotropic resolution), equivalent circular diameter ($mm$), intracranial slice coverage (%), centroid coordinates $(X, Y)$, and anatomical quadrant/lobe localization.
   - Auto-compiles a structured, formal **Clinical Diagnostic Report** with patient UID, radiological findings, thumbnail evidence, staging risk, and 1-click Print/PDF export.

---

## 🔬 Architecture & Model Specifications

```
[Input MRI Scan: (240 x 240 x 1/4)]
       │
       ▼
[Encoder Level 1: Conv2D(32) -> BatchNorm -> ReLU -> Conv2D(32)] ───────── [Skip Concatenation 1] ────────┐
       │ (MaxPool 2x2)                                                                                     │
       ▼                                                                                                   │
[Encoder Level 2: Conv2D(64) -> BatchNorm -> ReLU -> Conv2D(64)] ───── [Skip Concatenation 2] ─────┐      │
       │ (MaxPool 2x2)                                                                              │      │
       ▼                                                                                            │      │
[Encoder Level 3: Conv2D(128) -> BatchNorm -> ReLU -> Conv2D(128)] ─ [Skip Concatenation 3] ─┐     │      │
       │ (MaxPool 2x2)                                                                       │     │      │
       ▼                                                                                     │     │      │
[Bottleneck: Conv2D(256) -> BatchNorm -> ReLU -> Conv2D(256)]                                │     │      │
       │                                                                                     │     │      │
       ▼ (UpSample 2x2 + Concat)                                                             │     │      │
[Decoder Level 1: Conv2D(128) -> ReLU -> Conv2D(128)] <──────────────────────────────────────┘     │      │
       │                                                                                           │      │
       ▼ (UpSample 2x2 + Concat)                                                                   │      │
[Decoder Level 2: Conv2D(64) -> ReLU -> Conv2D(64)] <──────────────────────────────────────────────┘      │
       │                                                                                                  │
       ▼ (UpSample 2x2 + Concat)                                                                          │
[Decoder Level 3: Conv2D(32) -> ReLU -> Conv2D(32)] <─────────────────────────────────────────────────────┘
       │
       ▼
[Output Head 1: 1x1 Conv (Sigmoid) -> Tumor Probability Map (240 x 240 x 1)]
[Output Head 2: 1x1 Conv (Sigmoid) -> BraTS Sub-Regions (NCR / ED / ET)]
```

---

## 📂 Project Structure

```
Masthik Anveshan/
├── run_app.bat                   # 1-Click launcher at root
├── radhika_reference/            # Cloned reference repo (Muvva-Radhika/Brain_Tumor_Segmentation)
└── neuralBlack/
    ├── app.py                    # Unified Flask application & REST API
    ├── models_engine.py          # PyTorch U-Net & 4-Class diagnostic engine
    ├── datasets_data.py          # Combined datasets registry, statistics & presets
    ├── auth_db.py                # Clinician authentication & user management
    ├── generate_pdf_report.py    # Formal clinical PDF report generator
    ├── render.yaml               # 1-Click Render blueprint deployment config
    ├── railway.json              # Railway deployment configuration
    ├── fly.toml                  # Fly.io deployment configuration
    ├── Dockerfile                # Production container specification (Python 3.10 slim)
    ├── docker-compose.yml        # 1-Command self-hosted VPS compose file
    ├── Procfile                  # Production Gunicorn process runner
    ├── docs/                     # Static front-end & docs hosted on GitHub Pages
    │   ├── index.html            # Interactive clinical landing page & simulator
    │   └── images/               # High-res scans, benchmark curves, confusion matrix
    ├── index.html                # Root GitHub Pages redirection entrypoint
    ├── .github/workflows/        # Automated GitHub Pages deployment workflow
    │   └── pages.yml
    ├── models/                   # Deep learning model state weights
    ├── test_images/              # Authentic clinical test MRI scans
    ├── results/                  # Training curves, confusion matrices, evaluation plots
    ├── static/                   # Flask dynamic webstation static assets
    └── template/                 # Flask Jinja2 workstation templates
```

---

## 📚 Citations & References

- **Muvva-Radhika**: [Brain_Tumor_Segmentation](https://github.com/Muvva-Radhika/Brain_Tumor_Segmentation)
- **BraTS 2020**: Bakas et al., *"Advancing The Cancer Genome Atlas glioma analysis with pre-processed volumetric data and self-organizing maps"*, Nature Scientific Data (2017).
- **Jun Cheng Figshare**: Cheng et al., *"Enhanced Performance of Brain Tumor Classification via Tumor Region Augmentation"*, PLOS ONE (2015).
- **Kaggle Brain Tumor MRI**: Nickparvar, M., *"Brain Tumor MRI Dataset"*, Kaggle Archives (2021).
