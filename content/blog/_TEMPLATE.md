---
title: Your Post Title Here
description: One or two sentences. This becomes the meta description, the LinkedIn/OG unfurl text, the RSS summary, and the listing blurb. Keep it under ~160 characters.
slug: your-post-title-here
date: 2026-06-29
author: Surrey Street Partners
eyebrow: Payments
hero: /blog/your-post-title-here/hero.jpg   # optional: shows on-page AND becomes the OG unfurl card. ~1200px wide JPEG, co-locate in the post's folder. Omit for no hero.
og_image: /logo/leopard_face.png            # only needed if you want a DIFFERENT unfurl image than the hero; otherwise delete this and the hero is used
og_image_alt: Surrey Street Partners
draft: true
---

Write the post body in Markdown below the frontmatter.

## A section heading

Paragraphs, **bold**, *italic*, [links](https://surreystreet.ai), and `inline code`
all work. So do lists:

- point one
- point two

> And blockquotes for pull-quotes.

When the draft is final, set `draft: false` (or delete the line), drop this file
into content/blog/ with a real filename, and run `python3 build_blog.py --check`.

Files whose name starts with `_` (like this one) are ignored by the builder.
