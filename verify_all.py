"""
Masthik Anveshan - Comprehensive System Verification Suite
Validates all endpoints, models, presets, file uploads, metrics, and static assets.
"""

import time
import requests
import os

time.sleep(1)
base_url = 'http://127.0.0.1:5000'

def test(url, method='GET', **kwargs):
    try:
        if method == 'GET':
            r = requests.get(url, **kwargs)
        else:
            r = requests.post(url, **kwargs)
        status = r.status_code
        ok = (status == 200)
        print(f"{method} {url:<50} -> {status} (OK: {ok})")
        return r
    except Exception as e:
        print(f"{method} {url:<50} -> EXCEPTION: {e}")
        return None

print("=== MASTHIK ANVESHAN END-TO-END VERIFICATION ===\n")

# 1. Health check
r = test(f"{base_url}/api/health")
assert r and r.json()['status'] == 'healthy', 'Health check failed'
print(f"  Health Payload: {r.json()}\n")

# 2. Main Workstation
r = test(f"{base_url}/")
assert r and '<!DOCTYPE html>' in r.text, 'Workstation root failed'

# 3. Presets catalog
r = test(f"{base_url}/api/presets")
presets = r.json()['presets']
print(f"  Found {len(presets)} registered presets.")

# 4. Datasets catalog
r = test(f"{base_url}/api/datasets")
datasets = r.json()['datasets']
print(f"  Found {len(datasets)} registered datasets: {list(datasets.keys())}\n")

# 5. Multimodal endpoint
r = test(f"{base_url}/api/multimodal/brats_gbm_01")
assert r and 'sequences' in r.json(), 'Multimodal endpoint failed'

# 6. Analyze all 6 presets
print("--- Verifying Inference on All Presets ---")
for p in presets:
    pid = p['id']
    resp = test(f"{base_url}/api/analyze", method='POST', data={'preset_id': pid, 'threshold': 0.5})
    assert resp and resp.status_code == 200, f"Failed on preset {pid}"
    data = resp.json()
    assert data['status'] == 'success', f"Preset {pid} failed status"
    seg = data['segmentation']
    cls_diag = data['prediction']
    conf = cls_diag['confidence'] * 100
    pixels = seg['tumor_pixels']
    dice = seg.get('dice_score', 'N/A')
    print(f"  -> Preset {pid}: Class={cls_diag['class_name']} ({conf:.1f}%) | Lesion={pixels}px | Dice={dice}")

# 7. File Upload analysis
print("\n--- Verifying Direct File Upload ---")
sample_file = os.path.join(os.path.dirname(__file__), 'test_images', '1.jpg')
with open(sample_file, 'rb') as fp:
    resp = test(f"{base_url}/api/analyze", method='POST', files={'file': ('1.jpg', fp, 'image/jpeg')}, data={'threshold': 0.5})
    assert resp.status_code == 200
    diag = resp.json()['prediction']['class_name']
    print(f"  Direct file upload analysis returned 200 OK with prediction: {diag}")

# 8. Legacy /predict endpoint
with open(sample_file, 'rb') as fp:
    resp = test(f"{base_url}/predict", method='POST', files={'file': ('1.jpg', fp, 'image/jpeg')})
    assert resp.status_code == 200
    print(f"  Legacy /predict endpoint returned 200 OK: {resp.json()}")

# 9. Results assets
print("\n--- Verifying Evaluation Assets ---")
for asset in ['loss_metrics.png', 'accuracy_metrics.png', 'cm.png']:
    resp = test(f"{base_url}/results/{asset}")
    assert resp.status_code == 200

# 10. Static assets
print("\n--- Verifying Static Frontend Assets ---")
for asset in ['css/main.css', 'js/app.js']:
    resp = test(f"{base_url}/static/{asset}")
    assert resp.status_code == 200

print("\n>>> ALL 10 TEST SUITES COMPLETED WITH 100% SUCCESS! <<<")
