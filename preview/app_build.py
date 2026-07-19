#!/usr/bin/env python3
"""VOLTA frontend builder — emits preview/app.html. Edit THIS file, never app.html.
Zero frameworks. One artifact: web + PWA. Server is the source of truth."""
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
  --bg:#f4f5f7; --panel:#ffffff; --panel2:#f0f1f4; --line:#e2e4ea;
  --txt:#12141a; --dim:#4a5162; --faint:#8b93a5;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",Helvetica,Arial,sans-serif;min-height:100vh}
#app{max-width:420px;margin:0 auto;min-height:100vh;display:flex;flex-direction:column;padding:0 18px env(safe-area-inset-bottom)}
.screen{flex:1;display:flex;flex-direction:column;padding-top:14px}
.t-xs{font-size:10px;letter-spacing:.18em;color:var(--faint)}
.t-q{font-size:23px;font-weight:800;letter-spacing:-.01em;line-height:1.25;margin:8px 0 4px}
.t-hint{font-size:13px;color:var(--dim);line-height:1.5}
.card{background:var(--panel2);border:1px solid var(--line);border-radius:16px;padding:14px;margin-top:12px}
.card h4{font-size:10px;letter-spacing:.15em;color:var(--faint);font-weight:600;margin-bottom:10px}
.opt{border:1px solid var(--line);background:var(--panel2);border-radius:14px;padding:14px;margin-top:10px;font-size:14px;font-weight:600;cursor:pointer;user-select:none}
.opt.sel{border-color:var(--green);background:rgba(61,220,132,.08)}
.opt small{display:block;font-weight:400;color:var(--faint);font-size:11px;margin-top:2px}
.btn{margin-top:16px;background:linear-gradient(90deg,var(--green),var(--cyan));color:#04110a;font-weight:800;text-align:center;padding:15px;border-radius:14px;font-size:15px;cursor:pointer;border:none;width:100%}
.btn.ghost{background:none;border:1px solid var(--line);color:var(--dim)}
.btn:disabled{opacity:.4}
.inp{width:100%;background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:13px;color:var(--txt);font-size:15px;margin-top:10px}
.inp:focus{outline:none;border-color:var(--cyan)}
.inp-row{display:flex;gap:10px}
.seg{display:flex;gap:8px;margin-top:10px}
.seg .opt{flex:1;text-align:center;padding:11px 4px;font-size:13px;margin-top:0}
.wf-row{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);font-size:12.5px}
.wf-row:last-child{border-bottom:none}
.wf-name{flex:1;color:var(--dim)}
.wf-val{font-variant-numeric:tabular-nums;font-weight:700}
.pos{color:var(--green)} .neg{color:var(--red)} .neu{color:var(--amber)}
.ring-c{display:flex;justify-content:center;padding:12px 0 4px}
.lvl{font-size:10px;letter-spacing:.2em;color:var(--green);text-align:center}
.nav{display:flex;justify-content:space-around;border-top:1px solid var(--line);padding:12px 0 18px;margin-top:auto}
.nav div{font-size:9px;color:var(--faint);letter-spacing:.08em;text-align:center;cursor:pointer}
.nav .on{color:var(--green)}
.dots{display:flex;gap:5px;justify-content:center;margin:16px 0}
.dot{width:6px;height:6px;border-radius:50%;background:var(--line)}
.dot.on{background:var(--green)}
.meter{height:8px;border-radius:4px;background:var(--line);overflow:hidden;margin-top:8px;opacity:.6}
.meter i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--green),var(--cyan))}
.tick{display:flex;justify-content:space-between;font-size:9px;color:var(--faint);margin-top:4px}
.note{font-size:10.5px;color:var(--faint);text-align:center;margin-top:12px;line-height:1.55}
.chk{display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--line);font-size:13.5px;cursor:pointer}
.chk:last-child{border-bottom:none}
.chk .box{width:22px;height:22px;border-radius:7px;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0}
.chk.done .box{background:var(--green);border-color:var(--green);color:#04110a}
.chk.done .lbl{color:var(--faint);text-decoration:line-through}
.streak{display:flex;gap:5px;justify-content:space-between;margin-top:4px}
.streak div{width:100%;height:14px;border-radius:4px;background:var(--line)}
.streak div.on{background:var(--green)}
.err{color:var(--red);font-size:12px;margin-top:8px;text-align:center}
.center{text-align:center}
.big{font-size:52px;font-weight:800;letter-spacing:-.03em;line-height:1}
.spin{color:var(--faint);text-align:center;padding:40px}
.cap-row{display:flex;justify-content:space-between;font-size:12px;color:var(--dim);padding:6px 0}
.cap-row b{color:var(--txt)}
</style>
</head>
<body>
<div id="app"></div>
<script>
const API = window.VOLTA_API || '';
let T = localStorage.getItem('volta_token') || null;
let S = {screen: T ? 'loading' : 'auth', mode: 'login', surveyStep: 0, survey: {}, today: null, weekly: null, err: ''};
if(localStorage.getItem('volta_theme')==='light') document.body.classList.add('light');
function toggleTheme(){
  document.body.classList.toggle('light');
  localStorage.setItem('volta_theme', document.body.classList.contains('light')?'light':'dark');
}

const $ = sel => document.querySelector(sel);
const el = html => html;
async function api(path, method='GET', body=null){
  const r = await fetch(API + path, {
    method,
    headers: {'content-type':'application/json', ...(T?{authorization:'Bearer '+T}:{})},
    body: body ? JSON.stringify(body) : null
  });
  const d = await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(d.detail || 'Something went wrong — try again');
  return d;
}
function save(){ localStorage.setItem('volta_token', T); }
function logout(){ localStorage.removeItem('volta_token'); T=null; S={screen:'auth',mode:'login',surveyStep:0,survey:{},err:''}; render(); }

function ringSVG(score, size=170){
  const c = 528, off = c - (c * score/100);
  return `<svg width="${size}" height="${size}" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="84" fill="none" stroke="var(--line)" stroke-width="14"/>
    <circle cx="100" cy="100" r="84" fill="none" stroke="url(#g1)" stroke-width="14" stroke-linecap="round"
      stroke-dasharray="${c}" stroke-dashoffset="${off}" transform="rotate(-90 100 100)"/>
    <defs><linearGradient id="g1"><stop offset="0%" stop-color="#3ddc84"/><stop offset="100%" stop-color="#41d6e8"/></linearGradient></defs>
    <text x="100" y="98" text-anchor="middle" fill="var(--txt)" font-size="50" font-weight="800">${score}</text>
    <text x="100" y="124" text-anchor="middle" fill="var(--faint)" font-size="11" letter-spacing="2">${score>=70?'CHARGED':score>=40?'GOOD':'LOW'}</text>
  </svg>`;
}

/* ---------- AUTH ---------- */
function viewAuth(){
  return `<div class="screen">
    <div style="text-align:center;margin-top:70px">
      <div class="t-xs">KNOW YOUR CHARGE</div>
      <div class="t-q" style="font-size:42px;margin-top:8px">VOLTA</div>
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

/* ---------- SURVEY ---------- */
const SURVEY_STEPS = [1,2,3,4];
function viewSurvey(){
  const st = S.surveyStep, v = S.survey;
  let body = '';
  if(st===0){
    body = `<div class="t-xs">FIRST — THE ONLY QUESTION THAT MATTERS</div>
    <div class="t-q">What do you actually want?</div>
    <div class="t-hint">Not what sounds good. What you want.</div>
    ${[['longevity','🧬','Live as long as possible — in a body that works'],['lean','🔥','Get lean & stay lean — finally'],['energy','⚡','Energy every single day'],['bloodwork','🩸','Fix my bloodwork']]
      .map(([k,e,l])=>`<div class="opt ${v.outcome===k?'sel':''}" onclick="setS('outcome','${k}')"><span>${e}</span> ${l}</div>`).join('')}`;
  }else if(st===1){
    body = `<div class="t-xs">BE HONEST — NOBODY SEES THIS BUT YOU</div>
    <div class="t-q">Where is your body today?</div>
    <div class="inp-row">
      <input class="inp" id="age" type="number" placeholder="Age" value="${v.age||''}" oninput="captureBodyInputs()">
      <input class="inp" id="height" type="number" placeholder="Height (in)" value="${v.height_in||''}" oninput="captureBodyInputs()">
      <input class="inp" id="weight" type="number" placeholder="Weight (lb)" value="${v.weight_lb||''}" oninput="captureBodyInputs()">
    </div>
    <div class="t-hint" style="margin-top:14px">Estimated body fat:</div>
    <div class="seg">${[['','Not sure'],[27,'~25–30%'],[22,'~20–25%'],[17,'~15–20%']].map(([k,l])=>`<div class="opt ${String(v.bf_estimate??'')===String(k)?'sel':''}" onclick="setS('bf_estimate','${k}')">${l}</div>`).join('')}</div>
    <div class="t-hint" style="margin-top:16px">Working with a doctor on a medical weight-management plan?</div>
    <div class="seg">
      <div class="opt ${v.doctor_plan===true?'sel':''}" onclick="setS('doctor_plan',true)">Yes</div>
      <div class="opt ${v.doctor_plan===false?'sel':''}" onclick="setS('doctor_plan',false)">No</div>
    </div>
    <div class="note">VOLTA never recommends medication. If your doctor does,<br>we track how your body responds.</div>`;
  }else if(st===2){
    body = `<div class="t-xs">THE BASELINE — NO JUDGMENT, ONLY DATA</div>
    <div class="t-q">Your average week, honestly.</div>
    <div class="t-hint" style="margin-top:12px">Training days per week</div>
    <div class="seg">${[1,3,5].map(n=>`<div class="opt ${v.training_days===n?'sel':''}" onclick="setS('training_days',${n})">${n===1?'0–1':n===3?'2–3':'4+'}</div>`).join('')}</div>
    <div class="t-hint" style="margin-top:14px">Drinks per week</div>
    <div class="seg">${[0,2,6].map(n=>`<div class="opt ${v.drinks_wk===n?'sel':''}" onclick="setS('drinks_wk',${n})">${n===0?'0':n===2?'1–4':'5+'}</div>`).join('')}</div>
    <div class="t-hint" style="margin-top:14px">Your diet, most days</div>
    ${[['whole','Mostly whole foods'],['half','Half whole, half whatever'],['packaged','Mostly restaurants / packaged']].map(([k,l])=>`<div class="opt ${v.diet_honesty===k?'sel':''}" onclick="setS('diet_honesty','${k}')">${l}</div>`).join('')}
    <div class="t-hint" style="margin-top:14px">Sleep, most nights</div>
    <div class="seg">${[['<6','<6h'],['6-7','6–7h'],['7+','7h+']].map(([k,l])=>`<div class="opt ${v.sleep_hours===k?'sel':''}" onclick="setS('sleep_hours','${k}')">${l}</div>`).join('')}</div>`;
  }else{
    body = `<div class="t-xs">LAST ONE — AND IT'S THE WHOLE GAME</div>
    <div class="t-q">Will you track, honestly, every day?</div>
    <div class="t-hint">The system only works on true data. 60 seconds a day. That's the deal.</div>
    <div class="card"><h4>WHAT HONEST TRACKING BUYS YOU</h4>
      <div class="wf-row"><span class="wf-name">A number you can trust every morning</span><span class="wf-val pos">Daily</span></div>
      <div class="wf-row"><span class="wf-name">Proof of what works on YOUR body</span><span class="wf-val pos">~90 days</span></div>
      <div class="wf-row"><span class="wf-name">A score that proves you're getting healthier</span><span class="wf-val pos">Monthly</span></div>
      <div class="wf-row"><span class="wf-name">Blood results before the needle</span><span class="wf-val pos">6 months</span></div>
    </div>
    <div class="opt ${v.committed?'sel':''}" onclick="setS('committed',true)">✊ I'm in. Every day.</div>`;
  }
  const ready = st===0 ? !!v.outcome
    : st===1 ? (v.age&&v.height_in&&v.weight_lb&&v.doctor_plan!==undefined)
    : st===2 ? (v.training_days!==undefined&&v.drinks_wk!==undefined&&v.diet_honesty&&v.sleep_hours)
    : !!v.committed;
  return `<div class="screen">
    ${body}
    <div class="dots">${SURVEY_STEPS.map((_,i)=>`<div class="dot ${i<=st?'on':''}"></div>`).join('')}</div>
    <div class="err">${S.err}</div>
    <button class="btn" ${ready?'':'disabled'} onclick="surveyNext()">${st===3?'Build My Plan →':'Continue →'}</button>
  </div>`;
}
function setS(k,val){
  if(S.surveyStep===1 && !['age','height_in','weight_lb'].includes(k)) captureBodyInputs();
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
  if(S.surveyStep===1){
    captureBodyInputs();
    if(!S.survey.age||!S.survey.height_in||!S.survey.weight_lb){S.err='Fill in age, height and weight';render();return;}
  }
  S.err='';
  if(S.surveyStep<3){ S.surveyStep++; render(); return; }
  try{
    const d = await api('/api/survey','POST',S.survey);
    S.targets = d.targets; S.screen='northstar'; render();
  }catch(e){ S.err=e.message; render(); }
}

/* ---------- NORTH STAR ---------- */
function viewNorthStar(){
  const t = S.targets;
  const pct = Math.min(100, Math.max(0, (t.current_bf - t.north_star_bf) / (45 - t.north_star_bf) * 100));
  return `<div class="screen">
    <div class="t-xs center" style="margin-top:30px">YOUR NORTH STAR</div>
    <div class="center" style="margin-top:10px">
      <div class="big">12<span style="font-size:24px;color:var(--faint)">%</span></div>
      <div class="lvl">BODY FAT — THE TARGET</div>
    </div>
    <div class="card">
      <div class="cap-row"><span>Today (estimated)</span><b>${t.current_bf}%</b></div>
      <div class="meter"><i style="width:${100-pct}%"></i></div>
      <div class="tick"><span>${t.current_bf}%</span><span>10–12%</span></div>
      <div class="cap-row" style="margin-top:8px"><span>Goal weight at 12%</span><b class="pos">${t.goal_weight_lb} lb</b></div>
      <div class="cap-row"><span>Daily protein target</span><b>${t.protein_target_g}g</b></div>
    </div>
    <div class="card"><h4>WHY THIS NUMBER</h4>
      <div class="wf-row"><span class="wf-name">Visceral fat — the dangerous kind — clears out</span></div>
      <div class="wf-row"><span class="wf-name">Insulin sensitivity resets toward optimal</span></div>
      <div class="wf-row"><span class="wf-name">Testosterone &amp; inflammation normalize</span></div>
      <div class="wf-row"><span class="wf-name">Every longevity marker moves at once</span></div>
    </div>
    <div class="note">Not a crash diet. A whole-foods rebuild at a pace<br>your body can hold for decades.</div>
    <button class="btn" onclick="goToday()">Accept the Target →</button>
  </div>`;
}
async function goToday(){ S.today = await api('/api/today'); S.screen='today'; render(); }

/* ---------- TODAY (Battery home) ---------- */
function viewToday(){
  const d = S.today, b = d.battery, t = d.targets;
  const batt = b ? b.score : '—';
  return `<div class="screen">
    <div class="t-xs">TODAY'S BATTERY</div>
    <div class="ring-c">${b?ringSVG(b.score):'<div class="spin">Log below to generate your battery</div>'}</div>
    ${b?`<div class="lvl">${b.recommendation.toUpperCase()}</div>`:''}
    ${b?`<div style="margin-top:8px">${b.components.map(c=>`<div class="wf-row"><span class="wf-name">${c.label}</span><span class="wf-val ${c.points>0?'pos':'neg'}">${c.points>0?'+':''}${c.points}</span></div>`).join('')}</div>`:''}
    <div class="card" style="border-color:rgba(61,220,132,.3)">
      <h4 style="color:var(--green)">TODAY'S ONE ACTION</h4>
      <p style="font-size:13px;color:var(--dim);line-height:1.55">${d.one_action.action}</p>
      ${d.tomorrow_projection?`<p style="font-size:11px;color:var(--faint);margin-top:6px">Tomorrow's projected battery: <b class="pos">${d.tomorrow_projection}</b></p>`:''}
    </div>
    <div class="card"><h4>QUICK LOG — TODAY</h4>
      ${quickLog()}
    </div>
    ${nav('today')}
  </div>`;
}
function quickLog(){
  const l = S.today.log || {};
  return `
    <div class="chk ${l.weight_lb?'done':''}" onclick="logPrompt('weight_lb','Morning weigh-in (lb)')"><div class="box">${l.weight_lb?'✓':''}</div><div class="lbl">🌅 Weigh-in ${l.weight_lb?'· '+l.weight_lb+' lb':''}</div></div>
    <div class="chk ${l.sleep_quality?'done':''}" onclick="logPrompt('sleep_quality','Sleep quality last night (1–10)')"><div class="box">${l.sleep_quality?'✓':''}</div><div class="lbl">😴 Sleep ${l.sleep_quality?'· '+l.sleep_quality+'/10':''}</div></div>
    <div class="chk ${l.energy?'done':''}" onclick="logPrompt('energy','Energy right now (1–10)')"><div class="box">${l.energy?'✓':''}</div><div class="lbl">⚡ Energy ${l.energy?'· '+l.energy+'/10':''}</div></div>
    <div class="chk ${l.protein_g?'done':''}" onclick="logPrompt('protein_g','Protein so far today (g)')"><div class="box">${l.protein_g?'✓':''}</div><div class="lbl">🥩 Protein ${l.protein_g?'· '+l.protein_g+'g / '+S.today.targets.protein_target_g+'g':''}</div></div>
    <div class="chk ${l.trained?'done':''}" onclick="logField('trained',${l.trained?false:true})"><div class="box">${l.trained?'✓':''}</div><div class="lbl">🏋️ Trained today</div></div>
    <div class="chk ${l.drinks?'done':''}" onclick="logPrompt('drinks','Drinks today (0 if none)')"><div class="box">${l.drinks?'✓':''}</div><div class="lbl">🍷 Drinks ${l.drinks?'· '+l.drinks:''}</div></div>
    <div class="chk ${l.whole_foods_score?'done':''}" onclick="logPrompt('whole_foods_score','Whole foods score today (0–100)')"><div class="box">${l.whole_foods_score?'✓':''}</div><div class="lbl">🥦 Whole foods ${l.whole_foods_score?'· '+l.whole_foods_score+'%':''}</div></div>
    <div class="card" style="margin-top:10px"><h4>STREAK</h4>
      <div class="streak">${[...Array(7)].map((_,i)=>`<div class="${i<Math.min(S.today.streak,7)?'on':''}"></div>`).join('')}</div>
      <div class="tick"><span>${S.today.streak}-DAY STREAK</span><span>KEEP IT ALIVE</span></div>
    </div>`;
}
async function logPrompt(field, label){
  const v = prompt(label);
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
  return `<div class="screen">
    <div class="t-xs">${t.start_bf}% → 12% · PHASE ${ph.number} OF 4</div>
    <div class="t-q" style="font-size:20px">Phase ${ph.number}: ${ph.name}</div>
    <div class="t-hint">No restriction yet. We install the floor first.</div>
    <div class="card"><h4>THIS PHASE, ONLY 4 THINGS MATTER</h4>
      <div class="wf-row"><span class="wf-name">Hit your protein number daily</span><span class="wf-val">${t.protein_target_g}g</span></div>
      <div class="wf-row"><span class="wf-name">Whole foods only — nothing in a wrapper</span><span class="wf-val">✓</span></div>
      <div class="wf-row"><span class="wf-name">Train 3×/week — full body</span><span class="wf-val">✓</span></div>
      <div class="wf-row"><span class="wf-name">In bed by ${t.bedtime}</span><span class="wf-val">✓</span></div>
    </div>
    <div class="card"><h4>PHASE PROGRESS</h4>
      <div class="meter"><i style="width:${Math.min(100, S.today.streak/28*100)}%"></i></div>
      <div class="tick"><span>DAY ${S.today.streak} OF 28</span><span class="pos">${S.today.streak>=1?'ON TRACK':'START TODAY'}</span></div>
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

/* ---------- WEEKLY ---------- */
function viewWeekly(){
  const w = S.weekly;
  if(!w){ return `<div class="screen"><div class="spin">Loading…</div>${nav('weekly')}</div>`; }
  const m = w.metrics;
  return `<div class="screen">
    <div class="t-xs">YOUR WEEK, GRADED</div>
    <div class="t-q" style="font-size:22px">This week: <span class="pos">${w.grade}</span></div>
    <div class="card"><h4>THE SCOREBOARD</h4>
      <div class="wf-row"><span class="wf-name">Tracking honesty</span><span class="wf-val">${m.tracking_days}</span></div>
      <div class="wf-row"><span class="wf-name">Whole foods avg</span><span class="wf-val ${m.whole_foods_avg>=85?'pos':'neu'}">${m.whole_foods_avg}%</span></div>
      <div class="wf-row"><span class="wf-name">Protein target</span><span class="wf-val">${m.protein_hit_rate}</span></div>
      <div class="wf-row"><span class="wf-name">Training sessions</span><span class="wf-val">${m.training_sessions}/3</span></div>
      <div class="wf-row"><span class="wf-name">Avg battery</span><span class="wf-val">${m.avg_battery}</span></div>
      <div class="wf-row"><span class="wf-name">Drinks</span><span class="wf-val ${m.drinks>4?'neg':'neu'}">${m.drinks}</span></div>
    </div>
    <div class="card" style="border-color:rgba(61,220,132,.3)">
      <h4 style="color:var(--green)">NEXT WEEK — ONE FOCUS</h4>
      <p style="font-size:13px;color:var(--dim);line-height:1.55">${w.focus_text}</p>
    </div>
    <div class="note">One focus per week. Never ten.</div>
    ${nav('weekly')}
  </div>`;
}

/* ---------- LOCKED ---------- */
function viewLocked(name, desc){
  return `<div class="screen">
    <div class="t-xs">${name}</div>
    <div style="text-align:center;margin-top:80px">
      <div style="font-size:44px">🔒</div>
      <div class="t-q" style="font-size:20px;margin-top:14px">${desc}</div>
      <div class="t-hint" style="margin-top:10px">Earned by your honest data.<br>Keep the streak alive.</div>
    </div>
    ${nav('locked')}
  </div>`;
}

function nav(active){
  return `<div class="nav">
    <div class="${active==='today'?'on':''}" onclick="go('today')">TODAY</div>
    <div class="${active==='path'?'on':''}" onclick="go('path')">PATH</div>
    <div onclick="go('body')">BODY 🔒</div>
    <div class="${active==='weekly'?'on':''}" onclick="go('weekly')">WEEK</div>
    <div onclick="toggleTheme()">☀/☾</div>
    <div onclick="logout()" style="color:var(--faint)">EXIT</div>
  </div>`;
}
async function go(scr){
  if(scr==='body'){ S.screen='locked'; render(); return; }
  if(scr==='weekly' && !S.weekly){ try{ S.weekly = await api('/api/weekly'); }catch(e){} }
  S.screen = scr; render();
}

async function boot(){
  if(!T){ render(); return; }
  try{
    S.today = await api('/api/today');
    S.screen = (S.today.targets && S.today.targets.protein_target_g) ? 'today' : 'survey';
  }catch(e){ S.screen='auth'; }
  render();
}

function render(){
  const v = {auth:viewAuth, survey:viewSurvey, northstar:viewNorthStar, today:viewToday,
             path:viewPath, weekly:viewWeekly, locked:()=>viewLocked("YOUR BODY'S RULES","Unlocks after 90 days of honest data"),
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
