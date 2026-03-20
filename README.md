# roulette_bot
A bot that has roulette games

# How to use the bot
Use `/solo <game mode>` if you want to host a game (2 players). This command has 2 modes: Russian Roulette and Salesman

Use `/single <game mode>` if you want to host a singleplayer game. This command has 1 mode: Russian Roulette

Use `/join <ping the user>` if you want to join a game that the pinged user is in

Use `/leave` if you want to leave a game at any time

# Russian Roulette (Solo) game mode
This game mode will be started if 2 players successfully joined the game (aka one user used `/join` on another user that used `/solo russian roulette`)

How to play:

- On your turn, use `/shoot`. You will have a `1` in `6` chance to lose. This is how Russian Roulette works

# Salesman game mode
This game mode will be started if 2 players successfully joined the game (aka one user use `/join` on another user that used `/solo salesman`)

How to play:

- At the start of the game, one player will take the role of Gi-hun, and the other player will take the role of the Salesman (this choice will be picked randomly by the bot, and this game mode is highly inspired by Squid Games). Gi-hun will go first

- The gun will have `6` chambers, `5` of which is blank and `1` chamber has a bullet. The Salesman inserts a bullet and rolls the shooting wheel

- Each player takes turn shoot at themselves by using `/shoot`, but instead of the normal Russian Roulette (your chances of death resets to `1` in `6` because you roll the shooting wheel after your turn), you don't roll the shooting wheel and pass the gun to the other player

- Whoever is left surviving wins

# Russian Roulette (Singleplayer) game mode
This game mode will be started if you run `/single russian roulette`. The rules are as like normal Russian Roulette, but you play with the bot.

# Salesman (Singleplayer) game mode
This game mode will be started if you run `/single salesman`. The rules are as like normal Salesman, but you play with the bot. You are always Gi-hun in any case, thus you always go first.

# How to host the bot
In case if you wanted to host the bot, here is how you can do it:

1. Install Python `3.12` or above and all of the following in `requirements.txt`

2. Clone this repository and add the following files/folders:

   - `joined_game.json`
  
   - `waiting_games.json`
  
   - `game_data/solo/russian_roulette.json`
  
   - `game_data/solo/salesman.json`

   - `game_data/single/russian_roulette.json`

   - `game_data/single/salesman.json`
  
   - `.env`

   Each `.json` file should be initialized with `{}`

4. Initialize the `.env` file with the following variables:

   - `DISCORD_TOKEN`: Your Discord bot's token
  
   - `GENERAL_ID`: The channel ID for `#general`

5. Host the bot
