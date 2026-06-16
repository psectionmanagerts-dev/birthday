"""
birthday_scene.py  –  Enchanting Interactive Birthday Scene
Run:   python birthday_scene.py
Open:  http://localhost:5000

Deploy to Render:
  - Build command:  pip install -r requirements.txt
  - Start command:  python birthday_scene.py
  - Add env var:    FLASK_ENV=production

pip install flask
"""
from __future__ import annotations
import logging, os, time
from flask import Flask, make_response

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s")
log = logging.getLogger(__name__)
_START = time.time()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "birthday-secret-2025")

# ── HARD disable every cache layer so Render always serves fresh HTML ─────────
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"]        = "no-cache"
    response.headers["Expires"]       = "0"
    return response

@app.route("/")
def home():
    resp = make_response(HTML)
    resp.content_type = "text/html; charset=utf-8"
    return resp

@app.route("/api/health")
def health():
    from flask import jsonify
    return jsonify(status="ok", uptime=round(time.time()-_START,1)), 200

# ═════════════════════════════════════════════════════════════════════════════
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>🎂 Birthday Scene v3</title>
<style>
/* ── Reset ─────────────────────────────────────── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{overflow:hidden;font-family:'Comic Sans MS',cursive;
  background:linear-gradient(180deg,#87CEEB 0%,#b0e0ff 60%,#4CAF50 60%,#2e7d32 100%);
  transition:background 2.5s}
body.night{background:linear-gradient(180deg,#0a0a2e 0%,#1a1a4e 60%,#1a3a1a 60%,#0d1f0d 100%)}

/* ── Canvas fills everything behind DOM ─── */
#bg-canvas{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}

/* ── Scene wrapper ─────────────────────────────── */
#scene{position:relative;width:100vw;height:100vh;overflow:hidden;z-index:1}

/* ── River ──────────────────────────────────────── */
#river{position:absolute;bottom:0;left:0;width:32%;height:58%;
  background:linear-gradient(135deg,#1E90FFaa,#00CED1bb);
  border-radius:0 55% 0 0;overflow:hidden;z-index:2}
body.night #river{filter:brightness(0.45) hue-rotate(20deg)}
.ripple{position:absolute;border:1.5px solid rgba(255,255,255,0.55);
  border-radius:50%;animation:rippleOut ease-in-out infinite;opacity:0}
@keyframes rippleOut{0%{transform:scale(0.2);opacity:0.7}100%{transform:scale(1);opacity:0}}
.glint{position:absolute;width:4px;height:4px;background:white;border-radius:50%;
  opacity:0;animation:glintFlash ease-in-out infinite}
@keyframes glintFlash{0%,100%{opacity:0}50%{opacity:0.9}}
.fish{position:absolute;font-size:18px;animation:swim linear infinite}
@keyframes swim{0%{left:5%;transform:scaleX(1)}
  49%{left:75%;transform:scaleX(1)}
  50%{left:75%;transform:scaleX(-1)}
  100%{left:5%;transform:scaleX(-1)}}
.stone{position:absolute;background:rgba(120,100,80,0.6);border-radius:50%}

/* ── Ground flowers ───────────────────────────── */
.flower{position:absolute;cursor:pointer;z-index:4;
  transition:transform 0.3s;animation:sway ease-in-out infinite}
@keyframes sway{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
.flower:hover{filter:brightness(1.3)}

/* ── PANDA ──────────────────────────────────────── */
#panda{position:absolute;cursor:pointer;z-index:20;
  transition:left 2s cubic-bezier(.4,0,.2,1), bottom 2s cubic-bezier(.4,0,.2,1);
  animation:pandaBob 0.75s ease-in-out infinite}
@keyframes pandaBob{0%,100%{filter:drop-shadow(0 8px 6px rgba(0,0,0,.2))}
  50%{filter:drop-shadow(0 14px 10px rgba(0,0,0,.25));margin-top:-6px}}
#panda.dancing{animation:pandaDance 0.35s ease-in-out infinite!important}
@keyframes pandaDance{
  0%{transform:rotate(-14deg) translateY(-6px) scale(1.05)}
  50%{transform:rotate(14deg) translateY(-14px) scale(1.1)}
  100%{transform:rotate(-14deg) translateY(-6px) scale(1.05)}}
svg#panda-svg{overflow:visible;filter:drop-shadow(2px 4px 6px rgba(0,0,0,.2))}

/* ── Balloons ────────────────────────────────────── */
.balloon-wrap{position:absolute;z-index:15;cursor:pointer}
.balloon-body{border-radius:50% 50% 50% 50%/40% 40% 60% 60%;
  position:relative;transition:transform .2s}
.balloon-body:hover{transform:scale(1.08)}
.balloon-string{width:1px;background:rgba(80,60,40,.45);margin:0 auto;
  transform-origin:top;animation:stringSway ease-in-out infinite}
@keyframes stringSway{0%,100%{transform:skewX(-6deg)}50%{transform:skewX(6deg)}}
.balloon-shine{position:absolute;top:14%;left:20%;width:28%;height:38%;
  background:rgba(255,255,255,.5);border-radius:50%;transform:rotate(-30deg)}

/* ── Butterflies ─────────────────────────────────── */
.butterfly{position:absolute;z-index:18;pointer-events:none;font-size:24px}

/* ── Sparkles ────────────────────────────────────── */
.sparkle{position:absolute;pointer-events:none;border-radius:50%;z-index:16;
  animation:sparkleLife ease-in-out infinite}
@keyframes sparkleLife{0%,100%{opacity:0;transform:scale(.4)}
  50%{opacity:1;transform:scale(1.6)}}

/* ── Burst particles ─────────────────────────────── */
.burst{position:absolute;pointer-events:none;z-index:100;font-size:18px;
  animation:burstFly .9s ease-out forwards}
@keyframes burstFly{0%{transform:translate(0,0) scale(1);opacity:1}
  100%{transform:translate(var(--bx),var(--by)) scale(0);opacity:0}}

/* ── HUD ─────────────────────────────────────────── */
#hud{position:fixed;top:14px;left:50%;transform:translateX(-50%);z-index:200;
  display:flex;align-items:center;gap:14px;
  background:rgba(255,255,255,.28);backdrop-filter:blur(8px);
  border:1px solid rgba(255,255,255,.45);border-radius:30px;padding:8px 20px}
#hud-label{font-size:13px;font-weight:700;color:#333;transition:color 2.5s;user-select:none}
body.night #hud-label{color:#ddd}
#tog{width:52px;height:28px;border:none;border-radius:14px;background:#87CEEB;
  cursor:pointer;position:relative;transition:background .4s;outline:none}
#tog::after{content:"";position:absolute;top:3px;left:3px;width:22px;height:22px;
  border-radius:50%;background:white;transition:transform .4s,background .4s;
  box-shadow:0 1px 4px rgba(0,0,0,.25)}
body.night #tog{background:#1a1a4e}
body.night #tog::after{transform:translateX(24px);background:#FFD700}
#score{position:fixed;top:14px;right:18px;z-index:200;font-size:13px;font-weight:700;
  background:rgba(255,255,255,.28);backdrop-filter:blur(6px);
  border:1px solid rgba(255,255,255,.35);border-radius:20px;padding:6px 14px;
  color:#333;transition:color 2.5s}
body.night #score{color:#eee}
#hint{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);
  font-size:12px;color:rgba(0,0,0,.5);background:rgba(255,255,255,.3);
  border-radius:20px;padding:4px 14px;z-index:200}
body.night #hint{color:rgba(255,255,255,.5)}

/* ── Night aurora ────────────────────────────────── */
#aurora{position:fixed;top:0;left:0;width:100%;height:40%;
  background:linear-gradient(180deg,transparent,rgba(0,200,100,.07) 40%,transparent);
  opacity:0;transition:opacity 2.5s;pointer-events:none;z-index:1;
  animation:auroraPulse 6s ease-in-out infinite}
@keyframes auroraPulse{0%,100%{opacity:0}50%{opacity:1}}
body.night #aurora{opacity:1}
</style>
</head>
<body id="body">
<canvas id="bg-canvas"></canvas>
<div id="aurora"></div>
<div id="scene">
  <div id="river"></div>
  <div id="flowers-layer"></div>

  <!-- PANDA (SVG so no images needed) -->
  <div id="panda">
    <svg id="panda-svg" width="140" height="190" viewBox="0 0 140 190">
      <!-- Shadow -->
      <ellipse cx="70" cy="186" rx="45" ry="8" fill="rgba(0,0,0,.18)"/>
      <!-- Body -->
      <ellipse cx="70" cy="140" rx="52" ry="50" fill="#f7f7f7" stroke="#222" stroke-width="3"/>
      <!-- Belly patch -->
      <ellipse cx="70" cy="148" rx="28" ry="26" fill="#e8e8e8"/>
      <!-- Legs -->
      <ellipse cx="48" cy="180" rx="18" ry="13" fill="#f7f7f7" stroke="#222" stroke-width="2.5"/>
      <ellipse cx="92" cy="180" rx="18" ry="13" fill="#f7f7f7" stroke="#222" stroke-width="2.5"/>
      <!-- Left arm (holds pig string) -->
      <rect x="16" y="120" width="22" height="38" rx="11" fill="#f7f7f7" stroke="#222" stroke-width="2.5" transform="rotate(18,27,130)"/>
      <!-- Right arm (holds lollipop) - animated via JS -->
      <g id="rarm">
        <rect x="102" y="118" width="22" height="38" rx="11" fill="#f7f7f7" stroke="#222" stroke-width="2.5" transform="rotate(-18,113,128)"/>
      </g>
      <!-- Lollipop stick -->
      <line x1="128" y1="118" x2="128" y2="88" stroke="#c8a020" stroke-width="3" stroke-linecap="round"/>
      <!-- Lollipop swirl (conic via multiple arcs) -->
      <circle cx="128" cy="82" r="18" fill="white" stroke="#dd2244" stroke-width="2"/>
      <path d="M128,64 A18,18 0 0,1 146,82" fill="#ff4466" opacity=".9"/>
      <path d="M146,82 A18,18 0 0,1 128,100" fill="#ff99bb" opacity=".9"/>
      <path d="M128,100 A18,18 0 0,1 110,82" fill="#ff4466" opacity=".9"/>
      <path d="M110,82 A18,18 0 0,1 128,64" fill="#ff99bb" opacity=".9"/>
      <circle cx="128" cy="82" r="8" fill="white" opacity=".4"/>
      <!-- Lollipop glow -->
      <circle cx="128" cy="82" r="20" fill="none" stroke="#ff4466" stroke-width="2" opacity=".3">
        <animate attributeName="r" values="18;24;18" dur="1.5s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values=".3;.0;.3" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <!-- Tongue (licking) -->
      <ellipse cx="118" cy="90" rx="6" ry="4" fill="#ff6b81">
        <animateTransform attributeName="transform" type="translate"
          values="0,0;8,-6;0,0" dur="1s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;1;0" dur="1s" repeatCount="indefinite"/>
      </ellipse>

      <!-- Head -->
      <ellipse cx="70" cy="72" rx="54" ry="52" fill="#f7f7f7" stroke="#222" stroke-width="3"/>
      <!-- Ears (dark) -->
      <circle cx="22" cy="28" r="20" fill="#1a1a1a" stroke="#000" stroke-width="2"/>
      <circle cx="118" cy="28" r="20" fill="#1a1a1a" stroke="#000" stroke-width="2"/>
      <!-- Inner ears -->
      <circle cx="22" cy="28" r="10" fill="#3a3a3a"/>
      <circle cx="118" cy="28" r="10" fill="#3a3a3a"/>
      <!-- Eye patches -->
      <ellipse cx="46" cy="68" rx="19" ry="16" fill="#1a1a1a" transform="rotate(-12,46,68)"/>
      <ellipse cx="94" cy="68" rx="19" ry="16" fill="#1a1a1a" transform="rotate(12,94,68)"/>
      <!-- Eyes -->
      <circle cx="46" cy="68" r="8" fill="white"/>
      <circle cx="94" cy="68" r="8" fill="white"/>
      <circle cx="48" cy="66" r="4.5" fill="#111"/>
      <circle cx="96" cy="66" r="4.5" fill="#111"/>
      <!-- Eye shine -->
      <circle cx="50" cy="64" r="2" fill="white"/>
      <circle cx="98" cy="64" r="2" fill="white"/>
      <!-- Cheeks -->
      <ellipse cx="26" cy="82" rx="14" ry="10" fill="#ffb3c6" opacity=".7"/>
      <ellipse cx="114" cy="82" rx="14" ry="10" fill="#ffb3c6" opacity=".7"/>
      <!-- Nose -->
      <ellipse cx="70" cy="84" rx="8" ry="5" fill="#333"/>
      <!-- Smile -->
      <path d="M60,94 Q70,104 80,94" fill="none" stroke="#333" stroke-width="2.5" stroke-linecap="round"/>
      <!-- Bow (top right of head) -->
      <g transform="translate(88,12)">
        <!-- Left wing -->
        <path d="M0,10 Q-20,-8 -28,2 Q-18,14 0,10" fill="#ffb3c6" stroke="#cc6688" stroke-width="1.5"/>
        <!-- Right wing -->
        <path d="M0,10 Q20,-8 28,2 Q18,14 0,10" fill="#ffb3c6" stroke="#cc6688" stroke-width="1.5"/>
        <!-- Center knot -->
        <ellipse cx="0" cy="10" rx="5" ry="4" fill="#ff9eb5" stroke="#cc5577" stroke-width="1"/>
        <!-- Ribbon tails -->
        <path d="M-3,13 Q-10,24 -6,30" fill="none" stroke="#cc6688" stroke-width="1.5"/>
        <path d="M3,13 Q10,24 6,30" fill="none" stroke="#cc6688" stroke-width="1.5"/>
      </g>
    </svg>

    <!-- Mini pig bag (DOM, beside panda) -->
    <div style="position:absolute;bottom:16px;left:-38px;animation:pigWobble 2s ease-in-out infinite">
      <svg width="52" height="52" viewBox="0 0 52 52">
        <!-- Bag body -->
        <circle cx="26" cy="30" r="20" fill="#ffb3c6" stroke="#cc6688" stroke-width="2"/>
        <!-- Ears -->
        <ellipse cx="14" cy="14" rx="7" ry="5" fill="#ffb3c6" stroke="#cc6688" stroke-width="1.5" transform="rotate(-30,14,14)"/>
        <ellipse cx="38" cy="14" rx="7" ry="5" fill="#ffb3c6" stroke="#cc6688" stroke-width="1.5" transform="rotate(30,38,14)"/>
        <!-- Inner ears -->
        <ellipse cx="14" cy="14" rx="4" ry="3" fill="#ff9eb5" transform="rotate(-30,14,14)"/>
        <ellipse cx="38" cy="14" rx="4" ry="3" fill="#ff9eb5" transform="rotate(30,38,14)"/>
        <!-- Eyes -->
        <circle cx="20" cy="26" r="3.5" fill="#333"/>
        <circle cx="32" cy="26" r="3.5" fill="#333"/>
        <circle cx="21" cy="25" r="1.2" fill="white"/>
        <circle cx="33" cy="25" r="1.2" fill="white"/>
        <!-- Snout -->
        <ellipse cx="26" cy="34" rx="8" ry="6" fill="#ff9eb5"/>
        <circle cx="23" cy="34" r="1.8" fill="#cc6688"/>
        <circle cx="29" cy="34" r="1.8" fill="#cc6688"/>
        <!-- Cheeks -->
        <ellipse cx="13" cy="31" rx="5" ry="3.5" fill="#ff99aa" opacity=".6"/>
        <ellipse cx="39" cy="31" rx="5" ry="3.5" fill="#ff99aa" opacity=".6"/>
        <!-- Bag handle string -->
        <path d="M26,10 Q40,-2 50,8" fill="none" stroke="#cc6688" stroke-width="1.5" stroke-dasharray="3,2"/>
      </svg>
    </div>
  </div>

  <div id="balloons-layer"></div>
  <div id="butterflies-layer"></div>
  <div id="sparkles-layer"></div>
</div>

<!-- HUD -->
<div id="hud">
  <span id="hud-label">☀️ Day Mode</span>
  <button id="tog" onclick="toggleNight()" aria-label="Toggle day/night"></button>
</div>
<div id="score">🎈 Popped: <span id="pop-ct">0</span></div>
<div id="hint">🐼 Click panda to dance • 🎈 Click balloons to pop • 🌸 Click flowers to bloom</div>

<script>
/* ══════════════════════════════════════════════════════════
   Birthday Scene – Main Script
   ══════════════════════════════════════════════════════════ */
(()=>{
"use strict";

/* ── Canvas for sky (sun rays, stars, moon craters) ─ */
const canvas=document.getElementById('bg-canvas');
const ctx=canvas.getContext('2d');
let W=innerWidth, H=innerHeight, isNight=false, pops=0, pandaBusy=false;

function resize(){ W=canvas.width=innerWidth; H=canvas.height=innerHeight; }
resize(); addEventListener('resize',resize);

/* ── State for canvas objects ── */
const stars=[];
const sunRays=[];
for(let i=0;i<24;i++) sunRays.push({angle:i*15*Math.PI/180,len:0,phase:Math.random()*Math.PI*2});
for(let i=0;i<200;i++) stars.push({x:Math.random()*2,y:Math.random(),r:Math.random()*1.8+.4,phase:Math.random()*Math.PI*2});
const moonCraters=[{x:.18,y:.28,r:.08},{x:.6,y:.55,r:.05},{x:.35,y:.7,r:.06},{x:.72,y:.25,r:.04}];

let tick=0;
function drawCanvas(){
  ctx.clearRect(0,0,W,H);
  tick+=0.016;

  if(!isNight){
    /* Sun + rays */
    const sx=W*.88, sy=55;
    for(let r of sunRays){
      r.len=28+Math.sin(tick*1.2+r.phase)*8;
      ctx.save();ctx.translate(sx,sy);ctx.rotate(r.angle+tick*.2);
      ctx.strokeStyle=`rgba(255,210,0,${.25+.12*Math.sin(tick+r.phase)})`;
      ctx.lineWidth=2.5;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(38,0);ctx.lineTo(38+r.len,0);ctx.stroke();
      ctx.restore();
    }
    /* Sun body */
    const sg=ctx.createRadialGradient(sx,sy,0,sx,sy,38);
    sg.addColorStop(0,'#FFE44d');sg.addColorStop(.6,'#FFA500');sg.addColorStop(1,'rgba(255,140,0,0)');
    ctx.beginPath();ctx.arc(sx,sy,38,0,Math.PI*2);ctx.fillStyle=sg;ctx.fill();
    /* Lens flare */
    ctx.save();ctx.globalAlpha=.12+.06*Math.sin(tick*1.5);
    const lf=ctx.createRadialGradient(sx,sy,0,sx,sy,90);
    lf.addColorStop(0,'white');lf.addColorStop(1,'transparent');
    ctx.beginPath();ctx.arc(sx,sy,90,0,Math.PI*2);ctx.fillStyle=lf;ctx.fill();
    ctx.restore();
  } else {
    /* Moon */
    const mx=W*.88, my=55, mr=36;
    const mg=ctx.createRadialGradient(mx-8,my-8,2,mx,my,mr);
    mg.addColorStop(0,'#fffde0');mg.addColorStop(.6,'#e8e4b0');mg.addColorStop(1,'#c8c090');
    ctx.beginPath();ctx.arc(mx,my,mr,0,Math.PI*2);ctx.fillStyle=mg;ctx.fill();
    /* Moon glow halo */
    ctx.save();ctx.globalAlpha=.12+.06*Math.sin(tick);
    const mh=ctx.createRadialGradient(mx,my,mr,mx,my,mr+40);
    mh.addColorStop(0,'rgba(255,255,200,.5)');mh.addColorStop(1,'transparent');
    ctx.beginPath();ctx.arc(mx,my,mr+40,0,Math.PI*2);ctx.fillStyle=mh;ctx.fill();
    ctx.restore();
    /* Craters */
    for(let c of moonCraters){
      ctx.save();ctx.globalAlpha=.35;
      ctx.beginPath();ctx.arc(mx+c.x*mr*2-mr,my+c.y*mr*2-mr,c.r*mr,0,Math.PI*2);
      ctx.fillStyle='#aaa080';ctx.fill();ctx.restore();
    }
    /* Stars */
    for(let s of stars){
      const a=.3+.7*Math.abs(Math.sin(tick*0.8+s.phase));
      ctx.save();ctx.globalAlpha=a;
      ctx.beginPath();ctx.arc(s.x*W,s.y*H*.65,s.r,0,Math.PI*2);
      ctx.fillStyle='white';ctx.fill();ctx.restore();
    }
  }
  requestAnimationFrame(drawCanvas);
}
drawCanvas();

/* ── Helpers ── */
const rand=(a,b)=>Math.random()*(b-a)+a;
const pick=a=>a[Math.floor(Math.random()*a.length)];

/* ── River ── */
const river=document.getElementById('river');
/* Ripples */
for(let i=0;i<10;i++){
  const r=document.createElement('div'); r.className='ripple';
  const s=rand(25,75);
  r.style.cssText=`width:${s}px;height:${s}px;left:${rand(5,80)}%;top:${rand(10,80)}%;
    animation-duration:${rand(1.8,3.2)}s;animation-delay:-${rand(0,3)}s;
    border-radius:${rand(40,60)}% ${rand(40,60)}%`;
  river.appendChild(r);
}
/* Glints */
for(let i=0;i<12;i++){
  const g=document.createElement('div'); g.className='glint';
  g.style.cssText=`width:${rand(3,6)}px;height:${rand(3,6)}px;
    left:${rand(5,90)}%;top:${rand(5,90)}%;
    animation-duration:${rand(1,2.5)}s;animation-delay:-${rand(0,2.5)}s`;
  river.appendChild(g);
}
/* Stones */
['rgba(100,90,80,.5)','rgba(120,100,70,.5)','rgba(80,80,80,.4)'].forEach(c=>{
  const s=document.createElement('div'); s.className='stone';
  const sw=rand(12,28),sh=rand(8,16);
  s.style.cssText=`width:${sw}px;height:${sh}px;background:${c};
    left:${rand(5,80)}%;top:${rand(20,80)}%`;
  river.appendChild(s);
});
/* Fish */
['🐠','🐟','🐡'].forEach(f=>{
  const el=document.createElement('div'); el.className='fish'; el.textContent=f;
  el.style.cssText=`bottom:${rand(10,60)}%;animation-duration:${rand(5,9)}s;animation-delay:-${rand(0,8)}s`;
  river.appendChild(el);
});

/* ── Flowers ── */
const FLOWER_TYPES=[
  {e:'🌸',s:26},{e:'🌼',s:28},{e:'🌻',s:30},{e:'🌷',s:24},{e:'🌺',s:26},{e:'💐',s:28}
];
const fl=document.getElementById('flowers-layer');
for(let i=0;i<22;i++){
  const fd=pick(FLOWER_TYPES);
  const el=document.createElement('div'); el.className='flower';
  el.textContent=fd.e; el.style.fontSize=fd.s+'px';
  el.style.cssText+=`left:${rand(2,94)}%;bottom:${rand(20,34)}vh;
    animation-duration:${rand(2.2,4.8)}s;animation-delay:-${rand(0,4)}s;font-size:${fd.s}px`;
  el.title='Click to bloom!';
  el.onclick=e=>{
    el.style.transform='scale(1.7) rotate(20deg)';
    setTimeout(()=>el.style.transform='',600);
    burst(e.pageX,e.pageY,fd.e);
  };
  fl.appendChild(el);
}

/* ── Balloons ── */
const BCOLORS=['#ff4d6d','#4dabf7','#ffd43b','#69db7c','#b197fc','#ff922b','#f06595','#20c997'];
const bl=document.getElementById('balloons-layer');
function makeBalloon(){
  const wrap=document.createElement('div'); wrap.className='balloon-wrap';
  const color=pick(BCOLORS);
  const x=rand(4,90);
  const ht=rand(55,82), wt=ht*.82;
  const floatDur=rand(4.5,8), swayDur=rand(2.5,4.5);
  wrap.style.cssText=`left:${x}%;bottom:-160px`;

  const body=document.createElement('div'); body.className='balloon-body';
  body.style.cssText=`width:${wt}px;height:${ht}px;background:${color};
    box-shadow:inset -10px -10px 22px rgba(0,0,0,.18);`;
  body.style.animation=`balloonFloat ${floatDur}s ease-in-out infinite`;

  /* Shine */
  const shine=document.createElement('div'); shine.className='balloon-shine';
  body.appendChild(shine);

  /* Shimmer pulse ring */
  const ring=document.createElement('div');
  ring.style.cssText=`position:absolute;inset:-4px;border-radius:inherit;
    border:2px solid rgba(255,255,255,.3);
    animation:shimmerPulse ${rand(1.5,2.5)}s ease-in-out infinite`;
  body.appendChild(ring);

  /* Knot */
  const knot=document.createElement('div');
  knot.style.cssText=`position:absolute;bottom:-9px;left:50%;transform:translateX(-50%);
    width:10px;height:9px;background:${color};border-radius:50% 50% 40% 40%;
    box-shadow:0 2px 3px rgba(0,0,0,.2)`;
  body.appendChild(knot);

  const str=document.createElement('div'); str.className='balloon-string';
  str.style.cssText=`height:${rand(60,90)}px;animation-duration:${swayDur}s`;

  wrap.appendChild(body); wrap.appendChild(str);

  body.onclick=e=>{
    e.stopPropagation();
    pops++; document.getElementById('pop-ct').textContent=pops;
    burst(e.pageX,e.pageY,pick(['💥','🎉','✨','⭐','🌟']));
    wrap.remove();
    setTimeout(makeBalloon,rand(600,2000));
  };
  bl.appendChild(wrap);

  /* Float up and remove */
  const riseDur=rand(11000,19000);
  const startY=-160, endY=-(H+200);
  let startTime=null;
  function rise(t){
    if(!startTime) startTime=t;
    const prog=Math.min((t-startTime)/riseDur,1);
    const y=startY+(endY-startY)*prog;
    wrap.style.bottom=(-y)+'px';
    if(prog<1) requestAnimationFrame(rise);
    else wrap.remove();
  }
  requestAnimationFrame(rise);
}
for(let i=0;i<8;i++) setTimeout(makeBalloon,i*500);
setInterval(()=>{ if(bl.children.length<8) makeBalloon(); },2500);

/* Shimmer keyframe (inject once) */
const ss=document.createElement('style');
ss.textContent=`@keyframes shimmerPulse{0%,100%{opacity:.15;transform:scale(1)}50%{opacity:.5;transform:scale(1.08)}}
@keyframes balloonFloat{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-20px) rotate(2deg)}}
@keyframes pigWobble{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}`;
document.head.appendChild(ss);

/* ── Butterflies ── */
const BUTTS=['🦋','🦋','🦋','🪲'];
const btl=document.getElementById('butterflies-layer');
BUTTS.forEach((b,i)=>{
  const el=document.createElement('div'); el.className='butterfly'; el.textContent=b;
  const startX=rand(15,70), startY=rand(18,55);
  el.style.cssText=`left:${startX}%;top:${startY}%`;
  btl.appendChild(el);
  /* Random wander via JS */
  let tx=startX,ty=startY,cx=startX,cy=startY;
  function wander(){
    cx+=(tx-cx)*.018; cy+=(ty-cy)*.018;
    el.style.left=cx+'%'; el.style.top=cy+'%';
    if(Math.abs(cx-tx)<.5&&Math.abs(cy-ty)<.5){tx=rand(10,85);ty=rand(15,60);}
    requestAnimationFrame(wander);
  }
  wander();
  setInterval(()=>{tx=rand(10,85);ty=rand(15,60);},rand(3000,7000));
});

/* ── Sparkles ── */
const sl=document.getElementById('sparkles-layer');
for(let i=0;i<35;i++){
  const sp=document.createElement('div'); sp.className='sparkle';
  const sz=rand(3,7);
  const col=isNight?'white':'gold';
  sp.style.cssText=`width:${sz}px;height:${sz}px;background:gold;
    left:${rand(0,100)}%;top:${rand(8,85)}%;
    animation-duration:${rand(1.5,4)}s;animation-delay:-${rand(0,4)}s`;
  sl.appendChild(sp);
}

/* ── Panda movement ── */
const panda=document.getElementById('panda');
function movePanda(){
  if(pandaBusy) return;
  const maxL=Math.max(10, W-180);
  panda.style.left=rand(8,maxL)+'px';
  panda.style.bottom=rand(26,38)+'vh';
}
movePanda();
setInterval(movePanda,2600);

panda.onclick=()=>{
  if(pandaBusy) return;
  pandaBusy=true;
  panda.classList.add('dancing');
  burst(panda.getBoundingClientRect().left+70,
        panda.getBoundingClientRect().top+50,
        pick(['🎉','🌟','💖','✨','🎊']));
  setTimeout(()=>{ panda.classList.remove('dancing'); pandaBusy=false; },2800);
};

/* ── Burst helper ── */
function burst(x,y,emoji){
  for(let i=0;i<10;i++){
    const p=document.createElement('div'); p.className='burst';
    p.textContent=emoji;
    const ang=rand(0,Math.PI*2), dist=rand(45,110);
    p.style.cssText=`left:${x}px;top:${y}px;`+
      `--bx:${Math.cos(ang)*dist}px;--by:${Math.sin(ang)*dist}px;`+
      `animation-delay:${rand(0,.15)}s`;
    document.body.appendChild(p);
    setTimeout(()=>p.remove(),1000);
  }
}

/* ── Day / Night toggle ── */
window.toggleNight=function(){
  isNight=!isNight;
  document.body.classList.toggle('night',isNight);
  document.getElementById('hud-label').textContent=isNight?'🌙 Night Mode':'☀️ Day Mode';
  /* Update sparkle colours */
  document.querySelectorAll('.sparkle').forEach(s=>{
    s.style.background=isNight?'rgba(255,255,255,.9)':'gold';
  });
};

})();
</script>
</body>
</html>"""

# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    log.info("🎂 Starting on http://0.0.0.0:%d",port)
    app.run(host="0.0.0.0",port=port,debug=False)
