# roulette_bot
A bot that has roulette games

# How to use the bot
Use `/solo <game mode>` if you want to host a game (2 players). This command has 2 modes: Russian Roulette and Salesman

Use `/join <ping the user>` if you want to join a game that the pinged user is in

Use `/leave` if you want to leave a game at any time

# Russian Roulette (Solo) game mode
This game mode will be started if 2 players successfully joined the game (aka one user used `/join` on another user that used `/solo russian roulette`)

How to play:

- On your turn, use `/shoot`. You will have a `1` in `6` chance to lose. This is how Russian Roulette works

# Salesman game mode
This game mode will be started if 2 players successfully joined the game (aka one user use `/join` on aother user that used `/solo salesman`)

How to play:

- At the start of the game, one player will take the role of Gi-hun, and the other player will take the role of the Salesman (this choice will be picked randomly by the bot, and this game mode is highly inspired by Squid Games). Gi-hun will go first

- The gun will have `6` chambers, `5` of which is blank and `1` chamber has a bullet. The Salesman inserts a bullet and rolls the shooting wheel

- Each player takes turn shoot at themselves by using `/shoot`, but instead of the normal Russian Roulette (your chances of death resets to `1` in `6` because you roll the shooting wheel after your turn), you don't roll the shooting wheel and pass the gun to the other player

- Whoever is left surviving wins
