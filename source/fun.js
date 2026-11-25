// ===== Oss! Squad fun pack: tap-out finishes, ref calls + crowd, rolling combos, gym events,
// ===== your gym + pet, grudge rematches, instructionals, Daily Superfight share card.
let ATK=null;
const _refA={};
function ossRef(k,vol){ try{ const OSS_REF=(window.OSS_ART&&OSS_ART.ref)||{}; if(muted||!OSS_REF[k]) return; const v=(SET.sfx==null?.8:SET.sfx)*(vol||1); if(v<=0) return; let a=_refA[k]; if(!a){ a=_refA[k]=new Audio(OSS_REF[k]); a.preload='auto'; } a.volume=Math.min(1,v); a.currentTime=0; const p=a.play(); if(p&&p.catch)p.catch(()=>{}); }catch(_){} }
// ---- crowd: looping filtered noise whose volume follows the action ----
let _crowd=null;
function ossCrowd(){ if(_crowd||!AC||!SFXG) return _crowd; try{ const s=AC.createBufferSource(); s.buffer=noiseBuf(); s.loop=true; const bp=AC.createBiquadFilter(); bp.type='bandpass'; bp.frequency.value=900; bp.Q.value=.6; const lp=AC.createBiquadFilter(); lp.type='lowpass'; lp.frequency.value=2400; const g=AC.createGain(); g.gain.value=0; s.connect(bp); bp.connect(lp); lp.connect(g); g.connect(SFXG); s.start(); _crowd={g,lvl:0,pulse:0}; }catch(_){ _crowd=null; } return _crowd; }
function ossCheer(n){ const c=ossCrowd(); if(c) c.pulse=Math.max(c.pulse,n||1); }
function ossCrowdTick(dt){ const c=ossCrowd(); if(!c) return; const fight=G&&G.state==='play'&&!G.paused&&G.phase==='fight';
  const streak=(G&&G.t-(G.cmT||-9)<1.6)?(G.cmN||0):0;
  const target=fight?Math.min(.085,.012+streak*.0016+(G.enemies.some(e=>e.type==='boss'&&!e.dead)?.012:0)):0;
  c.pulse=Math.max(0,c.pulse-dt*1.2); c.lvl+=(target+c.pulse*.07-c.lvl)*Math.min(1,dt*3);
  try{ c.g.gain.setTargetAtTime(muted?0:c.lvl,AC.currentTime,.08); }catch(_){} }
const PTX=(en,pt)=>PTL()?pt:en;

// ---- 1. tap-out finishes ----
const OSS_FIN=[['Back Take → Rear Naked Choke','Pegada nas Costas → Mata-Leão'],['Inside Heel Hook','Heel Hook por Dentro'],['Kimura from Side Control','Kimura dos 100 Quilos'],['Double Leg → Pin','Baiana → Imobilização'],['Butterfly Sweep → Guillotine','Raspagem de Borboleta → Guilhotina'],['Cross Collar Choke','Estrangulamento de Gola Cruzada'],['Straight Ankle Lock','Chave de Pé Reta'],['Arm Triangle','Katagatame'],['Rubber Guard Omoplata','Omoplata da Guarda de Borracha'],['Bow and Arrow Choke','Estrangulamento Arco e Flecha']];
const OSS_FIN_SEC={founder:['Americana from Mount','Americana da Montada'],redbelt:['Ezekiel Choke','Ezequiel']};
function ossFinCheck(e){ if(!G||G.fin||G.tut||e.dead||e.type!=='boss'||e.tag||e.secret&&!OSS_FIN_SEC[e.secret]) return;
  const thr=e.finTry?.06:.15; if(e.finDone||e.hp>e.max*thr||e.hp<=0) return; e.finDone=e.finTry?1:0; e.finTry=1;
  const mv=e.secret?OSS_FIN_SEC[e.secret]:OSS_FIN[e.bi!=null?e.bi:bossIdx(G.wave)]||OSS_FIN[0];
  G.fin={e,t:0,dur:SET.kids?3.6:2.8,n:0,need:SET.kids?7:11,mv:PTX(mv[0],mv[1])};
  ossRef('finish'); ossCheer(1.5); buzz(30); G.flash=Math.max(G.flash||0,.2);
  let el=document.getElementById('finUI'); if(!el){ el=document.createElement('div'); el.id='finUI'; document.body.appendChild(el); }
  const fsrc=e.secret?null:ossFx('fin_'+(e.bi!=null?e.bi:bossIdx(G.wave))); G.fin.img=fsrc;
  el.innerHTML=`${fsrc?`<img class="fimg" src="${fsrc}" alt="">`:''}<div class="fmv">🔒 ${G.fin.mv}</div><div class="ftap">${PTX('TAP! TAP! TAP!','TOQUE! TOQUE!')}</div><div class="fbar"><i id="finFill"></i></div><div class="fhint">${PTX('Tap fast to finish!','Toque rápido para finalizar!')}</div>`; el.className='on'; }
function ossFinTap(ev){ if(!G||!G.fin) return; if(ev&&ev.type==='keydown'&&!/^( |Enter|Space|ArrowUp|ArrowDown|ArrowLeft|ArrowRight|w|a|s|d|W|A|S|D)$/.test(ev.key)) return; if(ev&&ev.cancelable) ev.preventDefault(); if(ev) ev.stopPropagation(); G.fin.n++; buzz(8); sfx('hit'); const f=document.getElementById('finFill'); if(f) f.style.width=Math.min(100,G.fin.n/G.fin.need*100)+'%'; if(G.fin.n>=G.fin.need) ossFinEnd(true); }
['pointerdown','keydown'].forEach(t=>window.addEventListener(t,ev=>{ if(G&&G.fin) ossFinTap(ev); },true));
function ossFinTick(dt){ const F=G.fin; if(!F) return; F.t+=dt; if(F.e.dead){ ossFinEnd(true,true); return; } if(F.t>=F.dur) ossFinEnd(false); }
function ossFinEnd(ok,already){ const F=G.fin; if(!F) return; G.fin=null; const el=document.getElementById('finUI'); if(el){ el.className=''; el.innerHTML=''; } const e=F.e;
  if(ok){ ossRef('tap'); ossCheer(3); if(F.img){ let w=document.getElementById('finWin'); if(!w){ w=document.createElement('div'); w.id='finWin'; document.body.appendChild(w); } w.innerHTML=`<img src="${F.img}" alt=""><b>${PTX('TAP OUT!','BATEU!')}</b><small>${F.mv}</small>`; w.className=''; void w.offsetWidth; w.className='on'; setTimeout(()=>{ w.className=''; },2200); } G.banner={text:PTX('TAP OUT!','BATEU!'),sub:F.mv,t:2.4,col:'#ffd86b'}; G.score+=1500; if(!already&&!e.dead){ e.finisher=1; hurtEnemy(e,e.hp+1,true); } G.shake=Math.max(G.shake,.6); G.hs=Math.max(G.hs||0,.12); META.fins=(META.fins||0)+1; saveMeta(); }
  else { ossRef('escaped'); G.banner={text:PTX('ESCAPED!','ESCAPOU!'),sub:PTX('Wear them down and try again','Canse e tente de novo'),t:2,col:'#ff8a6a'}; e.hp=Math.min(e.max,e.hp+e.max*.08); } }

// ---- special-move cut-ins ----
function ossFx(k){ return window.OSS_ART&&OSS_ART.fx&&OSS_ART.fx[k]; }
function ossCutIn(h,SK){ const src=ossFx('sp_'+h.kind); if(!src||!G) return; const now=performance.now(); if(ossCutIn.t&&now-ossCutIn.t<6500) return; ossCutIn.t=now;
  let el=document.getElementById('cutIn'); if(!el){ el=document.createElement('div'); el.id='cutIn'; document.body.appendChild(el); }
  const col=KINDS[h.kind].col; el.style.setProperty('--c',col); el.innerHTML=`<img src="${src}" alt=""><div class="cn"><small>${tr(KINDS[h.kind].name)}</small><b>${SK.ico} ${tr(SK.name)}</b></div>`;
  el.className=''; void el.offsetWidth; el.className='on'; clearTimeout(ossCutIn.tm); ossCutIn.tm=setTimeout(()=>{ el.className=''; },1500); }

// ---- 4. rolling combos ----
const OSS_TD=['knight','archer','mage'];
function ossOnKill(e){ if(!G||G.tut) return; const k=ATK; const now=G.t; G.rc=(G.rc||[]).filter(r=>now-r.t<2.2); if(k) G.rc.push({k,t:now});
  const prev=G.rc.length>1?G.rc[G.rc.length-2]:null, lead=G.party[0]?hpos(G.party[0]):{x:e.x,y:e.y};
  if(k==='rogue'&&prev&&OSS_TD.includes(prev.k)&&now-prev.t<1.4&&!(G.rcN>now)){ G.rcN=now+3; G.score+=150; text(e.x,e.y-1,PTX('Takedown → Tap! +150','Queda → Finalização! +150'),'#ffd86b',true); ossRef('adv',.8); META.rolls=(META.rolls||0)+1; }
  const kinds=new Set(G.rc.map(r=>r.k)).size;
  if(kinds>=3&&!(G.rcT>now)){ G.rcT=now+4; const n=kinds, pts=120*n; G.score+=pts; G.gold+=n; G.charge=Math.min(100,(G.charge||0)+4); text(clamp(lead.x,G.camX+VW*.25,G.camX+VW*.75),lead.y-1.6,(n>=5?PTX('🌀 OPEN MAT FLOW','🌀 FLUXO DE TREINO LIVRE'):PTX('🤼 TEAM ROLL','🤼 ROLA EM EQUIPE'))+' x'+n+' +'+pts,'#7fe6d8',true); ossRef('points',.8); ossCheer(1.2); META.rolls=(META.rolls||0)+1; }
  if(e.nem){ ossGrudgeWin(e); }
  if(e.type==='boss'&&!e.finisher&&!e.tag){ setTimeout(()=>ossRef('winner'),300); ossCheer(2.5); }
  if(!e.nem&&e.type!=='boss'&&Math.random()<(e.elite?.12:.004)*(G.event&&G.event.id==='moon'?1.5:1)&&!G.daily) ossDropInstr(e.x,e.y); }

// ---- 5. gym events mid-round ----
const OSS_EV=[
 {id:'open',ico:'🪙',n:['OPEN MAT!','TREINO LIVRE!'],d:['Double coins for 20s','Moedas em dobro por 20s'],dur:20},
 {id:'coach',ico:'👀',n:['COACH IS WATCHING','O PROFESSOR ESTÁ OLHANDO'],d:['No wall bumps for 20s: +300 and a reward','Sem bater na parede por 20s: +300 e um prêmio'],dur:20},
 {id:'comp',ico:'🏟️',n:['COMP CLASS!','TREINO DE CAMPEONATO!'],d:['Everyone hits 25% harder for 15s','Todo mundo bate 25% mais forte por 15s'],dur:15},
 {id:'drill',ico:'⏱️',n:['SHARK TANK!','TANQUE DE TUBARÃO!'],d:['Fresh rivals keep coming: +2 coins each for 15s','Rivais descansados não param: +2 moedas cada por 15s'],dur:15}];
function ossEvStart(){ const ev=OSS_EV[Math.floor(Math.random()*OSS_EV.length)]; G.gev={ev,t:0,bumps:G.bumpsN||0}; G.banner={text:ev.ico+' '+PTX(ev.n[0],ev.n[1]),sub:PTX(ev.d[0],ev.d[1]),t:2.6,col:'#7fe6d8'}; ossRef('lutem',.7); ossCheer(1); }
function ossEvEnd(){ const g=G.gev; G.gev=null; if(!g) return; const lead=G.party[0]?hpos(G.party[0]):{x:0,y:0};
  if(g.ev.id==='coach'){ if((G.bumpsN||0)===g.bumps){ G.score+=300; G.pickups.push({type:'potion',pt:potType(),x:lead.x,y:lead.y-1.2,t:0}); text(lead.x,lead.y-1.4,PTX('👀 Coach approves! +300','👀 O professor aprovou! +300'),'#7dffa0',true); sfx('good'); } else text(lead.x,lead.y-1.4,PTX('👀 Coach saw that…','👀 O professor viu isso…'),'#ff9a8a',true); } }
function ossCoinM(){ return G&&G.gev&&G.gev.ev.id==='open'?2:1; }
function ossDmgM(h){ let m=1; if(G&&G.gev&&G.gev.ev.id==='comp') m*=1.25; if(G&&G.instr&&G.instr[h.kind]) m*=1.15; return m; }
function ossTakeM(){ return G&&G.gev&&G.gev.ev.id==='comp'?1.25:1; }

// ---- 6. your gym + pet ----
const OSS_GYM=[
 {id:'plant',ico:'🪴',n:['Plant','Planta'],c:100},{id:'flag',ico:'🇧🇷',n:['Brazil Flag','Bandeira do Brasil'],c:150},{id:'bag',ico:'🥊',n:['Heavy Bag','Saco de Pancada'],c:200},
 {id:'shelf',ico:'🏆',n:['Trophy Shelf','Estante de Troféus'],c:250},{id:'tv',ico:'📺',n:['Instructional TV','TV de Instrucionais'],c:300},{id:'ice',ico:'🧊',n:['Ice Bath','Banheira de Gelo'],c:350},
 {id:'cat',ico:'🐈',n:['Gym Cat','Gato da Academia'],c:400,pet:1},{id:'dog',ico:'🐕',n:['Gym Dog','Cachorro da Academia'],c:400,pet:1},{id:'parrot',ico:'🦜',n:['Parrot','Papagaio'],c:600,pet:1},{id:'gator',ico:'🐊',n:['Jacaré','Jacaré'],c:900,pet:1},{id:'capy',ico:'🦫',n:['Capybara','Capivara'],c:1200,pet:1}];
function ossGymM(){ META.gym=META.gym||{own:[],pet:null}; return META.gym; }
function ossGymStrip(){ const M=ossGymM(); if(!M.own.length) return ''; const it=OSS_GYM.filter(g=>M.own.includes(g.id)&&!g.pet).map(g=>g.ico).join(' '); const pet=M.pet?(OSS_GYM.find(g=>g.id===M.pet)||{}).ico:''; return `<div class="gymstrip">${it}${pet?' · '+pet:''}</div>`; }
function ossGymShop(back){ const M=ossGymM();
  const rows=OSS_GYM.map(g=>{ const own=M.own.includes(g.id), on=g.pet&&M.pet===g.id; return `<div class="it"><div class="ic" style="font-size:30px;width:40px;text-align:center">${g.ico}</div><div class="tx"><b>${PTX(g.n[0],g.n[1])}</b><br><small>${g.pet?PTX('Follows your crew on the mat','Segue sua equipe no tatame'):PTX('Shows in your gym on the menu','Aparece na sua academia no menu')}</small></div>${own?(g.pet?`<button class="btn ${on?'':'sec'}" data-pet="${g.id}">${on?PTX('With you','Junto'):PTX('Bring','Levar')}</button>`:`<button class="btn sec" disabled>✓</button>`):`<button class="btn buy" data-gym="${g.id}" ${META.bank<g.c?'disabled':''}>${g.c} 🪙</button>`}</div>`; }).join('');
  showOverlay(`<div class="card" style="max-width:420px;max-height:92vh;overflow:auto"><h2>🏠 ${PTX('Your Gym','Sua Academia')}</h2><div class="bank">${META.bank} 🪙</div>${ossGymStrip()||`<p><small>${PTX('Decorate your gym and adopt a gym pet.','Decore sua academia e adote um mascote.')}</small></p>`}<div class="shop">${rows}</div><button class="btn sec" id="gback">${PTX('Back','Voltar')}</button></div>`);
  const o=$('overlay');
  o.querySelectorAll('[data-gym]').forEach(b=>b.onclick=()=>{ const g=OSS_GYM.find(x=>x.id===b.dataset.gym); if(!g||META.bank<g.c||M.own.includes(g.id)) return; META.bank-=g.c; M.own.push(g.id); if(g.pet) M.pet=g.id; saveMeta(); sfx('good'); ossGymShop(back); });
  o.querySelectorAll('[data-pet]').forEach(b=>b.onclick=()=>{ M.pet=M.pet===b.dataset.pet?null:b.dataset.pet; saveMeta(); sfx('pick'); ossGymShop(back); });
  $('gback').onclick=()=>back(); }
function ossPetTick(dt){ const M=META.gym; if(!M||!M.pet||!G.party.length){ G.pet=null; return; } const tail=hpos(G.party[G.party.length-1]); if(!G.pet) G.pet={x:tail.x,y:tail.y,f:1,hop:0}; const P=G.pet, dx=tail.x-P.x, dy=tail.y+.15-P.y, d=Math.hypot(dx,dy);
  if(d>.75){ const sp=Math.min(1,dt*4.5); P.x+=dx*sp*(1-.75/d); P.y+=dy*sp*(1-.75/d); P.hop+=dt*14; if(Math.abs(dx)>.05) P.f=Math.sign(dx); } if(d>6){ P.x=tail.x; P.y=tail.y; } }
function ossDrawPet(){ const P=G&&G.pet, M=META.gym; if(!P||!M||!M.pet) return; const g=OSS_GYM.find(x=>x.id===M.pet); if(!g) return; const b=Math.abs(Math.sin(P.hop))*.12;
  ctx.save(); ctx.translate(P.x,P.y-b); ctx.fillStyle='rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(0,.28+b,.22,.07,0,0,TAU); ctx.fill(); ctx.scale(P.f<0?1:-1,1); ctx.scale(1/48,1/48); ctx.font='30px system-ui,"Apple Color Emoji","Segoe UI Emoji",sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(g.ico,0,0); ctx.restore(); }

// ---- 7. grudge rematches ----
function ossGrudgeSave(){ try{ if(!G||G.tut||G.daily) return; const s=G.lastSrc; if(!s||s.type==='boss'||s.nem) return; const key=s.mut||s.type; const nm=s.mut&&MUT[s.mut]?MUT[s.mut].n:(ENINFO[s.type]||[])[1]; if(!nm) return; META.grudge={k:key,n:nm,w:G.wave}; saveMeta(); }catch(_){} }
function ossGrudgeSpawn(){ const g=META.grudge; if(!g||!G||G.state!=='play'||G.daily||G.tut||G.nemDone) return; G.nemDone=1;
  let e; try{ e=spawnEnemy(g.k,true); }catch(_){ return; } if(!e) return; e.nem=1; e.hp=e.max=e.max*1.6; G.waveTotal++;
  const nm=PTL()&&typeof tr==='function'?tr(g.n):g.n; G.banner={text:'👿 '+PTX('YOUR NEMESIS','SEU RIVAL'),sub:nm+PTX(' tapped you last time. Get revenge!',' te finalizou da última vez. Vingança!'),t:3,col:'#ff5a5a'}; ossRef('taunt',.9); ossCheer(1); }
function ossGrudgeWin(e){ META.grudge=null; META.nemWins=(META.nemWins||0)+1; saveMeta(); G.gold+=40; G.score+=1000; for(let i=0;i<10;i++) G.pickups.push({type:'coin',x:e.x+rand(-.8,.8),y:e.y+rand(-.8,.8),t:rand(0,2)}); G.banner={text:PTX('😤 GRUDGE SETTLED!','😤 VINGANÇA FEITA!'),sub:'+40 🪙 +1000',t:2.6,col:'#ffd86b'}; ossRef('winner'); ossCheer(2.5); }
function ossNemTick(dt){ G.nemT=(G.nemT||0)-dt; if(G.nemT>0) return; G.nemT=1.4; for(const e of G.enemies) if(e.nem&&!e.dead) text(e.x,e.y-e.def.r-.6,'👿 '+PTX('NEMESIS','RIVAL'),'#ff5a5a'); }

// ---- 8. instructionals ----
const OSS_INS={knight:['Pressure Passing Vol. 1','Passagem de Pressão Vol. 1'],archer:['Ippon Science','Ciência do Ippon'],rogue:['Leg Lock Bible','Bíblia das Chaves de Pé'],mage:['Sambo Secrets','Segredos do Sambo'],cleric:['Corner Coaching 101','Conselhos de Corner 101'],bard:['Cardio Kings','Reis do Cardio'],necro:['Running an Academy','Como Tocar uma Academia']};
function ossDropInstr(x,y){ const ks=G.party.map(h=>h.kind).filter(k=>OSS_INS[k]&&!(G.instr&&G.instr[k])); if(!ks.length) return; const k=ks[Math.floor(Math.random()*ks.length)]; G.pickups.push({type:'instr',kind:k,x,y,t:0}); }
function ossInstrPick(k){ G.instr=G.instr||{}; G.instr[k.kind]=1; const nm=OSS_INS[k.kind]; ring(k.x,k.y,1.3,'#ffd86b'); burst(k.x,k.y,'#ffd86b',16,4,true); sfx('good'); G.banner={text:'📀 '+PTX(nm[0],nm[1]),sub:tr(KINDS[k.kind].name)+PTX(' +15% damage this run',' +15% de dano nesta partida'),t:2.4,col:'#ffd86b'}; META.instrN=(META.instrN||0)+1; saveMeta(); }
function ossDrawInstr(k){ const b=Math.sin(k.t*4)*.08; ctx.save(); glowAt(k.x,k.y+b,1.1,'#ffd86b',.7); ctx.translate(k.x,k.y+b); ctx.rotate(Math.sin(k.t*2)*.15);
  ctx.fillStyle='#1c1432'; ctx.fillRect(-.3,-.38,.6,.76); ctx.fillStyle=KINDS[k.kind].col; ctx.fillRect(-.26,-.34,.52,.36); ctx.fillStyle='#ffd86b'; ctx.fillRect(-.26,.06,.52,.08); ctx.strokeStyle='#fff'; ctx.lineWidth=.04; ctx.strokeRect(-.3,-.38,.6,.76);
  ctx.scale(1/48,1/48); ctx.font='18px system-ui,"Apple Color Emoji",sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(KINDS[k.kind].ico,0,-8); ctx.restore(); }
function ossPickTick(){ const P=G.party; for(const k of G.pickups){ if(k.type!=='instr'||k.dead) continue; for(const h of P){ const q=hpos(h); if(dist(q.x,q.y,k.x,k.y)<.75){ k.dead=true; ossInstrPick(k); break; } } } }

// ---- round start / per-frame tick ----
function ossRoundStart(w,boss){ G.gev=null; G.gevDone=0; G.gevAt=boss||G.tut?1e9:G.t+rand(10,22); G.rc=[]; if(boss||w===1){ setTimeout(()=>{ if(G&&G.wave===w) ossRef(boss?'combate':'lutem'); },900); }
  const g=META.grudge; if(g&&!boss&&!G.daily&&!G.nemDone&&w>=Math.min(g.w,4)&&w>=2){ setTimeout(()=>{ if(G&&G.wave===w&&G.phase==='fight') ossGrudgeSpawn(); },2600); } }
function ossFunTick(dt){ if(!G||G.state!=='play') return; ossCrowdTick(dt); ossPetTick(dt); ossNemTick(dt); ossPickTick();
  if(G.phase==='fight'&&!G.gev&&!G.gevDone&&G.t>=(G.gevAt||1e9)&&G.enemies.length>2&&G.wave>=3&&Math.random()<.5){ G.gevDone=1; ossEvStart(); } else if(G.phase==='fight'&&!G.gev&&!G.gevDone&&G.t>=(G.gevAt||1e9)){ G.gevDone=1; }
  if(G.gev){ G.gev.t+=dt; if(G.gev.ev.id==='drill'&&G.spawnQ.length<3&&Math.random()<dt*.8) G.spawnQ.push(pickType(G.wave)), G.waveTotal++; if(G.gev.t>=G.gev.ev.dur||G.phase!=='fight') ossEvEnd(); } }

// ---- 3. Daily Superfight share card ----
const OSS_DAY0=Date.UTC(2026,10,25);
function ossDayN(){ const d=new Date(); return Math.max(1,Math.floor((Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())-OSS_DAY0)/864e5)+1); }
function ossSfLine(){ const w=G.wave||0, sq=[]; for(let i=1;i<=10;i++){ const rd=i*5; sq.push(w>rd?'🟩':w===rd?'🟨':'⬛'); } return sq.join(''); }
function ossSfText(){ return PTX(`🥋 Oss! Squad Daily Superfight #${ossDayN()}\nRound ${G.wave} · ${G.score.toLocaleString()} pts\n${ossSfLine()}`,`🥋 Oss! Squad Superluta Diária #${ossDayN()}\nRound ${G.wave} · ${G.score.toLocaleString()} pts\n${ossSfLine()}`); }
function ossSfCard(){ const c=document.createElement('canvas'); c.width=1080; c.height=1080; const x=c.getContext('2d');
  const g=x.createLinearGradient(0,0,0,1080); g.addColorStop(0,'#3a2170'); g.addColorStop(1,'#120c22'); x.fillStyle=g; x.fillRect(0,0,1080,1080);
  x.textAlign='center'; x.fillStyle='#ffd86b'; x.font='900 92px system-ui,sans-serif'; x.fillText('OSS! SQUAD',540,150);
  x.fillStyle='#fff'; x.font='800 54px system-ui,sans-serif'; x.fillText(PTX('DAILY SUPERFIGHT #','SUPERLUTA DIÁRIA #')+ossDayN(),540,230);
  try{ const n=G.party.length, sz=Math.min(180,900/Math.max(1,n)); G.party.forEach((h,i)=>{ const im=HST&&HST.chibi&&HST.chibi[h.kind]; if(im&&im.complete) x.drawImage(im,540-n*sz/2+i*sz,300,sz,sz); }); }catch(_){}
  x.fillStyle='#ffd86b'; x.font='900 150px system-ui,sans-serif'; x.fillText(G.score.toLocaleString(),540,680);
  x.fillStyle='#efe7ff'; x.font='700 56px system-ui,sans-serif'; x.fillText(PTX('Round ','Round ')+G.wave+' · '+G.kills+PTX(' rivals',' rivais'),540,770);
  x.font='72px system-ui,"Apple Color Emoji","Segoe UI Emoji",sans-serif'; x.fillText(ossSfLine(),540,880);
  x.fillStyle='#d4c4ff'; x.font='600 40px system-ui,sans-serif'; x.fillText(PTX('Same rounds for everyone. One try a day. Beat me!','Mesmos rounds para todos. Uma chance por dia. Me supera!'),540,980);
  return c; }
async function ossSfShare(btn){ const txt=ossSfText(), url=siteUrl(); const done=m=>{ if(btn){ const o=btn.textContent; btn.textContent=m; setTimeout(()=>{btn.textContent=o;},1800); } };
  try{ const c=ossSfCard(); const blob=await new Promise(r=>c.toBlob(r,'image/png')); const f=new File([blob],'oss-squad-superfight.png',{type:'image/png'});
    if(navigator.canShare&&navigator.canShare({files:[f]})){ await navigator.share({files:[f],text:txt+(url?'\n'+url:''),title:'Oss! Squad'}); return; }
    if(navigator.share){ await navigator.share({text:txt,url:url||undefined,title:'Oss! Squad'}); return; }
    const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='oss-squad-superfight.png'; a.click();
    if(navigator.clipboard) navigator.clipboard.writeText(txt+(url?'\n'+url:'')).then(()=>done(PTX('✅ Copied + saved!','✅ Copiado + salvo!')),()=>done('✅')); }catch(_){} }
function ossSfPanel(){ if(!G||!G.daily) return ''; return `<div class="sfcard"><div class="sfl">${ossSfLine()}</div><button class="btn" id="sfShare">📣 ${PTX('Share my Superfight','Compartilhar minha Superluta')}</button></div>`; }
window.__ossFun={ossCutIn,ossFinCheck,ossFinTap,ossEvStart,ossGrudgeSpawn,ossDropInstr,ossGymShop,ossSfPanel,ossSfCard,ossOnKill,get G(){return G;},get META(){return META;},setATK:k=>{ATK=k;}};
