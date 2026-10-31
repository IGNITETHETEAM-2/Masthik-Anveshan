"""
Masthik Anveshan - CLI Test & Diagnostic Verification Script
Evaluates brain MRI scans for both Classification and U-Net Segmentation.
Supports CLI arguments: python test.py [path/to/image.jpg]
"""

import os
import sys
# pyrefly: ignore[missing-import]
import torch
# pyrefly: ignore[missing-import]
import torch.nn as nn
# pyrefly: ignore[missing-import]
from torchvision import transforms, models
from PIL import Image

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure local module directory is in Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

try:
    from models_engine import ENGINE
    HAS_ENGINE = True
except ImportError:
    HAS_ENGINE = False


def run_diagnostic_test(image_path, threshold=0.5):
    """Executes full diagnostic segmentation and classification on the target image."""
    normalized_path = os.path.abspath(image_path)
    if not os.path.exists(normalized_path):
        print(f"\n[Error] File does not exist: {image_path}\n")
        return False

    print("=" * 65)
    print("  MASTHIK ANVESHAN - MRI DIAGNOSTIC ANALYSIS")
    print(f"  Target Scan: {os.path.basename(normalized_path)}")
    print("=" * 65)

    try:
        with Image.open(normalized_path) as img:
            img_pil = img.convert('RGB')
    except Exception as e:
        print(f"[Error] Failed to open image: {e}")
        return False

    if HAS_ENGINE:
        # Full high-precision segmentation + classification via ENGINE
        results = ENGINE.run_inference(img_pil, threshold=threshold)
        p = results['prediction']
        s = results['segmentation']
        c_detail = p['class_details']

        print("\n[1] CLASSIFICATION DIAGNOSIS:")
        print(f"    * Primary Finding : {p['class_name']}")
        print(f"    * Confidence Score: {p['confidence'] * 100:.1f}%")
        print(f"    * Classification  : {c_detail['who_grade']}")
        print(f"    * Clinical Urgency: {c_detail['urgency']}")

        print("\n[2] CLASS PROBABILITY DISTRIBUTION:")
        for cls, prob in p['all_confidences'].items():
            bar_len = int(prob * 30)
            bar = "#" * bar_len + "-" * (30 - bar_len)
            print(f"    * {cls:<12}: [{bar}] {prob * 100:5.1f}%")

        print("\n[3] U-NET LESION SEGMENTATION:")
        print(f"    * Threshold Used  : {s['threshold']:.2f}")
        print(f"    * Tumor Pixels    : {s['tumor_pixels']:,} px")
        print(f"    * Estimated Area  : {s['estimated_area_mm2']:.1f} mm²")
        print(f"    * Max Diameter    : {s['estimated_diameter_mm']:.1f} mm")
        print(f"    * Slice Coverage  : {s['slice_coverage_pct']:.2f}%")
        print(f"    * Anatomical Lobe : {s['anatomical_location']}")
        print(f"    * Centroid Coord  : X:{s['centroid']['x']}, Y:{s['centroid']['y']}")
        print(f"    * Risk Level      : {s['risk_level']}")

        if s['subregions']['necrotic_core_pixels'] > 0:
            print("\n[4] BRATS SUB-REGION DECOMPOSITION:")
            print(f"    * Necrotic Core (NCR)   : {s['subregions']['necrotic_core_pixels']:,} px")
            print(f"    * Enhancing Tumor (ET)  : {s['subregions']['enhancing_tumor_pixels']:,} px")
            print(f"    * Peritumoral Edema (ED): {s['subregions']['edema_pixels']:,} px")

    else:
        # Fallback to direct PyTorch ResNet inference if standalone
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"Engine running on fallback mode ({device})...")


        resnet = models.resnet50(weights=None)
        n_inputs = resnet.fc.in_features
        resnet.fc = nn.Sequential(
            nn.Linear(n_inputs, 2048),
            nn.SELU(),
            nn.Dropout(p=0.4),
            nn.Linear(2048, 2048),
            nn.SELU(),
            nn.Dropout(p=0.4),
            nn.Linear(2048, 4),
            nn.LogSigmoid()
        )

        model_path = os.path.join(CURRENT_DIR, 'models', 'bt_resnet50_model.pt')
        if os.path.exists(model_path):
            resnet.load_state_dict(torch.load(model_path, map_location=device, weights_only=False))
        resnet.to(device)
        resnet.eval()

        transform = transforms.Compose([
            transforms.Resize((512, 512)),
            transforms.ToTensor()
        ])
        tensor = transform(img_pil).unsqueeze(0).to(device)

        labels = ['No Tumor', 'Meningioma', 'Glioma', 'Pituitary']
        with torch.no_grad():
            output = resnet(tensor)
            pred_idx = torch.argmax(output, dim=1).item()
            print(f"\nPrediction: {labels[pred_idx]}")

    print("\n" + "=" * 65)
    return True


if __name__ == '__main__':
    # Accept image path from CLI argument or prompt interactively
    if len(sys.argv) > 1:
        target_image = sys.argv[1]
    else:
        default_sample = os.path.join(CURRENT_DIR, 'test_images', '1.jpg')
        user_input = input(f"Enter path to MRI image [Default: {default_sample}]: ").strip()
        target_image = user_input if user_input else default_sample

    run_diagnostic_test(target_image)