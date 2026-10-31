# Masthik Anveshan: Advanced Brain Tumor Segmentation & Diagnostic Intelligence

[![PyTorch](https://img.shields.io/badge/PyTorch-2.14-EE4C2C.svg?logo=pytorch)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg?logo=flask)](https://flask.palletsprojects.com/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online%20Workstation-00f2fe.svg?logo=googlechrome&logoColor=white)](https://a22aac9d53a20336-103-165-15-20.serveousercontent.com)
[![BraTS 2020](https://img.shields.io/badge/Dataset-BraTS%202020-00f2fe.svg)](https://www.med.upenn.edu/cbica/brats2020/)
[![Jun Cheng Figshare](https://img.shields.io/badge/Dataset-Jun%20Cheng%20Figshare-8b5cf6.svg)](https://figshare.com/articles/brain_tumor_dataset/1512427)
[![Kaggle 4-Class](https://img.shields.io/badge/Dataset-Kaggle%204--Class-10b981.svg)](https://www.kaggle.com/)

> 🌐 **Public Live Working URL**: [https://a22aac9d53a20336-103-165-15-20.serveousercontent.com](https://a22aac9d53a20336-103-165-15-20.serveousercontent.com)
> *(Also configured for 1-click cloud deployment via `Procfile` & `render.yaml`)*

**Masthik Anveshan** (Brain Exploration & Investigation) is a clinical-grade neuro-oncology AI diagnostic workstation. It unifies deep learning brain tumor segmentation (inspired by and extending [Muvva-Radhika/Brain_Tumor_Segmentation](https://github.com/Muvva-Radhika/Brain_Tumor_Segmentation)) with multi-class diagnostic classification across all major benchmark datasets.


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

## 🚀 Quick Launch

### Windows 1-Click Launch:
Double-click `run_app.bat` in the project root or `run.bat` in the `neuralBlack` folder:
```bat
run_app.bat
```
The server will start and automatically open **`http://localhost:5000`** in your default web browser.

### Manual Terminal Launch:
```powershell
& ".\neuralBlack\.python\python.exe" ".\neuralBlack\app.py"
```

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
    ├── deploy.py                 # Port 3000 secondary entrypoint
    ├── run.bat                   # Direct launcher inside neuralBlack
    ├── models/                   # Deep learning model state weights
    ├── test_images/              # Authentic clinical test MRI scans
    ├── results/                  # Training curves, confusion matrices, evaluation plots
    ├── static/
    │   ├── css/main.css          # Glassmorphic dark-mode clinical UI styling
    │   ├── js/app.js             # Reactive interactive logic, split slider, presets
    │   └── images/               # Workstation logos and graphics
    └── template/
        └── index.html            # Main 5-tab medical workstation single-page application
```

---

## 📚 Citations & References

- **Muvva-Radhika**: [Brain_Tumor_Segmentation](https://github.com/Muvva-Radhika/Brain_Tumor_Segmentation)
- **BraTS 2020**: Bakas et al., *"Advancing The Cancer Genome Atlas glioma analysis with pre-processed volumetric data and self-organizing maps"*, Nature Scientific Data (2017).
- **Jun Cheng Figshare**: Cheng et al., *"Enhanced Performance of Brain Tumor Classification via Tumor Region Augmentation"*, PLOS ONE (2015).
- **Kaggle Brain Tumor MRI**: Nickparvar, M., *"Brain Tumor MRI Dataset"*, Kaggle Archives (2021).
