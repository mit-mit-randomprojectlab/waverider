# waverider
A motion-racing game using the Wii Balance Board for Linux/Raspberry Pi.
Game developed by "mit-mit" during Global Game Jam 2017 (theme "Waves").

=============
Requirements:
=============

  Linux/Raspberry Pi: Functions for bluetooth communications with the Wii Balance Board are specific to Linux.

  Python 2.7+ (tested on 2.7.6, should work on earlier versions): http://www.python.org/
  Pygame 1.9+: http://www.pygame.org/
  
  Requires the following packages to be installed: bluez bluez-utils python-bluez

=================
Running the game:
=================

Open a terminal/console/shell, "cd" to the game directory and run the command

  python run_game.py

================
Playing the game
================

When the game first starts, you need to press the red synch button on the bottom of your Wii Balance Board (located inside the battery area).

Lean left or right to control your bead: lean right to go uphill and left to go down. Beat the white bead to the end of the course to proceed to the next level!

=======
Credits
=======

Game Design/Programming/Graphics: mit-mit

"wii_balance_board.py" uses code and methods modified from:
"gr8w8upd8m8" by Stavros Korokithakis
https://github.com/skorokithakis/gr8w8upd8m8

Music and Sound:

"Electrodoodle" by Kevin MacLeod (incompetech.com) 
Licensed under Creative Commons: By Attribution 3.0
http://creativecommons.org/licenses/by/3.0/

"Magical_1_0" by JaggedStone (CC0)
http://opengameart.org/content/magic-spell-sfx

