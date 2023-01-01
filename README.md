# CGOL &middot; [![PyPI](https://img.shields.io/pypi/v/CGOL?style=for-the-badge&logo=PyPi)](https://pypi.org/project/CGOL/) [![GitHub release](https://img.shields.io/github/v/release/INeido/CGOL?label=GitHub&style=for-the-badge&logo=GitHub)](https://github.com/INeido/CGOL/releases) ![GitHub repo size](https://img.shields.io/github/repo-size/INeido/CGOL?style=for-the-badge) ![GitHub License](https://img.shields.io/github/license/INeido/CGOL?style=for-the-badge)

A Conway's Game of Life implementation using numpy and pygame.

![](https://github.com/INeido/CGOL/blob/main/samples/logo.png?raw=true)

## Description

This project has no particular aim. It is a purely a personal project and barely maintained.

It is a CLI based [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life): implementation using numpy for fast calculations and pygame for an interactive simulation.

---

Rules of Conway's Game of Life
1. Any live cell with two or three live neighbors survives.
2. Any dead cell with three live neighbors becomes a live cell.
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

## Installing

Install using pip
```bash
pip install cgol
```

Manually install using CLI
```bash
git clone https://github.com/INeido/CGOL
pip install -e CGOL/.
```

## Usage

Here are some examples.

Start a simulation with the default setting but with a custom seed.
```bash
cgol -s 42
```
![](https://github.com/INeido/CGOL/blob/main/samples/demo1.gif?raw=true)

Change grid size, cell size and fade color.
```bash
cgol -cf 130 20 0 -cs 8 -sx 90 -sy 160
```
![](https://github.com/INeido/CGOL/blob/main/samples/demo2.gif?raw=true)

Change the color to white on black without fade.
```bash
cgol -fd 0.0 -ca 255 255 255
```
![](https://github.com/INeido/CGOL/blob/main/samples/demo3.gif?raw=true)

Draw with the mouse to birth or kill cells.

![](https://github.com/INeido/CGOL/blob/main/samples/demo0.gif?raw=true)


## Arguments

```
usage: CGOL [-h] [--res-h RH] [--res-w RW] [--colour-alive CA [CA ...]] [--colour-dead CD [CD ...]] [--colour-fade CF [CF ...]]
            [--colour-background CB [CB ...]] [--cell_size CS] [--size-x SX] [--size-y SY] [--tickrate T] [--seed S] [--save-file F] [--load L]
            [--pause-stalemate PS] [--pause-oscillators PO] [--fade-rate FR] [--fade-death-value FD]

Conway's Game of Life

options:
  -h, --help            show this help message and exit
  --res-h RH, -rh RH    Height of the Game.
  --res-w RW, -rw RW    Width of the Game.
  --colour-alive CA [CA ...], -ca CA [CA ...]
                        Colour for alive cells. 'R G B'
  --colour-dead CD [CD ...], -cd CD [CD ...]
                        Colour for dead cells. 'R G B'
  --colour-fade CF [CF ...], -cf CF [CF ...]
                        Colour to fade dead cells to. 'R G B'
  --colour-background CB [CB ...], -cb CB [CB ...]
                        Colour for dead cells. 'R G B'
  --cell_size CS, -cs CS
                        Size of a cell in pixel.
  --size-x SX, -sx SX   Height of the World.
  --size-y SY, -sy SY   Width of the World.
  --tickrate T, -t T    Number of times the game shall update in a second (FPS).
  --seed S, -s S        Seed value used to create World.
  --save-file F, -f F   Path of the in-/output file. (Should be .csv)
  --load L, -l L        Load revious save.
  --pause-stalemate PS, -ps PS
                        Game pauses on a stalemate.
  --pause-oscillators PO, -po PO
                        Game pauses when only oscillators remain.
  --fade-rate FR, -fr FR
                        Value by which a cell should decrease every generation.
  --fade-death-value FD, -fd FD
                        Value a cell should have after death.
```

| Argument | Description | Default Value |
| ------ | ------ | ------ |
| --res-h (-rh) | Height of the Game. | 720 |
| --res-w (-rw) | Width of the Game. | 1280 |
| --colour-alive (-ca) | Colour for alive cells. 'R G B' | 255, 144, 0 |
| --colour-dead (-cd) | Colour for dead cells. 'R G B' | 0, 0, 0 |
| --colour-fade (-cf) | Colour to fade dead cells to. 'R G B' | 0, 0, 0 |
| --colour-background (-cb) | Colour of background. 'R G B' | 16, 16, 16 |
| --cell-size (-cs) | Size of a cell in pixel | 8 |
| --size-x (-sx) | Height of the World. | 90 |
| --size-y (-sy) | Width of the World. | 160 |
| --tickrate (-t) | Number of times the game shall update in a second (FPS). | 60 |
| --seed (-s) | Seed value used to create World. | -1 |
| --save-file (-f) | Path of the in-/output file. (Should be .csv) | './cgol.csv' |
| --load (-l) | Load revious save. | False |
| --pause-stalemate (-ps) | Game pauses on a stalemate. | False |
| --pause-oscillators (-po) | Game pauses when only oscillators remain. | False |
| --fade-rate (-fr) | Value by which a cell should decrease every generation. | 0.01 |
| --fade-death-value (-fd) | Value a cell should have after death. | 0.5 |

## Controls

| Button | Description |
| ------ | ------ |
| ESC | Closes game. |
| RETURN | Pauses game. |
| Left Click | Births cell. |
| Right Click | Kills cell. |
| Middle Click | Drags screen. |
| Middle Scroll | Zoom in and out. |
| R | Reset game. |
| F | Fill with random cells. |
| A | Fill with alive cells. |
| D | Fill with dead cells. |
| K | Kill alive cells. |
| R | Reset game. |
| L | Load last saved game. |
| S | Save current game. |
| C | Center view. |
| P | Save screenshot. |
| Right Arrow | Forward one generation. |
| + | Extend grid by one cell in every direction. |
| - | Reduce grid by one cell in every direction. |
