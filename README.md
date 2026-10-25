# ilkyazs.com

Personal site of İlkyaz Sarımehmetoğlu. Everything that was on the Cargo site
is stored here as plain, structured data, sorted by what kind of information
it is. That data then drives an archive-style site with five tabs: **Research**
(home), **Awards**, **Teaching**, **Exhibition** and **About**. Each tab is a
sortable table with an image grid beside it.

Moving off Cargo? Start with **MOVING-FROM-CARGO.md**.

## The content (reusable for any future site)

| File | What's in it |
|---|---|
| `_projects/*.md` | one file per research project or exhibition (21 in total) |
| `_data/about.yml` | name, pronouns, bio paragraphs, email, CV, blog |
| `_data/awards.yml` | awards, fellowships and grants |
| `_data/teaching.yml` | courses and workshops taught |
| `_data/publications.yml` | papers, shown on the About tab |
| `tools/media.csv` | every image and video: file, project, caption, size, Cargo source |
| `site-content.json` | all of the above in one file, for building some other site |

The project files hold YAML only (between the `---` lines). Each one has
named fields for the facts, then the page content as an ordered list of
typed blocks:

```yaml
title: 'Performative Agency: Human Knitting'
short_title: Human Knitting
number: '02'                  # your own numbering
section: research             # research | exhibition  -> which tab it appears in
theme: 'Soft Intelligence: Embodied Mind'
year: 2023                    # the YEAR column, used for sorting
period: 2023–2024             # the date as you wrote it
type: Academic                # the TYPE column
mode: Group
institution: University of Michigan
institution_short:            # optional shorter name for the table, e.g. MIT
program: MS Digital and Material Technologies
course: Systems Engagement
city: Ann Arbor
country: US
instructors: [Sean Ahlquist]
collaborators: [Jutang Gao, Archit Goyal, Daniel Merupu, Lucas Yan, Yi-Chin Lee (fabrication)]
cover: /assets/images/human-knitting/human-knitting.jpg
hidden: false
summary: Opening paragraph, shown large.
blocks:
  - type: heading
    text: Installation II
  - type: text
    text: Paragraph text, with **bold**, *italic* and [links](https://example.com).
  - type: image
    src: /assets/images/human-knitting/dsc-4108.jpg
    caption: isometric diagram showing knit placement   # optional
    size: small                                         # optional
  - type: gallery                 # images side by side
    items:
      - src: /assets/images/human-knitting/a.jpg
      - src: /assets/images/human-knitting/b.jpg
    caption: optional
  - type: video                   # an .mp4 file, plays silently on loop
    src: /assets/images/speed-of-sound/clip.mp4
  - type: embed                   # YouTube, Vimeo or SoundCloud link
    url: https://youtu.be/GUCw5ZysEmY
    caption: process video
  - type: caption                 # a small standalone note
    text: ...
  - type: note                    # a grey italic line
    text: ...
```

A few fields only appear where they're needed:

- **`parts`**: sub-projects with their own facts (05).
- **`credits`**: grouped name lists (ZAP!).
- **`links`**: outside links.
- **`machine`**: the fabrication machine (the Machines of Making sub-projects).
- **`parent`**: for sub-projects (the five Machines of Making pages).
- **`venue`** and **`role`**: for exhibitions.

Captions were matched to images from where they sat on the Cargo pages: an
italic line directly above an image became that image's caption.

## Editing

**Visual editor:** go to <https://app.pagescms.org>, sign in with GitHub,
install it on this repository and open it. You get *Research & exhibitions*,
*Awards*, *Teaching*, *Publications*, *About* and *Site settings*, each with
proper form fields. Saving publishes within a minute or two.

**On GitHub:** open any file, click the pencil, edit, commit.

Common changes:

- **Remove a project:** delete its file in `_projects/`, or set `hidden: true`
  to keep the file but take it off the site.
- **Move a project between tabs:** change its `section`.
- **Change the order:** the tables sort by `year`, newest first. Visitors can
  also click any column heading to re-sort.
- **Change the colour:** set `accent` in `_data/settings.yml`. It's `#2600FF`.
- **Make thumbnails black & white:** set `grayscale_thumbnails: true` in
  `_data/settings.yml`, like aatb.ch.
- **Rename or reorder the tabs:** edit `tabs` in `_data/settings.yml`.

## Images

Every image is a grey placeholder until its file exists. To pull them all from
Cargo while it's still online, run this from the top folder:

```bash
python3 tools/download_cargo_images.py
```

You can also fetch one project at a time:

```bash
python3 tools/download_cargo_images.py human-knitting
```

To preview with Cargo's copies before downloading, set
`show_cargo_images: true` in `_data/settings.yml`. Set it back to `false`
before cancelling Cargo, because those copies disappear with your account.

## Fonts

aatb.ch uses commercial fonts (PP Mondwest, PP Neue Bit). This site uses two
free Google Fonts in the same spirit: **Newsreader** for the serif text and
tables, and **Geist** for the uppercase labels. To swap them, edit `--serif`
and `--sans` at the top of `assets/css/style.css`, and the font link in
`_layouts/default.html`.

## Re-extracting from Cargo

`tools/extract.py` (with `tools/cargo_common.py`) is the script that turned
the Cargo pages into these files. You only need it to redo the extraction;
running it overwrites `_projects/` and `_data/`.
