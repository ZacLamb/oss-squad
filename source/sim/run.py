import sys,json,time
from playwright.sync_api import sync_playwright
import os as _os
ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
df=sys.argv[1]; seed=sys.argv[2] if len(sys.argv)>2 else '1'
m={'tut':1,'seen':['enemy:'+k for k in ['slime','bat','skel','spider','brute','ghost','golem','wizard','bomber','charger','shaman','necro','splitter','voidling','boss']]+['hero:'+k for k in ['knight','archer','mage','cleric','rogue','bard','necro']]}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':780});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("localStorage.setItem('ossSquad.meta',%s);localStorage.setItem('ossSquad.settings',%s)"%(json.dumps(json.dumps(m)),json.dumps(json.dumps({'df':df,'fx':'min','music':0,'sfx':0,'dn':'once'}))))
    pg.goto('file://'+ROOT+'/game2/index.html');pg.wait_for_timeout(500)
    pg.add_script_tag(path=ROOT+'/sim/bot.js')
    pg.evaluate("window.__dc.newGame();document.getElementById('overlay').classList.add('hide')")
    t0=time.time()
    while True:
        r=pg.evaluate("(()=>{const l=window.__bot(3000,1/30);return {dead:l.dead,won:l.won,n:l.floors.length,w:window.__dc.G.wave}})()")
        if r['dead'] or r['won'] or time.time()-t0>1500: break
    log=pg.evaluate("(()=>{const l=window.__log;if(l.cur)l.floors.push(l.cur);return {floors:l.floors,dead:l.dead,won:l.won,party:window.__dc.G.party.map(h=>h.kind+'*'+(h.star||1)+' L'+h.lvl)}})()")
    log['errs']=errs[:5];log['real']=round(time.time()-t0)
    json.dump(log,open(ROOT+f'/sim/out_{df}_{seed}.json','w'))
    print(df,'dead' if log['dead'] else 'won' if log['won'] else 'timeout',len(log['floors']),log['real'],'s',errs[:2])
    b.close()
