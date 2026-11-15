# HIL GBP Blog Post Automation — Runbook

Runs Mon / Wed / Fri. One run = one GBP post for the next blog not yet added to GBP.
Saturday area posts follow `AREAS.md` (same mechanics, different queue).
Owner: Storm Media (Julz) for Howard Injury Law. Repo is PUBLIC — never commit secrets, client data, or anything not meant to be public.

## Standing rules (non-negotiable)
- Never reply to reviews. This runbook only creates blog posts.
- Workers' comp is only ever framed as **third-party personal injury claims**.
- No guaranteed outcomes, no "best", no dollar figures except Nevada statutory facts. Educational tone.
- Every image gets SEO alt text when uploaded to WordPress.
- If any step fails, STOP before publishing and report what failed. Never publish a post without its image, link and correct copy.
- Never post the same blog twice: re-check the sheet checkbox AND the last 20 GBP posts' CTA URLs before publishing.

## IDs
- GBP location (Windsor.ai `google_my_business`): account `locations/11343912957460750355`
- Google Sheet: `1vF4sepiiuv4npOtPjAkc6m5CGqDGq6PP6cozBi53qtc` ("2026 HIL Content-Focused Keywords + All Pages")
  - Each practice-area tab has a header row containing `SUPPORTING BLOG CONTENT | URLs | Submit To GSC | Links/Images/YT | Title/Meta | Categorized | Added To GBP`. Blog title = column A, URL = column B, checkbox = column G (`Added To GBP`).
- WordPress: `https://www.howardinjurylaw.com` (WPVibe)
- Raw image base: `https://raw.githubusercontent.com/Howard-Injury-Law/gbp-assets/main/images/posts/`

## Tab priority (money-page order)
1. 🟡 Car Accidents → 2. 🟢 Motor Vehicle → 3. 🟡 Fatal Crash → 4. 🟡 Truck Accidents → 5. 🟡 Motorcycle Accidents → 6. 🟡 Rideshare and Taxi → 7. 🟡 Pedestrian Accidents → 8. 🟡 Drunk Driving → 9. 🟡 Hit and Run → 10. 🟡 Casino Injury → 11. 🟡 Slip and Fall → 12. 🟢 Premises Liability → 13. 🟢 Wrongful Death → 14. 🟢 Catastrophic Injury → 15. 🟢 Medical Malpractice → remaining tabs in sheet order, then 🔵 General Blogs.
Within a tab, go top to bottom. Pick the first row with a URL whose `Added To GBP` is FALSE/empty.

## Steps
1. **Pick the blog** from the sheet (Google Sheets `get_values` on the tab). Note tab, row, title, URL.
2. **Read the blog** through WordPress (WebFetch can't reach the site): WPVibe `rest_api` GET `/wp/v2/posts` with query `{slug: <last path segment of the URL>, per_page: 1}` and fields `id,title,content,link`. If no post comes back or it's off-topic, skip the row, note it, and move to the next one.
3. **Write the post copy** (≤ 1,200 chars): question/hook line → 3–5 plain-language takeaways (bullets "•") accurate to Nevada law and to the blog → "Our full guide walks through…" → "Hurt in a crash? Howard Injury Law offers a free case review, 24/7: (702) 331-5722." Adapt the closer to the topic (premises, medical, etc.).
4. **Render the image** with the approved v4 design:
   ```
   cd kit && python3 render.py job.json
   ```
   job.json: `{"posts":[{"eyebrow":"<CLUSTER>  ·  LAS VEGAS GUIDE","title":"<blog title, title case, ≤ 3 lines>","teaser":"<≤ 2 lines, 1–2 sentences>","icon":"<icon key>","out":"../images/posts/gbp-<slug>.png"}]}`
   - Icon keys: car, rollover, cone, phone, swipe, heartcrack, moto, truck, pin, wineoff, ped, zap, bike, siren, bus, anchor, wrench, building, alert, chip, utensils, paw, hardhat, heart, shieldalert, home, activity, package, stetho, hospital, heartpulse, book.
   - Requires Pillow + cairosvg (`pip install pillow cairosvg`).
   - Look at the rendered PNG before continuing (title not clipped, ≤ 3 lines).
5. **Commit + push** the PNG to `main` (message: `GBP post: <slug>`). Wait until the raw URL returns 200.
6. **Upload to WordPress**: WPVibe `upload_media` with url = raw GitHub URL, title = `<Blog Title> - Howard Injury Law`, alt_text = descriptive SEO alt (e.g. "<blog question> — Howard Injury Law Las Vegas guide").
7. **Publish to GBP**: Windsor `execute_action` → `create_local_post` with summary, photo_url = the WordPress media URL, cta_type `LEARN_MORE`, cta_url = `<blog URL>?utm_source=google&utm_medium=organic&utm_campaign=gbp_post&utm_content=<slug>`.
8. **Tick the sheet**: set column G of that row to TRUE (`update_values`, value `true`).
9. **Log** a line to `POSTED.md` (date, tab, row, title, GBP post id) and push.
10. **Report** to Julz: title, link, and that the box is ticked.

## Design spec (approved, v4)
1200×900. Dark ink gradient (#1E1D28 → #14131B), subtle red glow top-right, thin frame. Content block vertically centered (survives GBP Overview top and center crops): eyebrow pill → Alegreya ExtraBold title → red rule → larger gray teaser → big red CTA pill ("READ THE FULL GUIDE →"; area posts: "SEE HOW WE HELP LOCALLY →") with icon badge to the right. No footer wordmark/phone.
