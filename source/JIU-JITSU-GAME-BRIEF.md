# Jiu-Jitsu Conga Game: Project Brief

**Working title:** TBD (shortlist: *Oss! Squad*, *Tatame Heroes*, *Mat Conga*, *Guard Party*). Pick one before buying a domain.
**Owner:** Zac Lamb
**Started:** Nov 24, 2026
**Base:** a replica of *Everlight Heroes* (everlightheroes.com, v1.57.0), reskinned for jiu-jitsu and grappling.

---

## 1. What this is

A copy of the Everlight Heroes game with a grappling theme. The gameplay and systems stay the same. Everything you see and read changes: classes, enemies, bosses, story, art, sound and the website.

It is a **fully standalone game and brand**, with its own world, story, domain, saves and codebase. Everlight Heroes stays as it is, and fixes there are not automatically copied here. It is also not tied to the open-world jiu-jitsu RPG.

**One-line pitch:** *A dark "Master Spell" has taken control of the world's greatest grapplers. Lead your crew of wrestlers, judokas, jiu-jiteros and coaches academy by academy to break the spell and free the champions.*

**Audience:** the jiu-jitsu, grappling and MMA community. Fans of the sport should feel the in-jokes; non-grapplers should still enjoy it as an arcade roguelite.

---

## 2. Story

- **The Master Spell:** a cursed technique scroll (or belt) that mind-controls whoever wins with it. The best grapplers in the world have fallen under it one by one.
- **The villain:** an original villain who stole the spell (name TBD), working through a shadowy fight league of its own. The game has its own world; it does **not** reuse Liga Ouro or the open-world game's lore.
- **The heroes:** a scrappy crew from a small academy who are immune because they "train for the love of it".
- **Structure:** academies replace dungeon floors. Each region ends with a freed champion (boss). The finale takes place at the "World Grand Prix".
- **Chapters:** keep the Everlight story-chapter system (illustrated slides with narration, played after bosses), with new art and script.

### ⚠️ Rule: no real athletes without permission
Do **not** use real names or recognizable likenesses (Gordon Ryan, Craig Jones, Marcelo Garcia, etc.) unless the athlete agrees. It's a right-of-publicity legal risk, app stores reject it, and showing someone as a mind-controlled villain makes it worse. Get a lawyer's quick check before launch.

**Plan:** build with **original champions inspired by fighting styles**, then pitch real athletes on licensed "guest boss" cameos once the game is playable. A real cameo is a strong marketing hook.

Example original champions:

| Boss | Style |
|---|---|
| The Pressure King | Smothering passer, crushes your line from top |
| The Leglock Trickster | Pulls you into leg entanglements, spins and traps |
| The Butterfly Master | Sweeps and back takes, untouchable from guard |
| The Gi Grandmaster | Lapel and collar chokes, slow and deadly |
| The Iron Sambist | Explosive throws and leglocks |
| The Olympic Wrestler | Double legs that knock the whole line back |
| The Masked Champion (final) | Wields the Master Spell itself |

---

## 3. Classes (7, replacing Everlight's 7)

Each class keeps the gameplay role of the Everlight hero it replaces, so the balance carries over.

### Starting classes and unlocks

New players start with **3 classes: Wrestler, Judoka and Jiu-jitero**. The other 4 are locked and earned. This is a code change from Everlight, which starts with Knight, Archer and Mage.

| Class | How it unlocks (whichever comes first) |
|---|---|
| Wrestler, Judoka, Jiu-jitero | Unlocked from the start |
| **Sambo** | Free the champion of region 1, **or** buy it in the Academy for 400 mat fees |
| **Coach** | Free the champion of region 2, **or** 500 mat fees |
| **Athlete** | Free the champion of region 3, **or** 700 mat fees |
| **7th class** | Free the champion of region 4, **or** 1,000 mat fees |

Rules:
- A locked class **never appears on the mat** as a recruit. Unlocking one adds it to the recruit pool and to the starting-crew picker.
- Unlocking shows a celebration card ("Sambo joined the academy!") with the class's signature move.
- **Starting crew slots:** the run starts with 3 crew slots (as Everlight). Extra starting slots are a permanent Legacy upgrade, the same as Everlight's slots perk.
- Prices are starting points; tune them with the balance bot so the 4th unlock lands around the second or third run.

| New class | Replaces | Role | Signature idea |
|---|---|---|---|
| **Wrestler** | Knight | Front-line tank | Takedowns, high HP, protects the line |
| **Judoka** | Archer | Reach / knockback | Throws that fling enemies away |
| **Sambo** | Mage | Area damage | Explosive throw-into-leglock bursts |
| **Coach** | Cleric | Healer / support | Corner advice heals; "water break" |
| **Jiu-jitero** | Rogue | Crits / finisher | Back takes and submissions on weakened enemies |
| **Athlete** | Bard | Team buffs | Conditioning aura: speed and stamina for the line |
| **7th: TBD** | Necromancer | Summoner | Suggested: **Academy Owner (Mestre)**, who calls in students to fight beside you. Alternatives: Luta Livre, Catch Wrestler, MMA Fighter |

---

## 4. Everything else to reskin

| Everlight system | Grappling version |
|---|---|
| Banners (recruit heroes) | Teammates waiting on the mat ("joins your crew") |
| Monsters | Spell-bound students by belt: white → blue → purple → brown, plus tough "elite" rivals |
| Bosses | Freed champions (table above) |
| Biomes (9) | Garage gym, college wrestling room, judo dojo, Rio academy, sambo hall, MMA cage, ADCC-style arena, etc. |
| Floor traps (spikes, lava, water, ice, ink…) | Slippery sweat puddles, mat burns, tangled ropes, weights, spilled water, broken tatami… |
| NOVA ultimate | Team "OSS!" (all-out team scramble) |
| Gear (weapons, armor, charms) | Gi, rash guard, belt, mouthguard, knee pads, tape (stat gear, no power creep) |
| Gold / Camp | Mat fees / Academy upgrades |
| Potions | Water, electrolytes, ice bath, coffee, honey (same effects) |
| Daily quests, trophies, codex | Same systems, new names and icons |
| Kids Mode | Keep: kids' jiu-jitsu classes are a real audience |

---

## 5. What stays the same (don't redesign)

- The conga-line movement, recruiting, star-ups, upgrade cards, paths, gear and Camp system.
- Difficulty modes (Kids / Easy / Normal / Hard), pack spawns and the floor-difficulty ramp.
- Daily quests (cloud-synced, merged progress), the Trophy Hall, the Codex, reviews and cloud save codes.
- Clean combat settings: aggregated damage numbers, calm effects, characters drawn at 90% size.
- The simplified main menu: Continue / New run / Modes, and the 5-icon dock.
- English + Portuguese from day one (keep Kids Mode).

### Rules carried over from Everlight
- Heroes should **never feel overpowered**; clearing a level should feel earned.
- **No hero position swapping**; party and gear changes only between levels.
- Rerolls are **random only** (players never pick).
- **Original art only**; no copied characters or logos.
- **Ask Zac before spending Higgs credits** (case by case).
- Never enter card or payment details; Zac handles purchases and sign-ins.
- Test on a hidden build first; push live only when Zac says so.

---

## 6. Technical starting point

The attached **`everlight-source.zip`** holds the full Everlight source. **`everlight-game.html`** is the finished single-file game (it runs in any browser).

| File | What it is |
|---|---|
| `story/index_tpl.html` | The whole game (template). All gameplay, UI and drawing live here |
| `story/make_game.py` | Builds the template + story/translation JSON into `game2/index.html` |
| `story/pt.json` | Portuguese translations (keyed by English text) |
| `story/story.json`, `story_pt.json`, `times_en.json`, `boss_vo.json` | Story chapters, narration timing, boss voice lines |
| `launch/` | Website assets: service worker `sw.js` (bump the cache version every release), manifest, icons, CSS |
| `pages/gen.py` | Generates the SEO site pages (heroes, how-to-play, sitemap) |
| `build.py` | Packages the site into a deploy zip for a given domain |
| `sim/bot.js`, `sim/run.py` | Balance bot that auto-plays runs and reports health per floor |
| `clip/rec.js`, `clip/drive.js` | Smooth gameplay-video recorder (fixed 30 fps) for trailers and social clips |

**Paths:** the scripts use absolute paths (`/home/claude/...`). Update them when unzipping somewhere else.

**Build order:**
1. Edit the template.
2. Run `make_game.py`.
3. Bump `sw.js`.
4. Run `gen.py`.
5. Run `build.py <domain>`.
6. Deploy the zip.

**Before deploying:** open the built game and confirm it loads with no page errors.

**Hosting:** a **new Netlify site** with its own domain (not the Everlight site), plus a new Search Console property.

**Art:** existing art is loaded from Higgs CDN URLs and painted icon sheets (`UISHEETS`). All of it is Everlight-themed and must be replaced with new grappling art: heroes, enemies, bosses, tiles, icons, story slides.

**Cloud saves:** use a **separate save server/database**, or a different key prefix, so this game never mixes with Everlight players' saves.

---

## 7. First milestone: playable demo (about 1 week)

- [ ] Fork the code, rename, give it its own save keys (`localStorage` prefix) and service-worker cache name
- [ ] 3 starting classes reskinned: Wrestler, Judoka, Jiu-jitero (other 4 show as locked)
- [ ] 1 region (Garage Gym), 5 floors, spell-bound white/blue belts
- [ ] 1 boss: The Pressure King
- [ ] Story intro (3–4 slides) explaining the Master Spell
- [ ] New title screen and menu theme
- [ ] Hidden test link only, shared with Zac's jiu-jitsu community for feedback
- [ ] Measure: do people finish floor 5, and do they come back the next day?

**After the demo:** all 7 classes, all regions and bosses, the full story, Portuguese, the website and the launch plan (Steam + mobile + web portals, same as the Everlight business plan).

---

## 8. Open decisions for Zac

1. Final game name and domain.
2. The 7th class (Academy Owner, Luta Livre, Catch, or MMA).
3. The villain's name and look.
4. Art style: same painted fantasy look as Everlight, or a grittier gym style?
5. Approach athletes for guest-boss cameos now, or after the demo?
