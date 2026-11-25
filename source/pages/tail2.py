
import datetime, json as _json
TODAY=datetime.date.today().isoformat()
CDN='https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/'
SHEETS=[(CDN+'770decc7-dece-4268-8672-0e2a3a39da8f.webp',['knight','archer','mage','cleric','rogue','bard','necro','p_heal','p_spd','p_dmg','p_dr','p_nova']),
 (CDN+'2a18e8bd-9f39-4c39-815f-f22a24a12475.webp',['q_kill','q_floor','q_coin','q_banner','q_nova','q_chest','q_crate','q_elite','q_boss','q_star','q_potion','q_combo','m_trophy','m_quests','m_daily','m_arcade','m_camp','m_settings','m_help','m_codex','m_review','m_ranks','m_tag','m_kids']),
 (CDN+'458b67d6-a92e-4126-b4a5-4aaca0aaacd6.webp',['u_mastery','u_might','u_vigor','u_haste','u_reach','u_whirl','u_thorns','u_bulwark','u_multi','u_pierce','u_blast','u_twin','u_anthem','u_legion','u_boneward','u_encore','u_mend','u_mass','u_crit','u_flurry','u_rally','u_rations','u_iron','u_magnet','u_bounty','u_sprint','u_glass','u_blood','u_frenzy','u_greed','r_normal','r_vault','r_hunt','r_camp','r_shrine','m_key']),
 (CDN+'fa21619d-831c-4d88-a8e6-cff647e75d1c.webp',['a_w5','a_w10','a_w15','a_w20','a_w30','a_k200','a_k500','a_k1000','a_el14','a_el42','a_traps','a_relics','a_full','a_p4','a_p6','a_arc20','a_classes5','a_skills','a_skills5','a_star3','a_legend','a_leg2','a_gold500','a_cb_necro','a_syn','a_syn5','a_cb_all','a_curse','a_curse3','a_flaw','a_cb_knight','a_cb_archer','a_cb_mage','a_cb_cleric','a_cb_rogue','a_cb_bard'])]
SPR={}
for si,(u,keys) in enumerate(SHEETS):
    for i,k in enumerate(keys): SPR[k]=(si,i,len(keys))
def ico(k,px=28,cls=''):
    si,i,n=SPR[k]; x=0 if n==1 else i/(n-1)*100
    return f'<i class="ui s{si} {cls}" style="--s:{px}px;background-position:{x:.4f}% 0;background-size:{n*100}% 100%" aria-hidden="true"></i>'
UPK={'Whirlwind':'u_whirl','Thorns':'u_thorns','Bulwark':'u_bulwark','Multishot':'u_multi','Piercing Shots':'u_pierce','Wider Blast':'u_blast','Twin Orbs':'u_twin','Greater Heal':'u_mend','Mass Heal':'u_mass','Assassin':'u_crit','Flurry':'u_flurry','Anthem':'u_anthem','Encore':'u_encore','Legion':'u_legion','Bone Ward':'u_boneward'}
STEPICO=['m_arcade','q_banner','q_star','r_normal','q_nova','q_boss','m_codex','m_camp']
FAQ={'en':[('Is Everlight Heroes free?','Yes. It is completely free to play, with no ads, no in-game purchases and no sign-up.'),
 ('Do I need to download anything?','No. It plays right in your web browser on phones, tablets and computers. On a phone you can add it to your home screen so it opens like an app.'),
 ('Is it OK for kids?','Yes. It is a cartoon fantasy adventure with no chat and no ads. Kids Mode removes wall bumps, softens hits, gently auto-steers and adds checkpoints, and Tag Team lets two players share one device.'),
 ('Does my progress save?','Yes. Progress saves automatically on your device. Cloud Save in Settings gives you a code to carry your heroes to another device.'),
 ('How long does a run take?','Each floor takes under a minute. A full climb is 50 floors with 10 bosses, and you can save and quit between floors at any time.'),
 ('Which languages are supported?','English and Portuguese (Brazil), including the narrated story.')],
'pt':[('Everlight Heroes é grátis?','Sim. É totalmente grátis, sem anúncios, sem compras dentro do jogo e sem cadastro.'),
 ('Preciso baixar alguma coisa?','Não. O jogo roda direto no navegador, no celular, tablet ou computador. No celular você pode adicioná-lo à tela inicial para abrir como um app.'),
 ('É adequado para crianças?','Sim. É uma aventura de fantasia em desenho, sem chat e sem anúncios. O Modo Criança tira as batidas nas paredes, deixa os golpes mais leves, ajuda a guiar e adiciona pontos de controle. O Revezamento deixa dois jogadores dividirem o mesmo aparelho.'),
 ('Meu progresso fica salvo?','Sim. O progresso é salvo automaticamente no aparelho. O Salvamento na Nuvem, nas Configurações, gera um código para levar seus heróis para outro aparelho.'),
 ('Quanto tempo dura uma partida?','Cada andar leva menos de um minuto. A escalada completa tem 50 andares e 10 chefões, e você pode salvar e sair entre os andares quando quiser.'),
 ('Quais idiomas o jogo tem?','Inglês e português (Brasil), incluindo a história narrada.')]}
X={'en':dict(crumbs='Home',faq='Frequently asked questions',jump='Jump to',free='Free · No ads · No download',onthis='On this page',
  learn='Learn',playh='Play',about='About',footdesc='A free hero adventure for phones, tablets and computers. Lead your party, beat 10 bosses and bring back the light.',
  start='Starter',idxintro='Tap a hero to see their powers, upgrades, best team-ups and secret Nova move.',
  more='More heroes',faqlink='FAQ',lang='Português',langshort='PT',hg='Hero guide',fight='How they fight',power='Special power',team='Best team-ups',tip='Tip',kids='Playing with kids?'),
'pt':dict(crumbs='Início',faq='Perguntas frequentes',jump='Ir para',free='Grátis · Sem anúncios · Sem download',onthis='Nesta página',
  learn='Aprenda',playh='Jogue',about='Sobre',footdesc='Uma aventura de heróis grátis para celular, tablet e computador. Lidere seu grupo, derrote 10 chefões e traga a luz de volta.',
  start='Inicial',idxintro='Toque num herói para ver poderes, melhorias, melhores combinações e a Nova secreta.',
  more='Mais heróis',faqlink='Dúvidas',lang='English',langshort='EN',hg='Guia do herói',fight='Como luta',power='Poder especial',team='Melhores combinações',tip='Dica',kids='Jogando com crianças?')}
C=CDN
PTIMG={0:C+'66a35b61-77d7-4e51-a384-03505c8e71a5.webp',1:C+'e0f030e8-aa7f-4fcd-8e21-17c6e71ed843.webp',2:C+'cd76e801-8e37-405e-a059-6c1b534751a5.webp',3:C+'e801c8ba-ab94-4d0d-ac00-87b82e4b8888.webp',6:C+'76c61d8a-4590-4da1-b589-c0f66b5dcca2.webp',7:C+'c5b5c39d-289e-478d-9dc9-9f2c9cb4f4b9.webp'}
def strip(s): return re.sub('<[^>]+>','',s)
def build(lang):
    t=T[lang]; x=X[lang]; P=t['pre']; other='pt' if lang=='en' else 'en'; OP=T[other]['pre']
    home='/?lang=pt' if lang=='pt' else '/'
    def ld(o): return '<script type="application/ld+json">'+_json.dumps(o,ensure_ascii=False)+'</script>'
    def crumbs(items,selfurl):
        html='<nav class="crumbs" aria-label="breadcrumb">'+' <span>›</span> '.join((f'<a href="{h}">{E(n)}</a>' if h else f'<b>{E(n)}</b>') for n,h in items)+'</nav>'
        data={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":'__SITE__'+(h or selfurl).lstrip('/')} for i,(n,h) in enumerate(items)]}
        return html, ld(data)
    def page(path,title,desc,body,og='/og.jpg',extra_ld='',active=''):
        full=P+path; os.makedirs(os.path.dirname(L+full),exist_ok=True)
        rel=path.lstrip('/').replace('index.html','')
        url='__SITE__'+full.lstrip('/').replace('index.html','')
        en_url='__SITE__'+rel; pt_url='__SITE__pt/'+rel
        lp=OP+path.replace('index.html','')
        def na(h,lab,key):
            cur=' aria-current="page"' if active==key else ''
            return f'<a href="{h}"{cur}>{lab}</a>'
        NAV=(f'<header class="snav"><div class="sin"><a class="brand" href="{home}"><img src="/icons/icon-192.png" alt="" width="34" height="34"><span>Everlight <b>Heroes</b></span></a>'
             f'<nav class="links">{na(P+"/how-to-play/",t["howto"],"how")}{na(P+"/heroes/",t["heroes"],"heroes")}{na(P+"/how-to-play/#faq",x["faqlink"],"faq")}</nav>'
             f'<div class="act"><a class="lang" href="{lp}" hreflang="{T[other]["htmllang"]}" title="{x["lang"]}">🌐 {x["langshort"]}</a><a class="sbtn" href="{t["play"]}">{t["playtxt"]}</a></div></div></header>')
        FOOT=(f'<footer class="sfoot"><div class="fin"><div class="fbrand"><a class="brand" href="{home}"><img src="/icons/icon-192.png" alt="" width="40" height="40" loading="lazy"><span>Everlight <b>Heroes</b></span></a><p>{x["footdesc"]}</p><p class="free">{x["free"]}</p></div>'
              f'<div><h4>{x["playh"]}</h4><a href="{t["play"]}">{t["playtxt"].replace("▶ ","")}</a><a href="{home}">{t["home"]}</a></div>'
              f'<div><h4>{x["learn"]}</h4><a href="{P}/how-to-play/">{t["howto"]}</a><a href="{P}/heroes/">{t["heroes"]}</a><a href="{P}/how-to-play/#faq">{x["faqlink"]}</a></div>'
              f'<div><h4>{x["about"]}</h4><a href="/privacy.html">{t["privacy"]}</a><a href="/terms.html">{t["terms"]}</a><a href="{lp}" hreflang="{T[other]["htmllang"]}">🌐 {x["lang"]}</a></div></div>'
              f'<p class="copy">© {datetime.date.today().year} Everlight Heroes</p></footer><div class="pbar"><a class="sbtn" href="{t["play"]}">{t["playtxt"]}</a></div>')
        ogi=og if og.startswith('http') else '__SITE__'+og.lstrip('/')
        locale='pt_BR' if lang=='pt' else 'en_US'; alt_loc='en_US' if lang=='pt' else 'pt_BR'
        sheets=''.join(f'.ui.s{i}{{background-image:url({u})}}' for i,(u,_) in enumerate(SHEETS))
        html=(f'<!DOCTYPE html><html lang="{t["htmllang"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
              f'<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}">\n'
              f'<link rel="alternate" hreflang="en" href="{en_url}"><link rel="alternate" hreflang="pt-BR" href="{pt_url}"><link rel="alternate" hreflang="x-default" href="{en_url}">\n'
              f'<meta property="og:type" content="website"><meta property="og:site_name" content="Everlight Heroes"><meta property="og:locale" content="{locale}"><meta property="og:locale:alternate" content="{alt_loc}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{ogi}"><meta property="og:url" content="{url}">'
              f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{ogi}">\n'
              f'<meta name="theme-color" content="#1c1432"><link rel="icon" href="/icons/icon-192.png"><link rel="apple-touch-icon" href="/icons/apple-touch-icon.png"><link rel="manifest" href="/manifest.webmanifest"><link rel="preconnect" href="https://d2ol7oe51mr4n9.cloudfront.net" crossorigin><link rel="stylesheet" href="/site.css"><style>{sheets}</style>{extra_ld}</head>'
              f'<body>{NAV}<main>{body}</main>{FOOT}</body></html>')
        open(L+full,'w').write(html)
    def bars(st):
        lab=list(zip(['hp','dmg','rng','spd'],t['stats']))
        return '<div class="stats">'+''.join(f'<div><span>{l}</span><i>{"".join("<b></b>" if j<st[k] else "<em></em>" for j in range(5))}</i></div>' for k,l in lab)+'</div>'
    HS=[loc(h,lang) for h in HEROES]; BK={h['k']:h for h in HS}; ENH={h['k']:h for h in HEROES}
    sub=(P.lstrip('/')+'/') if P else ''
    # ---- heroes index
    cards=''.join(f'<a class="hcard" href="{P}/heroes/{h["k"]}/" style="--c:{h["col"]}"><img src="/img/hero-{h["k"]}.webp" alt="{E(h["name"])}" width="160" height="160" loading="lazy"><b>{ico(h["k"],22)} {h["name"]}</b><span>{h["role"]}</span><small class="{"st" if h["start"] else "lk"}">{x["start"] if h["start"] else str(h.get("cost",""))+" 🪙"}</small></a>' for h in HS)
    cr,crld=crumbs([(x['crumbs'],home),(t['heroes'],None)],P+'/heroes/')
    il={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"__SITE__{sub}heroes/{h['k']}/","name":h['name']} for i,h in enumerate(HS)]}
    page('/heroes/index.html',t['idx_title'],t['idx_desc'],
     f'{cr}<section class="phead"><h1>{t["idx_h1"]}</h1><p>{t["idx_p"]} {x["idxintro"]}</p></section><div class="hgrid">{cards}</div>'
     f'<section class="box"><h2>{ico("q_banner",30)} {t["idx_h2"]}</h2><p>{t["idx_box"]}</p></section>'
     f'<section class="cta"><a class="sbtn big" href="{t["play"]}">{t["playtxt"]}</a><p class="free">{x["free"]}</p></section>',extra_ld=crld+ld(il),active='heroes')
    # ---- hero pages
    for i,h in enumerate(HS):
        eh=ENH[h['k']]; prev=HS[i-1]; nxt=HS[(i+1)%len(HS)]
        pairs=''.join(f'<a class="pair" href="{P}/heroes/{p}/" style="--c:{BK[p]["col"]}"><img src="/img/hero-{p}.webp" alt="{E(BK[p]["name"])}" width="56" height="56" loading="lazy"><div><b>{BK[p]["name"]} · {E(n)}</b><span>{E(d)}</span></div></a>' for p,n,d in h['pairs'])
        ups=''.join(f'<li>{ico(UPK.get(eh["ups"][j][1],"q_star"),40)}<div><b>{E(b)}</b><span>{E(c)}</span></div></li>' for j,(a,b,c) in enumerate(h['ups']))
        unlock=t['start'] if h['start'] else t['unl'].format(c=h['cost'])
        the=t['the'].format(n=h['name']); nd=h["nova"][2]; nd=nd[0].lower()+nd[1:]
        cr,crld=crumbs([(x['crumbs'],home),(t['heroes'],P+'/heroes/'),(h['name'],None)],f'{P}/heroes/{h["k"]}/')
        others=''.join(f'<a href="{P}/heroes/{o["k"]}/" style="--c:{o["col"]}"><img src="/img/hero-{o["k"]}.webp" alt="{E(o["name"])}" width="64" height="64" loading="lazy"><span>{o["name"]}</span></a>' for o in HS if o['k']!=h['k'])
        body=(f'{cr}<section class="hhero" style="--c:{h["col"]}"><div class="hpic"><img src="/img/hero-{h["k"]}.webp" alt="{E(the)}" width="160" height="160" fetchpriority="high">{ico(h["k"],48,"badge")}</div>'
              f'<div class="hinfo"><p class="kick">{x["hg"]} · {h["role"]}</p><h1>{the}</h1><p class="lead">{E(h["blurb"])}</p><p class="unl">{ico("q_floor" if h["start"] else "m_camp",22)} {unlock}</p>{bars(h["stats"])}</div></section>'
              f'<div class="g2"><section class="box"><h2>{ico("q_kill",30)} {x["fight"]}</h2><p>{E(h["attack"])}</p><h3>{ico("m_review",22)} {x["power"]}: {E(h["power"][0])}</h3><p>{E(h["power"][1])}</p></section>'
              f'<section class="box"><h2>{ico(h["k"],30)} {t["skill"].format(s=E(h["skill"][1]))}</h2><p>{E(h["skill"][2])} {t["skunl"].format(n=h["name"])}</p><h3>{t["upg"]}</h3><ul class="ups">{ups}</ul></section></div>'
              f'<section class="box"><h2>{ico("q_banner",30)} {x["team"]}</h2><p>{t["teamp"]}</p><div class="pairs">{pairs}</div></section>'
              f'<section class="box nova"><h2>{ico("a_cb_"+h["k"],34)} {t["nova"].format(n=E(h["nova"][1]))}</h2><p>{t["novap"].format(n=h["name"],v=E(h["nova"][1]),d=E(nd))}</p></section>'
              f'<section class="box tip"><h2>{ico("m_help",30)} {x["tip"]}</h2><p>{E(h["tip"])}</p></section>'
              f'<section class="cta"><a class="sbtn big" href="{t["play"]}">{t["playtxt"]}</a><p class="free">{x["free"]}</p></section>'
              f'<section class="more"><h2>{x["more"]}</h2><div class="mrow">{others}</div><div class="pn"><a href="{P}/heroes/{prev["k"]}/">← {prev["name"]}</a><a href="{P}/heroes/">{t["all"]}</a><a href="{P}/heroes/{nxt["k"]}/">{nxt["name"]} →</a></div></section>')
        page(f'/heroes/{h["k"]}/index.html',t['h_title'].format(n=h['name']),t['h_desc'].format(n=h['name'],r=h['role'].lower(),p=h['power'][1]),body,extra_ld=crld,active='heroes')
    # ---- how to play
    SS=STEPS if lang=='en' else [(PTIMG.get(i,STEPS[i][0]),)+s for i,s in enumerate(PT_STEPS)]
    nm=lambda tt: re.sub(r'^[0-9]+\. ','',strip(tt))
    toc=''.join(f'<a href="#s{i+1}">{ico(STEPICO[i],20)} {nm(tt)}</a>' for i,(img,tt,b,tip) in enumerate(SS))
    steps=''.join(f'<section class="step" id="s{i+1}"><figure><img src="{img}" alt="{E(nm(tt))}" loading="{"eager" if i==0 else "lazy"}" width="960" height="540"></figure><div><h2><span class="num">{i+1}</span>{ico(STEPICO[i],30)} {nm(tt)}</h2><p>{b}</p><p class="tip">💡 {tip}</p></div></section>' for i,(img,tt,b,tip) in enumerate(SS))
    faq=''.join(f'<details class="qa"{" open" if j==0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for j,(q,a) in enumerate(FAQ[lang]))
    cr,crld=crumbs([(x['crumbs'],home),(t['howto'],None)],P+'/how-to-play/')
    howto={"@context":"https://schema.org","@type":"HowTo","name":t['ht_title'],"description":t['ht_desc'],"totalTime":"PT2M","step":[{"@type":"HowToStep","position":i+1,"name":nm(tt),"text":strip(b),"image":img,"url":f"__SITE__{sub}how-to-play/#s{i+1}"} for i,(img,tt,b,tip) in enumerate(SS)]}
    faqld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ[lang]]}
    page('/how-to-play/index.html',t['ht_title'],t['ht_desc'],
     f'{cr}<section class="phead"><h1>{t["ht_h1"]}</h1><p>{t["ht_p"]}</p></section><nav class="toc" aria-label="{x["onthis"]}"><b>{x["jump"]}:</b>{toc}<a href="#faq">{ico("m_help",20)} {x["faqlink"]}</a></nav>{steps}'
     f'<section class="box kids"><h2>{ico("m_kids",34)} {x["kids"]}</h2><p>{t["kids"]}</p></section>'
     f'<section class="faq" id="faq"><h2>{ico("m_help",30)} {x["faq"]}</h2>{faq}</section>'
     f'<section class="cta"><a class="sbtn big" href="{t["play"]}">{t["first"]}</a><p class="free">{x["free"]}</p></section>',og=STEPS[5][0],extra_ld=crld+ld(howto)+ld(faqld),active='how')
build('en'); build('pt')
# sitemap with hreflang alternates + lastmod
def urlx(en,pt,pri):
    alt=f'<xhtml:link rel="alternate" hreflang="en" href="{en}"/><xhtml:link rel="alternate" hreflang="pt-BR" href="{pt}"/><xhtml:link rel="alternate" hreflang="x-default" href="{en}"/>'
    return f'<url><loc>{en}</loc><lastmod>{TODAY}</lastmod><priority>{pri}</priority>{alt}</url>\n<url><loc>{pt}</loc><lastmod>{TODAY}</lastmod><priority>{pri}</priority>{alt}</url>\n'
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
sm+=f'<url><loc>__SITE__</loc><lastmod>{TODAY}</lastmod><priority>1.0</priority></url>\n'
for p in ['how-to-play/','heroes/']+[f'heroes/{h["k"]}/' for h in HEROES]: sm+=urlx('__SITE__'+p,'__SITE__pt/'+p,'0.8' if p in ('how-to-play/','heroes/') else '0.6')
sm+=f'<url><loc>__SITE__privacy.html</loc><lastmod>{TODAY}</lastmod><priority>0.2</priority></url>\n<url><loc>__SITE__terms.html</loc><lastmod>{TODAY}</lastmod><priority>0.2</priority></url>\n</urlset>\n'
open(L+'/sitemap.xml','w').write(sm)
print('pages ok')
