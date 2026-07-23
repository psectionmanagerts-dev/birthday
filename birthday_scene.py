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
  - Large festive cake with 25 lit, flickering candles appears at the
    finale, alongside a custom "Happy Birthday ABC" message.

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
#river{position:absolute;bottom:0;left:0;width:100%;height:22vh;
  background:linear-gradient(180deg,#3fb8e0 0%,#1E90FF 45%,#0d6fc7 100%);
  overflow:hidden;z-index:2;transition:filter 4s;
  box-shadow:0 -4px 14px rgba(0,60,120,.25) inset}
body.night #river{filter:brightness(.42) hue-rotate(15deg)}
/* Flowing current stripes — the actual "water flowing" motion */
.current-stripe{position:absolute;height:100%;top:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.16) 40%,rgba(255,255,255,.28) 50%,rgba(255,255,255,.16) 60%,transparent);
  animation:currentFlow linear infinite}
@keyframes currentFlow{0%{transform:translateX(-100%)}100%{transform:translateX(100vw)}}
/* Gentle wave undulation on the surface */
.wave-layer{position:absolute;left:0;width:200%;height:18px;top:0;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.3) 0 24px,transparent 24px 60px);
  animation:waveSlide linear infinite;opacity:.55}
@keyframes waveSlide{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
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
@keyframes swim{0%{left:2%;transform:scaleX(1)}49%{left:92%;transform:scaleX(1)}
  50%{left:92%;transform:scaleX(-1)}100%{left:2%;transform:scaleX(-1)}}
.stone{position:absolute;background:rgba(110,95,75,.55);border-radius:50%}

/* ── Flowers ───────────────────────────────────────── */
.flower-wrap{position:absolute;cursor:pointer;z-index:4;width:20px;height:70px;
  transform-origin:bottom center;
  transform:rotate(var(--wind,0deg));transition:transform .9s ease-out}
.flower{display:block;position:absolute;animation:flowerSway ease-in-out infinite;
  transform-origin:bottom center;transition:filter .4s, transform .4s}
@keyframes flowerSway{0%,100%{transform:translateX(-50%) rotate(-5deg)}50%{transform:translateX(-50%) rotate(5deg)}}
.flower.flaring{
  filter:drop-shadow(0 0 14px gold) drop-shadow(0 0 26px #fff89a) drop-shadow(0 0 38px #ffe98a) brightness(1.6);
  transform:translateX(-50%) scale(2) !important;
  animation:none !important;
}
.flower.settling{
  transition:transform 1.8s cubic-bezier(.34,1.2,.4,1), filter 1.8s ease-out;
}

/* ── Jojo character animations ─────────────────────── */
#teddy{position:absolute;cursor:pointer;z-index:25;
  transition:left 2.4s cubic-bezier(.45,0,.2,1), bottom 2.4s cubic-bezier(.45,0,.2,1);
}

/* Idle breathing — whole body rises/falls gently */
#teddy svg#teddy-svg{
  animation:jojoIdle 2.8s ease-in-out infinite;
  overflow:visible;
  filter:drop-shadow(2px 5px 7px rgba(180,80,100,.22));
  transition:filter .6s;
}
@keyframes jojoIdle{
  0%,100%{transform:translateY(0) scale(1)}
  50%{transform:translateY(-4px) scale(1.012)}
}

/* Walking — bouncy left-right sway with foot lift */
#teddy.walking svg#teddy-svg{animation:jojoBob .5s ease-in-out infinite}
@keyframes jojoBob{
  0%,100%{transform:translateY(0) rotate(-4deg) scale(1)}
  25%{transform:translateY(-10px) rotate(-2deg) scale(1.02)}
  50%{transform:translateY(0) rotate(4deg) scale(1)}
  75%{transform:translateY(-10px) rotate(2deg) scale(1.02)}
}
#teddy.walking #leg-left{animation:legStepL .5s ease-in-out infinite}
#teddy.walking #leg-right{animation:legStepR .5s ease-in-out infinite}
#teddy.walking #larm{animation:armSwingL .5s ease-in-out infinite}
#teddy.walking #rarm{animation:armSwingR .5s ease-in-out infinite}
@keyframes legStepL{0%,100%{transform:rotate(-24deg) translateY(0)}50%{transform:rotate(24deg) translateY(-4px)}}
@keyframes legStepR{0%,100%{transform:rotate(24deg) translateY(-4px)}50%{transform:rotate(-24deg) translateY(0)}}
@keyframes armSwingL{0%,100%{transform:rotate(16deg)}50%{transform:rotate(-14deg)}}
@keyframes armSwingR{0%,100%{transform:rotate(-16deg)}50%{transform:rotate(14deg)}}

/* Bows wiggle gently when walking */
#teddy.walking #bow-left{animation:bowWiggleL .5s ease-in-out infinite}
#teddy.walking #bow-right{animation:bowWiggleR .5s ease-in-out infinite}
@keyframes bowWiggleL{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(8deg)}}
@keyframes bowWiggleR{0%,100%{transform:rotate(8deg)}50%{transform:rotate(-8deg)}}

/* Heart pulse (always on) */
#jojo-heart{animation:heartPulse 1.1s ease-in-out infinite}
@keyframes heartPulse{
  0%,100%{transform:scale(1) rotate(0deg)}
  30%{transform:scale(1.25) rotate(-5deg)}
  60%{transform:scale(1.1) rotate(3deg)}
}

/* Sleeping */
#teddy.sleeping svg#teddy-svg{animation:jojoSleep 3.5s ease-in-out infinite}
@keyframes jojoSleep{
  0%,100%{transform:rotate(-2deg) translateY(0)}
  50%{transform:rotate(2deg) translateY(-3px)}
}

/* Laptop watching */
#teddy.watching svg#teddy-svg{
  animation:jojoWatch 2.2s ease-in-out infinite;
  transform-origin:80px 140px;
}
@keyframes jojoWatch{
  0%,100%{transform:rotate(-2deg)}
  50%{transform:rotate(2deg) translateY(-2px)}
}

/* Happy dance — exuberant Jojo bounce */
#teddy.dancing svg#teddy-svg{
  animation:jojoDance .36s ease-in-out infinite !important;
}
@keyframes jojoDance{
  0%{transform:rotate(-16deg) translateY(-8px) scale(1.06)}
  25%{transform:rotate(0deg) translateY(-18px) scale(1.14)}
  50%{transform:rotate(16deg) translateY(-8px) scale(1.06)}
  75%{transform:rotate(0deg) translateY(-18px) scale(1.14)}
  100%{transform:rotate(-16deg) translateY(-8px) scale(1.06)}
}
/* Bows go wild during dance */
#teddy.dancing #bow-left{animation:bowDanceL .36s ease-in-out infinite}
#teddy.dancing #bow-right{animation:bowDanceR .36s ease-in-out infinite}
@keyframes bowDanceL{0%,100%{transform:rotate(-20deg)}50%{transform:rotate(20deg)}}
@keyframes bowDanceR{0%,100%{transform:rotate(20deg)}50%{transform:rotate(-20deg)}}

/* Celebratory golden glow */
#teddy.glowing svg{filter:drop-shadow(0 0 16px gold) drop-shadow(0 0 32px #ffe9a8) drop-shadow(0 0 5px #ffccdd)}

.zzz{position:absolute;font-size:22px;opacity:0;pointer-events:none;color:#b0a0ff;
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

/* ── Falling gift (collectible, clickable) ────────────── */
.falling-gift{
  position:absolute;
  pointer-events:none;   /* disabled during fall; JS enables after landing */
  cursor:pointer;
  z-index:60;
  font-size:34px;
  filter:drop-shadow(0 3px 6px rgba(0,0,0,.25));
}
.falling-gift:hover{
  filter:drop-shadow(0 0 12px rgba(255,210,120,.9)) drop-shadow(0 3px 6px rgba(0,0,0,.25));
}
@keyframes giftIdleBob{
  0%,100%{transform:translateY(0) rotate(-3deg)}
  50%{transform:translateY(-7px) rotate(3deg)}
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

/* ── Quote card — vivid reveal when a fallen gift is opened ───── */
.quote-card{
  position:absolute;
  transform:translateX(-50%) scale(.3);
  z-index:230;
  pointer-events:none;
  background:linear-gradient(135deg,rgba(255,255,255,.95),rgba(255,240,250,.9));
  color:#7a3a8f;
  font-weight:700;
  font-size:16px;
  padding:10px 18px;
  border-radius:20px;
  white-space:nowrap;
  box-shadow:0 0 0 2px rgba(255,210,230,.8), 0 0 22px rgba(255,200,230,.7), 0 6px 14px rgba(0,0,0,.15);
  animation:quoteReveal 3.4s cubic-bezier(.34,1.5,.4,1) forwards;
}
@keyframes quoteReveal{
  0%{opacity:0;transform:translateX(-50%) scale(.3) translateY(10px)}
  15%{opacity:1;transform:translateX(-50%) scale(1.12) translateY(-6px)}
  25%{transform:translateX(-50%) scale(1) translateY(-10px)}
  78%{opacity:1;transform:translateX(-50%) scale(1) translateY(-46px)}
  100%{opacity:0;transform:translateX(-50%) scale(.92) translateY(-78px)}
}

/* ── Butterflies / birds ───────────────────────────── */
.flyer{position:absolute;z-index:18;pointer-events:none;font-size:22px}
.bird-flyer{font-size:26px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.15))}
@keyframes birdFlyRight{
  0%{left:-40px;transform:scaleX(1) translateY(0)}
  25%{transform:scaleX(1) translateY(-18px)}
  50%{transform:scaleX(1) translateY(6px)}
  75%{transform:scaleX(1) translateY(-10px)}
  100%{left:108vw;transform:scaleX(1) translateY(0)}
}
@keyframes birdFlyLeft{
  0%{right:-40px;transform:scaleX(-1) translateY(0)}
  25%{transform:scaleX(-1) translateY(-18px)}
  50%{transform:scaleX(-1) translateY(6px)}
  75%{transform:scaleX(-1) translateY(-10px)}
  100%{right:108vw;transform:scaleX(-1) translateY(0)}
}

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
#score{position:fixed;top:14px;right:18px;z-index:200;font-size:13px;font-weight:700;
  background:rgba(255,255,255,.28);backdrop-filter:blur(6px);
  border:1px solid rgba(255,255,255,.35);border-radius:20px;padding:6px 14px;
  color:#333;transition:color 4s}
body.night #score{color:#eee}
#hint{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);font-size:12px;
  color:rgba(0,0,0,.5);background:rgba(255,255,255,.3);border-radius:20px;
  padding:4px 14px;z-index:200;text-align:center}
body.night #hint{color:rgba(255,255,255,.55)}

@keyframes introStarFloat{0%,100%{transform:translateY(0) rotate(0deg);opacity:.6}
  50%{transform:translateY(-22px) rotate(180deg);opacity:1}}

/* ── Pop-ripple shockwave ──────────────────────────────── */
.pop-ripple{position:fixed;border-radius:50%;pointer-events:none;z-index:90;
  border:3px solid rgba(255,255,255,.7);
  animation:popRippleOut .9s ease-out forwards}
@keyframes popRippleOut{
  0%{transform:translate(-50%,-50%) scale(0);opacity:.8}
  100%{transform:translate(-50%,-50%) scale(1);opacity:0}
}

/* ── Musical notes floating from teddy ─────────────────── */
.music-note{position:absolute;pointer-events:none;z-index:70;
  font-size:18px;animation:noteFloat ease-out forwards}
@keyframes noteFloat{
  0%{opacity:0;transform:translateY(0) scale(.6) rotate(-10deg)}
  20%{opacity:1;transform:translateY(-14px) scale(1) rotate(5deg)}
  100%{opacity:0;transform:translateY(-70px) scale(.8) rotate(15deg)}
}

/* ── Fireworks canvas ───────────────────────────────────── */
#fireworks-canvas{position:fixed;inset:0;width:100%;height:100%;
  pointer-events:none;z-index:240;opacity:0;transition:opacity .6s}
#fireworks-canvas.active{opacity:1}

/* ── Rainbow arc ───────────────────────────────────────── */
#rainbow{position:fixed;bottom:30vh;left:50%;transform:translateX(-50%) scaleY(0);
  width:min(90vw,700px);height:min(45vw,350px);
  border-radius:min(45vw,350px) min(45vw,350px) 0 0;
  background:conic-gradient(from 180deg at 50% 100%,
    #ff0000,#ff7700,#ffee00,#00bb00,#0066ff,#8800ff,#ff0000);
  opacity:0;z-index:5;pointer-events:none;
  transition:transform 2s cubic-bezier(.34,1.2,.4,1), opacity 1.8s ease;
  mask:radial-gradient(ellipse 100% 100% at 50% 100%, transparent 76%, black 77%)}
#rainbow.show{transform:translateX(-50%) scaleY(1);opacity:.55}

/* ── Petal rain ─────────────────────────────────────────── */
.petal-rain{position:fixed;top:-30px;pointer-events:none;z-index:85;font-size:18px;
  animation:petalDrift linear forwards}
@keyframes petalDrift{
  0%{transform:translateY(0) rotate(0deg) translateX(0);opacity:1}
  100%{transform:translateY(110vh) rotate(720deg) translateX(var(--pdx));opacity:0}
}

/* ── Shooting star ──────────────────────────────────────── */
.shooting-star{position:fixed;pointer-events:none;z-index:88;
  width:3px;height:3px;border-radius:50%;background:white;
  box-shadow:0 0 6px 2px white;
  animation:shootStar linear forwards}
@keyframes shootStar{
  0%{opacity:1;transform:translate(0,0)}
  100%{opacity:0;transform:translate(var(--ssx),var(--ssy))}
}
.shooting-star::after{content:"";position:absolute;right:3px;top:50%;
  transform:translateY(-50%);
  width:clamp(40px,8vw,120px);height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.8))}

/* ── Crown on teddy during finale ───────────────────────── */
#teddy-crown{position:absolute;top:-38px;left:50%;transform:translateX(-50%);
  font-size:36px;opacity:0;z-index:30;
  transition:opacity .5s ease, transform .6s cubic-bezier(.34,1.8,.4,1)}
#teddy-crown.show{opacity:1;transform:translateX(-50%) translateY(-6px)}

/* ── Mobile responsive ────────────────────────────────── */
@media(max-width:768px){
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
<canvas id="fireworks-canvas"></canvas>
<div id="aurora"></div>
<div id="rainbow"></div>

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
  <h1>🎉 Happy Birthday ABC 🎉</h1>
  <p>✨ Wishing you a magical year ahead ✨</p>
</div>

<div id="score">🎈 Popped: <span id="pop-ct">0</span> / 25</div>
<div id="hint">🧸 Click teddy for a happy dance • 🎈 Pop all 25 balloons for a surprise!</div>

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
const CYCLE_MS = 120000; // auto-cycle day→night every 120s, no manual control
setInterval(()=>{ if(window.toggleNight) window.toggleNight(); }, CYCLE_MS);

/* ── River: ripples / glints / reflections / stones / fish ───── */
const river=document.getElementById('river');
/* Flowing current — diagonal light stripes sweeping across, giving real "water flow" motion */
for(let i=0;i<4;i++){
  const cs=document.createElement('div');cs.className='current-stripe';
  cs.style.cssText=`width:${rand(120,220)}px;left:${i*30}%;
    animation-duration:${rand(3.5,5.5)}s;animation-delay:-${rand(0,5)}s;
    transform:skewX(-18deg)`;
  river.appendChild(cs);
}
/* Surface wave undulation */
for(let i=0;i<3;i++){
  const wl=document.createElement('div');wl.className='wave-layer';
  wl.style.cssText=`top:${i*30+6}%;animation-duration:${rand(2.5,4)}s;
    animation-direction:${i%2?'reverse':'normal'}`;
  river.appendChild(wl);
}
for(let i=0;i<10;i++){
  const r=document.createElement('div');r.className='ripple';
  const s=rand(25,75);
  r.style.cssText=`width:${s}px;height:${s}px;left:${rand(5,80)}%;top:${rand(10,80)}%;
    animation-duration:${rand(1.8,3.2)}s;animation-delay:-${rand(0,3)}s;
    border-radius:${rand(40,60)}% ${rand(40,60)}%`;
  river.appendChild(r);
}
for(let i=0;i<18;i++){
  const g=document.createElement('div');g.className='glint';
  g.style.cssText=`width:${rand(3,6)}px;height:${rand(3,6)}px;left:${rand(2,98)}%;top:${rand(10,85)}%;
    animation-duration:${rand(1,2.5)}s;animation-delay:-${rand(0,2.5)}s`;
  river.appendChild(g);
}
for(let i=0;i<8;i++){
  const rf=document.createElement('div');rf.className='reflection';
  rf.style.cssText=`left:${rand(2,95)}%;top:${rand(15,80)}%;
    animation-duration:${rand(2,4)}s;animation-delay:-${rand(0,3)}s`;
  river.appendChild(rf);
}
['rgba(100,90,80,.5)','rgba(120,100,70,.5)','rgba(80,80,80,.4)'].forEach(c=>{
  for(let i=0;i<3;i++){
    const s=document.createElement('div');s.className='stone';
    const sw=rand(14,30),sh=rand(9,17);
    s.style.cssText=`width:${sw}px;height:${sh}px;background:${c};left:${rand(2,95)}%;top:${rand(60,88)}%`;
    river.appendChild(s);
  }
});
['🐠','🐟','🐡'].forEach(f=>{
  const el=document.createElement('div');el.className='fish';el.textContent=f;
  el.style.cssText=`bottom:${rand(20,60)}%;animation-duration:${rand(6,10)}s;animation-delay:-${rand(0,8)}s`;
  river.appendChild(el);
});

/* ── Flowers (rooted at the bottom edge, stems growing upward) ── */
const FLOWER_TYPES=[{e:'🌸',s:26},{e:'🌼',s:28},{e:'🌻',s:30},{e:'🌷',s:24},{e:'🌺',s:26},{e:'💐',s:28}];
const flowersLayer=document.getElementById('flowers-layer');
const allFlowers=[];
for(let i=0;i<22;i++){
  const fd=pick(FLOWER_TYPES);
  const wrap=document.createElement('div');wrap.className='flower-wrap';
  // Rooted right at the ground line; small jitter so they don't form a perfect row
  const stemH=rand(26,54);
  wrap.style.cssText=`left:${rand(1,96)}%;bottom:${rand(20,23)}vh`;

  const stem=document.createElement('div');
  stem.style.cssText=`width:3px;height:${stemH}px;margin:0 auto;
    background:linear-gradient(180deg,#3aad3a,#2d8a2d);border-radius:2px;
    transform-origin:bottom center`;
  wrap.appendChild(stem);

  const el=document.createElement('div');el.className='flower';
  el.style.cssText=`left:50%;bottom:${stemH-6}px;font-size:${fd.s}px`;
  el.textContent=fd.e;
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

/* ── Butterflies: wander near flowers ─────────────────────────── */
const BUTTERFLIES=['🦋','🦋','🦋'];
const flyersLayer=document.getElementById('flyers-layer');
BUTTERFLIES.forEach(emoji=>{
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

/* ── Birds: distinct gliding flight across the sky, periodic flocks ─ */
function spawnBird(){
  const el=document.createElement('div');el.className='flyer bird-flyer';
  el.textContent='🐦';
  const fromLeft = Math.random()<0.5;
  const flyY = rand(6,30); // upper sky band, well above flowers/teddy
  const dur = rand(8,13);
  el.style.cssText = fromLeft
    ? `left:-40px;top:${flyY}%;transform:scaleX(1);animation:birdFlyRight ${dur}s linear forwards`
    : `right:-40px;top:${flyY}%;transform:scaleX(-1);animation:birdFlyLeft ${dur}s linear forwards`;
  flyersLayer.appendChild(el);
  setTimeout(()=>el.remove(), dur*1000+200);
}
// frequent small flocks of 2-4 birds, so the sky rarely feels empty
function birdWave(){
  const count = 2+Math.floor(Math.random()*3);
  for(let i=0;i<count;i++) setTimeout(spawnBird, i*400);
  setTimeout(birdWave, rand(4000,7000));
}
setTimeout(birdWave, 800);
spawnBird(); // one immediately on load so the sky isn't empty at first paint

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

/* ── Musical notes from teddy while walking ──────────────────────── */
const NOTES=['🎵','🎶','🎼','♪','♫'];
function spawnMusicNote(){
  const t=document.getElementById('teddy');
  if(!t || !t.classList.contains('walking')) return;
  const r=t.getBoundingClientRect();
  const note=document.createElement('div');
  note.className='music-note';
  note.textContent=pick(NOTES);
  note.style.cssText=`position:fixed;left:${r.left+rand(10,r.width-10)}px;
    top:${r.top+10}px;animation-duration:${rand(1.4,2.2)}s`;
  document.body.appendChild(note);
  setTimeout(()=>note.remove(),2300);
}
setInterval(spawnMusicNote,900);

/* ── Shooting stars (night only) ────────────────────────────────── */
function spawnShootingStar(){
  if(!isNight) return;
  const ss=document.createElement('div');ss.className='shooting-star';
  const startX=rand(10,70), startY=rand(5,35);
  const dist=rand(180,320), angle=rand(25,55);
  ss.style.cssText=`left:${startX}vw;top:${startY}vh;
    --ssx:${Math.cos(angle*Math.PI/180)*dist}px;
    --ssy:${Math.sin(angle*Math.PI/180)*dist}px;
    animation-duration:${rand(.7,1.2)}s`;
  document.body.appendChild(ss);
  setTimeout(()=>ss.remove(),1300);
}
setInterval(spawnShootingStar, rand(3000,6000));
setInterval(()=>{
  const ms=rand(3000,6000);
  setTimeout(spawnShootingStar,ms);
}, 5000);

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
<svg id="teddy-svg" width="170" height="215" viewBox="0 0 160 210" style="overflow:visible">
<defs>
  <radialGradient id="jFaceG" cx="42%" cy="35%" r="72%">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="75%" stop-color="#fdf6f0"/>
    <stop offset="100%" stop-color="#f8ede3"/>
  </radialGradient>
  <radialGradient id="jHatG" cx="40%" cy="30%" r="75%">
    <stop offset="0%" stop-color="#ffd0de"/>
    <stop offset="100%" stop-color="#f5a8bc"/>
  </radialGradient>
  <radialGradient id="jDressG" cx="40%" cy="20%" r="80%">
    <stop offset="0%" stop-color="#ffb8c8"/>
    <stop offset="100%" stop-color="#f094ae"/>
  </radialGradient>
  <radialGradient id="jSkirtG" cx="50%" cy="0%" r="80%">
    <stop offset="0%" stop-color="#ffd8e6"/>
    <stop offset="100%" stop-color="#ffbcd0"/>
  </radialGradient>
  <radialGradient id="jEarG" cx="40%" cy="35%" r="70%">
    <stop offset="0%" stop-color="#5a2e2e"/>
    <stop offset="100%" stop-color="#2d1515"/>
  </radialGradient>
  <radialGradient id="jBowG" cx="30%" cy="30%" r="70%">
    <stop offset="0%" stop-color="#ffd0de"/>
    <stop offset="100%" stop-color="#f090ac"/>
  </radialGradient>
  <radialGradient id="jBlushG" cx="50%" cy="50%" r="60%">
    <stop offset="0%" stop-color="#ff9aaa" stop-opacity=".8"/>
    <stop offset="100%" stop-color="#ff7090" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="jArmG" cx="38%" cy="30%" r="70%">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="100%" stop-color="#f8ede3"/>
  </radialGradient>
  <radialGradient id="jFootG" cx="40%" cy="30%" r="70%">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="100%" stop-color="#f0e4dc"/>
  </radialGradient>
  <filter id="jDs" x="-15%" y="-10%" width="130%" height="130%">
    <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="rgba(180,80,100,.18)"/>
  </filter>
</defs>

<!-- ground shadow -->
<ellipse cx="80" cy="206" rx="44" ry="6" fill="rgba(180,100,110,.12)"/>

<!-- FEET -->
<g id="leg-left" style="transform-origin:58px 195px">
  <ellipse cx="58" cy="198" rx="21" ry="11" fill="url(#jFootG)" stroke="#c88090" stroke-width="1.8"/>
</g>
<g id="leg-right" style="transform-origin:102px 195px">
  <ellipse cx="102" cy="198" rx="21" ry="11" fill="url(#jFootG)" stroke="#c88090" stroke-width="1.8"/>
</g>

<!-- SKIRT -->
<path d="M42,154 Q40,174 42,184 Q55,192 80,192 Q105,192 118,184 Q120,174 118,154 Z"
  fill="url(#jSkirtG)" stroke="#c88090" stroke-width="1.8"/>
<line x1="60" y1="159" x2="58" y2="186" stroke="#f0a0bc" stroke-width="1.2" opacity=".55"/>
<line x1="72" y1="157" x2="71" y2="187" stroke="#f0a0bc" stroke-width="1.2" opacity=".55"/>
<line x1="84" y1="157" x2="84" y2="188" stroke="#f0a0bc" stroke-width="1.2" opacity=".55"/>
<line x1="96" y1="157" x2="98" y2="187" stroke="#f0a0bc" stroke-width="1.2" opacity=".55"/>

<!-- BODY / pink top -->
<path d="M40,118 Q38,143 42,154 L118,154 Q122,143 120,118 Q108,106 80,106 Q52,106 40,118 Z"
  fill="url(#jDressG)" stroke="#c88090" stroke-width="1.8"/>
<path d="M62,106 Q80,116 98,106" fill="none" stroke="#ffd8e6" stroke-width="2.2" stroke-linecap="round"/>

<!-- LEFT ARM (under, behind right) -->
<g id="larm" style="transform-origin:50px 134px">
  <path d="M44,120 Q26,128 24,142 Q23,152 36,155 Q50,158 58,148 Q64,138 58,126 Z"
    fill="url(#jArmG)" stroke="#c8a090" stroke-width="1.6"/>
  <ellipse cx="32" cy="152" rx="14" ry="10" fill="url(#jArmG)" stroke="#c8a090" stroke-width="1.5"/>
</g>

<!-- RIGHT ARM (over) -->
<g id="rarm" style="transform-origin:110px 134px">
  <path d="M116,120 Q134,128 136,142 Q137,152 124,155 Q110,158 102,148 Q96,138 102,126 Z"
    fill="url(#jArmG)" stroke="#c8a090" stroke-width="1.6"/>
  <ellipse cx="128" cy="152" rx="14" ry="10" fill="url(#jArmG)" stroke="#c8a090" stroke-width="1.5"/>
</g>

<!-- HEART held by Jojo — pulses with animation -->
<g id="jojo-heart" style="transform-origin:80px 146px">
  <path d="M80,154 C80,154 67,143 67,137 C67,132 71,129 76,130 C78,130 80,132 80,132
           C80,132 82,130 84,130 C89,129 93,132 93,137 C93,143 80,154 80,154 Z"
    fill="#ff5577" stroke="#dd3355" stroke-width="1.4"/>
  <ellipse cx="73" cy="134" rx="3.5" ry="2.5" fill="rgba(255,255,255,.6)" transform="rotate(-35,73,134)"/>
  <animateTransform attributeName="transform" type="scale"
    values="1;1.18;1;1.12;1" dur="1.2s" repeatCount="indefinite"
    additive="sum"/>
</g>

<!-- HEAD — big white circle -->
<circle cx="80" cy="72" r="60"
  fill="url(#jFaceG)" stroke="#c8a090" stroke-width="2.2"
  filter="url(#jDs)"/>

<!-- PINK HAT DOME (layered above head) -->
<path d="M24,68 Q20,26 80,14 Q140,26 136,68 Q118,54 80,52 Q42,54 24,68 Z"
  fill="url(#jHatG)" stroke="#d080a0" stroke-width="2.2"/>

<!-- HAT SIDE FLAPS -->
<path d="M30,66 Q14,80 16,108 Q20,122 32,118 Q44,112 42,92 Q40,76 30,66 Z"
  fill="url(#jHatG)" stroke="#d080a0" stroke-width="1.8"/>
<path d="M130,66 Q146,80 144,108 Q140,122 128,118 Q116,112 118,92 Q120,76 130,66 Z"
  fill="url(#jHatG)" stroke="#d080a0" stroke-width="1.8"/>

<!-- PANDA EARS (dark brown, sit on hat) -->
<circle cx="36" cy="26" r="21" fill="url(#jEarG)" stroke="#1a0808" stroke-width="1.6"/>
<circle cx="36" cy="26" r="11" fill="#7a4040"/>
<circle cx="124" cy="26" r="21" fill="url(#jEarG)" stroke="#1a0808" stroke-width="1.6"/>
<circle cx="124" cy="26" r="11" fill="#7a4040"/>

<!-- BOWS — left -->
<g id="bow-left" style="transform-origin:40px 50px">
  <path d="M40,50 C28,42 22,46 26,53 C30,58 36,56 40,50 Z"
    fill="url(#jBowG)" stroke="#d880a0" stroke-width="1.3"/>
  <path d="M40,50 C52,42 58,46 54,53 C50,58 44,56 40,50 Z"
    fill="url(#jBowG)" stroke="#d880a0" stroke-width="1.3"/>
  <ellipse cx="40" cy="51" rx="4" ry="3.5" fill="#ffc0d4" stroke="#d880a0" stroke-width="1"/>
  <path d="M37,54 Q32,65 34,70" fill="none" stroke="#efa8c0" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M43,54 Q48,65 46,70" fill="none" stroke="#efa8c0" stroke-width="1.8" stroke-linecap="round"/>
</g>
<!-- BOWS — right -->
<g id="bow-right" style="transform-origin:120px 50px">
  <path d="M120,50 C108,42 102,46 106,53 C110,58 116,56 120,50 Z"
    fill="url(#jBowG)" stroke="#d880a0" stroke-width="1.3"/>
  <path d="M120,50 C132,42 138,46 134,53 C130,58 124,56 120,50 Z"
    fill="url(#jBowG)" stroke="#d880a0" stroke-width="1.3"/>
  <ellipse cx="120" cy="51" rx="4" ry="3.5" fill="#ffc0d4" stroke="#d880a0" stroke-width="1"/>
  <path d="M117,54 Q112,65 114,70" fill="none" stroke="#efa8c0" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M123,54 Q128,65 126,70" fill="none" stroke="#efa8c0" stroke-width="1.8" stroke-linecap="round"/>
</g>

<!-- FACE FEATURES -->
<!-- happy squint eyes (default Jojo expression) -->
<g id="eyes">
  <path d="M51,70 Q62,61 73,70" fill="none" stroke="#3a1818" stroke-width="3.2" stroke-linecap="round"/>
  <path d="M87,70 Q98,61 109,70" fill="none" stroke="#3a1818" stroke-width="3.2" stroke-linecap="round"/>
  <!-- tiny lash ticks -->
  <line x1="51" y1="70" x2="48" y2="66" stroke="#3a1818" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="73" y1="70" x2="76" y2="66" stroke="#3a1818" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="87" y1="70" x2="84" y2="66" stroke="#3a1818" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="109" y1="70" x2="112" y2="66" stroke="#3a1818" stroke-width="1.6" stroke-linecap="round"/>
</g>
<!-- sleeping eyes -->
<g id="eyes-closed" style="display:none">
  <path d="M51,70 Q62,78 73,70" fill="none" stroke="#3a1818" stroke-width="3" stroke-linecap="round"/>
  <path d="M87,70 Q98,78 109,70" fill="none" stroke="#3a1818" stroke-width="3" stroke-linecap="round"/>
</g>
<!-- laptop watching — slight downward squint -->
<g id="eyes-down" style="display:none">
  <path d="M51,73 Q62,64 73,73" fill="none" stroke="#3a1818" stroke-width="3.2" stroke-linecap="round"/>
  <path d="M87,73 Q98,64 109,73" fill="none" stroke="#3a1818" stroke-width="3.2" stroke-linecap="round"/>
</g>

<!-- tiny nose dot -->
<circle cx="80" cy="84" r="3.2" fill="#3a1818"/>

<!-- MOUTH — happy W shape with tongue peek -->
<path id="mouth" d="M67,92 Q80,106 93,92" fill="#ff6688" stroke="#3a1818" stroke-width="2" stroke-linecap="round"/>
<ellipse cx="80" cy="100" rx="8" ry="6" fill="#ff4466"/>
<ellipse cx="80" cy="98" rx="5.5" ry="3.5" fill="#ff88aa" opacity=".65"/>

<!-- BLUSH — big rosy ovals -->
<ellipse cx="42" cy="84" rx="20" ry="14" fill="url(#jBlushG)"/>
<ellipse cx="118" cy="84" rx="20" ry="14" fill="url(#jBlushG)"/>
<!-- blush sparkle dots -->
<circle cx="30" cy="82" r="1.6" fill="#ffaac0" opacity=".7"/>
<circle cx="35" cy="76" r="1.1" fill="#ffaac0" opacity=".5"/>
<circle cx="130" cy="82" r="1.6" fill="#ffaac0" opacity=".7"/>
<circle cx="125" cy="76" r="1.1" fill="#ffaac0" opacity=".5"/>

</svg>

<!-- Lollipop hidden in Jojo mode - she holds a heart instead -->
<div id="teddy-lollipop" style="display:none"></div>

<!-- Laptop -->
<div id="teddy-laptop" style="position:absolute;left:18px;bottom:18px;display:none;z-index:30">
  <svg width="70" height="50" viewBox="0 0 70 50">
    <rect x="8" y="2" width="54" height="34" rx="4" fill="#3a3a5c" stroke="#222" stroke-width="1.5"/>
    <rect x="11" y="5" width="48" height="28" fill="#7fd4ff"/>
    <rect x="16" y="10" width="38" height="4" rx="2" fill="rgba(255,255,255,.4)"/>
    <rect x="16" y="17" width="28" height="4" rx="2" fill="rgba(255,255,255,.3)"/>
    <rect x="2" y="36" width="66" height="6" rx="2" fill="#555" stroke="#222" stroke-width="1"/>
  </svg>
  <div class="laptop-glow" style="width:50px;height:30px;left:10px;top:0"></div>
</div>

<!-- Food -->
<div id="teddy-food" style="position:absolute;left:6px;bottom:10px;display:none;z-index:30;font-size:32px">🍰</div>

<!-- Zzz -->
<div id="teddy-zzz" style="position:absolute;right:4px;top:-12px;display:none">
  <span class="zzz">💤</span>
</div>

<!-- Crown — finale -->
<div id="teddy-crown">👑</div>
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
const TOTAL_BALLOONS_TO_POP=25;
let pops=0, finaleTriggered=false, nightTriggeredAt14=false;
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

function giftBoxPop(popX, popY){
  /* ── Stage 0: sparkle ring + floating gift-box emoji at pop site ── */
  const ring=document.createElement('div');ring.className='gift-sparkle-ring';
  ring.style.cssText=`left:${popX-35}px;top:${popY-35}px`;
  document.body.appendChild(ring);
  setTimeout(()=>ring.remove(),1250);

  const g=document.createElement('div');g.className='gift-box';
  g.textContent='🎁';
  g.style.cssText=`left:${popX-26}px;top:${popY-26}px`;
  document.body.appendChild(g);
  setTimeout(()=>g.remove(),1850);

  // sparkle trails at the pop site
  [0,1].forEach(i=>{
    setTimeout(()=>{
      const s=document.createElement('div');
      s.textContent='✨';
      s.style.cssText=`position:absolute;left:${popX-10+rand(-14,14)}px;top:${popY-10}px;
        font-size:18px;pointer-events:none;z-index:121;
        animation:giftPop 1.4s ease-out forwards`;
      document.body.appendChild(s);
      setTimeout(()=>s.remove(),1450);
    }, i*180);
  });

  /* ── Stage 1: gift falls from balloon position to ground ─────────
     🤫 appears AUTOMATICALLY mid-fall (not on click).
     Quote appears AUTOMATICALLY after landing (not on click).
     Click on settled gift = pops it open with sparkle burst only.  */
  const landY  = window.innerHeight - 110;
  const startY = Math.max(popY, 60);
  const fallDur= 1800;

  const fg=document.createElement('div');
  fg.className='falling-gift';
  fg.textContent='🎁';
  fg.style.cssText=`left:${popX-16}px;top:${startY}px;
    animation:none;opacity:0;transform:scale(.5) rotate(-15deg);
    pointer-events:none`;   // not clickable during fall
  fg.dataset.opened='0';
  document.body.appendChild(fg);
  giftPositions.push({x:popX-26, y:landY, collected:false, element:fg});

  let shhShown=false;
  let t0=null;
  function animateFall(ts){
    if(!t0) t0=ts;
    const prog=Math.min((ts-t0)/fallDur,1);
    const eased=prog*prog;
    const cy=startY+(landY-startY)*eased;
    fg.style.top=cy+'px';
    fg.style.opacity=String(Math.min(prog*4,1));
    fg.style.transform=`scale(${.5+.5*prog}) rotate(${-15+15*prog}deg)`;

    // rainbow trail particles during fall
    if(Math.random()<.16 && window.__spawnGiftTrail){
      window.__spawnGiftTrail(popX, cy);
    }

    // 🤫 appears automatically at 45% through the fall — clearly mid-air
    if(prog>=0.45 && !shhShown){
      shhShown=true;
      const shh=document.createElement('div');
      shh.textContent='🤫';
      shh.style.cssText=`position:fixed;left:${popX+22}px;top:${cy-18}px;
        font-size:30px;pointer-events:none;z-index:220;opacity:1;
        transition:transform 1s ease-out, opacity 1s ease-out`;
      document.body.appendChild(shh);
      requestAnimationFrame(()=>requestAnimationFrame(()=>{
        shh.style.transform='translateY(-50px) scale(.75)';
        shh.style.opacity='0';
      }));
      setTimeout(()=>shh.remove(),1100);
    }

    if(prog<1){ requestAnimationFrame(animateFall); return; }

    /* ── Gift landed: bounce → idle bob → quote auto-reveals → clickable ── */
    fg.style.transition='transform .22s ease-out';
    fg.style.transform='scale(1.18) rotate(0deg)';
    setTimeout(()=>{
      fg.style.transform='scale(1) rotate(0deg)';
      setTimeout(()=>{
        fg.style.transition='';
        fg.style.animation='giftIdleBob 1.8s ease-in-out infinite';
        fg.style.filter='drop-shadow(0 3px 8px rgba(0,0,0,.22))';
        // gift is now clickable — click just pops it open
        fg.style.pointerEvents='auto';
        fg.style.cursor='pointer';
        fg.addEventListener('click',(e)=>{
          e.stopPropagation();
          if(fg.dataset.opened==='1') return;
          fg.dataset.opened='1';
          openFallenGift(fg);
        });

        // Quote auto-pops 400ms after gift fully settles
        setTimeout(()=>{
          if(fg.isConnected && fg.dataset.opened==='0'){
            const r=fg.getBoundingClientRect();
            revealQuote(r.left+r.width/2, r.top-20);
          }
        }, 400);

      }, 200);
    }, 240);

    // auto-fade if nobody clicks after 14s
    setTimeout(()=>{
      if(fg.dataset.opened==='0' && fg.isConnected){
        fg.style.animation='none';
        fg.style.transition='opacity 1.2s ease, transform 1.2s ease';
        fg.style.opacity='0';
        fg.style.transform='scale(.55) rotate(15deg)';
        setTimeout(()=>fg.remove(),1300);
      }
    }, 14000);
  }
  requestAnimationFrame(animateFall);
}

/* ── Click on SETTLED gift: pop open + sparkle burst only ──────────
   Shush already happened mid-fall. Quote already auto-revealed.
   Click is just the satisfying "open" moment.                    ── */
function openFallenGift(fg){
  const r=fg.getBoundingClientRect();
  const cx=r.left+r.width/2, cy=r.top+r.height/2;
  fg.style.animation='none';
  fg.style.transition='transform .28s cubic-bezier(.34,1.56,.64,1), opacity .28s ease';
  fg.style.transform='scale(1.6) rotate(-14deg)';
  setTimeout(()=>{ fg.style.opacity='0'; fg.style.transform='scale(.1) rotate(30deg)'; },260);
  setTimeout(()=>fg.isConnected && fg.remove(),580);
  burst(cx,cy,'✨',12);
  confettiBurst(cx,cy,10);
}

/* ── Flower flare trigger (defined in part1, exposed via window) ─ */
function triggerFlowerFlare(){
  if(window.__sceneRefs && window.__sceneRefs.flareRandomFlowers){
    window.__sceneRefs.flareRandomFlowers(rand(3,6)|0);
  }
}

/* ── 25 unique birthday quotes — one revealed per gift opened ──── */
const BIRTHDAY_QUOTES=[
  "You are the best! 💖",
  "It's your day today! 🎉",
  "Wishing you endless joy! ✨",
  "You make the world brighter! 🌟",
  "Keep shining always! 🌈",
  "Dream big, today and always! 🚀",
  "You are truly one of a kind! 🦄",
  "May your heart stay this happy! 😊",
  "Here's to another magical year! 🎂",
  "You deserve all the love today! 💕",
  "Your smile lights up the room! 😄",
  "Celebrate you — you're amazing! 🥳",
  "Today is all about you! 🎈",
  "May your wishes all come true! 🌠",
  "You bring so much joy to others! 🌸",
  "Stay wonderful, just as you are! 🌷",
  "Another year wiser and brighter! 📚",
  "You're a gift to everyone around you! 🎁",
  "Sending you warmth and sweetness! 🍰",
  "Here's to new adventures ahead! 🗺️",
  "You light up every room you enter! 💡",
  "May happiness follow you all year! 🍀",
  "You are loved more than you know! 💗",
  "Cheers to you on your special day! 🥂",
  "Your kindness makes the world better! 🌻",
  "May this year bring you magic! 🪄",
  "You're stronger than you realize! 💪",
  "Forever grateful you exist! 🙏"
];

/* ── Reveal a quote card — vivid, glowing, gently floats up ─────── */
function revealQuote(x,y){
  const card=document.createElement('div');
  card.className='quote-card';
  card.textContent=pick(BIRTHDAY_QUOTES);
  card.style.cssText=`left:${x}px;top:${y}px`;
  document.body.appendChild(card);
  setTimeout(()=>card.remove(),3400);
}

/* ── Motivational floating message (shown when a balloon auto-pops) ─── */
function showMotivation(x,y){
 const msg=document.createElement("div");
 msg.textContent=pick(BIRTHDAY_QUOTES);
 msg.style.cssText=`
 position:absolute;
 left:${x}px;
 top:${y}px;
 color:gold;
 font-weight:bold;
 font-size:16px;
 z-index:200;
 animation:msgFloat 3s forwards;
 pointer-events:none;
 text-shadow:0 0 8px rgba(255,210,80,.6);
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
    spawnPopRipple(px,py);

    wrap.remove();

    if(viaClick){
      pops++;
      document.getElementById('pop-ct').textContent=Math.min(pops,TOTAL_BALLOONS_TO_POP);

      // Special moment: 14th balloon smoothly transitions the scene into night
      if(pops===13 && !nightTriggeredAt14){
        nightTriggeredAt14=true;
        setTimeout(()=>{ if(window.toggleNight) window.toggleNight(); }, 400);
      }

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
  const topY=152, candleCount=25;
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

/* ══════════════════════════════════════════════════════════════
   EXTRAVAGANZA FEATURES
   ══════════════════════════════════════════════════════════════ */

/* ── Pop-ripple shockwave ring on every balloon pop ──────────── */
function spawnPopRipple(x,y){
  const r=document.createElement('div');r.className='pop-ripple';
  const size=Math.min(window.innerWidth,window.innerHeight)*.9;
  r.style.cssText=`left:${x}px;top:${y}px;width:${size}px;height:${size}px`;
  document.body.appendChild(r);
  setTimeout(()=>r.remove(),950);
}

/* ── Canvas fireworks engine ─────────────────────────────────── */
(()=>{
  const fc=document.getElementById('fireworks-canvas');
  const fctx=fc.getContext('2d');
  let fW=fc.width=innerWidth, fH=fc.height=innerHeight;
  addEventListener('resize',()=>{fW=fc.width=innerWidth;fH=fc.height=innerHeight;});
  const particles=[];
  const FW_COLORS=['#ff4d6d','#ffd43b','#69db7c','#4dabf7','#b197fc','#ff922b','#f06595','#fff'];
  class FWParticle{
    constructor(x,y,color){
      this.x=x;this.y=y;this.color=color;
      const ang=rand(0,Math.PI*2);
      const spd=rand(2,9);
      this.vx=Math.cos(ang)*spd; this.vy=Math.sin(ang)*spd;
      this.life=1; this.decay=rand(.012,.028);
      this.r=rand(2,4);
      this.trail=[[x,y],[x,y]];
    }
    update(){
      this.trail.unshift([this.x,this.y]);
      if(this.trail.length>8) this.trail.pop();
      this.vy+=.09; this.vx*=.97; this.vy*=.97;
      this.x+=this.vx; this.y+=this.vy;
      this.life-=this.decay;
    }
    draw(){
      fctx.save();
      fctx.globalAlpha=this.life;
      fctx.strokeStyle=this.color;
      fctx.lineWidth=this.r*.6;
      fctx.lineCap='round';
      fctx.beginPath();
      fctx.moveTo(this.trail[0][0],this.trail[0][1]);
      this.trail.forEach(p=>fctx.lineTo(p[0],p[1]));
      fctx.stroke();
      fctx.fillStyle=this.color;
      fctx.shadowColor=this.color; fctx.shadowBlur=6;
      fctx.beginPath();fctx.arc(this.x,this.y,this.r,0,Math.PI*2);fctx.fill();
      fctx.restore();
    }
  }
  function launchShell(x,y){
    const color=pick(FW_COLORS);
    const count=rand(60,100)|0;
    for(let i=0;i<count;i++) particles.push(new FWParticle(x,y,color));
    // secondary sparkle ring
    for(let i=0;i<20;i++){
      const p=new FWParticle(x,y,'white');
      p.vx*=.35; p.vy*=.35;
      particles.push(p);
    }
  }
  let fwActive=false,fwLoop=null;
  function startFWLoop(){
    fc.classList.add('active');
    fwActive=true;
    function draw(){
      if(!fwActive) return;
      fctx.fillStyle='rgba(0,0,0,.18)';
      fctx.fillRect(0,0,fW,fH);
      for(let i=particles.length-1;i>=0;i--){
        particles[i].update();
        particles[i].draw();
        if(particles[i].life<=0) particles.splice(i,1);
      }
      fwLoop=requestAnimationFrame(draw);
    }
    draw();
  }
  function stopFWLoop(){
    fwActive=false;
    if(fwLoop) cancelAnimationFrame(fwLoop);
    fctx.clearRect(0,0,fW,fH);
    fc.classList.remove('active');
  }
  window.launchFireworks=function(){
    startFWLoop();
    const positions=[
      [fW*.2,fH*.22],[fW*.5,fH*.12],[fW*.8,fH*.2],
      [fW*.35,fH*.3],[fW*.65,fH*.18],[fW*.1,fH*.35],[fW*.9,fH*.3]
    ];
    positions.forEach((pos,i)=>setTimeout(()=>launchShell(pos[0],pos[1]),i*380));
    // continuous volleys
    let volleys=0;
    const volley=setInterval(()=>{
      launchShell(rand(fW*.1,fW*.9), rand(fH*.08,fH*.38));
      volleys++;
      if(volleys>18) clearInterval(volley);
    },520);
    setTimeout(stopFWLoop, 14000);
  };
})();

/* ── Petal rain during finale ────────────────────────────────── */
function startPetalRain(){
  const petals=['🌸','🌺','🌷','🌼','🌻','💮'];
  let count=0;
  const iv=setInterval(()=>{
    const p=document.createElement('div');p.className='petal-rain';
    p.textContent=pick(petals);
    p.style.cssText=`left:${rand(0,100)}vw;
      animation-duration:${rand(3.5,6.5)}s;animation-delay:${rand(0,.8)}s;
      font-size:${rand(14,24)}px;--pdx:${rand(-80,80)}px`;
    document.body.appendChild(p);
    setTimeout(()=>p.remove(),7000);
    count++;
    if(count>60) clearInterval(iv);
  },150);
}

/* ── Rainbow reveal ──────────────────────────────────────────── */
function showRainbow(){
  const rb=document.getElementById('rainbow');
  rb.classList.add('show');
  setTimeout(()=>rb.classList.remove('show'),9000);
}

/* ── Gift trail particles during fall ────────────────────────── */
function spawnGiftTrail(x,y){
  const colors=['#ff4d6d','#ffd43b','#69db7c','#4dabf7','#b197fc'];
  const t=document.createElement('div');
  t.style.cssText=`position:fixed;left:${x+rand(-8,8)}px;top:${y}px;
    width:6px;height:6px;border-radius:50%;pointer-events:none;z-index:65;
    background:${pick(colors)};opacity:1;
    transition:transform ${rand(.6,1)}s ease-out, opacity ${rand(.6,1)}s ease-out`;
  document.body.appendChild(t);
  requestAnimationFrame(()=>{
    t.style.transform=`translate(${rand(-30,30)}px,${rand(10,40)}px) scale(0)`;
    t.style.opacity='0';
  });
  setTimeout(()=>t.remove(),1100);
}
window.__spawnGiftTrail=spawnGiftTrail;

function triggerFinale(){
  cakeFlickerOn=true;

  const cx=window.innerWidth/2, cy=window.innerHeight/2;

  // Immediate: fireworks + flower flare + teddy glow
  launchFireworks();
  triggerFlowerFlare();
  if(window.__teddyRef) window.__teddyRef.triggerGlow();

  // 400ms: rainbow arcs across sky
  setTimeout(showRainbow, 400);

  // 600ms: cake slides up
  setTimeout(()=>document.getElementById('cake-wrap').classList.add('show'), 600);

  // 800ms: crown appears on teddy + teddy dances
  setTimeout(()=>{
    const crown=document.getElementById('teddy-crown');
    if(crown) crown.classList.add('show');
    const teddy=document.getElementById('teddy');
    if(teddy){
      teddy.classList.remove('walking','sleeping','watching');
      teddy.classList.add('dancing','glowing');
    }
  }, 800);

  // 900ms: confetti volleys + final message
  setTimeout(()=>{
    document.getElementById('final-msg').classList.add('show');
    confettiBurst(cx, cy, 70);
    for(let i=0;i<5;i++) setTimeout(()=>confettiBurst(rand(0,window.innerWidth),rand(0,220),18),i*200);
  }, 900);

  // 1200ms: petal rain begins
  setTimeout(startPetalRain, 1200);

  // Continuous confetti rain
  let rainCount=0;
  const rainInterval=setInterval(()=>{
    confettiBurst(rand(0,window.innerWidth),-10,8);
    rainCount++;
    if(rainCount>22) clearInterval(rainInterval);
  },400);
}

/* ── Day/Night toggle (manual + auto) ─────────────────────────────── */
window.toggleNight=function(){
  autoToggleNight();
};
function autoToggleNight(){
  const body=document.getElementById('body');
  const willBeNight=!body.classList.contains('night');
  body.classList.toggle('night',willBeNight);
  window.__isNightFlag = willBeNight;
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
