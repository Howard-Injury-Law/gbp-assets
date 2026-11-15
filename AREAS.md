# HIL GBP Area Post Automation — Runbook

Runs **Saturdays**. One run = one "Serving [Area]" GBP post for the next area in the queue below.
Owner: Storm Media (Julz) for Howard Injury Law. Repo is PUBLIC — never commit secrets or client data.

Follow every **Standing rule** and the **IDs**, render, upload and publish mechanics in `AUTOMATION.md`. This file only changes *what* gets posted.

## Picking the area
Go down the queue top to bottom. Skip any area that already has an `(area)` row in `POSTED.md` (match on the area name). Post the first one left. When every area is posted, start over at the top with a new angle (different practice focus from the notes column), and log it as `(area, round 2)`.

## Queue (in order)
| # | Area | Page URL | Practice focus / notes |
|---|---|---|---|
| 1 | Henderson | https://www.howardinjurylaw.com/service-areas/henderson-personal-injury-lawyer/ | Car and general injury |
| 2 | Summerlin | https://www.howardinjurylaw.com/service-areas/summerlin-personal-injury-lawyer/ | Car and general injury |
| 3 | North Las Vegas | https://www.howardinjurylaw.com/service-areas/north-las-vegas-personal-injury-lawyer/ | Car, pedestrian |
| 4 | Las Vegas Strip | https://www.howardinjurylaw.com/service-areas/las-vegas-strip-injury-lawyer/ | Casino injury, pedestrian, rideshare, tourists hurt while visiting |
| 5 | Boulder City | https://www.howardinjurylaw.com/service-areas/boulder-city-personal-injury-lawyer/ | Truck and motorcycle |
| 6 | Pahrump | https://www.howardinjurylaw.com/service-areas/pahrump-personal-injury-lawyer/ | Car, truck, wrongful death, rideshare. **Pahrump is in Nye County** — say Nye County (not Clark County) for courts and law enforcement |
| 7 | Laughlin | https://www.howardinjurylaw.com/service-areas/laughlin-personal-injury-lawyer/ | Car, slip and fall, casino injury (slip-and-fall angle points to the casinos); boat on the Colorado River is optional |
| 8 | Reno | https://www.howardinjurylaw.com/service-areas/reno-personal-injury-lawyer/ | Car and general injury |
| 9 | Downtown Las Vegas | https://www.howardinjurylaw.com/service-areas/#downtown | Pedestrian, casino, car |
| 10 | Paradise | https://www.howardinjurylaw.com/service-areas/las-vegas-strip-injury-lawyer/#paradise | Car, casino, pedestrian |
| 11 | Spring Valley | https://www.howardinjurylaw.com/service-areas/#spring-valley | Already posted 2026-11-14 (test) — skip in round 1 |
| 12 | Enterprise | https://www.howardinjurylaw.com/service-areas/#enterprise | Car and general injury |
| 13 | East Las Vegas | https://www.howardinjurylaw.com/service-areas/#east-las-vegas | Car, pedestrian |
| 14 | Mesquite | https://www.howardinjurylaw.com/service-areas/#mesquite | Car, truck (I-15) |
| 15 | Elko | https://www.howardinjurylaw.com/service-areas/#elko | Car, truck |
| 16 | Ely | https://www.howardinjurylaw.com/service-areas/#ely | Car, truck |
| 17 | Beatty | https://www.howardinjurylaw.com/service-areas/#beatty | Car, truck |
| 18 | California | https://www.howardinjurylaw.com/service-areas/california-personal-injury-lawyer/ | **Local counsel wording only** (see below) |
| 19 | Arizona | https://www.howardinjurylaw.com/service-areas/arizona-personal-injury-lawyer/ | **Local counsel wording only** |
| 20 | Colorado | https://www.howardinjurylaw.com/service-areas/colorado-personal-injury-lawyer/ | **Local counsel wording only** |

## Copy rules for area posts
- ≤ 1,000 characters. Hook ("Injured in Henderson?") → 2–4 plain-language points tied to the practice focus → how HIL helps → "Free case review, 24/7: (702) 331-5722."
- Only facts you are sure of. No invented crash statistics, no named intersections or "dangerous road" claims unless the area page itself says so (read the page via WPVibe `rest_api` GET `/wp/v2/pages?slug=<slug>` when the URL has its own slug; anchor-only areas use the general `service-areas` page).
- **California, Arizona, Colorado:** never say "California/Arizona/Colorado personal injury lawyer" or imply HIL attorneys are licensed there. Use: "Howard Injury Law works with local counsel in California to help people injured there." Same for Arizona and Colorado. Title example: "Hurt in California? We Work With Local Counsel."
- Workers' comp only as third-party claims. No promised results.

## Image (same approved v4 design)
job.json entry: `{"eyebrow":"<AREA>  ·  SERVING YOUR COMMUNITY","title":"Injured in <Area>?","teaser":"<1–2 sentences, ≤ 2 lines>","icon":"pin","cta":"SEE HOW WE HELP LOCALLY","out":"../images/posts/gbp-area-<area-slug>.png"}`
Look at the PNG before using it.

## Publish + log
- Upload to WordPress with alt text: `Injured in <Area>? Howard Injury Law personal injury help serving <Area>, Nevada` (for CA/AZ/CO: `Howard Injury Law working with local counsel in <State>`).
- `create_local_post` with cta_type `LEARN_MORE`, cta_url = `<page URL>` + `?utm_source=google&utm_medium=organic&utm_campaign=gbp_area&utm_content=<area-slug>` (put the query string **before** any `#anchor`).
- There is no sheet checkbox for areas. Log `| <date> | (area) | - | Injured in <Area>? | <post id> |` in `POSTED.md` and push.
