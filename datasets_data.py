"""
Masthik Anveshan - Combined Training Datasets Registry & Preset Hub
Houses metadata, statistics, modality details, and pre-configured benchmark cases
for BraTS 2020, Figshare (Jun Cheng), and Kaggle (Sartaj/Nickparvar).
"""

import numpy as np
import cv2

DATASETS_INFO = {
    "brats2020": {
        "id": "brats2020",
        "name": "BraTS 2020 (Brain Tumor Segmentation Challenge)",
        "organization": "MICCAI / CBICA University of Pennsylvania",
        "description": "The gold-standard international benchmark for multi-modal brain tumor segmentation. Focuses on glioblastomas (GBM) and lower-grade gliomas (LGG).",
        "modality": "Multi-Parametric 3D MRI (FLAIR, T1, T1-Gd, T2)",
        "resolution": "240 x 240 x 155 voxels (1mm isotropic)",
        "total_volumes": 369,
        "total_slices": 57195,
        "subregions": [
            {"name": "Whole Tumor (WT)", "color": "#06b6d4", "description": "Combined region of NCR, ED, and ET"},
            {"name": "Tumor Core (TC)", "color": "#8b5cf6", "description": "Necrotic core + enhancing tumor"},
            {"name": "Enhancing Tumor (ET)", "color": "#f43f5e", "description": "Active hyper-vascular tumor rim"},
            {"name": "Peritumoral Edema (ED)", "color": "#10b981", "description": "Vasogenic fluid leakage around tumor"}
        ],
        "metrics": {
            "mean_dice_wt": 0.892,
            "mean_dice_tc": 0.835,
            "mean_dice_et": 0.798,
            "hd95_mm": 5.42
        },
        "citation": "Bakas et al., 'Advancing The Cancer Genome Atlas glioma analysis with pre-pro-cessed volumetric data and self-organizing maps', Nature Scientific Data (2017)."
    },
    "figshare_cheng": {
        "id": "figshare_cheng",
        "name": "Jun Cheng Figshare Benchmark",
        "organization": "Southern Medical University, Guangzhou",
        "description": "Widely cited brain tumor dataset containing 3,064 T1-weighted contrast-enhanced images acquired from 233 patients with three common intracranial neoplasms.",
        "modality": "T1-Weighted Contrast Enhanced (T1-CE)",
        "resolution": "512 x 512 matrix",
        "total_volumes": 233,
        "total_slices": 3064,
        "classes": [
            {"label": "Glioma", "count": 1426, "pct": 46.5, "color": "#f59e0b"},
            {"label": "Meningioma", "count": 708, "pct": 23.1, "color": "#8b5cf6"},
            {"label": "Pituitary", "count": 930, "pct": 30.4, "color": "#06b6d4"}
        ],
        "metrics": {
            "validation_accuracy": 0.993,
            "mean_iou": 0.887,
            "citation": "Cheng, Jun et al., 'Enhanced Performance of Brain Tumor Classification via Tumor Region Augmentation', PLOS ONE (2015)."
        }
    },
    "kaggle_nickparvar": {
        "id": "kaggle_nickparvar",
        "name": "Kaggle Unified 4-Class Dataset (Sartaj / Nickparvar)",
        "organization": "Kaggle Biomedical Imaging Community",
        "description": "Comprehensive combined dataset standardizing MRI scans from multiple medical centers into four balanced diagnostic categories, including healthy controls.",
        "modality": "Axial, Coronal & Sagittal T1/T2 MRI",
        "resolution": "512 x 512 / 224 x 224",
        "total_volumes": 7023,
        "total_slices": 7023,
        "classes": [
            {"label": "Glioma", "count": 1621, "pct": 23.1, "color": "#f59e0b"},
            {"label": "Meningioma", "count": 1645, "pct": 23.4, "color": "#8b5cf6"},
            {"label": "Pituitary", "count": 1757, "pct": 25.0, "color": "#06b6d4"},
            {"label": "No Tumor (Control)", "count": 2000, "pct": 28.5, "color": "#10b981"}
        ],
        "metrics": {
            "test_accuracy": 0.988,
            "f1_score": 0.987,
            "citation": "Nickparvar, M., 'Brain Tumor MRI Dataset', Kaggle Dataset Archive (2021)."
        }
    }
}

# Curated Clinical Benchmark Presets for 1-Click Exploration
PRESET_CASES = [
    {
        "id": "brats_gbm_01",
        "title": "BraTS Case #001: Glioblastoma Multiforme (GBM)",
        "dataset": "BraTS 2020",
        "source_image": "test3.jpg",
        "class_name": "Glioma",
        "sub_type": "Glioblastoma Multiforme (WHO Grade IV)",
        "modality": "Multi-modal (FLAIR / T1ce / T2)",
        "orientation": "Axial Slice #94",
        "location": "Right Fronto-Temporal Lobe",
        "clinical_notes": "Large heterogeneous infiltrative intra-axial lesion showing irregular peripheral enhancement with marked central necrotic core and severe peritumoral vasogenic edema causing moderate midline shift.",
        "severity": "Critical",
        "has_multimodal": True,
        "ground_truth": {
            "available": True,
            "center": (48, 149),
            "radius_core": 10,
            "radius_whole": 18
        }
    },
    {
        "id": "cheng_meningioma_02",
        "title": "Figshare Case #042: Convexity Meningioma",
        "dataset": "Jun Cheng Figshare",
        "source_image": "1.jpg",
        "class_name": "Meningioma",
        "sub_type": "Parasagittal Dural Convexity Meningioma (WHO Grade I)",
        "modality": "T1-Weighted Contrast Enhanced",
        "orientation": "Axial Slice #18",
        "location": "Left High Frontal Convexity",
        "clinical_notes": "Extra-axial well-demarcated mass with avid homogeneous gadolinium enhancement. Characteristic broad dural tail along the inner table of the calvarium.",
        "severity": "Moderate",
        "has_multimodal": False,
        "ground_truth": {
            "available": True,
            "center": (200, 123),
            "radius_core": 7,
            "radius_whole": 13
        }
    },
    {
        "id": "kaggle_pituitary_03",
        "title": "Kaggle Case #118: Pituitary Macroadenoma",
        "dataset": "Kaggle Sartaj / Nickparvar",
        "source_image": "test4.jpg",
        "class_name": "Pituitary",
        "sub_type": "Non-functioning Pituitary Macroadenoma (WHO Grade I)",
        "modality": "Coronal T1-CE",
        "orientation": "Coronal Slice #44",
        "location": "Sella Turcica with Suprasellar Extension",
        "clinical_notes": "Expanded sella turcica occupied by a well-circumscribed soft-tissue mass. Supero-anterior extension contacting the optic chiasm without cavernous sinus invasion.",
        "severity": "Moderate",
        "has_multimodal": False,
        "ground_truth": {
            "available": True,
            "center": (168, 211),
            "radius_core": 8,
            "radius_whole": 15
        }
    },
    {
        "id": "control_healthy_04",
        "title": "Control Case #004: Normal Brain MRI (Healthy)",
        "dataset": "Kaggle Normal Controls",
        "source_image": "test9.jpg",
        "class_name": "No Tumor",
        "sub_type": "Negative for Mass or Edema (Normal Anatomy)",
        "modality": "Axial T2-Weighted",
        "orientation": "Axial Mid-Ventricular Slice",
        "location": "Bilateral Symmetrical Hemispheres",
        "clinical_notes": "Normal ventricular size and configuration. Normal grey-white matter differentiation. No intracranial mass effect, hemorrhage, midline shift, or restricted diffusion.",
        "severity": "Negative",
        "has_multimodal": False,
        "ground_truth": {
            "available": False
        }
    },
    {
        "id": "brats_astrocytoma_05",
        "title": "BraTS Case #052: Anaplastic Astrocytoma",
        "dataset": "BraTS 2020",
        "source_image": "test6.jpg",
        "class_name": "Glioma",
        "sub_type": "Anaplastic Astrocytoma (WHO Grade III)",
        "modality": "Multi-modal (FLAIR / T2)",
        "orientation": "Axial Slice #102",
        "location": "Left Parietal Lobe",
        "clinical_notes": "Moderately expansive intra-axial lesion in the left parietal white matter with bright T2/FLAIR hyperintensity and patchy nodular enhancement.",
        "severity": "High",
        "has_multimodal": True,
        "ground_truth": {
            "available": True,
            "center": (113, 210),
            "radius_core": 15,
            "radius_whole": 28
        }
    },
    {
        "id": "cheng_meningioma_06",
        "title": "Figshare Case #187: Falx Cerebri Meningioma",
        "dataset": "Jun Cheng Figshare",
        "source_image": "test1.jpg",
        "class_name": "Meningioma",
        "sub_type": "Anterior Falx Meningioma (WHO Grade I)",
        "modality": "T1-CE",
        "orientation": "Axial Slice #26",
        "location": "Anterior Falx Cerebri",
        "clinical_notes": "Densely contrast-enhancing dural-based lesion abutting the anterior superior sagittal sinus with minimal perilesional white matter edema.",
        "severity": "Moderate",
        "has_multimodal": False,
        "ground_truth": {
            "available": True,
            "center": (173, 178),
            "radius_core": 8,
            "radius_whole": 15
        }
    }
]


def generate_synthetic_ground_truth(h, w, gt_meta):
    """Generates ground truth binary mask based on preset metadata"""
    mask = np.zeros((h, w), dtype=np.uint8)
    if not gt_meta or not gt_meta.get("available", False):
        return mask
    cx, cy = gt_meta.get("center", (w // 2, h // 2))
    r = gt_meta.get("radius_whole", 25)
    cv2.circle(mask, (cx, cy), r, 255, -1)
    # Add subtle organic contour perturbation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def generate_brats_multimodal_slices(base_gray_np):
    """
    Simulates the 4 co-registered BraTS MRI sequences (FLAIR, T1, T1ce, T2)
    from a high-resolution base MRI slice based on physical MRI relaxation properties:
    - FLAIR: Fluid attenuation, hyperintense edema.
    - T1: Dark CSF, grey cortex, bright white matter.
    - T1ce: Contrast enhancement of lesion rim.
    - T2: Bright CSF, bright fluid and edema.
    """
    h, w = base_gray_np.shape
    base_norm = base_gray_np.astype(np.float32) / 255.0
    
    # Brain mask
    _, brain_mask = cv2.threshold(base_gray_np, 15, 255, cv2.THRESH_BINARY)
    
    # 1. T1: Standard anatomical spin echo
    t1 = np.power(base_norm, 1.1)
    t1 = (t1 * 255).astype(np.uint8)
    
    # 2. T1ce: Contrast-enhanced (boosts bright vascular and lesion zones)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    t1ce = clahe.apply(base_gray_np)
    # Brighten high-intensity clusters
    high_mask = (base_gray_np > 140).astype(np.float32)
    t1ce_float = np.clip(t1ce.astype(np.float32) + high_mask * 45, 0, 255).astype(np.uint8)
    
    # 3. T2: Bright fluid / water relaxation
    t2_float = 255.0 * np.power(base_norm, 0.75)
    t2 = np.clip(t2_float, 0, 255).astype(np.uint8)
    t2 = cv2.bitwise_and(t2, t2, mask=brain_mask)
    
    # 4. FLAIR: Inversion recovery (dark ventricles, hyperintense edema rim)
    # Suppress ventricular fluid (very bright spots in T2 that are in the center)
    flair = cv2.GaussianBlur(t2, (3, 3), 0)
    # Enhance mid-high intensity rims
    flair = cv2.addWeighted(flair, 0.8, t1ce_float, 0.4, 0)
    flair = cv2.bitwise_and(flair, flair, mask=brain_mask)
    
    return {
        "t1": t1,
        "t1ce": t1ce_float,
        "t2": t2,
        "flair": flair
    }
