Password Generator
==================

A Python script to generate strong passwords that are easy to remember.

Inspired by [xkcd](http://xkcd.com):

![xkcd password strength](http://imgs.xkcd.com/comics/password_strength.png)

## Requirements

### wordlist
It uses a file called `wordlist.txt` in the same directory as source for the 
words to be used. In the package I included a list based on the 
[Oxford 3000](http://oald8.oxfordlearnersdictionaries.com/oxford3000/), but 
you can use any other list.

### PyCrypto (optional)
It's highly recommended that you install [PyCrypto](https://www.dlitz.net/software/pycrypto/), 
so the random number generator is cryptographically secure. It will work without 
it as well, defaulting to Python's own `random` module.

    > pip install pycrypto

or

    > easy_install pycrypto

## Usage
Usage is simple:
    > ./generate_password.py
    correcthorsebatterystaple - correct.horse.battery.staple

You can also generate passwords with a different number of words:

    > ./generate_password.py -w 3
    philosophyobviousfancy - philosophy.obvious.fancy

You also can put constraints on the length of the words to be used, for instance to 
only consider words that are 3 to 5 letters long:

    > ./generate_password.py --min-word-length 3 --max-word-length 5
    backpintwrapready - back.pint.wrap.ready

_Use this carefully, as it might reduce the number of possible words a LOT, resulting in weaker passwords._

Or generate a couple of passwords at the same time to pick one you like:
    
    > ./generate_password.py -n 10
    developmentfalseorganizedonly - development.false.organized.only
    shapekilometrecontrastcouncil - shape.kilometre.contrast.council
    woundtheorybulletgovernor - wound.theory.bullet.governor
    playerderivetwiststressed - player.derive.twist.stressed
    destroyleanindependencehearing - destroy.lean.independence.hearing
    carelessbelllisthang - careless.bell.list.hang
    handleinvolvementheavenbeside - handle.involvement.heaven.beside
    restrictedworsemeandouble - restricted.worse.mean.double
    extremetransparentrollscrew - extreme.transparent.roll.screw
    scaredvalidjewellerycrop - scared.valid.jewellery.crop

Furthermore it can give you some more information about the generated password(s):
    
    > ./generate_password.py -v
    cableheatingtailcombination - cable.heating.tail.combination
    length: 27 chars, size: 127 bits, strength: 47 bits

Finally it has a mode to output all passwords and their info in a tab-separated list for 
further processing. For instance to sort by length:
    
    > ./generate_password.py -w 2 -n 8 -l | sort -nk 3
    sidegreat  side.great	9	43	24
    commitonce	commit.once	10	48	24
    listenslow	listen.slow	10	48	24
    ruinforget	ruin.forget	10	48	24
    easilyplant	easily.plant	11	52	24
    measureborder	measure.border	13	62	24
    determineactor	determine.actor	14	66	24
    vehicleleading	vehicle.leading	14	66	24
