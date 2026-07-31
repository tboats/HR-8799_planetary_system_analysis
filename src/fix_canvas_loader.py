"""
Fix async canvas image loading bug in HR 8799 Blink Comparator tool.
Adds a requestAnimationFrame auto-retry loop so that images render immediately upon loading.
Fixes black screen issues on initial page load across all browsers.
"""

import os

HTML_PATH = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/docs/hr8799_blink_comparator.html"

def fix_canvas_loader():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace render() image drawing block with robust requestAnimationFrame retry
    old_block = """            // DRAW IMAGE
            if (opacityBlend > 0 && opacityBlend < 100) {
                const imgA = loadedImages[currentEpochA];
                const imgB = loadedImages[currentEpochB];
                if (imgA && imgA.complete) {
                    ctx.globalAlpha = (100 - opacityBlend) / 100;
                    ctx.drawImage(imgA, centerX - 350, centerY - 350, 700, 700);
                }
                if (imgB && imgB.complete) {
                    ctx.globalAlpha = opacityBlend / 100;
                    ctx.drawImage(imgB, centerX - 350, centerY - 350, 700, 700);
                }
                ctx.globalAlpha = 1.0;
            } else {
                const img = loadedImages[activeEpochKey];
                if (img && img.complete) {
                    ctx.drawImage(img, centerX - 350, centerY - 350, 700, 700);
                }
            }"""

    new_block = """            // DRAW IMAGE WITH AUTO-RETRY
            function drawOrRetry(img, alpha) {
                if (img && img.complete && img.naturalWidth > 0) {
                    ctx.globalAlpha = alpha;
                    ctx.drawImage(img, centerX - 350, centerY - 350, 700, 700);
                    ctx.globalAlpha = 1.0;
                    return true;
                } else {
                    requestAnimationFrame(() => render());
                    return false;
                }
            }

            if (opacityBlend > 0 && opacityBlend < 100) {
                drawOrRetry(loadedImages[currentEpochA], (100 - opacityBlend) / 100);
                drawOrRetry(loadedImages[currentEpochB], opacityBlend / 100);
            } else {
                drawOrRetry(loadedImages[activeEpochKey], 1.0);
            }"""

    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Successfully patched {HTML_PATH} with requestAnimationFrame auto-retry!")
    else:
        print("Block not found, checking content...")

if __name__ == "__main__":
    fix_canvas_loader()
