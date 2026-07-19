#!/usr/bin/env python3
"""VOLTA frontend builder — emits preview/app.html. Edit THIS file, never app.html.
Zero frameworks. One artifact: web + PWA. Server is the source of truth.
Design spec: ~/healthapp/app-screens.html — match, don't approximate."""
import pathlib

OUT = pathlib.Path(__file__).parent / "app.html"

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>VOLTA</title>
<style>
:root{
  --bg:#06070a; --panel:#0d0f14; --panel2:#11141b; --line:#1c212c;
  --txt:#e8ecf3; --dim:#8b93a5; --faint:#5a6274;
  --green:#3ddc84; --amber:#ffb340; --red:#ff5a5a; --cyan:#41d6e8; --violet:#9b7bff;
}
body.light{
  --bg:#f4f5f7; --panel:#ffffff; --panel2:#ffffff; --line:#e2e4ea;
  --txt:#12141a; --dim:#4a5162; --faint:#8b93a5;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",Helvetica,Arial,sans-serif;min-height:100vh}
.glow{position:fixed;inset:0;pointer-events:none;background:
  radial-gradient(700px 500px at 15% 0%,rgba(61,220,132,.07),transparent 60%),
  radial-gradient(700px 500px at 85% 20%,rgba(65,214,232,.05),transparent 60%),
  radial-gradient(800px 600px at 50% 100%,rgba(155,123,255,.06),transparent 60%)}
body.light .glow{opacity:.5}
#app{position:relative;max-width:420px;margin:0 auto;min-height:100vh;display:flex;flex-direction:column;padding:0 18px env(safe-area-inset-bottom)}
@media(min-width:480px){#app{border-left:1px solid var(--line);border-right:1px solid var(--line);background:var(--panel)}}
.screen{flex:1;display:flex;flex-direction:column;padding-top:10px}
.status{display:flex;justify-content:space-between;align-items:center;font-size:10px;color:var(--faint);padding:12px 2px;letter-spacing:.14em}
.status .ctl{cursor:pointer;letter-spacing:.08em}
.status .ctl:hover{color:var(--dim)}
.t-xs{font-size:10px;letter-spacing:.18em;color:var(--faint)}
.t-q{font-size:22px;font-weight:800;letter-spacing:-.01em;line-height:1.25;margin:8px 0 4px}
.t-hint{font-size:13px;color:var(--dim);line-height:1.5}
.big{font-size:50px;font-weight:800;letter-spacing:-.03em;line-height:1}
.lvl{font-size:10px;letter-spacing:.2em;color:var(--green);text-align:center}
.chip{display:inline-block;font-size:10px;padding:3px 9px;border-radius:99px;border:1px solid var(--line);color:var(--dim);vertical-align:middle}
.opt{border:1px solid var(--line);background:var(--panel2);border-radius:14px;padding:13px 14px;margin-top:10px;font-size:13.5px;font-weight:600;display:flex;align-items:center;gap:10px;cursor:pointer;user-select:none}
.opt.sel{border-color:var(--green);background:rgba(61,220,132,.08)}
.opt .em{font-size:16px}
.opt small{display:block;font-weight:400;color:var(--faint);font-size:11px;margin-top:2px}
.opt .st{margin-left:auto;font-size:9px;letter-spacing:.1em;color:var(--faint);flex-shrink:0}
.opt.sel .st{color:var(--green)}
.seg{display:flex;gap:8px;margin-top:10px}
.seg .opt{flex:1;justify-content:center;text-align:center;padding:12px 4px;font-size:13px;margin-top:0}
.inp{width:100%;background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:13px;color:var(--txt);font-size:15px;margin-top:10px}
.inp:focus{outline:none;border-color:var(--cyan)}
.inp-row{display:flex;gap:10px}
.inp-row .inp{text-align:center;font-size:18px;font-weight:800}
.inp-row .inp::placeholder{font-size:12px;font-weight:400}
.btn{margin-top:16px;background:linear-gradient(90deg,var(--green),var(--cyan));color:#04110a;font-weight:800;text-align:center;padding:14px;border-radius:14px;font-size:14.5px;cursor:pointer;border:none;width:100%}
.btn.push{margin-top:auto}
.btn.ghost{background:none;border:1px solid var(--line);color:var(--dim)}
.btn:disabled{opacity:.4}
.dots{display:flex;gap:5px;justify-content:center;margin:16px 0 4px}
.dot{width:6px;height:6px;border-radius:50%;background:var(--line)}
.dot.on{background:var(--green)}
.card{background:var(--panel2);border:1px solid var(--line);border-radius:16px;padding:14px;margin-top:12px}
.card h4{font-size:10px;letter-spacing:.15em;color:var(--faint);font-weight:600;margin-bottom:10px}
.card p{font-size:12px;color:var(--dim);line-height:1.55}
.wf-row{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);font-size:12.5px}
.wf-row:last-child{border-bottom:none}
.wf-name{flex:1;color:var(--dim)}
.wf-val{font-variant-numeric:tabular-nums;font-weight:700}
.pos{color:var(--green)} .neg{color:var(--red)} .neu{color:var(--amber)}
.cap-row{display:flex;justify-content:space-between;font-size:12px;color:var(--dim);padding:6px 0}
.cap-row b{color:var(--txt)}
.ring-c{display:flex;justify-content:center;padding:10px 0 4px}
.meter{height:8px;border-radius:4px;background:var(--line);overflow:hidden;margin-top:8px}
.meter i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--green),var(--cyan))}
.tick{display:flex;justify-content:space-between;font-size:9px;color:var(--faint);margin-top:4px;letter-spacing:.06em}
.note{font-size:10.5px;color:var(--faint);text-align:center;margin-top:12px;line-height:1.55}
.chk{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);font-size:13px;cursor:pointer}
.chk:last-child{border-bottom:none}
.chk .box{width:22px;height:22px;border-radius:7px;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0}
.chk.done .box{background:var(--green);border-color:var(--green);color:#04110a}
.chk .lbl{flex:1}
.chk .rv{font-size:11.5px;font-weight:700;color:var(--faint);font-variant-numeric:tabular-nums}
.chk.done .rv{color:var(--green)}
.streak{display:flex;gap:5px;justify-content:space-between;margin-top:4px}
.streak div{width:100%;height:14px;border-radius:4px;background:var(--line)}
.streak div.on{background:var(--green)}
.err{color:var(--red);font-size:12px;margin-top:8px;text-align:center;min-height:15px}
.center{text-align:center}
.spin{color:var(--faint);text-align:center;padding:40px;font-size:13px}
.nav{display:flex;justify-content:space-around;border-top:1px solid var(--line);padding:12px 0 16px;margin-top:auto}
.nav div{font-size:9px;color:var(--faint);letter-spacing:.08em;cursor:pointer}
.nav .on{color:var(--green)}
svg{display:block}
.axis{font-size:8px;fill:var(--faint)}
.grid{stroke:var(--line);stroke-width:1}
</style>
</head>
<body>
<div class="glow"></div>
<div id="app"></div>
<script>
const API = window.VOLTA_API || '';
let T = localStorage.getItem('volta_token') || null;
let S = {screen: T ? 'loading' : 'auth', mode: 'login', surveyStep: 0, survey: {}, sensors: JSON.parse(localStorage.getItem('volta_sensors')||'[]'), today: null, weekly: null, err: ''};
if(localStorage.getItem('volta_theme')==='light') document.body.classList.add('light');
function toggleTheme(){
  document.body.classList.toggle('light');
  localStorage.setItem('volta_theme', document.body.classList.contains('light')?'light':'dark');
}

const $ = sel => document.querySelector(sel);
async function api(path, method='GET', body=null){
  const r = await fetch(API + path, {
    method,
    headers: {'content-type':'application/json', ...(T?{authorization:'Bearer '+T}:{})},
    body: body ? JSON.stringify(body) : null
  });
  const d = await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(typeof d.detail==='string' ? d.detail : 'Something went wrong — try again');
  return d;
}
function save(){ localStorage.setItem('volta_token', T); }
function logout(){ localStorage.removeItem('volta_token'); T=null; S={screen:'auth',mode:'login',surveyStep:0,survey:{},sensors:S.sensors,err:''}; render(); }

/* ---------- shared pieces ---------- */
function clock(){ const d=new Date(); return d.getHours()+':'+String(d.getMinutes()).padStart(2,'0'); }
function statusBar(label){
  return `<div class="status"><span>${clock()}</span><span>${label}</span>
    <span><span class="ctl" onclick="toggleTheme()">☀/☾</span>&nbsp;&nbsp;<span class="ctl" onclick="logout()">EXIT</span></span></div>`;
}
function levelLine(level){
  return {LOW:'LOW — RECOVERY DAY, PROTECT THE STREAK',
          GOOD:'GOOD — TRAIN MODERATE TODAY',
          CHARGED:'CHARGED — PUSH TODAY, MAKE IT COUNT'}[level] || '';
}
function ringSVG(score, empty=false){
  const c = 528, off = empty ? c : c - (c * score/100);
  return `<svg width="170" height="170" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="84" fill="none" stroke="var(--line)" stroke-width="14"/>
    <circle cx="100" cy="100" r="84" fill="none" stroke="url(#g1)" stroke-width="14" stroke-linecap="round"
      stroke-dasharray="${c}" stroke-dashoffset="${off}" transform="rotate(-90 100 100)"/>
    <defs><linearGradient id="g1"><stop offset="0%" stop-color="#3ddc84"/><stop offset="100%" stop-color="#41d6e8"/></linearGradient></defs>
    <text x="100" y="98" text-anchor="middle" fill="var(--txt)" font-size="50" font-weight="800">${empty?'–':score}</text>
    <text x="100" y="124" text-anchor="middle" fill="var(--faint)" font-size="11" letter-spacing="2">${empty?'NO DATA':score>=70?'CHARGED':score>=40?'GOOD':'LOW'}</text>
  </svg>`;
}
function northStarSVG(bf){
  // display map: bf 10% → x 250 (right end), bf 35%+ → x 10 (left end)
  const x = Math.max(14, Math.min(246, 250 - (bf - 10) / 25 * 240));
  const lx = Math.max(12, Math.min(190, x - 24));
  return `<svg viewBox="0 0 260 120" style="width:100%;margin-top:14px">
    <line class="grid" x1="10" y1="95" x2="250" y2="95"/>
    <rect x="10" y="20" width="240" height="14" rx="7" fill="var(--line)"/>
    <rect x="10" y="20" width="240" height="14" rx="7" fill="url(#nsg)" opacity=".15"/>
    <defs><linearGradient id="nsg"><stop offset="0%" stop-color="#ffb340"/><stop offset="100%" stop-color="#3ddc84"/></linearGradient></defs>
    <rect x="212" y="20" width="38" height="14" rx="7" fill="rgba(61,220,132,.25)"/>
    <circle cx="${x}" cy="27" r="8" fill="#ffb340"/>
    <text class="axis" x="${lx}" y="14" fill="#ffb340">YOU · ${bf}%</text>
    <text class="axis" x="206" y="48" fill="#3ddc84">10–12%</text>
    <text class="axis" x="10" y="112">TODAY</text>
    <text class="axis" x="250" y="112" text-anchor="end">~${Math.max(1,Math.round(bf-12))} MONTHS AT YOUR PACE</text>
  </svg>`;
}

/* ---------- AUTH ---------- */
function viewAuth(){
  return `<div class="screen">
    <div class="center" style="margin-top:70px">
      <div class="t-xs">KNOW YOUR CHARGE</div>
      <div class="t-q" style="font-size:44px;margin-top:8px">VOLTA</div>
      <div class="t-hint" style="margin-top:10px">One number. One action. Proof.</div>
    </div>
    <div style="margin-top:40px">
      <input class="inp" id="email" type="email" placeholder="Email" autocapitalize="none">
      <input class="inp" id="pw" type="password" placeholder="Password">
      <div class="err">${S.err}</div>
      <button class="btn" onclick="doAuth()">${S.mode==='login'?'Log In':'Create Account'}</button>
      <button class="btn ghost" onclick="S.mode=S.mode==='login'?'signup':'login';S.err='';render()">
        ${S.mode==='login'?'New here? Create account':'Have an account? Log in'}</button>
    </div>
  </div>`;
}
async function doAuth(){
  try{
    const d = await api('/api/'+S.mode, 'POST', {email:$('#email').value.trim(), password:$('#pw').value});
    T = d.token; save();
    const t = await api('/api/today');
    S.screen = t.targets && t.targets.protein_target_g ? 'today' : 'survey';
    S.today = t; S.err=''; render();
  }catch(e){ S.err = e.message; render(); }
}

/* ---------- ONBOARDING — sensors first, then only what apps can't know ---------- */
const SENSORS = [
  ['apple','🍎','Apple Health','Steps, workouts, weight'],
  ['oura','💍','Oura Ring','Sleep, HRV, temperature'],
  ['cronometer','🥗','Cronometer','Food, protein, micros'],
  ['fitindex','⚖️','FitIndex Scale','Weight & body-fat trend'],
  ['fitbod','🏋️','Fitbod','Training volume & strength'],
];
const SURVEY_N = 5;
function viewSurvey(){
  const st = S.surveyStep, v = S.survey;
  let body = '';
  if(st===0){
    body = `<div class="t-xs">STEP 1 — PLUG IN YOUR SENSORS</div>
    <div class="t-q">Connect what you already use.</div>
    <div class="t-hint">Whatever your sensors know, you'll never be asked to type.</div>
    ${SENSORS.map(([k,e,n,d])=>`<div class="opt ${S.sensors.includes(k)?'sel':''}" onclick="toggleSensor('${k}')">
      <span class="em">${e}</span><div>${n}<small>${d}</small></div>
      <span class="st">${S.sensors.includes(k)?'✓ LINKED':'TAP TO LINK'}</span></div>`).join('')}
    <div class="note">Live sync is rolling out in updates — until your data flows,<br>anything missing takes 60 seconds by hand. Honest data only.</div>`;
  }else if(st===1){
    body = `<div class="t-xs">NEXT — THE ONLY QUESTION THAT MATTERS</div>
    <div class="t-q">What do you actually want?</div>
    <div class="t-hint">Not what sounds good. What you want.</div>
    ${[['longevity','🧬','Live as long as possible — in a body that works','The longevity path. Everything optimizes for healthspan.'],
       ['lean','🔥','Get lean & stay lean — finally','Reach your number. Keep it. Never diet again.'],
       ['energy','⚡','Energy every single day','Wake up charged. Stop crashing at 3pm.'],
       ['bloodwork','🩸','Fix my bloodwork','Doctor flagged something. Time to move it.']]
      .map(([k,e,l,d])=>`<div class="opt ${v.outcome===k?'sel':''}" onclick="setS('outcome','${k}')"><span class="em">${e}</span><div>${l}<small>${d}</small></div></div>`).join('')}`;
  }else if(st===2){
    body = `<div class="t-xs">NOTHING SYNCED YET — CALIBRATE BY HAND</div>
    <div class="t-q">Where is your body today?</div>
    <div class="t-hint">The moment a sensor connects, it takes over these numbers.</div>
    <div class="inp-row" style="margin-top:12px">
      <input class="inp" id="age" type="number" placeholder="AGE" value="${v.age||''}" oninput="captureBodyInputs()">
      <input class="inp" id="height" type="number" placeholder="HEIGHT (IN)" value="${v.height_in||''}" oninput="captureBodyInputs()">
      <input class="inp" id="weight" type="number" placeholder="WEIGHT (LB)" value="${v.weight_lb||''}" oninput="captureBodyInputs()">
    </div>
    <div class="t-hint" style="margin-top:14px">Estimated body fat</div>
    <div class="seg">${[['','Not sure'],[27,'25–30%'],[22,'20–25%'],[17,'15–20%']].map(([k,l])=>`<div class="opt ${String(v.bf_estimate??'')===String(k)?'sel':''}" onclick="setS('bf_estimate','${k}')">${l}</div>`).join('')}</div>
    <div class="t-hint" style="margin-top:14px">Training days per week</div>
    <div class="seg">${[1,3,5].map(n=>`<div class="opt ${v.training_days===n?'sel':''}" onclick="setS('training_days',${n})">${n===1?'0–1':n===3?'2–3':'4+'}</div>`).join('')}</div>
    <div class="t-hint" style="margin-top:14px">Sleep, most nights</div>
    <div class="seg">${[['<6','&lt;6h'],['6-7','6–7h'],['7+','7h+']].map(([k,l])=>`<div class="opt ${v.sleep_hours===k?'sel':''}" onclick="setS('sleep_hours','${k}')">${l}</div>`).join('')}</div>`;
  }else if(st===3){
    body = `<div class="t-xs">WHAT NO APP CAN KNOW — NO JUDGMENT, ONLY DATA</div>
    <div class="t-q">The truth about your week.</div>
    <div class="t-hint" style="margin-top:12px">Drinks per week</div>
    <div class="seg">${[0,2,6].map(n=>`<div class="opt ${v.drinks_wk===n?'sel':''}" onclick="setS('drinks_wk',${n})">${n===0?'0':n===2?'1–4':'5+'}</div>`).join('')}</div>
    <div class="t-hint" style="margin-top:14px">Your diet, most days</div>
    ${[['whole','Mostly whole foods'],['half','Half whole, half whatever'],['packaged','Mostly restaurants / packaged']].map(([k,l])=>`<div class="opt ${v.diet_honesty===k?'sel':''}" onclick="setS('diet_honesty','${k}')">${l}</div>`).join('')}
    <div class="t-hint" style="margin-top:16px">Working with a doctor on a medical weight-management plan?</div>
    <div class="seg">
      <div class="opt ${v.doctor_plan===true?'sel':''}" onclick="setS('doctor_plan',true)">Yes</div>
      <div class="opt ${v.doctor_plan===false?'sel':''}" onclick="setS('doctor_plan',false)">No</div>
    </div>
    <div class="note">VOLTA never recommends medication. If your doctor does,<br>we track exactly how your body responds.</div>`;
  }else{
    body = `<div class="t-xs">LAST ONE — AND IT'S THE WHOLE GAME</div>
    <div class="t-q">Will you track, honestly, every day?</div>
    <div class="t-hint">The system only works on true data. 60 seconds a day. That's the deal.</div>
    <div class="card" style="margin-top:16px"><h4>WHAT HONEST TRACKING BUYS YOU</h4>
      <div class="wf-row"><span class="wf-name">A number you can trust every morning</span><span class="wf-val pos">Daily</span></div>
      <div class="wf-row"><span class="wf-name">Proof of what works on YOUR body</span><span class="wf-val pos">~90 days</span></div>
      <div class="wf-row"><span class="wf-name">A score that proves you're getting healthier</span><span class="wf-val pos">Monthly</span></div>
      <div class="wf-row"><span class="wf-name">Blood results before the needle</span><span class="wf-val pos">6 months</span></div>
    </div>
    <div class="opt ${v.committed===true?'sel':''}" style="margin-top:14px" onclick="setS('committed',true)"><span class="em">✊</span><div>I'm in. Every day.</div></div>
    <div class="opt ${v.committed===false?'sel':''}" onclick="setS('committed',false)"><div>I want to see how it works first</div></div>`;
  }
  const ready = st===0 ? true
    : st===1 ? !!v.outcome
    : st===2 ? (v.age&&v.height_in&&v.weight_lb&&v.training_days!==undefined&&v.sleep_hours)
    : st===3 ? (v.drinks_wk!==undefined&&v.diet_honesty&&v.doctor_plan!==undefined)
    : v.committed!==undefined;
  return `<div class="screen">
    ${body}
    <div class="dots" style="margin-top:auto">${[...Array(SURVEY_N)].map((_,i)=>`<div class="dot ${i<=st?'on':''}"></div>`).join('')}</div>
    <div class="err">${S.err}</div>
    <button class="btn" style="margin-top:4px" ${ready?'':'disabled'} onclick="surveyNext()">${st===SURVEY_N-1?'Build My Plan →':'Continue →'}</button>
    ${st>0?`<button class="btn ghost" style="margin-top:8px" onclick="S.surveyStep--;S.err='';render()">← Back</button>`:''}
  </div>`;
}
function toggleSensor(k){
  S.sensors = S.sensors.includes(k) ? S.sensors.filter(x=>x!==k) : [...S.sensors, k];
  localStorage.setItem('volta_sensors', JSON.stringify(S.sensors));
  render();
}
function setS(k,val){
  if(S.surveyStep===2 && !['age','height_in','weight_lb'].includes(k)) captureBodyInputs();
  if(k==='bf_estimate') val = val===''?null:parseFloat(val);
  S.survey[k]=val; render();
}
function captureBodyInputs(){
  const a=$('#age'),h=$('#height'),w=$('#weight');
  if(a&&a.value) S.survey.age=parseInt(a.value);
  if(h&&h.value) S.survey.height_in=parseFloat(h.value);
  if(w&&w.value) S.survey.weight_lb=parseFloat(w.value);
}
async function surveyNext(){
  if(S.surveyStep===2){
    captureBodyInputs();
    if(!S.survey.age||!S.survey.height_in||!S.survey.weight_lb){S.err='Fill in age, height and weight';render();return;}
  }
  S.err='';
  if(S.surveyStep<SURVEY_N-1){ S.surveyStep++; render(); return; }
  try{
    const d = await api('/api/survey','POST',{committed:false, ...S.survey});
    S.targets = d.targets; S.screen='northstar'; render();
  }catch(e){ S.err=e.message; render(); }
}

/* ---------- NORTH STAR ---------- */
function viewNorthStar(){
  const t = S.targets;
  return `<div class="screen">
    <div class="t-xs center" style="margin-top:26px">YOUR NORTH STAR</div>
    <div class="center" style="margin-top:8px">
      <div class="big">12<span style="font-size:22px;color:var(--faint)">%</span></div>
      <div class="lvl">BODY FAT — THE TARGET</div>
    </div>
    ${northStarSVG(t.current_bf)}
    <div class="card">
      <div class="cap-row"><span>Today (estimated)</span><b>${t.current_bf}%</b></div>
      <div class="cap-row"><span>Goal weight at 12%</span><b class="pos">${t.goal_weight_lb} lb</b></div>
      <div class="cap-row"><span>Daily protein target</span><b>${t.protein_target_g}g</b></div>
    </div>
    <div class="card"><h4>WHY THIS NUMBER</h4>
      <div class="wf-row"><span class="wf-name">Visceral fat — the dangerous kind — clears out</span></div>
      <div class="wf-row"><span class="wf-name">Insulin sensitivity resets toward optimal</span></div>
      <div class="wf-row"><span class="wf-name">Testosterone &amp; inflammation normalize</span></div>
      <div class="wf-row"><span class="wf-name">Every longevity marker moves at once</span></div>
    </div>
    <div class="note">Not a crash diet. A whole-foods rebuild at a pace<br>your body can hold for decades.</div>
    <button class="btn push" onclick="goToday()">Accept the Target →</button>
  </div>`;
}
async function goToday(){ S.today = await api('/api/today'); S.screen='today'; render(); }

/* ---------- TODAY — the Battery home ---------- */
function viewToday(){
  const d = S.today, b = d.battery;
  return `<div class="screen">
    ${statusBar('VOLTA')}
    <div class="t-xs">TODAY'S BATTERY</div>
    <div class="ring-c">${b?ringSVG(b.score):ringSVG(0,true)}</div>
    <div class="lvl">${b?levelLine(b.level):'LOG YOUR DAY BELOW — THE BATTERY CHARGES FROM DATA'}</div>
    ${b&&b.components.length?`<div style="margin-top:10px">${b.components.map(c=>`<div class="wf-row"><span class="wf-name">${c.label}</span><span class="wf-val ${c.points>0?'pos':'neg'}">${c.points>0?'+':''}${c.points}</span></div>`).join('')}</div>`:''}
    <div class="card" style="border-color:rgba(61,220,132,.3)">
      <h4 style="color:var(--green)">TODAY'S ONE ACTION</h4>
      <p style="font-size:12.5px">${d.one_action.action}</p>
      ${d.tomorrow_projection?`<p style="font-size:11px;color:var(--faint);margin-top:6px">Tomorrow's battery: projected <b class="pos">${d.tomorrow_projection}</b></p>`:''}
    </div>
    <div class="card"><h4>THE 60-SECOND DAY</h4>${quickLog()}</div>
    <div class="card"><h4>STREAK</h4>
      <div class="streak">${[...Array(7)].map((_,i)=>`<div class="${i<Math.min(d.streak,7)?'on':''}"></div>`).join('')}</div>
      <div class="tick"><span>${d.streak}-DAY STREAK</span><span>${d.streak>=7?'ON FIRE':'KEEP IT ALIVE'}</span></div>
    </div>
    ${(d.log&&d.log.whole_foods_score)?`<div class="card"><h4>WHOLE FOODS SCORE TODAY</h4>
      <div class="meter"><i style="width:${d.log.whole_foods_score}%"></i></div>
      <div class="tick"><span>${d.log.whole_foods_score}% WHOLE</span><span class="${d.log.whole_foods_score>=85?'pos':'neu'}">${d.log.whole_foods_score>=85?'EXCELLENT':'FLOOR IS 85%'}</span></div>
    </div>`:''}
    ${nav('today')}
  </div>`;
}
function quickLog(){
  const l = S.today.log || {}, t = S.today.targets || {};
  const row = (field,em,label,val,done) =>
    `<div class="chk ${done?'done':''}" onclick="${field==='trained'?`logField('trained',${l.trained?'false':'true'})`:`logPrompt('${field}')`}">
      <div class="box">${done?'✓':''}</div><div class="lbl">${em} ${label}</div><span class="rv">${val}</span></div>`;
  return row('weight_lb','🌅','Morning weigh-in', l.weight_lb?l.weight_lb+' lb':'—', !!l.weight_lb)
    + row('sleep_quality','😴','Sleep last night', l.sleep_quality?l.sleep_quality+'/10':'—', !!l.sleep_quality)
    + row('energy','⚡','Energy now', l.energy?l.energy+'/10':'—', !!l.energy)
    + row('protein_g','🥩',`Protein — target ${t.protein_target_g||'—'}g`, l.protein_g?Math.round(l.protein_g)+'g':'—', !!l.protein_g)
    + row('trained','🏋️','Trained today', l.trained?'Done':'Pending', !!l.trained)
    + row('drinks','🍷','Drinks', (l.drinks!==undefined&&l.drinks!==null)?String(l.drinks):'—', l.drinks!==undefined&&l.drinks!==null)
    + row('whole_foods_score','🥦','Whole foods %', l.whole_foods_score?l.whole_foods_score+'%':'—', !!l.whole_foods_score);
}
const PROMPTS = {
  weight_lb:'Morning weigh-in (lb)', sleep_quality:'Sleep quality last night (1–10)',
  energy:'Energy right now (1–10)', protein_g:'Protein so far today (g)',
  drinks:'Drinks today (0 if none)', whole_foods_score:'Whole foods score today (0–100)'};
async function logPrompt(field){
  const v = prompt(PROMPTS[field]);
  if(v===null) return;
  await logField(field, parseFloat(v)||0);
}
async function logField(field, value){
  try{
    await api('/api/log','POST',{[field]:value});
    S.today = await api('/api/today');
    render();
  }catch(e){ alert(e.message); }
}

/* ---------- PATH ---------- */
function viewPath(){
  const t = S.today.targets, ph = S.today.phase;
  const day = Math.min(28, Math.max(1, S.today.streak||1));
  return `<div class="screen">
    ${statusBar('PATH')}
    <div class="t-xs">${t.start_bf}% → 12% · PHASE ${ph.number} OF 4</div>
    <div class="t-q" style="font-size:19px">Phase ${ph.number}: ${ph.name} <span class="chip">WKS 1–4</span></div>
    <div class="t-hint">No restriction yet. We install the floor first.</div>
    <div class="card"><h4>THIS PHASE, ONLY 4 THINGS MATTER</h4>
      <div class="wf-row"><span class="wf-name">Hit your protein number daily</span><span class="wf-val">${t.protein_target_g}g</span></div>
      <div class="wf-row"><span class="wf-name">Whole foods only — nothing in a wrapper</span><span class="wf-val">✓</span></div>
      <div class="wf-row"><span class="wf-name">Train 3×/week — full body</span><span class="wf-val">✓</span></div>
      <div class="wf-row"><span class="wf-name">In bed by ${t.bedtime}</span><span class="wf-val">✓</span></div>
    </div>
    <div class="card"><h4>PHASE PROGRESS</h4>
      <div class="meter"><i style="width:${Math.round(day/28*100)}%"></i></div>
      <div class="tick"><span>DAY ${day} OF 28</span><span class="pos">${S.today.streak>=1?'ON TRACK':'START TODAY'}</span></div>
    </div>
    <div class="card"><h4>WHAT'S NEXT — LOCKED</h4>
      <div class="cap-row"><span>Phase 2 · The Deficit</span><b>🔒</b></div>
      <div class="cap-row"><span>Phase 3 · The Refinement</span><b>🔒</b></div>
      <div class="cap-row"><span>Phase 4 · 12% — Maintenance for life</span><b>🔒</b></div>
    </div>
    <div class="note">Phases unlock as you complete them.<br>The plan adapts to your data every week.</div>
    ${nav('path')}
  </div>`;
}

/* ---------- BODY — the rules, locked until earned ---------- */
function viewBody(){
  return `<div class="screen">
    ${statusBar('BODY')}
    <div class="t-xs">EARNED BY ~90 DAYS OF YOUR DATA</div>
    <div class="t-q" style="font-size:19px">What's proven true — for you</div>
    <div class="t-hint">Personal dose-response curves. Not studies — you.</div>
    <div class="card"><h4>YOUR RULES — UNLOCKING</h4>
      <div class="wf-row"><span class="wf-name">Alcohol → your deep sleep</span><span class="wf-val">🔒</span></div>
      <div class="wf-row"><span class="wf-name">Caffeine cutoff → your sleep</span><span class="wf-val">🔒</span></div>
      <div class="wf-row"><span class="wf-name">Sleep debt → next-day eating</span><span class="wf-val">🔒</span></div>
      <div class="wf-row"><span class="wf-name">Protein × training → lean mass</span><span class="wf-val">🔒</span></div>
      <div class="wf-row"><span class="wf-name">Meal timing → your battery</span><span class="wf-val">🔒</span></div>
    </div>
    <div class="card" style="border-color:rgba(65,214,232,.3)">
      <h4 style="color:var(--cyan)">HOW RULES GET WRITTEN</h4>
      <p>Every honest day is evidence. Around day 90 the patterns become statistically yours — sample size and confidence shown on every curve.</p>
    </div>
    <div class="note">These aren't studies. They're you.<br>New rules unlock as your data matures.</div>
    ${nav('body')}
  </div>`;
}

/* ---------- SCORE — the week, graded ---------- */
function viewWeekly(){
  const w = S.weekly;
  if(!w){ return `<div class="screen">${statusBar('SCORE')}<div class="spin">Grading your week…</div>${nav('weekly')}</div>`; }
  const m = w.metrics, t = S.today.targets;
  const climb = Math.max(0, Math.min(100, (t.start_bf - t.current_bf) / Math.max(0.1, t.start_bf - 12) * 100));
  return `<div class="screen">
    ${statusBar('SCORE')}
    <div class="t-xs">YOUR WEEK, GRADED</div>
    <div class="t-q" style="font-size:20px">This week: <span class="pos">${w.grade}</span></div>
    <div class="card"><h4>THE SCOREBOARD</h4>
      <div class="wf-row"><span class="wf-name">Tracking honesty</span><span class="wf-val pos">${m.tracking_days} days</span></div>
      <div class="wf-row"><span class="wf-name">Whole foods</span><span class="wf-val ${m.whole_foods_avg>=85?'pos':'neu'}">${m.whole_foods_avg}%</span></div>
      <div class="wf-row"><span class="wf-name">Protein target</span><span class="wf-val pos">${m.protein_hit_rate}</span></div>
      <div class="wf-row"><span class="wf-name">Training</span><span class="wf-val ${m.training_sessions>=3?'pos':'neu'}">${m.training_sessions}/3 ${m.training_sessions>=3?'✓':''}</span></div>
      <div class="wf-row"><span class="wf-name">Avg battery</span><span class="wf-val pos">${m.avg_battery}</span></div>
      <div class="wf-row"><span class="wf-name">Alcohol</span><span class="wf-val ${m.drinks>4?'neg':'neu'}">${m.drinks} drink${m.drinks===1?'':'s'}</span></div>
    </div>
    <div class="card"><h4>THE CLIMB TO 12%</h4>
      <div class="meter"><i style="width:${Math.round(climb)}%"></i></div>
      <div class="tick"><span>${t.start_bf}% → ${t.current_bf}%</span><span>12% · THE NORTH STAR</span></div>
    </div>
    <div class="card" style="border-color:rgba(61,220,132,.3)">
      <h4 style="color:var(--green)">NEXT WEEK — ONE FOCUS</h4>
      <p style="font-size:12.5px">${w.focus_text}</p>
    </div>
    <div class="note">One focus per week. Never ten.</div>
    ${nav('weekly')}
  </div>`;
}

function nav(active){
  return `<div class="nav">
    <div class="${active==='today'?'on':''}" onclick="go('today')">TODAY</div>
    <div class="${active==='path'?'on':''}" onclick="go('path')">PATH</div>
    <div class="${active==='body'?'on':''}" onclick="go('body')">BODY</div>
    <div class="${active==='weekly'?'on':''}" onclick="go('weekly')">SCORE</div>
  </div>`;
}
async function go(scr){
  if(scr==='weekly' && !S.weekly){ try{ S.weekly = await api('/api/weekly'); }catch(e){} }
  S.screen = scr; render();
}

async function boot(){
  if(!T){ render(); return; }
  try{
    S.today = await api('/api/today');
    S.screen = (S.today.targets && S.today.targets.protein_target_g) ? 'today' : 'survey';
  }catch(e){ T=null; localStorage.removeItem('volta_token'); S.screen='auth'; }
  render();
}

function render(){
  const v = {auth:viewAuth, survey:viewSurvey, northstar:viewNorthStar, today:viewToday,
             path:viewPath, body:viewBody, weekly:viewWeekly,
             loading:()=>'<div class="screen"><div class="spin">Charging…</div></div>'};
  document.getElementById('app').innerHTML = (v[S.screen]||viewAuth)();
}
boot();
</script>
</body>
</html>
"""

OUT.write_text(HTML)
print(f"built {OUT} ({len(HTML)} bytes)")
