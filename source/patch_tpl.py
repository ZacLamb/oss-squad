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
rep('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="noindex,nofollow">\n<script>/* CDN serves .js as text/plain+nosniff, so fetch and run instead of <script src> */\n(function(){function L(u,cb,n){n=n||0;fetch(u,{cache:"force-cache"}).then(function(r){if(!r.ok)throw 0;return r.text();}).then(function(t){try{(new Function(t))();}catch(e){} if(cb)cb();}).catch(function(){ if(n<4) setTimeout(function(){L(u,cb,n+1);},1500*(n+1)); });}\nL("'+ART_URL+'",function(){ if(window.ossArtReady) ossArtReady(); });\nL("'+ATLAS_URL+'");\nL("'+STORY_URL+'");})();</script>')
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


# ---------- 9. Polish: achievement + event names, class icons from new portraits ----------
ACHN={'Dungeon Delver':'First Stripe','Deep Diver':'Blue Belt Energy','Abyss Walker':'Purple Belt Patience','Void Strider':'Brown Belt Grit','Dungeon Legend':'Black Belt Legend','Monster Masher':'Rival Roller','Slaughterhouse':'Open Mat Machine','Reaper':'Tap Collector','Relic Hoarder':'Medal Collector','Trap Expert':'Mat Awareness','Long Conga':'Long Conga Line','Small Band':'Small Crew','Marching Band':'Full Class','Dragon Hoard':'Gear Hoarder','Legendary Find':'Legendary Gear','Master of Arts':'Master of Moves','Champion Hunter':'Elite Hunter'}
for a,b in ACHN.items():
    if ("n:'"+a+"'") in s: s=s.replace("n:'"+a+"'","n:'"+b+"'")
s=s.replace("d:'Find all 10 boss relics'","d:'Win all 10 champion medals'").replace("d:'Discover every kind of trap'","d:'Discover every kind of mat hazard'")
s=s.replace("d:'Defeat 200 monsters in one run'","d:'Defeat 200 rivals in one run'").replace("d:'Defeat 500 monsters in one run'","d:'Defeat 500 rivals in one run'").replace("d:'Defeat 1000 monsters in one run'","d:'Defeat 1000 rivals in one run'").replace("d:'Defeat an elite of every monster type'","d:'Defeat an elite of every rival type'")
EV=[("{id:'vents',name:'Lava Vents',ico:'🌋',desc:'Fire erupts from the floor. It burns everyone!'}","{id:'vents',name:'Mat Burns',ico:'🔥',desc:'Scorching patches flare up on the mats. They burn everyone!'}"),
    ("{id:'moon',name:'Blood Moon',ico:'🌙',desc:'Monsters are faster but drop more loot.'}","{id:'moon',name:'Competition Day',ico:'🏟️',desc:'Rivals are faster but drop more loot.'}"),
    ("{id:'spring',name:'Healing Spring',ico:'⛲',desc:'Touch the spring to heal the party.'}","{id:'spring',name:'Water Break',ico:'🚰',desc:'Touch the water cooler to heal the crew.'}"),
    ("{id:'rush',name:'Gold Rush',ico:'💰',desc:'Gold rains from above. Kills pay extra.'}","{id:'rush',name:'Sponsor Day',ico:'💰',desc:'Coins rain from the stands. Wins pay extra.'}"),
    ("{id:'hail',name:'Ice Storm',ico:'🧊',desc:'Ice shards crash down. Watch the shadows!'}","{id:'hail',name:'Ice Bath Spill',ico:'🧊',desc:'Ice chunks crash down. Watch the shadows!'}"),
    ("{id:'rift',name:'Void Rifts',ico:'🌀',desc:'Rifts tear open and spit out Voidlings.'}","{id:'rift',name:'Spell Rifts',ico:'🌀',desc:'Rifts tear open and spit out Spell Wisps.'}")]
for a,b in EV: rep(a,b)
rep("dark:'New: dark floors, stay near your torch'","dark:'New: lights out, stay close to your crew'")
rep('function applyOssArt(){ const A=window.OSS_ART; if(!A) return; const im=u=>{const i=new Image(); i.src=u; return i;};',
    """function applyOssArt(){ const A=window.OSS_ART; if(!A) return; const im=u=>{const i=new Image(); i.src=u; return i;};
  try{ for(const k of KIND_LIST){ const u=A.port&&A.port['hero:'+k]; if(!u||(typeof UIC!=='undefined'&&UIC[k]&&UIC[k].__oss)) continue; const pi=new Image(); pi.onload=()=>{ try{ const c=document.createElement('canvas'); c.width=c.height=128; const x=c.getContext('2d'); x.beginPath(); x.arc(64,64,62,0,Math.PI*2); x.clip(); x.drawImage(pi,0,0,128,128); c.__oss=1; UIC[k]=c; try{UICU[k]=c.toDataURL('image/png');}catch(e){} window.__ossIcons=(window.__ossIcons||0)+1; clearTimeout(window.__ossIT); window.__ossIT=setTimeout(()=>{ try{ if(G&&G.party&&G.party.length) hud(true); }catch(e){} try{ if(document.getElementById('qstb')&&typeof menu==='function') menu(); }catch(e){} },60); }catch(e){ window.__ossIconErr=String(e); } }; pi.src=u; } }catch(e){ window.__ossIconErr=String(e); }""")

rep("keys.forEach((k,i)=>{ const c=document", "keys.forEach((k,i)=>{ if(UIC[k]&&UIC[k].__oss) return; const c=document")

# ---------- 10. Fixes: no hero flicker (whole-sprite animation, cached images), story slides not zoomed ----------
rep("function applyOssArt(){ const A=window.OSS_ART; if(!A) return; const im=u=>{const i=new Image(); i.src=u; return i;};",
    "function applyOssArt(){ const A=window.OSS_ART; if(!A) return; const IC=window.__ossImc||(window.__ossImc={}); const im=u=>IC[u]||(IC[u]=(()=>{const i=new Image(); i.__oss=1; i.src=u; return i;})());")
rep("  if(hsx&&hsx.complete&&hsx.naturalWidth){\n    const atk=h.atk>0,ph=hph(h),k=HSZ/56,X0=-HSZ/2,Y0=-HSZ;",
    """  if(hsx&&hsx.__oss&&hsx.complete&&hsx.naturalWidth){
    // Oss! Squad art: one whole sprite with a smooth bob, squash and waddle (no slicing, so nothing tears)
    const atk=h.atk>0,ph=hph(h),sn=Math.sin(ph),S=HSZ*1.08;
    if(wc){ctx.save();ctx.globalCompositeOperation='lighter';ctx.fillStyle=rg(0,.1,0,.65,[hexA(wc,.35),hexA(wc,0)]);ctx.beginPath();ctx.arc(0,.1,.65,0,TAU);ctx.fill();ctx.restore();}
    ctx.save(); ctx.translate(atk?.14*sw:0,.5-Math.abs(sn)*.06);
    ctx.rotate(sn*.05+(atk?.12*sw:0)); ctx.scale(1+Math.abs(sn)*.02,1-Math.abs(sn)*.025);
    ctx.drawImage(hsx,-S/2,-S,S,S); ctx.restore(); return;
  }
  if(hsx&&hsx.complete&&hsx.naturalWidth){
    const atk=h.atk>0,ph=hph(h),k=HSZ/56,X0=-HSZ/2,Y0=-HSZ;""")
rep("#story.txtonly .sty-bg{", """#story:not(.txtonly) .sty-img img{object-fit:contain!important;object-position:center 40%!important}
#story:not(.txtonly) .sty-img img.kb0{animation:okb0 14s ease-out forwards!important}
#story:not(.txtonly) .sty-img img.kb1{animation:okb1 14s ease-out forwards!important}
@keyframes okb0{from{transform:scale(1)}to{transform:scale(1.035)}}
@keyframes okb1{from{transform:scale(1.035)}to{transform:scale(1)}}
#story.txtonly .sty-bg{""")


# ---------- 11. Grappling upgrades, curses, paths, drinks, perks, gear, champion medals, combos ----------
for _old,_new in _json.load(open(DST+'/content/upgrades.json'))['swaps']: rep(_old,_new)


# ---------- 12. The team ultimate is "OSS!" (was NOVA) ----------
rep("Shield Wall, Arrow Storm, Meteor Shower, Holy Light, Shadow Strike, Encore or Bone Army.", "Wrestling Room, Ippon Party, Sambo Storm, Corner Crew, Submission Hunt, Conditioning Circuit or Full Academy.")
rep('aria-label="Party Nova"','aria-label="Team OSS"')
rep("'PARTY NOVA!'","'TEAM OSS!'")
s=s.replace('💥 Nova charge','💥 OSS charge')
s=re.sub(r'NOVA(?! CLASSE)','OSS',s)


# ---------- 13. Crew wording on upgrade/path screens ----------
rep("b('⚔️ +'+Math.round((r.enemyM-1)*100)+'% monsters'); if(r.enemyM<1)g('🕊️ fewer monsters');", "b('⚔️ +'+Math.round((r.enemyM-1)*100)+(PTL()?'% rivais':'% rivals')); if(r.enemyM<1)g(PTL()?'🕊️ menos rivais':'🕊️ fewer rivals');")
rep("${u.curse?'☠ CURSED':'PARTY-WIDE'}", "${u.curse?'☠ CURSED':(PTL()?'PARA TODOS':'CREW-WIDE')}")
rep("<b>Your Party</b>", "<b>${PTL()?'Sua Equipe':'Your Crew'}</b>")
rep("const sub=u.curse?'Cursed bargain':h?`${KINDS[h.kind].name}`:'Whole Party';", "const sub=u.curse?'Cursed bargain':h?`${KINDS[h.kind].name}`:'Whole Crew';")


# ---------- 14. Hero frame cache must key on the actual sprite image (fixes two-image flicker) ----------
rep("+'|'+(SET.hs||'')+'|'+k;}", "+'|'+(SET.hs||'')+'|'+k+'|'+(()=>{try{const im=HST[SET.hs]&&HST[SET.hs][h.kind];return im&&im.complete&&im.naturalWidth?(im.__oss?'o':'e')+im.naturalWidth+'.'+im.src.length:'x';}catch(e){return 'x';}})();}")


# ---------- 15. Traps become real gym dangers (behavior unchanged) ----------
_i=s.find('const HAZN='); _j=s.find('};',_i)+2
s=s[:_i]+"""const HAZN={rift:['⚠️','Mat gaps','Mats split apart every few seconds. Step off before the gap opens, and watch for rivals slipping out!'],ink:['🪢','Tangled jump ropes','Loose jump ropes trip up your line and drain your OSS meter. Go around!'],shard:['🥊','Swinging heavy bags','Heavy bags wind up, then swing. Stay out of the ring when they light up!'],saw:['🏋️','Rolling weight plates','Loose plates roll back and forth across the floor. Time your path between them.'],abyss:['🌪️','Open mat chaos','At open mat, every gym hazard shows up at once.'],spike:['⚠️','Broken tatami','Cracked mat tiles flip up — the red flash is your warning. Steer around them!'],water:['💧','Spilled water','Someone knocked over the water cooler. Wading through it slows your whole line down.'],lava:['🔥','Mat burn','Rough, overheated mats burn anyone standing on them — rivals too!'],ice:['💦','Sweat slick','Fresh sweat makes your line slide much faster. Careful with the turns!'],portal:['🚪','Locker room hatches','Step on a hatch and your line pops out at its twin. Use them to escape!']};"""+s[_j:]
for _o,_n in [("spike:'New trap: spikes'","spike:'New hazard: broken tatami'"),("water:'New: deep water slows you'","water:'New: spilled water slows you'"),("lava:'New trap: lava'","lava:'New hazard: mat burn'"),("ice:'New: slippery ice'","ice:'New: sweat slick'"),("portal:'New: portals'","portal:'New: locker room hatches'"),("ink:'New: sticky ink pools'","ink:'New: tangled jump ropes'"),("rift:'New trap: void rifts'","rift:'New hazard: mat gaps'"),("shard:'New trap: crystal pylons pulse'","shard:'New hazard: swinging heavy bags'"),("saw:'New trap: saw blades'","saw:'New hazard: rolling weight plates'"),("abyss:'New: the Abyss mixes every trap'","abyss:'New: open mat mixes every hazard'"),
  ("(PTL()?'Lava queima!':'Lava burns!'),sub:PTL()?'Saia das poças de lava':'Steer off the glowing pools'","(PTL()?'Queimadura de tatame!':'Mat burn!'),sub:PTL()?'Saia do tatame quente':'Steer off the hot mats'")]:
    rep(_o,_n)


# ---------- 16. Legacy belts (white -> red), new rivals, secret rivals, tag-team & secret bosses ----------
_LR=_json.load(open(DST+'/content/legacy_roster.json'))
_PSZB={'spider':[1.4,.46,0],'bat':[1.3,.4,-.15],'brute':[1.4,.5,0],'slime':[1.3,.46,0],'wizard':[1.4,.48,0],'golem':[1.5,.5,0],'charger':[1.5,.48,0],'shaman':[1.4,.48,0],'splitter':[1.4,.46,0],'ghost':[1.3,.4,-.1],'necro':[1.4,.48,0]}
_mut=[];_psz=[];_ul=[];_na=[];_pt=[];_sec=[]
for k,base,hp,fl,sec,ico,n,d,npt,dpt,art in _LR['rivals']:
    _mut.append(f"{k}:{{base:'{base}',hp:{hp},col:'#c08aff',n:{_json.dumps(n)},d:{_json.dumps(d)}{',sec:1' if sec else ''}}}")
    _psz.append(f"{k}:{_json.dumps(_PSZB[base])}")
    if sec: _sec.append(f"['{k}',(beltLv()>=2&&w>=8)?1.3:0]")
    else:
        _ul.append(f"{k}:{fl}"); _na.append(f"{k}:'New rival: {n}'"); _pt.append(f"['{k}',U('{k}')?3:0]")
for k,n,npt,art in _LR['bosses']:
    _mut.append(f"{k}:{{base:'boss',hp:1,col:'#ff3a3a',n:{_json.dumps(n)},d:'Secret boss',boss:1,sec:1}}")
    _psz.append(f"{k}:[1.7,.5,0]")
rep("const MUT={","const MUT={"+",".join(_mut)+",")
rep("boss:[1.7,.5,0]};","boss:[1.7,.5,0],"+",".join(_psz)+"};")
rep("const UNLOCK={","const UNLOCK={"+",".join(_ul)+",")
rep("const N={bat:'New rival: Blue Belt',","const N={"+",".join(_na)+",bat:'New rival: Blue Belt',")
rep("const o={};for(const k in UNLOCK)o[UNLOCK[k]]=N[k];return o;","const o={};for(const k in UNLOCK){const f=UNLOCK[k];if(N[k])o[f]=o[f]?o[f]+' · '+N[k]:N[k];}return o;")
rep("['abyssfiend',U('abyssfiend')?3:0]]","['abyssfiend',U('abyssfiend')?3:0],"+",".join(_pt+_sec)+"]")
rep("for(const k of Object.keys(MUT)){","for(const k of Object.keys(MUT).filter(k=>!MUT[k].boss)){")
rep("(PTL()?'Ainda não encontrado. Aparece no andar ':'Not met yet. Shows up from floor ')+UNLOCK[k]","(MUT[k].sec?(PTL()?'🔒 Rival secreto. Aparece a partir da faixa roxa no Legado.':'🔒 Secret rival. Shows up from Legacy purple belt.'):(PTL()?'Ainda não encontrado. Aparece no andar ':'Not met yet. Shows up from floor ')+UNLOCK[k])")
# sprites: per-enemy boss index for tag partners, mutant sprite in styled modes
rep("const bk2=e.type==='boss'?'boss'+bossIdx(G.wave):''","const bk2=e.type==='boss'?'boss'+(e.bi!=null?e.bi:bossIdx(G.wave)):''")
rep("MST[msk]['boss'+bossIdx(G.wave)]","MST[msk]['boss'+(e.bi!=null?e.bi:bossIdx(G.wave))]",count=3)
rep("?((e.type==='boss'&&MST[msk]['boss'+(e.bi!=null","?((e.type==='boss'&&!e.mut&&MST[msk]['boss'+(e.bi!=null")
rep(":MST[msk][e.type]):null",":((e.mut&&MST[msk][e.mut]&&MST[msk][e.mut].naturalWidth)?MST[msk][e.mut]:MST[msk][e.type])):null")
rep("if(e.elite)sc*=1.25;","if(e.elite)sc*=1.25; if(e.tag&&!e.secret)sc*=.85;")
rep("const bk=bossIdx(G.wave),bi=","const bk=e.bi!=null?e.bi:bossIdx(G.wave),bi=")
rep("const boss=G.enemies.find(e=>e.type==='boss');","const boss=G.enemies.find(e=>e.type==='boss'&&!e.tag&&!e.dead)||G.enemies.find(e=>e.type==='boss'&&!e.dead);")
rep("drawText(BOSS_NAMES[bossIdx(G.wave)],bx+bw/2","drawText(boss.sname||BOSS_NAMES[boss.bi!=null?boss.bi:bossIdx(G.wave)],bx+bw/2")
rep("if(e.type==='boss'&&!e.enraged&&UL('enrage',G.wave)&&e.hp<e.max*.5){","if(e.type==='boss'&&!e.tag&&!e.tag0&&beltLv()>=7){e.tag0=1;try{tagTeam(e,1);}catch(_){}} if(e.type==='boss'&&!e.tag&&!e.tagged&&e.hp<e.max*.5){e.tagged=1;try{tagTeam(e,0);}catch(_){}} if(e.type==='boss'&&!e.tag&&!e.enraged&&UL('enrage',G.wave)&&e.hp<e.max*.5){")
rep("qEv('kill'); if(e.type==='boss'){qEv('boss');","qEv('kill'); if(e.type==='boss'&&e.tag){try{tagDown(e);}catch(_){}} else if(e.type==='boss'){try{bossLootX(e);}catch(_){} qEv('boss');")
# belts + rewards
rep("Object.assign({won:0,lp:0,asc:0,best:0}","Object.assign({won:0,lp:0,asc:0,best:0,belt:-1}",count=2)
rep("const L=META.leg; L.won++; L.best=Math.max(L.best,G.wave);","const L=META.leg; const _pb=beltLv(); L.won++; L.best=Math.max(L.best,G.wave); G._promo=null; { const nb=Math.min(7,Math.max(0,L.asc)); if(nb>_pb){ L.belt=nb; G._promo=nb; } }")
rep("const lp=10+5*L.asc; L.lp+=lp;","const lp=3*(10+5*L.asc)+(G._promo!=null?25*(G._promo+1):0); L.lp+=lp;")
rep("const lp=Math.floor(G.wave/5)*(1+L.asc)","const lp=3*Math.floor(G.wave/5)*(1+L.asc)")
rep("<h1>👑 EVERLIGHT RESTORED!</h1><p>You fought through all <b>${MAX_FLOOR}</b> floors, toppled the Abyss King and brought the light home.</p>","<h1>👑 ${PTL()?'TORRE CONQUISTADA!':'TOWER CONQUERED!'}</h1><p>${PTL()?'Vocês venceram os '+MAX_FLOOR+' andares e libertaram o Campeão Mascarado.':'You fought through all '+MAX_FLOOR+' floors and freed the Masked Champion.'}</p>${G._promo!=null?beltPromo(G._promo):''}")
rep("const hpM=1+.015*META.perks.hp+.04*META.leg.perks.vit","const hpM=1+.015*META.perks.hp+.08*META.leg.perks.vit")
rep("dmgM:1+.01*META.perks.dmg+.04*META.leg.perks.might","dmgM:1+.01*META.perks.dmg+.08*META.leg.perks.might")
rep("(1+.05*META.leg.perks.bank)","(1+.1*META.leg.perks.bank)")
rep("(1+.05*L.perks.bank)","(1+.1*L.perks.bank)")
rep("+4% damage for every grappler","+8% damage for every grappler")
rep("+4% max HP for every grappler","+8% max HP for every grappler")
rep("+5% banked coins from every run","+10% banked coins from every run")
rep("Earn ⚜️ every run: 1 per 5 floors (× Ascension tier), +10 for conquering the Tower.","Earn ⚜️ every run: 3 per 5 floors (× Ascension tier), +30 or more for conquering the Tower, and a big bonus for every new belt. Conquer the Tower at a higher Ascension to earn the next belt.")
rep("bb=Math.min(.6,(boost||0)*2.5)","bb=Math.min(.6,((boost||0)+(beltLv()>=4?.12:0))*2.5)")
rep("7+Math.min(3,(META.leg&&META.leg.perks.slots)||0)","7+Math.min(3,(META.leg&&META.leg.perks.slots)||0)+(beltLv()>=6?1:0)")
rep("for(let i=0;i<META.perks.cache;i++) G.bag.push(rollItem(0,undefined,1)); }","for(let i=0;i<META.perks.cache;i++) G.bag.push(rollItem(0,undefined,1)); if(!G.daily){ if(beltLv()>=2) G.bag.push(rollItem(.3,undefined,2)); if(beltLv()>=4) G.bag.push(rollItem(.5,undefined,3)); } }")
rep("META.party.forEach((k,i)=>{k=KINDS[k]?k:'knight';const ex=!G.arcade&&G.party.find(h=>h.kind===k);if(ex)starUp(ex,true);else G.party.push(mkHero(k,sx-G.party.length,sy));}); }","META.party.forEach((k,i)=>{k=KINDS[k]?k:'knight';G.party.push(mkHero(k,sx-G.party.length,sy));}); if(!G.arcade&&!G.daily&&!G.duo){ const b=beltLv(); if(b>=1){ let pool=(META.unlocked||[]).filter(k=>KINDS[k]&&!G.party.some(h=>h.kind===k)); if(!pool.length) pool=KIND_LIST.filter(k=>KINDS[k]&&!G.party.some(h=>h.kind===k)); const k=pool.length?pool[Math.floor(Math.random()*pool.length)]:null; if(k) G.party.push(mkHero(k,sx-G.party.length,sy)); } if(b>=6&&G.party[0]&&(G.party[0].star||1)<2) starUp(G.party[0],true); } }")
rep("<div class=\"shop\">${perks}</div>","${beltLadder()}<div class=\"shop\">${perks}</div>")
rep("<h2>⚜️ Legacy Hall</h2><div class=\"bank\">${L.lp} ⚜️ points","<h2>⚜️ Legacy Hall</h2>${beltBadge()}<div class=\"bank\">${L.lp} ⚜️ points")
_SB={k:[n,npt] for k,n,npt,art in _LR['bosses']}
rep("const MUT={", "const SECB="+_json.dumps(_SB,ensure_ascii=False)+"; const BELTS=[['White Belt','Faixa Branca','#f4f4f4',null,'Legacy Hall opens. Legacy points ×3.','Salão do Legado aberto. Pontos de Legado ×3.'],['Blue Belt','Faixa Azul','#2f6fe0',null,'Start every run with a 4th grappler.','Comece toda corrida com um 4º lutador.'],['Purple Belt','Faixa Roxa','#8a3ad0',null,'6 secret rivals appear. Free Epic gear at the start of every run.','6 rivais secretos aparecem. Equipamento Épico grátis no início de cada corrida.'],['Brown Belt','Faixa Marrom','#7a4a22',null,'Tag-team bosses: a past champion jumps in at half health. Double boss loot.','Chefes em dupla: um campeão do passado entra na metade da vida. Saque de chefe em dobro.'],['Black Belt','Faixa Preta','#151515',null,'Better gear drops. Free Legendary gear at the start of every run.','Equipamentos melhores. Equipamento Lendário grátis no início de cada corrida.'],['Coral Belt','Faixa Coral','#151515','#d42020','Triple boss fights. Secret boss THE FOUNDER on floor 25.','Lutas triplas contra chefes. Chefe secreto O FUNDADOR no andar 25.'],['Coral Belt II','Faixa Coral II','#d42020','#f4f4f4','Start with a ★★ grappler. +1 crew slot.','Comece com um lutador ★★. +1 vaga na equipe.'],['Red Belt','Faixa Vermelha','#c81414',null,'GRAND MASTER. Tag teams from the first second of every boss fight. Secret final boss THE RED BELT on floor 50.','GRÃO-MESTRE. Duplas desde o primeiro segundo de toda luta de chefe. Chefe final secreto O FAIXA-VERMELHA no andar 50.']];\n"
 "function beltLv(){const L=META&&META.leg;if(!L)return -1;if(L.won>0&&!(L.belt>=0))L.belt=0;return L.belt>=0?L.belt:-1;}\n"
 "function beltSw(i,w,h){const B=BELTS[i];w=w||44;h=h||14;const bg=B[3]?`repeating-linear-gradient(90deg,${B[2]} 0 ${w/6}px,${B[3]} ${w/6}px ${w/3}px)`:B[2];return `<span style=\"display:inline-block;width:${w}px;height:${h}px;border-radius:3px;background:${bg};border:1px solid #0008;box-shadow:inset 0 -2px 0 #0003;vertical-align:middle;position:relative\"><span style=\"position:absolute;right:${w*.12}px;top:0;bottom:0;width:${w*.18}px;background:${i>=4&&i<7?'#c81414':i===7?'#111':'#111'};opacity:${i===7?.0:.85}\"></span></span>`;}\n"
 "function beltBadge(){const b=beltLv();if(b<0)return '';const B=BELTS[b];return `<div style=\"margin:4px 0 6px;font-weight:800\">${beltSw(b,64,18)} ${PTL()?B[1]:B[0]}${b===7?(PTL()?' · GRÃO-MESTRE':' · GRAND MASTER'):''}</div>`;}\n"
 "function beltLadder(){const b=beltLv();return '<div style=\"text-align:left;margin:6px 0 10px\"><b>'+(PTL()?'🥋 Faixas do Legado':'🥋 Legacy belts')+'</b>'+BELTS.map((B,i)=>`<div class=\"it\" style=\"opacity:${i<=b?1:.55}\"><div class=\"ic\" style=\"width:52px;display:flex;justify-content:center;align-items:center\">${beltSw(i)}</div><div class=\"tx\"><b>${i<=b?'✅ ':'🔒 '}${PTL()?B[1]:B[0]}</b><br><small>${PTL()?B[5]:B[4]}</small>${i>b?`<br><small style=\"opacity:.8\">${i===0?(PTL()?'Conquiste a Torre.':'Conquer the Tower.'):(PTL()?'Conquiste a Torre na Ascensão '+i+'.':'Conquer the Tower at Ascension '+i+'.')}</small>`:''}</div></div>`).join('')+'</div>';}\n"
 "function beltPromo(i){const B=BELTS[i];return `<div style=\"margin:8px 0;padding:10px;border-radius:12px;background:#0006;border:2px solid ${B[3]||B[2]}\"><div style=\"font-size:22px;font-weight:900\">🥋 ${PTL()?'PROMOVIDO!':'PROMOTED!'}</div><div style=\"margin:6px 0\">${beltSw(i,90,22)}</div><b>${PTL()?B[1]:B[0]}</b><br><small>${PTL()?B[5]:B[4]}</small><br><small style=\"color:#ffd86b\">+${25*(i+1)} ⚜️ ${PTL()?'bônus de faixa':'belt bonus'}</small></div>`;}\n"
 "function tagTeam(e,start){ if(!G||G.daily||G.tut) return; const b=beltLv(); if(b<3) return; const w=G.wave,cur=bossIdx(w); const n=start?1:(b>=5?2:1); const pool=[]; for(let i=0;i<Math.min(cur,9);i++) pool.push(i); const add=[]; if(!start&&b>=5&&w===25) add.push('founder'); if(!start&&b>=7&&w===50) add.push('redbelt'); const tgt=n+add.length; while(add.length<tgt&&pool.length) add.push(pool.splice(Math.floor(Math.random()*pool.length),1)[0]); if(!add.length) return; const nm=[];\n"
 "  for(const a of add){ const sec=typeof a==='string'; const p=spawnEnemy(sec?a:'boss'); p.tag=1; if(sec){ p.bi=9; p.secret=a; p.sname=SECB[a][PTL()?1:0]; p.hp=p.max=e.max*.7; } else { p.bi=a; p.hp=p.max=e.max*(start?.3:.35); p.dmgS*=.7; } p.x=clamp(e.x+rand(-2.2,2.2),.8,COLS-.8); p.y=clamp(e.y+rand(-2.2,2.2),.8,ROWS-.8); p.born=0; G.waveTotal++; G.portals.push({x:p.x,y:p.y,life:.6,max:.6,col:sec?'#ff2a2a':'#ff9a4a'}); ring(p.x,p.y,1.8,sec?'#ff2a2a':'#ff9a4a'); nm.push(sec?p.sname:BOSS_NAMES[a]); if(sec){ try{markSeen('secboss:'+a);}catch(_){} } }\n"
 "  const _bn={text:add.some(a=>typeof a==='string')?(PTL()?'⚠️ CHEFE SECRETO!':'⚠️ SECRET BOSS!'):(PTL()?'🤼 DUPLA!':'🤼 TAG TEAM!'),sub:nm.join(' + ')+(PTL()?' entrou na luta!':' jumped in!'),t:2.8,col:'#ff6a4a'}; G.shake=1; G.flash=.4; sfx('boom'); setTimeout(()=>{ if(G&&G.state==='play') G.banner=_bn; },900); }\n"
 "function tagDown(e){ G.score+=e.secret?5000:1500; G.pickups.push({type:'chest',x:e.x,y:e.y,t:0,item:rollItem(e.secret?.6:.35,undefined,e.secret?3:2)}); text(e.x,e.y-.8,(e.sname||BOSS_NAMES[e.bi]||'')+(PTL()?' saiu!':' tapped out!'),'#ffd86b',true); if(e.secret){ const L=META.leg; L.sec=L.sec||{}; if(!L.sec[e.secret]){ L.sec[e.secret]=1; L.lp+=50; saveMeta(); try{dtoast('🏆 '+(PTL()?'Segredo do Legado: ':'Legacy secret: ')+'<b>'+e.sname+'</b> +50 ⚜️','#ff5a5a');}catch(_){} } } }\n"
 "function bossLootX(e){ if(beltLv()<3||G.daily) return; for(let i=0;i<2;i++) G.pickups.push({type:'chest',x:clamp(e.x+rand(-1,1),.8,COLS-.8),y:clamp(e.y+rand(-1,1),.8,ROWS-.8),t:0,item:rollItem(.3,undefined,2)}); }\n"
 "const MUT={")

rep('window.__dc={pickFlagKind,', 'window.__dc={camp:()=>camp(),unlockCard:(k,d)=>unlockCard(k,d),kindPool:()=>kindPool(),hideOverlay:()=>hideOverlay(),get G(){return G},pickFlagKind,')

# ---------- 17. Never show the old fantasy crew: neutral fallback banner until the Oss art loads ----------
s=re.sub(r':root\{--heroimg:url\("data:image/webp;base64,[A-Za-z0-9+/=]+"\)\}', ':root{--heroimg:radial-gradient(circle at 30% 30%,#7a3ad0 0,#2a1450 55%,#140a24 100%)}', s, count=1)

# ---------- 18. Old Everlight A3 sprites (Shade/Doom Caller) must never replace the Oss rivals ----------
rep("if(k!=='rift'){const im=new Image();im.src=cv.toDataURL('image/png');PSP[k]=[im];}","")

# ---------- 19. New Oss icons: consumables, gear, relics, upgrades, perks, quests, menu, achievements, pickups ----------
rep("const POT={heal:{ico:'💧',n:'Water',","const POT={heal:{ico:'🍫',n:'Protein Bar',")
rep("dmg:{ico:'🧃',n:'Electrolytes',","dmg:{ico:'⚡',n:'Pre-Workout',")
rep("dr:{ico:'🧊',n:'Ice Bath',","dr:{ico:'🧊',n:'Ice Pack',")
rep("nova:{ico:'🍯',n:'Honey',","nova:{ico:'🍌',n:'Banana',")
rep("'Drink {n} potions'","'Grab {n} gym snacks'")
rep("'Run into crates and barrels with your leader to break them — they hide coins, potions and sometimes treasure.'","'Run into crates and barrels with your leader to break them — they hide coins, gym snacks and sometimes gear.'")
rep("'Potions drop from crates and elites.'","'Gym snacks drop from crates and elites.'")
rep("'Potion colours!'","'Gym snacks!'")
rep("function gearIco(it,px,fb){px=px||30;","function gearIco(it,px,fb){px=px||30; { const _k=it?(it.rid?'rl_'+it.rid:'g_'+String(it.base||'').toLowerCase().replace(/[^a-z]+/g,'_').replace(/^_|_$/g,'')):''; if(_k&&UICU[_k]) return `<img src=\"${UICU[_k]}\" alt=\"\" style=\"width:${px}px;height:${px}px;vertical-align:middle;object-fit:contain\">`; }")
rep("    if(A.banner) document.documentElement.style.setProperty('--heroimg','url('+A.banner+')');",
    "    if(A.banner) document.documentElement.style.setProperty('--heroimg','url('+A.banner+')');\n"
    "    if(A.icons){ let n=0; for(const k in A.icons){ if(UIC[k]&&UIC[k].__oss) continue; const u=A.icons[k]; if(k==='rift'){ const ri=new Image(); ri.onload=()=>{ const c=document.createElement('canvas'); c.width=c.height=192; c.getContext('2d').drawImage(ri,0,0,192,192); A3.rift=c; }; ri.src=u; continue; } const ii=new Image(); ii.onload=()=>{ try{ const c=document.createElement('canvas'); c.width=c.height=128; c.getContext('2d').drawImage(ii,0,0,128,128); c.__oss=1; UIC[k]=c; UICU[k]=u; if(++n===Object.keys(A.icons).length-1){ try{ if(G&&G.party&&G.party.length) hud(true); }catch(e){} try{ if(document.getElementById('qstb')&&typeof menu==='function'&&(!G||G.state!=='play')) menu(); }catch(e){} } }catch(e){} }; ii.src=u; }\n"
    "      for(const st in PKS){ for(const [pk,ik] of [['coin','w_coin'],['chest','w_chest'],['banner','w_banner']]){ if(A.icons[ik]) PKS[st][pk]=im(A.icons[ik]); } } }")

# ---------- 20. Tape Tossers throw rolls of athletic tape, not bones ----------
rep("else{ctx.fillStyle='#f1ead2';ctx.strokeStyle=OUT;ctx.lineWidth=.03;ctx.beginPath();ctx.moveTo(-.16,0);ctx.lineTo(.16,0);ctx.lineWidth=.07;ctx.strokeStyle='#f1ead2';ctx.stroke();ctx.fillStyle='#f1ead2';ctx.beginPath();ctx.arc(-.17,-.04,.045,0,TAU);ctx.arc(-.17,.04,.045,0,TAU);ctx.arc(.17,-.04,.045,0,TAU);ctx.arc(.17,.04,.045,0,TAU);ctx.fill();}",
    "else{ctx.scale(1.25,1.25);ctx.fillStyle='rgba(11,12,28,.35)';ctx.beginPath();ctx.ellipse(.03,.05,.2,.09,0,0,TAU);ctx.fill();ctx.fillStyle='#fbfaf4';ctx.strokeStyle='#2a2440';ctx.lineWidth=.035;ctx.beginPath();ctx.arc(0,0,.17,0,TAU);ctx.fill();ctx.stroke();ctx.strokeStyle='#d9d4c4';ctx.lineWidth=.025;ctx.beginPath();ctx.arc(0,0,.12,0,TAU);ctx.stroke();ctx.fillStyle='#b98a52';ctx.beginPath();ctx.arc(0,0,.075,0,TAU);ctx.fill();ctx.fillStyle='#3a2a1a';ctx.beginPath();ctx.arc(0,0,.04,0,TAU);ctx.fill();ctx.strokeStyle='#fbfaf4';ctx.lineWidth=.06;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(.16,.04);ctx.quadraticCurveTo(.28,.1,.34,.02);ctx.stroke();}")
rep("text(e.x,e.y-.6,'It rises!','#f0f0e0');","text(e.x,e.y-.6,PTL()?'Levantou de novo!':'Back on their feet!','#f0f0e0');")

# ---------- 21. Gym names for elite flavors and crew combos ----------
rep("swift:{c:'#7fdcff',ico:'💨',n:'Swift'},bulwark:{c:'#d0d0e0',ico:'🛡️',n:'Bulwark'},volatile:{c:'#ff8a3a',ico:'💥',n:'Volatile'}","swift:{c:'#7fdcff',ico:'💨',n:'Cardio Machine'},bulwark:{c:'#d0d0e0',ico:'🛡️',n:'Heavyweight'},volatile:{c:'#ff8a3a',ico:'💥',n:'Hothead'}")
rep("const AN={swift:'💨 Swift',bulwark:'🛡️ Bulwark',volatile:'💥 Volatile'};","const AN={swift:'💨 Cardio Machine',bulwark:'🛡️ Heavyweight',volatile:'💥 Hothead'};")
rep("d:'Defeat every elite in all 3 flavors (Swift, Bulwark, Volatile)'","d:'Defeat every elite in all 3 flavors (Cardio Machine, Heavyweight, Hothead)'")
rep("💨 Swift ones are fast, 🛡️ Bulwark ones are tanky, 💥 Volatile ones explode when beaten.","💨 Cardio Machines are fast, 🛡️ Heavyweights are extra tough, 💥 Hotheads blow up when beaten — step away!")
for _o,_n in [("n:'Holy Bulwark',ico:'🛡️'","n:'Wrestling Room',ico:'🤼'"),("n:'Arcane Volley',ico:'🏹'","n:'Jacket Wrestlers',ico:'🥋'"),("n:'Deadly Duo',ico:'🗡️'","n:'Gi Specialists',ico:'🥋'"),("n:'Mana Well',ico:'💧'","n:'Red Corner',ico:'📋'"),("n:'Flank',ico:'⚔️'","n:'Wrestle-Jitsu',ico:'🤼'"),("n:'Choir',ico:'🎶'","n:'Strength & Conditioning',ico:'🏋️'"),("n:'Wandering Band',ico:'🎻'","n:'No-Gi Athletes',ico:'🏃'"),("n:'Dark Pact',ico:'🔮'","n:'Sambo Academy',ico:'🏫'"),("n:'Dread Guard',ico:'⚰️'","n:'Takedown Academy',ico:'🏫'")]:
    rep(_o,_n)

# ---------- 22. Wording pass: heroes->grapplers, monsters->rivals, gold->coins, Tower->Circuit, ⚜️->🎖️, party->crew ----------
rep("Monsters with a coloured glow have a zone power: skeletons that rise again, toxic slimes, fire bats that explode, frost brutes that slow you, and void creatures", "Rivals with a coloured glow have a gym power: some get back up after you tap them, some leave sweaty puddles, some burst like a pre-workout overdose, some slow you down, and some blink around")
s=s.replace("☠ CURSED","⚠️ RISKY").replace("'Cursed bargain'","'Risky bargain'").replace("Take a cursed upgrade","Take a risky upgrade").replace("Take 3 cursed upgrades in one run","Take 3 risky upgrades in one run")
s=s.replace("e.g. my kids love the bard!","e.g. my kids love the Athlete!").replace("New: dungeon events","New: gym events").replace("✨ New relic discovered: ","✨ New champion medal: ")
_EN=[(r'\bHEROES\b','GRAPPLERS'),(r'\bheroes\b','grapplers'),(r'\bHeroes\b','Grapplers'),(r'\bhero\b','grappler'),(r'\bHero\b','Grappler'),
     (r'\bmonsters\b','rivals'),(r'\bMonsters\b','Rivals'),(r'\bmonster\b','rival'),(r'\bMonster\b','Rival'),
     (r'\bgold\b','coins'),(r'\bGold Thief\b','Coin Thief'),(r'\bGOLD THIEF\b','COIN THIEF'),(r'\bTower\b','Circuit'),(r'\btower\b','circuit'),(r'\bTOWER\b','CIRCUIT'),
     (r'\bParty Wiped\b','Crew Tapped Out'),(r'\bparty\b','crew'),(r'\bParty\b','Crew'),(r'\bslimes\b','white belts'),('⚜️','🎖️')]
def _prose(t):
    out=[];i=0
    while i<len(t):
        j=t.find('${',i)
        seg=t[i:] if j<0 else t[i:j]
        for a,b in _EN:
            seg=re.sub(r'(?<![\w/:\-.#])'+a+r'(?![\w/:\-])' if a[0]=='\\' else re.escape(a),b,seg)
        out.append(seg)
        if j<0: break
        d=1;k=j+2
        while k<len(t) and d: 
            d+= (t[k]=='{')-(t[k]=='}'); k+=1
        out.append(t[j:k]); i=k
    return ''.join(out)
def _isprose(t):
    if len(t)<6 or ' ' not in t or 'data:image' in t or 'href=' in t and 'heroes/' in t and len(t)<80: return ' ' in t and 'data:image' not in t
    return True
def _fixlits(src):
    def rp(m):
        q=m.group(1); body=m.group(2)
        if not re.search(r'[A-Za-z]{3,} [A-Za-z]{2,}',body) and '⚜️' not in body: return m.group(0)
        if re.match(r'^[\w$.\[\]()]+$',body): return m.group(0)
        return q+_prose(body)+q
    return re.sub(r"(')((?:[^'\\\n]|\\.){2,600})'|(\")((?:[^\"\\\n]|\\.){2,600})\"|(`)([^`]{2,4000})`",lambda m: rp(type('M',(),{'group':lambda self,n,_m=m:( _m.group(1) or _m.group(3) or _m.group(5)) if n==1 else ((_m.group(2) if _m.group(1) else _m.group(4) if _m.group(3) else _m.group(6)) if n==2 else _m.group(0))})()),src)
_i=s.find('<script>',s.find('</style>'))
s=s[:_i]+_fixlits(s[_i:])
EN_FIX=_prose
s=s.replace("+120 gold","+120 coins").replace("<b>🪙 Gold</b> &mdash; picked up from coins","<b>🪙 Coins</b> &mdash; picked up").replace("Gold resets each run.","Coins reset each run.").replace("<b>🏦 Banked coins</b>","<b>🏦 Mat fees</b>")

# ---------- 23. Signature tricks for the 16 new rivals ----------
rep("function updateEnemies(dt){\n  const P=G.party, E=G.enemies;\n  for(const e of E){\n    if(e.dead) continue;",
    "function updateEnemies(dt){\n  const P=G.party, E=G.enemies;\n  for(const e of E){\n    if(e.dead) continue;\n    if(e.mut&&OSST[e.mut]){ try{ OSST[e.mut](e,dt); }catch(_){} }")
rep("function hurtHero(h,d,quiet,src){","function hurtHero(h,d,quiet,src){ if(G&&G.scoutT>G.t) d*=1.2;")
rep("function hurtEnemy(e,d,crit){\n  if(e.dead) return;","function hurtEnemy(e,d,crit){\n  if(e.dead) return; if(e.mut==='sprawl') d*=.7; if(e.mut==='bouncer'){ d*=.6; if(Math.random()<.15){ const n=ossNear(e); if(n&&n.d<1.6) hurtHero(n.h,Math.ceil(d*.25),false,e); } } if(e.mut==='smokebomb'&&e.smokeT>G.t) d*=.2;")
rep("if(e.type==='splitter'){for(let q=0;q<2;q++)","if(e.type==='splitter'){for(let q=0;q<(e.mut==='triplets'?3:2);q++)")
rep("function updateEnemies(dt){","""function ossNear(e){ let best=null; for(const h of G.party){ const p=hpos(h),d=dist(p.x,p.y,e.x,e.y); if(!best||d<best.d) best={h,d,p}; } return best; }
function ossSay(e,t,c){ text(e.x,e.y-.75,t,c||'#ffd86b'); }
function ossHit(e,mult){ const n=ossNear(e); if(n&&n.d<1.5){ hurtHero(n.h,Math.ceil((e.def.dmg||8)*e.dmgS*mult),false,e); return n; } return null; }
const OSST={
 kimura:(e,dt)=>{ e.tk=(e.tk==null?2:e.tk)-dt; if(e.tk<=0){ e.tk=3; if(ossHit(e,1.6)) ossSay(e,PTL()?'Kimura!':'Kimura!','#ff9a6a'); } },
 bolo:(e,dt)=>{ e.tk=(e.tk==null?3:e.tk)-dt; if(e.tk<=0){ e.tk=3.5; const hd=hpos(G.party[0]); burst(e.x,e.y,'#8a7aff',8,2.5,true); e.x=clamp(2*hd.x-e.x,.8,COLS-.8); e.y=clamp(2*hd.y-e.y,.8,ROWS-.8); burst(e.x,e.y,'#8a7aff',8,2.5,true); ossSay(e,'Berimbolo!','#b9aaff'); } },
 guardcarl:(e,dt)=>{ e.tk=(e.tk==null?2:e.tk)-dt; if(e.tk<=0){ e.tk=2.5; if(ossHit(e,.8)){ e.hp=Math.min(e.max,e.hp+e.max*.05); ossSay(e,PTL()?'Guarda fechada!':'Closed guard!','#7fd0ff'); } } },
 scout:(e,dt)=>{ e.tk=(e.tk==null?4:e.tk)-dt; if(e.tk<=0){ e.tk=6; G.scoutT=G.t+3; const hd=hpos(G.party[0]); ring(hd.x,hd.y,1.4,'#ff5a5a'); ossSay(e,PTL()?'Estudado!':'Scouted!','#ff7a7a'); G.banner={text:PTL()?'📹 VOCÊ FOI ESTUDADO':'📹 YOU GOT SCOUTED',sub:PTL()?'+20% de dano recebido por 3s':'Take +20% damage for 3s',t:1.4,col:'#ff7a7a'}; } },
 cradle:(e,dt)=>{ e.tk=(e.tk==null?2:e.tk)-dt; if(e.tk<=0){ e.tk=3.2; if(ossHit(e,2)){ G.shake=Math.max(G.shake,.5); ossSay(e,'Cradle!','#ff9a6a'); } } },
 heelhook:(e,dt)=>{ e.tk=(e.tk==null?3:e.tk)-dt; if(e.tk<=0){ e.tk=4; const t=G.party[G.party.length-1]; if(t){ const p=hpos(t); if(dist(p.x,p.y,e.x,e.y)<2.2){ hurtHero(t,Math.ceil((e.def.dmg||10)*e.dmgS*1.7),false,e); ossSay(e,'Heel hook!','#ff6a6a'); } } } },
 hypeman:(e,dt)=>{ e.tk=(e.tk==null?3:e.tk)-dt; if(e.tk<=0){ e.tk=4.5; ring(e.x,e.y,3,'#ffd84a'); for(const o of G.enemies) if(!o.dead&&o!==e&&o.type!=='boss'&&dist(o.x,o.y,e.x,e.y)<3&&!(o.hyped>2)){ o.hyped=(o.hyped||0)+1; o.dmgS*=1.08; } ossSay(e,'HYPE!','#ffd84a'); } },
 chokeghost:(e,dt)=>{ e.tk=(e.tk==null?2:e.tk)-dt; if(e.tk<=0){ e.tk=2.4; if(ossHit(e,1)){ e.hp=Math.min(e.max,e.hp+e.max*.06); ossSay(e,PTL()?'Gola!':'Collar choke!','#bfe8ff'); } } },
 oldtimer:(e,dt)=>{ e.hp=Math.min(e.max,e.hp+e.max*.02*dt); },
 wristlock:(e,dt)=>{ e.tk=(e.tk==null?3:e.tk)-dt; if(e.tk<=0){ e.tk=3.4; const hd=hpos(G.party[0]),a=Math.atan2(hd.y-e.y,hd.x-e.x); for(const o of [-.25,0,.25]) G.proj.push({x:e.x,y:e.y,vx:Math.cos(a+o)*5,vy:Math.sin(a+o)*5,life:3,team:'e',dmg:6*e.dmgS,col:'#c08aff',kind:'fire',a:a+o,spin:0}); ossSay(e,PTL()?'Chave de pulso!':'Wristlock!','#c08aff'); } },
 stalker:(e,dt)=>{ e.tk=(e.tk==null?3:e.tk)-dt; if(e.tk<=0){ e.tk=4; const t=G.party[G.party.length-1]; if(t){ const p=hpos(t); burst(e.x,e.y,'#7aff9a',8,2.5,true); e.x=clamp(p.x+rand(-.8,.8),.8,COLS-.8); e.y=clamp(p.y+rand(-.8,.8),.8,ROWS-.8); ossSay(e,PTL()?'Pegou as costas!':'Took the back!','#7aff9a'); } } },
 locksmith:(e,dt)=>{ e.tk=(e.tk==null?5:e.tk)-dt; if(e.tk<=0){ e.tk=6; e.hp=Math.min(e.max,e.hp+e.max*.15); ring(e.x,e.y,1.2,'#ffd84a'); ossSay(e,'🗝️','#ffd84a'); } },
 smokebomb:(e,dt)=>{ e.tk=(e.tk==null?4:e.tk)-dt; if(e.tk<=0){ e.tk=5.5; e.smokeT=G.t+1.5; burst(e.x,e.y,'#b07aff',18,3,true); ossSay(e,'💨','#b07aff'); } }
};
function updateEnemies(dt){""")

# ---------- 24. One Oss art style: lock looks to the Oss art, hide the old style pickers ----------
rep("function applyOssArt(){ const A=window.OSS_ART; if(!A) return;","function applyOssArt(){ try{ SET.hs='chibi'; SET.ms='chibi'; SET.ps='chibi'; }catch(_){} const A=window.OSS_ART; if(!A) return;")
rep("#story .sty-title{","#overlay .srow2:has(#setHS),#overlay .srow2:has(#setMS),#overlay .srow2:has(#setPS){display:none!important} #story .sty-title{")

# ---------- 25. Gym sound: whistle, mat slaps, body slams, buzzer, and a workout beat for every gym ----------
rep("function sfx(n){\n  if(muted||!AC) return;\n  const now=AC.currentTime; if(lastS[n]&&now-lastS[n]<.045) return; lastS[n]=now;",
    "function sfx(n){\n  if(muted||!AC) return;\n  const now=AC.currentTime; if(lastS[n]&&now-lastS[n]<.045) return; lastS[n]=now;\n  if(OSSFX[n]){ try{ OSSFX[n](now,SFXG||AC.destination); }catch(e){} return; }")
rep("function fanfare(big){", r"""let _NB=null; function noiseBuf(){ if(_NB) return _NB; const n=AC.sampleRate*1, b=AC.createBuffer(1,n,AC.sampleRate), d=b.getChannelData(0); for(let i=0;i<n;i++) d[i]=Math.random()*2-1; return _NB=b; }
function nz(t,dur,type,freq,vol,out,q){ const s=AC.createBufferSource(); s.buffer=noiseBuf(); const f=AC.createBiquadFilter(); f.type=type; f.frequency.value=freq; if(q) f.Q.value=q; const g=AC.createGain(); g.gain.setValueAtTime(vol,t); g.gain.exponentialRampToValueAtTime(.0008,t+dur); s.connect(f); f.connect(g); g.connect(out); s.start(t); s.stop(t+dur+.02); return f; }
function tone(t,f0,f1,dur,type,vol,out){ const o=AC.createOscillator(),g=AC.createGain(); o.type=type; o.frequency.setValueAtTime(f0,t); if(f1) o.frequency.exponentialRampToValueAtTime(f1,t+dur); g.gain.setValueAtTime(vol,t); g.gain.exponentialRampToValueAtTime(.0008,t+dur); o.connect(g); g.connect(out); o.start(t); o.stop(t+dur+.02); return o; }
const OSSFX={
 hit:(t,o)=>{ nz(t,.06,'lowpass',900,.10,o); tone(t,140,60,.06,'sine',.06,o); },
 swing:(t,o)=>{ const f=nz(t,.12,'bandpass',600,.05,o,1.2); f.frequency.exponentialRampToValueAtTime(2200,t+.12); },
 bump:(t,o)=>{ tone(t,95,50,.16,'sine',.12,o); nz(t,.1,'lowpass',400,.08,o); },
 boom:(t,o)=>{ tone(t,120,38,.28,'sine',.18,o); nz(t,.22,'lowpass',700,.12,o); },
 die:(t,o)=>{ tone(t,118,0,.42,'square',.035,o); tone(t,123,0,.42,'square',.03,o); },
 wave:(t,o)=>{ const w=tone(t,2650,0,.32,'sine',.05,o); const l=AC.createOscillator(),lg=AC.createGain(); l.frequency.value=28; lg.gain.value=90; l.connect(lg); lg.connect(w.frequency); l.start(t); l.stop(t+.34); tone(t+.36,2650,2500,.14,'sine',.04,o); },
 shoot:(t,o)=>{ nz(t,.05,'highpass',2500,.04,o); },
 coin:(t,o)=>{ tone(t,1320,1980,.08,'sine',.045,o); tone(t+.06,1980,0,.1,'sine',.03,o); },
 good:(t,o)=>{ for(let i=0;i<5;i++) nz(t+i*.045+Math.random()*.02,.05,'bandpass',1400+Math.random()*900,.05,o,2); tone(t,660,990,.25,'triangle',.04,o); },
 pick:(t,o)=>{ tone(t,520,940,.22,'triangle',.06,o); nz(t,.05,'highpass',3000,.02,o); },
 heal:(t,o)=>{ tone(t,620,930,.15,'sine',.04,o); }
};
function fanfare(big){""")
s=re.sub(r"const ZMUS=\[.*?\n\];", """const ZMUS=[
 {bpm:92, lead:[0,2,4,2,0,4,2,1], leadT:'square',bass:[0,0,3,2], bassT:'sawtooth', perc:'gym', stac:1},   // Garage Gym: lo-fi boom bap
 {bpm:104,lead:[4,0,5,0,4,2,0,2], leadT:'triangle',bass:[0,2,0,3], bassT:'sawtooth', perc:'gym', stac:1},  // Beach shack: bouncy
 {bpm:118,lead:[0,0,2,0,3,2,0,4], leadT:'square',bass:[0,0,0,3], bassT:'sawtooth', perc:'gym', eighth:1}, // Sambo hall: march
 {bpm:122,lead:[5,7,4,7,5,4,2,4], leadT:'square',bass:[0,3,2,1], bassT:'sawtooth', perc:'gym', stac:1},   // Wrestling room: hype
 {bpm:96, lead:[0,1,0,4,3,1,6,5], leadT:'triangle',bass:[0,0,1,0], bassT:'sawtooth', perc:'gym'},         // Butterfly club: smooth
 {bpm:110,lead:[2,4,5,4,2,1,0,1], leadT:'square',bass:[0,3,0,4], bassT:'sawtooth', perc:'gym', stac:1},   // Rio academy: groove
 {bpm:100,lead:[5,9,7,10,9,7,5,4], leadT:'triangle',bass:[0,4,3,2], bassT:'sawtooth', perc:'gym'},        // Little Italy: swing
 {bpm:126,lead:[0,2,0,4,0,2,5,4], leadT:'square',bass:[0,0,3,3], bassT:'sawtooth', perc:'gym', stac:1, eighth:1}, // Blue basement: training montage
 {bpm:132,lead:[0,1,0,3,0,1,4,3], leadT:'sawtooth',bass:[0,0,0,1], bassT:'sawtooth', perc:'gym', detune:1, eighth:1} // Cage / finals: heavy
];""", s, count=1, flags=re.S)
rep("    if(Z.perc==='drum'&&i%4===0) mnote(root*.5,t,.18,'triangle',.06);",
    "    if(Z.perc==='drum'&&i%4===0) mnote(root*.5,t,.18,'triangle',.06);\n    if(Z.perc==='gym'){ const M=MUSG||AC.destination; const k=i%16; if(k===0||k===7||k===10) { tone(t,110,42,.22,'sine',.09,M); } if(k===4||k===12){ nz(t,.14,'bandpass',1800,.06,M,.8); nz(t,.05,'highpass',5000,.025,M); } if(i%2===0) nz(t,.03,'highpass',8000,(k%4===2?.02:.012),M); }")
rep('window.__dc={camp:','window.__dc={tagTeam:(e,st)=>tagTeam(e,st),beltLv:()=>beltLv(),legacyHall:b=>legacyHall(b),towerWin0:()=>towerWin0(),get MUT(){return MUT},startWave:()=>startWave(),camp:')
open(DST + '/story/index_tpl.html', 'w').write(s)
print('template patched', len(s)//1024, 'KB')
