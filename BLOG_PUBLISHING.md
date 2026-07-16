# Surrey Street — Blog Publishing Runbook

How a finished blog draft becomes a live post on `surreystreet.ai/blog/<slug>`, and
how it relates to beehiiv (send) and LinkedIn (distribution).

> **Where prose comes from:** drafts are written in a separate Cowork session and
> arrive as markdown files. This repo only handles structure + publishing wiring.

---

## The architecture (recap)

- **Canonical home = `surreystreet.ai/blog/<slug>/`.** This is the copy search
  engines should index and the URL everything links back to.
- **beehiiv = the send mechanism.** It mails the post to subscribers.
- **LinkedIn = distribution.** Excerpt or full text, always linking back to the
  canonical URL.

---

## File map

```
content/blog/<slug>.md      ← you drop finished drafts here (with frontmatter)
content/blog/_TEMPLATE.md    ← copy this to start a new post (ignored by builder)
templates/post.html          ← the ONE post layout (edit once, applies to all)
templates/blog-index.html    ← the /blog listing layout
build_blog.py                ← run this to (re)generate everything
blog/<slug>/index.html       ← GENERATED — do not hand-edit
blog/index.html              ← GENERATED listing
blog/rss.xml                 ← GENERATED feed
sitemap.xml                  ← GENERATED (core pages + every post)
```

Generated files are produced from markdown + templates. Never edit anything under
`blog/` by hand — re-run the builder instead.

---

## Publish a post (the whole loop)

1. **Add the draft.** Save the finished markdown as `content/blog/<slug>.md`.
   Required frontmatter: `title`, `description`. Recommended: `date`, `eyebrow`,
   `og_image`. See `content/blog/_TEMPLATE.md` for the full list. Set
   `draft: true` to keep it out of the build until ready.

2. **Build + self-check.**
   ```
   python3 build_blog.py --check
   ```
   This regenerates the post, the `/blog` index, `rss.xml`, `sitemap.xml`, and the
   `teasers/<slug>.md` promo blurb, then verifies every post has a title, meta
   description, self-referencing canonical, complete Open Graph + Twitter tags,
   and that the `og:image` actually resolves to a file on disk. It exits non-zero
   if anything is missing — so a bad unfurl can't slip through.

3. **Preview locally.** Serve the repo root and open the post:
   ```
   npx http-server -p 8080 -c-1
   # → http://localhost:8080/blog/<slug>/
   # → http://localhost:8080/blog/
   ```

4. **Stage & deploy.** Commit and push to `main`; Cloudflare Pages builds from
   the repo root. **This is a STOP-and-ask step — nothing goes live without your
   go-ahead** (see Boundaries). The deploy is just static files; no build command
   needed on Cloudflare's side.

5. **Send via beehiiv** — **full post** in the email with a link back to the
   canonical site (see "Email model" below). Either compose from your saved
   template or let RSS automation draft it.

6. **Post to LinkedIn / lead-gen** using `teasers/<slug>.md` (ready-to-paste blurb
   + UTM links).

### Email model: FULL post in beehiiv (decided)
The beehiiv email carries the **full** article with a link back to
`surreystreet.ai/blog/<slug>/`. Because beehiiv can't set a `rel=canonical`, a
full-text web copy on `*.beehiiv.com` would compete with the site in search — so
**turn OFF beehiiv's site-wide "Discoverable on the web"** (Settings → Website/SEO)
to keep the hosted copy out of Google. The email still sends normally; the site
stays the only indexed copy. Since the RSS feed carries full content
(`<content:encoded>`), beehiiv **RSS automation** can auto-draft the full email
from `https://surreystreet.ai/blog/rss.xml` — optional, removes double-entry.

### Teasers for LinkedIn / lead-gen
Every build writes `teasers/<slug>.md`: a ready-to-paste headline + lede hook +
"read the full piece" CTA, plus **UTM-tagged share links** (LinkedIn / X /
newsletter / generic) so source tracking survives referrer stripping. Edit before
posting; rebuilding overwrites it. These files are working copies, not linked from
the site.

---

## Unfurl check (before you share anywhere)

`build_blog.py --check` validates the tags are present and the image resolves
locally. Once the post is **live**, do a real-world unfurl check so LinkedIn shows
the right card:

- **LinkedIn Post Inspector:** https://www.linkedin.com/post-inspector/ — paste the
  live URL, confirm the title/description/image render. (Inspector also clears
  LinkedIn's cache if you change the OG image later.)
- **Open Graph preview:** https://www.opengraph.xyz/ — paste the URL, eyeball the
  card.

**OG image guidance:** the ideal share image is **1200×630 px**. The template
defaults `og_image` to `/logo/leopard_face.png` (square) — fine as a fallback, but
for important posts set a per-post `og_image:` in frontmatter pointing at a
1200×630 graphic for a full-width card. A bad/empty unfurl kills click-through.

---

## beehiiv ⟷ canonical: important limitation + what to do

**The brief assumed beehiiv could carry a `rel=canonical` pointing back to
surreystreet.ai. Per beehiiv's own documentation, it cannot.** beehiiv's per-post
SEO fields are: post slug, meta title, meta description, Open Graph fields, and X
(Twitter) fields — **no canonical-URL field and no per-post noindex**. The only
indexing control is a *site-wide* "Discoverable on the web" toggle.

Sources:
- https://www.beehiiv.com/support/article/14493017506583-options-on-the-web-page-of-the-post-flow
- https://www.beehiiv.com/support/article/37100791400727-seo-settings-for-your-website

**DECISION (made):** the email is the **full post** with a link back to the site,
so we use **Option A** — keep the beehiiv web copy out of search.

### Option A — Keep the beehiiv web version out of search ✅ (in use)
Turn **OFF** the publication's site-wide **"Discoverable on the web"** toggle
(beehiiv → Settings → Website/SEO → "Discoverable on the web").
The email still sends; subscribers can still open the hosted web version via their
emailed link; but Google won't index a competing full-text copy, so
surreystreet.ai stays the only indexed home.
*Trade-off:* the toggle is all-or-nothing for the whole beehiiv site — fine here,
since the Surrey Street publication exists only to send.

### beehiiv fields to set on every post
In the post's **Web** tab → **SEO Settings**:
- **Slug:** match the site slug if you like, but it doesn't need to.
- **Meta title:** the post `title`.
- **Meta description:** the post `description`.
- **Open Graph image/title/description** and **X fields:** mirror the site's
  `og_image` / `title` / `description` so the beehiiv copy unfurls consistently.

**Boundary:** connecting/authenticating the beehiiv account is yours to do. I can
prepare exact values to paste, but I won't log in or connect it.

---

## Subscribe form (wired)

A navy "newsletter" band renders at the end of every post and on `/blog`. It
loads the live beehiiv form, which supplies its own title + subtitle + field +
button, so our band is just the frame around it (no duplicate heading).

**beehiiv account structure:** one login, two publications — Yuki Bird and
**Surrey Street** (`surreystreetai.beehiiv.com`). The subscribe form must be
created *inside the Surrey Street publication* or sign-ups land in the wrong list.

**How it's wired:** `BEEHIIV_FORM_ID` in `build_blog.py` holds the v3 form's
`data-beehiiv-form` id. The band emits beehiiv's v3 script embed
(`subscribe-forms.beehiiv.com/v3/loader.js`). To swap the form, change that id and
re-run `python3 build_blog.py`. (If the id is ever blank, the band falls back to a
styled, non-functional placeholder.)

**Editing the form copy:** title/subtitle live in the beehiiv form builder and
update the live form with no rebuild needed.

**Known styling ceiling:** on the current beehiiv plan/tier, the form's font
(serif) and button color (black) aren't customizable, so the form isn't a
pixel-perfect match to the site's Inter. The clean fix, if wanted later: a small
Cloudflare Pages Function that posts to beehiiv's API behind our own Inter-styled
form. **Connecting/authenticating beehiiv stays yours.**

## (Optional, later) Syndication — stop double-entry

`blog/rss.xml` already includes full post HTML (`<content:encoded>`). beehiiv can
**import an RSS feed** and auto-draft (or auto-send) a post when a new item
appears (beehiiv → Automations / RSS-to-send, plan-dependent). Wiring
`https://surreystreet.ai/blog/rss.xml` into that means: publish on the site →
beehiiv drafts the email automatically. Left as a follow-up; the feed is ready
whenever you want to turn it on.

---

## Analytics (Cloudflare Web Analytics)

Analytics = **Cloudflare Web Analytics** (free, cookieless). The beacon is
**manually installed** before `</body>` in every page and in both blog templates
(so future posts inherit it) — because Cloudflare's *automatic* edge-injection
didn't fire on this GitHub-Pages-behind-Cloudflare setup. Dashboard setting:
**"Enable with JS Snippet installation."**

**What it shows:** totals (visits, page views, top paths, countries, devices) +
a **Referrers** report. **What it does NOT do:** track **UTM parameters** — it
doesn't log query strings. So the `utm_source=...` tags on social links are
ignored here; channel attribution comes only from the `Referer` header, and
LinkedIn's app / X / email clients often **strip it → traffic lands in "Direct."**

**Gotcha:** ad-blockers / privacy extensions block `cloudflareinsights`, so your
*own* visits often don't register (dashboard looks empty/null). **Test in
Incognito** or on a phone over cellular — real un-blocked visitors are counted.

**To actually read UTMs later** (only if the referrer gaps bug you): GA4 (free,
but Google/cookies), or self-hosted **Umami / Plausible CE** (free + privacy-first,
on the VPS), or paid **Plausible/Fathom** (~$9/mo). Decided for now: wait and see
with Cloudflare before adding a second tool.

## Boundaries (won't do without your explicit go-ahead)

- **Publishing live / pushing to production** — staged and shown to you first.
- **Connecting or authenticating beehiiv** — your account step.
- **DNS, domain, or account settings** — not touched.

I build, stage, and prepare freely; you flip the final live/auth switches.
