# The World in One Day — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Ngntier/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Ngntier/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A dense newspaper front page summing up the world's news of
**Tuesday 24 November 2026** in one image: two top stories (the COP31
climate talks collapsing in Antalya, Jensen Huang's return as Nvidia
CEO), a UTC timeline of the day, and 21 more sourced stories across
war and diplomacy, business and tech, science, sport and culture —
every one of them an event that happened, or was first reported, on
24 November 2026.

Entry for the [news-image-20261124](https://make.fun/bounty/news-image-20261124)
bounty on [make.fun](https://make.fun).

## Run it

Pure Python 3 standard library — no dependencies, no network.
The program draws the page pixel by pixel with a hand-built 5x7
bitmap font and writes a PNG with zlib.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png` (1024x1024, under 1 MiB). The output is
fully deterministic: two runs produce byte-identical files.

## License

MIT — see [LICENSE](LICENSE).
