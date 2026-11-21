# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Anggizx90/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Anggizx90/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page — **THE WORLD TODAY, Saturday 21 November 2026** — summing up the day's world news in a single 1024×1024 image. The lead story is the AI stock rout that dragged the S&P 500 and the Dow into correction and wiped out the Nasdaq's 2026 gains. Twelve further stories cover Russia's biggest strikes of the year on Ukraine and the missiles that landed in Poland, the ICJ's genocide ruling against Myanmar, the UK–EU post-Brexit deals, Houthi missiles fired on Riyadh for a third night, the foiled plot to kill a Ukrainian rapper in Copenhagen, COP31 running past its deadline, Bolsonaro back in hospital, the FBI's crime database being hacked, Trump's warning to tech firms over foreign data centres, the SEC probe into Nvidia, and Estonia shutting its border with Russia — plus a round-up strip (the daraxonrasib cancer pill, GTA VI's $3.8bn first day, the Peru quake, Gen Z protests in 25 countries, the Palisades fire conviction, and Salvadoran soldiers killed in Haiti).

`main.py` (Python 3.13, standard library only) copies the finished `entry.png` to the output directory. `draw_poster.py` is the Pillow program that draws the page from scratch — every illustration is drawn with shapes, no photographs, no network — and writes `entry.png`. Both runs of `main.py` write byte-identical output.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the poster from scratch (needs Pillow):

```sh
python3 draw_poster.py
```

## News sources

All stories were reported 21 November 2026 (Reuters, CNN, BBC, AFP, AP, FT, Guardian, Al Jazeera):

- AI sell-off: S&P 500 −3.7% and Dow into correction; Nasdaq −5.3%, erasing all its 2026 gains; Nikkei −5.1%; gold −4.6%; Anthropic shares down as much as 10%.
- Russia fires 400+ drones and 110 missiles at Ukraine overnight; at least eight killed in Kyiv; bridges and railway stations hit. Two Russian missiles and a suspected drone come down in Poland; PM Tusk calls it a deliberate provocation.
- International Court of Justice finds Myanmar responsible for genocide against the Rohingya.
- UK PM Andy Burnham and EU leaders sign three post-Brexit agreements in Brussels: food exports, carbon markets and youth mobility; 100,000 young Britons gain EU access.
- Saudi-led coalition intercepts three Houthi missiles aimed at Riyadh, the third night in a row.
- Denmark arrests two men and expels a Russian diplomat over a plot to kill Ukrainian rapper Kyivstoner in Copenhagen.
- COP31 climate talks in Antalya run past their deadline, deadlocked over fossil fuels.
- Jailed former Brazilian president Jair Bolsonaro, 71, hospitalised with a near-complete intestinal obstruction.
- FBI investigates an apparent breach of its National Crime Information Center database — the second FBI intrusion in recent months.
- Trump threatens "tremendous penalties" for US tech firms building data centres abroad.
- SEC opens an investigation into Nvidia's accounting after Jensen Huang resigns; Trump urges Nvidia to bring him back.
- Estonia to close its Russia border crossings from 1 December after a GRU-linked arson attempt on drone maker Threod Systems; eight detained.
- Also: trial pill daraxonrasib makes pancreatic tumours undetectable in 1 in 12 patients; GTA VI sets a $3.8bn first-day sales record; a 6.9-magnitude quake shakes the Peruvian Andes; Gen Z protests spread across 25 European countries; a man is convicted of starting LA's Palisades fire; three Salvadoran soldiers are killed handling explosives in Haiti.
