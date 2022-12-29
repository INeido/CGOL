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
| --size-x (-sx) | Height of the World. | 45 |
| --size-y (-sy) | Width of the World. | 80 |
| --tickrate (-t) | Number of times the game shall update in a second (FPS). | 30 |
| --seed (-s) | Seed value used to create World. | -1 |
| --save-file (-f) | Path of the in-/output file. (Should be .csv) | './cgol.csv' |
| --load (-l) | Boolean determining if a previous save should be loaded. | False |

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

## Controls

| Button | Description |
| ------ | ------ |
| ESC | Closes game. |
| RETURN | Pauses game. |
| Left Click | Births cell. |
| Right Click | Kills cell. |
| Middle Click | Drags screen. |