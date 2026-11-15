"""Render HIL premium GBP graphics (products 1200x1200, posts 1200x900)."""
import io, json, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cairosvg

import os
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
INK, INK2 = (20, 19, 27), (30, 29, 40)
RED, CREAM, MUTE = (226, 0, 0), (244, 241, 234), (169, 167, 179)

def mix(a, c=None):
    c = c or CREAM
    return tuple(int(c[i]*a + INK2[i]*(1-a)) for i in range(3))

def font(name, size, wght):
    f = ImageFont.truetype(F + name, size)
    try:
        f.set_variation_by_axes([wght])
    except Exception:
        pass
    return f

ICONS = {
 "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
 "rollover": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
 "cone": '<path d="M16.05 10.966a5 2.5 0 0 1-8.1 0"/><path d="m16.923 14.049 4.48 2.04a1 1 0 0 1 .001 1.831l-8.574 3.9a2 2 0 0 1-1.66 0l-8.574-3.9a1 1 0 0 1 0-1.83l4.484-2.04"/><path d="M16.949 14.14a5 2.5 0 1 1-9.9 0L10.063 3.5a2 2 0 0 1 3.874 0z"/><path d="M9.194 6.57a5 2.5 0 0 0 5.61 0"/>',
 "phone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
 "swipe": '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
 "heartcrack": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="m12 13-1-1 2-2-3-3 2-2"/>',
 "moto": '<circle cx="5" cy="17" r="3"/><circle cx="19" cy="17" r="3"/><path d="M5 17h5l3-6h4l2 6"/><path d="M13 11 11 7H8"/><path d="M16 7h3"/>',
 "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
 "pin": '<path d="M20 10c0 5-5.5 10.2-7.4 11.8a1 1 0 0 1-1.2 0C9.5 20.2 4 15 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
 "wineoff": '<path d="M8 22h8"/><path d="M12 15v7"/><path d="M12 15a5 5 0 0 0 5-5c0-2-.5-4-2-8H9c-1.5 4-2 6-2 8a5 5 0 0 0 5 5Z"/><path d="M3 3l18 18"/>',
 "ped": '<circle cx="12" cy="4.5" r="1.6"/><path d="m9 21 3-6.5 3 6.5"/><path d="m6 9 6 2 6-2"/><path d="M12 11v3.5"/>',
 "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
 "bike": '<circle cx="18.5" cy="17.5" r="3.5"/><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="15" cy="5" r="1"/><path d="M12 17.5V14l-3-3 4-3 2 3h2"/>',
 "siren": '<path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M21 12h1"/><path d="M18.5 4.5 18 5"/><path d="M2 12h1"/><path d="M12 2v1"/><path d="m4.929 4.929.707.707"/><path d="M12 12v6"/>',
 "bus": '<path d="M8 6v6"/><path d="M15 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><path d="M9 18h5"/><circle cx="16" cy="18" r="2"/>',
 "anchor": '<path d="M12 22V8"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/><circle cx="12" cy="5" r="3"/>',
 "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 "building": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
 "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
 "chip": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>',
 "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
 "paw": '<circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="20" cy="16" r="2"/><path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.84 1.045Q6.52 17.48 4.46 16.84A3.5 3.5 0 0 1 5.5 10Z"/>',
 "hardhat": '<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/>',
 "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
 "shieldalert": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
 "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
 "package": '<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/><path d="M12 22V12"/><path d="m3.3 7 7.703 4.734a2 2 0 0 0 1.994 0L20.7 7"/>',
 "stetho": '<path d="M11 2v2"/><path d="M5 2v2"/><path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/><path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/>',
 "hospital": '<path d="M12 6v4"/><path d="M14 14h-4"/><path d="M14 18h-4"/><path d="M14 8h-4"/><path d="M18 12h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2"/><path d="M18 22V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v18"/>',
 "heartpulse": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
 "book": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
}

def icon_img(key, px):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 24 24" fill="none" '
           f'stroke="rgb{CREAM}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[key]}</svg>')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")

def background(w, h, glow_xy):
    img = Image.new("RGB", (w, h), INK)
    px = img.load()
    for y in range(h):
        for x in range(0, w):
            t = max(0.0, min(1.0, (x * 0.6 + y * 0.8) / (w * 0.6 + h * 0.8)))
            px[x, y] = tuple(int(INK2[i] + (INK[i] - INK2[i]) * t) for i in range(3))
    glow = Image.new("L", (w, h), 0)
    gd = ImageDraw.Draw(glow)
    gx, gy = glow_xy
    for r in range(520, 0, -8):
        gd.ellipse([gx - r, gy - r, gx + r, gy + r], fill=int(60 * (1 - r / 520) ** 1.6))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    red = Image.new("RGB", (w, h), RED)
    return Image.composite(red, img, glow)

def text_center(d, cx, y, s, f, fill, spacing=0):
    if spacing:
        widths = [d.textlength(ch, font=f) + spacing for ch in s]
        x = cx - (sum(widths) - spacing) / 2
        for ch, wd in zip(s, widths):
            d.text((x, y), ch, font=f, fill=fill)
            x += wd
    else:
        d.text((cx - d.textlength(s, font=f) / 2, y), s, font=f, fill=fill)

def fit_lines(d, lines, maxw, start, wght=800):
    size = start
    while size > 60:
        f = font("Alegreya.ttf", size, wght)
        if all(d.textlength(l, font=f) <= maxw for l in lines):
            return f, size
        size -= 4
    return font("Alegreya.ttf", size, wght), size

def product(title, icon, eyebrow, sub, out):
    W = H = 1200
    img = background(W, H, (600, -40)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([80, 80, 1120, 1120], radius=8, outline=mix(0.14), width=2)
    lines = title.split("\n")
    ft, size = fit_lines(d, lines, 880, 132)
    lh = int(size * 0.98)
    block = 200 + 36 + 34 + 36 + lh * len(lines) + 36 + 6 + 36 + 46
    y = (H - block) // 2 - 20
    # badge
    badge = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.ellipse([1, 1, 199, 199], fill=(*RED, 31), outline=(*RED, 150), width=2)
    ic = icon_img(icon, 104)
    badge.alpha_composite(ic, (48, 48))
    img.alpha_composite(badge, ((W - 200) // 2, y))
    y += 200 + 36
    text_center(d, W / 2, y, eyebrow, font("WorkSans.ttf", 30, 600), MUTE, spacing=6)
    y += 34 + 36
    last_bottom = y
    for l in lines:
        text_center(d, W / 2, y, l, ft, CREAM)
        last_bottom = y + d.textbbox((0, 0), "Ag", font=ft)[3]
        y += lh
    y = last_bottom + 34
    d.rectangle([W / 2 - 60, y, W / 2 + 60, y + 6], fill=RED)
    y += 6 + 36
    text_center(d, W / 2, y, sub, font("AlegreyaItalic.ttf", 40, 400), mix(0.82))
    text_center(d, W / 2, 1010, "HOWARD INJURY LAW", font("WorkSans.ttf", 24, 600), mix(0.5), spacing=7)
    img.convert("RGB").save(out, quality=92)

def wrap(d, text, f, maxw):
    words, lines, cur = text.replace('Las Vegas', 'Las\u00a0Vegas').split(' '), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

def blog_post(eyebrow, title, teaser, icon, out, cta=None):
    """Blog/update post 1200x900. Content block is vertically centered and kept
    inside y=150..750 so it survives both the top crop and the center crop
    (~1200x690) that the GBP Overview card uses."""
    W, H = 1200, 900
    img = background(W, H, (1050, -60)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([60, 60, 1140, 840], radius=8, outline=mix(0.12), width=2)
    ef = font("WorkSans.ttf", 24, 600)
    bf = font("Alegreya.ttf", 34, 400)
    cf = font("WorkSans.ttf", 28, 700)
    cta = cta or "READ THE FULL GUIDE"
    # Area posts are short: bigger title, block centered in the band that
    # survives the GBP top crop (y=0..690) and the center crop (y=105..795).
    area = cta.startswith("SEE HOW")
    size = 84 if area else 66
    while True:
        tf = font("Alegreya.ttf", size, 800)
        lines = wrap(d, title, tf, 800)
        if len(lines) <= (2 if area else 3) or size <= 56:
            break
        size -= 4
    tlines = [l for part in teaser.split("\n") for l in wrap(d, part, bf, 960)][:2]
    lh = int(size * 1.05)
    block = 52 + 28 + lh * len(lines) + 18 + 6 + 30 + 48 * len(tlines) + 32 + 72
    y = max(120, 400 - block // 2) if area else max(150, (H - block) // 2)
    # eyebrow pill
    tw = sum(d.textlength(ch, font=ef) + 4 for ch in eyebrow)
    d.rounded_rectangle([110, y, 110 + tw + 44, y + 52], radius=26, fill=mix(0.16, RED), outline=mix(0.75, RED), width=2)
    x = 132
    for ch in eyebrow:
        d.text((x, y + 11), ch, font=ef, fill=CREAM); x += d.textlength(ch, font=ef) + 4
    y += 52 + 28
    for l in lines:
        d.text((110, y), l, font=tf, fill=CREAM); y += lh
    y += 18
    d.rectangle([110, y, 250, y + 6], fill=RED)
    y += 6 + 30
    for l in tlines:
        d.text((110, y), l, font=bf, fill=mix(0.92)); y += 48
    y += 32
    label = cta + "   →"
    cw = sum(d.textlength(ch, font=cf) + 5 for ch in label)
    d.rounded_rectangle([110, y, 110 + cw + 60, y + 72], radius=36, fill=RED)
    x = 140
    for ch in label:
        d.text((x, y + 19), ch, font=cf, fill=(255, 255, 255)); x += d.textlength(ch, font=cf) + 5
    badge = Image.new("RGBA", (112, 112), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.ellipse([1, 1, 111, 111], fill=(*RED, 31), outline=(*RED, 150), width=2)
    badge.alpha_composite(icon_img(icon, 58), (27, 27))
    img.alpha_composite(badge, (978, y - 20))
    img.convert("RGB").save(out, quality=92)
    return y + 72

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    for p in cfg.get("products", []):
        product(p["title"], p["icon"], p.get("eyebrow", "LAS VEGAS INJURY LAWYER"),
                p.get("sub", "Free case review  ·  Available 24/7"), p["out"])
    for b in cfg.get("posts", []):
        blog_post(b["eyebrow"], b["title"], b["teaser"], b["icon"], b["out"], b.get("cta", "READ THE FULL GUIDE"))
    print("done")
