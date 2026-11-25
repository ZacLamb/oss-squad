const {chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:900,height:456},deviceScaleFactor:1.5});
 const pg=await ctx.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
 const d=new Date(),tk=d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
 await pg.addInitScript(`localStorage.setItem('ossSquad.meta',JSON.stringify({tut:1,qDay:'${tk}',story:['prologue','p0','intro'],seen:${JSON.stringify(['slime','bat','skel','spider','brute','ghost','golem','wizard','bomber','charger','shaman','necro','splitter','voidling','boss'].map(k=>'enemy:'+k).concat(['knight','archer','mage','cleric','rogue','bard','necro'].map(k=>'hero:'+k)))}}));localStorage.setItem('ossSquad.settings',JSON.stringify({music:0,sfx:0,story:0,dn:'once',fx:'calm'}))`);
 await pg.clock.install();
 await pg.goto(process.env.GAME_URL||'http://localhost:8080/',{waitUntil:'load'}); await pg.clock.runFor(4000); await pg.waitForTimeout(4000); await pg.clock.runFor(2000);
 await pg.addStyleTag({content:'#qCard,#dtoast{display:none!important}'}); await pg.addScriptTag({path:'bot.js'}); await pg.addScriptTag({path:'drive.js'});
 await pg.evaluate(()=>{window.__dc.newGame();});
 for(let i=0;i<6;i++){ await pg.clock.runFor(800); await pg.evaluate(()=>{const s=[...document.querySelectorAll('button')].find(b=>/Skip/.test(b.textContent)); if(s) s.click(); const o=document.getElementById('overlay'); if(o) o.classList.add('hide');}); }
 const START=+(process.env.START||3);
 // fast-forward to floor START
 for(let i=0;i<400;i++){ const w=await pg.evaluate(()=>{window.__bot(300,1/30);return window.__dc.G.wave}); if(w>=START) break; }
 fs.mkdirSync('fr',{recursive:true}); let n=0; const MAX=+(process.env.FRAMES||600);
 for(let i=0;i<MAX*6&&n<MAX;i++){
   const st=await pg.evaluate(()=>{ const sk=document.getElementById('story'); if(sk){ const b=[...sk.querySelectorAll('button')].find(b=>/Skip/.test(b.textContent)); if(b) b.click(); return 'skip'; } const r=window.__drive(); const G=window.__dc.G; const ov=document.getElementById('overlay'); return r==='play'&&!G.paused&&(!ov||ov.classList.contains('hide'))?'play':(G.state==='over'?'over':'skip');});
   if(st==='over') break;
   await pg.clock.runFor(16.67); await pg.clock.runFor(16.67);
   if(st==='play'){ await pg.screenshot({path:`fr/${String(n).padStart(5,'0')}.jpg`,type:'jpeg',quality:92}); n++; }
 }
 console.log('frames',n,'errs',errs.slice(0,3)); await b.close();
})();
