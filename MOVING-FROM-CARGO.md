# Moving ilkyazs.com from Cargo to GitHub Pages

Do the steps in this order. **Don't cancel Cargo until step 6.** Your domain and
all your images are still on Cargo until then.

---

## 1. Start the domain transfer (do this first, it's the slow part)

ilkyazs.com was bought through Cargo, so it has to move to a domain registrar
you control. Common choices are Cloudflare Registrar, Porkbun and Namecheap.
A transfer normally adds a year of registration, which you pay for at the new
registrar.

1. Email Cargo support. Ask them to **unlock ilkyazs.com** and send you its
   **transfer (auth/EPP) code**.
2. Create an account at the registrar you picked and start a *transfer in*
   for ilkyazs.com, using that code.
3. Approve the confirmation email when it arrives.

Transfers usually take up to about a week. Domains also can't be moved within
60 days of being registered or last transferred. If that applies, Cargo will
tell you, and you'll have to wait out the 60 days.

Your Cargo site keeps working during the transfer. Keep going with the steps below.

## 2. Put the site on GitHub

1. Sign in to GitHub as **ilkyazs7**.
2. Create a new **public** repository named exactly **`ilkyazs7.github.io`**.
3. Upload everything in this folder, including the hidden `.pages.yml` file.
   The easiest way is **GitHub Desktop**: clone the empty repository, copy these
   files into it, then *Commit* and *Push*. The web uploader takes about 100
   files at a time, which also works, just in batches.
4. In the repository, go to **Settings → Pages**. Under *Build and deployment*,
   choose **Deploy from a branch**, then pick **main** and **/ (root)**.
5. Within a couple of minutes the site is live at **https://ilkyazs7.github.io**.

## 3. Bring your images over

1. Open the repository folder on your computer (the GitHub Desktop copy).
2. In Terminal, run `python3 tools/download_cargo_images.py`.
3. Check the results, then delete anything you don't want. For a project you
   want gone entirely, delete its file in `_projects/` and its folder in
   `assets/images/`.
4. Commit and push.

Large photos come down at 2000px wide, which keeps the repository well under
GitHub's size limits. Swap in your own originals any time by keeping the
same file name.

## 4. Turn on the visual editor

1. Go to <https://app.pagescms.org> and sign in with GitHub.
2. Install it on the `ilkyazs7.github.io` repository and open it.
3. You can now edit projects, the about page and site settings from the
   browser, much like Cargo's editor. Each save republishes the site.

## 5. Point ilkyazs.com at GitHub (after the transfer finishes)

1. **Verify the domain** in GitHub: go to your profile **Settings → Pages →
   Add a domain**, enter `ilkyazs.com`, and add the TXT record it shows at your
   new registrar. This stops anyone else from claiming the domain on GitHub.
2. In the repository, go to **Settings → Pages → Custom domain**, enter
   `ilkyazs.com` and save. GitHub adds a `CNAME` file to the repository.
3. At your registrar's DNS settings, delete any default records it added for
   the bare domain or `www`, then add:

   | Type | Name | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | ilkyazs7.github.io |

   Optionally, also add these AAAA records for IPv6:
   `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.

4. DNS can take up to 24 hours to take effect. Once it does, tick **Enforce
   HTTPS** in the same Pages settings. The option can take a while to appear.

## 6. Cancel Cargo

Cancel only when all three of these are true:

- ilkyazs.com shows the new site.
- The domain appears in your new registrar account.
- Your images are in the repository, or you've decided which ones you don't need.

Then cancel your Cargo subscription.

---

### Things to check or fill in

- **Perception and Capturing.** Cargo has no year, institution or type for
  these, so they sort to the bottom of the Research table. Add `year` and
  `type` in their files.
- **Teaching.** Neither course says which institution it was at. Add
  `institution` and `country` in `_data/teaching.yml`.
- **Two awards.** ACADIA Student Scholarship has no country, and Ulus 100th
  Year Bazaar has no "granted by". Fill these in `_data/awards.yml`.
- **Blog link.** It was a placeholder on Cargo, so it's hidden. Add the real
  address as `blog_url` in `_data/about.yml`.
- **About photo.** Optionally add a portrait (`portrait` in `_data/about.yml`).
  It shows beside the bio.

### What changed from the Cargo version

- **Fonts.** Cargo's fonts can't be carried over; see README.md.
- **[11] Spring Force Mechanics.** It now has its own row; on Cargo the home
  link went to Speed of Sound.
- **Email.** The contact form is now an email link.
- **Omnifab.** The dead "omnifab" link on the Machines of Making sub-pages
  became plain text.
- **Old links.** Cargo addresses like `/[02]-perfomative-agency-human-knitting`
  redirect to the new pages.
