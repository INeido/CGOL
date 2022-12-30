# CGOL

A whack Conway's Game of Life implementation.

## Description

As the titel says.

## Arguments

| Argument | Description | Default Value |
| ------ | ------ | ------ |
| --res-h (-rh) | Height of the Game. | 720 |
| --res-w (-rw) | Width of the Game. | 1280 |
| --colour-alive (-ca) | Colour for alive cells. 'R G B' | 255, 255, 255 |
| ---colour-dead (-cd) | Colour for dead cells. 'R G B' | 0, 0, 0 |
| ---colour-background (-cb) | Colour of background. 'R G B' | 125, 125, 125 |
| ---cell-size (-cs) | Size of a cell in pixel | 16 |
| --size-x (-sx) | Height of the World. | 45 |
| --size-y (-sy) | Width of the World. | 80 |
| --tickrate (-t) | Number of times the game shall update in a second (FPS). | 30 |
| --seed (-s) | Seed value used to create World. | -1 |
| --save-file (-f) | Path of the in-/output file. (Should be .csv) | './cgol.csv' |
| --load (-l) | Load revious save. | False |
| --pause-stalemate (-ps) | Game pauses on a stalemate. | False |
| --pause-oscillators (-po) | Game pauses when only oscillators remain. | False |

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
| L | Load last saved game. |
| S | Save current game. |
| C | Center view. |
| Right Arrow | Forward one generation. |
| + | Extend grid by one cell in every direction. |
| - | Reduce grid by one cell in every direction. |

## Installing

You can install the code and download the requirements with the following commands.
```bash
git clone https://github.com/INeido/CGOL
cd CGOL
pip install -r requirements.txt
```
Finally run the code with.
```bash
python main.py
```