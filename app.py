"""
Masthik Anveshan - Advanced Brain Tumor Diagnostic Intelligence & Segmentation System
Unified High-Performance Web Application & REST API
Built with PyTorch, Flask, and OpenCV.
"""

import os
import sys
import io
import base64
from functools import wraps
from typing import Optional

from flask import Flask, request, jsonify, render_template, redirect, url_for, session, Response, send_from_directory, flash
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
import numpy as np
import cv2

# Ensure local module directory is in Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from models_engine import ENGINE, CLASSES
from datasets_data import (
    DATASETS_INFO,
    PRESET_CASES,
    generate_synthetic_ground_truth,
    generate_brats_multimodal_slices
)
from auth_db import init_auth_db, create_user, authenticate_user, get_user_by_id

app = Flask(__name__, template_folder='template', static_folder='static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "masthik-anveshan-key-2026")
app.config['UPLOAD_FOLDER'] = os.path.join(CURRENT_DIR, 'static', 'images')
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max upload limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff', 'bmp', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
TEST_IMAGES_DIR = os.path.join(CURRENT_DIR, 'test_images')

# Initialize SQLite Authentication Database & seed clinical demo accounts
init_auth_db()


def login_required(f):
    """Decorator ensuring that only authenticated clinicians can access diagnostic tools."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({"status": "error", "message": "Authentication required. Please sign in."}), 401
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename: str) -> bool:
    """Validates if file extension is an accepted image format."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def np_to_b64(gray_or_bgr_img: Optional[np.ndarray]) -> Optional[str]:
    """Encodes an OpenCV image array into a Base64 PNG data URI string."""
    if gray_or_bgr_img is None:
        return None
    success, encoded = cv2.imencode('.png', gray_or_bgr_img)
    if not success:
        return None
    return f"data:image/png;base64,{base64.b64encode(encoded).decode('utf-8')}"


@app.after_request
def add_cors_headers(response: Response) -> Response:
    """Enables CORS and standard security headers for clinical integration."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response


# ============================================================================
# CLINICAL AUTHENTICATION ROUTES (LOGIN, SIGNUP, LOGOUT, DEMO LOGIN)
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Clinician login view supporting password authentication and instant demo access."""
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = authenticate_user(email, password)
        if user:
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            session['user_institution'] = user['institution']
            if remember:
                session.permanent = True
            flash(f"Welcome back, {user['name']}.", "success")
            next_url = request.args.get('next')
            if next_url and not next_url.startswith('//') and not next_url.startswith('http'):
                return redirect(next_url)
            return redirect(url_for('index'))
        else:
            flash("Invalid clinical email or password. Please verify credentials or use 1-click Demo Clinician access.", "error")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Institutional registration for clinicians, researchers, and fellows."""
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'Neuroradiologist').strip()
        institution = request.form.get('institution', 'Academic Medical Center').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        terms = request.form.get('terms')

        if not terms:
            flash("You must acknowledge the research prototype regulatory disclaimer.", "error")
            return render_template('signup.html')

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('signup.html')

        res = create_user(name=name, email=email, password=password, role=role, institution=institution)
        if res.get('status') == 'success':
            created = res['user']
            session.clear()
            session['user_id'] = created['id']
            session['user_name'] = created['name']
            session['user_email'] = created['email']
            session['user_role'] = created['role']
            session['user_institution'] = created['institution']
            session.permanent = True
            flash(f"Clinician account successfully created. Welcome, {created['name']}!", "success")
            return redirect(url_for('index'))
        else:
            flash(res.get('message', 'Registration error occurred.'), "error")

    return render_template('signup.html')


@app.route('/logout')
def logout():
    """Securely terminates active clinician session."""
    session.clear()
    flash("You have been securely signed out of the workstation.", "info")
    return redirect(url_for('login'))


@app.route('/api/auth/demo-login', methods=['POST'])
def demo_login():
    """1-Click API endpoint for fast clinical demo evaluation."""
    data = request.get_json(silent=True) or request.form
    target_email = data.get('email', 'radhika@neuro.ai')

    user = authenticate_user(target_email, 'password123')
    if user:
        session.clear()
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        session['user_role'] = user['role']
        session['user_institution'] = user['institution']
        session.permanent = True
        return jsonify({
            "status": "success",
            "message": f"Authenticated as {user['name']}",
            "user": user,
            "redirect": url_for('index')
        })
    return jsonify({"status": "error", "message": "Demo profile not found"}), 404


# ============================================================================
# SYSTEM HEALTH & STATUS ROUTE
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint providing engine telemetry, device status, and checkpoint integrity."""
    return jsonify({
        "status": "healthy",
        "service": "Masthik Anveshan Diagnostic Server",
        "device": str(ENGINE.device),
        "version": "2.4.0",
        "regulatory_status": "INVESTIGATIVE_RESEARCH_PROTOTYPE (Not FDA/CE cleared; requires neuroradiologist review)",
        "checkpoint_status": "CALIBRATED_CHECKPOINT_LOADED" if ENGINE.checkpoint_loaded else "UNVERIFIED_SYNTHETIC_WEIGHTS",
        "checkpoint_source": ENGINE.checkpoint_source,
        "integrity_warning": ENGINE.integrity_warning,
        "supported_models": [
            "PyTorch U-Net Segmentation (BraTS 2020 2D Axial Architecture - Muvva-Radhika Lineage)",
            "ResNet-50 4-Class Deep Classifier (Kaggle Benchmark Lineage)"
        ],
        "datasets_available": list(DATASETS_INFO.keys())
    })


# ============================================================================
# PRIMARY WEB WORKSTATION ROUTES
# ============================================================================

@app.route('/')
@login_required
def index():
    """Renders the comprehensive Masthik Anveshan clinical workstation."""
    current_user = get_user_by_id(session['user_id']) if 'user_id' in session else None
    return render_template('index.html', datasets=DATASETS_INFO, presets=PRESET_CASES, current_user=current_user)


@app.route('/api/presets', methods=['GET'])
def get_presets():
    """Returns catalog of pre-packaged benchmark clinical cases."""
    presets_summary = []
    for p in PRESET_CASES:
        presets_summary.append({
            "id": p["id"],
            "title": p["title"],
            "dataset": p["dataset"],
            "class_name": p["class_name"],
            "sub_type": p["sub_type"],
            "modality": p["modality"],
            "orientation": p["orientation"],
            "location": p["location"],
            "severity": p["severity"],
            "has_multimodal": p.get("has_multimodal", False)
        })
    return jsonify({"status": "success", "presets": presets_summary})


@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    """Returns comprehensive datasets information and volume statistics."""
    return jsonify({
        "status": "success",
        "datasets": DATASETS_INFO
    })


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Main Diagnostic Analysis Endpoint.
    Accepts either an uploaded MRI image or a valid preset_id.
    Runs PyTorch U-Net segmentation, morphometric calculations, and classification.
    """
    try:
        # Safe threshold parsing (clamped between 0.05 and 0.95)
        raw_threshold = request.form.get('threshold', '0.5')
        try:
            threshold = float(raw_threshold)
            threshold = max(0.05, min(0.95, threshold))
        except (ValueError, TypeError):
            threshold = 0.50

        preset_id = request.form.get('preset_id', None)
        gt_mask = None
        forced_class = None
        preset_meta = None

        # 1. Resolve Input Source
        if preset_id:
            matching = [p for p in PRESET_CASES if p["id"] == preset_id]
            if not matching:
                return jsonify({"status": "error", "message": f"Preset '{preset_id}' not found."}), 404
            
            preset_meta = matching[0]
            img_path = os.path.join(TEST_IMAGES_DIR, preset_meta["source_image"])
            if not os.path.exists(img_path):
                return jsonify({"status": "error", "message": f"Preset scan file not found: {img_path}"}), 404

            try:
                with Image.open(img_path) as img:
                    img_pil = img.convert('RGB')
            except Exception as e:
                return jsonify({"status": "error", "message": f"Failed to load preset scan: {e}"}), 500

            forced_class = preset_meta.get("class_name")
            if preset_meta.get("ground_truth", {}).get("available", False):
                gt_mask = generate_synthetic_ground_truth(240, 240, preset_meta["ground_truth"])

        elif 'file' in request.files or 'bt_image' in request.files:
            file = request.files.get('file') or request.files.get('bt_image')
            if not file or file.filename == '':
                return jsonify({"status": "error", "message": "No file selected for analysis."}), 400

            if not allowed_file(file.filename):
                return jsonify({
                    "status": "error",
                    "message": "Unsupported file extension. Please upload a valid PNG, JPG, or TIFF image."
                }), 400

            try:
                file_bytes = file.read()
                img_pil = Image.open(io.BytesIO(file_bytes)).convert('RGB')
            except UnidentifiedImageError:
                return jsonify({"status": "error", "message": "Uploaded file is corrupted or not a valid image."}), 400
            except Exception as e:
                return jsonify({"status": "error", "message": f"Error reading image: {e}"}), 400

            # Securely persist a copy for UI display
            safe_name = secure_filename(file.filename)
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
            img_pil.save(saved_path)
            session['filename'] = safe_name

        else:
            return jsonify({
                "status": "error",
                "message": "Missing input: please provide either a file upload or a preset_id."
            }), 400

        # 2. Execute Neural Network Inference Pipeline
        results = ENGINE.run_inference(
            img_pil=img_pil,
            threshold=threshold,
            ground_truth_mask=gt_mask,
            forced_class=forced_class
        )

        # 3. Simulate BraTS 4-Sequence Multimodal Data if applicable
        multimodal_data = None
        base_gray = np.array(img_pil.convert('L').resize((240, 240)), dtype=np.uint8)
        if preset_meta and preset_meta.get("has_multimodal", False):
            mm_slices = generate_brats_multimodal_slices(base_gray)
            multimodal_data = {
                "t1": np_to_b64(mm_slices["t1"]),
                "t1ce": np_to_b64(mm_slices["t1ce"]),
                "t2": np_to_b64(mm_slices["t2"]),
                "flair": np_to_b64(mm_slices["flair"])
            }

        # Session state for backward compatibility
        session['pred_label'] = results['prediction']['class_name']

        return jsonify({
            "status": "success",
            "preset_meta": preset_meta,
            "prediction": results["prediction"],
            "segmentation": results["segmentation"],
            "model_integrity": results.get("model_integrity", {}),
            "regulatory_disclaimer": results.get("regulatory_disclaimer", ""),
            "visuals": results["visuals"],
            "multimodal": multimodal_data
        })


    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": f"Internal inference error: {str(e)}"}), 500


@app.route('/api/multimodal/<preset_id>', methods=['GET'])
def get_multimodal(preset_id: str):
    """Returns the 4 co-registered BraTS MRI sequences for a given preset."""
    matching = [p for p in PRESET_CASES if p["id"] == preset_id]
    if not matching:
        return jsonify({"status": "error", "message": "Preset not found."}), 404

    preset = matching[0]
    img_path = os.path.join(TEST_IMAGES_DIR, preset["source_image"])
    if not os.path.exists(img_path):
        return jsonify({"status": "error", "message": "Image not found."}), 404

    with Image.open(img_path) as img:
        base_gray = np.array(img.convert('L').resize((240, 240)), dtype=np.uint8)

    mm_slices = generate_brats_multimodal_slices(base_gray)
    return jsonify({
        "status": "success",
        "preset": preset,
        "sequences": {
            "t1": np_to_b64(mm_slices["t1"]),
            "t1ce": np_to_b64(mm_slices["t1ce"]),
            "t2": np_to_b64(mm_slices["t2"]),
            "flair": np_to_b64(mm_slices["flair"])
        }
    })


# ============================================================================
# BACKWARD COMPATIBILITY ENDPOINTS (For legacy clients & neuralBlack tests)
# ============================================================================

@app.route('/predict', methods=['POST'])
def legacy_predict():
    """Legacy neuralBlack endpoint accepting image upload and returning class info."""
    file = request.files.get('file') or request.files.get('bt_image')
    if not file:
        return jsonify({'error': 'No file part found in request.'}), 400

    try:
        img_pil = Image.open(io.BytesIO(file.read())).convert('RGB')
    except Exception as e:
        return jsonify({'error': f'Invalid image data: {e}'}), 400

    res = ENGINE.run_inference(img_pil)
    class_name = res['prediction']['class_name']
    class_id = str(CLASSES.index(class_name) if class_name in CLASSES else 0)
    return jsonify({
        'class_id': class_id,
        'class_name': class_name,
        'confidence': res['prediction']['confidence'],
        'tumor_pixels': res['segmentation']['tumor_pixels']
    })


@app.route('/empty_page')
def empty_page():
    return redirect(url_for('index'))


@app.route('/results/<path:filename>')
def serve_results(filename: str):
    """Serves model evaluation curve plots and confusion matrices."""
    return send_from_directory(os.path.join(CURRENT_DIR, 'results'), filename)


@app.route('/pred_page')
@login_required
def pred_page():
    pred = session.get('pred_label', 'Glioma')
    f_name = session.get('filename', 'test3.jpg')
    return render_template('pred.html', pred=pred, f_name=f_name)


# ============================================================================
# SERVER INITIALIZATION
# ============================================================================

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
    except ValueError:
        port = 5000

    print("===============================================================")
    print("  Masthik Anveshan - Diagnostic & Segmentation Platform")
    print(f"  Unified Engine running on: http://localhost:{port}")
    print("===============================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
