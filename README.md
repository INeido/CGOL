# CGOL

A whack Conway's Game of Life implementation.

## Description

As the titel says.

## Arguments

| Argument | Description | Default Value |
| ------ | ------ | ------ |
| --size-x (-x) | Height of the World. | 10 |
| --size-y (-y) | Width of the World. | 10 |
| --tickrate (-t) | Number of times the game shall update in a second (FPS). | 1 |
| --seed (-s) | Seed value used to create World. | -1 |
| --toroidal (-o) | Boolean indicating whether the space is toroidal or not. | False |
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