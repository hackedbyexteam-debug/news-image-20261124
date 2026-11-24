# Tuesday, 24 November 2026 — The World's News in One Image

Entry for the make.fun bounty
[`news-image-20261124`](https://make.fun/bounty/news-image-20261124)
— *"Sum up 24 November's world news in one image"* ($100, entries close
Thu 26 Nov 2026, 07:00 WIB / 2026-11-26T00:00:00Z).

## What it is

`main.py` renders **1024 × 1024 PNG** that sums up Tuesday 24 November
2026 — built around a different hierarchy from the usual wall of
headlines:

- **Masthead — the date, huge:** a dark navy band names the day in 52-pt
  type — "Tuesday 24 November 2026" — so the judge can tell at a glance
  which day the image sums up.
- **Lead story — the $41bn deal:** Sanofi buys Insmed for $41bn in cash
  at $175 a share — a 46% premium, the biggest biotech takeover in
  nearly three years, betting on the rare-lung-disease drug Brensocatib.
  Three big numbers carry it, beside a drawn panel of the deal itself
  ($41bn set huge, a rising bar chart, a two-tone capsule). The deal
  closes in the first half of 2027.
- **The day in brief — six stories, each dated 24 NOV:** Solomon Islands
  drops its China security pact (new Australia treaty due Wednesday);
  Russian aircraft enter South Korea's air defence zone; a gas blast in
  Hanoi kills 6; the Shenzhou-24 crew is unveiled, including Pakistan's
  Zeeshan Ali, the first foreigner to visit Tiangong; Australia strikes
  a big-tech duty-of-care deal with fines up to 5% of global revenue;
  Dhaka says ousted leader Hasina returns on 16 December, only under
  extradition.
- **Also today:** a 5.6-magnitude quake in Nepal near the Chinese border;
  Baghdad orders a takeover of Kurdish oilfields; 47,000 women and girls
  were killed by partners or family in 2025 (UN); Euclid finds the most
  distant quasar ever seen.

Every story was verified against reports first published on 24 November
2026 before it was drawn (Sanofi's press release, Reuters, ESA, UN
Women / UNODC, CMSA, the Australian government, AP / AJP, USGS).
Stories first reported on earlier days were deliberately left out — the
leaked Rosstat war-dead figures (23 Nov, the previous lead), the capture
of "El Chapo Isidro" (20–21 Nov), Bukele's Haiti announcement (22–23
Nov), the UK's Myanmar sanctions (23 Nov), the Gaza strikes (23 Nov),
the SpaceX suits (23 Nov) and the Ma spying sentence (23 Nov). Figures
are as reported on the day.

## How to run

```sh
python3 main.py
# writes /output/entry.png (1024x1024 PNG)
```

Requirements: Python 3.12+ and Pillow. No network, no clock, no randomness —
two runs write byte-identical output.

The program renders the page procedurally with the fonts bundled under
`assets/fonts/` (DejaVu Serif/Sans — freely licensed, copied from the
system font directory), so it renders identically on any machine with
Pillow. If rendering fails for any reason (e.g. Pillow missing), it falls
back to copying the pre-rendered image shipped as `assets/entry.png`, so
it still writes a valid entry.

## Layout

- `main.py` — the whole program: data, layout and renderer.
- `assets/entry.png` — pre-rendered fallback image (identical bytes to
  what the renderer produces).
- `assets/fonts/` — bundled DejaVu fonts used by the renderer.

Design: a dark navy masthead with the date set huge, one dominant hero
story with three big stat numbers beside a hand-drawn deal panel, a
2 × 3 digest grid in which every card carries a "24 NOV" chip and a
single verifiable fact line, and a short "Also today" strip with a
source line at the foot — every block sized so no text overlaps or runs
off the page.

## Licence

MIT — see `LICENSE`.
