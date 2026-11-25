import json,sys
import os as _os
ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
h=open(ROOT+'/story/index_tpl.html').read()
m=json.load(open(ROOT+'/story/map.json'))
times=json.load(open(ROOT+'/story/times_en.json'))
pt=json.load(open(ROOT+'/story/pt.json'))
try: spt=json.load(open(ROOT+'/story/story_pt.json'))
except Exception: spt={}
try: bvo=json.load(open(ROOT+'/story/boss_vo.json'))
except Exception: bvo={}
s=json.load(open(ROOT+'/story/story.json'))
STO=[{'id':c['id'],'at':c['at'],'title':c['title'],'tp':c.get('title_pt',c['title']),'frames':[{kk:f[kk] for kk in ('t','pt','fx','fxAt','fxAtPt','e') if kk in f} for f in c['frames']]} for c in s['chapters']]
import re as _re
_VER=_re.search(r"oss-squad-v([0-9.]+)",open(ROOT+'/launch/sw.js').read()).group(1)
for k,v in [('__VER__',_VER),('__STORY__',STO),('__STORY_MAP__',m),('__STORY_AUD__',times),('__STORY_PT__',spt),('__BOSS_VO__',bvo),('__PT_JSON__',pt)]:
    assert k in h, k
    h=h.replace(k,json.dumps(v,ensure_ascii=False,separators=(',',':')))
for _a,_b in [('Gold resets each run','Coins reset each run'),('Gold goes straight','Coins go straight'),('Gold rains from above','Coins rain from above'),('Gold Thief','Coin Thief'),('spare gear for gold.','spare gear for coins.'),('__SITE__og.jpg','https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/309f3a26-da9a-43ce-b6e3-1b8b6a3fb156.jpg'),('a free hero adventure game','a free jiu-jitsu adventure game'),('🏰 Camp','🥋 Camp'),('Grab banners to recruit, pick upgrades and a path between levels.','Grab recruit flags, pick upgrades and a path between rounds.'),('🪜 CLIMB THE STAIRS · FLOOR ','🪜 NEXT ROUND · ROUND '),('☠ BOSS FLOOR ','☠ CHAMPION ROUND '),("'FLOOR '","'ROUND '"),("name:'Elite monsters'","name:'Elite rivals'"),('</b> monsters.</p>','</b> rivals.</p>'),('"monsters.":"rivais."','"rivals.":"rivais."'),("NOVO NESTE ANDAR","NOVO NESTE ROUND"),("NEW ON THIS FLOOR","NEW THIS ROUND"),('Meet the heroes','Meet the crew'),('camp upgrades, heroes and Codex','camp upgrades, grapplers and Codex'),('Lead your party of heroes through 50 floors and 10 bosses.','Lead your jiu-jitsu crew through 50 rounds and 10 champions.'),('"icons/icon-192.png"','"'+'https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/04e8362a-99da-41d3-804b-62b663677540.png'+'"'),('🏰 Acampamento','🥋 Acampamento'),('A Circuito','O Circuito'),('🏰','🏆'),('A free hero party adventure for phones, tablets and computers: steer your line of heroes, recruit allies, pick upgrades and beat 10 bosses across 50 floors to bring back the light.','A free jiu-jitsu party adventure for phones, tablets and computers: steer your crew of grapplers, recruit teammates, pick upgrades and beat 10 champions across 50 rounds to break the Master Spell.'),('EVERLIGHT RESTORED!','MASTER SPELL BROKEN!'),('LUZ ETERNA RESTAURADA!','FEITIÇO DO MESTRE QUEBRADO!'),('Lead your party of heroes through 50 floors and 10 bosses to bring back the light. Free, no ads, plays on phone or computer.','Lead your jiu-jitsu crew through 50 rounds and 10 champions to break the Master Spell. Free, no ads, plays on phone or computer.')]:
    h=h.replace(_a,_b)

# ---- final wording pass over user-visible string literals (applies to English and the PT keys alike) ----
import re as _re2
_W=[(r'\bmonsters\b','rivals'),(r'\bMonsters\b','Rivals'),(r'\bmonster\b','rival'),(r'\bMonster\b','Rival'),
    (r'\bBOSS FLOOR\b','CHAMPION ROUND'),(r'\bFLOORS\b','ROUNDS'),(r'\bFLOOR\b','ROUND'),(r'\bFloors\b','Rounds'),(r'\bFloor\b','Round'),(r'\bfloors\b','rounds'),(r'\bfloor\b','round'),
    (r'CLIMB THE STAIRS','NEXT ROUND'),(r'\bheroes\b','grapplers'),(r'\bHeroes\b','Grapplers'),(r'\bHero\b','Grappler'),(r'\bhero\b','grappler'),
    (r'\bskeletons\b','tape tossers'),(r'\bskeleton\b','tape tosser'),(r'\bdungeons?\b','gym'),(r'YOU FOUND A BANNER','YOU FOUND A RECRUIT FLAG'),
    (r'ANDAR DO CHEFE','ROUND DO CAMPEÃO'),(r'\bANDARES\b','ROUNDS'),(r'\bANDAR\b','ROUND'),(r'\bandares\b','rounds'),(r'\bandar\b','round'),(r'\bAndar\b','Round'),(r'SUBA A ESCADA','PRÓXIMO ROUND'),(r'ESTANDARTE','BANDEIRA'),(r'\besqueletos\b','arremessadores de fita'),(r'\bmasmorras?\b','academia')]
def _vis(body):
    if ' ' not in body or 'data:' in body or 'http' in body or any(x in body for x in ('==','&&','||','=>','G.','();')): return body
    out=[];i=0
    while i<len(body):
        j=body.find('${',i); seg=body[i:] if j<0 else body[i:j]
        for a,b in _W: seg=_re2.sub(r'(?<![\w/:\-.#="])'+a+r'(?![\w/:\-="])',b,seg)
        out.append(seg)
        if j<0: break
        d=1;k=j+2
        while k<len(body) and d: d+=(body[k]=='{')-(body[k]=='}'); k+=1
        out.append(body[j:k]); i=k
    return ''.join(out)
def _lits(src):
    return _re2.sub(r"'((?:[^'\\\n]|\\.){1,600})'|\"((?:[^\"\\\n]|\\.){1,600})\"|`([^`]{1,4000})`",
        lambda m: ("'"+_vis(m.group(1))+"'") if m.group(1) is not None else ('"'+_vis(m.group(2))+'"') if m.group(2) is not None else ('`'+_vis(m.group(3))+'`'), src)
_sc=_re2.split(r'(<script>[\s\S]*?</script>)',h)
h=''.join(_lits(x) if x.startswith('<script>') else x for x in _sc)
for _a,_b in [('from the round','from the mat'),('on the round and','on the mat and'),('across the round','across the mat'),('in the round tear','in the mat tear'),('the round plates','the mat plates'),('Cracks in the round','Cracks in the mat'),('the training round','the training mat')]: h=h.replace(_a,_b)
open(ROOT+'/game2/index.html','w').write(h)
CDN='https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/'
json.dump({k:CDN+v+'.'+k.split('.')[1] for k,v in m.items()},open(ROOT+'/launch/story-manifest.json','w'),indent=0)
print('built game', len(h)//1024,'KB')
