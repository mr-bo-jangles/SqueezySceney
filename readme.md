
#Quick and dirty FoundryVTT Scene resizer

No warranty, no nothing.. if this breaks your scenes or legs I'm not liable got it?

## Installation

```
~/P/SqueezySceney ❯❯❯ pipenv sync
Courtesy Notice: Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project. You can set PIPENV_IGNORE_VIRTUALENVS=1 to force pipenv to ignore that environment and create its own instead. You can set PIPENV_VERBOSITY=-1 to suppress this warning.
Installing dependencies from Pipfile.lock (34f698)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 0/0 — 00:00:00
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
All dependencies are now up-to-date!
```

## Usage

```
python main.py <input filename> <output filename> <decimal scale value>
```

The decimal scale value is based on 1 as the current size, aka 100%.
For example if you wanted to resize your scene down by 72% you'd do the following:
```
~/P/SqueezySceney ❯❯❯ pipenv shell
Launching subshell in virtual environment...
(SqueezySceney) ~/P/SqueezySceney ❯❯❯ python main.py ~/Downloads/Brazenthrone.fvttadv ./backup.fvttadv 0.72
input_filename: /home/josh/Downloads/Brazenthrone.fvttadv. output_filename: /home/josh/PycharmProjects/SqueezySceney/backup.fvttadv. scale: 0.7199999999999999733546474089962430298328399658203125
Processing scene/L1smabYvMPHPVcTE.json
Processing scene/thr1FnwdAVIm8KBp.json
Processing scene/21QR5V87fEqpKuny.json
Processing scene/bbwr1a0pnUk129od.json
Processing scene/Q5GU8CEF027KCbhb.json
Processing scene/3zXtjTrtRu8mumf7.json
Processing scene/UZAvLOVcigySJkml.json
__pycache__  backup.fvttadv  main.py  Pipfile  Pipfile.lock  readme.md  scaler.py
(SqueezySceney) ~/P/SqueezySceney ❯❯❯ 
```

You would then end up with a backup.fvttadv in the current directory that you can re-import via Foundry Adventure import/exporter
