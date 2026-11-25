import sys
from playwright.sync_api import sync_playwright
G=sys.argv[1]; O=sys.argv[2]; errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True).new_page()
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+G); pg.wait_for_timeout(2500); pg.screenshot(path=O+'/a0_landing.png')
    pg.evaluate("document.getElementById('lSkip')&&document.getElementById('lSkip').click()"); pg.wait_for_timeout(800); pg.screenshot(path=O+'/a1_menu.png')
    pg.evaluate("window.__dc.newGame(false,false,false)"); pg.wait_for_timeout(1500); pg.screenshot(path=O+'/a2_story.png')
    pg.evaluate("(()=>{const s=document.getElementById('story'); if(s) s.remove(); const D=window.__dc; D.hideOverlay(); D.G.inIntro=false; D.G.paused=false; D.G.introQ=[];})()")
    pg.wait_for_timeout(300)
    pg.evaluate("(()=>{const D=window.__dc,G=D.G; for(let i=0;i<4;i++) D.spawnEnemy('slime'); for(let i=0;i<3;i++) D.spawnEnemy('bat'); G.wave=5; D.spawnEnemy('boss'); D.hideOverlay(); G.paused=false; G.inIntro=false;})()")
    pg.wait_for_timeout(1800); pg.screenshot(path=O+'/a3_play.png')
    print(pg.evaluate("(()=>{const D=window.__dc; return {wrestlerPort:(D.PORT['hero:knight']||'').slice(0,40), bossPort:(D.PORT['enemy:boss0']||'').slice(0,30)}})()"))
    pg.evaluate("(()=>{window.__dc.META.bank=500; window.__dc.G.state='menu'; window.__dc.camp();})()"); pg.wait_for_timeout(700); pg.screenshot(path=O+'/a4_academy.png')
    b.close()
print('ERRORS', errs or 'none')
