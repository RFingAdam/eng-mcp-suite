# Playbook — engineering MCP toolkit

Reference, training, and outreach material for the engineering MCP
toolkit. Pick the doc that matches your audience.

| Doc | For who | Length |
|---|---|---|
| [`cheat-sheet.md`](cheat-sheet.md) | I just want commands | ~1 page |
| [`playbook.md`](playbook.md) | I want the full strategy | ~10 min read |
| [`workshop.md`](workshop.md) | I'm running a hands-on session | 2.5 hr workshop |
| [`slides.md`](slides.md) | I'm giving a talk | 20-slide Marp deck |
| [`blog.md`](blog.md) | I'm writing about the toolkit | ~1500-word post |

## When to reach for each one

- **First time seeing the toolkit?** Read `playbook.md`. It's the
  reference doc and the longest one, but it covers the whole picture:
  why MCP, the four-layer model, the workflows, the case study, the
  FAQ.
- **Already up and running, need a command?** `cheat-sheet.md` is
  one page, all commands, all workflows.
- **Bringing a team up to speed?** Run them through `workshop.md`.
  Five sections, 2.5 hours, gets a participant from "I have Python"
  to "I just ran a full pre-compliance EMC scan."
- **Giving a meetup or conference talk?** `slides.md` is a Marp deck.
  Render with `marp slides.md` and present.
- **Writing an announcement?** `blog.md` is a ready-to-adapt draft —
  HN, dev.to, LinkedIn, personal blog. Edit the voice; the structure
  works.

## Format

- All five docs are plain markdown.
- Slides use [Marp](https://marp.app/) frontmatter. To render:
  `marp slides.md -o slides.pdf` (or `.html`, or `.pptx`).
- No external assets — everything lives in this directory.

## Contributing

Found a gap or an error? Open an issue or PR on
[eng-mcp-suite](https://github.com/RFingAdam/eng-mcp-suite). For
substantive rewrites, file an issue first so we can talk through the
scope.
