---
title: "Sample Post — Delete Me After Reviewing the Pipeline"
description: A throwaway post that exists only to demonstrate the publishing pipeline end to end. Delete this file once you've confirmed the layout, OG tags, and RSS look right.
slug: sample-hello-world
date: 2026-06-29
author: Surrey Street Partners
eyebrow: Pipeline Test
og_image: /logo/leopard_face.png
og_image_alt: Surrey Street Partners
---

This page is **not real content**. It's here to prove the build works: drop a
markdown file into `content/blog/`, run the builder, and a fully-formed,
SEO-ready post appears at `/blog/<slug>/`.

## What this demonstrates

The builder renders the elements a real post will use:

- Section headings (`##` and `###`)
- **Bold** and *italic* text
- [Links back to the canonical site](https://surreystreet.ai)
- `Inline code` and lists

### A sub-heading

> Pull-quotes render with the brand accent rule, so a strong line from the post
> can be set apart.

When you're done eyeballing this, delete `content/blog/sample-hello-world.md`
and re-run `python3 build_blog.py` — the post and its folder disappear from the
listing, RSS, and sitemap.
