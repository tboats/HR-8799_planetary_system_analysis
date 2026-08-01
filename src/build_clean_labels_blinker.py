"""
Generate HR 8799 Blink Comparator with clean, dynamic Frame A and Frame B labels.
Removes static hardcoded descriptions in control labels (<label>Frame A</label>, <label>Frame B</label>).
"""

import os

HTML_PATH = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/docs/hr8799_blink_comparator.html"

def create_clean_labels_blinker():
    os.makedirs(os.path.dirname(HTML_PATH), exist_ok=True)
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HR 8799 Multi-Epoch Astronomical Blink Comparator</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #090d16;
            --bg-secondary: #111827;
            --bg-card: #1f293d;
            --accent-cyan: #38bdf8;
            --accent-emerald: #10b981;
            --accent-purple: #a855f7;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-color: #374151;
            --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --blink-duration: 0.6s;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            font-family: var(--font-main);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        header {
            background: linear-gradient(180deg, #182238 0%, var(--bg-secondary) 100%);
            border-bottom: 1px solid var(--border-color);
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            z-index: 10;
        }

        .logo-title { display: flex; align-items: center; gap: 12px; }

        .logo-badge {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-emerald));
            color: #000;
            font-weight: 700;
            font-size: 0.75rem;
            padding: 4px 8px;
            border-radius: 6px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        h1 { font-size: 1.15rem; font-weight: 600; color: #fff; }

        .header-meta { font-size: 0.85rem; color: var(--text-muted); display: flex; gap: 16px; }
        .header-meta span strong { color: var(--accent-cyan); }

        .workspace {
            display: grid;
            grid-template-columns: 320px 1fr 340px;
            flex: 1;
            overflow: hidden;
        }

        .panel {
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            overflow-y: auto;
        }

        .panel-right { border-right: none; border-left: 1px solid var(--border-color); }

        .section-title {
            font-size: 0.8rem; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 6px;
            display: flex; justify-content: space-between; align-items: center;
        }

        .control-group {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        label { font-size: 0.85rem; font-weight: 600; color: var(--text-main); display: flex; justify-content: space-between; }
        label .val-badge { font-family: var(--font-mono); color: var(--accent-cyan); font-size: 0.8rem; }

        select, input[type="range"] {
            width: 100%;
            background: #0d1322;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 7px 10px;
            border-radius: 6px;
            font-size: 0.85rem;
            outline: none;
        }

        .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .btn-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }

        .btn {
            background: #2a374e;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 9px 10px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex; align-items: center; justify-content: center; gap: 4px;
        }

        .btn:hover { background: #374763; border-color: var(--accent-cyan); color: #fff; }
        .btn.active {
            background: linear-gradient(135deg, #0284c7, #2563eb);
            border-color: var(--accent-cyan);
            color: #fff;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
        }

        .btn-primary {
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            border: none; color: #fff; font-weight: 700;
        }

        .viewport-container {
            position: relative;
            background: #020408;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        .viewer-box-wrapper {
            position: relative;
            width: 650px;
            height: 650px;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.9);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            background: #000;
            cursor: grab;
        }

        .viewer-box-wrapper:active { cursor: grabbing; }

        .viewport-content {
            position: absolute;
            top: 0; left: 0;
            width: 650px; height: 650px;
            transform-origin: center center;
            transition: transform 0.1s ease-out;
        }

        .frame-layer {
            position: absolute;
            top: 0; left: 0;
            width: 650px; height: 650px;
            object-fit: cover;
        }

        #frameLayerA {
            z-index: 2;
            animation: gpuBlinkFrameA var(--blink-duration) infinite step-end;
        }

        #frameLayerB {
            z-index: 1;
        }

        @keyframes gpuBlinkFrameA {
            0%, 49.9% { opacity: 1; visibility: visible; }
            50%, 100% { opacity: 0; visibility: hidden; }
        }

        .paused #frameLayerA { animation-play-state: paused !important; }
        .show-a-only #frameLayerA { animation: none !important; opacity: 1 !important; visibility: visible !important; }
        .show-b-only #frameLayerA { animation: none !important; opacity: 0 !important; visibility: hidden !important; }

        .overlay-svg {
            position: absolute;
            top: 0; left: 0;
            width: 650px; height: 650px;
            pointer-events: none;
            z-index: 5;
        }

        .epoch-overlay {
            position: absolute;
            top: 20px; left: 20px;
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 8px;
            padding: 12px 18px;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            z-index: 10;
        }

        .epoch-tag { color: var(--accent-cyan); font-weight: 700; font-size: 1.05rem; }
        .epoch-details { color: var(--text-muted); font-size: 0.78rem; margin-top: 3px; }

        .blink-indicator {
            width: 12px; height: 12px; border-radius: 50%; background: var(--accent-rose);
            box-shadow: 0 0 8px var(--accent-rose); transition: background 0.1s;
        }
        .blink-indicator.active {
            background: var(--accent-cyan);
            box-shadow: 0 0 12px var(--accent-cyan);
            animation: pulseBlink 0.6s infinite alternate;
        }

        @keyframes pulseBlink {
            0% { transform: scale(0.9); opacity: 0.6; }
            100% { transform: scale(1.2); opacity: 1; }
        }

        .astrometric-table { width: 100%; border-collapse: collapse; font-size: 0.78rem; font-family: var(--font-mono); }
        .astrometric-table th, .astrometric-table td { padding: 6px 8px; text-align: left; border-bottom: 1px solid #26334d; }
        .astrometric-table th { color: var(--text-muted); }
    </style>
</head>
<body>

    <header>
        <div class="logo-title">
            <span class="logo-badge">Direct Optical Suite</span>
            <h1>HR 8799 Multi-Epoch Astronomical Blink Comparator</h1>
        </div>
        <div class="header-meta">
            <span>Target: <strong>HR 8799</strong></span>
            <span>Distance: <strong>39.4 pc</strong></span>
            <span>Orbit Geometry: <strong>i = 28.0°, Ω = 62.0°</strong></span>
        </div>
    </header>

    <div class="workspace">
        <!-- Left Panel -->
        <aside class="panel">
            <div class="section-title">
                <span>Select Observation Pair</span>
                <div id="blinkStatus" class="blink-indicator active"></div>
            </div>

            <div class="control-group">
                <label for="epochA">Frame A</label>
                <select id="epochA">
                    <option value="2008" selected>2008.8 — Discovery (Keck II NIRC2 L')</option>
                    <option value="2015">2015.5 — Archival Baseline (Subaru/GPI)</option>
                    <option value="2022">2022.9 — JWST NIRCam Epoch 1</option>
                    <option value="2024">2024.5 — JWST NIRCam Epoch 2</option>
                    <option value="2026">2026.2 — JWST NIRCam Epoch 3</option>
                </select>

                <label for="epochB">Frame B</label>
                <select id="epochB">
                    <option value="2008">2008.8 — Discovery (Keck II NIRC2 L')</option>
                    <option value="2015">2015.5 — Archival Baseline (Subaru/GPI)</option>
                    <option value="2022">2022.9 — JWST NIRCam Epoch 1</option>
                    <option value="2024">2024.5 — JWST NIRCam Epoch 2</option>
                    <option value="2026" selected>2026.2 — JWST NIRCam Epoch 3</option>
                </select>
            </div>

            <div class="control-group">
                <button id="btnToggleBlink" class="btn btn-primary">
                    <span>⏸ Pause Automatic Blinking</span>
                </button>
                <div class="btn-grid">
                    <button id="btnShowA" class="btn">Show Frame A Only</button>
                    <button id="btnShowB" class="btn">Show Frame B Only</button>
                </div>
            </div>

            <div class="control-group">
                <label for="blinkRate">Blink Speed <span id="blinkRateVal" class="val-badge">300 ms</span></label>
                <input type="range" id="blinkRate" min="50" max="1500" step="50" value="300">
            </div>

            <!-- Zoom & Pan Controls -->
            <div class="section-title">🔍 Zoom & Inspection</div>
            <div class="control-group">
                <label>Zoom Level <span id="zoomVal" class="val-badge">100%</span></label>
                <div class="btn-grid-3">
                    <button id="btnZoomIn" class="btn">➕ Zoom In</button>
                    <button id="btnZoomOut" class="btn">➖ Zoom Out</button>
                    <button id="btnResetZoom" class="btn">🔄 Reset</button>
                </div>
            </div>

            <!-- Astrometric Overlay Controls -->
            <div class="section-title">Astrometric Overlay</div>
            <div class="control-group">
                <button id="btnToggleOrbits" class="btn active">⭕ Toggle 3D Keplerian Tracks</button>
                <button id="btnToggleLabels" class="btn active">🏷️ Toggle Planet Markers</button>
            </div>
        </aside>

        <!-- Center Viewport -->
        <main class="viewport-container">
            <div class="epoch-overlay">
                <div id="epochTitle" class="epoch-tag">BLINKING: 2008.8 (Keck II) ⟷ 2026.2 (JWST)</div>
                <div id="epochSub" class="epoch-details">18-Year Orbital Motion | Scale: 91.15 px/arcsec</div>
            </div>

            <div id="viewerBoxWrapper" class="viewer-box-wrapper">
                <div id="viewportContent" class="viewport-content">
                    <!-- FRAME A AND FRAME B LAYERS (GPU COMPOSITOR BLINKING) -->
                    <img id="frameLayerA" class="frame-layer" src="images/hr8799_epoch_2008.png" alt="Frame A">
                    <img id="frameLayerB" class="frame-layer" src="images/hr8799_epoch_2026.png" alt="Frame B">

                    <!-- ASTROMETRICALLY ACCURATE SVG OVERLAY FOR 3D KEPLERIAN ORBITS -->
                    <svg id="svgOverlay" class="overlay-svg" viewBox="0 0 650 650">
                        <!-- Astronomical Compass (North UP, East LEFT) -->
                        <g transform="translate(60, 600)" stroke="#9ca3af" stroke-width="1.5" fill="none">
                            <line x1="0" y1="0" x2="0" y2="-30" />
                            <polygon points="0,-35 -4,-28 4,-28" fill="#9ca3af" />
                            <text x="0" y="-40" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle" font-family="sans-serif">N</text>
                            <line x1="0" y1="0" x2="-30" y2="0" />
                            <polygon points="-35,0 -28,-4 -28,4" fill="#9ca3af" />
                            <text x="-42" y="4" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle" font-family="sans-serif">E</text>
                        </g>

                        <!-- 3D Keplerian Orbit Ellipses -->
                        <g id="orbitEllipseGroup" transform="translate(325, 325) rotate(-62)">
                            <!-- HR 8799 b (68 AU) -->
                            <ellipse cx="0" cy="0" rx="129.0" ry="146.1" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.85" />
                            <!-- HR 8799 c (43 AU) -->
                            <ellipse cx="0" cy="0" rx="81.6" ry="92.4" fill="none" stroke="#4ade80" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.85" />
                            <!-- HR 8799 d (27 AU) -->
                            <ellipse cx="0" cy="0" rx="51.2" ry="58.0" fill="none" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.85" />
                            <!-- HR 8799 e (16 AU) -->
                            <ellipse cx="0" cy="0" rx="30.4" ry="34.4" fill="none" stroke="#f87171" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.85" />
                        </g>

                        <!-- Dynamic Planet Marker Group -->
                        <g id="planetMarkerGroup"></g>
                    </svg>
                </div>
            </div>
        </main>

        <!-- Right Panel: Astrometry Measurements & Resonances -->
        <aside class="panel panel-right">
            <div class="section-title">📐 Keplerian Astrometric Orbits</div>
            <div class="control-group">
                <table class="astrometric-table">
                    <thead>
                        <tr><th>Planet</th><th>a (AU)</th><th>Sep (arcsec)</th><th>Period</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><span style="color:#f87171;">●</span> <strong>HR 8799 e</strong></td><td>16.0 AU</td><td>0.406"</td><td>~45 yr</td></tr>
                        <tr><td><span style="color:#fbbf24;">●</span> <strong>HR 8799 d</strong></td><td>27.0 AU</td><td>0.685"</td><td>~100 yr</td></tr>
                        <tr><td><span style="color:#4ade80;">●</span> <strong>HR 8799 c</strong></td><td>43.0 AU</td><td>1.091"</td><td>~190 yr</td></tr>
                        <tr><td><span style="color:#38bdf8;">●</span> <strong>HR 8799 b</strong></td><td>68.0 AU</td><td>1.726"</td><td>~460 yr</td></tr>
                    </tbody>
                </table>
            </div>

            <div class="section-title">ℹ️ Orbital Parameters (Wang et al. 2018)</div>
            <div class="control-group" style="font-size: 0.8rem; line-height: 1.5; color: var(--text-muted);">
                <p><strong>Distance (d):</strong> 39.40 ± 0.10 pc (GAIA DR3)</p>
                <p><strong>Inclination (i):</strong> 28.0° ± 2.0°</p>
                <p><strong>Ascending Node (Ω):</strong> 62.0° ± 3.0° East of North</p>
                <p><strong>Resonance Lock:</strong> 1:2:4:8 Laplace Resonance</p>
                <p><strong>Image Scale:</strong> 84.6 px/arcsec (2.148 px/AU)</p>
            </div>
        </aside>
    </div>

    <script>
        const EPOCH_PATHS = {
            '2008': 'images/hr8799_epoch_2008.png',
            '2015': 'images/hr8799_epoch_2015.png',
            '2022': 'images/hr8799_epoch_2022.png',
            '2024': 'images/hr8799_epoch_2024.png',
            '2026': 'images/hr8799_epoch_2026.png'
        };

        const EPOCH_TITLES = {
            '2008': '2008.8 (Keck II)',
            '2015': '2015.5 (Subaru)',
            '2022': '2022.9 (JWST Epoch 1)',
            '2024': '2024.5 (JWST Epoch 2)',
            '2026': '2026.2 (JWST Epoch 3)'
        };

        const PLANET_ORBITS = {
            'b': { a_au: 68.0, P_yr: 460.0, e: 0.02, omega_deg: 110.0, M0_deg: 240.0, color: '#38bdf8' },
            'c': { a_au: 43.0, P_yr: 190.0, e: 0.04, omega_deg: 140.0, M0_deg: 310.0, color: '#4ade80' },
            'd': { a_au: 27.0, P_yr: 100.0, e: 0.10, omega_deg: 85.0,  M0_deg: 180.0, color: '#fbbf24' },
            'e': { a_au: 16.0, P_yr: 45.0,  e: 0.12, omega_deg: 60.0,  M0_deg: 45.0,  color: '#f87171' }
        };

        const PARSEC_DIST = 39.4;
        const PX_PER_AU = 650.0 / (7.68 * PARSEC_DIST); // 2.14808 px/AU
        const INC_RAD = 28.0 * (Math.PI / 180.0);
        const OMEGA_RAD = 62.0 * (Math.PI / 180.0);

        let isBlinking = true;
        let showOrbits = true;
        let showLabels = true;

        let zoomLevel = 1.0;
        let panX = 0;
        let panY = 0;
        let isDragging = false;
        let startX, startY;

        const imgA = document.getElementById('frameLayerA');
        const imgB = document.getElementById('frameLayerB');
        const viewerBoxWrapper = document.getElementById('viewerBoxWrapper');
        const viewportContent = document.getElementById('viewportContent');
        const btnToggleBlink = document.getElementById('btnToggleBlink');

        function updateTransform() {
            viewportContent.style.transform = `translate(${panX}px, ${panY}px) scale(${zoomLevel})`;
            document.getElementById('zoomVal').innerText = `${Math.round(zoomLevel * 100)}%`;
        }

        function solveKepler(M, e) {
            M = M % (2 * Math.PI);
            let E = M;
            for (let i = 0; i < 10; i++) {
                let f = E - e * Math.sin(E) - M;
                let fPrime = 1.0 - e * Math.cos(E);
                E -= f / fPrime;
            }
            return E;
        }

        function getPlanetPixelPos(planetKey, year) {
            const p = PLANET_ORBITS[planetKey];
            const dt = year - 2008.8;
            const meanMotion = (2.0 * Math.PI) / p.P_yr;
            const M = (p.M0_deg * Math.PI / 180.0) + meanMotion * dt;
            const E = solveKepler(M, p.e);

            const sin_v = Math.sqrt(1 - p.e*p.e) * Math.sin(E) / (1 - p.e * Math.cos(E));
            const cos_v = (Math.cos(E) - p.e) / (1 - p.e * Math.cos(E));
            const v = Math.atan2(sin_v, cos_v);

            const r_au = p.a_au * (1.0 - p.e * Math.cos(E));
            const u = v + (p.omega_deg * Math.PI / 180.0);

            const x_sky_au = r_au * (Math.cos(u) * Math.sin(OMEGA_RAD) + Math.sin(u) * Math.cos(OMEGA_RAD) * Math.cos(INC_RAD));
            const y_sky_au = r_au * (Math.cos(u) * Math.cos(OMEGA_RAD) - Math.sin(u) * Math.sin(OMEGA_RAD) * Math.cos(INC_RAD));

            const px = 325.0 - (x_sky_au * PX_PER_AU);
            const py = 325.0 - (y_sky_au * PX_PER_AU);

            return { px, py };
        }

        function updateLayers() {
            const valA = document.getElementById('epochA').value;
            const valB = document.getElementById('epochB').value;

            imgA.src = EPOCH_PATHS[valA];
            imgB.src = EPOCH_PATHS[valB];

            document.getElementById('epochTitle').innerHTML = `BLINKING: ${EPOCH_TITLES[valA]} ⟷ ${EPOCH_TITLES[valB]}`;
            renderPlanetMarkers(2026.2);
        }

        function renderPlanetMarkers(year) {
            const markerGroup = document.getElementById('planetMarkerGroup');
            markerGroup.innerHTML = '';
            markerGroup.style.display = showLabels ? 'block' : 'none';

            if (!showLabels) return;

            for (const [key, p] of Object.entries(PLANET_ORBITS)) {
                const pos = getPlanetPixelPos(key, year);
                
                const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                circle.setAttribute('cx', pos.px);
                circle.setAttribute('cy', pos.py);
                circle.setAttribute('r', '5');
                circle.setAttribute('fill', 'none');
                circle.setAttribute('stroke', p.color);
                circle.setAttribute('stroke-width', '2');
                markerGroup.appendChild(circle);

                const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', pos.px + 10);
                text.setAttribute('y', pos.py - 6);
                text.setAttribute('fill', p.color);
                text.setAttribute('font-size', '11');
                text.setAttribute('font-weight', '700');
                text.setAttribute('font-family', 'sans-serif');
                text.textContent = `HR 8799 ${key}`;
                markerGroup.appendChild(text);
            }
        }

        function setBlinkSpeed(ms) {
            const sec = (ms * 2 / 1000).toFixed(2) + 's';
            document.documentElement.style.setProperty('--blink-duration', sec);
            document.getElementById('blinkRateVal').innerText = `${ms} ms`;
        }

        // ZOOM AND PAN LISTENERS
        document.getElementById('btnZoomIn').addEventListener('click', () => {
            zoomLevel = Math.min(5.0, zoomLevel * 1.25);
            updateTransform();
        });

        document.getElementById('btnZoomOut').addEventListener('click', () => {
            zoomLevel = Math.max(0.5, zoomLevel / 1.25);
            updateTransform();
        });

        document.getElementById('btnResetZoom').addEventListener('click', () => {
            zoomLevel = 1.0;
            panX = 0;
            panY = 0;
            updateTransform();
        });

        viewerBoxWrapper.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY < 0 ? 1.15 : 0.85;
            zoomLevel = Math.min(6.0, Math.max(0.5, zoomLevel * delta));
            updateTransform();
        });

        viewerBoxWrapper.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX - panX;
            startY = e.clientY - panY;
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            panX = e.clientX - startX;
            panY = e.clientY - startY;
            updateTransform();
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
        });

        // CONTROL LISTENERS
        document.getElementById('epochA').addEventListener('change', updateLayers);
        document.getElementById('epochB').addEventListener('change', updateLayers);

        document.getElementById('btnShowA').addEventListener('click', () => {
            isBlinking = false;
            viewerBoxWrapper.className = 'viewer-box-wrapper show-a-only';
            btnToggleBlink.classList.remove('active');
            btnToggleBlink.innerHTML = '<span>⚡ Resume Automatic Blinking</span>';
            document.getElementById('blinkStatus').classList.remove('active');
        });

        document.getElementById('btnShowB').addEventListener('click', () => {
            isBlinking = false;
            viewerBoxWrapper.className = 'viewer-box-wrapper show-b-only';
            btnToggleBlink.classList.remove('active');
            btnToggleBlink.innerHTML = '<span>⚡ Resume Automatic Blinking</span>';
            document.getElementById('blinkStatus').classList.remove('active');
        });

        btnToggleBlink.addEventListener('click', () => {
            isBlinking = !isBlinking;
            if (isBlinking) {
                viewerBoxWrapper.className = 'viewer-box-wrapper';
                btnToggleBlink.classList.add('active');
                btnToggleBlink.innerHTML = '<span>⏸ Pause Automatic Blinking</span>';
                document.getElementById('blinkStatus').classList.add('active');
            } else {
                viewerBoxWrapper.className = 'viewer-box-wrapper paused';
                btnToggleBlink.classList.remove('active');
                btnToggleBlink.innerHTML = '<span>⚡ Resume Automatic Blinking</span>';
                document.getElementById('blinkStatus').classList.remove('active');
            }
        });

        document.getElementById('blinkRate').addEventListener('input', (e) => {
            setBlinkSpeed(e.target.value);
        });

        document.getElementById('btnToggleOrbits').addEventListener('click', (e) => {
            const group = document.getElementById('orbitEllipseGroup');
            showOrbits = !showOrbits;
            e.target.classList.toggle('active', showOrbits);
            group.style.display = showOrbits ? 'block' : 'none';
        });

        document.getElementById('btnToggleLabels').addEventListener('click', (e) => {
            showLabels = !showLabels;
            e.target.classList.toggle('active', showLabels);
            renderPlanetMarkers(2026.2);
        });

        setBlinkSpeed(300);
        updateLayers();
    </script>
</body>
</html>
"""

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Created HR 8799 Blink Comparator with clean Frame A and Frame B labels at: {HTML_PATH}")

if __name__ == "__main__":
    create_clean_labels_blinker()
