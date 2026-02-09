import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from random import randint
import json

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
general_id = int(os.getenv("GENERAL_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

def reset():
    with open("joined_game.json", "w") as file:
        json.dump({}, file)
    
    with open("waiting_games.json", "w") as file:
        json.dump({}, file)
    
    with open("game_data/solo/russian_roulette.json", "w") as file:
        json.dump({}, file)
    
    with open("game_data/solo/salesman.json", "w") as file:
        json.dump({}, file)
    
    with open("game_data/single/russian_roulette.json", "w") as file:
        json.dump({}, file)

def on_leave(user_id):
    user = bot.get_user(int(user_id))
    with open("joined_game.json", "r") as file:
        joined_game = json.load(file)
    
    if user_id not in joined_game or not joined_game[user_id]:
        return f"{user.mention}, you're not in a game or waiting for a game right now!"
    
    with open("waiting_games.json", "r") as file:
        waiting_games = json.load(file)

    if user_id in waiting_games:
        del joined_game[user_id]
        del waiting_games[user_id]
        with open("joined_game.json", "w") as file:
            json.dump(joined_game, file)

        with open("waiting_games.json", "w") as file:
            json.dump(waiting_games, file)

        return f"{user.mention}, you've successfully left the game"
    
    with open("game_data/solo/russian_roulette.json", "r") as file:
        russian_roulette_solo = json.load(file)
    
    if user_id in russian_roulette_solo:
        game_data = russian_roulette_solo[user_id]
        p1_id = game_data[1]
        p2_id = game_data[2]
        
        del joined_game[p1_id]
        del joined_game[p2_id]
        
        del russian_roulette_solo[p1_id]
        del russian_roulette_solo[p2_id]
        
        with open("joined_game.json", "w") as file:
            json.dump(joined_game, file)
        
        with open("game_data/solo/russian_roulette.json", "w") as file:
            json.dump(russian_roulette_solo, file)
            
        if p1_id == user_id:
            winner = bot.get_user(int(p2_id))
            return f"{winner.mention} won by resignation!"
        else:
            winner = bot.get_user(int(p1_id))
            return f"{winner.mention} won by resignation!"
    
    with open("game_data/solo/salesman.json", "r") as file:
    	salesman_solo = json.load(file)
    
    if user_id in salesman_solo:
        game_data = salesman_solo[user_id]
        p1_id = game_data[1]
        p2_id = game_data[2]
        
        del joined_game[p1_id]
        del joined_game[p2_id]
        
        del salesman_solo[p1_id]
        del salesman_solo[p2_id]
        
        with open("joined_game.json", "w") as file:
            json.dump(joined_game, file)
        
        with open("game_data/solo/salesman.json", "w") as file:
            json.dump(salesman_solo, file)
            
        if p1_id == user_id:
            winner = bot.get_user(int(p2_id))
            return f"{winner.mention} won by resignation!"
        else:
            winner = bot.get_user(int(p1_id))
            return f"{winner.mention} won by resignation!"
    
    return "I think someone hacked into the system..."
        
@bot.event
async def on_ready():
    global general
    general = bot.get_channel(general_id)
    
    # Reset all data
    reset()
    print("Bot is online!")

@bot.event
async def on_member_join(member):
    await general.send(f"Greetings, {member.mention}! Welcome to Roulette Games, this is a server where we have roulette games hosted by the bot myself")

@bot.event
async def on_member_remove(member):
    user_id = str(member.id)
    msg = on_leave(user_id)
    
    await ctx.send(msg)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        
    await bot.process_commands(message)

@bot.command()
async def helloworld(ctx):
    await ctx.send("Hello, World!")

@bot.command()
async def solo(ctx, *, game_name: str = ""):
    with open("joined_game.json", "r") as file:
    	joined_game = json.load(file)
    
    user = ctx.author
    user_id = str(user.id)
    if user_id in joined_game and joined_game[user_id]:
        await ctx.send(f"{user.mention}, you are already in a game, or waiting for another game. Please leave the game if you wanted to start a new game")
        return
    
    match game_name.strip().lower():
        case "":
            await ctx.send(f"{user.mention}, it looks like you didn't choose a game mode at all. Please choose a game mode...")
            return
        case "russian roulette":
            pass
        case "salesman":
            pass
        case _:
            await ctx.send(f"{user.mention}, game mode {game_name} does not exist in me...")
            return
            
    with open("waiting_games.json", "r") as file:
        waiting_games = json.load(file)
    
    joined_game[user_id] = True
    waiting_games[user_id] = game_name.strip().lower()
    with open("joined_game.json", "w") as file:
        json.dump(joined_game, file)
        
    with open("waiting_games.json", "w") as file:
        json.dump(waiting_games, file)

    await ctx.send(f"{user.mention}, you're currently waiting with the game mode {game_name}. Please be patient and wait for someone to accept your duel!")

@bot.command()
async def single(ctx, *, game_name: str):
    user = ctx.author
    user_id = str(user.id)
    
    with open("joined_game.json", "r") as file:
        joined_game = json.load(file)
    
    if user_id in joined_game and joined_game[user_id]:
        await ctx.send(f"{user.mention}, you are already in a game, or waiting for another game. Please leave the game if you wanted to start a new game")
        return
    
    joined_game[user_id] = True
    match game_name.strip().lower():
        case "":
            await ctx.send(f"{user.mention}, it looks like you didn't choose a game mode at all. Please choose a game mode...")
            return
        case "russian roulette":
            # Stpre the data of if the player joined a game, which will always store as True
            turn = randint(0, 1)
            await ctx.send(f"{user.mention}, you've successfully joined a singleplayer game with the bot in game mode {game_name}. It's currently {"your" if turn == 0 else "the bot's"} turn")
            if turn == 1:
                if randint(1, 6) == 1:
                    await ctx.send(f"{user.mention}, the bot shot itself in its head. YOU WIN!")
                    return
                else:
                    await ctx.send(f"{user.mention}, the bot shot itself and hit a blank. It's currently your turn. Use /shoot to perform your turn")
                    
            with open("game_data/single/russian_roulette.json", "r") as file:
                russian_roulette_single = json.load(file)
            
            russian_roulette_single[user_id] = True
            with open("game_data/single/russian_roulette.json", "w") as file:
                json.dump(russian_roulette_single, file)
                
            with open("joined_game.json", "w") as file:
                json.dump(joined_game, file)
        case _:
            await ctx.send(f"{user.mention}, game mode {game_name} does not exist in me...")
            return
    
@bot.command()
async def leave(ctx):
    user = ctx.author
    user_id = str(user.id)
    msg = on_leave(user_id)
    
    await ctx.send(msg)

@bot.command()
async def join(ctx, player: discord.Member):
    with open("joined_game.json", "r") as file:
        joined_game = json.load(file)
    
    host_id = str(player.id)
    user = ctx.author
    user_id = str(user.id)
    if user_id in joined_game and joined_game[user_id]:
        await ctx.send(f"{user.mention}, you are in a game or waiting for a game right now, so you can't join another person's game")
        return
    
    if host_id not in joined_game:
        await ctx.send(f"{user.mention}, the user you mentioned is not in a game yet. You can only join someone's game when they are waiting for a player")
        return
    
    with open("waiting_games.json", "r") as file:
        waiting_games = json.load(file)
    
    if host_id not in waiting_games:
        await ctx.send(f"{user.mention}, the user you wanted to join is currently in a game right now. Please wait for them to finish the game")
        return
    
    # START GAME
    match waiting_games[host_id]:
        case "russian roulette":
            # We store the following data as an array
            # [turn, p1, p2] (randomly shuffled)
            # key is the host id and the player id so the bot can access it
            with open("game_data/solo/russian_roulette.json", "r") as file:
                russian_roulette_solo = json.load(file)
                
            stored_data = None
            if randint(0, 1) == 0:
                stored_data = [1, user_id, host_id]
            else:
                stored_data = [1, host_id, user_id]

            russian_roulette_solo[host_id] = stored_data
            russian_roulette_solo[user_id] = stored_data
            with open("game_data/solo/russian_roulette.json", "w") as file:
                json.dump(russian_roulette_solo, file)
            
            with open("waiting_games.json", "r") as file:
                waiting_games = json.load(file)
            
            del waiting_games[host_id]
            with open("waiting_games.json", "w") as file:
                json.dump(waiting_games, file)
            
            with open("joined_game.json", "r") as file:
                joined_game = json.load(file)
            
            joined_game[user_id] = True
            with open("joined_game.json", "w") as file:
                json.dump(joined_game, file)
            
            turn_player = bot.get_user(int(stored_data[stored_data[0]]))
            await ctx.send(f"{player.mention}, {user.mention} managed to join your game! It's currently {turn_player.mention}'s turn. Use /shoot to perform your turn!")
        case "salesman":
            # We store the following data as an array
            # [bullets_left, p1, p2] (turn order randomly shuffled)
            # key is the host id and the player id so the bot can access it
            with open("game_data/solo/salesman.json", "r") as file:
                salesman_solo = json.load(file)
            
            stored_data = None
            if randint(0, 1) == 0:
                stored_data = [6, user_id, host_id]
            else:
                stored_data = [6, host_id, user_id]
            
            salesman_solo[user_id] = stored_data
            salesman_solo[host_id] = stored_data
            with open("game_data/solo/salesman.json", "w") as file:
                json.dump(salesman_solo, file)
            
            del waiting_games[host_id]
            with open("waiting_games.json", "w") as file:
                json.dump(waiting_games, file)
            
            joined_game[user_id] = True
            with open("joined_game.json", "w") as file:
                json.dump(joined_game, file)
            
            gihun = bot.get_user(int(stored_data[1]))
            salesman = bot.get_user(int(stored_data[2]))
            
            await ctx.send(f"{player.mention}, {user.mention} managed to join your game! In this game, {salesman.mention} is the Salesman and {gihun.mention} is Gi-hun. It's currently Gi-hun's ({gihun.mention}'s) turn. Use /shoot to perform your turn! There are **6** chambers left to shoot...")
        case _:
            await ctx.send(f"{user.mention}, you can't join the selected person's game as it does not exist")

@bot.command()
async def shoot(ctx):
    user = ctx.author
    user_id = str(user.id)
    
    # Step 1: Check if the user is in a game
    with open("joined_game.json", "r") as file:
        joined_game = json.load(file)
    
    if user_id not in joined_game:
        await ctx.send(f"{user.mention}, you are currently not in a game, therefore, you can't use this command")
        return
    
    # Step 2: Check if the user is waiting for a game
    with open("waiting_games.json", "r") as file:
        waiting_games = json.load(file)
    
    if user_id in waiting_games:
        await ctx.send(f"{user.mention}, you are currently waiting for a game, therefore, you can't use this command")
        return
    
    # Step 3: Check if the user is in a Russian Roulette (Solo) game
    with open("game_data/solo/russian_roulette.json", "r") as file:
        russian_roulette_solo = json.load(file)
    
    if user_id in russian_roulette_solo:
        # Step 4: Get game data
        game_data = russian_roulette_solo[user_id]

        # Step 5: Check for turn
        current_turn_id = game_data[game_data[0]]
        if user_id != current_turn_id:
            await ctx.send(f"{user.mention}, please wait for your opponent's turn")
            return

        # Step 6: Perform the turn
        game_data[0] = 3-game_data[0]
        next_turn = bot.get_user(int(game_data[game_data[0]]))
        if randint(1, 6) == 1:
            await ctx.send(f"Unfortunately, the bullet went in your head, {user.mention}. You died... {next_turn.mention} WINS!")

            # Step 7: Remove the JSON data
            del joined_game[user_id]
            del joined_game[str(next_turn.id)]

            del russian_roulette_solo[user_id]
            del russian_roulette_solo[str(next_turn.id)]

            with open("joined_game.json", "w") as file:
                json.dump(joined_game, file)

            with open("game_data/solo/russian_roulette.json", "w") as file:
                json.dump(russian_roulette_solo, file)
            
            return

        await ctx.send(f"Luckily, you triggered a blank chamber, and you did not die. It's {next_turn.mention}'s turn. Use /shoot to perform your turn!")

        # Step 7: Save the JSON state
        russian_roulette_solo[user_id] = game_data
        russian_roulette_solo[str(next_turn.id)] = game_data

        with open("game_data/solo/russian_roulette.json", "w") as file:
            json.dump(russian_roulette_solo, file)
        
        return
    
    # Step 4: Check if the user is in a Salesman (Solo) game
    with open("game_data/solo/salesman.json", "r") as file:
        salesman_solo = json.load(file)
    
    if user_id in salesman_solo:
        # Step 5: Get game data
        game_data = salesman_solo[user_id]
        
        # Step 6: Check for turn
        turn_idx = game_data[0] % 2 + 1
        turn_id = game_data[turn_idx]
        
        if user_id != turn_id:
            await ctx.send(f"{user.mention}, please wait for your opponent's turn")
            return
        
        # Step 7: Perform the turn
        gihun = bot.get_user(int(game_data[1]))
        salesman = bot.get_user(int(game_data[2]))
        if game_data[0] == 4:
            await ctx.send(f"Salesman ({salesman.mention}): I've always wondered how you made it out of there alive. For one thing, you were even terrible at ddakji")
        elif game_data[0] == 2:
            await ctx.send(f"Salesman ({salesman.mention}): What's the matter? Is your mind starting to race? Now your odds of death are 1 in 2. That's pretty high indeed. I'm sure you're afraid. Lots going through your mind. Let me guess what you're thinking right now. \"The gun is in my hand. Screw the rules, pull the trigger once or twice, and I can blow this guy's face off\". Isn't that right? If you wanted to meet the person you mentioned earlier, the key is in my pocket. You can simply shoot me with the gun and take it. But I'll have to admit to you one thing. That you're a piece of trash, just like everyone else. A piece of trash who got lucky and made it out of the dumpster.")
        elif game_data[0] == 1:
            await ctx.send(f"Gi-hun ({gihun.mention}): What's the matter? Is your mind starting to race? That's right. Screw the rules. Now, with a single pull of the trigger, you could kill me. But, I'll have you admit one thing. You put a mask over your face and do whatever your master says. You run, bark, and wag your tail for them. You're nothing more than their dog.")
        
        if randint(1, game_data[0]) == 1:
            if turn_idx == 1:
                await ctx.send(f"Gi-hun ({gihun.mention}) got shot in the head and died! The Salesman ({salesman.mention}) WINS!")
            else:
                await ctx.send(f"The Salesman ({salesman.mention}) got shot in the head and died! Gi-hun ({gihun.mention}) WINS!")
            
            # Step 8: Remove the JSON data
            del joined_game[game_data[1]]
            del joined_game[game_data[2]]
            
            del salesman_solo[game_data[1]]
            del salesman_solo[game_data[2]]
            
            with open("joined_game.json", "w") as file:
                json.dump(joined_game, file)
            
            with open("game_data/solo/salesman", "w") as file:
                json.dump(salesman_solo, file)
            
            return
        
        game_data[0] -= 1
        if turn_idx == 1:
        	await ctx.send(f"Luckily, Gi-hun ({gihun.mention}), you hit a blank chamber. It's now the Salesman's ({salesman.mention}'s) turn. There are **{game_data[0]}** chambers left. Use /shoot to perform your turn")
        else:
            await ctx.send(f"Luckily, the Salesman ({salesman.mention}), you hit a blank chamber. It's now Gi-hun's ({gihun.mention}'s) turn. There are **{game_data[0]}** chambers left. Use /shoot to perform your turn")
        
		# Step 8: Save the JSON state
        salesman_solo[game_data[1]] = game_data
        salesman_solo[game_data[2]] = game_data
        
        with open("game_data/solo/salesman.json", "w") as file:
            json.dump(salesman_solo, file)
            
        return
    
    # Step 5: Check if a player is in a Russian Roulette (Single) game
    with open("game_data/single/russian_roulette.json", "r") as file:
        russian_roulette_single = json.load(file)
    
    if user_id in russian_roulette_single:
        # Step 6: Perform your turn
        if randint(1, 6) == 1:
            await ctx.send(f"{user.mention}, you shot yourself in the head and died... THE BOT WINS!")
            
            # Step 7: Remove the JSON data
            with open("joined_game.json", "r") as file:
                joined_game = json.load(file)
            
            del joined_game[user_id]
            del russian_roulette_single[user_id]
            with open("game_data/single/russian_roulette.json", "w") as file:
                json.dump(russian_roulette_single, file)
            
            with open("joined_game.json", "w") as file:
                json.dump(joined_game, file)
            
            return
        
        # Step 7: Perform bot's turn
        if randint(1, 6) == 1:
            await ctx.send(f"{user.mention}, you didn't die, and the bot shot itself in its head. YOU WIN!")
            
            # Step 8: Remove the JSON data
            with open("joined_game.json", "r") as file:
                joined_game = json.load(file)
            
            del joined_game[user_id]
            del russian_roulette_single[user_id]
            with open("game_data/single/russian_roulette.json", "w") as file:
                json.dump(russian_roulette_single, file)
            
            with open("joined_game.json", "w") as file:
                json.dump(joined_game, file)
                
            return
        else:
            await ctx.send(f"{user.mention}, you didn't die, and the bot shot itself and hit a blank. It's currently your turn. Use /shoot to perform your turn")
        
        return
    
    await ctx.send(f"{user.mention}, you are not in a game where you can use /shoot, therefore, you can't use this command")
    
bot.run(token)
