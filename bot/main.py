import discord
from discord.ext import commands, tasks
import os
import random
from datetime import datetime

# ===== SETTINGS =====
TOKEN = os.environ.get("DISCORD_TOKEN")
PREFIX = "!"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ===== FOOD LIST =====
food_list = [
    "🍕 Pizza",
    "🍔 Burger",
    "🍟 Fries",
    "🍩 Donut",
    "🍣 Sushi",
    "🥪 Sandwich",
    "🌮 Taco",
    "🍜 Ramen",
    "🍦 Ice Cream"
]

# ===== MEMBER INVENTORY =====
inventory = {}

# ===== DAILY SPECIAL =====
daily_special = random.choice(food_list)
def update_daily_special():
    global daily_special
    daily_special = random.choice(food_list)

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready to serve food!")
    await bot.change_presence(activity=discord.Game("Serving tasty treats!"))
    daily_special_task.start()

# ===== TASKS =====
@tasks.loop(hours=24)
async def daily_special_task():
    update_daily_special()

# ===== COMMANDS =====
@bot.command()
async def eat(ctx):
    """Get a random food item."""
    food = random.choice(food_list)
    user_id = str(ctx.author.id)
    inventory.setdefault(user_id, []).append(food)
    await ctx.send(f"{ctx.author.mention} ate {food}!")
    if random.randint(1, 4) == 1:
        await ctx.message.add_reaction("😋")

@bot.command()
async def menu(ctx):
    """See the food menu."""
    menu_text = "**Today's Menu:**\n" + "\n".join(food_list)
    await ctx.send(menu_text)

@bot.command()
async def my_food(ctx):
    """See what you've eaten."""
    user_id = str(ctx.author.id)
    foods = inventory.get(user_id, [])
    if foods:
        await ctx.send(f"{ctx.author.mention}, you've eaten: " + ", ".join(foods))
    else:
        await ctx.send(f"{ctx.author.mention}, you haven't eaten anything yet!")

@bot.command()
async def special(ctx):
    """See today's special food."""
    await ctx.send(f"Today's special is: {daily_special}!")

# ===== INTERACTIVE COMMANDS =====
@bot.command()
async def serve(ctx, member: discord.Member):
    """Serve a random food item to another member."""
    food = random.choice(food_list)
    user_id = str(member.id)
    inventory.setdefault(user_id, []).append(food)
    await ctx.send(f"{ctx.author.mention} served {food} to {member.mention}! 🍽️")

@bot.command()
async def steal(ctx, member: discord.Member):
    """Try to steal a random food item from another member."""
    thief_id = str(ctx.author.id)
    victim_id = str(member.id)
    victim_food = inventory.get(victim_id, [])
    if not victim_food:
        await ctx.send(f"{ctx.author.mention}, {member.mention} has no food to steal!")
        return

    # 50% chance to succeed
    if random.choice([True, False]):
        stolen_food = random.choice(victim_food)
        victim_food.remove(stolen_food)
        inventory.setdefault(thief_id, []).append(stolen_food)
        await ctx.send(f"{ctx.author.mention} successfully stole {stolen_food} from {member.mention}! 😏")
    else:
        await ctx.send(f"{ctx.author.mention} tried to steal from {member.mention} but failed! 😢")

# ===== RUN BOT =====
bot.run(TOKEN)
