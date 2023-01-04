# CGOL &middot; [![PyPI](https://img.shields.io/pypi/v/CGOL?style=for-the-badge&logo=PyPi)](https://pypi.org/project/CGOL/) [![GitHub release](https://img.shields.io/github/v/release/INeido/CGOL?label=GitHub&style=for-the-badge&logo=GitHub)](https://github.com/INeido/CGOL/releases) ![GitHub repo size](https://img.shields.io/github/repo-size/INeido/CGOL?style=for-the-badge) ![GitHub License](https://img.shields.io/github/license/INeido/CGOL?style=for-the-badge)

A Conway's Game of Life implementation using numpy and pygame.

![](https://github.com/INeido/CGOL/blob/main/samples/logo.png?raw=true)

## Description

This project has no particular aim. It is a purely a personal project and barely maintained.

It is a CLI based [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life): implementation using numpy for fast calculations and pygame for an interactive simulation.

No Hashlife or Quicklife algorithm support (yet).

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
cgol -se 42
```
![](https://github.com/INeido/CGOL/blob/main/samples/demo1.gif?raw=true)

Change grid size, cell size and fade color.
```bash
cgol -cf 130 20 0 -cs 8 -gh 90 -gw 160
```
![](https://github.com/INeido/CGOL/blob/main/samples/demo2.gif?raw=true)

Change the color to white on black without fade.
```bash
cgol -fa False -ca 255 255 255
```
![](https://github.com/INeido/CGOL/blob/main/samples/demo3.gif?raw=true)

Draw with the mouse to birth or kill cells.

![](https://github.com/INeido/CGOL/blob/main/samples/demo0.gif?raw=true)


## Arguments

```
usage: CGOL [-h] [-rw RW] [-rh RH] [-ca CA [CA ...]] [-cd CD [CD ...]] [-cf CF [CF ...]] [-cb CB [CB ...]] [-cs CS] [-gw GW] [-gh GH] [-ti TI] [-se SE]
            [-ps [PS]] [-po [PO]] [-fr FR] [-fd FD] [-to [TO]] [-fa [FA]]

Conway's Game of Life

options:
  -h, --help       show this help message and exit
  -rw RW           Width of the Game.
  -rh RH           Height of the Game.
  -ca CA [CA ...]  Color for alive cells. 'R G B'
  -cd CD [CD ...]  Color for dead cells. 'R G B'
  -cf CF [CF ...]  Color to fade dead cells to. 'R G B'
  -cb CB [CB ...]  Color for dead cells. 'R G B'
  -cs CS           Size of a cell in pixel.
  -gw GW           Width of the World.
  -gh GH           Height of the World.
  -ti TI           Number of times the game shall update in a second (FPS).
  -se SE           Seed value used to create World.
  -ps [PS]         Game pauses on a stalemate.
  -po [PO]         Game pauses when only oscillators remain.
  -fr FR           Value by which a cell should decrease every generation.
  -fd FD           Value a cell should have after death.
  -to [TO]         Enables toroidal space (Cells wrap around edges).
  -fa [FA]         Enables fade effect.
```

| Argument | Description | Default Value |
| ------ | ------ | ------ |
| -rh | Height of the Game. | 720 |
| -rw | Width of the Game. | 1280 |
| -ca | Colour for alive cells. 'R G B' | 255, 144, 0 |
| -cd | Colour for dead cells. 'R G B' | 0, 0, 0 |
| -cf | Colour to fade dead cells to. 'R G B' | 0, 0, 0 |
| -cb | Colour of background. 'R G B' | 16, 16, 16 |
| -cs | Size of a cell in pixel | 8 |
| -sx | Height of the World. | 90 |
| -sy | Width of the World. | 160 |
| -ti | Number of times the game shall update in a second (FPS). | 60 |
| -se | Seed value used to create World. | -1 |
| -ps | Game pauses on a stalemate. | False |
| -po | Game pauses when only oscillators remain. | False |
| -fr | Value by which a cell should decrease every generation. | 0.01 |
| -fd | Value a cell should have after death. | 0.5 |
| -to | Enables toroidal space (Cells wrap around edges). | True |
| -fa | Enables fade effect. | True |

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
