"""
Fix CSS z-index stacking bug in HR 8799 Blink Comparator tool.
Brings active image to z-index: 2 and opacity: 1, ensuring 100% visible blinking between Epoch A and Epoch B.
"""

import os

HTML_PATH = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/docs/hr8799_blink_comparator.html"

def fix_blinking_css():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace updateDisplay() function to include z-index update
    old_func = """        function updateDisplay() {
            const activeKey = (blinkActiveFrame === 0) ? currentEpochA : currentEpochB;
            
            // Toggle native <img> element visibility
            document.querySelectorAll('.astro-image').forEach(img => {
                if (img.id === `img_${activeKey}`) img.classList.add('active');
                else img.classList.remove('active');
            });"""

    new_func = """        function updateDisplay() {
            const activeKey = (blinkActiveFrame === 0) ? currentEpochA : currentEpochB;
            
            // Toggle native <img> element visibility and z-index stack
            document.querySelectorAll('.astro-image').forEach(img => {
                if (img.id === `img_${activeKey}`) {
                    img.style.zIndex = '2';
                    img.style.opacity = '1';
                } else {
                    img.style.zIndex = '1';
                    img.style.opacity = '0';
                }
            });"""

    if old_func in content:
        content = content.replace(old_func, new_func)
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Fixed CSS z-index stacking bug in updateDisplay()!")
    else:
        print("Function signature not found, checking file...")

if __name__ == "__main__":
    fix_blinking_css()
