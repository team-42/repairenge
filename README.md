# Repairenge

Repairenge is a 2D space arcade game created during the Global Game Jam 2020 at the jam site in Leipzig, Germany.

## Objective

In Repairenge, you control a space ship and try to survive attacks by other ships. There are regular opponents and boss enemies to defeat. To accomplish this, you will need to gather more components for your own ship.

## Controls

To move, use the W,A,S,D keys. To fire regular weapons, use the space bar. To fire special weapons (e.g. the railgun), use Enter.

The game can also be played with a game controller. However, not all controllers will work.

## Running the game

To run the game, either clone the repository and run `python repairenge.py` or download a [pre-built release](https://github.com/team-42/repairenge/releases) for your platform and run the game executable (e.g. repairenge.exe). If you don't have that yet, you may need to download pyglet first:

    pip install pyglet

## Building the game

To build an executable, execute

    ./build.sh

in the main directory. If you don't have pyinstaller yet, use

    pip install pyinstaller
    
first.

## Credits

### Game Jam Team

We have developed the game idea, source code and all sound ourselves. The team consisted of:

* Ada Schmidt
* merando
* parti
* PhilippEins
* SharkofMetal

### Libraries

This game was developed with the [pyglet library](https://github.com/pyglet/pyglet).
We very much appreciate their approach for providing a simple to use cross-platform windowing and multimedia library for Python.

### Third-party contributions

The enemy ship bodies as well as several components have been taken from
* https://craftpix.net/freebies/free-pixel-art-enemy-spaceship-2d-sprites/
* https://opengameart.org/content/nihil-ace-spaceship-building-pack-expansion by [Buch](https://opengameart.org/users/buch) 
* https://opengameart.org/content/set-faction4-spaceships by [MillionthVector](http://millionthvector.blogspot.de)

Credits also to the Global Game Jam for creating a weekend full of creativity all around the globe.
