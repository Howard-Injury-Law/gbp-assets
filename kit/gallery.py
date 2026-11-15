"""HIL GBP gallery graphics (1200x1200), same premium dark system as the product cards.
Usage: python3 gallery.py gallery.json
Card types: statement (title + sub + optional phone pill), stats (3 columns), list (2-column list).
"""
import json, sys
from PIL import Image, ImageDraw
import render as R
from render import font, mix, text_center, icon_img, background, RED, CREAM, MUTE

R.ICONS.update({
    "shieldcheck": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "msg": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "dollar": '<path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
})

W = H = 1200
PHONE = "(702) 331-5722"


def badge(img, key, x, y, size=150):
    b = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bd = ImageDraw.Draw(b)
    bd.ellipse([1, 1, size - 1, size - 1], fill=(*RED, 31), outline=(*RED, 150), width=2)
    ic = icon_img(key, int(size * 0.5))
    b.alpha_composite(ic, (int(size * 0.25), int(size * 0.25)))
    img.alpha_composite(b, (int(x), int(y)))


def title_block(d, lines, y, start=118, maxw=900):
    ft, size = R.fit_lines(d, lines, maxw, start)
    lh = int(size * 1.0)
    bottom = y
    for l in lines:
        text_center(d, W / 2, y, l, ft, CREAM)
        bottom = y + d.textbbox((0, 0), "Agjy", font=ft)[3]
        y += lh
    return bottom + 30


def card(c, out):
    base = background(W, H, (600, -40)).convert("RGBA")
    ImageDraw.Draw(base).rounded_rectangle([80, 80, 1120, 1120], radius=8, outline=mix(0.14), width=2)
    img = Image.new("RGBA", (W, 2000), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    kind = c.get("type", "statement")
    lines = c["title"].split("\n")
    ef = font("WorkSans.ttf", 28, 600)
    sf = font("AlegreyaItalic.ttf", 40, 400)

    # measure block height so the whole card is vertically centered
    _, tsize = R.fit_lines(d, lines, 900, c.get("size", 118))
    th = int(tsize * 1.0) * len(lines) + int(tsize * 0.18)
    body = {"statement": 0, "stats": 250, "list": 0}[kind]
    if kind == "list":
        body = 62 * ((len(c["items"]) + 1) // 2) + 10
    sub_h = 60 * len(c.get("sub", "").split("\n")) if c.get("sub") else 0
    pill_h = 110 if c.get("pill") else 0
    foot_h = 60 if c.get("foot") else 0
    icon_h = 150 + 40 if c.get("icon") else 0
    block = icon_h + 34 + 40 + th + 34 + 6 + 40 + sub_h + body + pill_h + foot_h
    y = 0

    if c.get("icon"):
        badge(img, c["icon"], (W - 150) / 2, y)
        y += 150 + 40
    text_center(d, W / 2, y, c["eyebrow"], ef, MUTE, spacing=6)
    y += 34 + 40
    y = title_block(d, lines, y, c.get("size", 118))
    d.rectangle([W / 2 - 60, y, W / 2 + 60, y + 6], fill=RED)
    y += 6 + 40

    if c.get("sub"):
        for s in c["sub"].split("\n"):
            text_center(d, W / 2, y, s, sf, mix(0.85))
            y += 60
        y += 10

    if kind == "stats":
        cols = c["stats"]
        cw = 300
        x0 = W / 2 - cw * len(cols) / 2
        nf = font("Alegreya.ttf", 92, 800)
        lf = font("WorkSans.ttf", 24, 600)
        for i, (num, label) in enumerate(cols):
            cx = x0 + cw * i + cw / 2
            if i:
                d.line([x0 + cw * i, y + 10, x0 + cw * i, y + 190], fill=mix(0.2), width=2)
            if num.startswith("icon:"):
                b = icon_img(num[5:], 92)
                img.alpha_composite(b, (int(cx - 46), int(y + 8)))
            else:
                text_center(d, cx, y, num, nf, RED if c.get("red_nums", True) else CREAM)
            ly = y + 124
            for part in label.split("\n"):
                text_center(d, cx, ly, part.upper(), lf, mix(0.8), spacing=3)
                ly += 34
        y += 250

    if kind == "list":
        lf = font("Alegreya.ttf", c.get("list_size", 40), 500)
        items = c["items"]
        half = (len(items) + 1) // 2
        y += c.get("list_gap", 0)
        cols_x = c.get("cols_x", (200, 640))
        for col, xs in ((items[:half], cols_x[0]), (items[half:], cols_x[1])):
            yy = y
            for it in col:
                d.ellipse([xs - 22, yy + 18, xs - 10, yy + 30], fill=RED)
                d.text((xs + 4, yy), it, font=lf, fill=mix(0.92))
                yy += 62
        y += 62 * half + 10

    if c.get("pill"):
        pf = font("WorkSans.ttf", 40, 700)
        label = c["pill"]
        tw = sum(d.textlength(ch, font=pf) + 3 for ch in label)
        x1 = W / 2 - tw / 2 - 48
        d.rounded_rectangle([x1, y + 10, W / 2 + tw / 2 + 48, y + 96], radius=43, fill=RED)
        x = W / 2 - tw / 2
        for ch in label:
            d.text((x, y + 30), ch, font=pf, fill=(255, 255, 255)); x += d.textlength(ch, font=pf) + 3
        y += pill_h

    if c.get("foot"):
        text_center(d, W / 2, y + 6, c["foot"], font("Alegreya.ttf", 32, 400), mix(0.62))
        y += 50
    content_h = y
    top = (80 + 1000 - content_h) // 2 + 20   # center between frame top and footer
    base.alpha_composite(img.crop((0, 0, W, content_h)), (0, top))
    img = base
    d = ImageDraw.Draw(img)
    text_center(d, W / 2, 1036, "HOWARD INJURY LAW  ·  " + PHONE, font("WorkSans.ttf", 26, 600), mix(0.62), spacing=5)
    img.convert("RGB").save(out, quality=92)


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    for c in cfg["cards"]:
        card(c, c["out"])
    print("done", len(cfg["cards"]))
