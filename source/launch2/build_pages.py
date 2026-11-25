#!/usr/bin/env python3
"""Builds the Oss! Squad static pages (how to play, the crew, one page per grappler, privacy, terms, 404)
in English and Portuguese, into OUT (default: ../launch_out). Images come from the Higgs CDN."""
import os, sys, html, json

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'launch_out')
CDN = 'https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/'
OG = CDN + '309f3a26-da9a-43ce-b6e3-1b8b6a3fb156.jpg'
IMG = {'knight': 'bbf23511-c182-4be2-9a52-208607201ac3', 'archer': 'f4b2553d-5771-44e3-a2a8-c413fa186ab0',
       'rogue': 'a4fa045b-3b33-4cab-8f07-17b7a407a05d', 'mage': 'ebf49815-57be-416b-a261-754c000b9b10',
       'cleric': '6504f35d-5993-4350-96ca-6693dc0aaf9f', 'bard': 'f97b87cf-a8af-440f-83ba-d6bdd9b5f0ae',
       'necro': '3a5dd796-2224-4a04-a854-720435627478'}
ORDER = ['knight', 'archer', 'rogue', 'mage', 'cleric', 'bard', 'necro']

# name, role, skill, skill text, passive, blurb, tip  (en, pt)
CREW = {
 'knight': {'col': '#6ea8ff', 'ico': '🤼', 'hp': 130, 'en': ['Wrestler', 'Tank', 'Double-Leg Slam', 'A huge takedown slams the mat, damaging and knocking back nearby rivals.', 'Base: the whole crew takes 10% less damage.', 'Built like a fridge and twice as stubborn. The Wrestler leads the line, soaks up the hits and keeps everyone behind him safe.', 'Put the Wrestler at the front of your line, where the hits land first.'],
            'pt': ['Lutador', 'Tanque', 'Baiana Explosiva', 'Uma queda enorme sacode o tatame, causando dano e empurrando os rivais por perto.', 'Base: toda a equipe sofre 10% menos dano.', 'Forte como uma geladeira e duas vezes mais teimoso. O Lutador puxa a fila, aguenta os golpes e protege quem vem atrás.', 'Coloque o Lutador na frente da fila, onde os golpes chegam primeiro.']},
 'archer': {'col': '#7ddc6a', 'ico': '🥋', 'hp': 70, 'en': ['Judoka', 'Long range', 'Ippon Storm', 'A flurry of big throws crashes down on the biggest group of rivals.', 'Throws from far away, so she rarely gets caught.', 'Quick feet, quicker hands. The Judoka throws rivals from across the mat before they ever reach your crew.', 'Great early pick: her reach clears rivals before they touch you.'],
            'pt': ['Judoca', 'Longo alcance', 'Chuva de Ippons', 'Uma sequência de grandes arremessos cai sobre o maior grupo de rivais.', 'Arremessa de longe, então quase nunca é pega.', 'Pés rápidos, mãos mais rápidas ainda. A Judoca arremessa rivais do outro lado do tatame antes que eles cheguem na equipe.', 'Ótima escolha no começo: o alcance dela limpa rivais antes que encostem em você.']},
 'rogue': {'col': '#ff8c6e', 'ico': '🔺', 'hp': 85, 'en': ['Jiu-jitero', 'Submissions', 'Scramble', 'Scrambles through nearby rivals and submits up to six of them.', 'Submissions (critical hits) deal 2.5x damage.', 'Patient, sneaky and always smiling. The Jiu-jitero waits for one small mistake, then the tap comes fast.', 'Gear with critical chance turns the Jiu-jitero into a tap-out machine.'],
           'pt': ['Jiu-jiteiro', 'Finalizações', 'Scramble', 'Passa por entre os rivais por perto e finaliza até seis deles.', 'Finalizações (acertos críticos) causam 2,5x de dano.', 'Paciente, malandro e sempre sorrindo. O Jiu-jiteiro espera um pequeno erro, e o tapinha vem rápido.', 'Equipamento com chance de crítico transforma o Jiu-jiteiro numa máquina de finalizar.']},
 'mage': {'col': '#c27bff', 'ico': '💥', 'hp': 60, 'en': ['Sambo', 'Area damage', 'Suplex Bomb', 'Launches a massive throw-into-leglock on the biggest cluster of rivals.', 'Big, slow hits that land on whole groups.', 'Loud, proud and very explosive. The Sambo fighter turns a crowd of rivals into one big highlight reel.', 'Keep the Sambo fighter in the middle of the line, away from the first hits.'],
          'pt': ['Sambista', 'Dano em área', 'Bomba de Suplex', 'Lança um arremesso gigante com chave de perna no maior grupo de rivais.', 'Golpes grandes e lentos que acertam grupos inteiros.', 'Barulhento, orgulhoso e muito explosivo. O Sambista transforma um monte de rivais num grande lance de melhores momentos.', 'Deixe o Sambista no meio da fila, longe dos primeiros golpes.']},
 'cleric': {'col': '#ffe27a', 'ico': '📋', 'hp': 85, 'en': ['Coach', 'Healer', 'Water Break', 'Corner advice heals the crew around the Coach for 5 seconds.', 'Corner advice heals the most hurt teammate, and every shout heals too.', 'Clipboard in one hand, water bottle in the other. The Coach keeps the crew on its feet when the rounds get long.', 'One Coach makes long runs much easier. Two is a party.'],
            'pt': ['Treinador', 'Cura', 'Pausa pra Água', 'Os conselhos do corner curam a equipe perto do Treinador por 5 segundos.', 'Os conselhos do corner curam o colega mais machucado, e cada grito também cura.', 'Prancheta numa mão, garrafa de água na outra. O Treinador mantém a equipe de pé quando os rounds ficam longos.', 'Um Treinador deixa as partidas longas bem mais fáceis.']},
 'bard': {'col': '#7fe6d8', 'ico': '⏱️', 'hp': 80, 'en': ['Athlete', 'Support', 'Second Wind', 'The whole crew attacks 35% faster for 5 seconds.', 'Conditioning aura: +8% attack speed and +10% damage for the crew. A breather heals everyone every 5 seconds.', 'Never tired, always counting reps. The Athlete makes everybody around her faster and stronger.', 'The Athlete gets better the bigger your crew is.'],
          'pt': ['Atleta', 'Suporte', 'Segundo Fôlego', 'Toda a equipe ataca 35% mais rápido por 5 segundos.', 'Aura de condicionamento: +8% de velocidade de ataque e +10% de dano para a equipe. Um respiro cura todos a cada 5 segundos.', 'Nunca cansa, sempre contando repetições. A Atleta deixa todo mundo em volta mais rápido e mais forte.', 'A Atleta fica melhor quanto maior for a sua equipe.']},
 'necro': {'col': '#6fe08a', 'ico': '🏫', 'hp': 65, 'en': ['Academy Owner', 'Summoner', 'Open Mat', 'Calls in students who hunt rivals for 8 seconds.', 'Calls a student onto the mat every few seconds to fight for you.', 'Forty years on the mat and still the first one in. The Academy Owner never fights alone: the students always show up.', 'Unlock the Academy Owner at Camp for a crew that keeps growing.'],
           'pt': ['Mestre', 'Invocador', 'Treino Livre', 'Chama alunos que caçam rivais por 8 segundos.', 'Chama um aluno para o tatame a cada poucos segundos para lutar por você.', 'Quarenta anos de tatame e ainda é o primeiro a chegar. O Mestre nunca luta sozinho: os alunos sempre aparecem.', 'Desbloqueie o Mestre no Camp para uma equipe que não para de crescer.']},
}

T = {
 'en': {'lang': 'en', 'pre': '', 'home': 'Home', 'how': 'How to play', 'crew': 'The crew', 'faq': 'FAQ', 'play': '▶ Play free',
        'free': 'Free · No ads · No download', 'other': '🌐 PT', 'otherl': 'pt-BR', 'privacy': 'Privacy', 'terms': 'Terms',
        'tag': 'A free jiu-jitsu party adventure for phones, tablets and computers. Lead your crew, beat 10 champions and break the Master Spell.',
        'role': 'Role', 'skill': 'Special move', 'passive': 'Passive', 'tip': 'Tip', 'hp': 'Health', 'meet': 'Meet the rest of the crew',
        'crew_t': 'The crew: all 7 grapplers', 'crew_d': 'Meet the Oss! Squad crew: the Wrestler, Judoka, Jiu-jitero, Sambo, Coach, Athlete and Academy Owner. What each one does and how to use them.',
        'crew_h': 'Seven grapplers, one crew. Mix them however you like: every crew plays differently.',
        'how_t': 'How to play Oss! Squad: beginner’s guide & FAQ', 'how_d': 'Learn Oss! Squad in 2 minutes: steer your crew, recruit grapplers, pick upgrades, use your special and beat the champions.',
        'how_h': 'Oss! Squad takes a minute to learn. Here’s everything you need for your first run.'},
 'pt': {'lang': 'pt-BR', 'pre': '/pt', 'home': 'Início', 'how': 'Como jogar', 'crew': 'A equipe', 'faq': 'Perguntas', 'play': '▶ Jogar grátis',
        'free': 'Grátis · Sem anúncios · Sem download', 'other': '🌐 EN', 'otherl': 'en', 'privacy': 'Privacidade', 'terms': 'Termos',
        'tag': 'Uma aventura de jiu-jitsu grátis para celular, tablet e computador. Lidere sua equipe, vença 10 campeões e quebre o Feitiço do Mestre.',
        'role': 'Função', 'skill': 'Golpe especial', 'passive': 'Passiva', 'tip': 'Dica', 'hp': 'Vida', 'meet': 'Conheça o resto da equipe',
        'crew_t': 'A equipe: os 7 lutadores', 'crew_d': 'Conheça a equipe do Oss! Squad: Lutador, Judoca, Jiu-jiteiro, Sambista, Treinador, Atleta e Mestre. O que cada um faz e como usar.',
        'crew_h': 'Sete lutadores, uma equipe. Misture como quiser: cada equipe joga de um jeito diferente.',
        'how_t': 'Como jogar Oss! Squad: guia para iniciantes e perguntas', 'how_d': 'Aprenda Oss! Squad em 2 minutos: guie sua equipe, recrute lutadores, escolha melhorias, use o especial e vença os campeões.',
        'how_h': 'Oss! Squad se aprende em um minuto. Aqui está tudo o que você precisa para a primeira partida.'},
}

STEPS = {
 'en': [('🧭', 'Steer your line', 'Your crew walks onto the mat in a line. <b>Swipe</b> on your phone, or use the <b>arrow keys / WASD</b> on a computer, to turn. You only steer: your grapplers fight on their own.', 'Don’t bump into the walls or your own tail. It hurts the whole crew, so turn early!'),
        ('🚩', 'Recruit new grapplers', 'Each gym hides a recruit flag. Steer into it to add a new grappler to your line, or to give one you already have another star.', 'A bigger crew hits harder, but a longer line is harder to steer.'),
        ('⬆️', 'Pick an upgrade after each round', 'Clear a round and choose one of three upgrades: power up one grappler, or help the whole crew.', 'Spread upgrades around. Every grappler can reach level 15.'),
        ('🛣️', 'Choose your path', 'Between rounds you pick what comes next: a normal round, a rest stop to heal, or a risky round with more rivals and better rewards.', 'Hurt? Take the rest. Feeling strong? Take the risk.'),
        ('⚡', 'Fire your special', 'Beating rivals fills the special meter in the corner. When it’s full, tap it (or press <b>Q</b>) to hit every rival near your crew.', 'Some crews unlock a secret special. Try a crew of only Wrestlers!'),
        ('🏆', 'Beat the champions', 'Every fifth round a champion is waiting, under the Master Spell. Watch their big moves and keep your line moving.', 'Each champion you free plays the next chapter of the story.'),
        ('🎒', 'Gear up between rounds', 'Open <b>Crew</b> between rounds to spend points, swap gear and check everyone’s stats. Crew and gear changes happen only between rounds.', 'Better gear goes to the grappler who needs it most.'),
        ('🎖️', 'Climb the belts', 'Coins you earn are kept even if your crew taps out. Spend them at <b>Camp</b>. Beat the whole circuit to start earning belts in the Legacy Hall, from White all the way to Red.', 'Each new belt brings real rewards, and some belts change how your crew looks.')],
 'pt': [('🧭', 'Guie sua fila', 'Sua equipe entra no tatame em fila. <b>Deslize</b> no celular, ou use as <b>setas / WASD</b> no computador, para virar. Você só guia: os lutadores lutam sozinhos.', 'Não bata nas paredes nem no próprio rabo da fila. Isso machuca a equipe toda, então vire cedo!'),
        ('🚩', 'Recrute novos lutadores', 'Cada academia esconde uma bandeira de recrutamento. Passe por ela para adicionar um lutador à fila, ou para dar mais uma estrela a um que você já tem.', 'Uma equipe maior bate mais forte, mas uma fila longa é mais difícil de guiar.'),
        ('⬆️', 'Escolha uma melhoria a cada round', 'Termine um round e escolha uma de três melhorias: fortaleça um lutador ou ajude a equipe toda.', 'Espalhe as melhorias. Cada lutador pode chegar ao nível 15.'),
        ('🛣️', 'Escolha seu caminho', 'Entre os rounds você escolhe o que vem: um round normal, uma parada para curar, ou um round arriscado com mais rivais e prêmios melhores.', 'Machucado? Descanse. Forte? Arrisque.'),
        ('⚡', 'Use o especial', 'Vencer rivais enche o medidor especial no canto. Quando estiver cheio, toque nele (ou aperte <b>Q</b>) para acertar todos os rivais perto da equipe.', 'Algumas equipes liberam um especial secreto. Tente uma equipe só de Lutadores!'),
        ('🏆', 'Vença os campeões', 'A cada cinco rounds um campeão espera, sob o Feitiço do Mestre. Fique de olho nos golpes grandes e mantenha a fila andando.', 'Cada campeão libertado mostra o próximo capítulo da história.'),
        ('🎒', 'Equipe-se entre os rounds', 'Abra <b>Equipe</b> entre os rounds para gastar pontos, trocar equipamentos e ver os atributos de todos. Mudanças de equipe e equipamento só acontecem entre os rounds.', 'O melhor equipamento vai para o lutador que mais precisa.'),
        ('🎖️', 'Suba de faixa', 'As moedas que você ganha ficam guardadas mesmo se a equipe bater. Gaste no <b>Camp</b>. Vença o circuito inteiro para começar a ganhar faixas no Salão do Legado, da Branca até a Vermelha.', 'Cada faixa nova traz prêmios de verdade, e algumas mudam o visual da equipe.')],
}
FAQ = {
 'en': [('Is Oss! Squad free?', 'Yes. It is completely free to play, with no ads, no in-game purchases and no sign-up.'),
        ('Do I need to download anything?', 'No. It plays in your web browser on phones, tablets and computers. On a phone you can add it to your home screen so it opens like an app.'),
        ('Is it OK for kids?', 'Yes. It is a cartoon grappling adventure with no chat, no ads and no blood. Kids Mode removes wall bumps, softens hits and adds checkpoints, and Tag Team lets two players share one device.'),
        ('Does my progress save?', 'Yes. Progress saves automatically on your device, and Cloud Save in Settings gives you a code to carry it to another device.'),
        ('How long does a run take?', 'Each round takes under a minute. The full circuit is 50 rounds with 10 champions, and you can save and quit between rounds.'),
        ('Which languages are supported?', 'English and Portuguese (Brazil), including the narrated story.')],
 'pt': [('Oss! Squad é grátis?', 'Sim. É totalmente grátis, sem anúncios, sem compras dentro do jogo e sem cadastro.'),
        ('Preciso baixar alguma coisa?', 'Não. Funciona no navegador do celular, tablet ou computador. No celular você pode adicionar à tela inicial para abrir como um app.'),
        ('É bom para crianças?', 'Sim. É uma aventura de luta em desenho, sem chat, sem anúncios e sem sangue. O Modo Criança tira as batidas na parede, suaviza os golpes e adiciona checkpoints, e o Revezamento deixa dois jogadores dividirem um aparelho.'),
        ('Meu progresso fica salvo?', 'Sim. O progresso é salvo automaticamente no aparelho, e o Salvamento na Nuvem em Configurações gera um código para levar para outro aparelho.'),
        ('Quanto tempo dura uma partida?', 'Cada round leva menos de um minuto. O circuito completo tem 50 rounds e 10 campeões, e você pode salvar e sair entre os rounds.'),
        ('Quais idiomas existem?', 'Inglês e português (Brasil), incluindo a história narrada.')],
}

CSS = """
.pg{max-width:980px;margin:0 auto;padding:18px 16px 90px}
.crumbs{font-size:14px;opacity:.8;margin:6px 0 10px}.crumbs a{color:#d4c4ff}
.ph h1{font-size:clamp(28px,6vw,44px);line-height:1.15;margin:6px 0 8px}.ph p{font-size:18px;opacity:.9;margin:0 0 18px}
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.cc{display:block;text-decoration:none;color:inherit;background:#ffffff0d;border:2px solid #ffffff1a;border-radius:16px;padding:12px;text-align:center}
.cc:hover{border-color:var(--c)}.cc img{width:112px;height:112px;object-fit:contain}.cc b{display:block;font-size:18px;color:var(--c)}.cc span{font-size:13px;opacity:.8}
.stp{display:flex;gap:14px;align-items:flex-start;background:#ffffff0a;border-radius:16px;padding:14px;margin:12px 0}
.stp .n{flex:none;width:44px;height:44px;border-radius:50%;background:#ffd86b;color:#1c1432;font-weight:900;display:grid;place-items:center;font-size:20px}
.stp h2{margin:0 0 4px;font-size:20px}.stp p{margin:4px 0}.tip{font-size:14px;opacity:.85}
.hero{display:grid;grid-template-columns:200px 1fr;gap:18px;align-items:center}.hero img{width:200px;height:200px;object-fit:contain;background:radial-gradient(circle,var(--c) -40%,transparent 70%);border-radius:20px}
@media(max-width:560px){.hero{grid-template-columns:1fr;text-align:center}.hero img{margin:0 auto}}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:16px 0}.facts div{background:#ffffff0d;border-radius:14px;padding:12px}.facts h3{margin:0 0 4px;font-size:14px;opacity:.75;font-weight:600}
details.qa{background:#ffffff0a;border-radius:12px;padding:10px 14px;margin:8px 0}details.qa summary{font-weight:700;cursor:pointer}
.ctab{text-align:center;margin:28px 0}.bigbtn{display:inline-block;background:#ffd86b;color:#1c1432;font-weight:900;font-size:20px;padding:14px 26px;border-radius:999px;text-decoration:none}
.mini{display:flex;flex-wrap:wrap;gap:8px}.mini a{display:flex;align-items:center;gap:6px;background:#ffffff0d;border-radius:999px;padding:4px 12px 4px 4px;text-decoration:none;color:inherit}.mini img{width:36px;height:36px}
.legal h2{font-size:20px;margin-top:22px}
"""

def esc(s): return html.escape(s, quote=True)

def page(L, path, title, desc, body, alt_path=None, crumbs=None):
    t = T[L]; o = 'pt' if L == 'en' else 'en'
    altp = alt_path if alt_path is not None else path
    me = (t['pre'] + path); other = (T[o]['pre'] + altp) if not path.endswith('.html') else path
    nav = (f'<header class="snav"><div class="sin"><a class="brand" href="{t["pre"] or "/"}{"/" if t["pre"] else ""}"><img src="https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/04e8362a-99da-41d3-804b-62b663677540.png" alt="" width="34" height="34"><span>Oss! <b>Squad</b></span></a>'
           f'<nav class="links"><a href="{t["pre"]}/how-to-play/">{t["how"]}</a><a href="{t["pre"]}/heroes/">{t["crew"]}</a><a href="{t["pre"]}/how-to-play/#faq">{t["faq"]}</a></nav>'
           f'<div class="act"><a class="lang" href="{other}" hreflang="{t["otherl"]}">{t["other"]}</a><a class="sbtn" href="/?play">{t["play"]}</a></div></div></header>')
    cr = ''
    if crumbs:
        cr = '<nav class="crumbs" aria-label="breadcrumb">' + ' › '.join(f'<a href="{u}">{esc(n)}</a>' if u else f'<b>{esc(n)}</b>' for n, u in crumbs) + '</nav>'
    foot = (f'<footer class="sfoot"><div class="fin"><div class="fbrand"><a class="brand" href="/"><img src="https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/04e8362a-99da-41d3-804b-62b663677540.png" alt="" width="40" height="40" loading="lazy"><span>Oss! <b>Squad</b></span></a>'
            f'<p>{esc(t["tag"])}</p><p class="free">{t["free"]}</p></div>'
            f'<div><h4>{t["play"][2:]}</h4><a href="/?play">{t["play"]}</a><a href="/">{t["home"]}</a></div>'
            f'<div><h4>{t["how"]}</h4><a href="{t["pre"]}/how-to-play/">{t["how"]}</a><a href="{t["pre"]}/heroes/">{t["crew"]}</a><a href="{t["pre"]}/how-to-play/#faq">{t["faq"]}</a></div>'
            f'<div><h4>Oss!</h4><a href="/privacy.html">{t["privacy"]}</a><a href="/terms.html">{t["terms"]}</a></div></div>'
            f'<p class="copy">© 2026 Oss! Squad</p></footer><div class="pbar"><a class="sbtn" href="/?play">{t["play"]}</a></div>')
    head = (f'<!DOCTYPE html><html lang="{t["lang"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="index,follow">'
            f'<link rel="canonical" href="__SITE__{me.lstrip("/")}"><link rel="alternate" hreflang="{t["lang"]}" href="__SITE__{me.lstrip("/")}"><link rel="alternate" hreflang="{T[o]["lang"]}" href="__SITE__{other.lstrip("/")}">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Oss! Squad"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
            f'<meta property="og:image" content="{OG}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{OG}">'
            f'<meta name="theme-color" content="#1c1432"><link rel="icon" href="https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/04e8362a-99da-41d3-804b-62b663677540.png"><link rel="apple-touch-icon" href="https://d2ol7oe51mr4n9.cloudfront.net/user_3EmROCl8evT8aLsxpJaXd5oq6pI/31326184-0326-42d9-b5de-885b589bde64.png">'
            f'<link rel="stylesheet" href="/site.css"><style>{CSS}</style></head><body>')
    return head + nav + f'<main class="pg">{cr}{body}</main>' + foot + '</body></html>'

def write(rel, txt):
    p = os.path.join(OUT, rel.lstrip('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(txt)

def img(k): return CDN + IMG[k] + '.webp'

def build(L):
    t = T[L]; pre = t['pre']
    # crew index
    cards = ''.join(f'<a class="cc" style="--c:{CREW[k]["col"]}" href="{pre}/heroes/{k}/"><img src="{img(k)}" alt="{esc(CREW[k][L][0])}" width="112" height="112" loading="lazy"><b>{esc(CREW[k][L][0])}</b><span>{CREW[k]["ico"]} {esc(CREW[k][L][1])}</span></a>' for k in ORDER)
    body = f'<section class="ph"><h1>{esc(t["crew_t"])}</h1><p>{esc(t["crew_h"])}</p></section><div class="cgrid">{cards}</div><div class="ctab"><a class="bigbtn" href="/?play">{t["play"]}</a><p class="free">{t["free"]}</p></div>'
    write(f'{pre}/heroes/index.html', page(L, '/heroes/', t['crew_t'] + ' · Oss! Squad', t['crew_d'], body, crumbs=[(t['home'], '/'), (t['crew'], None)]))
    # each grappler
    for k in ORDER:
        c = CREW[k]; n, role, sk, skd, pas, blurb, tip = c[L]
        others = ''.join(f'<a href="{pre}/heroes/{o}/"><img src="{img(o)}" alt="" width="36" height="36" loading="lazy">{esc(CREW[o][L][0])}</a>' for o in ORDER if o != k)
        body = (f'<section class="hero" style="--c:{c["col"]}"><img src="{img(k)}" alt="{esc(n)}" width="200" height="200"><div class="ph"><h1>{c["ico"]} {esc(n)}</h1><p>{esc(blurb)}</p></div></section>'
                f'<div class="facts"><div><h3>{t["role"]}</h3>{esc(role)}</div><div><h3>{t["hp"]}</h3>{c["hp"]}</div><div><h3>{t["skill"]}</h3><b>{esc(sk)}</b><br>{esc(skd)}</div><div><h3>{t["passive"]}</h3>{esc(pas)}</div><div><h3>💡 {t["tip"]}</h3>{esc(tip)}</div></div>'
                f'<h2>{t["meet"]}</h2><div class="mini">{others}</div><div class="ctab"><a class="bigbtn" href="/?play">{t["play"]}</a></div>')
        title = f'{n} ({role}) · Oss! Squad'
        write(f'{pre}/heroes/{k}/index.html', page(L, f'/heroes/{k}/', title, f'{blurb} {skd}', body, crumbs=[(t['home'], '/'), (t['crew'], f'{pre}/heroes/'), (n, None)]))
    # how to play
    st = ''.join(f'<section class="stp" id="s{i+1}"><div class="n">{i+1}</div><div><h2>{ic} {esc(h)}</h2><p>{p}</p><p class="tip">💡 {esc(tp)}</p></div></section>' for i, (ic, h, p, tp) in enumerate(STEPS[L]))
    fq = ''.join(f'<details class="qa"{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i, (q, a) in enumerate(FAQ[L]))
    body = f'<section class="ph"><h1>{esc(t["how"])}</h1><p>{esc(t["how_h"])}</p></section>{st}<section id="faq"><h2>❓ {t["faq"]}</h2>{fq}</section><div class="ctab"><a class="bigbtn" href="/?play">{t["play"]}</a><p class="free">{t["free"]}</p></div>'
    write(f'{pre}/how-to-play/index.html', page(L, '/how-to-play/', t['how_t'], t['how_d'], body, crumbs=[(t['home'], '/'), (t['how'], None)]))

LEGAL = {
 'privacy.html': ('Privacy', '<h1>Privacy</h1><p>Oss! Squad is a free browser game. We do not ask for your name, email or any account.</p><h2>What is stored</h2><p>Your progress (unlocked grapplers, coins, belts, settings) is saved on your own device using your browser’s local storage. If you use Cloud Save, a copy of that progress is stored under a random code so you can load it on another device. It contains no personal information.</p><h2>Ads and tracking</h2><p>There are no ads, no in-game purchases and no third-party tracking or advertising cookies.</p><h2>Kids</h2><p>The game has no chat and no way to contact other players, and it does not collect personal information from anyone, including children.</p><h2>Contact</h2><p>Questions about privacy can be sent to the team that runs this site.</p>'),
 'terms.html': ('Terms', '<h1>Terms of use</h1><p>Oss! Squad is provided free, as is, for personal entertainment.</p><h2>Fair play</h2><p>Please don’t try to break, overload or copy the game or its art.</p><h2>Characters</h2><p>All characters, champions and names in the game are fictional parodies. Any resemblance to real athletes is meant as a friendly tribute, not an endorsement.</p><h2>Changes</h2><p>The game may change or be updated at any time, and saved progress is kept on a best-effort basis.</p>'),
 '404.html': ('Not found', '<h1>Oops, wrong mat!</h1><p>This page tapped out. Head back and start a run.</p><p><a class="bigbtn" href="/">▶ Back to the gym</a></p>'),
}

if __name__ == '__main__':
    for L in ('en', 'pt'): build(L)
    for f, (ttl, body) in LEGAL.items():
        write(f, page('en', '/' + f, ttl + ' · Oss! Squad', ttl + ' for Oss! Squad, a free jiu-jitsu browser game.', f'<section class="legal">{body}</section>', alt_path='/' + f))
    print('pages written to', os.path.abspath(OUT))
