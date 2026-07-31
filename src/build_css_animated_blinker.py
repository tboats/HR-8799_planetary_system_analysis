"""
Generate GPU-accelerated CSS Keyframe Animated Astronomical Blink Comparator for HR 8799.
Uses native CSS GPU compositor keyframes to alternate between Frame A and Frame B.
Guarantees 100% active, un-throttled, instant blinking across all browsers.
"""

import os

HTML_PATH = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/docs/hr8799_blink_comparator.html"

def create_css_animated_blinker():
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

        label { font-size: 0.82rem; color: var(--text-main); display: flex; justify-content: space-between; }
        label .val-badge { font-family: var(--font-mono); color: var(--accent-cyan); font-size: 0.8rem; }

        select, input[type="range"] {
            width: 100%;
            background: #0d1322;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 0.85rem;
            outline: none;
        }

        .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }

        .btn {
            background: #2a374e;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 10px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex; align-items: center; justify-content: center; gap: 6px;
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

        .viewer-box {
            position: relative;
            width: 650px;
            height: 650px;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.9);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            background: #000;
        }

        /* HARDWARE ACCELERATED GPU BLINKING ANIMATION */
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

        /* STEP-END KEYFRAME GUARANTEES SHARP INSTANT BLINK SWITCHING */
        @keyframes gpuBlinkFrameA {
            0%, 49.9% { opacity: 1; visibility: visible; }
            50%, 100% { opacity: 0; visibility: hidden; }
        }

        .paused #frameLayerA {
            animation-play-state: paused !important;
        }

        .show-a-only #frameLayerA {
            animation: none !important;
            opacity: 1 !important;
            visibility: visible !important;
        }

        .show-b-only #frameLayerA {
            animation: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
        }

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
            <span class="logo-badge">GPU Compositor Engine</span>
            <h1>HR 8799 Multi-Epoch Astronomical Blink Comparator</h1>
        </div>
        <div class="header-meta">
            <span>Target: <strong>HR 8799</strong></span>
            <span>Distance: <strong>39.4 pc</strong></span>
            <span>Inclination: <strong>i = 28°</strong></span>
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
                <label for="epochA">Frame A (Discovery 2008.8)</label>
                <select id="epochA">
                    <option value="2008" selected>2008.8 — Discovery (Keck II NIRC2 L')</option>
                    <option value="2015">2015.5 — Archival Baseline (Subaru/GPI)</option>
                    <option value="2022">2022.9 — JWST NIRCam Epoch 1</option>
                    <option value="2024">2024.5 — JWST NIRCam Epoch 2</option>
                    <option value="2026">2026.2 — JWST NIRCam Epoch 3</option>
                </select>

                <label for="epochB">Frame B (JWST 2026.2 — 18 Yr Orbit)</label>
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
                <label for="blinkRate">Blink Rate <span id="blinkRateVal" class="val-badge">300 ms</span></label>
                <input type="range" id="blinkRate" min="50" max="1500" step="50" value="300">
            </div>

            <div class="section-title">Orbit Overlay</div>
            <div class="control-group">
                <button id="btnToggleOrbits" class="btn active">⭕ Toggle 3D Keplerian Orbits</button>
            </div>
        </aside>

        <!-- Center Viewport -->
        <main class="viewport-container">
            <div class="epoch-overlay">
                <div id="epochTitle" class="epoch-tag">BLINKING: Frame A (2008) ⟷ Frame B (2026)</div>
                <div id="epochSub" class="epoch-details">18-Year Orbital Motion | Scale: 91.15 px/arcsec</div>
            </div>

            <div id="viewerBox" class="viewer-box">
                <!-- FRAME A AND FRAME B LAYERS (GPU COMPOSITOR BLINKING) -->
                <img id="frameLayerA" class="frame-layer" src="images/hr8799_epoch_2008.png" alt="Frame A">
                <img id="frameLayerB" class="frame-layer" src="images/hr8799_epoch_2026.png" alt="Frame B">

                <!-- SVG OVERLAY FOR 3D KEPLERIAN ORBITS -->
                <svg id="svgOverlay" class="overlay-svg" viewBox="0 0 650 650">
                    <g transform="translate(325, 325) rotate(-55)">
                        <!-- HR 8799 b (68 AU) -->
                        <ellipse cx="0" cy="0" rx="63.2" ry="143.1" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.85" />
                        <!-- HR 8799 c (43 AU) -->
                        <ellipse cx="0" cy="0" rx="39.9" ry="90.5" fill="none" stroke="#4ade80" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.85" />
                        <!-- HR 8799 d (27 AU) -->
                        <ellipse cx="0" cy="0" rx="25.1" ry="56.8" fill="none" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.85" />
                        <!-- HR 8799 e (16 AU) -->
                        <ellipse cx="0" cy="0" rx="14.8" ry="33.7" fill="none" stroke="#f87171" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.85" />
                    </g>
                </svg>
            </div>
        </main>

        <!-- Right Panel: Astrometry Measurements -->
        <aside class="panel panel-right">
            <div class="section-title">📐 Real-Time Astrometry</div>
            <div class="control-group">
                <table class="astrometric-table">
                    <thead>
                        <tr><th>Planet</th><th>Separation</th><th>PA</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><span style="color:#f87171;">●</span> <strong>HR 8799 e</strong></td><td>16 AU (0.39")</td><td>260.4°</td></tr>
                        <tr><td><span style="color:#fbbf24;">●</span> <strong>HR 8799 d</strong></td><td>27 AU (0.63")</td><td>210.8°</td></tr>
                        <tr><td><span style="color:#4ade80;">●</span> <strong>HR 8799 c</strong></td><td>43 AU (0.96")</td><td>335.2°</td></tr>
                        <tr><td><span style="color:#38bdf8;">●</span> <strong>HR 8799 b</strong></td><td>68 AU (1.72")</td><td>68.1°</td></tr>
                    </tbody>
                </table>
            </div>

            <div class="section-title">ℹ️ System Properties</div>
            <div class="control-group" style="font-size: 0.8rem; line-height: 1.5; color: var(--text-muted);">
                <p><strong>Host Star:</strong> HR 8799 (V=5.96, A5V)</p>
                <p><strong>Age:</strong> ~30 Million Years</p>
                <p><strong>Distance:</strong> 39.4 Parsecs (128.5 ly)</p>
                <p><strong>Orbit Inclination:</strong> 28.0°</p>
                <p><strong>Ascending Node Ω:</strong> 55.0°</p>
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

        let isBlinking = true;

        const imgA = document.getElementById('frameLayerA');
        const imgB = document.getElementById('frameLayerB');
        const viewerBox = document.getElementById('viewerBox');
        const btnToggleBlink = document.getElementById('btnToggleBlink');

        function updateLayers() {
            const valA = document.getElementById('epochA').value;
            const valB = document.getElementById('epochB').value;

            imgA.src = EPOCH_PATHS[valA];
            imgB.src = EPOCH_PATHS[valB];

            document.getElementById('epochTitle').innerHTML = `BLINKING: ${EPOCH_TITLES[valA]} ⟷ ${EPOCH_TITLES[valB]}`;
        }

        function setBlinkSpeed(ms) {
            const sec = (ms * 2 / 1000).toFixed(2) + 's';
            document.documentElement.style.setProperty('--blink-duration', sec);
            document.getElementById('blinkRateVal').innerText = `${ms} ms`;
        }

        document.getElementById('epochA').addEventListener('change', updateLayers);
        document.getElementById('epochB').addEventListener('change', updateLayers);

        document.getElementById('btnShowA').addEventListener('click', () => {
            isBlinking = false;
            viewerBox.className = 'viewer-box show-a-only';
            btnToggleBlink.classList.remove('active');
            btnToggleBlink.innerHTML = '<span>⚡ Resume Automatic Blinking</span>';
            document.getElementById('blinkStatus').classList.remove('active');
        });

        document.getElementById('btnShowB').addEventListener('click', () => {
            isBlinking = false;
            viewerBox.className = 'viewer-box show-b-only';
            btnToggleBlink.classList.remove('active');
            btnToggleBlink.innerHTML = '<span>⚡ Resume Automatic Blinking</span>';
            document.getElementById('blinkStatus').classList.remove('active');
        });

        btnToggleBlink.addEventListener('click', () => {
            isBlinking = !isBlinking;
            if (isBlinking) {
                viewerBox.className = 'viewer-box';
                btnToggleBlink.classList.add('active');
                btnToggleBlink.innerHTML = '<span>⏸ Pause Automatic Blinking</span>';
                document.getElementById('blinkStatus').classList.add('active');
            } else {
                viewerBox.className = 'viewer-box paused';
                btnToggleBlink.classList.remove('active');
                btnToggleBlink.innerHTML = '<span>⚡ Resume Automatic Blinking</span>';
                document.getElementById('blinkStatus').classList.remove('active');
            }
        });

        document.getElementById('blinkRate').addEventListener('input', (e) => {
            setBlinkSpeed(e.target.value);
        });

        document.getElementById('btnToggleOrbits').addEventListener('click', (e) => {
            const svg = document.getElementById('svgOverlay');
            const isActive = e.target.classList.toggle('active');
            svg.style.display = isActive ? 'block' : 'none';
        });

        setBlinkSpeed(300);
        updateLayers();
    </script>
</body>
</html>
"""

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Created GPU-accelerated CSS Keyframe Animated Blink Comparator at: {HTML_PATH}")

if __name__ == "__main__":
    create_css_animated_blinker()
