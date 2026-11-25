# Applies the jiu-jitsu fork changes to a pristine Everlight template.
# Usage: python3 -I patch_tpl.py <pristine_src_dir> <project_dir>
import sys, re, json
SRC, DST = sys.argv[1], sys.argv[2]
s = open(SRC + '/story/index_tpl.html').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count} of {old[:70]!r}, found {n}'
    s = s.replace(old, new)

def rre(pat, new, count=1, flags=re.S):
    global s
    s2, n = re.subn(pat, new, s, flags=flags)
    assert n == count, f'expected {count} of /{pat[:60]}/, found {n}'
    s = s2

NAME = 'Oss! Squad'

# ---------- 1. Branding + hidden build ----------
rep('<title>Everlight Heroes — lead your party of heroes and bring back the light</title>',
    '<title>Oss! Squad — lead your grappling crew and break the Master Spell</title>\n<meta name="robots" content="noindex,nofollow">')
rre(r'<meta name="description" content="Everlight Heroes is[^"]*">',
    '<meta name="description" content="Oss! Squad is a free grappling party adventure: steer your crew of wrestlers, judokas and jiu-jiteros, recruit teammates, pick upgrades and free the champions from the Master Spell. Plays on phone or desktop.">')
rep('Everlight<br>Heroes', 'Oss!<br>Squad')
rep('EVERLIGHT<br>HEROES', 'OSS!<br>SQUAD')
rep("'Champion of Everlight'", "'Champion of the Mat'")
rep('The tale of the Everlight. A new chapter plays each time you reach a new zone. Tap Skip any time.',
    'The tale of the Master Spell. A new chapter plays each time you free a champion. Tap Skip any time.')
rep("'A história da Luz Eterna':'The Tale of the Everlight'", "'A história do Feitiço Mestre':'The Tale of the Master Spell'")
rep("PT?'Cinquenta andares. Dez chefões. Dez fragmentos.<br>Traga a luz de volta!':'Fifty floors. Ten bosses. Ten shards.<br>Bring the light home!'",
    "PT?'Academia por academia. Campeão por campeão.<br>Quebre o Feitiço Mestre!':'Academy by academy. Champion by champion.<br>Break the Master Spell!'")
s = s.replace('Everlight Heroes', NAME)   # remaining title/meta/share/settings strings
rep("<p>Lead your party of heroes in a conga line. They fight on their own &mdash; you steer.</p>",
    "<p>Lead your grappling crew in a conga line. They roll on their own &mdash; you steer.</p>")

# Everlight.com migration hand-off: not needed in a standalone game
rre(r'<script>\s*// Moving to everlightheroes\.com.*?</script>\s*', '')

# Crash reports went to Everlight's server: off until this game has its own
rep("var u='https://save-api-production-4197cec9.up.railway.app/err';", "var u='';if(!u)return;")

# ---------- 2. Own save keys ----------
n = s.count('dungeonConga.')
s = s.replace('dungeonConga.', 'ossSquad.')
print('storage keys renamed:', n)
assert 'dungeonConga' not in s

# Cloud saves/reviews: separate server later. Until then every call fails softly.
rep("const CLOUD_URL='https://save-api-production-4197cec9.up.railway.app';",
    "const CLOUD_URL=''; // TODO: this game's own save server (never Everlight's)\n"
    "function cFetch(p,o){ return CLOUD_URL?fetch(CLOUD_URL+p,o):Promise.reject(new Error(PTL()?'Salvar na nuvem chega em breve.':'Cloud save is coming soon.')); }")
n = s.count('fetch(CLOUD_URL+')
s = s.replace('fetch(CLOUD_URL+', 'cFetch(')
print('cloud fetches guarded:', n)

# ---------- 3. Classes ----------
CL = {
 'knight': ("Wrestler", '🤼', "Passive: Base. The whole crew takes 10% less damage."),
 'archer': ("Judoka", '🥋', None),
 'mage':   ("Sambo", '💥', None),
 'cleric': ("Coach", '📋', "Passive: corner advice heals the most hurt teammate, and every shout heals too."),
 'rogue':  ("Jiu-jitero", '🔺', "Passive: submissions (critical hits) deal 2.5x damage."),
 'bard':   ("Athlete", '⏱️', "Passive: conditioning aura gives the crew +8% attack speed and +10% damage. Every 5s a breather heals everyone a little."),
 'necro':  ("Academy Owner", '🏫', "Passive: calls a student onto the mat every few seconds to fight for you."),
}
old_kinds = {
 'knight': ("Knight", '🛡️', 'Passive: Guard. The whole party takes 10% less damage.'),
 'archer': ("Archer", '🏹', None),
 'mage':   ("Mage", '🔮', None),
 'cleric': ("Cleric", '✨', 'Passive: heals the most hurt hero, and every smite heals too.'),
 'rogue':  ("Rogue", '🗡️', 'Passive: critical hits deal 2.5x damage.'),
 'bard':   ("Bard", '🎵', 'Passive: party gets +8% attack speed and +10% damage. Every 5s a song heals everyone a little.'),
 'necro':  ("Necromancer", '💀', 'Passive: raises a skeleton every few seconds to fight for you.'),
}
for k, (on, oi, op) in old_kinds.items():
    nn, ni, np_ = CL[k]
    rep(f"  {k}:{{name:'{on}',ico:'{oi}',", f"  {k}:{{name:'{nn}',ico:'{ni}',")
    if op: rep(f"pas:'{op}'", f"pas:'{np_}'")
rep("const KSHORT={necro:'Necro'};", "const KSHORT={necro:'Mestre',rogue:'Jiu-jitero'};")

SK = {
 'knight': (("Shockwave",'💢',"Slams the ground, damaging and shoving back nearby foes."), ("Double-Leg Slam",'💢',"A huge takedown slams the mat, damaging and knocking back nearby foes.")),
 'archer': (("Arrow Rain",'🌧️',"Calls a storm of arrows down on the densest group."), ("Ippon Storm",'🌪️',"A flurry of big throws crashes down on the densest group.")),
 'mage':   (("Meteor",'☄️',"Drops a meteor on the biggest cluster of enemies."), ("Suplex Bomb",'☄️',"Launches a massive throw-into-leglock on the biggest cluster of enemies.")),
 'cleric': (("Sanctuary",'🔆',"A healing aura follows the Cleric for 5 seconds."), ("Water Break",'💧',"Corner advice heals the crew around the Coach for 5 seconds.")),
 'bard':   (("Crescendo",'🎶',"The whole party attacks 35% faster for 5 seconds."), ("Second Wind",'🫁',"The whole crew attacks 35% faster for 5 seconds.")),
 'necro':  (("Raise Dead",'💀',"Summons skeleton warriors that hunt enemies for 8 seconds."), ("Open Mat",'📣',"Calls in students who hunt enemies for 8 seconds.")),
 'rogue':  (("Blade Dance",'🌪️',"Spins through nearby enemies, shredding up to six."), ("Scramble",'🔁',"Scrambles through nearby enemies, submitting up to six.")),
}
for k, ((on, oi, od), (nn, ni, nd)) in SK.items():
    rep(f"{k}:{{name:'{on}',ico:'{oi}',", f"{k}:{{name:'{nn}',ico:'{ni}',")
    rep(f"desc:'{od}'", f"desc:'{nd}'")

UPT = [  # class upgrade text
 ("title:'Whirlwind',desc:'Wider sword sweep and +10% damage.'", "title:'Long Arms',desc:'Wider reach and +10% damage.'"),
 ("title:'Thorns',desc:'Reflects damage to enemies that hit him.'", "title:'Heavy Hips',desc:'Reflects damage to enemies that hit him.'"),
 ("title:'Bulwark',desc:'Takes 15% less damage.'", "title:'Iron Base',desc:'Takes 15% less damage.'"),
 ("title:'Multishot',desc:'+1 arrow per volley.'", "title:'Combo Throws',desc:'+1 throw per volley.'"),
 ("title:'Piercing Shots',desc:'Arrows pierce +1 enemy.'", "title:'Follow-Through',desc:'Throws hit +1 more enemy.'"),
 ("title:'Twin Orbs',desc:'+1 fireball per cast.'", "title:'Double Attack',desc:'+1 bomb per cast.'"),
 ("title:'Legion',desc:'+1 skeleton per Raise Dead.'", "title:'Packed Class',desc:'+1 student per Open Mat.'"),
 ("title:'Bone Ward',desc:'Skeletons last 3s longer and hit 25% harder.'", "title:'Black Belt Students',desc:'Students last 3s longer and hit 25% harder.'"),
 ("title:'Encore',desc:'+1 note per song.'", "title:'Extra Rounds',desc:'+1 burst per breather.'"),
 ("title:'Greater Heal',desc:'+50% healing power.'", "title:'Better Advice',desc:'+50% healing power.'"),
 ("title:'Mass Heal',desc:'Each heal also mends the whole party a little.'", "title:'Team Huddle',desc:'Each heal also mends the whole crew a little.'"),
 ("title:'Assassin',desc:'+15% critical chance.'", "title:'Killer Instinct',desc:'+15% submission (crit) chance.'"),
]
for a, b in UPT: rep(a, b)

# Landing page / how-to texts that list the classes
rep("'Knight, Archer, Mage, Cleric, Rogue, Bard and Necromancer, each with their own powers.'",
    "'Wrestler, Judoka, Jiu-jitero, Sambo, Coach, Athlete and Academy Owner, each with their own moves.'")
rep("[['knight','Knight','Cavaleiro'],['archer','Archer','Arqueiro'],['mage','Mage','Mago'],['cleric','Cleric','Clérigo'],['rogue','Rogue','Ladino'],['bard','Bard','Bardo'],['necro','Necromancer','Necromante']]",
    "[['knight','Wrestler','Lutador'],['archer','Judoka','Judoca'],['rogue','Jiu-jitero','Jiu-jiteiro'],['mage','Sambo','Sambista'],['cleric','Coach','Treinador'],['bard','Athlete','Atleta'],['necro','Academy Owner','Mestre']]")

# Camp -> Academy (display only; ids stay)
rep("${uIco('m_camp',30,'🏰')}<span>Camp</span>", "${uIco('m_camp',30,'🥋')}<span>${PTL()?'Academia':'Academy'}</span>")
rep("tr('goes straight to your Camp bank')", "tr('goes straight to your Academy bank')")
rep("<b>🏰 Camp</b> on permanent perks and to unlock heroes", "<b>🥋 Academy</b> on permanent perks and to unlock classes")
rep('<h2>🏰 Camp</h2>', "<h2>🥋 ${PTL()?'Academia':'Academy'}</h2>")

# ---------- 4. Starting classes + locked classes ----------
rep("m.unlocked=Array.isArray(m.unlocked)?m.unlocked:['knight','archer','mage'];",
    "m.unlocked=Array.isArray(m.unlocked)?m.unlocked:START_KINDS.slice();")
rep("m.party=Array.isArray(m.party)&&m.party.length===3?m.party:['knight','archer','mage'];",
    "m.party=Array.isArray(m.party)&&m.party.length===3?m.party:START_KINDS.slice(); m.party=m.party.map((k,i)=>m.unlocked.includes(k)?k:START_KINDS[i]);")
rep("META[k]=k==='unlocked'?['knight','archer','mage']:[];", "META[k]=k==='unlocked'?START_KINDS.slice():[];")
rep("META.party=['knight','archer','mage'];", "META.party=START_KINDS.slice();")
rep("const HERO_UNLOCK={cleric:400,rogue:500,bard:700,necro:1000};",
    "// Wrestler, Judoka, Jiu-jitero start unlocked. The rest: free region N's champion, or buy in the Academy.\n"
    "const START_KINDS=['knight','archer','rogue'];\n"
    "const HERO_UNLOCK={mage:400,cleric:500,bard:700,necro:1000};\n"
    "const REGION_UNLOCK=['mage','cleric','bard','necro']; // region 1..4 champion frees this class\n"
    "function kindPool(){ const u=(typeof META!=='undefined'&&META&&META.unlocked)||START_KINDS; const p=KIND_LIST.filter(k=>u.includes(k)); return p.length?p:START_KINDS.slice(); }\n"
    "function unlockKind(k,how){ if(!KINDS[k]||META.unlocked.includes(k)) return false; META.unlocked.push(k); saveMeta(); return true; }\n"
    "function unlockCard(k,done){ const K=KINDS[k],S=SKILLS[k],P=PTL(); sfx('good');\n"
    "  showOverlay(`<div class=\"card intro\" style=\"border-color:${K.col};box-shadow:0 0 40px ${K.col}66,0 14px 50px #000c\"><div class=\"tag\" style=\"color:${K.col}\">🎉 ${P?'NOVA CLASSE':'NEW CLASS'}</div><div class=\"ibig\" style=\"background:radial-gradient(circle,${K.col}55,transparent 70%)\">${K.ico}</div><h2>${P?tr(K.name)+' entrou na academia!':K.name+' joined the academy!'}</h2><p><b>${S.ico} ${tr(S.name)}</b> &mdash; ${tr(S.desc)}</p>${K.pas?'<p style=\"font-size:13px;opacity:.85\">'+tr(K.pas)+'</p>':''}<p style=\"font-size:13px;opacity:.85\">${P?'Agora pode aparecer no tatame e entrar na sua equipe inicial.':'Can now show up on the mat and join your starting crew.'}</p><button class=\"btn\" id=\"ulGo\">OSS!</button></div>`);\n"
    "  $('ulGo').onclick=done; }")
# Locked classes never show up as recruits
rep("const P=G.party,again=againKinds(),rec=G.flagHist||(G.flagHist=[]);\n  const w=KIND_LIST.map(",
    "const P=G.party,again=againKinds(),rec=G.flagHist||(G.flagHist=[]);\n  const w=kindPool().map(")
rep("const counts={};KIND_LIST.forEach(k=>counts[k]=0);P.forEach(h=>counts[h.kind]++);\n    const weights=KIND_LIST.map(",
    "const counts={};KIND_LIST.forEach(k=>counts[k]=0);P.forEach(h=>counts[h.kind]++);\n    const weights=kindPool().map(")
rep("if(nk===kind) nk=KIND_LIST.filter(k=>k!==kind)[Math.floor(Math.random()*(KIND_LIST.length-1))];",
    "if(nk===kind){ const ot=kindPool().filter(k=>k!==kind); if(ot.length) nk=ot[Math.floor(Math.random()*ot.length)]; }")
# Freeing a region champion unlocks its class (celebration card queued like other intros)
rep("qEv('kill'); if(e.type==='boss'){qEv('boss'); bossVO(bossIdx(G.wave),1);}",
    "qEv('kill'); if(e.type==='boss'){qEv('boss'); bossVO(bossIdx(G.wave),1); const uk=REGION_UNLOCK[bossIdx(G.wave)]; if(uk&&unlockKind(uk,'boss')){ (G.introQ=G.introQ||[]).push({kind:'unlock',id:uk}); if(!G.inIntro&&!G.choosing) setTimeout(()=>{ if(G&&!G.inIntro&&!G.choosing) nextIntro(); },1400); }}")
rep("  if(q.kind==='floor'){showFloorNew(q.items);return;}",
    "  if(q.kind==='floor'){showFloorNew(q.items);return;}\n  if(q.kind==='unlock'){unlockCard(q.id,nextIntro);return;}")
# Academy: locked classes with both unlock rules
rep("""const heroes=Object.keys(HERO_UNLOCK).filter(k=>!META.unlocked.includes(k)).map(k=>{const c=HERO_UNLOCK[k];
    return `<div class="it"><div class="ic" style="width:38px">${pic(k,36)}</div><div class="tx"><b>Recruit the ${KINDS[k].name}</b><br>Unlocks them as a starting hero</div><button class="btn buy" data-hero="${k}" ${META.bank<c?'disabled':''}>${c} 🪙</button></div>`}).join('');""",
    """const PA=PTL(), heroes=Object.keys(HERO_UNLOCK).filter(k=>!META.unlocked.includes(k)).map(k=>{const c=HERO_UNLOCK[k],rg=REGION_UNLOCK.indexOf(k)+1,K=KINDS[k];
    return `<div class="it locked"><div class="ic" style="width:38px;font-size:28px;filter:grayscale(.6)">${K.ico}</div><div class="tx"><b>🔒 ${tr(K.name)}</b> <small style="opacity:.75">${tr(SKILLS[k].name)}</small><br><small>${PA?`Liberte o campeão da região ${rg}, <b>ou</b> entre agora por ${c} 🪙`:`Free the region ${rg} champion, <b>or</b> join now for ${c} 🪙`}</small></div><button class="btn buy" data-hero="${k}" ${META.bank<c?'disabled':''}>${c} 🪙</button></div>`}).join('');""")
rep("if(META.bank>=c){META.bank-=c;META.unlocked.push(k);saveMeta();sfx('good');camp();}});",
    "if(META.bank>=c&&!META.unlocked.includes(k)){META.bank-=c;unlockKind(k,'buy');unlockCard(k,camp);}});")
s = s.replace('🏰 Camp', '🥋 Academy')
rep("${META.bank} 🪙 banked · Best floor", "${META.bank} 🪙 ${PTL()?'em mensalidades':'mat fees'} · Best floor")
rep("<p style=\"margin:2px 0\">Starting party <small>(tap a slot to swap)</small></p>",
    "<p style=\"margin:2px 0\">${PTL()?'Equipe inicial':'Starting crew'} <small>(${PTL()?'toque para trocar':'tap a slot to swap'})</small></p>")
rep("`🔒 Unlock in Camp &middot; ${HERO_UNLOCK[k]||'?'} 🪙`",
    "`🔒 ${PTL()?'Liberte o campeão da região '+(REGION_UNLOCK.indexOf(k)+1)+' ou '+(HERO_UNLOCK[k]||'?')+' 🪙 na Academia':'Free the region '+(REGION_UNLOCK.indexOf(k)+1)+' champion or '+(HERO_UNLOCK[k]||'?')+' 🪙 in the Academy'}`")

# ---------- 5. Story: text-first frames, no Everlight art/voice ----------
rep("nx.onerror=()=>{nx.style.opacity=0;};\n    nx.src=storyUrl(c.id+'_'+i,'webp'); bg.style.backgroundImage='url(\"'+nx.src+'\")';",
    "nx.onerror=()=>{nx.style.opacity=0;};\n    { const su=storyUrl(c.id+'_'+i,'webp'); host.classList.toggle('txtonly',!su); if(su){ nx.src=su; bg.style.backgroundImage='url(\"'+su+'\")'; } else { nx.removeAttribute('src'); bg.style.backgroundImage=''; } }\n    host.style.setProperty('--sty-e',JSON.stringify(f.e||''));")
rep("const pre=k=>{const im=new Image(); im.src=storyUrl(k,'webp');};",
    "const pre=k=>{const u=storyUrl(k,'webp'); if(!u) return; const im=new Image(); im.src=u;};")
rep("</head>", """<style>
#story.txtonly .sty-bg{background:radial-gradient(ellipse at 50% 30%,#3a1f5c 0%,#150c24 60%,#07040d 100%)!important;filter:none!important;opacity:1!important}
#story.txtonly .sty-img{display:flex;align-items:center;justify-content:center}
#story.txtonly .sty-img::after{content:var(--sty-e);font-size:min(34vw,34vh);line-height:1;filter:drop-shadow(0 0 30px #b06bff88);animation:styPulse 3s ease-in-out infinite}
@keyframes styPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
</style>
</head>""")

rep("'Lidere seu grupo. Recrute heróis. Traga a luz de volta.':'Lead your party. Recruit heroes. Bring back the light.'", "'Lidere sua equipe. Recrute lutadores. Quebre o Feitiço Mestre.':'Lead your crew. Recruit grapplers. Break the Master Spell.'")
rep("'Climb the tower, beat each boss and win back a shard of the Everlight.'", "'Fight academy by academy and free each champion from the Master Spell.'")
rep("'Suba a torre, vença cada chefão e recupere um fragmento da Luz Eterna.'", "'Lute academia por academia e liberte cada campeão do Feitiço Mestre.'")
rep("['🛡️','7 heróis','Cavaleiro, Arqueiro, Mago, Clérigo, Ladino, Bardo e Necromante, cada um com seus poderes.']", "['🥋','7 classes','Lutador, Judoca, Jiu-jiteiro, Sambista, Treinador, Atleta e Mestre, cada um com seus golpes.']")
rep("['🛡️','7 heroes','Wrestler,", "['🥋','7 classes','Wrestler,")

# ---------- 6. Region 1: Garage Gym, spell-bound belts, the Pressure King ----------
rep("const BOSS_NAMES=['OGRE KING',", "const BOSS_NAMES=['THE PRESSURE KING',")
rep("{name:'The Crypt',", "{name:'Garage Gym',")
rep("slime:['🟢','Slime','Slow and squishy. Swarms wear you down.'],bat:['🦇','Bat','Fast flyer that darts at your tail.']",
    "slime:['🤍','White Belt','Spell-bound beginner. Slow, but they come in swarms.'],bat:['💙','Blue Belt','Spell-bound scrambler. Fast, and goes for your tail.']")
rep("bat:'New monster: Bat'", "bat:'New rival: Blue Belt'")
rep('["Who dares wake the Ogre King? Hmph! Snack time!", "Quem ousa acordar o Rei Ogro? Hmpf! Hora do lanche!"]',
    '["You came to MY gym? Hope you like carrying weight!", "Vieram na MINHA academia? Espero que gostem de carregar peso!"]')


# ---------- 7. Original Oss! Squad art (Higgs), loaded from one CDN bundle ----------
_U=_json0=__import__('json').load(open(DST+'/content/urls.json'))
ART_URL=_U['art']; ATLAS_URL=_U['atlas']; STORY_URL=_U['story']
rep('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="noindex,nofollow">\n<script>/* CDN serves .js as text/plain+nosniff, so fetch and run instead of <script src> */\n(function(){function L(u,cb){fetch(u).then(function(r){return r.text();}).then(function(t){try{(new Function(t))();}catch(e){} if(cb)cb();}).catch(function(){});}\nL("'+ART_URL+'",function(){ if(window.ossArtReady) ossArtReady(); });\nL("'+ATLAS_URL+'");\nL("'+STORY_URL+'");})();</script>')
rep("function storyUrl(k,ext){ if(window.DC_LOCAL_STORY)", "function storyUrl(k,ext){ if(ext==='webp'&&window.OSS_ART&&OSS_ART.story&&OSS_ART.story[k]) return OSS_ART.story[k]; if(window.DC_LOCAL_STORY)")
rep('<video class="lvid" autoplay muted loop playsinline preload="metadata" poster="https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/5c5892ef-ab39-4d2b-9b62-885c8544955b.jpg" aria-label="${P?\'Trecho do jogo\':\'Gameplay clip\'}"><source src="https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/24779acf-ad6b-4f1e-b0d1-de87e5fef0ec.mp4" type="video/mp4"></video>',
    '<img class="lvid" id="ossBanner" ${window.OSS_ART&&OSS_ART.banner?`src="${OSS_ART.banner}"`:\'\'} alt="${P?\'A equipe\':\'The crew\'}" style="object-fit:cover;width:100%;height:100%">')
rep('window.__dc={', """function applyOssArt(){ const A=window.OSS_ART; if(!A) return; const im=u=>{const i=new Image(); i.src=u; return i;};
  try{ for(const st in HST) for(const k in A.hst) HST[st][k]=im(A.hst[k]);
    for(const st of ['chibi','pixel','vector','vinyl']) if(MST[st]) for(const k in A.mst){ MST[st][k]=im(A.mst[k]); }
    for(const k in A.mst){ PSP[k]=[im(A.mst[k])]; } if(PSZ.boss) PSZ.boss0=PSZ.boss;
    for(const k in A.port){ PORT[k]=A.port[k]; try{ delete PIMG[k]; }catch(e){} }
    if(A.banner) document.documentElement.style.setProperty('--heroimg','url('+A.banner+')');
  }catch(e){} }
applyOssArt(); [2600,5000,9000].forEach(t=>setTimeout(applyOssArt,t)); // re-apply after the old boss atlases finish loading
window.__dc={""")


# ---------- 8. All 10 regions: champions (parody names), biomes, enemies, moves, story + voice wiring ----------
import json as _json
CT=_json.load(open(DST+'/content/content.json'))
B=CT['bosses']
rep("const BOSS_NAMES=['THE PRESSURE KING','SWAMP TYRANT','MAGMA LORD','FROST COLOSSUS','VOID EMPRESS','INK WARDEN','CRYSTAL TITAN','BRASS COLOSSUS','ABYSS HERALD','THE ABYSS KING'];",
    "const BOSS_NAMES="+_json.dumps([b['short'] for b in B],ensure_ascii=False)+"; const BOSS_FULL="+_json.dumps([b['name'] for b in B],ensure_ascii=False)+";")
for old,new in zip(['Overgrown Sewers','Ember Forge','Frozen Halls','Void Sanctum','Sunken Library','Crystal Caverns','Clockwork Vault','The Abyss'],[r['biome'] for r in CT['regions'][1:]]):
    rep("{name:'"+old+"',", "{name:'"+new.replace("'","\\'")+"',")
for old,b in zip(['GROUND CHARGE!','SLIME SWARM!','FIRE SPIRAL!','DEEP FREEZE!','VOID ORBS!','INK FLOOD!','SHARD RAIN!','PISTON SLAM!','WAR HORN!','SHADOW HAND!'],B):
    rep("say('"+old+"')", "say(PTL()?'"+b['move_pt']+"':'"+b['move']+"')")
# boss taunts (shown before each fight in the chapter) EN/PT
i=s.find('const BOSS_LINES='); j=s.find('];',i)+2
s=s[:i]+'const BOSS_LINES='+_json.dumps([[b['intro'],b['intro_pt']] for b in B],ensure_ascii=False)+';'+s[j:]
# enemies
E=CT['enemies']; i=s.find('const ENINFO={'); j=s.find('};',i)+2
EI={'slime':['🤍','White Belt','Spell-bound beginner. Slow, but they come in swarms.'],'bat':['💙','Blue Belt','Spell-bound scrambler. Fast, and goes for your tail.']}
for k,v in E.items():
    if k in ('inkwraith','shardgolem','cogknight','abyssfiend','shade','doomcaller'): continue
    EI[k]=v[:3]
EI['boss']=['👑','Champion','A spell-bound champion. Free them and the loot is great.']
s=s[:i]+'const ENINFO='+_json.dumps(EI,ensure_ascii=False)+';'+s[j:]
for k in ('inkwraith','shardgolem','cogknight','abyssfiend','shade','doomcaller'):
    m=re.search(k+r":\{base:'(\w+)',hp:([\d.]+),col:'([^']+)',n:'[^']*',d:'[^']*'\}",s); assert m,k
    s=s.replace(m.group(0), k+":{base:'"+m.group(1)+"',hp:"+m.group(2)+",col:'"+m.group(3)+"',n:"+_json.dumps(E[k][1])+",d:"+_json.dumps(E[k][2])+"}")
NEWN={'skel':'Tape Tosser','spider':'Mat Rat','brute':'Brown Belt Bruiser','ghost':'Shadow Roller','bomber':'Pre-Workout Kid','golem':'Super Heavyweight','wizard':'Spell Coach','charger':'Bull Rusher','shaman':'Cornerman','necro':'McDojo Sensei','splitter':'Tag Team Twins','voidling':'Spell Wisp','shade':'Ninja Roller','doomcaller':'Grand McDojo','inkwraith':'Phantom Roller','shardgolem':'Trophy Golem','cogknight':'The Turtler','abyssfiend':'Berserker'}
for k,n in NEWN.items():
    m=re.search(k+r":'New monster: [^']*'",s)
    if m: s=s.replace(m.group(0),k+":'New rival: "+n+"'")
s=s.replace("champions:\"New: the Champions' Hall\"","champions:\"New: the Hall of Champions\"")
# chapter card after each boss: champions freed, not shards
rep("${PT?'FRAGMENTO':'SHARD'} ${k} / 10</h2>", "${PT?'CAMPEÃO LIBERTADO':'CHAMPION FREED'} ${k} / 10</h2>")
rep("(PT?'Próximo chefão: ':'Next boss: ')", "(PT?'Próximo campeão: ':'Next champion: ')")
# narration: one file per language, each chapter a slice {s,e,t,f}
rep("me=aud=NARR, src=OFF||END?storyUrl('pt_story','mp3'):storyUrl(c.id,'mp3');",
    "me=aud=NARR, src=(A&&A.f)?storyUrl(A.f,'mp3'):(OFF||END?storyUrl('pt_story','mp3'):storyUrl(c.id,'mp3'));")
rep("const OFF=(SET.lang==='pt'&&STORY_PT.ch&&A)?A.s:0, END=(SET.lang==='pt'&&STORY_PT.ch&&A)?A.e:0;",
    "const OFF=(A&&A.s)||0, END=(A&&A.e)||0;")
rep("function storyUrl(k,ext){ if(ext==='webp'&&window.OSS_ART&&OSS_ART.story&&OSS_ART.story[k]) return OSS_ART.story[k];",
    "function storyUrl(k,ext){ if(ext==='webp'&&window.OSS_STORY&&OSS_STORY[k]) return OSS_STORY[k]; if(ext==='webp'&&window.OSS_ART&&OSS_ART.story&&OSS_ART.story[k]) return OSS_ART.story[k];")
# never load Everlight sprite atlases; ours arrive via OSS_ATLAS
rep("setTimeout(()=>{try{loadBossArt();}catch(e){}},0);","")
rep("setTimeout(()=>{try{loadArt2();}catch(e){}},50);","")
rep("setTimeout(()=>{try{loadEsty();}catch(e){}},80);","")
rep("setTimeout(()=>{try{loadMV();}catch(e){}},120);","")
rep('applyOssArt(); [2600,5000,9000]', """window.ossArtReady=function(){ applyOssArt(); try{ const b=document.getElementById('ossBanner'); if(b&&window.OSS_ART&&OSS_ART.banner) b.src=OSS_ART.banner; }catch(e){} };
window.ossAtlasReady=function(){ const X=window.OSS_ATLAS; if(!X) return; try{ loadArt2(X.art2); loadEsty(X.esty); loadMV(X.mv); ENVA.src=X.env; BART.spr=X.bspr; BART.por=X.bpor; BART.sty=X.bsty; loadBossArt(); }catch(e){} [3000,6000].forEach(t=>setTimeout(applyOssArt,t)); };
if(window.OSS_ATLAS) ossAtlasReady();
applyOssArt(); [2600,5000,9000]""")

rep('window.__dc={pickFlagKind,', 'window.__dc={camp:()=>camp(),unlockCard:(k,d)=>unlockCard(k,d),kindPool:()=>kindPool(),hideOverlay:()=>hideOverlay(),get G(){return G},pickFlagKind,')
open(DST + '/story/index_tpl.html', 'w').write(s)
print('template patched', len(s)//1024, 'KB')
