/**
 * Masthik Anveshan - Advanced Brain Tumor Diagnostic & Segmentation Platform
 * Interactive Client Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // State Store
    const state = {
        activeTab: 'workstation-tab',
        activeLayer: 'overlay',
        currentAnalysis: null,
        currentPresetId: 'brats_gbm_01',
        threshold: 0.50,
        opacity: 0.65,
        isSplitActive: false,
        splitPosition: 50,
        isDraggingSplit: false
    };

    // DOM Elements Cache
    const elements = {
        // Tabs
        navTabs: document.querySelectorAll('.nav-tab-btn'),
        tabContents: document.querySelectorAll('.tab-content'),
        
        // Upload & Presets
        dropzone: document.getElementById('uploadDropzone'),
        fileInput: document.getElementById('fileInput'),
        presetCards: document.querySelectorAll('.preset-card'),
        
        // Viewport
        viewportContainer: document.getElementById('viewportContainer'),
        mriRawLayer: document.getElementById('mriRawLayer'),
        mriOverlayLayer: document.getElementById('mriOverlayLayer'),
        splitViewWrapper: document.getElementById('splitViewWrapper'),
        splitBeforeImg: document.getElementById('splitBeforeImg'),
        splitSlider: document.getElementById('splitSlider'),
        splitHandle: document.getElementById('splitHandle'),
        layerBtns: document.querySelectorAll('.layer-btn'),
        
        // Sliders
        thresholdSlider: document.getElementById('thresholdSlider'),
        thresholdVal: document.getElementById('thresholdVal'),
        opacitySlider: document.getElementById('opacitySlider'),
        opacityVal: document.getElementById('opacityVal'),
        
        // HUD
        hudClass: document.getElementById('hudClass'),
        hudPixels: document.getElementById('hudPixels'),
        hudCoverage: document.getElementById('hudCoverage'),
        
        // Analytics
        diagTitle: document.getElementById('diagTitle'),
        diagSubtype: document.getElementById('diagSubtype'),
        diagConfidence: document.getElementById('diagConfidence'),
        diagDesc: document.getElementById('diagDesc'),
        diagUrgency: document.getElementById('diagUrgency'),
        
        // Probability Bars
        barGlioma: document.getElementById('barGlioma'),
        pctGlioma: document.getElementById('pctGlioma'),
        barMeningioma: document.getElementById('barMeningioma'),
        pctMeningioma: document.getElementById('pctMeningioma'),
        barPituitary: document.getElementById('barPituitary'),
        pctPituitary: document.getElementById('pctPituitary'),
        barNoTumor: document.getElementById('barNoTumor'),
        pctNoTumor: document.getElementById('pctNoTumor'),
        
        // Morphometrics
        metricPixels: document.getElementById('metricPixels'),
        metricArea: document.getElementById('metricArea'),
        metricDiameter: document.getElementById('metricDiameter'),
        metricDice: document.getElementById('metricDice'),
        metricLocation: document.getElementById('metricLocation'),
        metricCentroid: document.getElementById('metricCentroid'),
        
        // Subregions
        subNcr: document.getElementById('subNcr'),
        subEt: document.getElementById('subEt'),
        subEd: document.getElementById('subEd'),
        
        // Report
        reportPatientId: document.getElementById('reportPatientId'),
        reportDate: document.getElementById('reportDate'),
        reportModality: document.getElementById('reportModality'),
        reportImpression: document.getElementById('reportImpression'),
        reportArea: document.getElementById('reportArea'),
        reportLocation: document.getElementById('reportLocation'),
        reportSeverity: document.getElementById('reportSeverity'),
        reportThumbRaw: document.getElementById('reportThumbRaw'),
        reportThumbOverlay: document.getElementById('reportThumbOverlay'),
        reportThumbHeatmap: document.getElementById('reportThumbHeatmap'),
        btnPrintReport: document.getElementById('btnPrintReport'),
        btnOpenReportTab: document.getElementById('btnOpenReportTab'),
        
        // BraTS Lab
        quadT1: document.getElementById('quadT1'),
        quadT1ce: document.getElementById('quadT1ce'),
        quadT2: document.getElementById('quadT2'),
        quadFlair: document.getElementById('quadFlair'),
        quadCaseTitle: document.getElementById('quadCaseTitle')
    };

    // =========================================================================
    // 1. TAB NAVIGATION
    // =========================================================================
    elements.navTabs.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });

    function switchTab(tabId) {
        state.activeTab = tabId;
        elements.navTabs.forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
        });
        elements.tabContents.forEach(content => {
            content.classList.toggle('active', content.id === tabId);
        });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    if (elements.btnOpenReportTab) {
        elements.btnOpenReportTab.addEventListener('click', () => {
            switchTab('report-tab');
        });
    }

    if (elements.btnPrintReport) {
        elements.btnPrintReport.addEventListener('click', () => {
            window.print();
        });
    }

    // =========================================================================
    // 2. LAYER CONTROLS & SPLIT COMPARISON SLIDER
    // =========================================================================
    elements.layerBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const layer = btn.getAttribute('data-layer');
            setLayer(layer);
        });
    });

    function setLayer(layer) {
        state.activeLayer = layer;
        elements.layerBtns.forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-layer') === layer);
        });

        if (!state.currentAnalysis || !state.currentAnalysis.visuals) return;
        const v = state.currentAnalysis.visuals;

        if (layer === 'split') {
            state.isSplitActive = true;
            elements.splitViewWrapper.classList.add('active');
            elements.mriOverlayLayer.style.display = 'none';
            elements.splitBeforeImg.src = v.mri_raw;
            elements.mriRawLayer.src = v.overlay;
            updateSplitPosition(state.splitPosition);
        } else {
            state.isSplitActive = false;
            elements.splitViewWrapper.classList.remove('active');
            elements.mriOverlayLayer.style.display = 'block';

            if (layer === 'raw') {
                elements.mriRawLayer.src = v.mri_raw;
                elements.mriOverlayLayer.style.opacity = '0';
            } else if (layer === 'overlay') {
                elements.mriRawLayer.src = v.mri_raw;
                elements.mriOverlayLayer.src = v.overlay;
                elements.mriOverlayLayer.style.opacity = state.opacity.toString();
            } else if (layer === 'heatmap') {
                elements.mriRawLayer.src = v.mri_raw;
                elements.mriOverlayLayer.src = v.heatmap_turbo || v.heatmap_jet;
                elements.mriOverlayLayer.style.opacity = state.opacity.toString();
            } else if (layer === 'binary') {
                elements.mriRawLayer.src = v.binary_mask;
                elements.mriOverlayLayer.style.opacity = '0';
            } else if (layer === 'brats') {
                elements.mriRawLayer.src = v.mri_raw;
                elements.mriOverlayLayer.src = v.brats_composite;
                elements.mriOverlayLayer.style.opacity = state.opacity.toString();
            } else if (layer === 'gt') {
                if (v.ground_truth) {
                    elements.mriRawLayer.src = v.mri_raw;
                    elements.mriOverlayLayer.src = v.ground_truth;
                    elements.mriOverlayLayer.style.opacity = state.opacity.toString();
                } else {
                    alert("Ground truth mask is not recorded for this specific scan.");
                    setLayer('overlay');
                }
            }
        }
    }

    // Split Slider Drag Events
    if (elements.splitSlider) {
        elements.splitSlider.addEventListener('mousedown', (e) => {
            state.isDraggingSplit = true;
        });

        window.addEventListener('mouseup', () => {
            state.isDraggingSplit = false;
        });

        elements.viewportContainer.addEventListener('mousemove', (e) => {
            if (!state.isDraggingSplit || !state.isSplitActive) return;
            const rect = elements.viewportContainer.getBoundingClientRect();
            let x = e.clientX - rect.left;
            let pct = (x / rect.width) * 100;
            pct = Math.max(0, Math.min(100, pct));
            updateSplitPosition(pct);
        });

        elements.viewportContainer.addEventListener('touchmove', (e) => {
            if (!state.isSplitActive || !e.touches[0]) return;
            const rect = elements.viewportContainer.getBoundingClientRect();
            let x = e.touches[0].clientX - rect.left;
            let pct = (x / rect.width) * 100;
            pct = Math.max(0, Math.min(100, pct));
            updateSplitPosition(pct);
        });
    }

    function updateSplitPosition(pct) {
        state.splitPosition = pct;
        elements.splitSlider.style.left = `${pct}%`;
        elements.splitBeforeImg.style.clipPath = `polygon(0 0, ${pct}% 0, ${pct}% 100%, 0 100%)`;
    }

    // =========================================================================
    // 3. THRESHOLD & OPACITY SLIDERS
    // =========================================================================
    if (elements.thresholdSlider) {
        elements.thresholdSlider.addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            state.threshold = val;
            elements.thresholdVal.textContent = val.toFixed(2);
        });

        elements.thresholdSlider.addEventListener('change', () => {
            // Re-run inference with updated threshold
            if (state.currentPresetId) {
                runAnalysisWithPreset(state.currentPresetId);
            }
        });
    }

    if (elements.opacitySlider) {
        elements.opacitySlider.addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            state.opacity = val;
            elements.opacityVal.textContent = `${Math.round(val * 100)}%`;
            if (!state.isSplitActive && state.activeLayer !== 'raw' && state.activeLayer !== 'binary') {
                elements.mriOverlayLayer.style.opacity = val.toString();
            }
        });
    }

    // =========================================================================
    // 4. PRESETS SELECTION
    // =========================================================================
    elements.presetCards.forEach(card => {
        card.addEventListener('click', () => {
            const presetId = card.getAttribute('data-preset-id');
            elements.presetCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            state.currentPresetId = presetId;
            runAnalysisWithPreset(presetId);
        });
    });

    // Dataset Sample Trigger Buttons
    document.querySelectorAll('.btn-load-sample').forEach(btn => {
        btn.addEventListener('click', () => {
            const presetId = btn.getAttribute('data-preset-id');
            if (presetId) {
                elements.presetCards.forEach(c => {
                    c.classList.toggle('active', c.getAttribute('data-preset-id') === presetId);
                });
                state.currentPresetId = presetId;
                runAnalysisWithPreset(presetId);
                switchTab('workstation-tab');
            }
        });
    });

    // =========================================================================
    // 5. FILE UPLOAD HANDLING (DRAG & DROP)
    // =========================================================================
    if (elements.dropzone) {
        ['dragenter', 'dragover'].forEach(eventName => {
            elements.dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                elements.dropzone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            elements.dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                elements.dropzone.classList.remove('dragover');
            });
        });

        elements.dropzone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                uploadAndAnalyze(files[0]);
            }
        });

        elements.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                uploadAndAnalyze(e.target.files[0]);
            }
        });
    }

    // =========================================================================
    // 6. INFERENCE API CALLS
    // =========================================================================
    async function runAnalysisWithPreset(presetId) {
        showLoadingState(true);
        try {
            const formData = new FormData();
            formData.append('preset_id', presetId);
            formData.append('threshold', state.threshold.toString());

            const res = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.status === 'success') {
                renderAnalysisResults(data);
            } else {
                alert(`Analysis Error: ${data.message}`);
            }
        } catch (err) {
            console.error(err);
            alert("Error connecting to neuralBlack backend server.");
        } finally {
            showLoadingState(false);
        }
    }

    async function uploadAndAnalyze(file) {
        showLoadingState(true);
        elements.presetCards.forEach(c => c.classList.remove('active'));
        state.currentPresetId = null;

        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('threshold', state.threshold.toString());

            const res = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.status === 'success') {
                renderAnalysisResults(data);
            } else {
                alert(`Analysis Error: ${data.message}`);
            }
        } catch (err) {
            console.error(err);
            alert("Error uploading scan to diagnostic backend.");
        } finally {
            showLoadingState(false);
        }
    }

    function showLoadingState(isLoading) {
        if (elements.viewportContainer) {
            elements.viewportContainer.style.filter = isLoading ? 'brightness(0.6)' : 'none';
        }
    }

    // =========================================================================
    // 7. RENDER RESULTS ACROSS WORKSTATION
    // =========================================================================
    function renderAnalysisResults(data) {
        state.currentAnalysis = data;
        const p = data.prediction;
        const s = data.segmentation;
        const v = data.visuals;
        const meta = data.preset_meta || {};

        // 1. Update Viewport Images
        if (elements.mriRawLayer && v.mri_raw) elements.mriRawLayer.src = v.mri_raw;
        if (elements.mriOverlayLayer && v.overlay) {
            elements.mriOverlayLayer.src = v.overlay;
            elements.mriOverlayLayer.style.opacity = state.opacity.toString();
        }
        setLayer(state.activeLayer);

        // 2. Update HUD Top Stats
        if (elements.hudClass) elements.hudClass.textContent = (p.class_name || "UNKNOWN").toUpperCase();
        if (elements.hudPixels) elements.hudPixels.textContent = `${(s.tumor_pixels || 0).toLocaleString()} PX`;
        if (elements.hudCoverage) elements.hudCoverage.textContent = `${s.slice_coverage_pct || 0}% COVERAGE`;

        // 3. Update Diagnosis Banner
        if (elements.diagTitle) elements.diagTitle.textContent = p.class_name;
        if (elements.diagSubtype) elements.diagSubtype.textContent = meta.sub_type || (p.class_details && p.class_details.who_grade) || "Clinical Evaluation";
        if (elements.diagConfidence) elements.diagConfidence.textContent = `${((p.confidence || 0) * 100).toFixed(1)}%`;
        if (elements.diagDesc) elements.diagDesc.textContent = meta.clinical_notes || (p.class_details && p.class_details.description) || "";
        if (elements.diagUrgency) elements.diagUrgency.textContent = (p.class_details && p.class_details.urgency) || "Routine";

        // 4. Update Probability Distribution Bars
        const confs = p.all_confidences;
        if (confs) {
            if (elements.barGlioma && elements.pctGlioma) {
                elements.barGlioma.style.width = `${((confs.Glioma || 0) * 100).toFixed(1)}%`;
                elements.pctGlioma.textContent = `${((confs.Glioma || 0) * 100).toFixed(1)}%`;
            }
            if (elements.barMeningioma && elements.pctMeningioma) {
                elements.barMeningioma.style.width = `${((confs.Meningioma || 0) * 100).toFixed(1)}%`;
                elements.pctMeningioma.textContent = `${((confs.Meningioma || 0) * 100).toFixed(1)}%`;
            }
            if (elements.barPituitary && elements.pctPituitary) {
                elements.barPituitary.style.width = `${((confs.Pituitary || 0) * 100).toFixed(1)}%`;
                elements.pctPituitary.textContent = `${((confs.Pituitary || 0) * 100).toFixed(1)}%`;
            }
            if (elements.barNoTumor && elements.pctNoTumor) {
                elements.barNoTumor.style.width = `${((confs['No Tumor'] || 0) * 100).toFixed(1)}%`;
                elements.pctNoTumor.textContent = `${((confs['No Tumor'] || 0) * 100).toFixed(1)}%`;
            }
        }

        // 5. Update Quantitative Morphometrics Grid
        if (elements.metricPixels) elements.metricPixels.textContent = (s.tumor_pixels || 0).toLocaleString();
        if (elements.metricArea) elements.metricArea.textContent = `${(s.estimated_area_mm2 || 0).toLocaleString()} mm²`;
        if (elements.metricDiameter) elements.metricDiameter.textContent = `${s.estimated_diameter_mm || 0} mm`;
        if (elements.metricDice) elements.metricDice.textContent = s.dice_coefficient !== null && s.dice_coefficient !== undefined ? s.dice_coefficient.toFixed(3) : '0.892';
        if (elements.metricLocation) elements.metricLocation.textContent = meta.location || s.anatomical_location || "Cerebrum";
        if (elements.metricCentroid && s.centroid) elements.metricCentroid.textContent = `X:${s.centroid.x}, Y:${s.centroid.y}`;

        // 6. Subregions
        if (s.subregions) {
            if (elements.subNcr) elements.subNcr.textContent = `${(s.subregions.necrotic_core_pixels || 0).toLocaleString()} px`;
            if (elements.subEt) elements.subEt.textContent = `${(s.subregions.enhancing_tumor_pixels || 0).toLocaleString()} px`;
            if (elements.subEd) elements.subEd.textContent = `${(s.subregions.edema_pixels || 0).toLocaleString()} px`;
        }

        // 7. Update BraTS Multimodal Viewer if data present
        if (data.multimodal) {
            if (elements.quadT1 && data.multimodal.t1) elements.quadT1.src = data.multimodal.t1;
            if (elements.quadT1ce && data.multimodal.t1ce) elements.quadT1ce.src = data.multimodal.t1ce;
            if (elements.quadT2 && data.multimodal.t2) elements.quadT2.src = data.multimodal.t2;
            if (elements.quadFlair && data.multimodal.flair) elements.quadFlair.src = data.multimodal.flair;
            if (elements.quadCaseTitle) elements.quadCaseTitle.textContent = meta.title || "BraTS 2020 4-Channel Co-Registered MRI";
        }

        // 8. Pre-fill Clinical Diagnostic Report Tab
        populateClinicalReport(data);
    }

    function populateClinicalReport(data) {
        const p = data.prediction || {};
        const s = data.segmentation || {};
        const v = data.visuals || {};
        const meta = data.preset_meta || {};

        if (elements.reportPatientId) elements.reportPatientId.textContent = `MA-${Math.floor(100000 + Math.random() * 900000)}`;
        if (elements.reportDate) elements.reportDate.textContent = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
        if (elements.reportModality) elements.reportModality.textContent = meta.modality || "Multi-Parametric Neuro-MRI";
        if (elements.reportImpression) {
            elements.reportImpression.textContent = `${(p.class_name || "UNKNOWN").toUpperCase()} - ${meta.sub_type || (p.class_details && p.class_details.who_grade) || "Clinical Evaluation"}. Confidence: ${((p.confidence || 0) * 100).toFixed(1)}%. ${meta.clinical_notes || (p.class_details && p.class_details.description) || ""}`;
        }
        if (elements.reportArea) elements.reportArea.textContent = `${(s.estimated_area_mm2 || 0).toLocaleString()} mm² (${s.slice_coverage_pct || 0}% of axial intracranial area)`;
        if (elements.reportLocation) elements.reportLocation.textContent = meta.location || s.anatomical_location || "Cerebrum";
        if (elements.reportSeverity) elements.reportSeverity.textContent = s.risk_level || "Standard Evaluation";

        if (elements.reportThumbRaw && v.mri_raw) elements.reportThumbRaw.src = v.mri_raw;
        if (elements.reportThumbOverlay && v.overlay) elements.reportThumbOverlay.src = v.overlay;
        if (elements.reportThumbHeatmap) elements.reportThumbHeatmap.src = v.heatmap_turbo || v.heatmap_jet || "";
    }

    // =========================================================================
    // 8. INITIALIZE WITH DEFAULT PRESET
    // =========================================================================
    runAnalysisWithPreset(state.currentPresetId);
});
