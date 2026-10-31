from pathlib import Path
from html import escape
P=Path(__file__).resolve().parents[1]/'assets'/'toolbox.svg'
INK='#242521'; PAPER='#F2F0E8'; ORANGE='#EA5A36'; MUTED='#625F57'
categories=[
 ('01 / LANGUAGES', ['Python','JavaScript','TypeScript','C++','SQL','HTML / CSS','Dart','Bash','PowerShell']),
 ('02 / PRODUCTS', ['React','Next.js','Flutter','FastAPI','Flask','Node.js','MapLibre','Three.js']),
 ('03 / DATA + CLOUD', ['PostgreSQL','MongoDB','Supabase','Neon','Docker','GCP','Cloudflare','Vercel','EasyPanel']),
 ('04 / INTELLIGENCE', ['PyTorch','OpenCV','YOLO','ONNX','TensorRT','Triton','Isaac Lab','Jetson','LeRobot'])]
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="810" viewBox="0 0 1200 810" role="img"><rect width="1200" height="810" fill="{PAPER}"/><rect width="1200" height="9" fill="{ORANGE}"/>',
 f'<text x="44" y="69" font-family="Arial, sans-serif" font-size="42" font-weight="900" fill="{INK}">MANY TOOLS. ONE WORKBENCH.</text>',
 f'<text x="45" y="102" font-family="Arial, sans-serif" font-size="17" fill="{MUTED}">Not a ranking. Not a certification wall. Just the stuff I build with.</text>']
palettes=['#EBC2B1','#EBCF82','#C7DFC9','#BFD4E9']
for k,(section,items) in enumerate(categories):
 x=44+(k%2)*564;y=134+(k//2)*321; bg=palettes[k]
 s.extend([f'<rect x="{x}" y="{y}" width="548" height="302" rx="10" fill="{bg}" stroke="{INK}" stroke-width="2"/>',f'<text x="{x+23}" y="{y+41}" fill="{INK}" font-family="Arial,sans-serif" font-size="21" font-weight="900" letter-spacing="1">{section}</text>',f'<path d="M{x+23} {y+55} h500" stroke="{INK}" stroke-width="1.5"/>'])
 for j,tool in enumerate(items):
  col=j%3;row=j//3;bx=x+23+col*171;by=y+80+row*67
  s.extend([f'<rect x="{bx}" y="{by}" width="160" height="52" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>',f'<circle cx="{bx+14}" cy="{by+25}" r="4" fill="{ORANGE}"/>',f'<text x="{bx+25}" y="{by+32}" fill="{INK}" font-family="Arial,sans-serif" font-size="{15 if len(tool)>10 else 17}" font-weight="700">{escape(tool)}</text>'])
s.extend([f'<rect x="0" y="778" width="1200" height="32" fill="{INK}"/>',f'<text x="44" y="799" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="{PAPER}">WEB / MOBILE / BACKEND / INFRA / AI / ROBOTICS</text>',f'<text x="1157" y="799" text-anchor="end" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="#EBCF82">ALWAYS LEARNING ↗</text>','</svg>'])
P.write_text(''.join(s),encoding='utf-8');print(P)
