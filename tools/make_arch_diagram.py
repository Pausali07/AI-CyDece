#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
out = Path.home()/ "AI-CyDece"/ "docs"/ "architecture_diagram.png"
out.parent.mkdir(parents=True, exist_ok=True)

W, H = 1200, 600
img = Image.new("RGB", (W,H), "white")
d = ImageDraw.Draw(img)
# simple boxes
boxes = [
    ("Attacker", 50, 80),
    ("Honeypot\n(container)", 300, 80),
    ("Watcher\n(analyze)", 650, 80),
    ("LLM\nAnalyzer", 950, 80),
    ("Reports & Charts", 650, 360),
]
font = None
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 16)
except:
    font = ImageFont.load_default()
for text, x, y in boxes:
    d.rectangle([x,y,x+200,y+100], outline="black", width=2)
    d.multiline_text((x+10,y+10), text, fill="black", font=font)
# arrows
d.line((250,130,300,130), fill="black", width=2)
d.line((500,130,650,130), fill="black", width=2)
d.line((850,130,950,130), fill="black", width=2)
d.line((750,180,750,360), fill="black", width=2)
img.save(out)
print("Saved diagram to", out)
