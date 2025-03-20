# CIA - Hackathon 2023-2024


## How to use it
Files:
  - 'game.py' - the main file
  - 'TankLib.py' - the module with the library for every modules
  - 'ModuleGame.py' - the module with the game
  - 'ModuleBot.py' - the module with the bot for enemies
  - 'ModulePlayer.py' - the module with the player's bot
  - 'ModuleTest.py' - A test of player bot
  - 'ModuleDisplay.py' - the module with the display
  - 'ModuleGenerator.py' - the module with the generator of the stage
    - Can be imported and function 'generate_stage' can be used with an argument 'stage' (int) that is the stage to generate

Folders:
  - 'stages' - one file per stage specifying the stage
  - 'original_stages.bak' - Backup of the original stages folder
  - 'logs' - one file per stage with every logs of the stage and a file with result of every stage


## The game
Goal: kill all enemies and survive in a limited time

Rules:
  - Map has a size of [450-800]x[450-650] pixels
  - Tanks can move in 4 directions (up, down, left, right)
  - Tanks can shoot at least 1 bullet and move in 1 direction at a time
  - Tanks have a maximum of bullets present at the same time
  - Tanks can't go through walls
  - Tanks can't go through tanks
  - Bullets can't go through walls
  - Enemies' bullets can go through enemies
  - Player's bullets can go through player
  - Tanks and bullets can't go through the border of the map
  - Tanks have a size of 19x19 pixels
  - Bullets have a size of 5x5 pixels
  - Tanks and bullets are squares
  - Tanks have a speed of 3 pixels per frame
  - Bullets have a speed of 10 pixels per frame
  - Player have a maximum of 5 bullets present at the same time
  - Enemies have a maximum of 3 bullets present at the same time per enemy
  - Every global constant are specified in StageData class
  - A frame is a time unit (1 frame = 1/10 second)
  - In a frame, tanks can move and shoot one time
  - The game is updated every frame
  - During an update, tanks move before bullets
  - The game is over when the player is dead or when all enemies are dead
  - Or when the maximum number of frames is reached
  - The game is won when all enemies are dead
