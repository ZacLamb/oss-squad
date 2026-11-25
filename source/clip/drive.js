window.__drive=function(){ const frames=1,dt=0;
  const d=window.__dc; const [C,Rw]=d.dims; let G=d.G;
  const log=window.__log=window.__log||{floors:[],cur:null,bumps:0,dead:false,won:false};
  for(let f=0;f<frames;f++){
    G=d.G; if(!G) return log;
    if(G.state==='over'){log.dead=true;return log;}
    if(G.phase==='won'){log.won=true;return log;}
    const ov=document.getElementById('overlay');
    if(G.inIntro&&document.getElementById('fGold')){ const fj=document.getElementById('fJoin'),up=[...ov.querySelectorAll('[data-up]')],sw=[...ov.querySelectorAll('[data-sw]')];
        if(fj&&Math.random()<.6) fj.click(); else if(up.length) up[0].click(); else if(fj) fj.click(); else if(sw.length&&Math.random()<.5) sw[sw.length-1].click(); else document.getElementById('fGold').click(); continue; }
    if(G.inIntro){ const sg=document.getElementById('swGold'); if(sg){
        // swap the weakest unstarred hero for the newcomer half the time, else gold
        const btn=[...ov.querySelectorAll('[data-sw]')]; if(btn.length&&Math.random()<.5){btn[btn.length-1].click();} else sg.click();
      } else d.nextIntro(); continue; }
    if(G.inParty){d.closeParty();continue;}
    if(G.choosing){
      if(G.phase==='upgrade'){
        // spend points like a sensible kid: unlock skills first, then might/vit
        let guard=0;
        while(G.pts>0&&guard++<40){ const h=G.party.find(h=>!h.skillOn&&G.pts>=3); if(h){d.unlockSkill(h);continue;}
          const t=G.party[Math.floor(Math.random()*G.party.length)]; d.spendPoint(t,Math.random()<.5?'pow':'vit'); }
        d.quickEquip(true);
        const i=G.offers.findIndex(o=>!o.u.curse); d.pickUpgrade(i<0?0:i);
      } else if(G.phase==='route'){ d.pickRoute(0); }
      continue;
    }
    // log floor start
    if(G.phase==='fight'&&(!log.cur||log.cur.w!==G.wave)){
      if(log.cur) log.floors.push(log.cur);
      window.__simlog={};log.cur={dmg:window.__simlog,w:G.wave,t:0,minHp:1,lost:0,size0:G.party.length,stars:G.party.reduce((a,h)=>a+(h.star||1),0),total:G.waveTotal,potions:0,maxed:G.party.length>=6&&G.party.every(h=>(h.star||1)>=3)};
    }
    if(log.cur&&G.phase==='fight'){log.cur.t+=dt; const hp=G.party.reduce((a,h)=>a+Math.max(0,h.hp),0)/G.party.reduce((a,h)=>a+h.max,0); log.cur.minHp=Math.min(log.cur.minHp,hp); log.cur.size=G.party.length; log.cur.combo=G.combo||'';}
    if(G.charge>=100&&G.enemies.some(e=>!e.dead)) d.ultimate();
    steer2(G,C,Rw);
    return 'play';
  }
  return log;
};
function steer2(G,C,Rw){
  const P=G.party,head=P[0]; if(!head) return;
  // cells occupied by body (excluding tail which will move)
  const occ=new Set(G.walls||[]); for(let i=0;i<P.length-1;i++) occ.add(P[i].x+','+P[i].y);
  // targets
  let tg=[];
  if(G.phase==='stairs'&&G.stairs){ const hx=head.x,hy=head.y,lootLeft=G.pickups.filter(k=>(k.type==='chest'||k.type==='banner')&&Math.abs(k.x-hx)+Math.abs(k.y-hy)<6); tg=(lootLeft.length?lootLeft:[G.stairs]).map(k=>[Math.floor(k.x),Math.floor(k.y)]); }
  else {
    for(const k of G.pickups) tg.push([Math.floor(k.x),Math.floor(k.y)]);
    if(!tg.length){ // drift toward enemy centroid but keep distance
      const E=G.enemies.filter(e=>!e.dead); if(E.length){let cx=0,cy=0;for(const e of E){cx+=e.x;cy+=e.y;}cx/=E.length;cy/=E.length;tg.push([Math.floor(cx),Math.floor(cy)]);}
      else tg.push([Math.floor(C/2),Math.floor(Rw/2)]);
    }
  }
  const tset=new Set(tg.map(t=>t[0]+','+t[1]));
  const dirs=[[1,0],[-1,0],[0,1],[0,-1]].filter(([dx,dy])=>!(dx===-G.dir.x&&dy===-G.dir.y));
  // enemy danger map
  const danger=new Set(); if(G.haz)for(const [k,z] of G.haz)if(z.k==='lava'||z.k==='spike')danger.add(k); for(const e of G.enemies) if(!e.dead&&(e.def.dmg>=14||e.type==='boss')) {for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++)danger.add((Math.floor(e.x)+a)+','+(Math.floor(e.y)+b));}
  let best=null,bs=-1e9;
  for(const [dx,dy] of dirs){
    const nx=head.x+dx,ny=head.y+dy; if(nx<0||ny<0||nx>=C||ny>=Rw||occ.has(nx+','+ny)) continue;
    // BFS free space + distance to target
    const seen=new Set([nx+','+ny]),q=[[nx,ny,0]];let reach=0,dist=999;
    while(q.length&&reach<800){const [x,y,dd]=q.shift();reach++; if(dist===999&&tset.has(x+','+y))dist=dd;
      for(const [ax,ay] of [[1,0],[-1,0],[0,1],[0,-1]]){const X=x+ax,Y=y+ay,k=X+','+Y;if(X<0||Y<0||X>=C||Y>=Rw||occ.has(k)||seen.has(k))continue;seen.add(k);q.push([X,Y,dd+1]);}}
    let sc=-dist*3+Math.min(reach,P.length*3+20)*2-(danger.has(nx+','+ny)&&!tset.has(nx+','+ny)?15:0)+Math.random();
    if(reach<P.length+4) sc-=500;
    if(sc>bs){bs=sc;best=[dx,dy];}
  }
  if(best) G.nextDir={x:best[0],y:best[1]};
}
