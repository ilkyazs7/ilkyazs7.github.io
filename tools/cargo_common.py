"""Convert Cargo page JSON into Jekyll markdown files with image placeholders."""
import json, re, os, sys, csv, html
from bs4 import BeautifulSoup, NavigableString, Tag

SRC = os.environ.get("CARGO_SRC", "cargo")
P = lambda pid: json.load(open(f"{SRC}/pages/{pid}.json"))

# ---------------------------------------------------------------- page plan
# id: (slug, number, category, order, label-override)
PLAN = {
    "N3908447647": ("00-sensing-glove", "00", "Soft Intelligence: Embodied Mind", 0),
    "K1002071343": ("01-tactile-intelligence", "01", "Soft Intelligence: Embodied Mind", 1),
    "G1486678012": ("02-human-knitting", "02", "Soft Intelligence: Embodied Mind", 2),
    "F4201063030": ("03-cnc-knitting", "03", "Soft Intelligence: Embodied Mind", 3),
    "Q2663307658": ("04-speed-of-sound", "04", "Situated Machines: Measurement Instruments", 4),
    "K1468495737": ("11-spring-force-mechanics", "11", "Situated Machines: Measurement Instruments", 5),
    "I0787905088": ("05-optimization-for-digital-fabrication", "05", "Digital to Physical: Advanced Fabrication", 6),
    "B3365839854": ("07-machines-of-making", "07", "Digital to Physical: Advanced Fabrication", 7),
    "Z3616925775": ("08-perception", "08", "Machine", 8),
    "F3779968120": ("09-capturing", "09", "Machine", 9),
    "N0046182474": ("10-learning", "10", "Machine", 10),
    "P1773310485": ("12-retro-fitting", "12", "Leftover Project", 11),
    "E3406970679": ("13-the-alphabet-song", "13", "Leftover Project", 12),
    "J0207791252": ("14-plotted-leftovers", "14", "Leftover Project", 13),
    "M1916100687": ("zap", "", "Exhibition", 20),
    "S4115486832": ("architecture-is-art", "", "Exhibition", 21),
    # machines of making sub-projects (freeform sort order)
    "E0285821388": ("precise-fit-3-axis-cnc", "", "Machines of Making", 30),
    "O2885552224": ("light-leak-zund-knife-cutter", "", "Machines of Making", 31),
    "Z3708164254": ("two-does-not-equal-to-one-waterjet", "", "Machines of Making", 32),
    "H1079254261": ("wall-with-a-hole-robotic-3dp", "", "Machines of Making", 33),
    "W3261113664": ("morphbox-hands", "", "Machines of Making", 34),
}
PARENT = {k: "07-machines-of-making" for k in
          ["E0285821388", "O2885552224", "Z3708164254", "H1079254261", "W3261113664"]}

# hover-index preview images taken from the Cargo homepage (hash per page)
home_html = P("R0209283200")["content"]
HOVER = {}
for m in re.finditer(r'(?:href="([^"]+)"[^>]*style="--preview:url\(\'([^\']+)\'\)|style="--preview:url\(\'([^\']+)\'\);">\s*<a href="([^"]+)")', home_html):
    href = m.group(1) or m.group(4); url = m.group(2) or m.group(3)
    HOVER.setdefault(href, url)

purl_to_id = {}
for pid in PLAN:
    purl_to_id[P(pid)["purl"]] = pid

def url_for(pid):
    return f"/projects/{PLAN[pid][0]}/"

ICONS = {"pointer-1": "☞", "pointer-2": "☜", "happy-face-1": "☺", "happy-face-2": "☺",
         "sad-face-1": "☹", "snowman": "☃", "leftwards-arrow": "←"}

def slug_file(name):
    base, ext = os.path.splitext(name)
    base = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-") or "image"
    return base + ext.lower()

IMAGE_ROWS = []          # for the CSV / JSON map
IMAGE_MAP = {}           # local path -> info

def register_media(m, slug, used):
    """Return local site path for a Cargo media dict."""
    name = m.get("name") or m.get("display_name") or (m["hash"] + ".jpg")
    fn = slug_file(name)
    key = (slug, m["hash"])
    if key in used:
        return used[key]
    taken = set(used.values())
    path = f"/assets/images/{slug}/{fn}"
    i = 2
    while path in taken:
        b, e = os.path.splitext(fn); path = f"/assets/images/{slug}/{b}-{i}{e}"; i += 1
    used[key] = path
    w, h = m.get("width"), m.get("height")
    is_video = bool(m.get("is_video"))
    orig = f"https://freight.cargo.site/t/original/i/{m['hash']}/{name}"
    big = (w or 0) > 2000 and not is_video and not name.lower().endswith(".gif")
    web = f"https://freight.cargo.site/w/2000/q/85/i/{m['hash']}/{name}" if big else orig
    IMAGE_MAP[path] = {"w": w, "h": h, "video": is_video, "cargo": web}
    IMAGE_ROWS.append({"local_path": path.lstrip("/"), "download_url": web, "original_url": orig,
                       "width": w, "height": h, "type": "video" if is_video else "image",
                       "page": slug})
    return path

# ---------------------------------------------------------------- html -> md
def inline(node, ctx):
    """Inline markdown for a node; <br> becomes '\n'."""
    if isinstance(node, NavigableString):
        if node.__class__.__name__ == "Comment":
            return ""
        return re.sub(r"\s+", " ", str(node))
    if not isinstance(node, Tag):
        return ""
    t = node.name
    if t == "br":
        return "\n"
    if t == "text-icon":
        return ICONS.get(node.get("icon"), "")
    inner = "".join(inline(c, ctx) for c in node.children)
    if t in ("b", "strong"):
        return wrap(inner, "**")
    if t in ("i", "em"):
        return wrap(inner, "*")
    if t == "u":
        return f"<u>{inner.strip()}</u>" if (ctx == "info" and inner.strip()) else inner
    if t == "a":
        href = (node.get("href") or "").strip()
        text = inner
        if not text.strip():
            return ""
        target = map_href(href)
        if target is None:
            return text
        return f"[{text.strip()}]({target})"
    return inner

def wrap(s, mark):
    if not s.strip():
        return s
    lead = s[: len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
    core = s.strip()
    # don't wrap across line breaks: wrap each line separately
    parts = [f"{mark}{p.strip()}{mark}" if p.strip() else "" for p in core.split("\n")]
    return lead + "\n".join(parts) + trail

def map_href(href):
    h = html.unescape(href)
    if h.startswith("mailto:"):
        return None if "erkilic" in h else h
    if re.match(r"https?://", h):
        m = re.match(r"https?://(www\.)?ilkyazs\.com/(.*)", h)
        if not m:
            return h
        h = m.group(2)
    h = h.strip("/")
    if h in ("omnifab", "contact-form", "PASTE_BLOG_LINK_HERE", ""):
        return None
    if h == "[i]":
        return "/"
    if h == "visual-index":
        return "/visual-index/"
    if h in purl_to_id:
        return url_for(purl_to_id[h])
    if h == "machines-of-making":
        return "/projects/07-machines-of-making/"
    return None

class Body:
    def __init__(self, slug, media_by_hash, used):
        self.blocks = []    # list of strings (markdown blocks)
        self.buf = ""       # current inline text
        self.slug = slug; self.media = media_by_hash; self.used = used
        self.marks = []

    def emit(self, s):
        for m in self.marks:
            s = wrap(s, m)
        self.buf += s

    def flush(self):
        text = self.buf
        self.buf = ""
        for para in re.split(r"\n\s*\n", text):
            lines = [l.strip() for l in para.split("\n")]
            lines = [l for l in lines if l and l not in ("**", "*", "****")]
            if lines:
                self.blocks.append("  \n".join(lines))

    def add(self, block):
        self.flush(); self.blocks.append(block)

    def media_md(self, el, small=False):
        h = el.get("hash")
        m = self.media.get(h)
        if not m:
            return None
        if m.get("is_url"):
            return m.get("url")
        path = register_media(m, self.slug, self.used)
        scale = (el.get("scale") or "").rstrip("%")
        if el.get("limit-by") == "fit" and scale and float(scale) <= 50:
            small = True
        if el.get("limit-by") == "width" and scale and float(scale) <= 50:
            small = small  # half-width images arrive in pairs -> row
        title = ' "small"' if small else ""
        return f"![]({path}{title})"

    def walk(self, node, centered=False):
        for c in list(node.children):
            if isinstance(c, NavigableString):
                self.emit(inline(c, None)); continue
            if not isinstance(c, Tag):
                continue
            t = c.name
            cls = c.get("class") or []
            style = (c.get("style") or "").replace(" ", "")
            if t == "media-item":
                md = self.media_md(c)
                if md: self.add(md)
            elif t.startswith("gallery-"):
                items = [self.media_md(x) for x in c.find_all("media-item")]
                items = [i for i in items if i]
                if not items:
                    continue
                cols = c.get("columns")
                if t == "gallery-grid" and cols == "1":
                    for i in items: self.add(i)
                else:
                    # images in one paragraph render as a row
                    self.add(" ".join(items))
            elif t == "column-set":
                for u in c.find_all("column-unit"):
                    self.flush(); self.walk(u); self.flush()
            elif t == "iframe":
                src = c.get("src") or ""
                m = re.search(r"youtube\.com/embed/([\w-]+)", src)
                if m: self.add(f"https://www.youtube.com/watch?v={m.group(1)}")
                elif "vimeo" in src:
                    m = re.search(r"video/(\d+)", src)
                    self.add(f"https://vimeo.com/{m.group(1)}" if m else str(c))
                else:
                    self.add(str(c))
            elif t in ("ul", "ol"):
                items = []
                for n, li in enumerate(c.find_all("li", recursive=False)):
                    txt = re.sub(r"\s+", " ", inline(li, None).replace("\n", " ")).strip()
                    items.append(("1." if t == "ol" else "-") + " " + txt)
                self.add("\n".join(items))
            elif t == "span" and "newsubtitle" in cls and c.find(["media-item"] + [f"gallery-{g}" for g in ("grid","justify","columnized","freeform")]):
                self.walk(c)
            elif t == "span" and "newsubtitle" in cls:
                txt = inline(c, None).replace("\n", " ").strip().strip("*").strip()
                if txt: self.add("### " + txt)
            elif t == "span" and "newindexsub" in cls:
                txt = inline(c, None).replace("\n", " ").strip()
                if txt: self.add("> " + txt)
            elif t == "div" and "text-align:center" in style:
                self.flush()
                self.walk_centered(c)
            elif t == "div":
                self.flush(); self.walk(c); self.flush()
            elif t in ("b", "strong", "i", "em", "span", "small", "u", "a") and c.find(["media-item"] + [f"gallery-{g}" for g in ("grid","justify","columnized","freeform")]):
                # formatting wrapper around block content: descend, keeping its style
                mark = {"b": "**", "strong": "**", "i": "*", "em": "*"}.get(t)
                if mark: self.marks.append(mark)
                self.walk(c)
                if mark: self.marks.pop()
            else:
                self.emit(inline(c, None))
        return self

    def walk_centered(self, div):
        """Centered blocks in Cargo are captions / sub-headings."""
        sub = Body(self.slug, self.media, self.used)
        sub.walk(div); sub.flush()
        for b in sub.blocks:
            if b.startswith(("![", "### ", "http", "> ", "<")):
                self.blocks.append(b)
            else:
                plain = b.replace("**", "")
                plain = re.sub(r"^\*(.*)\*$", r"\1", plain, flags=re.S)
                plain = re.sub(r"\*\s*  \n\s*\*", "  \n", plain)
                lines = [l.strip().strip("*").strip() for l in plain.split("  \n")]
                lines = [l for l in lines if l]
                if lines:
                    self.blocks.append("  \n".join(f"*{l}*" for l in lines))

def header_parts(soup):
    title_el = soup.select_one(".sayfalardaki-isim-basligi")
    title = ""
    if title_el:
        title = re.sub(r"\s+", " ", title_el.get_text(" ")).strip()
        title_el.decompose()
    info_lines = []
    for el in soup.select(".sayfa-basliklari"):
        # only take info spans that come before the first media item
        txt = inline(el, "info")
        for l in txt.split("\n"):
            l = l.strip()
            if l and l not in ("**", "****", "*"):
                info_lines.append(l)
        el.decompose()
    return title, info_lines

def tidy_title(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = t.replace("Perfomative", "Performative")
    return t

def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)

