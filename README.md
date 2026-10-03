# shmupfan MiSTer cores

A MiSTer Downloader / Update All database for the arcade cores published by
[shmupfan](https://github.com/shmupfan). Add it once and every new core and
update arrives with your normal Update All run.

## Install

Add these two lines to `/media/fat/downloader.ini` on your MiSTer SD card:

```ini
[shmupfan]
db_url = https://raw.githubusercontent.com/shmupfan/Distribution/main/db.json
```

Then run Update All (or `downloader`) from the Scripts menu. Cores install to
`_Arcade/cores/` and MRA files to `_Arcade/`, the same places as official
arcade cores. ROMs are not included: use the MAME set named in each core's
README, in `games/mame/`.

## Cores

| Core | Games | Source |
|---|---|---|
| 1945kIII | 1945k III, Solite Spirits, '96 Flag Rally | [Arcade-1945kIII_MiSTer](https://github.com/shmupfan/Arcade-1945kIII_MiSTer) |
| Dooyong | The Last Day, Gulf Storm, Pollux, Flying Tiger, Blue Hawk, Sadari, Gun Dealer '94, Super-X, R-Shark, Pop Bingo | [Arcade-Dooyong_MiSTer](https://github.com/shmupfan/Arcade-Dooyong_MiSTer) |

## Maintainers

`cores.json` lists each core repository and the commit its files are taken
from. After a core release, bump that commit and run `python3 tools/make_db.py`
to rebuild `db.json`. File URLs are pinned to the commit, so existing installs
never see a file change underneath them.
