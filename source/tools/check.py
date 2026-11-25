# Loads the built game fresh, checks for page errors, and takes phone screenshots.
import sys, json
from playwright.sync_api import sync_playwright
GAME = sys.argv[1]; OUT = sys.argv[2]
errs = []
def shot(pg, name): pg.screenshot(path=f'{OUT}/{name}.png')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    pg.on('console', lambda m: m.type == 'error' and errs.append('console: ' + m.text[:200]))
    pg.goto('file://' + GAME); pg.wait_for_timeout(2500)
    shot(pg, '00_landing')
    pg.evaluate("(()=>{const b=document.getElementById('lSkip'); if(b) b.click();})()"); pg.wait_for_timeout(1200)
    shot(pg, '01_menu')
    keys = pg.evaluate("Object.keys(localStorage)")
    print('localStorage keys:', keys)
    meta = pg.evaluate("(()=>{const M=window.__dc.META;return {unlocked:M.unlocked,party:M.party}})()")
    print('fresh meta:', meta)
    # Start a run: the prologue should play
    pg.evaluate("window.__dc.newGame(false,false,false)"); pg.wait_for_timeout(1500)
    has_story = pg.evaluate("!!document.getElementById('story')")
    print('prologue playing:', has_story)
    for i in range(4):
        shot(pg, f'02_story_{i+1}')
        pg.evaluate("(()=>{const h=document.getElementById('story'); if(h) h.dispatchEvent(new PointerEvent('pointerup',{bubbles:true}));})()")
        pg.wait_for_timeout(900)
    shot(pg, '03_titlecard')
    pg.evaluate("(()=>{const t=document.querySelector('.sty-title'); if(t) t.dispatchEvent(new PointerEvent('pointerup',{bubbles:true}));})()")
    pg.wait_for_timeout(1200)
    # Banner picks only ever offer unlocked classes
    picks = pg.evaluate("(()=>{const s={};for(let i=0;i<600;i++){const k=window.__dc.pickFlagKind();s[k]=(s[k]||0)+1;}return s})()")
    print('banner picks (600):', picks)
    pg.evaluate("(()=>{const o=document.getElementById('overlay'); o&&o.classList.add('hide'); window.__dc.G.paused=false;})()")
    pg.wait_for_timeout(2500)
    shot(pg, '04_gameplay')
    # Academy with some mat fees to show the locked classes
    pg.evaluate("(()=>{const M=window.__dc.META; M.bank=450; window.__dc.G.state='menu'; window.__dc.camp();})()"); pg.wait_for_timeout(600)
    shot(pg, '05_academy')
    # Buy Sambo -> celebration card
    pg.evaluate("document.querySelector('[data-hero=mage]').click()"); pg.wait_for_timeout(600)
    shot(pg, '06_unlock_card')
    pg.evaluate("document.getElementById('ulGo').click()"); pg.wait_for_timeout(500)
    print('after buy:', pg.evaluate("window.__dc.META.unlocked"), 'bank', pg.evaluate("window.__dc.META.bank"))
    # Boss of region 2 (floor 10) frees the Coach
    pg.evaluate("(()=>{const D=window.__dc; D.hideOverlay(); D.newGame(false,false,false); })()"); pg.wait_for_timeout(800)
    pg.evaluate("(()=>{const D=window.__dc,G=D.G; const s=document.getElementById('story'); if(s) s.remove(); G.wave=10; G.inIntro=false; G.paused=false; window.__dc.hideOverlay(); const e=D.spawnEnemy('boss'); D.killEnemy(e||G.enemies.find(x=>x.type==='boss')); })()")
    pg.wait_for_timeout(2500)
    shot(pg, '07_boss_unlock')
    print('after region-2 boss:', pg.evaluate("window.__dc.META.unlocked"))
    # Portuguese academy
    pg.evaluate("(()=>{window.__dc.SET.lang='pt'; window.__dc.hideOverlay(); window.__dc.G.state='menu'; window.__dc.camp();})()"); pg.wait_for_timeout(600)
    shot(pg, '08_academy_pt')
    b.close()
print('ERRORS:', errs if errs else 'none')
