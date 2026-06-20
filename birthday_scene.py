"""
birthday_scene.py  –  Enchanted Interactive Birthday Experience
─────────────────────────────────────────────────────────────────
Features:
  - Teddy bear with natural behavior states: walking, posing, sleeping,
    using a laptop, eating cake, and a happy dance on click.
  - Stylish glossy balloons with shimmer strings; auto-pop near the top
    of the screen if not clicked.
  - Every pop triggers: emoji burst + confetti + a gift-box pop animation
    + nearby flowers flare/glow/bloom then settle back.
  - Automatic day → night cycle (smooth multi-second crossfade), with
    sun rays, drifting clouds, a glowing moon, and gradually
    appearing twinkling stars. Manual toggle also available.
  - River with ripples, glints, reflections, stones, and fish.
  - Ambient floating sparkles and wandering butterflies/birds.
  - Large festive cake with 28 lit, flickering candles appears at the
    finale, alongside a custom "Happy Birthday AJ" message.

Run:   python birthday_scene.py
Open:  http://localhost:5000

Deploy to Render:
  Build command:  pip install -r requirements.txt
  Start command:  python birthday_scene.py

pip install flask
"""
from __future__ import annotations
import logging, os, time
from flask import Flask, make_response, jsonify

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s")
log = logging.getLogger(__name__)
_START = time.time()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "birthday-secret-2025")

# ── Disable every cache layer so deployments always serve fresh HTML ─────────
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def home():
    resp = make_response(HTML)
    resp.content_type = "text/html; charset=utf-8"
    return resp

@app.route("/api/health")
def health():
    return jsonify(status="ok", uptime=round(time.time() - _START, 1)), 200

# ═════════════════════════════════════════════════════════════════════════════
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>🎂 Enchanted Birthday Scene</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{overflow:hidden;height:100%;font-family:'Comic Sans MS',cursive}
body{
  background:linear-gradient(180deg,#87CEEB 0%,#bfe8ff 55%,#6fcf6f 55%,#3d9c40 100%);
  transition:background 4s ease-in-out;
  position:relative;
}
body.night{
  background:linear-gradient(180deg,#0b0b2e 0%,#1b1b4e 55%,#163a1c 55%,#0a1d0e 100%);
}

#bg-canvas{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
#aurora{position:fixed;top:0;left:0;width:100%;height:42%;
  background:linear-gradient(180deg,transparent,rgba(80,220,150,.08) 40%,transparent);
  opacity:0;transition:opacity 4s;pointer-events:none;z-index:1;
  animation:auroraPulse 7s ease-in-out infinite}
@keyframes auroraPulse{0%,100%{opacity:0}50%{opacity:1}}
body.night #aurora{opacity:1}

#scene{position:relative;width:100vw;height:100vh;overflow:hidden;z-index:1}

/* ── River ─────────────────────────────────────────── */
#river{position:absolute;bottom:0;left:0;width:34%;height:58%;
  background:linear-gradient(135deg,#1E90FFaa,#00CED1bb);
  border-radius:0 58% 0 0;overflow:hidden;z-index:2;transition:filter 4s}
body.night #river{filter:brightness(.42) hue-rotate(15deg)}
.ripple{position:absolute;border:1.5px solid rgba(255,255,255,.55);border-radius:50%;
  animation:rippleOut ease-in-out infinite;opacity:0}
@keyframes rippleOut{0%{transform:scale(.2);opacity:.7}100%{transform:scale(1);opacity:0}}
.glint{position:absolute;width:4px;height:4px;background:white;border-radius:50%;
  opacity:0;animation:glintFlash ease-in-out infinite}
@keyframes glintFlash{0%,100%{opacity:0}50%{opacity:.9}}
.reflection{position:absolute;width:30px;height:6px;border-radius:50%;
  background:rgba(255,255,255,.35);filter:blur(1px);
  animation:reflectionShift ease-in-out infinite}
@keyframes reflectionShift{0%,100%{opacity:.2;transform:scaleX(1)}50%{opacity:.5;transform:scaleX(1.4)}}
.fish{position:absolute;font-size:18px;animation:swim linear infinite}
@keyframes swim{0%{left:5%;transform:scaleX(1)}49%{left:75%;transform:scaleX(1)}
  50%{left:75%;transform:scaleX(-1)}100%{left:5%;transform:scaleX(-1)}}
.stone{position:absolute;background:rgba(110,95,75,.55);border-radius:50%}

/* ── Flowers ───────────────────────────────────────── */
.flower-wrap{position:absolute;cursor:pointer;z-index:4;transform-origin:bottom center;
  transform:rotate(var(--wind,0deg));transition:transform .9s ease-out}
.flower{display:block;animation:flowerSway ease-in-out infinite;transform-origin:bottom center;
  transition:filter .4s, transform .4s}
@keyframes flowerSway{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
.flower.flaring{
  filter:drop-shadow(0 0 14px gold) drop-shadow(0 0 26px #fff89a) drop-shadow(0 0 38px #ffe98a) brightness(1.6);
  transform:scale(2) !important;
  animation:none !important;
}
.flower.settling{
  transition:transform 1.8s cubic-bezier(.34,1.2,.4,1), filter 1.8s ease-out;
}

/* ── Teddy bear ────────────────────────────────────── */
#teddy{position:absolute;cursor:pointer;z-index:25;
  transition:left 2.4s cubic-bezier(.45,0,.2,1), bottom 2.4s cubic-bezier(.45,0,.2,1);
}
#teddy.walking{animation:teddyBob .6s ease-in-out infinite}
@keyframes teddyBob{0%,100%{transform:translateY(0) rotate(-1deg)}50%{transform:translateY(-7px) rotate(1deg)}}
#teddy.sleeping{animation:teddySleep 3s ease-in-out infinite}
@keyframes teddySleep{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-2px) rotate(0deg)}}
#teddy.watching svg#teddy-svg{transform:rotate(4deg) translateY(2px);transition:transform .8s ease}
#teddy.watching{animation:teddyWatchBob 2.4s ease-in-out infinite}
@keyframes teddyWatchBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
#teddy.dancing{animation:teddyDance .35s ease-in-out infinite !important}
@keyframes teddyDance{
  0%{transform:rotate(-14deg) translateY(-6px) scale(1.05)}
  50%{transform:rotate(14deg) translateY(-15px) scale(1.12)}
  100%{transform:rotate(-14deg) translateY(-6px) scale(1.05)}
}
#teddy.glowing svg{filter:drop-shadow(0 0 14px gold) drop-shadow(0 0 26px #ffe9a8)}
svg#teddy-svg{overflow:visible;filter:drop-shadow(2px 5px 7px rgba(0,0,0,.22));transition:filter .6s}
.zzz{position:absolute;font-size:22px;opacity:0;pointer-events:none;color:#7c8cff;
  font-weight:bold;animation:zzzFloat 2.4s ease-in-out infinite}
@keyframes zzzFloat{0%{opacity:0;transform:translateY(0) scale(.6)}
  20%{opacity:1}80%{opacity:.8}100%{opacity:0;transform:translateY(-46px) scale(1.3)}}
.laptop-glow{position:absolute;border-radius:6px;background:radial-gradient(circle,#aee8ff,transparent 70%);
  opacity:0;animation:laptopFlicker 2.2s ease-in-out infinite}
@keyframes laptopFlicker{0%,100%{opacity:.35}50%{opacity:.7}}
.food-crumb{position:absolute;font-size:13px;opacity:0;animation:crumbFall 1.4s ease-in forwards}
@keyframes crumbFall{0%{opacity:1;transform:translateY(0) rotate(0)}100%{opacity:0;transform:translateY(24px) rotate(120deg)}}

/* ── Balloons ──────────────────────────────────────── */
.balloon-wrap{position:absolute;z-index:15;cursor:pointer;
  transform:translateX(var(--windpx,0px)) rotate(var(--windrot,0deg));
  transition:transform 1.1s ease-out}
.balloon-body{border-radius:50% 50% 50% 50%/40% 40% 60% 60%;position:relative;
  transition:transform .25s}
.balloon-body:hover{transform:scale(1.1)}
.balloon-string{width:2px;margin:0 auto;transform-origin:top;position:relative;
  animation:stringSway ease-in-out infinite;
  background:linear-gradient(180deg,rgba(255,255,255,.85),rgba(200,170,255,.55))}
.balloon-string::before{content:"";position:absolute;inset:-1px;width:4px;left:-1px;
  background:linear-gradient(180deg,transparent,gold,transparent);
  opacity:0;border-radius:2px;
  animation:stringTingle 1.8s ease-in-out infinite}
@keyframes stringSway{0%,100%{transform:skewX(-6deg)}50%{transform:skewX(6deg)}}
@keyframes stringTingle{0%,15%{opacity:0;top:-10%}45%{opacity:.95}85%,100%{opacity:0;top:100%}}
.balloon-shine{position:absolute;top:12%;left:18%;width:30%;height:40%;
  background:linear-gradient(135deg,rgba(255,255,255,.85),rgba(255,255,255,.1) 70%);
  border-radius:50%;transform:rotate(-30deg)}
.balloon-shine2{position:absolute;bottom:18%;right:16%;width:12%;height:14%;
  background:rgba(255,255,255,.4);border-radius:50%}

/* ── Gift box burst ────────────────────────────────── */
.gift-box{position:absolute;pointer-events:none;z-index:120;font-size:52px;
  animation:giftPop 1.8s cubic-bezier(.34,1.56,.64,1) forwards;
  filter:drop-shadow(0 0 14px rgba(255,210,120,.9)) drop-shadow(0 4px 8px rgba(0,0,0,.25))}
.gift-sparkle-ring{position:absolute;pointer-events:none;z-index:119;
  width:70px;height:70px;border-radius:50%;
  border:2px solid rgba(255,220,140,.8);
  animation:giftRing 1.2s ease-out forwards}
@keyframes giftPop{
  0%{transform:translateY(0) scale(.15) rotate(-25deg);opacity:0}
  22%{transform:translateY(-22px) scale(1.35) rotate(8deg);opacity:1}
  45%{transform:translateY(-44px) scale(1.05) rotate(-6deg);opacity:1}
  65%{transform:translateY(-58px) scale(1.15) rotate(4deg);opacity:1}
  100%{transform:translateY(-95px) scale(.75) rotate(0deg);opacity:0}
}
@keyframes giftRing{
  0%{transform:scale(.2);opacity:.9;border-width:3px}
  100%{transform:scale(2.4);opacity:0;border-width:0.5px}
}

/* ── Confetti ──────────────────────────────────────── */
.confetti{position:absolute;pointer-events:none;z-index:115;border-radius:2px;
  animation:confettiFall ease-in forwards}
@keyframes confettiFall{
  0%{transform:translate(0,0) rotate(0deg);opacity:1}
  100%{transform:translate(var(--cx),var(--cy)) rotate(var(--cr));opacity:0}
}

/* ── Burst emoji (existing effect kept) ───────────────── */
.burst{position:absolute;pointer-events:none;z-index:100;font-size:18px;
  animation:burstFly .9s ease-out forwards}
@keyframes burstFly{0%{transform:translate(0,0) scale(1);opacity:1}
  100%{transform:translate(var(--bx),var(--by)) scale(0);opacity:0}}

/* ── Fireworks (finale) ───────────────────────────────── */
.firework{
  position:absolute;
  pointer-events:none;
  z-index:300;
  font-size:24px;
  animation:fireworkBlast 1.5s ease-out forwards;
}
@keyframes fireworkBlast{
  0%{
    transform:scale(.3);
    opacity:1;
  }
  100%{
    transform:scale(4);
    opacity:0;
  }
}

/* ── Falling gift (collectible) ───────────────────────── */
.falling-gift{
  position:absolute;
  pointer-events:none;
  z-index:60;
  font-size:32px;
  animation:giftFall 2s ease-out forwards;
}
@keyframes giftFall{
  0%{
    transform:translateY(-80px) scale(.4);
    opacity:0;
  }
  100%{
    transform:translateY(0) scale(1);
    opacity:1;
  }
}

/* ── Motivational floating message ────────────────────── */
@keyframes msgFloat{
 from{
  opacity:1;
  transform:translateY(0);
 }
 to{
  opacity:0;
  transform:translateY(-120px);
 }
}

/* ── Butterflies / birds ───────────────────────────── */
.flyer{position:absolute;z-index:18;pointer-events:none;font-size:22px}

/* ── Sparkles ─────────────────────────────────────── */
.sparkle{position:absolute;pointer-events:none;border-radius:50%;z-index:16;
  animation:sparkleLife ease-in-out infinite}
@keyframes sparkleLife{0%,100%{opacity:0;transform:scale(.4)}50%{opacity:1;transform:scale(1.6)}}

/* ── Cake ─────────────────────────────────────────── */
#cake-wrap{position:fixed;bottom:-340px;left:50%;transform:translateX(-50%);z-index:250;
  transition:bottom 1.6s cubic-bezier(.34,1.2,.4,1);text-align:center}
#cake-wrap.show{bottom:18px}
#cake-glow{position:absolute;top:-60px;left:50%;transform:translateX(-50%);
  width:340px;height:200px;background:radial-gradient(circle,rgba(255,220,120,.55),transparent 70%);
  filter:blur(6px);animation:cakeGlowPulse 2s ease-in-out infinite;pointer-events:none}
@keyframes cakeGlowPulse{0%,100%{opacity:.6;transform:translateX(-50%) scale(1)}
  50%{opacity:1;transform:translateX(-50%) scale(1.08)}}

/* ── Final message ────────────────────────────────── */
#final-msg{position:fixed;top:18%;left:50%;transform:translateX(-50%) scale(.4);
  z-index:260;text-align:center;opacity:0;pointer-events:none;
  transition:opacity 1s ease, transform 1s cubic-bezier(.34,1.6,.5,1)}
#final-msg.show{opacity:1;transform:translateX(-50%) scale(1);pointer-events:auto}
#final-msg h1{font-size:clamp(2rem,7vw,4rem);color:#ff5d8f;
  text-shadow:0 0 18px #fff, 0 0 34px #ffd2e5, 3px 3px 0 #fff;
  margin:0;letter-spacing:1px;animation:msgPulse 1.6s ease-in-out infinite}
@keyframes msgPulse{0%,100%{filter:brightness(1)}50%{filter:brightness(1.25)}}
#final-msg p{font-size:clamp(1rem,3vw,1.4rem);color:#7a4ad1;margin-top:.4rem;font-weight:bold}

/* ── HUD ──────────────────────────────────────────── */
#hud{position:fixed;top:14px;left:50%;transform:translateX(-50%);z-index:200;
  display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.28);
  backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.45);
  border-radius:30px;padding:8px 20px}
#hud-label{font-size:13px;font-weight:700;color:#333;transition:color 4s;user-select:none}
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
  color:#333;transition:color 4s}
body.night #score{color:#eee}
#hint{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);font-size:12px;
  color:rgba(0,0,0,.5);background:rgba(255,255,255,.3);border-radius:20px;
  padding:4px 14px;z-index:200;text-align:center}
body.night #hint{color:rgba(255,255,255,.55)}

/* ── Mobile responsive ────────────────────────────────── */
@media(max-width:768px){
 #hud{
   transform:translateX(-50%) scale(.9);
 }
 #score{
   font-size:11px;
   right:8px;
 }
 #hint{
   width:90%;
   font-size:10px;
 }
 #final-msg h1{
   font-size:2rem;
 }
 #final-msg p{
   font-size:1rem;
 }
 #cake-wrap{
   transform:translateX(-50%) scale(.75);
 }
 #teddy{
   transform:scale(.8);
 }
 .balloon-body{
   transform:scale(.85);
 }
}
</style>
</head>
<body id="body">
<audio id="bgMusic" loop>
  <source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8d1d4f4b0.mp3" type="audio/mpeg">
</audio>
<canvas id="bg-canvas"></canvas>
<div id="aurora"></div>
<div id="scene">
  <div id="river"></div>
  <div id="flowers-layer"></div>
  <div id="teddy-layer"></div>
  <div id="balloons-layer"></div>
  <div id="flyers-layer"></div>
  <div id="sparkles-layer"></div>
</div>

<div id="cake-wrap">
  <div id="cake-glow"></div>
  <div id="cake-canvas-holder"></div>
</div>

<div id="final-msg">
  <h1>🎉 Happy Birthday AJ 🎉</h1>
  <p>✨ Wishing you a magical year ahead ✨</p>
</div>

<div id="hud">
  <span id="hud-label">☀️ Day Mode</span>
  <button id="tog" onclick="toggleNight(true)" aria-label="Toggle day/night"></button>
</div>
<div id="score">🎈 Popped: <span id="pop-ct">0</span> / 28</div>
<div id="hint">🧸 Click teddy for a happy dance • 🎈 Pop all 28 balloons for a surprise!</div>

<script>
/* ══════════════════════════════════════════════════════════════
   Enchanted Birthday Scene — Main Engine
   ══════════════════════════════════════════════════════════════ */
(()=>{
"use strict";

/* ── Globals ──────────────────────────────────────────────── */
const canvas=document.getElementById('bg-canvas');
const ctx=canvas.getContext('2d');
let W=innerWidth,H=innerHeight,isNight=false,pops=0,teddyBusy=false,finaleDone=false;
const rand=(a,b)=>Math.random()*(b-a)+a;
const pick=a=>a[Math.floor(Math.random()*a.length)];

function resize(){W=canvas.width=innerWidth;H=canvas.height=innerHeight;}
resize();addEventListener('resize',resize);

/* ── Background music: browsers block autoplay, so start on first click ─ */
document.addEventListener("click",()=>{
  const music=document.getElementById("bgMusic");
  if(music && music.paused){
    music.volume=0.35;
    music.play().catch(()=>{});
  }
},{once:true});

/* ── Canvas sky: sun / moon / stars / clouds ─────────────────── */
const stars=[];
for(let i=0;i<220;i++) stars.push({x:Math.random(),y:Math.random()*.62,r:Math.random()*1.8+.4,
  phase:Math.random()*Math.PI*2, bornAt:Math.random()*8}); // staggered appearance
const sunRays=[];
for(let i=0;i<24;i++) sunRays.push({angle:i*15*Math.PI/180,phase:Math.random()*Math.PI*2});
const moonCraters=[{x:.18,y:.28,r:.08},{x:.6,y:.55,r:.05},{x:.35,y:.7,r:.06},{x:.72,y:.25,r:.04}];
const clouds=[];
for(let i=0;i<6;i++) clouds.push({x:Math.random()*1.4-.2,y:rand(.05,.3),
  w:rand(80,160),h:rand(30,50),speed:rand(.0035,.008)});

let tick=0, nightProgress=0; // 0=full day, 1=full night (for smooth canvas blending)
function drawCanvas(dt){
  ctx.clearRect(0,0,W,H);
  tick+=dt;
  // ease night progress toward target
  const target=isNight?1:0;
  nightProgress += (target-nightProgress)*0.008;

  /* Clouds (both modes, dimmer at night) */
  for(let c of clouds){
    c.x+=c.speed*dt*60/1000;
    if(c.x>1.3) c.x=-0.3;
    const cx=c.x*W, cy=c.y*H;
    ctx.save();
    ctx.globalAlpha=(1-nightProgress*0.82);
    ctx.fillStyle='white';
    ctx.beginPath();ctx.ellipse(cx,cy,c.w*.5,c.h*.5,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(cx-c.w*.3,cy+c.h*.12,c.w*.32,c.h*.38,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(cx+c.w*.32,cy+c.h*.08,c.w*.28,c.h*.34,0,0,Math.PI*2);ctx.fill();
    ctx.restore();
  }

  /* Sun fading out / Moon fading in */
  const sx=W*.88, sy=H*.09;
  if(nightProgress<0.98){
    ctx.save();ctx.globalAlpha=1-nightProgress;
    for(let r of sunRays){
      const len=28+Math.sin(tick/1000*1.2+r.phase)*8;
      ctx.save();ctx.translate(sx,sy);ctx.rotate(r.angle+tick/1000*.2);
      ctx.strokeStyle=`rgba(255,210,0,${.25+.12*Math.sin(tick/1000+r.phase)})`;
      ctx.lineWidth=2.5;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(38,0);ctx.lineTo(38+len,0);ctx.stroke();
      ctx.restore();
    }
    const sg=ctx.createRadialGradient(sx,sy,0,sx,sy,38);
    sg.addColorStop(0,'#FFE44d');sg.addColorStop(.6,'#FFA500');sg.addColorStop(1,'rgba(255,140,0,0)');
    ctx.beginPath();ctx.arc(sx,sy,38,0,Math.PI*2);ctx.fillStyle=sg;ctx.fill();
    ctx.save();ctx.globalAlpha*=.12+.06*Math.sin(tick/1000*1.5);
    const lf=ctx.createRadialGradient(sx,sy,0,sx,sy,90);
    lf.addColorStop(0,'white');lf.addColorStop(1,'transparent');
    ctx.beginPath();ctx.arc(sx,sy,90,0,Math.PI*2);ctx.fillStyle=lf;ctx.fill();
    ctx.restore();
    ctx.restore();
  }
  if(nightProgress>0.02){
    ctx.save();ctx.globalAlpha=nightProgress;
    const mx=sx,my=sy,mr=36;
    const mg=ctx.createRadialGradient(mx-8,my-8,2,mx,my,mr);
    mg.addColorStop(0,'#fffde0');mg.addColorStop(.6,'#e8e4b0');mg.addColorStop(1,'#c8c090');
    ctx.beginPath();ctx.arc(mx,my,mr,0,Math.PI*2);ctx.fillStyle=mg;ctx.fill();
    ctx.save();ctx.globalAlpha*=.14+.07*Math.sin(tick/1000);
    const mh=ctx.createRadialGradient(mx,my,mr,mx,my,mr+44);
    mh.addColorStop(0,'rgba(255,255,200,.55)');mh.addColorStop(1,'transparent');
    ctx.beginPath();ctx.arc(mx,my,mr+44,0,Math.PI*2);ctx.fillStyle=mh;ctx.fill();
    ctx.restore();
    for(let c of moonCraters){
      ctx.save();ctx.globalAlpha*=.35;
      ctx.beginPath();ctx.arc(mx+c.x*mr*2-mr,my+c.y*mr*2-mr,c.r*mr,0,Math.PI*2);
      ctx.fillStyle='#aaa080';ctx.fill();ctx.restore();
    }
    /* Stars fade in gradually one by one based on bornAt */
    for(let s of stars){
      const appear=Math.min(1,Math.max(0,(nightProgress*10-s.bornAt)));
      const tw=.3+.7*Math.abs(Math.sin(tick/1000*0.8+s.phase));
      ctx.save();ctx.globalAlpha=appear*tw*nightProgress;
      ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);
      ctx.fillStyle='white';ctx.fill();ctx.restore();
    }
    ctx.restore();
  }
}
let lastT=performance.now();
function loop(t){const dt=t-lastT;lastT=t;drawCanvas(dt);requestAnimationFrame(loop);}
requestAnimationFrame(loop);

/* ── Automatic day → night cycle ─────────────────────────────── */
const CYCLE_MS = 120000; // auto toggle every 120s
setInterval(()=>{ if(window.toggleNight) window.toggleNight(false); }, CYCLE_MS);

/* ── River: ripples / glints / reflections / stones / fish ───── */
const river=document.getElementById('river');
for(let i=0;i<10;i++){
  const r=document.createElement('div');r.className='ripple';
  const s=rand(25,75);
  r.style.cssText=`width:${s}px;height:${s}px;left:${rand(5,80)}%;top:${rand(10,80)}%;
    animation-duration:${rand(1.8,3.2)}s;animation-delay:-${rand(0,3)}s;
    border-radius:${rand(40,60)}% ${rand(40,60)}%`;
  river.appendChild(r);
}
for(let i=0;i<14;i++){
  const g=document.createElement('div');g.className='glint';
  g.style.cssText=`width:${rand(3,6)}px;height:${rand(3,6)}px;left:${rand(5,90)}%;top:${rand(5,90)}%;
    animation-duration:${rand(1,2.5)}s;animation-delay:-${rand(0,2.5)}s`;
  river.appendChild(g);
}
for(let i=0;i<6;i++){
  const rf=document.createElement('div');rf.className='reflection';
  rf.style.cssText=`left:${rand(5,80)}%;top:${rand(15,85)}%;
    animation-duration:${rand(2,4)}s;animation-delay:-${rand(0,3)}s`;
  river.appendChild(rf);
}
['rgba(100,90,80,.5)','rgba(120,100,70,.5)','rgba(80,80,80,.4)'].forEach(c=>{
  const s=document.createElement('div');s.className='stone';
  const sw=rand(12,28),sh=rand(8,16);
  s.style.cssText=`width:${sw}px;height:${sh}px;background:${c};left:${rand(5,80)}%;top:${rand(20,80)}%`;
  river.appendChild(s);
});
['🐠','🐟','🐡'].forEach(f=>{
  const el=document.createElement('div');el.className='fish';el.textContent=f;
  el.style.cssText=`bottom:${rand(10,60)}%;animation-duration:${rand(5,9)}s;animation-delay:-${rand(0,8)}s`;
  river.appendChild(el);
});

/* ── Flowers (with flare-bloom-settle reaction to balloon pops) ─ */
const FLOWER_TYPES=[{e:'🌸',s:26},{e:'🌼',s:28},{e:'🌻',s:30},{e:'🌷',s:24},{e:'🌺',s:26},{e:'💐',s:28}];
const flowersLayer=document.getElementById('flowers-layer');
const allFlowers=[];
for(let i=0;i<22;i++){
  const fd=pick(FLOWER_TYPES);
  const wrap=document.createElement('div');wrap.className='flower-wrap';
  wrap.style.cssText=`left:${rand(2,94)}%;bottom:${rand(20,34)}vh`;
  const el=document.createElement('div');el.className='flower';
  el.textContent=fd.e;el.style.fontSize=fd.s+'px';
  el.style.animationDuration=rand(2.2,4.8)+'s';
  el.style.animationDelay='-'+rand(0,4)+'s';
  el.title='Click to bloom!';
  el.onclick=e=>{flareFlower(el);burst(e.pageX,e.pageY,fd.e);};
  wrap.appendChild(el);
  flowersLayer.appendChild(wrap);
  allFlowers.push(el);
}
function flareFlower(el){
  el.classList.add('settling');
  el.classList.add('flaring');
  setTimeout(()=>{
    el.classList.remove('flaring');
    setTimeout(()=>el.classList.remove('settling'), 1800);
  },950);
}
function flareRandomFlowers(count){
  const sample=[...allFlowers].sort(()=>Math.random()-.5).slice(0,count);
  sample.forEach((el,i)=>setTimeout(()=>flareFlower(el), i*60));
}

/* ── Sparkles ─────────────────────────────────────────────────── */
const sparklesLayer=document.getElementById('sparkles-layer');
const sparkleEls=[];
for(let i=0;i<38;i++){
  const sp=document.createElement('div');sp.className='sparkle';
  const sz=rand(3,7);
  sp.style.cssText=`width:${sz}px;height:${sz}px;background:gold;
    left:${rand(0,100)}%;top:${rand(8,85)}%;
    animation-duration:${rand(1.5,4)}s;animation-delay:-${rand(0,4)}s`;
  sparklesLayer.appendChild(sp);
  sparkleEls.push(sp);
}

/* ── Birds / butterflies wandering ───────────────────────────── */
const FLYERS=['🦋','🦋','🦋','🐦'];
const flyersLayer=document.getElementById('flyers-layer');
FLYERS.forEach(emoji=>{
  const el=document.createElement('div');el.className='flyer';el.textContent=emoji;
  let cx=rand(10,85),cy=rand(15,55),tx=cx,ty=cy;
  el.style.cssText=`left:${cx}%;top:${cy}%`;
  flyersLayer.appendChild(el);
  function wander(){
    cx+=(tx-cx)*.018;cy+=(ty-cy)*.018;
    el.style.left=cx+'%';el.style.top=cy+'%';
    if(Math.abs(cx-tx)<.5&&Math.abs(cy-ty)<.5){tx=rand(8,88);ty=rand(12,60);}
    requestAnimationFrame(wander);
  }
  wander();
  setInterval(()=>{tx=rand(8,88);ty=rand(12,60);},rand(3000,7000));
});

/* ── Wind gust engine ───────────────────────────────────────────
   Periodically sends a soft gust across the scene: flower stems
   lean together and balloons drift/sway in the same direction,
   layered on top of their own idle animations. ──────────────── */
function applyWindGust(){
  const strength = rand(8,18);              // degrees for flowers
  const direction = Math.random()<0.5?-1:1;
  const balloonShift = rand(10,28)*direction; // px drift for balloons
  const balloonTilt = rand(3,9)*direction;    // deg tilt for balloons

  document.querySelectorAll('.flower-wrap').forEach(f=>{
    f.style.setProperty('--wind', (strength*direction)+'deg');
  });
  document.querySelectorAll('.balloon-wrap').forEach(b=>{
    b.style.setProperty('--windpx', balloonShift+'px');
    b.style.setProperty('--windrot', balloonTilt+'deg');
  });

  // ease back to rest after the gust passes
  setTimeout(()=>{
    document.querySelectorAll('.flower-wrap').forEach(f=>{
      f.style.setProperty('--wind','0deg');
    });
    document.querySelectorAll('.balloon-wrap').forEach(b=>{
      b.style.setProperty('--windpx','0px');
      b.style.setProperty('--windrot','0deg');
    });
  }, 1500);
}
setInterval(applyWindGust, rand(4500,7000));
setTimeout(applyWindGust, 2000); // first gentle gust soon after load

window.__sceneRefs = {flareRandomFlowers, sparkleEls};
window.__setCanvasNight = (val)=>{ isNight = val; };
</script>

<script>
/* ══════════════════════════════════════════════════════════════
   TEDDY BEAR — SVG render + natural behavior state machine
   States: walking, sitting-pose, sleeping, laptop, eating, dancing
   ══════════════════════════════════════════════════════════════ */
(()=>{
"use strict";
const rand=(a,b)=>Math.random()*(b-a)+a;
const pick=a=>a[Math.floor(Math.random()*a.length)];

const teddyLayer=document.getElementById('teddy-layer');
const teddy=document.createElement('div');
teddy.id='teddy';
teddy.innerHTML=`
<svg id="teddy-svg" width="150" height="190" viewBox="0 0 150 190">
  <defs>
    <radialGradient id="furGrad" cx="40%" cy="30%" r="75%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="70%" stop-color="#f3f3f3"/>
      <stop offset="100%" stop-color="#dcdcdc"/>
    </radialGradient>
    <radialGradient id="furGradLight" cx="40%" cy="30%" r="75%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f0f0f0"/>
    </radialGradient>
  </defs>
  <ellipse cx="75" cy="186" rx="48" ry="8" fill="rgba(0,0,0,.18)"/>

  <!-- body -->
  <ellipse cx="75" cy="138" rx="50" ry="48" fill="url(#furGrad)" stroke="#999999" stroke-width="3"/>
  <ellipse cx="75" cy="146" rx="27" ry="25" fill="url(#furGradLight)"/>

  <!-- legs -->
  <ellipse cx="52" cy="178" rx="17" ry="12" fill="url(#furGrad)" stroke="#999999" stroke-width="2.5"/>
  <ellipse cx="98" cy="178" rx="17" ry="12" fill="url(#furGrad)" stroke="#999999" stroke-width="2.5"/>

  <!-- left arm -->
  <g id="larm" style="transform-origin:32px 128px">
    <rect x="20" y="118" width="22" height="38" rx="11" fill="url(#furGrad)" stroke="#999999" stroke-width="2.5" transform="rotate(18,31,128)"/>
  </g>
  <!-- right arm (holds item depending on state) -->
  <g id="rarm" style="transform-origin:118px 128px">
    <rect x="106" y="116" width="22" height="38" rx="11" fill="url(#furGrad)" stroke="#999999" stroke-width="2.5" transform="rotate(-18,117,126)"/>
  </g>

  <!-- head -->
  <ellipse cx="75" cy="70" rx="52" ry="50" fill="url(#furGrad)" stroke="#999999" stroke-width="3"/>
  <!-- ears -->
  <circle cx="30" cy="28" r="19" fill="url(#furGrad)" stroke="#999999" stroke-width="2.5"/>
  <circle cx="120" cy="28" r="19" fill="url(#furGrad)" stroke="#999999" stroke-width="2.5"/>
  <circle cx="30" cy="28" r="9" fill="#ffd9e0"/>
  <circle cx="120" cy="28" r="9" fill="#ffd9e0"/>
  <!-- soft shading under chin/body for depth on white fur -->
  <ellipse cx="75" cy="158" rx="40" ry="14" fill="rgba(180,180,200,.12)"/>
  <!-- muzzle -->
  <ellipse cx="75" cy="84" rx="26" ry="20" fill="url(#furGradLight)"/>

  <!-- eyes group (id for state changes) -->
  <g id="eyes">
    <circle cx="54" cy="64" r="6.5" fill="#3a2415"/>
    <circle cx="96" cy="64" r="6.5" fill="#3a2415"/>
    <circle cx="56" cy="61.5" r="2" fill="white"/>
    <circle cx="98" cy="61.5" r="2" fill="white"/>
  </g>
  <!-- closed eyes (for sleeping) -->
  <g id="eyes-closed" style="display:none">
    <path d="M47,64 Q54,69 61,64" fill="none" stroke="#3a2415" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M89,64 Q96,69 103,64" fill="none" stroke="#3a2415" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <!-- downward-looking eyes (for watching laptop screen) -->
  <g id="eyes-down" style="display:none">
    <circle cx="54" cy="67" r="6.5" fill="#3a2415"/>
    <circle cx="96" cy="67" r="6.5" fill="#3a2415"/>
    <circle cx="54" cy="70" r="2" fill="white"/>
    <circle cx="96" cy="70" r="2" fill="white"/>
  </g>

  <!-- cheeks -->
  <ellipse cx="38" cy="82" rx="13" ry="9" fill="#ff9eb0" opacity=".55"/>
  <ellipse cx="112" cy="82" rx="13" ry="9" fill="#ff9eb0" opacity=".55"/>
  <!-- nose -->
  <ellipse cx="75" cy="86" rx="9" ry="6" fill="#3a2415"/>
  <!-- mouth -->
  <path id="mouth" d="M64,96 Q75,106 86,96" fill="none" stroke="#3a2415" stroke-width="2.5" stroke-linecap="round"/>
</svg>

<!-- Lollipop (visible in walking/idle states) -->
<div id="teddy-lollipop" style="position:absolute;right:-12px;top:8px;z-index:30">
  <svg width="48" height="80" viewBox="0 0 48 80" style="overflow:visible">
    <line x1="24" y1="78" x2="24" y2="40" stroke="#c8a020" stroke-width="3" stroke-linecap="round"/>
    <circle cx="24" cy="30" r="18" fill="white" stroke="#dd2244" stroke-width="2"/>
    <path d="M24,12 A18,18 0 0,1 42,30" fill="#ff4466" opacity=".9"/>
    <path d="M42,30 A18,18 0 0,1 24,48" fill="#ff99bb" opacity=".9"/>
    <path d="M24,48 A18,18 0 0,1 6,30" fill="#ff4466" opacity=".9"/>
    <path d="M6,30 A18,18 0 0,1 24,12" fill="#ff99bb" opacity=".9"/>
    <circle cx="24" cy="30" r="8" fill="white" opacity=".4"/>
    <circle cx="24" cy="30" r="20" fill="none" stroke="#ff4466" stroke-width="2" opacity=".3">
      <animate attributeName="r" values="18;25;18" dur="1.5s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values=".3;0;.3" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <ellipse cx="14" cy="38" rx="6" ry="4" fill="#ff6b81">
      <animateTransform attributeName="transform" type="translate" values="0,0;8,-6;0,0" dur="1s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;0" dur="1s" repeatCount="indefinite"/>
    </ellipse>
  </svg>
</div>

<!-- Laptop (hidden unless laptop state) -->
<div id="teddy-laptop" style="position:absolute;left:18px;bottom:14px;display:none;z-index:30">
  <svg width="70" height="50" viewBox="0 0 70 50">
    <rect x="8" y="2" width="54" height="34" rx="3" fill="#444" stroke="#222" stroke-width="1.5"/>
    <rect x="11" y="5" width="48" height="28" fill="#7fd4ff"/>
    <rect x="2" y="36" width="66" height="6" rx="2" fill="#666" stroke="#222" stroke-width="1"/>
  </svg>
  <div class="laptop-glow" style="width:50px;height:30px;left:10px;top:0"></div>
</div>

<!-- Food bowl (hidden unless eating state) -->
<div id="teddy-food" style="position:absolute;left:6px;bottom:6px;display:none;z-index:30;font-size:30px">🍰</div>

<!-- Zzz for sleeping -->
<div id="teddy-zzz" style="position:absolute;right:6px;top:-10px;display:none">
  <span class="zzz" style="left:0px">💤</span>
</div>
`;
teddyLayer.appendChild(teddy);

/* ── Behavior state machine ─────────────────────────────────── */
const STATES=['walking','pose','sleeping','laptop','eating'];
let currentState='walking';
let stateTimer=null;
let teddyDancing=false;

function setVisualForState(state){
  document.getElementById('teddy-lollipop').style.display = (state==='walking'||state==='pose') ? 'block':'none';
  document.getElementById('teddy-laptop').style.display = state==='laptop' ? 'block':'none';
  document.getElementById('teddy-food').style.display = state==='eating' ? 'block':'none';
  document.getElementById('teddy-zzz').style.display = state==='sleeping' ? 'block':'none';
  document.getElementById('eyes').style.display = (state==='sleeping'||state==='laptop') ? 'none':'block';
  document.getElementById('eyes-closed').style.display = state==='sleeping' ? 'block':'none';
  document.getElementById('eyes-down').style.display = state==='laptop' ? 'block':'none';

  teddy.classList.remove('walking','sleeping','watching');
  if(state==='walking') teddy.classList.add('walking');
  if(state==='sleeping') teddy.classList.add('sleeping');
  if(state==='laptop') teddy.classList.add('watching');

  // mouth shape: smiling normally, 'o' shape while eating
  const mouth=document.getElementById('mouth');
  if(state==='eating'){
    mouth.setAttribute('d','M68,96 Q75,108 82,96 Q75,102 68,96');
  } else {
    mouth.setAttribute('d','M64,96 Q75,106 86,96');
  }

  // food crumb particles while eating
  if(state==='eating'){
    spawnCrumbs();
  }
}

function spawnCrumbs(){
  let n=0;
  const crumbInterval=setInterval(()=>{
    if(currentState!=='eating' || n>=4){clearInterval(crumbInterval);return;}
    n++;
    const c=document.createElement('div');
    c.className='food-crumb';
    c.textContent=pick(['🍰','✨','.']);
    c.style.left=(rand(2,20))+'px';
    c.style.bottom='30px';
    teddy.appendChild(c);
    setTimeout(()=>c.remove(),1500);
  },700);
}

function moveTeddyTo(){
  const maxL=Math.max(10,W()-180);
  teddy.style.left=rand(8,maxL)+'px';
  teddy.style.bottom=rand(24,38)+'vh';
}
function W(){return window.innerWidth;}

function cycleState(){
  if(teddyDancing || finaleActiveCheck()) { scheduleNext(2000); return; }
  // weighted random next state
  const weights=[{s:'walking',w:5},{s:'pose',w:2},{s:'sleeping',w:1.4},{s:'laptop',w:1.6},{s:'eating',w:1.6}];
  const total=weights.reduce((a,b)=>a+b.w,0);
  let r=Math.random()*total, chosen='walking';
  for(const item of weights){ if(r<item.w){chosen=item.s;break;} r-=item.w; }
  currentState=chosen;
  setVisualForState(chosen);

  if(chosen==='walking') moveTeddyTo();
  // duration per state (cinematic pacing)
  const durations={walking:3200, pose:2200, sleeping:4800, laptop:4200, eating:3000};
  scheduleNext(durations[chosen]||3000);
}
function scheduleNext(ms){
  clearTimeout(stateTimer);
  stateTimer=setTimeout(cycleState,ms);
}
function finaleActiveCheck(){ return window.__finaleActive===true; }

// kick off
setVisualForState('walking');
moveTeddyTo();
scheduleNext(2600);

/* ── Click → happy dance + celebratory glow ───────────────────── */
teddy.onclick=()=>{
  if(teddyDancing) return;
  teddyDancing=true;
  clearTimeout(stateTimer);
  teddy.classList.remove('walking','sleeping');
  teddy.classList.add('dancing','glowing');
  setVisualForState('pose');
  document.getElementById('teddy-lollipop').style.display='block';

  const rect=teddy.getBoundingClientRect();
  window.__burst && window.__burst(rect.left+74,rect.top+60,pick(['🎉','🌟','💖','✨','🎊']));
  window.__confetti && window.__confetti(rect.left+74,rect.top+60,18);

  setTimeout(()=>{
    teddy.classList.remove('dancing','glowing');
    teddyDancing=false;
    cycleState();
  },2600);
};

window.__teddyRef = {teddy, triggerGlow:()=>{
  teddy.classList.add('glowing');
  setTimeout(()=>teddy.classList.remove('glowing'),2200);
}};
})();
</script>

<script>
/* ══════════════════════════════════════════════════════════════
   BALLOONS · GIFT BOX · CONFETTI · CAKE · FINALE
   ══════════════════════════════════════════════════════════════ */
(()=>{
"use strict";
const rand=(a,b)=>Math.random()*(b-a)+a;
const pick=a=>a[Math.floor(Math.random()*a.length)];
const TOTAL_BALLOONS_TO_POP=28;
let pops=0, finaleTriggered=false;
window.__finaleActive=false;

/* ── Burst (emoji particles) — kept from previous version ─────── */
function burst(x,y,emoji,count=10){
  for(let i=0;i<count;i++){
    const p=document.createElement('div');p.className='burst';
    p.textContent=emoji;
    const ang=rand(0,Math.PI*2), dist=rand(45,110);
    p.style.cssText=`left:${x}px;top:${y}px;`+
      `--bx:${Math.cos(ang)*dist}px;--by:${Math.sin(ang)*dist}px;`+
      `animation-delay:${rand(0,.15)}s`;
    document.body.appendChild(p);
    setTimeout(()=>p.remove(),1000);
  }
}
window.__burst=burst;

/* ── Confetti burst ─────────────────────────────────────────── */
const CONFETTI_COLORS=['#ff4d6d','#4dabf7','#ffd43b','#69db7c','#b197fc','#ff922b','#f06595','#20c997'];
function confettiBurst(x,y,count=24){
  for(let i=0;i<count;i++){
    const c=document.createElement('div');c.className='confetti';
    const w=rand(5,9), h=rand(8,14);
    const ang=rand(-Math.PI/2-1.1,-Math.PI/2+1.1), dist=rand(80,220);
    const cx=Math.cos(ang)*dist, cy=Math.sin(ang)*dist+rand(40,100);
    c.style.cssText=`left:${x}px;top:${y}px;width:${w}px;height:${h}px;
      background:${pick(CONFETTI_COLORS)};
      --cx:${cx}px;--cy:${cy}px;--cr:${rand(180,720)}deg;
      animation-duration:${rand(1.1,1.8)}s`;
    document.body.appendChild(c);
    setTimeout(()=>c.remove(),2000);
  }
}
window.__confetti=confettiBurst;

/* ── Gift box pop animation ────────────────────────────────────── */
const giftPositions=[];

function giftBoxPop(x,y){
  const ring=document.createElement('div');ring.className='gift-sparkle-ring';
  ring.style.cssText=`left:${x-35}px;top:${y-35}px`;
  document.body.appendChild(ring);
  setTimeout(()=>ring.remove(),1250);

  const g=document.createElement('div');g.className='gift-box';
  g.textContent='🎁';
  g.style.cssText=`left:${x-26}px;top:${y-26}px`;
  document.body.appendChild(g);
  setTimeout(()=>g.remove(),1850);

  // a couple of sparkle stars trailing the gift for extra delight
  [0,1].forEach(i=>{
    setTimeout(()=>{
      const s=document.createElement('div');
      s.textContent='✨';
      s.style.cssText=`position:absolute;left:${x-10+rand(-14,14)}px;top:${y-10}px;
        font-size:18px;pointer-events:none;z-index:121;
        animation:giftPop 1.4s ease-out forwards`;
      document.body.appendChild(s);
      setTimeout(()=>s.remove(),1450);
    }, i*180);
  });

  // a real collectible gift drifts down to the ground for the teddy to find
  const fg=document.createElement('div');
  fg.className='falling-gift';
  fg.textContent='🎁';
  fg.style.left=(x-16)+'px';
  fg.style.top=(window.innerHeight-120)+'px';
  document.body.appendChild(fg);

  giftPositions.push({
    x:x-26,
    y:window.innerHeight-120,
    collected:false,
    element:fg
  });
}

/* ── Flower flare trigger (defined in part1, exposed via window) ─ */
function triggerFlowerFlare(){
  if(window.__sceneRefs && window.__sceneRefs.flareRandomFlowers){
    window.__sceneRefs.flareRandomFlowers(rand(3,6)|0);
  }
}

/* ── Motivational floating message (shown on auto-pop) ─────────── */
const MOTIVATIONAL=[
 "You are amazing! ✨",
 "Keep shining! 🌟",
 "Dream big! 🚀",
 "You can do it! 💖",
 "Magic is within you! 🪄",
 "Today is your day! 🎉"
];
function showMotivation(x,y){
 const msg=document.createElement("div");
 msg.textContent=pick(MOTIVATIONAL);
 msg.style.cssText=`
 position:absolute;
 left:${x}px;
 top:${y}px;
 color:gold;
 font-weight:bold;
 font-size:18px;
 z-index:200;
 animation:msgFloat 3s forwards;
 pointer-events:none;
 `;
 document.body.appendChild(msg);
 setTimeout(()=>msg.remove(),3000);
}

/* ── Balloons ─────────────────────────────────────────────────── */
const BCOLORS=[
  {fill:'#ff4d6d',shine:'#ffb3c2'},{fill:'#4dabf7',shine:'#bfe3ff'},
  {fill:'#ffd43b',shine:'#fff3b0'},{fill:'#69db7c',shine:'#c3f0cb'},
  {fill:'#b197fc',shine:'#ddd0ff'},{fill:'#ff922b',shine:'#ffd1a3'},
  {fill:'#f06595',shine:'#ffc2da'},{fill:'#20c997',shine:'#a8eed4'}
];
const balloonsLayer=document.getElementById('balloons-layer');
let activeBalloons=0;
const MAX_ACTIVE=8;

function makeBalloon(){
  if(finaleTriggered) return;
  if(activeBalloons>=MAX_ACTIVE){ setTimeout(makeBalloon, 600); return; }
  activeBalloons++;

  const wrap=document.createElement('div');wrap.className='balloon-wrap';
  const c=pick(BCOLORS);
  const x=rand(4,90);
  const ht=rand(58,86), wt=ht*.82;
  const swayDur=rand(2.5,4.5);
  wrap.style.cssText=`left:${x}%;bottom:-160px`;

  const body=document.createElement('div');body.className='balloon-body';
  body.style.cssText=`width:${wt}px;height:${ht}px;
    background:radial-gradient(circle at 32% 28%, ${c.shine}, ${c.fill} 75%);
    box-shadow:inset -10px -10px 22px rgba(0,0,0,.18), 0 4px 10px rgba(0,0,0,.12);`;
  body.style.animation=`balloonFloat ${rand(4.5,8)}s ease-in-out infinite`;

  const shine=document.createElement('div');shine.className='balloon-shine';body.appendChild(shine);
  const shine2=document.createElement('div');shine2.className='balloon-shine2';body.appendChild(shine2);

  const ring=document.createElement('div');
  ring.style.cssText=`position:absolute;inset:-4px;border-radius:inherit;
    border:2px solid rgba(255,255,255,.32);
    animation:shimmerPulse ${rand(1.5,2.5)}s ease-in-out infinite`;
  body.appendChild(ring);

  const knot=document.createElement('div');
  knot.style.cssText=`position:absolute;bottom:-9px;left:50%;transform:translateX(-50%);
    width:10px;height:9px;background:${c.fill};border-radius:50% 50% 40% 40%;
    box-shadow:0 2px 3px rgba(0,0,0,.2)`;
  body.appendChild(knot);

  const str=document.createElement('div');str.className='balloon-string';
  str.style.cssText=`height:${rand(60,92)}px;animation-duration:${swayDur}s`;

  wrap.appendChild(body);wrap.appendChild(str);

  function popBalloon(viaClick, clientX, clientY){
    if(wrap.dataset.popped) return;
    wrap.dataset.popped='1';
    activeBalloons--;
    const r=body.getBoundingClientRect();
    const px=clientX ?? (r.left+r.width/2), py=clientY ?? (r.top+r.height/2);

    burst(px,py,pick(['💥','🎉','✨','⭐','🌟']));
    confettiBurst(px,py, viaClick?22:14);
    giftBoxPop(px,py);
    triggerFlowerFlare();

    wrap.remove();

    if(viaClick){
      pops++;
      document.getElementById('pop-ct').textContent=Math.min(pops,TOTAL_BALLOONS_TO_POP);
      if(pops>=TOTAL_BALLOONS_TO_POP && !finaleTriggered){
        finaleTriggered=true;
        window.__finaleActive=true;
        setTimeout(triggerFinale, 500);
        return;
      }
    }
    if(!finaleTriggered) setTimeout(makeBalloon, rand(500,1600));
  }

  body.onclick=e=>{ e.stopPropagation(); popBalloon(true, e.clientX, e.clientY); };
  balloonsLayer.appendChild(wrap);

  /* Rise animation; auto-pop if it floats too high without being clicked */
  const riseDur=rand(11000,18000);
  const startY=-160;
  let startTime=null;
  function rise(t){
    if(wrap.dataset.popped) return;
    if(!startTime) startTime=t;
    const prog=Math.min((t-startTime)/riseDur,1);
    const y=startY + (window.innerHeight+220)*prog;
    wrap.style.bottom=y+'px';
    // auto-burst once it's near the top of the screen
    if(prog>0.86){
      const r=body.getBoundingClientRect();
      showMotivation(r.left+r.width/2, r.top);
      popBalloon(false);
      return;
    }
    if(prog<1) requestAnimationFrame(rise);
  }
  requestAnimationFrame(rise);
}

// shimmer/float keyframes injected once
const ss=document.createElement('style');
ss.textContent=`
@keyframes shimmerPulse{0%,100%{opacity:.15;transform:scale(1)}50%{opacity:.5;transform:scale(1.08)}}
@keyframes balloonFloat{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-20px) rotate(2deg)}}
`;
document.head.appendChild(ss);

for(let i=0;i<8;i++) setTimeout(makeBalloon,i*500);

/* ── Cake (canvas-drawn, 28 glowing candles) ───────────────────── */
const cakeHolder=document.getElementById('cake-canvas-holder');
const cakeCanvas=document.createElement('canvas');
cakeCanvas.width=380; cakeCanvas.height=300;
cakeHolder.appendChild(cakeCanvas);
const cctx=cakeCanvas.getContext('2d');

function drawCake(flicker){
  cctx.clearRect(0,0,380,300);
  // plate shadow
  cctx.beginPath();cctx.ellipse(190,280,150,14,0,0,Math.PI*2);
  cctx.fillStyle='rgba(0,0,0,.18)';cctx.fill();

  // tiers
  const tiers=[
    {y:230,w:300,h:46,color:'#ffb3c6'},
    {y:190,w:240,h:42,color:'#ffd9e6'},
    {y:152,w:180,h:40,color:'#fff0f5'},
  ];
  tiers.forEach(t=>{
    cctx.fillStyle=t.color;
    roundRect(cctx,190-t.w/2,t.y,t.w,t.h,10);
    cctx.fill();
    cctx.strokeStyle='rgba(200,120,150,.5)';cctx.lineWidth=2;cctx.stroke();
    // drip icing
    cctx.fillStyle='rgba(255,255,255,.85)';
    for(let i=0;i<t.w/18;i++){
      const dx=190-t.w/2+i*18+rand(0,6);
      cctx.beginPath();
      cctx.moveTo(dx,t.y);
      cctx.quadraticCurveTo(dx+9,t.y+rand(8,18),dx+18,t.y);
      cctx.fill();
    }
  });

  // candles (28) on top tier
  const topY=152, candleCount=28;
  for(let i=0;i<candleCount;i++){
    const angle=(i/candleCount)*Math.PI*2;
    const rx=70*Math.cos(angle)*0.55+190;
    const depth=Math.sin(angle)*10; // slight 3D scatter
    const cy=topY-2+depth*0.3;
    const cx=rx;
    // stick
    cctx.fillStyle=i%2===0?'#fff':'#aee8ff';
    cctx.fillRect(cx-1.5,cy-22,3,22);
    // flame glow
    const flick=flicker?rand(.7,1):1;
    const fg=cctx.createRadialGradient(cx,cy-26,0,cx,cy-26,9*flick);
    fg.addColorStop(0,'rgba(255,240,180,.9)');
    fg.addColorStop(1,'rgba(255,180,60,0)');
    cctx.fillStyle=fg;
    cctx.beginPath();cctx.arc(cx,cy-26,9*flick,0,Math.PI*2);cctx.fill();
    // flame
    cctx.fillStyle='#ffb703';
    cctx.beginPath();
    cctx.moveTo(cx,cy-32*flick);
    cctx.quadraticCurveTo(cx+4,cy-24,cx,cy-18);
    cctx.quadraticCurveTo(cx-4,cy-24,cx,cy-32*flick);
    cctx.fill();
    cctx.fillStyle='#fff3b0';
    cctx.beginPath();cctx.ellipse(cx,cy-23,1.6,3.2,0,0,Math.PI*2);cctx.fill();
  }

  // topper
  cctx.font='28px serif';
  cctx.fillText('🎂',172,135);
}
function roundRect(c,x,y,w,h,r){
  c.beginPath();
  c.moveTo(x+r,y);
  c.arcTo(x+w,y,x+w,y+h,r);
  c.arcTo(x+w,y+h,x,y+h,r);
  c.arcTo(x,y+h,x,y,r);
  c.arcTo(x,y,x+w,y,r);
  c.closePath();
}
let cakeFlickerOn=false;
function cakeLoop(){ drawCake(cakeFlickerOn); requestAnimationFrame(cakeLoop); }
cakeLoop();

/* ── Finale sequence ────────────────────────────────────────────── */
/* ── Fireworks (finale burst across the sky) ───────────────────── */
function firework(x,y){
  const fw=document.createElement("div");
  fw.className="firework";
  fw.textContent="🎆";
  fw.style.left=x+"px";
  fw.style.top=y+"px";
  document.body.appendChild(fw);
  setTimeout(()=>fw.remove(),1500);
}
function launchFireworks(){
  for(let i=0;i<40;i++){
    setTimeout(()=>{
      firework(
        rand(100,window.innerWidth-100),
        rand(50,window.innerHeight/2)
      );
    },i*150);
  }
}

function triggerFinale(){
  cakeFlickerOn=true;
  document.getElementById('cake-wrap').classList.add('show');

  // big confetti + glow on teddy
  const cx=window.innerWidth/2, cy=window.innerHeight/2;
  for(let i=0;i<5;i++) setTimeout(()=>confettiBurst(rand(0,window.innerWidth), rand(0,200), 16), i*180);
  if(window.__teddyRef) window.__teddyRef.triggerGlow();
  triggerFlowerFlare();
  launchFireworks();

  setTimeout(()=>{
    document.getElementById('final-msg').classList.add('show');
    confettiBurst(cx,cy,60);
  }, 900);

  // keep gentle confetti raining for a while
  let rainCount=0;
  const rainInterval=setInterval(()=>{
    confettiBurst(rand(0,window.innerWidth), -10, 6);
    rainCount++;
    if(rainCount>16) clearInterval(rainInterval);
  },500);
}

/* ── Day/Night toggle (manual + auto) ─────────────────────────────── */
window.toggleNight=function(manual){
  isNightGlobalToggle();
};
function isNightGlobalToggle(){
  const body=document.getElementById('body');
  const willBeNight=!body.classList.contains('night');
  body.classList.toggle('night',willBeNight);
  document.getElementById('hud-label').textContent = willBeNight ? '🌙 Night Mode' : '☀️ Day Mode';
  window.__isNightFlag = willBeNight;
  // sync the module-scoped isNight flag used by canvas loop in part1
  if(window.__setCanvasNight) window.__setCanvasNight(willBeNight);
}

/* ── Teddy gift collection: periodically walk to the nearest
   uncollected gift on the ground and "pick it up" ──────────────── */
function collectNearbyGift(){
 if(!giftPositions.length) return;
 const teddy=document.getElementById('teddy');
 if(!teddy) return;
 const teddyRect=teddy.getBoundingClientRect();
 let nearest=null;
 let nearestDistance=999999;
 giftPositions.forEach(g=>{
   if(g.collected) return;
   const d=Math.abs(
      teddyRect.left-g.x
   );
   if(d<nearestDistance){
      nearestDistance=d;
      nearest=g;
   }
 });
 if(!nearest) return;
 nearest.collected=true;
 teddy.style.left=nearest.x+"px";
 setTimeout(()=>{
   burst(
      nearest.x,
      nearest.y,
      "🎁",
      10
   );
   nearest.element.remove();
 },2500);
}
setInterval(collectNearbyGift,7000);
})();
</script>

</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    log.info("Starting Enchanted Birthday Scene on http://0.0.0.0:%d", port)
    app.run(host="0.0.0.0", port=port, debug=False)
