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
   This regenerates the post, the `/blog` index, `rss.xml`, and `sitemap.xml`,
   then verifies every post has a title, meta description, self-referencing
   canonical, complete Open Graph + Twitter tags, and that the `og:image`
   actually resolves to a file on disk. It exits non-zero if anything is missing
   — so a bad unfurl can't slip through.

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

5. **Send via beehiiv** (see below).

6. **Post to LinkedIn** linking to `https://surreystreet.ai/blog/<slug>/`.

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

So to keep surreystreet.ai as the single indexed copy, pick **one** of these
(the builder supports either — no code change needed):

### Option A — Keep the beehiiv web version out of search (recommended if email = full post)
Use beehiiv purely as the send channel and turn **OFF** the publication's
site-wide **"Discoverable on the web"** toggle
(beehiiv → Settings → Website/Publication → SEO → "Discoverable on the web").
The email still sends; subscribers can still open the hosted web version via their
emailed link; but Google won't index a competing full-text copy. surreystreet.ai
stays the only indexed home.
*Trade-off:* the toggle is all-or-nothing for the whole beehiiv site, so only use
this if you don't need beehiiv's web pages indexed for anything else.

### Option B — Make the beehiiv email a teaser (recommended if you want beehiiv web pages discoverable)
The email contains a summary + "read the full piece on surreystreet.ai" link. The
only *full* copy that exists (and gets indexed) is the canonical site, so there's
no duplicate-content competition even if beehiiv's web version is discoverable.
This is the **teaser email model** — one of the two models you left open. The
build already produces both a short `<description>` and full `<content:encoded>`
in `rss.xml`, so either model works downstream.

> You still haven't chosen teaser-vs-full, and you asked me not to choose it.
> Note only that **Option A pairs with a full-post email; Option B pairs with a
> teaser.** Decide that one and the beehiiv path is settled.

### beehiiv fields to set on every post (either option)
In the post's **Web** tab → **SEO Settings**:
- **Slug:** match the site slug if you like, but it doesn't need to.
- **Meta title:** the post `title`.
- **Meta description:** the post `description`.
- **Open Graph image/title/description** and **X fields:** mirror the site's
  `og_image` / `title` / `description` so the beehiiv copy unfurls consistently.

**Boundary:** connecting/authenticating the beehiiv account is yours to do. I can
prepare exact values to paste, but I won't log in or connect it.

---

## (Optional, later) Syndication — stop double-entry

`blog/rss.xml` already includes full post HTML (`<content:encoded>`). beehiiv can
**import an RSS feed** and auto-draft (or auto-send) a post when a new item
appears (beehiiv → Automations / RSS-to-send, plan-dependent). Wiring
`https://surreystreet.ai/blog/rss.xml` into that means: publish on the site →
beehiiv drafts the email automatically. Left as a follow-up; the feed is ready
whenever you want to turn it on.

---

## Boundaries (won't do without your explicit go-ahead)

- **Publishing live / pushing to production** — staged and shown to you first.
- **Connecting or authenticating beehiiv** — your account step.
- **DNS, domain, or account settings** — not touched.

I build, stage, and prepare freely; you flip the final live/auth switches.
