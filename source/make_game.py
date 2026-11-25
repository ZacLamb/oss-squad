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
for _a,_b in [('Gold resets each run','Coins reset each run'),('Gold goes straight','Coins go straight'),('Gold rains from above','Coins rain from above'),('Gold Thief','Coin Thief'),('spare gear for gold.','spare gear for coins.'),('__SITE__og.jpg','https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/309f3a26-da9a-43ce-b6e3-1b8b6a3fb156.jpg'),('a free hero adventure game','a free jiu-jitsu adventure game'),('🏰 Camp','🥋 Camp'),('🏰 Acampamento','🥋 Acampamento'),('A Circuito','O Circuito'),('🏰','🏆'),('A free hero party adventure for phones, tablets and computers: steer your line of heroes, recruit allies, pick upgrades and beat 10 bosses across 50 floors to bring back the light.','A free jiu-jitsu party adventure for phones, tablets and computers: steer your crew of grapplers, recruit teammates, pick upgrades and beat 10 champions across 50 rounds to break the Master Spell.'),('EVERLIGHT RESTORED!','MASTER SPELL BROKEN!'),('LUZ ETERNA RESTAURADA!','FEITIÇO DO MESTRE QUEBRADO!'),('Lead your party of heroes through 50 floors and 10 bosses to bring back the light. Free, no ads, plays on phone or computer.','Lead your jiu-jitsu crew through 50 rounds and 10 champions to break the Master Spell. Free, no ads, plays on phone or computer.')]:
    h=h.replace(_a,_b)
open(ROOT+'/game2/index.html','w').write(h)
CDN='https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/'
json.dump({k:CDN+v+'.'+k.split('.')[1] for k,v in m.items()},open(ROOT+'/launch/story-manifest.json','w'),indent=0)
print('built game', len(h)//1024,'KB')
