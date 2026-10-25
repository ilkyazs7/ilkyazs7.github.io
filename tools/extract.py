"""Extract Cargo content into typed, site-independent data files.

Output (into OUT):
  _projects/<slug>.md      one YAML document per project (front matter only)
  _data/about.yml          bio, contact, links
  _data/awards.yml         awards & grants
  _data/teaching.yml       teaching
  _data/publications.yml   publications
  tools/media.csv          every image / video: file, project, caption, Cargo source
  assets/media-map.json    file -> size + Cargo URL (used for placeholders)
  site-content.json        everything above in one file
"""
import json, re, os, sys, csv
import yaml
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(__file__))
import cargo_common as cc

OUT = sys.argv[1]

# ------------------------------------------------------------------ project plan
# Cargo page id -> slug, section, number, theme, sort order
PLAN = {
    "N3908447647": ("sensing-glove", "research", "00", "Soft Intelligence: Embodied Mind"),
    "K1002071343": ("textile-jukebox", "research", "01", "Soft Intelligence: Embodied Mind"),
    "G1486678012": ("human-knitting", "research", "02", "Soft Intelligence: Embodied Mind"),
    "F4201063030": ("cnc-knitting", "research", "03", "Soft Intelligence: Embodied Mind"),
    "Q2663307658": ("speed-of-sound", "research", "04", "Situated Machines: Measurement Instruments"),
    "K1468495737": ("spring-force-mechanics", "research", "11", "Situated Machines: Measurement Instruments"),
    "I0787905088": ("optimization-for-digital-fabrication", "research", "05", "Digital to Physical: Advanced Fabrication"),
    "B3365839854": ("machines-of-making", "research", "07", "Digital to Physical: Advanced Fabrication"),
    "Z3616925775": ("perception", "research", "08", "Machine"),
    "F3779968120": ("capturing", "research", "09", "Machine"),
    "N0046182474": ("learning", "research", "10", "Machine"),
    "P1773310485": ("retro-fitting", "research", "12", "Leftover Project"),
    "E3406970679": ("the-alphabet-song", "research", "13", "Leftover Project"),
    "J0207791252": ("plotted-leftovers", "research", "14", "Leftover Project"),
    "M1916100687": ("zap", "exhibition", "", ""),
    "S4115486832": ("architecture-is-art", "exhibition", "", ""),
    # Machines of Making sub-projects, in the order Cargo showed them
    "E0285821388": ("precise-fit", "research", "07.1", "Digital to Physical: Advanced Fabrication"),
    "O2885552224": ("light-leak", "research", "07.2", "Digital to Physical: Advanced Fabrication"),
    "Z3708164254": ("wall-with-a-hole", "research", "07.3", "Digital to Physical: Advanced Fabrication"),
    "H1079254261": ("two-does-not-equal-to-one", "research", "07.4", "Digital to Physical: Advanced Fabrication"),
    "W3261113664": ("morphbox", "research", "07.5", "Digital to Physical: Advanced Fabrication"),
}
CHILDREN = ["E0285821388", "O2885552224", "Z3708164254", "H1079254261", "W3261113664"]

UM = dict(institution="University of Michigan", city="Ann Arbor", country="US",
          program="MS Digital and Material Technologies")
MIT = dict(institution="Massachusetts Institute of Technology", institution_short="MIT", city="Cambridge", country="US")
METU = dict(institution="METU", city="Ankara", country="TR")
PRACTICUM = dict(UM, period="2023–2024 Fall", year=2023, type="Academic", mode="Individual",
                 course="MS Practicum", instructors=["Catie Newell", "Mark Meier"])

# Facts read from each page's info block, split into fields by hand.
META = {
    "N3908447647": dict(MIT, title="Sensing Through the Body: Glove for AR Interaction", period="2025–2026 Fall", year=2025,
                        type="Academic", mode="Group", course="3.173 Computing Fabrics", collaborators=["Clara Emmerling"]),
    "K1002071343": dict(UM, title="Tactile Intelligence: Haptic Library / Textile Jukebox", short_title="Textile Jukebox",
                        period="2024–2025 Fall", year=2024, type="Academic", mode="Group", course="MS Capstone",
                        instructors=["Sean Ahlquist"], collaborators=["Lucas Yan"],
                        acknowledgements=["University of Michigan, ArtsEngine Student MicroGrant",
                                          "University of Michigan, Rackham Graduate Student Research Grant",
                                          "Ricardo Tiangson"]),
    "G1486678012": dict(UM, title="Performative Agency: Human Knitting", short_title="Human Knitting", period="2023–2024",
                        year=2023, type="Academic", mode="Group", course="Systems Engagement", instructors=["Sean Ahlquist"],
                        collaborators=["Jutang Gao", "Archit Goyal", "Daniel Merupu", "Lucas Yan", "Yi-Chin Lee (fabrication)"]),
    "F4201063030": dict(UM, title="Programmable Knitting: CNC Knitting", short_title="CNC Knitting", period="2023–2024 Spring",
                        year=2024, type="Academic", mode="Group", course="Systems Engagement", instructors=["Sean Ahlquist"],
                        collaborators=["Jutang Gao", "Archit Goyal", "Daniel Merupu", "Lucas Yan", "John Hilla (fabrication)"]),
    "Q2663307658": dict(MIT, title="Speed of Sound", period="2025–2026 Fall", year=2025, type="Academic",
                        course="2.132 MICA Projects"),
    "K1468495737": dict(MIT, title="Spring Force Mechanics", subtitle="[adapting]", period="2025–2026 Fall", year=2025,
                        type="Academic", course="2.132 MICA Projects"),
    "I0787905088": dict(UM, title="Optimization for Digital Fabrication", period="2023–2024", year=2023, type="Academic",
                        parts=[
                            dict(title="Cavity Slab", number="5.i", period="2023–2024 Fall", course="Independent Study",
                                 instructors=["Mania Aghei Meibodi"], contributors=["Stuti Bindlish", "Zaid Marji"]),
                            dict(title="3DGS + Robotics", number="5.ii", period="2023–2024 Spring", mode="Individual",
                                 course="Robotic Engagement", instructors=["Wes McGee"]),
                            dict(title="Toolpath Optimization + Material-Design Symbiosis", number="5.iii",
                                 period="2023–2024 Fall", course="Material Engagement", instructors=["Mania Aghei Meibodi"]),
                        ]),
    "B3365839854": dict(UM, title="Machines of Making", period="2023–2024 Fall", year=2023, type="Academic",
                        course="MS Practicum", instructors=["Catie Newell", "Mark Meier"]),
    "Z3616925775": dict(title="Perception", year=None, type=""),
    "F3779968120": dict(title="Capturing", subtitle="camera machine / film work", year=None, type=""),
    "N0046182474": dict(METU, title="Learning", period="2022–2023 Spring", year=2023, type="Academic", mode="Individual",
                        program="Architecture", course="BS723 Machine Learning Applications in Architecture",
                        instructors=["Prof. Dr. Arzu Gönenç Sorguç (studio coordinator)", "Müge Krusa Yemiscioglu",
                                     "Ozan Yetkin", "Sevval Cologlu"]),
    "P1773310485": dict(title="Retro-fitting (ML)", subtitle="Machine Learning Applications of Leftover Materials in Digital Fabrication",
                        period="2019–present", year=2019, type="Personal", status="work in progress"),
    "E3406970679": dict(title="The Alphabet Song", period="2023", year=2023, type="Personal"),
    "J0207791252": dict(title="Plotted Leftovers", period="2024", year=2024, type="Personal"),
    "M1916100687": dict(title="ZAP!", subtitle="Bio-Inspired Large-Scale Multimedia Installation", period="2024–2025 Fall",
                        year=2024, type="Exhibition", role="Artist",
                        venue="University of Michigan Duderstadt Gallery + Video Studio", city="Ann Arbor", country="US",
                        institution="FEAST: Faculty Engineering/Arts Student Teams, University of Michigan ArtsEngine",
                        credits=[
                            dict(group="Artists & Lab", names=["SMART (Sound and Media Art) Lab", "Director: Dr. Zeynep Özcan"]),
                            dict(group="SMART Lab Student Members", names=[
                                "İlkyaz Sarımehmetoğlu (Architecture, MS)", "Shoma Sawa (Computer Science, MA)",
                                "Sabrina Sugg (Environment, BS & MS)", "Brooke Steele (Fine Arts, BA)",
                                "Natalia Quintanilla Cabrera (Performing Arts Technology, MA)"]),
                            dict(group="Thank you", names=["Zeke Bolukh", "Eva Choi", "Carly Lowe", "Paul Luckhoff",
                                                           "Emma Reich", "Lucas Yan", "Ginny Jiang"]),
                        ],
                        links=[dict(label="SMART Lab website", url="https://smartlab.cargo.site")]),
    "S4115486832": dict(METU, program="Architecture", title="Architecture is Art", period="2022–2023 Spring", year=2023, type="Exhibition",
                        role="Exhibition assistant; exhibition design team participant; exhibition catalog designer",
                        venue="CerModern", course="ARCH524 Architecture and Different Modes of Representation",
                        instructors=["Prof. Dr. Aysen Savas (seminar instructor)"]),
    "E0285821388": dict(PRACTICUM, title="Precise Fit", short_title="3-axis CNC", machine="3-axis CNC router",
                        mode="Group", collaborators=["Lucas Yan"]),
    "O2885552224": dict(PRACTICUM, title="Light Leak", short_title="Zund knife cutter", machine="Zund CNC knife cutter"),
    "Z3708164254": dict(PRACTICUM, title="Omnifab: Wall with a Hole", short_title="Robotic 3D printing",
                        machine="KUKA KR60 robotic clay printing"),
    "H1079254261": dict(PRACTICUM, title="Omnifab: Two Does Not Equal to One", short_title="Waterjet", machine="Waterjet"),
    "W3261113664": dict(PRACTICUM, title="Omnifab: Morphbox", short_title="Hands", machine="Hands"),
}

# slugs used by the first rebuild (/projects/...), kept as redirects
cc_old = {k: v[0] for k, v in cc.PLAN.items()}

# make the shared parser link to the new addresses
cc.PLAN = {k: (v[0], v[2], v[3], i) for i, (k, v) in enumerate(PLAN.items())}
cc.purl_to_id = {cc.P(pid)["purl"]: pid for pid in PLAN}
cc.url_for = lambda pid: f"/work/{PLAN[pid][0]}/"
_old_map = cc.map_href
def map_href(href):
    r = _old_map(href)
    if r == "/projects/07-machines-of-making/":
        return "/work/machines-of-making/"
    if r == "/visual-index/":
        return "/"
    return r
cc.map_href = map_href

# ------------------------------------------------------------------ markdown blocks -> typed blocks
IMG_RE = re.compile(r'!\[\]\(([^)\s]+)(?:\s+"small")?\)')
SOUNDCLOUD_CREDIT = re.compile(r'^\[[^\]]+\]\(https://soundcloud\.com/[^)]+\)\s*·')

def is_caption(b):
    lines = b.split("  \n")
    return all(re.fullmatch(r"\*[^*].*?\*", l.strip()) for l in lines)

def strip_italics(b):
    return " ".join(l.strip()[1:-1].strip() for l in b.split("  \n"))

def media_block(srcs, small):
    items = []
    for s in srcs:
        info = cc.IMAGE_MAP.get(s, {})
        items.append(dict(type="video" if info.get("video") or re.search(r"\.(mp4|mov|webm)$", s) else "image", src=s))
    if len(items) == 1:
        b = items[0]
        if small: b["size"] = "small"
        return b
    return dict(type="gallery", items=[dict(src=i["src"]) if i["type"] == "image" else i for i in items])

def typed(blocks):
    out = []
    for b in blocks:
        b = b.strip()
        if not b or SOUNDCLOUD_CREDIT.match(b):
            continue
        srcs = IMG_RE.findall(b)
        if srcs and not IMG_RE.sub("", b).strip():
            out.append(media_block(srcs, '"small"' in b)); continue
        if re.fullmatch(r"https?://\S+", b):
            out.append(dict(type="embed", url=b)); continue
        m = re.match(r'<iframe[^>]*src="([^"]+)"', b)
        if m:
            out.append(dict(type="embed", url=m.group(1).replace("&amp;", "&"))); continue
        if b.startswith("### "):
            out.append(dict(type="heading", text=b[4:].strip())); continue
        if b.startswith("> "):
            out.append(dict(type="note", text=b[2:].strip())); continue
        if is_caption(b):
            out.append(dict(type="caption", text=strip_italics(b))); continue
        out.append(dict(type="text", text=b.replace("  \n", "\n")))
    # attach a caption to the media right after it (Cargo puts captions above images)
    merged = []
    i = 0
    while i < len(out):
        b = out[i]
        if b["type"] == "caption" and i + 1 < len(out) and out[i + 1]["type"] in ("image", "video", "gallery", "embed"):
            nxt = dict(out[i + 1]); nxt["caption"] = b["text"]; merged.append(nxt); i += 2; continue
        merged.append(b); i += 1
    return merged

def clean_title_from_heading(h):
    return re.sub(r"^\[[\d.]+[ivx.]*\]\s*", "", h).strip()

# ------------------------------------------------------------------ build projects
projects = {}
for idx, (pid, (slug, section, number, theme)) in enumerate(PLAN.items()):
    p = cc.P(pid)
    media = {m["hash"]: m for m in (p.get("media") or [])}
    used = {}
    soup = BeautifulSoup(p["content"], "html.parser")
    for a in soup.find_all("a", href=re.compile("erkilic")):
        a.decompose()
    cc.header_parts(soup)                      # removes title + info spans (facts come from META)
    body = cc.Body(slug, media, used).walk(soup); body.flush()
    blocks = typed(body.blocks)
    # project link line on ZAP is in META.links
    blocks = [b for b in blocks if not (b["type"] == "text" and "smartlab.cargo.site" in b["text"])]
    # summary = first text block
    summary = ""
    for i, b in enumerate(blocks):
        if b["type"] == "text" and len(b["text"]) > 80:
            summary = b["text"]; blocks.pop(i); break
        if b["type"] in ("image", "gallery", "video", "embed", "heading"):
            break
    meta = dict(META[pid])
    cover = ""
    th = p.get("thumbnail")
    if th and th.get("hash"):
        cover = cc.register_media(th, slug, used)
    hover = ""
    hv = cc.HOVER.get(p["purl"])
    if hv:
        hm = re.search(r"/i/([A-Z0-9]+)/([^/']+)$", hv)
        if hm:
            hover = cc.register_media(media.get(hm.group(1)) or {"hash": hm.group(1), "name": hm.group(2)}, slug, used)
    rec = {
        "title": meta.pop("title"),
        "subtitle": meta.pop("subtitle", ""),
        "short_title": meta.pop("short_title", ""),
        "number": number,
        "section": section,
        "theme": theme,
        "parent": "machines-of-making" if pid in CHILDREN else "",
        "year": meta.pop("year", None),
        "period": meta.pop("period", ""),
        "type": meta.pop("type", ""),
        "mode": meta.pop("mode", ""),
        "role": meta.pop("role", ""),
        "institution": meta.pop("institution", ""),
        "institution_short": meta.pop("institution_short", ""),
        "program": meta.pop("program", ""),
        "course": meta.pop("course", ""),
        "venue": meta.pop("venue", ""),
        "city": meta.pop("city", ""),
        "country": meta.pop("country", ""),
        "instructors": meta.pop("instructors", []),
        "collaborators": meta.pop("collaborators", []),
        "contributors": meta.pop("contributors", []),
        "acknowledgements": meta.pop("acknowledgements", []),
    }
    rec.update(meta)   # parts, credits, links, machine, status
    rec["cover"] = cover
    rec["hover_image"] = hover if hover and hover != cover else ""
    rec["hidden"] = False
    rec["redirect_from"] = ["/" + p["purl"] + "/"] + (["/machines-of-making/"] if slug == "machines-of-making" else []) \
        + (["/projects/" + cc_old.get(pid, slug) + "/"] if pid in cc_old else [])
    rec["summary"] = summary
    rec["blocks"] = blocks
    # drop empty fields so files stay readable
    keep_empty = {"title", "number", "section", "year", "type", "cover", "hidden", "summary", "blocks", "redirect_from"}
    rec = {k: v for k, v in rec.items() if k in keep_empty or v not in ("", [], None, {})}
    projects[slug] = rec

# captions into the media registry
captions = {}
for slug, r in projects.items():
    for b in r["blocks"]:
        if b.get("caption"):
            for s in ([b["src"]] if "src" in b else [i["src"] for i in b.get("items", [])]):
                captions.setdefault(s, b["caption"])

# ------------------------------------------------------------------ the lists
about = {
    "name": "İlkyaz Sarımehmetoğlu",
    "pronouns": "she/her/hers",
    "tagline": "embodied interfaces & soft intelligence",
    "role": "Transdisciplinary designer, researcher, and dancer",
    "affiliation": "Master of Science in Design Computation (’27) candidate, MIT",
    "email": "ilkyazs@mit.edu",
    "cv_url": "https://drive.google.com/file/d/1H-ei93_hHOUkkT53fl9qg6IS2k8PepB2/view?usp=sharing",
    "blog_url": "",
    "blog_label": "how the brain machine works (blog)",
    "portrait": "",
    "bio": [
        "İlkyaz Sarımehmetoğlu is a transdisciplinary designer, researcher, and dancer exploring how machines think and communicate through material skins. Her research centers on embodied interfaces, computational textiles, and responsive material systems that integrate sensing, haptics, and computation. She is a **Master of Science in Design Computation (’27)** candidate at **MIT**.",
        "Her research draws on advanced fabrication methods, including CNC machine knitting, robotic fabrication, and soft material systems to develop bi-directional interfaces. Through these systems, she reframes textiles and material assemblies as active participants in human–machine interaction, performance, and making.",
    ],
    "footer": "© 2025 İlkyaz Sarımehmetoğlu. All rights reserved.",
}
awards = [
    dict(title="MIT Architecture Department Fellow", granted_by="MIT Department of Architecture", country="US",
         type="Fellowship", year=2025, period="2025", note="Awarded fellowship by the MIT Department of Architecture", related=""),
    dict(title="Fulbright Scholarship, Master’s Grantee", granted_by="US Department of State, Fulbright Türkiye", country="US",
         type="Scholarship", year=2023, period="2023–2024", note="US Department of State Scholarship, Fulbright Türkiye", related=""),
    dict(title="Master of Science Research Fellow", granted_by="University of Michigan Taubman College of Architecture",
         country="US", type="Fellowship", year=2023, period="2023", note="", related=""),
    dict(title="Rackham Graduate Student Research Grant", granted_by="University of Michigan, Rackham Graduate School",
         country="US", type="Grant", year=2024, period="2024", note="", related="textile-jukebox"),
    dict(title="ArtsEngine Student Research Grant", granted_by="University of Michigan, ArtsEngine", country="US",
         type="Grant", year=2024, period="2024", note="", related="textile-jukebox"),
    dict(title="ACADIA Student Scholarship", granted_by="ACADIA", country="", type="Scholarship", year=2023,
         period="2023", note="", related=""),
    dict(title="Ulus 100th Year Bazaar — Winning Competition Entry", granted_by="", country="TR", type="Competition",
         year=2022, period="2022", note="Project in architecture", related=""),
]
teaching = [
    dict(title="Cultures of Form", role="Assistant Instructor", institution="", country="", type="Course",
         year=2025, period="2025", related=""),
    dict(title="Project Leftovers Workshop", role="Instructor", institution="", country="", type="Workshop",
         year=2023, period="2023", related=""),
]
publications = [
    dict(authors="Sarimehmetoglu, I., Qiu, J., Thaprawat, P., Zhou, G., Valikodath, N., Draelos, M., & Alves-Oliveira, P.",
         year=2025, period="2025, July", title="Robot characters for innovative medical eye exams in kids",
         venue="Proceedings of the Designing Interactive Systems Conference (DIS ’25)", publisher="ACM", pages="",
         type="Conference paper", url="https://doi.org/10.1145/3715336.3735445", related=""),
    dict(authors="Sarimehmetoglu, I., & Özcan, Z.", year=2025, period="2025",
         title="ZAP!: Bio-Inspired Large-Scale Multimedia Installation",
         venue="Proceedings of the International Computer Music Conference (ICMC 2025)",
         publisher="International Computer Music Association", pages="90–95", type="Conference paper", url="",
         related="zap"),
    dict(authors="Schiesser, A., Şimşek, D., Sarımehmetoğlu, İ., & Esendemir, G.", year=2018, period="2018",
         title="Evaluation of antimicrobial activity of methylglyoxal – The major antibacterial component of Manuka honey",
         venue="Mellifera", publisher="", pages="18, 1–6", type="Journal article",
         url="https://dergipark.org.tr/tr/pub/mellifera/issue/41786/504450", related=""),
]

# ------------------------------------------------------------------ write
class Lit(str): pass
def lit_rep(d, s): return d.represent_scalar("tag:yaml.org,2002:str", s, style="|" if "\n" in s else None)
yaml.add_representer(Lit, lit_rep)
def lit(o):
    if isinstance(o, dict): return {k: lit(v) for k, v in o.items()}
    if isinstance(o, list): return [lit(v) for v in o]
    if isinstance(o, str) and "\n" in o: return Lit(o)
    return o
def dump(o):
    return yaml.dump(lit(o), allow_unicode=True, sort_keys=False, width=100000, default_flow_style=False)

os.makedirs(f"{OUT}/_projects", exist_ok=True); os.makedirs(f"{OUT}/_data", exist_ok=True)
os.makedirs(f"{OUT}/tools", exist_ok=True); os.makedirs(f"{OUT}/assets", exist_ok=True)
for slug, r in projects.items():
    open(f"{OUT}/_projects/{slug}.md", "w").write("---\n" + dump(r) + "---\n")
for name, data in [("about", about), ("awards", awards), ("teaching", teaching), ("publications", publications)]:
    open(f"{OUT}/_data/{name}.yml", "w").write(dump(data))

rows = []
for r in cc.IMAGE_ROWS:
    path = "/" + r["local_path"]
    rows.append(dict(file=r["local_path"], project=r["page"], kind=r["type"], width=r["width"], height=r["height"],
                     caption=captions.get(path, ""), download_url=r["download_url"], cargo_original=r["original_url"]))
rows.insert(0, dict(file="favicon.ico", project="site", kind="image", width="", height="", caption="",
                    download_url="https://freight.cargo.site/t/original/i/E1972393106331469414731633347276/icon.ico",
                    cargo_original="https://freight.cargo.site/t/original/i/E1972393106331469414731633347276/icon.ico"))
with open(f"{OUT}/tools/media.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(cc.IMAGE_MAP, open(f"{OUT}/assets/media-map.json", "w"), ensure_ascii=False)
json.dump(dict(about=about, research=[dict(slug=k, **v) for k, v in projects.items() if v["section"] == "research"],
               exhibitions=[dict(slug=k, **v) for k, v in projects.items() if v["section"] == "exhibition"],
               awards=awards, teaching=teaching, publications=publications),
          open(f"{OUT}/site-content.json", "w"), ensure_ascii=False, indent=1)

for slug, r in projects.items():
    kinds = {}
    for b in r["blocks"]: kinds[b["type"]] = kinds.get(b["type"], 0) + 1
    print(slug.ljust(38), r.get("year"), str(r.get("type")).ljust(10), "cap:", sum(1 for b in r["blocks"] if b.get("caption")), kinds)
print("media:", len(rows))
