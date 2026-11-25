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
open(ROOT+'/game2/index.html','w').write(h)
CDN='https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/'
json.dump({k:CDN+v+'.'+k.split('.')[1] for k,v in m.items()},open(ROOT+'/launch/story-manifest.json','w'),indent=0)
print('built game', len(h)//1024,'KB')
