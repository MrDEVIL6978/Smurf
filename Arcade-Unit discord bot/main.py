import asyncio
import json
import os
import random
import time
from collections import defaultdict
from datetime import datetime, timedelta
import discord
import decimal
from discord.ext import commands, tasks
from dotenv import load_dotenv
from ITEMS_LISTS import FISHING_RODS, FISHING_ITEMS, FISHING_LOCATIONS, FishingRod, FISHING_BAITS, FISHING_ACCESSORIES, FishingItem, FishingLocation, FishingBait, FishingAccessory

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

DEFAULT_PREFIX = '?'
PREFIXES_FILE = 'prefixes.json'


#Function to get the prefix for a specific guild
def get_prefix(bot, message):
    if not message.guild:
        return DEFAULT_PREFIX
    try:
        with open(PREFIXES_FILE, 'r') as f:
            prefixes = json.load(f)
        return prefixes.get(str(message.guild.id), DEFAULT_PREFIX)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_PREFIX


bot = commands.Bot(command_prefix=get_prefix, intents=intents)

if not os.path.exists(PREFIXES_FILE):
    with open(PREFIXES_FILE, 'w') as f:
        json.dump({}, f)

#BOOM BAAM BADA BAP BOOM, POW !!!


# Load data from JSON files
def load_data(filename):
    if not os.path.exists(filename):
        print(f"File {filename} does not exist. Creating a new one.")
        save_data(filename, {})
        return {}

    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print(
            f"Error reading {filename}. File may be corrupted. Backing up and creating a new one."
        )
        backup_and_reset_file(filename)
        return {}


def backup_and_reset_file(filename):
    if os.path.exists(filename):
        backup_name = f"{filename}.backup"
        os.rename(filename, backup_name)
        print(f"Corrupted file backed up as {backup_name}")
    save_data(filename, {})
    print(f"Created new empty file: {filename}")


def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def reset_json_file(filename):
    with open(filename, 'w') as f:
        json.dump({}, f)
    print(f"{filename} has been reset to an empty JSON object.")


# Define file names
BANK_FILE = "bank_data.json"
CASH_FILE = "cash_data.json"
DAILY_REWARD_FILE = "daily_reward_data.json"
INVENTORY_FILE = "inventory_data.json"
FISHING_ROD_FILE = "fishing_rod_data.json"
FARM_FILE = "farm_data.json"
LEADERBOARD_FILE = "leaderboard_data.json"
EXPEDITION_FILE = "expedition_data.json"
CRAFTING_FILE = "crafting_data.json"
HOE_FILE = "hoe_data.json"
PICKAXE_FILE = "pickaxe_data.json"
SWORD_FILE = "sword_data.json"
ACCESSORIES_FILE = "accessories_data.json"
PUPPIES_FILE = "puppies_data.json"
AUCTION_FILE = "auction_data.json"
OPEN_AUCTION_FILE = "open_auction_data.json"
PLAYER_DATA = "player_data.json"
GUILD_DATA = "guild_data.json"
FISHING_LOCATIONS_FILE = "fishing_locations_data.json"
daily_cooldowns_file = "daily_cooldowns_data.json"
streaks_file = "streaks_data.json"
streak_bonuses_file = "streak_bonuses_data.json"

# Load data
inventory_data = load_data(INVENTORY_FILE)
fishing_rod_data = load_data(FISHING_ROD_FILE)
fishing_locations_data = load_data(FISHING_LOCATIONS_FILE)
accessories_data = load_data(ACCESSORIES_FILE)
player_data = load_data(PLAYER_DATA)
daily_cooldowns = load_data(daily_cooldowns_file)
streaks = load_data(streaks_file)
streak_bonuses = load_data(streak_bonuses_file)


def initialize_data():
    files = [
        INVENTORY_FILE, PLAYER_DATA, BANK_FILE, CASH_FILE, DAILY_REWARD_FILE,
        FARM_FILE, LEADERBOARD_FILE, EXPEDITION_FILE, CRAFTING_FILE, HOE_FILE,
        PICKAXE_FILE, SWORD_FILE, AUCTION_FILE, OPEN_AUCTION_FILE, GUILD_DATA,
        daily_cooldowns_file, streaks_file, streak_bonuses_file, PUPPIES_FILE
    ]
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                json.dump({}, f)


initialize_data()

# Helper functions


def load_player_data():
    try:
        with open(PLAYER_DATA, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_player_data(data):
    with open(PLAYER_DATA, 'w') as f:
        json.dump(data, f, indent=4)


def add_xp(user_id, xp_amount):
    data = load_player_data()
    if str(user_id) not in data:
        data[str(user_id)] = {'xp': 0, 'level': 0}
    data[str(user_id)]['xp'] += xp_amount
    data[str(user_id)]['level'] = calculate_level(data[str(user_id)]['xp'])
    save_player_data(data)


def calculate_level(xp):
    return xp // 100  # Increase level every 100 XP


def get_xp(user_id):
    data = load_player_data()
    return data.get(str(user_id), {}).get('xp', 0)


def get_level(user_id):
    data = load_player_data()
    return data.get(str(user_id), {}).get('level', 0)


def get_user_inventory(user_id):
    with open('inventory_data.json', 'r') as f:
        inventories = json.load(f)
    user_inventory = inventories.get(str(user_id), {})

    # Ensure all categories are present
    categories = ["rods", "baits", "accessories", "fish", "other"]
    for category in categories:
        if category not in user_inventory:
            user_inventory[category] = {}

    # Normalize item names in the inventory
    for category in user_inventory:
        user_inventory[category] = {
            k.replace(" ", "_"): v
            for k, v in user_inventory[category].items()
        }

    return user_inventory


def update_user_inventory(user_id, category, item, amount):
    user_id = str(user_id)
    with open('inventory_data.json', 'r') as f:
        all_inventories = json.load(f)

    if user_id not in all_inventories:
        all_inventories[user_id] = {
            "rods": {},
            "baits": {},
            "accessories": {},
            "fish": {},
            "other": {}
        }

    if category not in all_inventories[user_id]:
        all_inventories[user_id][category] = {}

    normalized_item = item.replace(" ", "_")
    all_inventories[user_id][category][
        normalized_item] = all_inventories[user_id][category].get(
            normalized_item, 0) + amount

    with open('inventory_data.json', 'w') as f:
        json.dump(all_inventories, f, indent=4)


def remove_from_inventory(user_id, category, item_name, amount=1):
    if user_id in inventory_data and item_name in inventory_data[user_id]:
        inventory_data[user_id][item_name] -= amount
        if inventory_data[user_id][item_name] <= 0:
            del inventory_data[user_id][item_name]
        save_data(INVENTORY_FILE, inventory_data)


@bot.command(name="level")
async def level(ctx):
    user_id = str(ctx.author.id)
    player_data = load_player_data()

    if user_id not in player_data:
        await ctx.send(
            "You haven't started fishing yet! Use the `?fish` command to begin."
        )
        return

    xp = player_data[user_id].get("xp", 0)
    level = calculate_level(xp)
    xp_for_next_level = (level + 1) * 100  # Assuming 100 XP per level

    embed = discord.Embed(title="🎣 Fishing Level", color=0x00ff00)
    embed.add_field(name="Current Level", value=level, inline=False)
    embed.add_field(name="Current XP", value=xp, inline=True)
    embed.add_field(name="XP for Next Level",
                    value=xp_for_next_level,
                    inline=True)
    embed.add_field(name="Progress",
                    value=f"{xp}/{xp_for_next_level} XP",
                    inline=False)

    progress_bar = "█" * int((xp % 100) / 10) + "░" * (10 - int(
        (xp % 100) / 10))
    embed.add_field(name="Progress Bar", value=progress_bar, inline=False)

    await ctx.send(embed=embed)


#equip function:
@bot.command(name="equip")
async def equip(ctx, item_type: str, *, item: str):
    user_id = str(ctx.author.id)
    inventory = get_user_inventory(user_id)

    item_type = item_type.lower()
    if item_type not in ["rod", "bait", "accessory"]:
        await ctx.send(
            "Invalid category. You can only equip rods, baits, or accessories."
        )
        return

    category = "accessories" if item_type == "accessory" else item_type + "s"
    normalized_input = item.lower().replace(' ', '_')

    matching_item = next(
        (inv_item for inv_item in inventory[category].keys()
         if inv_item.lower().replace(' ', '_') == normalized_input), None)

    if matching_item is None:
        available_items = ", ".join(inventory[category].keys())
        embed = discord.Embed(title="❌ Equip Failed", color=0xff0000)
        embed.add_field(name="Error",
                        value=f"You don't have a {item} to equip.",
                        inline=False)
        embed.add_field(name="Available Items",
                        value=available_items if available_items else "None",
                        inline=False)
        await ctx.send(embed=embed)
        return

    player_data = load_player_data()
    if user_id not in player_data:
        player_data[user_id] = {}
    if "equipped" not in player_data[user_id]:
        player_data[user_id]["equipped"] = {}

    old_item = player_data[user_id]["equipped"].get(item_type)
    player_data[user_id]["equipped"][item_type] = matching_item
    save_player_data(player_data)

    embed = discord.Embed(title="✅ Item Equipped", color=0x00ff00)
    embed.add_field(name="Item", value=matching_item, inline=True)
    embed.add_field(name="Type", value=item_type.capitalize(), inline=True)
    if old_item:
        embed.add_field(name="Replaced", value=old_item, inline=True)

    if item_type == "rod":
        rod_info = FISHING_RODS[matching_item]
        embed.add_field(name="Durability",
                        value=rod_info.durability,
                        inline=True)
        embed.add_field(name="Efficiency",
                        value=rod_info.efficiency,
                        inline=True)
        embed.add_field(name="Luck", value=rod_info.luck, inline=True)
    elif item_type == "bait":
        bait_info = FISHING_BAITS[matching_item]
        embed.add_field(name="Efficiency",
                        value=bait_info.efficiency,
                        inline=True)
    elif item_type == "accessory":
        acc_info = FISHING_ACCESSORIES[matching_item]
        embed.add_field(name="Luck Bonus", value=acc_info.luck, inline=True)
        embed.add_field(name="Efficiency Bonus",
                        value=acc_info.efficiency,
                        inline=True)

    embed.set_footer(text=f"Equipped by {ctx.author.name}")
    await ctx.send(embed=embed)


def update_equipped_rod(user_id, rod):
    player_data = load_player_data()
    if user_id not in player_data:
        player_data[user_id] = {}
    if "equipped" not in player_data[user_id]:
        player_data[user_id]["equipped"] = {}
    player_data[user_id]["equipped"]["rod"] = rod
    save_player_data(player_data)


def update_equipped_bait(user_id, bait):
    player_data = load_player_data()
    if user_id not in player_data:
        player_data[user_id] = {}
    if "equipped" not in player_data[user_id]:
        player_data[user_id]["equipped"] = {}
    player_data[user_id]["equipped"]["bait"] = bait
    save_player_data(player_data)


def update_equipped_accessory(user_id, accessory):
    player_data = load_player_data()
    if user_id not in player_data:
        player_data[user_id] = {}
    if "equipped" not in player_data[user_id]:
        player_data[user_id]["equipped"] = {}
    if "accessory" not in player_data[user_id]["equipped"]:
        player_data[user_id]["equipped"]["accessory"] = []
    if accessory not in player_data[user_id]["equipped"]["accessory"]:
        player_data[user_id]["equipped"]["accessory"].append(accessory)
    save_player_data(player_data)


#unequipe function:


@bot.command(name="unequip")
async def unequip(ctx, item_type: str):
    user_id = str(ctx.author.id)
    player_data = load_player_data()

    item_type = item_type.lower()
    if item_type not in ["rod", "bait", "accessory"]:
        await ctx.send(
            "Invalid category. You can only unequip rods, baits, or accessories."
        )
        return

    if user_id not in player_data or "equipped" not in player_data[
            user_id] or item_type not in player_data[user_id]["equipped"]:
        embed = discord.Embed(title="❌ Unequip Failed", color=0xff0000)
        embed.add_field(name="Error",
                        value=f"You don't have any {item_type} equipped.",
                        inline=False)
        await ctx.send(embed=embed)
        return

    unequipped_item = player_data[user_id]["equipped"][item_type]
    del player_data[user_id]["equipped"][item_type]
    save_player_data(player_data)

    embed = discord.Embed(title="🔄 Item Unequipped", color=0xffa500)
    embed.add_field(name="Item", value=unequipped_item, inline=True)
    embed.add_field(name="Type", value=item_type.capitalize(), inline=True)
    embed.set_footer(text=f"Unequipped by {ctx.author.name}")
    await ctx.send(embed=embed)


#inventory:
@bot.command(name="inventory", aliases=["inv"])
async def inventory(ctx):
    user_id = str(ctx.author.id)
    inventory = get_user_inventory(user_id)

    if not inventory:
        await ctx.send("Your inventory is empty.")
        return

    embeds = []
    categories = ["Rods", "Baits", "Accessories", "Fish", "Other"]

    for category in categories:
        embed = discord.Embed(title=f"{ctx.author.name}'s {category}",
                              color=0x00ff00)
        items = inventory.get(category.lower(), {})
        if items:
            for item, amount in items.items():
                embed.add_field(name=item.replace("_", " "),
                                value=f"Amount: {amount}",
                                inline=True)
        else:
            embed.description = f"No {category.lower()} in your inventory."
        embeds.append(embed)

    # Send the first embed
    message = await ctx.send(embed=embeds[0])

    # Add navigation reactions
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

    current_page = 0
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add",
                                                timeout=60.0,
                                                check=check)
            if str(reaction.emoji) == "▶️" and current_page < len(embeds) - 1:
                current_page += 1
                await message.edit(embed=embeds[current_page])
            elif str(reaction.emoji) == "◀️" and current_page > 0:
                current_page -= 1
                await message.edit(embed=embeds[current_page])
            await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.clear_reactions()
            break


#to see equipped items :
@bot.command(name="equipped")
async def equipped(ctx):
    user_id = str(ctx.author.id)
    player_data = load_player_data()

    if user_id not in player_data or "equipped" not in player_data[user_id]:
        await ctx.send("You don't have any items equipped.")
        return

    equipped_items = player_data[user_id]["equipped"]

    embed = discord.Embed(title=f"🎒 {ctx.author.name}'s Equipped Items",
                          color=0x00ff00)

    for item_type in ["rod", "bait", "accessory"]:
        item = equipped_items.get(item_type, "None")
        embed.add_field(name=item_type.capitalize(), value=item, inline=False)

        if item != "None":
            if item_type == "rod":
                rod_info = FISHING_RODS[item]
                embed.add_field(
                    name="Rod Stats",
                    value=
                    f"Durability: {rod_info.durability}\nEfficiency: {rod_info.efficiency}\nLuck: {rod_info.luck}",
                    inline=True)
            elif item_type == "bait":
                bait_info = FISHING_BAITS[item]
                embed.add_field(name="Bait Stats",
                                value=f"Efficiency: {bait_info.efficiency}",
                                inline=True)
            elif item_type == "accessory":
                acc_info = FISHING_ACCESSORIES[item]
                embed.add_field(
                    name="Accessory Stats",
                    value=
                    f"Luck Bonus: {acc_info.luck}\nEfficiency Bonus: {acc_info.efficiency}",
                    inline=True)

    await ctx.send(embed=embed)


@bot.command(name="locations")
async def locations(ctx):
    user_id = str(ctx.author.id)
    player_data = load_player_data()

    if user_id not in player_data:
        await ctx.send(
            "You haven't started fishing yet! Use the `?fish` command to begin."
        )
        return

    level = calculate_level(player_data[user_id].get("xp", 0))
    unlocked_locations = get_unlocked_locations(level)
    current_location = player_data[user_id].get("fishing_location",
                                                "Calm Lake")

    embed = discord.Embed(title="🗺️ Fishing Locations", color=0x00ff00)
    for location in FISHING_LOCATIONS:
        status = "🔓 Unlocked" if location in unlocked_locations else "🔒 Locked"
        if location == current_location:
            status += " (Current)"
        embed.add_field(name=location, value=status, inline=False)

    await ctx.send(embed=embed)


@bot.command(name="fish")
async def fish(ctx):
    user_id = str(ctx.author.id)
    player_data = load_player_data()
    if user_id not in player_data or "equipped" not in player_data[user_id]:
        await ctx.send(
            "You need to equip a fishing rod and bait before fishing!")
        return

    equipped_items = player_data[user_id]["equipped"]
    rod_name = equipped_items.get("rod")
    bait_name = equipped_items.get("bait")
    accessory_name = equipped_items.get("accessory")

    if not rod_name or not bait_name:
        await ctx.send(
            "You need to equip both a fishing rod and bait before fishing!")
        return

    if rod_name not in FISHING_RODS:
        await ctx.send("Error: Invalid fishing rod equipped.")
        return

    rod = FISHING_RODS[rod_name]
    bait = FISHING_BAITS[bait_name]
    accessory = FISHING_ACCESSORIES.get(accessory_name, {
        "luck": 1.0,
        "efficiency": 1.0,
        "catch_bonus": 0
    })

    # Check bait quantity
    bait_quantity = get_user_inventory(user_id)["baits"].get(bait_name, 0)
    if bait_quantity <= 0:
        await ctx.send(
            f"You've run out of {bait_name}! Please equip a new bait.")
        del player_data[user_id]["equipped"]["bait"]
        save_player_data(player_data)
        return

    current_location = player_data[user_id].get("fishing_location",
                                                "Calm Lake")

    embed = discord.Embed(title="🎣 Fishing Expedition", color=0x00ff00)
    embed.add_field(
        name="Equipment",
        value=f"Rod: {rod_name} (Durability: {rod.durability})\n"
        f"Location: {current_location}\n"
        f"Accessory: {accessory_name if accessory_name else 'None'}\n"
        f"Bait: {bait_name} (Quantity: {bait_quantity})",
        inline=False)
    embed.set_image(
        url=
        "https://www.wikihow.com/images/thumb/2/25/Fish-Step-1-Version-3.jpg/v4-460px-Fish-Step-1-Version-3.jpg.webp"
    )
    message = await ctx.send(embed=embed)

    # Calculate wait time based on efficiency
    total_efficiency = rod.efficiency * accessory[
        "efficiency"] * bait.efficiency
    wait_time = max(5, 16 - (total_efficiency - 1) * 5)

    await asyncio.sleep(wait_time)

    embed.set_image(
        url=
        "https://www.wikihow.com/images/thumb/8/8b/Fish-Step-4-Version-3.jpg/v4-460px-Fish-Step-4-Version-3.jpg.webp"
    )
    embed.add_field(name="Event",
                    value="Something has been caught on the fishing rod!",
                    inline=False)
    await message.edit(embed=embed)
    await message.add_reaction("🎣")

    def check(reaction, user):
        return user == ctx.author and str(
            reaction.emoji) == "🎣" and reaction.message.id == message.id

    try:
        await bot.wait_for("reaction_add", timeout=3.0, check=check)
    except asyncio.TimeoutError:
        embed.set_field_at(-1,
                           name="Result",
                           value="You were too late! The fish got away.",
                           inline=False)
        await message.edit(embed=embed)
        return

    # Calculate luck and determine catches
    total_luck = rod.luck * accessory["luck"]
    catch_bonus = accessory["catch_bonus"]
    num_catches = random.randint(1, catch_bonus + 1)

    catches = []
    for _ in range(num_catches):
        possible_items = [
            item for item, data in FISHING_ITEMS.items()
            if current_location in data.locations
        ]
        weights = [
            FISHING_ITEMS[item].rarity_weight * total_luck
            for item in possible_items
        ]
        caught_item = random.choices(possible_items, weights=weights, k=1)[0]
        catches.append(caught_item)
        update_user_inventory(user_id, "fish", caught_item, 1)

    xp_gained = random.randint(5, 20) * len(catches)
    add_xp(user_id, xp_gained)

    # Use up one bait
    update_user_inventory(user_id, "baits", bait_name, -1)

    # Update rod durability
    rod.durability -= 1
    if rod.durability <= 0:
        del player_data[user_id]["equipped"]["rod"]
        remove_from_inventory(user_id, rod_name)
        embed.add_field(
            name="Rod Status",
            value=
            "Your fishing rod has broken and has been removed from your inventory!",
            inline=False)

    # Display results
    catch_text = ", ".join(catches) if catches else "Nothing"
    embed.set_field_at(-1,
                       name="Result",
                       value=f"You caught: {catch_text}!",
                       inline=False)
    embed.add_field(name="XP Gained", value=f"{xp_gained} XP", inline=False)
    embed.set_image(
        url=
        "https://www.shutterstock.com/image-vector/great-catch-during-fishing-concept-600nw-2056287488.jpg"
    )

    # Update equipment field
    new_bait_quantity = get_user_inventory(user_id)["baits"].get(bait_name, 0)
    embed.set_field_at(
        0,
        name="Equipment",
        value=f"Rod: {rod_name} (Durability: {rod.durability})\n"
        f"Location: {current_location}\n"
        f"Accessory: {accessory_name if accessory_name else 'None'}\n"
        f"Bait: {bait_name} (Quantity: {new_bait_quantity})",
        inline=False)

    await message.edit(embed=embed)
    save_player_data(player_data)

    @bot.command(name="select_location")
    async def select_location(ctx, *, location):
        user_id = str(ctx.author.id)
        player_data = load_player_data()

        if user_id not in player_data:
            await ctx.send(
                "You haven't started fishing yet! Use the `?fish` command to begin."
            )
            return

        level = calculate_level(player_data[user_id].get("xp", 0))
        unlocked_locations = get_unlocked_locations(level)

        if location not in FISHING_LOCATIONS:
            await ctx.send(
                "Invalid location. Please choose from the available fishing locations."
            )
            return

        if location not in unlocked_locations:
            await ctx.send(
                f"You haven't unlocked {location} yet. Keep leveling up to access new locations!"
            )
            return

        player_data[user_id]["fishing_location"] = location
        save_player_data(player_data)

        embed = discord.Embed(title="🎣 Location Selected", color=0x00ff00)
        embed.add_field(name="New Fishing Spot", value=location, inline=False)
        embed.add_field(name="Good luck!",
                        value="Happy fishing in your new location!",
                        inline=False)

        await ctx.send(embed=embed)

    player_data[user_id]["fishing_location"] = location
    save_data(PLAYER_DATA, player_data)
    await ctx.send(f"Your fishing location has been set to {location}.")


def update_leaderboard(user_id, amount):
    leaderboard_data = load_data(CASH_FILE)
    leaderboard_data[str(user_id)] = amount
    save_data(CASH_FILE, leaderboard_data)


@bot.command(name="leaderboard", aliases=["lb"])
async def leaderboard(ctx):
    sorted_data = sorted(
        player_data.items(),
        key=lambda x:
        (get_cash_balance(x[0]) + get_bank_balance(x[0]), get_level(x[0])),
        reverse=True)

    embed = discord.Embed(title="Melon Economy Leaderboard", color=0x00ff00)
    embed.set_thumbnail(url="https://img.icons8.com/color/96/leaderboard.png")

    for i, (user_id, data) in enumerate(sorted_data[:10], 1):
        user = await bot.fetch_user(int(user_id))
        total_balance = get_cash_balance(user_id) + get_bank_balance(user_id)
        embed.add_field(
            name=f"{i}. {user.name}",
            value=f"Balance: {total_balance} 🍈 | Level: {get_level(user_id)}",
            inline=False)

    await ctx.send(embed=embed)


# Convert FISHING_RODS
FISHING_RODS = {
    name:
    FishingRod(name, data['price'], data['durability'], data['efficiency'],
               data['luck'])
    for name, data in FISHING_RODS.items()
}

# Convert FISHING_ITEMS
FISHING_ITEMS = {
    name:
    FishingItem(name, data['rarity'], data['rarity_weight'], data['price'],
                data['locations'])
    for name, data in FISHING_ITEMS.items()
}

# Convert FISHING_LOCATIONS
FISHING_LOCATIONS = {
    name:
    FishingLocation(name, data['difficulty'], data['min_level'],
                    data['description'])
    for name, data in FISHING_LOCATIONS.items()
}

# Convert FISHING_BAITS
FISHING_BAITS = {
    name:
    FishingBait(name, data['efficiency'], data['rarity'],
                data['rarity_weight'], data['price'], data['locations'])
    for name, data in FISHING_BAITS.items()
}

# Convert FISHING_ACCESSORIES
FISHING_ACCESSORIES = {
    name:
    FishingAccessory(name, data['price'], data.get('efficiency', 1.0),
                     data.get('luck', 1.0), data.get('catch_bonus', 0))
    for name, data in FISHING_ACCESSORIES.items()
}


@bot.command(name="market", aliases=["shop"])
async def market(ctx, category: str = None):
    categories = ["rods", "baits", "accessories", "fish"]

    if category is None:
        embed = discord.Embed(title="Melon Market",
                              description="Choose a category:",
                              color=0x00ff00)
        for cat in categories:
            embed.add_field(name=cat.capitalize(),
                            value=f"Use ?market {cat}",
                            inline=False)
        await ctx.send(embed=embed)
        return

    category = category.lower()
    if category not in categories:
        await ctx.send(
            f"Invalid category. Available categories: {', '.join(categories)}")
        return

    if category == "rods":
        embed = create_market_embed("Fishing Rod Market", FISHING_RODS,
                                    get_rod_info)
    elif category == "baits":
        embed = create_market_embed("Fishing Bait Market", FISHING_BAITS,
                                    get_bait_info)
    elif category == "accessories":
        embed = create_market_embed("Fishing Accessory Market",
                                    FISHING_ACCESSORIES, get_accessory_info)
    elif category == "fish":
        embed = create_market_embed("Fish Market", FISHING_ITEMS,
                                    get_fish_info,
                                    lambda x: x.rarity != "Trash")

    await ctx.send(embed=embed)


def create_market_embed(title, items, info_func, filter_func=None):
    embed = discord.Embed(title=title, color=0x00ff00)
    for name, item in items.items():
        if filter_func is None or filter_func(item):
            embed.add_field(name=name, value=info_func(item), inline=False)
    return embed


def get_rod_info(rod):
    return f"Price: {rod.price} 🍈\nDurability: {rod.durability}\nEfficiency: {rod.efficiency}\nLuck: {rod.luck}"


def get_bait_info(bait):
    return f"Price: {bait.price} 🍈\nEfficiency: {bait.efficiency}\nRarity: {bait.rarity}"


def get_accessory_info(acc):
    return f"Price: {acc.price} 🍈\nEfficiency: {acc.efficiency}\nLuck: {acc.luck}"


def get_fish_info(fish):
    return f"Price: {fish.price} 🍈\nRarity: {fish.rarity}"


# Buy command
@bot.command(name="buy")
async def buy(ctx, item: str, amount: int = 1):
    original_item = item
    item = item.lower().replace(' ', '_')

    # Find the category and item
    category = None
    matching_item = None
    for cat, item_list in [("rods", FISHING_RODS), ("baits", FISHING_BAITS),
                           ("accessories", FISHING_ACCESSORIES)]:
        if item in [i.lower().replace(' ', '_') for i in item_list.keys()]:
            category = cat
            matching_item = next(i for i in item_list.keys()
                                 if i.lower().replace(' ', '_') == item)
            break

    if not matching_item:
        await ctx.send(
            f"Invalid item. Available items: {', '.join(FISHING_RODS.keys() + FISHING_BAITS.keys() + FISHING_ACCESSORIES.keys())}"
        )
        return

    item_data = (FISHING_RODS if category == "rods" else FISHING_BAITS if
                 category == "baits" else FISHING_ACCESSORIES)[matching_item]
    price = item_data.price * amount
    user_balance = get_cash_balance(str(ctx.author.id))

    if user_balance < price:
        await ctx.send(
            f"You don't have enough melons. You need {price} melons, but you only have {user_balance} melons."
        )
        return

    # Create confirmation embed
    confirm_embed = discord.Embed(title="Purchase Confirmation",
                                  color=0xffa500)
    confirm_embed.add_field(name="Item", value=matching_item, inline=True)
    confirm_embed.add_field(name="Category",
                            value=category.capitalize(),
                            inline=True)
    confirm_embed.add_field(name="Amount", value=str(amount), inline=True)
    confirm_embed.add_field(name="Price", value=f"{price} melons", inline=True)
    confirm_embed.add_field(name="Your Balance",
                            value=f"{user_balance} melons",
                            inline=True)
    confirm_embed.set_footer(text="React with ✅ to confirm or ❌ to cancel")

    confirm_msg = await ctx.send(embed=confirm_embed)
    await confirm_msg.add_reaction("✅")
    await confirm_msg.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [
            "✅", "❌"
        ] and reaction.message.id == confirm_msg.id

    try:
        reaction, user = await bot.wait_for("reaction_add",
                                            timeout=30.0,
                                            check=check)

        if str(reaction.emoji) == "✅":
            # Process the purchase
            new_balance = user_balance - price
            update_cash_balance(str(ctx.author.id), new_balance)

            # Update inventory
            update_user_inventory(str(ctx.author.id), category, matching_item,
                                  amount)

            success_embed = discord.Embed(title="Purchase Successful",
                                          color=0x00ff00)
            success_embed.add_field(name="Item",
                                    value=matching_item,
                                    inline=True)
            success_embed.add_field(name="Category",
                                    value=category.capitalize(),
                                    inline=True)
            success_embed.add_field(name="Amount",
                                    value=str(amount),
                                    inline=True)
            success_embed.add_field(name="Price",
                                    value=f"{price} melons",
                                    inline=True)
            success_embed.add_field(name="New Balance",
                                    value=f"{new_balance} melons",
                                    inline=False)
            success_embed.set_footer(text="Thank you for your purchase!")

            await confirm_msg.edit(embed=success_embed)
            await confirm_msg.clear_reactions()
        else:
            cancel_embed = discord.Embed(title="Purchase Cancelled",
                                         color=0xff0000)
            cancel_embed.description = "Your purchase has been cancelled. No melons were deducted."
            await confirm_msg.edit(embed=cancel_embed)
            await confirm_msg.clear_reactions()

    except asyncio.TimeoutError:
        timeout_embed = discord.Embed(title="Purchase Timed Out",
                                      color=0xff0000)
        timeout_embed.description = "You didn't respond in time. The purchase has been cancelled."
        await confirm_msg.edit(embed=timeout_embed)
        await confirm_msg.clear_reactions()


@bot.command(name="sell")
async def sell(ctx, category, amount):
    user_id = str(ctx.author.id)
    inventory = get_user_inventory(user_id)

    if category.lower() not in ["fish", "baits", "rods", "accessories"]:
        await ctx.send(
            "Invalid category. Please choose from: fish, baits, rods, or accessories."
        )
        return

    if amount.lower() == "all":
        items_to_sell = inventory[category]
    else:
        try:
            amount = int(amount)
            items_to_sell = {
                item: min(count, amount)
                for item, count in inventory[category].items()
            }
        except ValueError:
            await ctx.send("Invalid amount. Please use a number or 'all'.")
            return

    total_value = 0
    items_sold = {}

    for item, count in items_to_sell.items():
        if count > 0:
            item_price = get_item_price(category, item)
            value = item_price * count
            total_value += value
            items_sold[item] = {"count": count, "value": value}
            update_user_inventory(user_id, category, item, -count)

    if not items_sold:
        await ctx.send(
            f"You don't have any items to sell in the {category} category.")
        return

    update_cash_balance(user_id, get_bank_balance() + total_value)

    embed = discord.Embed(title="🏷️ Items Sold", color=0x00ff00)
    for item, data in items_sold.items():
        embed.add_field(
            name=item,
            value=f"Quantity: {data['count']}\nValue: {data['value']} coins",
            inline=True)

    embed.add_field(name="Total Items Sold",
                    value=sum(data['count'] for data in items_sold.values()),
                    inline=False)
    embed.add_field(name="Total Value",
                    value=f"{total_value} coins",
                    inline=False)

    await ctx.send(embed=embed)


@bot.command(name="repair")
async def repair_item(ctx, *, item_type: str):
    user_id = str(ctx.author.id)
    if item_type == "fishing_rod":
        if "equipped" not in player_data[
                user_id] or "fishing_rod" not in player_data[user_id][
                    "equipped"]:
            await ctx.send("You don't have a fishing rod equipped.")
            return

        rod_name = player_data[user_id]["equipped"]["fishing_rod"]
        rod_data = Items.FISHING_RODS[rod_name]

        repair_cost = int(rod_data["price"] * 0.2)  # 20% of original price
        if get_cash_balance(user_id) < repair_cost:
            await ctx.send(
                f"You don't have enough coins to repair your {rod_name}. Repair cost: {repair_cost} coins."
            )
            return

        # Repair the rod
        cash = get_cash_balance(user_id)
        rod_data["durability"] = rod_data.get(
            "max_durability",
            rod_data["durability"])  # Reset to max durability
        update_cash_balance(user_id, cash - repair_cost)
        save_data(PLAYER_DATA, player_data)
        await ctx.send(
            f"You have repaired your {rod_name} for {repair_cost} coins.")

    else:
        await ctx.send(
            "Invalid item type. You can only repair `fishing_rod` for now.")


#BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!!!!!!!!!!!


def get_bank_balance(user_id):
    user_id = str(user_id)
    file_path = 'bank_data.json'

    try:
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Creating new file.")
            with open(file_path, 'w') as f:
                json.dump({}, f)

        with open(file_path, 'r') as f:
            bank_data = json.load(f)

        balance = bank_data.get(user_id, 0)
        print(f"Retrieved bank balance for user {user_id}: {balance}")

        return balance

    except Exception as e:
        print(f"An error occurred while getting bank balance: {str(e)}")
        return 0


def get_cash_balance(user_id):
    user_id = str(user_id)
    file_path = 'cash_data.json'

    print(f"Attempting to get balance for user ID: {user_id}")

    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({}, f)

        with open(file_path, 'r') as f:
            cash_data = json.load(f)

        balance = cash_data.get(user_id, 0)  # Default to 0 if user not found
        return balance

    except Exception as e:
        print(f"An error occurred while getting cash balance: {str(e)}")
        return 0


def update_cash_balance(user_id, amount):
    user_id = str(user_id)
    file_path = 'cash_data.json'

    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({}, f)

        with open(file_path, 'r') as f:
            cash_data = json.load(f)

        cash_data[user_id] = amount

        with open(file_path, 'w') as f:
            json.dump(cash_data, f, indent=4)

    except Exception as e:
        print(f"An error occurred while updating cash balance: {str(e)}")


def update_bank_balance(user_id, amount):
    user_id = str(user_id)
    file_path = 'bank_data.json'

    try:
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Creating new file.")
            with open(file_path, 'w') as f:
                json.dump({}, f)

        with open(file_path, 'r') as f:
            bank_data = json.load(f)

        bank_data[user_id] = amount

        with open(file_path, 'w') as f:
            json.dump(bank_data, f, indent=4)

        print(f"Updated bank balance for user {user_id}: {amount}")

    except Exception as e:
        print(f"An error occurred while updating bank balance: {str(e)}")


def deposit_to_bank(user_id, amount):
    try:
        amount = int(amount)  # Ensure amount is an integer
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        cash_balance = get_cash_balance(user_id)
        bank_balance = get_bank_balance(user_id)

        if cash_balance >= amount:
            new_cash_balance = cash_balance - amount  # Subtract from cash
            new_bank_balance = bank_balance + amount  # Add to bank

            update_cash_balance(user_id, new_cash_balance)
            update_bank_balance(user_id, new_bank_balance)

            return f"Deposited {amount} melons. New bank balance is {new_bank_balance} melons."
        else:
            raise ValueError("Insufficient funds in your cash balance.")

    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred: {str(e)}"


def withdraw_from_bank(user_id, amount):
    try:
        amount = int(amount)  # Ensure amount is an integer
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        bank_balance = get_bank_balance(user_id)

        if bank_balance >= amount:
            new_bank_balance = bank_balance - amount
            new_cash_balance = get_cash_balance(user_id) + amount

            update_bank_balance(user_id, new_bank_balance)
            update_cash_balance(user_id, new_cash_balance)

            return f"Withdrew {amount} melons. New bank balance is {new_bank_balance} melons."
        else:
            raise ValueError("Insufficient funds in the bank.")

    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_last_claim_time(user_id):
    reward_data = load_data(DAILY_REWARD_FILE)
    return reward_data.get(str(user_id), 0)


def update_last_claim_time(user_id, timestamp):
    reward_data = load_data(DAILY_REWARD_FILE)
    reward_data[str(user_id)] = timestamp
    save_data(DAILY_REWARD_FILE, reward_data)


@bot.command()
async def deposit(ctx, amount: int):
    user_id = ctx.author.id
    result = deposit_to_bank(user_id, amount)
    await ctx.send(result)


def load_daily_data():
    try:
        with open(DAILY_REWARD_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_daily_data(data):
    with open(DAILY_REWARD_FILE, 'w') as f:
        json.dump(data, f)


# Check for Cooldown
def check_cooldown(user_id):
    """Checks if the user has a daily cooldown."""
    now = datetime.now()  # Corrected line
    if user_id in daily_cooldowns:
        last_claim = daily_cooldowns[user_id]
        if (now - last_claim
            ).total_seconds() < 86400:  # 86400 seconds = 24 hours
            return True  # Cooldown active
    return False  # No cooldown


def get_initial_reward(user_id):
    """Returns the initial reward amount for a user."""
    if str(user_id) not in daily_cooldowns:
        return 100  # Default initial reward
    else:
        return DAILY_REWARD_FILE[user_id]


@tasks.loop(hours=24)
async def backup_data():
    for filename in [
            INVENTORY_FILE, CASH_FILE, PLAYER_DATA, DAILY_REWARD_FILE
    ]:
        backup_name = f"{filename}.{datetime.now().strftime('%Y%m%d%H%M%S')}.backup"
        try:
            with open(filename, 'r') as source, open(backup_name,
                                                     'w') as target:
                target.write(source.read())
            print(f"Backup created: {backup_name}")
        except Exception as e:
            print(f"Error creating backup for {filename}: {str(e)}")


# Claim Daily Reward
@bot.command(name='daily')
async def daily(ctx):
    user_id = str(ctx.author.id)
    now = datetime.now()
    daily_data = load_daily_data()

    if user_id not in daily_data:
        daily_data[user_id] = {
            "last_claim": None,
            "streak": 0,
            "base_reward": 100
        }

    user_data = daily_data[user_id]
    last_claim = datetime.fromisoformat(
        user_data["last_claim"]) if user_data["last_claim"] else None

    if last_claim and (now - last_claim) < timedelta(hours=21):
        remaining_time = timedelta(hours=21) - (now - last_claim)
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        await ctx.send(
            f"You can claim your daily reward in {hours} hours and {minutes} minutes."
        )
        return

    # Calculate reward
    base_reward = user_data["base_reward"]
    streak_bonus = user_data[
        "streak"] * 0.1  # 10% increase for each day in the streak
    total_reward = int(base_reward * (1 + streak_bonus))

    # Update user's balance
    update_cash_balance(user_id, get_cash_balance(user_id) + total_reward)

    # Update daily data
    user_data["last_claim"] = now.isoformat()
    user_data["streak"] += 1
    user_data["base_reward"] = total_reward  # Set new base for next time
    save_daily_data(daily_data)

    # Send confirmation message
    embed = discord.Embed(title="Daily Reward", color=0x00ff00)
    embed.add_field(name="Reward",
                    value=f"{total_reward} melons",
                    inline=False)
    embed.add_field(name="Streak",
                    value=f"{user_data['streak']} days",
                    inline=False)
    embed.set_footer(text="Come back in 21 hours for another reward!")
    await ctx.send(embed=embed)


@bot.command(name="prefix")
@commands.has_permissions(administrator=True)
async def change_prefix(ctx, new_prefix: str):
    if len(new_prefix) > 5:
        await ctx.send("The prefix must be 5 characters or fewer.")
        return
    with open(PREFIXES_FILE, 'r') as f:
        prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = new_prefix

    with open(PREFIXES_FILE, 'w') as f:
        json.dump(prefixes, f)

    await ctx.send(
        f"The prefix for this server has been changed to '{new_prefix}'")


@change_prefix.error
async def change_prefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to be an administrator to change the prefix.")


@bot.command(name="bank")
async def bank(ctx):
    user_id = ctx.author.id
    balance = get_bank_balance(user_id)
    await ctx.send(
        f"{ctx.author.mention}, you have {balance} melons in your bank.")


@bot.command()
async def withdraw(ctx, amount: int):
    try:
        result = withdraw_from_bank(ctx.author.id, amount)
        await ctx.send(result)
    except ValueError as e:
        await ctx.send(str(e))


@bot.command(name="coinflip", aliases=["cf"])
async def coinflip(ctx, bet_amount: int = None):
    balance = get_cash_balance(ctx.author.id)
    if bet_amount is None:
        await ctx.send(
            f"Your current balance: {balance} 🍈\nEnter the amount you want to bet (or type 'exit' to leave):"
        )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
        return

    if msg.content.lower() == 'exit':
        await ctx.send("Thanks for playing!")
        return

    try:
        bet_amount = int(msg.content)
    except ValueError:
        await ctx.send("Invalid input. Please enter a number.")
        return

    if bet_amount > balance:
        await ctx.send("Insufficient funds.")
        return

    await ctx.send("Choose 'heads' or 'tails':")
    try:
        user_choice = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
        return


# Coin Flip Animation
    coin_message = await ctx.send("Flipping the coin...")
    for _ in range(5):
        await asyncio.sleep(1)
        await coin_message.edit(content=f"{coin_message.content}.")

    if random.random() < 0.01:  # 1% chance of encountering Saitama
        await ctx.send("Saitama appeared! You ran away and lost your melons!")
        update_cash_balance(ctx.author.id, balance - bet_amount)
        return

    coinflip_result = random.choice(['heads', 'tails'])
    await ctx.send(f"... and it is {coinflip_result}!")

    if user_choice.content.lower() == coinflip_result:
        winnings = bet_amount * 2
        await ctx.send(
            f"You won! You doubled your bet amount. Your new balance: {winnings} 🍈"
        )
        update_cash_balance(ctx.author.id, balance + bet_amount)
    else:
        await ctx.send("You lost. Better luck next time.")
        update_cash_balance(ctx.author.id, balance - bet_amount)


@bot.command(name="tictactoe", aliases=["ttt"])
async def tic_tac_toe(ctx, bet_amount: int = None):
    balance = get_cash_balance(ctx.author.id)

    if bet_amount is None:
        embed = discord.Embed(title="❌⭕ Tic-Tac-Toe", color=0x00FFFF)
        embed.add_field(name="Your Balance",
                        value=f"{balance} 🍈",
                        inline=False)
        embed.add_field(name="How to Play",
                        value="Enter the amount you want to bet!",
                        inline=False)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
            return

        if msg.content.lower() == 'exit':
            await ctx.send("Thanks for playing!")
            return

        try:
            bet_amount = int(msg.content)
        except ValueError:
            await ctx.send("Invalid input. Please enter a number.")
            return

    if bet_amount > balance:
        await ctx.send("Insufficient funds. 😢")
        return

    board = ["⬜" for _ in range(9)]  # 3x3 board
    current_player = "❌"

    def display_board():
        return "\n".join([" ".join(board[i:i + 3]) for i in range(0, 9, 3)])

    def create_board_embed():
        embed = discord.Embed(title="❌⭕ Tic-Tac-Toe", color=0x00FFFF)
        embed.add_field(name="Board", value=display_board(), inline=False)
        embed.add_field(name="Current Turn",
                        value=f"{current_player}'s turn",
                        inline=False)
        return embed

    board_message = await ctx.send(embed=create_board_embed())

    while True:
        if current_player == "❌":
            await ctx.send(f"{ctx.author.mention}, choose a position (1-9):")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = await bot.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")
                return

            if msg.content.isdigit():
                position = int(msg.content) - 1
                if position < 0 or position > 8 or board[position] != "⬜":
                    await ctx.send(
                        "Invalid position. Choose a number between 1-9 that is not already taken."
                    )
                    continue
            else:
                await ctx.send(
                    "Invalid input. Please enter a number between 1-9.")
                continue
        else:
            # Bot's turn
            await asyncio.sleep(1)  # Add a delay to simulate thinking
            available_positions = [
                i for i, spot in enumerate(board) if spot == "⬜"
            ]
            position = random.choice(available_positions)

        board[position] = current_player
        await board_message.edit(embed=create_board_embed())

        # Check for a win
        win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # horizontal
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # vertical
            [0, 4, 8],
            [2, 4, 6]  # diagonal
        ]

        for condition in win_conditions:
            if all(board[i] == current_player for i in condition):
                win_embed = discord.Embed(title="❌⭕ Tic-Tac-Toe",
                                          color=0x00FFFF)
                win_embed.add_field(name="Final Board",
                                    value=display_board(),
                                    inline=False)
                if current_player == "❌":
                    win_embed.add_field(
                        name="Result",
                        value=f"You win! 🎉 You've won {bet_amount * 1.1} 🍈!",
                        inline=False)
                    update_cash_balance(ctx.author.id, balance + bet_amount)
                else:
                    win_embed.add_field(
                        name="Result",
                        value=f"Bot wins! 🤖 You've lost {bet_amount} 🍈.",
                        inline=False)
                    update_cash_balance(ctx.author.id, balance - bet_amount)
                await board_message.edit(embed=win_embed)
                return

        if "⬜" not in board:
            tie_embed = discord.Embed(title="❌⭕ Tic-Tac-Toe", color=0x00FFFF)
            tie_embed.add_field(name="Final Board",
                                value=display_board(),
                                inline=False)
            tie_embed.add_field(
                name="Result",
                value="It's a tie! 🤝 Your bet has been returned.",
                inline=False)
            await board_message.edit(embed=tie_embed)
            return

        # Switch player
        current_player = "⭕" if current_player == "❌" else "❌"


@bot.command(name="rockpaperscissors", aliases=["rps"])
async def rock_paper_scissors(ctx, bet_amount: int = None):
    balance = get_cash_balance(ctx.author.id)

    if bet_amount is None:
        embed = discord.Embed(title="🪨📄✂️ Rock Paper Scissors", color=0xFFA500)
        embed.add_field(name="Your Balance",
                        value=f"{balance} 🍈",
                        inline=False)
        embed.add_field(name="How to Play",
                        value="Enter the amount you want to bet!",
                        inline=False)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
            return

        if msg.content.lower() == 'exit':
            await ctx.send("Thanks for playing!")
            return

        try:
            bet_amount = int(msg.content)
        except ValueError:
            await ctx.send("Invalid input. Please enter a number.")
            return

    if bet_amount > balance:
        await ctx.send("Insufficient funds. 😢")
        return

    choices = {"rock": "🥌", "paper": "📄", "scissors": "✂️"}

    embed = discord.Embed(title="🪨📄✂️ Rock Paper Scissors", color=0xFFA500)
    embed.add_field(name="Choose your move",
                    value="React with your choice!",
                    inline=False)
    message = await ctx.send(embed=embed)

    for emoji in choices.values():
        await message.add_reaction(emoji)

    try:
        reaction, user = await bot.wait_for(
            "reaction_add",
            check=lambda r, u: u == ctx.author and str(r.emoji
                                                       ) in choices.values(),
            timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to choose. Game over!")
        return

    user_choice = list(choices.keys())[list(choices.values()).index(
        str(reaction.emoji))]
    computer_choice = random.choice(list(choices.keys()))

    # Animation
    for choice in ["Rock...", "Paper...", "Scissors..."]:
        animation_embed = discord.Embed(title="🪨📄✂️ Rock Paper Scissors",
                                        color=0xFFA500)
        animation_embed.add_field(name="Choosing...",
                                  value=choice,
                                  inline=False)
        await message.edit(embed=animation_embed)
        await asyncio.sleep(1)

    result_embed = discord.Embed(title="🪨📄✂️ Rock Paper Scissors",
                                 color=0xFFA500)
    result_embed.add_field(
        name="Your Choice",
        value=f"{choices[user_choice]} {user_choice.capitalize()}",
        inline=True)
    result_embed.add_field(
        name="Computer's Choice",
        value=f"{choices[computer_choice]} {computer_choice.capitalize()}",
        inline=True)

    if random.random() < 0.01:  # 1% chance of encountering Saitama
        result_embed.add_field(
            name="It turns out that your opponent was Saitama!",
            value="You ran away and lost your melons! 💨",
            inline=False)
        result_embed.set_image(
            url="https://images.app.goo.gl/c2CCxcPHtJxEwqBDA"
        )  # Replace with actual Saitama image URL
        update_cash_balance(ctx.author.id, balance - bet_amount)
    elif user_choice == computer_choice:
        result_embed.add_field(
            name="Result",
            value="It's a tie! 🤝 Your bet has been returned.",
            inline=False)
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        winnings = bet_amount * 1.2
        result_embed.add_field(
            name="Result",
            value=
            f"You won! 🎉 You doubled your bet amount. Your new balance: {balance + bet_amount} 🍈",
            inline=False)
        update_cash_balance(ctx.author.id, balance + bet_amount)
    else:
        result_embed.add_field(
            name="Result",
            value=
            f"You lost. 😢 Better luck next time. You lost {bet_amount} 🍈.",
            inline=False)
        update_cash_balance(ctx.author.id, balance - bet_amount)

    await message.edit(embed=result_embed)


SUITS = {'♠': '♠️', '♥': '♥️', '♦': '♦️', '♣': '♣️'}
RANKS = {
    '2': '2️⃣',
    '3': '3️⃣',
    '4': '4️⃣',
    '5': '5️⃣',
    '6': '6️⃣',
    '7': '7️⃣',
    '8': '8️⃣',
    '9': '9️⃣',
    '10': '🔟',
    'J': '🃏',
    'Q': '👸',
    'K': '🤴',
    'A': '🅰️'
}


async def print_hand(message, hand, owner):
    hand_str = ' '.join([f"{RANKS[card[0]]}{SUITS[card[1]]}" for card in hand])
    await message.edit(content=f"{owner} hand: {hand_str}")


def initialize_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]


def deal_cards(deck, num_cards):
    return [
        deck.pop(random.randint(0,
                                len(deck) - 1)) for _ in range(num_cards)
    ]


def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card[0] in ['J', 'Q', 'K']:
            value += 10
        elif card[0] == 'A':
            aces += 1
        else:
            value += int(card[0])
    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
    return value


def evaluate_poker_hand(hand):
    ranks = [card[0] for card in hand]
    suits = [card[1] for card in hand]

    is_flush = len(set(suits)) == 1
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}

    rank_values = [{
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }[r] for r in ranks]
    rank_values.sort()
    is_straight = (len(set(rank_values)) == 5
                   and max(rank_values) - min(rank_values)
                   == 4) or set(rank_values) == {14, 2, 3, 4, 5}

    if is_flush and is_straight:
        return 8, max(rank_values)  # Straight Flush
    elif 4 in rank_counts.values():
        return 7, [r for r, count in rank_counts.items()
                   if count == 4][0]  # Four of a Kind
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        return 6, [r for r, count in rank_counts.items()
                   if count == 3][0]  # Full House
    elif is_flush:
        return 5, max(rank_values)  # Flush
    elif is_straight:
        return 4, max(rank_values)  # Straight
    elif 3 in rank_counts.values():
        return 3, [r for r, count in rank_counts.items()
                   if count == 3][0]  # Three of a Kind
    elif list(rank_counts.values()).count(2) == 2:
        return 2, max([r for r, count in rank_counts.items()
                       if count == 2])  # Two Pair
    elif 2 in rank_counts.values():
        return 1, [r for r, count in rank_counts.items()
                   if count == 2][0]  # One Pair
    else:
        return 0, max(rank_values)  # High Card


def format_hand(hand):
    return ' '.join([f"{RANKS[card[0]]}{SUITS[card[1]]}" for card in hand])


def get_hand_name(score):
    hand_names = [
        "High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight",
        "Flush", "Full House", "Four of a Kind", "Straight Flush"
    ]
    return hand_names[score]


@bot.command(name="blackjack", aliases=["bj"])
async def blackjack(ctx, bet_amount: int = None):
    balance = get_cash_balance(ctx.author.id)

    if bet_amount is None:
        await ctx.send(
            f"Your current balance: {balance} melons\nEnter the amount you want to bet (or type 'exit' to leave):"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
            return

        if msg.content.lower() == 'exit':
            await ctx.send("Thanks for playing!")
            return

        try:
            bet_amount = int(msg.content)
        except ValueError:
            await ctx.send("Invalid input. Please enter a number.")
            return

    if bet_amount > balance:
        await ctx.send("Insufficient funds.")
        return

    deck = initialize_deck()
    player_hand = deal_cards(deck, 2)
    dealer_hand = deal_cards(deck, 2)

    player_message = await ctx.send("Your hand:")
    dealer_message = await ctx.send("Dealer's hand:")

    await print_hand(player_message, player_hand, "Your")
    await print_hand(dealer_message, [dealer_hand[0], ('?', '?')], "Dealer's")

    while calculate_hand_value(player_hand) < 21:
        await ctx.send("Do you want to 'hit' or 'stand'?")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower(
            ) in ['hit', 'stand']

        try:
            action = await bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
            return

        if action.content.lower() == 'hit':
            player_hand.append(deck.pop())
            await print_hand(player_message, player_hand, "Your")
            if calculate_hand_value(player_hand) > 21:
                await ctx.send(f"You busted! You lost {bet_amount} melons.")
                update_cash_balance(ctx.author.id, balance - bet_amount)
                return
        else:
            break

    await print_hand(dealer_message, dealer_hand, "Dealer's")

    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        await asyncio.sleep(1)  # Add delay for suspense
        await print_hand(dealer_message, dealer_hand, "Dealer's")

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if dealer_value > 21:
        await ctx.send(f"Dealer busted! You won {bet_amount * 2} melons!")
        update_cash_balance(ctx.author.id, balance + bet_amount)
    elif player_value > dealer_value:
        await ctx.send(f"You win! You won {bet_amount * 2} melons!")
        update_cash_balance(ctx.author.id, balance + bet_amount)
    elif player_value < dealer_value:
        await ctx.send(f"Dealer wins! You lost {bet_amount} melons.")
        update_cash_balance(ctx.author.id, balance - bet_amount)
    else:
        await ctx.send("It's a tie! Your bet has been returned.")


@bot.command(name="poker")
async def poker(ctx, bet_amount: int = None):
    balance = get_cash_balance(ctx.author.id)

    if bet_amount is None:
        await ctx.send(
            f"Your current balance: {balance} 🍈\nEnter the amount you want to bet (or type 'exit' to leave):"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
            return

        if msg.content.lower() == 'exit':
            await ctx.send("Thanks for playing!")
            return

        try:
            bet_amount = int(msg.content)
        except ValueError:
            await ctx.send("Invalid input. Please enter a number.")
            return

    if bet_amount > balance:
        await ctx.send("Insufficient funds.")
        return

    deck = initialize_deck()
    player_hand = deal_cards(deck, 5)
    bot_hand = deal_cards(deck, 5)

    def create_hand_embed(title, hand, show_all=True):
        embed = discord.Embed(title=title, color=0x00ff00)
        hand_str = format_hand(hand) if show_all else "🂠 " * len(hand)
        embed.add_field(name="Cards", value=hand_str, inline=False)
        return embed

    player_embed = create_hand_embed("Your Hand", player_hand)
    await ctx.send(embed=player_embed)

    bot_embed = create_hand_embed("Bot's Hand", bot_hand, show_all=False)
    await ctx.send(embed=bot_embed)

    await ctx.send(
        "Enter the positions (1-5) of cards to discard, separated by spaces:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        discard_msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
        return

    try:
        discard_positions = list(map(int, discard_msg.content.split()))
        discard_positions.sort(reverse=True)
        for pos in discard_positions:
            player_hand.pop(pos - 1)
        player_hand.extend(deal_cards(deck, len(discard_positions)))

        player_embed = create_hand_embed("Your New Hand", player_hand)
        await ctx.send(embed=player_embed)

        # Bot's turn
        bot_discard = random.randint(0, 3)
        for _ in range(bot_discard):
            bot_hand.pop(random.randint(0, len(bot_hand) - 1))
        bot_hand.extend(deal_cards(deck, bot_discard))

        bot_embed = create_hand_embed("Bot's New Hand", bot_hand)
        await ctx.send(embed=bot_embed)

        user_score, user_hand_ranks = evaluate_poker_hand(player_hand)
        bot_score, bot_hand_ranks = evaluate_poker_hand(bot_hand)

        await ctx.send(f"Your hand: {get_hand_name(user_score)}")
        await ctx.send(f"Bot's hand: {get_hand_name(bot_score)}")

        if user_score > bot_score or (user_score == bot_score
                                      and user_hand_ranks > bot_hand_ranks):
            await ctx.send(
                f"Congratulations! You won the Poker game. You won {bet_amount * 2} 🍈!"
            )
            update_cash_balance(ctx.author.id, balance + bet_amount)
        else:
            await ctx.send(
                f"Bot won the game. Better luck next time. You lost {bet_amount} 🍈."
            )
            update_cash_balance(ctx.author.id, balance - bet_amount)

    except ValueError:
        await ctx.send(
            "Invalid input. Please enter card positions as numbers separated by spaces."
        )

    if random.random() < 0.01:  # 1% chance of encountering Saitama
        await ctx.send("Saitama appeared! You ran away and lost your melons!")
        update_cash_balance(ctx.author.id, balance - bet_amount)


def get_hand_name(score):
    hand_names = [
        "High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight",
        "Flush", "Full House", "Four of a Kind", "Straight Flush"
    ]
    return hand_names[score]


@bot.command(name="russianroulette", aliases=["rr"])
async def russian_roulette(ctx):
    balance = get_cash_balance(ctx.author.id)
    await ctx.send(
        f"Warning: If you choose to play, your entire current balance ({balance} 🍈) will be placed as a bet."
    )
    await ctx.send("Are you sure you want to play? (yes/no)")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower(
        ) in ['yes', 'no']

    try:
        response = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("No response received. Game cancelled.")
        return

    if response.content.lower() == 'no':
        await ctx.send("Game cancelled. Thanks for considering!")
        return

    def initialize_chamber():
        total_bullets = random.randint(5, 10)
        num_blanks = random.randint(1, min(total_bullets - 1, 3))
        revolver_chamber = [0] * num_blanks + [1
                                               ] * (total_bullets - num_blanks)
        random.shuffle(revolver_chamber)
        return revolver_chamber, num_blanks, total_bullets - num_blanks

    revolver_chamber, num_blanks, num_live = initialize_chamber()
    await ctx.send(
        f"The revolver chamber is loaded with {num_blanks} blanks and {num_live} live rounds."
    )

    prize_pool = balance * 2
    user_lives = 3
    dealer_lives = 3
    current_turn = 'user'

    while user_lives > 0 and dealer_lives > 0:
        if not revolver_chamber:
            await ctx.send("\nThe chamber is empty. Reinitializing...")
            revolver_chamber, num_blanks, num_live = initialize_chamber()
            await ctx.send(
                f"The revolver chamber is reloaded with {num_blanks} blanks and {num_live} live rounds."
            )

        live_rounds_left = sum(revolver_chamber)
        blank_rounds_left = len(revolver_chamber) - live_rounds_left

        if current_turn == 'user':
            await ctx.send("\nIt's your turn to shoot.")
            if live_rounds_left == 0:
                await ctx.send(
                    "All live rounds have been fired. The dealer must shoot.")
                current_turn = 'dealer'
                continue

            await ctx.send(
                "Do you want to shoot yourself (y) or the dealer (n)?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower(
                ) in ['y', 'n']

            try:
                choice_msg = await bot.wait_for('message',
                                                check=check,
                                                timeout=30.0)
                choice = choice_msg.content.lower()
            except asyncio.TimeoutError:
                await ctx.send("No response received. Game ended.")
                return

            if choice == 'y':
                await ctx.send("You chose to shoot yourself.")
                await asyncio.sleep(2)  # Add delay for suspense
                chamber_result = revolver_chamber.pop(0)
                if chamber_result == 1:
                    await ctx.send("You hit a live round! You lost a life.")
                    user_lives -= 1
                else:
                    await ctx.send(
                        "The chamber was empty. You survived this round!")
                    prize_pool += 0.15 * prize_pool
                    await ctx.send(
                        f"Prize pool increased by 15%. Current prize pool: {prize_pool:.2f} 🍈"
                    )
            else:
                await ctx.send("You chose to shoot the dealer.")
                await asyncio.sleep(2)  # Add delay for suspense
                chamber_result = revolver_chamber.pop(0)
                if chamber_result == 1:
                    await ctx.send(
                        "Dealer hit a live round! Dealer lost a life.")
                    dealer_lives -= 1
                else:
                    await ctx.send(
                        "The chamber was empty. Dealer survived this round!")

            current_turn = 'dealer'

        elif current_turn == 'dealer':
            await ctx.send("\nIt's the dealer's turn to shoot.")
            await asyncio.sleep(2)  # Add delay for suspense
            shoot_probability = live_rounds_left / len(revolver_chamber)

            if blank_rounds_left == 0 or random.random() < shoot_probability:
                await ctx.send("The dealer chose to shoot you.")
                chamber_result = revolver_chamber.pop(0)
                if chamber_result == 1:
                    await ctx.send("Dealer hit a live round! You lost a life.")
                    user_lives -= 1
                else:
                    await ctx.send(
                        "The chamber was empty. You survived this round!")
            else:
                await ctx.send("The dealer chose to shoot himself.")
                chamber_result = revolver_chamber.pop(0)
                if chamber_result == 1:
                    await ctx.send(
                        "Dealer hit a live round! Dealer lost a life.")
                    dealer_lives -= 1
                else:
                    await ctx.send(
                        "The chamber was empty. Dealer survived this round!")
                    prize_pool -= 0.2 * prize_pool
                    await ctx.send(
                        f"Prize pool decreased by 20%. Current prize pool: {prize_pool:.2f} 🍈"
                    )

            current_turn = 'user'

        await ctx.send(f"\nYou have {user_lives} lives left.")
        await ctx.send(f"The dealer has {dealer_lives} lives left.")
        await asyncio.sleep(2)  # Add delay before next round

    if user_lives > 0 and dealer_lives <= 0:
        await ctx.send(
            f"\nCongratulations! You survived Russian Roulette and won {prize_pool:.2f} 🍈."
        )
        update_cash_balance(ctx.author.id, balance + int(prize_pool) - balance)
    elif dealer_lives > 0 and user_lives <= 0:
        await ctx.send(
            "\nGame over. The dealer survived, and you lost all lives and your bet."
        )
        update_cash_balance(ctx.author.id, 0)


REEL_SYMBOLS = ['🍉', '🍇', '🍊', '🍓', '🍒', '🍋', '🍍', '🥝', '🍎', '🍑', '7️⃣', '💎']
WEIGHTS = [12, 12, 12, 12, 12, 10, 10, 10, 10, 10, 7, 5]

SLOT_MACHINE = '''
╔═══════════════════╗
║    MELON SLOTS    ║
╠═══════════════════╣
║  [{0}] [{1}] [{2}]  ║
║  [{3}] [{4}] [{5}]  ║
║ >[{6}] [{7}] [{8}]< ║
║  [{9}] [{10}] [{11}]  ║
║  [{12}] [{13}] [{14}]  ║
╠═══════════════════╣
║ {15: ^19} ║
╚═══════════════════╝
'''


def generate_reel():
    return [
        random.choices(REEL_SYMBOLS, weights=WEIGHTS, k=1)[0] for _ in range(5)
    ]


def format_slot_machine(reels, highlight=None):
    symbols = [symbol for reel in zip(*reels) for symbol in reel]
    result = SLOT_MACHINE.format(*symbols, highlight or "")
    return f"```{result}```"


def check_win(result):
    if result[0] == result[1] == result[2]:
        if result[0] == '💎':
            return "JACKPOT", 3
        elif result[0] == '7️⃣':
            return "MEGA WIN", 2
        else:
            return "BIG WIN", 1.8
    elif result[0] == result[1] or result[1] == result[2] or result[
            0] == result[2]:
        if '7️⃣' in result or '💎' in result:
            return "NICE WIN", 1.5
        else:
            return "SMALL WIN", 1.2
    else:
        return "YOU LOST", -1


@bot.command(name="slots")
async def slot_machine(ctx, bet_amount: int = None):
    balance = get_cash_balance(ctx.author.id)

    if bet_amount is None:
        embed = discord.Embed(title="🎰 Melon Slots 🎰", color=0xFFD700)
        embed.add_field(name="Your Balance",
                        value=f"{balance} 🍈",
                        inline=False)
        embed.add_field(name="How to Play",
                        value="Enter the amount you want to bet!",
                        inline=False)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit(
            )

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
            bet_amount = int(msg.content)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
            return
        except ValueError:
            await ctx.send("Invalid input. Please enter a number.")
            return

    if bet_amount > balance:
        await ctx.send("Insufficient funds.")
        return

    reels = [generate_reel() for _ in range(3)]
    message = await ctx.send(format_slot_machine(reels, "SPINNING..."))

    # Update every 1 second for smoother updates
    for _ in range(10):
        await asyncio.sleep(1)
        reels = [generate_reel() for _ in range(3)]
        if _ % 2 == 0:
            await message.edit(
                content=format_slot_machine(reels, "SPINNING..."))

    # Stop each reel one by one with increasing delays
    final_reels = [reel[:] for reel in reels]
    for i in range(3):
        await asyncio.sleep(1.5 + i * 1.5)
        final_reels[i] = generate_reel()
        await message.edit(
            content=format_slot_machine(final_reels, "SPINNING..."))

    # Get final result from the middle horizontal line of the final reels
    result = [reel[2] for reel in final_reels]

    # Check win using the separate function
    outcome, multiplier = check_win(result)
    winnings = bet_amount * multiplier

    if multiplier > 0:
        outcome_message = f"{outcome}! +{winnings}🍈"
    else:
        outcome_message = f"{outcome}. -{bet_amount}🍈"

    new_balance = balance + winnings
    update_cash_balance(ctx.author.id, new_balance)

    await message.edit(
        content=format_slot_machine(final_reels, outcome_message))

    # Log the result for debugging
    print(f"Result: {result}")
    print(f"Outcome: {outcome}")
    print(f"Multiplier: {multiplier}")

    await ctx.send(
        f"New Balance: {new_balance} 🍈\nDo you want to play again? (yes/no)")

    def check_play_again(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower(
        ) in ['yes', 'no']

    try:
        response = await bot.wait_for('message',
                                      check=check_play_again,
                                      timeout=30.0)
        if response.content.lower() == 'yes':
            await slot_machine(ctx)
        else:
            await ctx.send("Thanks for playing!")
    except asyncio.TimeoutError:
        await ctx.send("No response received. Thanks for playing!")


# Dice Roll Game
@bot.command(name="diceroll", aliases=["dr"])
async def diceroll(ctx, bet_amount: int = None):
    balance = get_cash_balance(ctx.author.id)

    if bet_amount is None:
        embed = discord.Embed(title="🎲 Melon Dice 🎲", color=0x1E90FF)
        embed.add_field(name="Your Balance",
                        value=f"{balance} 🍈",
                        inline=False)
        embed.add_field(name="How to Play",
                        value="Enter the amount you want to bet!",
                        inline=False)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
            bet_amount = int(msg.content)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
            return
        except ValueError:
            await ctx.send("Invalid input. Please enter a number.")
            return

    if bet_amount > balance:
        await ctx.send(f"Insufficient funds. Your balance is {balance} 🍈")
        return

    dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    embed = discord.Embed(title="🎲 Melon Dice 🎲", color=0x1E90FF)
    embed.add_field(name="Bet Amount", value=f"{bet_amount} 🍈", inline=False)
    embed.add_field(name="Rolling...", value="Good luck!", inline=False)
    message = await ctx.send(embed=embed)

    # Rolling animation
    for _ in range(5):
        embed.set_field_at(1,
                           name="Rolling...",
                           value=random.choice(dice_faces),
                           inline=False)
        await message.edit(embed=embed)
        await asyncio.sleep(0.5)

    # Final result
    result = random.randint(1, 6)
    embed.set_field_at(1,
                       name="Result",
                       value=dice_faces[result - 1],
                       inline=False)

    if result > 3:
        win_amount = bet_amount * 2
        embed.add_field(name="Outcome",
                        value=f"You won {win_amount} 🍈!",
                        inline=False)
        embed.color = 0x00FF00  # Green color for win
        update_cash_balance(ctx.author.id, balance + win_amount - bet_amount)
    else:
        embed.add_field(name="Outcome",
                        value=f"You lost {bet_amount} 🍈.",
                        inline=False)
        embed.color = 0xFF0000  # Red color for loss
        update_cash_balance(ctx.author.id, balance - bet_amount)

    new_balance = get_cash_balance(ctx.author.id)
    embed.add_field(name="New Balance", value=f"{new_balance} 🍈", inline=False)
    await message.edit(embed=embed)


# Wheel of Fortune Game
@bot.command(name="wheeloffortune", aliases=["wof"])
async def wheel_of_fortune(ctx, bet_amount: int = None):
    balance = get_cash_balance(ctx.author.id)

    if bet_amount is None:
        embed = discord.Embed(title="🎡 Wheel of Fortune 🎡", color=0xFFD700)
        embed.add_field(name="Your Balance",
                        value=f"{balance} 🍈",
                        inline=False)
        embed.add_field(name="How to Play",
                        value="Enter the amount you want to bet!",
                        inline=False)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
            bet_amount = int(msg.content)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
            return
        except ValueError:
            await ctx.send("Invalid input. Please enter a number.")
            return

    if bet_amount > balance:
        await ctx.send(f"Insufficient funds. Your balance is {balance} 🍈")
        return

    wheel = [{
        "multiplier": 0,
        "chance": 20,
        "color": 0xFF0000
    }, {
        "multiplier": 0.5,
        "chance": 20,
        "color": 0xFFA500
    }, {
        "multiplier": 1,
        "chance": 20,
        "color": 0xFFFF00
    }, {
        "multiplier": 1,
        "chance": 15,
        "color": 0x00FF00
    }, {
        "multiplier": 1.2,
        "chance": 10,
        "color": 0x0000FF
    }, {
        "multiplier": 1.5,
        "chance": 8,
        "color": 0x4B0082
    }, {
        "multiplier": 1.7,
        "chance": 5,
        "color": 0x8A2BE2
    }, {
        "multiplier": 2,
        "chance": 3,
        "color": 0xFFD700
    }]

    embed = discord.Embed(title="🎡 Wheel of Fortune 🎡", color=0xFFD700)
    embed.add_field(name="Bet Amount", value=f"{bet_amount} 🍈", inline=False)
    embed.add_field(name="Spinning...", value="Good luck!", inline=False)
    message = await ctx.send(embed=embed)

    # Spinning animation
    for _ in range(5):
        random_segment = random.choice(wheel)
        embed.color = random_segment["color"]
        embed.set_field_at(1,
                           name="Spinning...",
                           value=f"{random_segment['multiplier']}x",
                           inline=False)
        await message.edit(embed=embed)
        await asyncio.sleep(0.7)

    # Final result
    result = random.choices(wheel,
                            weights=[item["chance"] for item in wheel],
                            k=1)[0]
    winnings = int(bet_amount * result["multiplier"])

    embed.color = result["color"]
    embed.set_field_at(1,
                       name="Wheel Landed On",
                       value=f"{result['multiplier']}x",
                       inline=False)

    if winnings > bet_amount:
        embed.add_field(name="Result",
                        value=f"You won {winnings} 🍈!",
                        inline=False)
    elif winnings == bet_amount:
        embed.add_field(name="Result", value="You broke even!", inline=False)
    else:
        embed.add_field(name="Result",
                        value=f"You lost {bet_amount - winnings} 🍈.",
                        inline=False)

    update_cash_balance(ctx.author.id, balance - bet_amount + winnings)
    new_balance = get_cash_balance(ctx.author.id)
    embed.add_field(name="New Balance", value=f"{new_balance} 🍈", inline=False)

    await message.edit(embed=embed)


@bot.command(name="give", aliases=["send"])
async def give(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("You must give a positive amount of melons.")
        return

    if member.bot:
        await ctx.send("You cannot give melons to a bot.")
        return

    if member == ctx.author:
        await ctx.send("You cannot give melons to yourself.")
        return

    giver_id = str(ctx.author.id)
    receiver_id = str(member.id)

    giver_balance = get_cash_balance(giver_id)

    if giver_balance < amount:
        await ctx.send("You don't have enough melons to give.")
        return

    # Create confirmation embed
    confirm_embed = discord.Embed(title="Melon Transfer Confirmation",
                                  color=0xffa500)
    confirm_embed.set_thumbnail(
        url=member.avatar.url if member.avatar else member.default_avatar.url)
    confirm_embed.add_field(name="From", value=ctx.author.name, inline=True)
    confirm_embed.add_field(name="To", value=member.name, inline=True)
    confirm_embed.add_field(name="Amount",
                            value=f"{amount} melons",
                            inline=False)
    confirm_embed.set_footer(text="React with ✅ to confirm or ❌ to cancel")

    confirm_msg = await ctx.send(embed=confirm_embed)
    await confirm_msg.add_reaction("✅")
    await confirm_msg.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [
            "✅", "❌"
        ] and reaction.message.id == confirm_msg.id

    try:
        reaction, user = await bot.wait_for("reaction_add",
                                            timeout=30.0,
                                            check=check)

        if str(reaction.emoji) == "✅":
            # Update balances
            update_cash_balance(giver_id, giver_balance - amount)
            receiver_balance = get_cash_balance(receiver_id)
            update_cash_balance(receiver_id, receiver_balance + amount)

            # Create success embed
            success_embed = discord.Embed(title="Melon Transfer Successful",
                                          color=0x00ff00)
            success_embed.set_thumbnail(url=member.avatar.url if member.
                                        avatar else member.default_avatar.url)
            success_embed.add_field(name="From",
                                    value=ctx.author.name,
                                    inline=True)
            success_embed.add_field(name="To", value=member.name, inline=True)
            success_embed.add_field(name="Amount",
                                    value=f"{amount} melons",
                                    inline=False)
            success_embed.add_field(name="New Balance",
                                    value=f"{giver_balance - amount} melons",
                                    inline=False)

            await confirm_msg.edit(embed=success_embed)
            await confirm_msg.clear_reactions()

        else:
            cancel_embed = discord.Embed(title="Melon Transfer Cancelled",
                                         color=0xff0000)
            await confirm_msg.edit(embed=cancel_embed)
            await confirm_msg.clear_reactions()

    except asyncio.TimeoutError:
        timeout_embed = discord.Embed(title="Melon Transfer Timed Out",
                                      color=0xff0000)
        await confirm_msg.edit(embed=timeout_embed)
        await confirm_msg.clear_reactions()


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="Well I don't know how to play this ping...🏓 Pong! game.",
        color=0x00ff00)
    embed.add_field(name="Bot Latency: ", value=f"{latency}ms", inline=False)
    message = await ctx.send("But, I can tell you the ping of the bot...")
    await asyncio.sleep(1)
    await message.edit(content="", embed=embed)


@bot.event
async def on_message(message):
    print(f"Received message: {message.content} from {message.author}")
    if bot.user in message.mentions:
        await message.channel.send(
            "Hello! Type `?help` to get started on this fishing journey.")
    await bot.process_commands(
        message)  # Important to call this to allow commands to work


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds."
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing a required argument for this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(
            "Could not find the specified user. Please make sure you've mentioned a valid user."
        )
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Invalid argument. Please use the format: ?give @user amount")
    else:
        await ctx.send(f"An error occurred: {str(error)}")


class CustomHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Melon Economy Bot Help",
            description=
            "Use `?help <category>` for more information on each category.",
            color=0x00ff00)
        categories = {
            "Economy": "💰",
            "Fishing": "🎣",
            "Farming": "🌾",
            "Expedition": "⛏️",
            "Crafting": "🛠️",
            "Market": "🛒",
            "Inventory": "🎒",
            "Puppies": "🐶",
            "Games": "🎮",
            "Utility": "🔧"
        }
        for category, emoji in categories.items():
            embed.add_field(name=f"{emoji} {category}",
                            value=f"`?help {category.lower()}`",
                            inline=True)

        embed.set_footer(
            text="Tip: You can also use ?menu for quick utility commands!")
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        await self.send_bot_help(None)

    async def send_group_help(self, group):
        await self.send_bot_help(None)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Command: {command.name}", color=0x00ff00)
        embed.add_field(name="Description",
                        value=command.help or "No description available.",
                        inline=False)
        embed.add_field(name="Usage",
                        value=f"`?{command.name} {command.signature}`",
                        inline=False)
        if command.aliases:
            embed.add_field(name="Aliases",
                            value=", ".join(command.aliases),
                            inline=False)
        await self.get_destination().send(embed=embed)

    async def command_callback(self, ctx, *, command=None):
        if command is None:
            await self.send_bot_help(None)
            return

        category = command.lower()
        categories = {
            "economy": self.economy_help,
            "fishing": self.fishing_help,
            #progress   "farming": self.farming_help,
            #progress  "expedition": self.expedition_help,
            #progress   "crafting": self.crafting_help,
            "market": self.market_help,
            "inventory": self.inventory_help,
            #progress   "puppies": self.puppies_help,
            "games": self.games_help,
            "utility": self.utility_help
        }

        if category in categories:
            await categories[category](ctx)
        else:
            await ctx.send(
                "Invalid category. Use `?help` to see all categories.")

    async def economy_help(self, ctx):
        embed = discord.Embed(title="Economy Commands", color=0x00ff00)
        commands = {
            "balance":
            "Check your melon balance\nUsage: `?balance`",
            "deposit <amount>":
            "Deposit melons into your bank\nUsage: `?deposit 1000`",
            "withdraw <amount>":
            "Withdraw melons from your bank\nUsage: `?withdraw 500`",
            "daily":
            "Claim your daily reward\nUsage: `?daily`",
            "give <user> <amount>":
            "Give melons to another user\nUsage: `?give @user 100`"
        }
        for cmd, description in commands.items():
            embed.add_field(name=cmd, value=description, inline=False)
        await ctx.send(embed=embed)

    async def inventory_help(self, ctx):
        embed = discord.Embed(title="🎒 Inventory & Character Commands 🎒",
                              color=0x00ff00)
        commands = {
            "inventory (inv)": "View your inventory\nUsage: `?inventory`",
            "equip <item>":
            "Equip an item from your inventory\nUsage: `?equip fishing_rod`",
            "unequip <item>": "Unequip an item\nUsage: `?unequip fishing_rod`",
            "equipped":
            "View your currently equipped items\nUsage: `?equipped`",
            "trade <user> <your_item> <their_item>":
            "Propose a trade with another user\nUsage: `?trade @user my_fish their_sword`",
            "level (lvl)": "Check your current level and XP\nUsage: `?level`",
            "xp": "View your XP progress\nUsage: `?xp`",
            "leaderboard (lb)":
            "View the XP leaderboard\nUsage: `?leaderboard`"
        }
        for cmd, description in commands.items():
            embed.add_field(name=cmd, value=description, inline=False)

        inventory_explanation = (
            "Your inventory stores all the items you've collected. You can equip items to enhance "
            "your abilities, trade with other players, and manage your gear. Gain XP through various "
            "activities to level up and unlock new features!")
        embed.add_field(name="About Inventory & Character",
                        value=inventory_explanation,
                        inline=False)

        await ctx.send(embed=embed)

    async def fishing_help(self, ctx):
        embed = discord.Embed(title="Fishing Commands", color=0x00ff00)
        commands = {
            "fish": "Go fishing for items and melons\nUsage: `?fish`",
            "upgrade_rod": "Upgrade your fishing rod\nUsage: `?upgrade_rod`",
            "fishingshop": "View the fishing shop\nUsage: `?fishingshop`",
            "fishstats": "View your fishing statistics\nUsage: `?fishstats`"
        }
        for cmd, description in commands.items():
            embed.add_field(name=cmd, value=description, inline=False)
        await ctx.send(embed=embed)

    # ... (implement similar methods for other categories)

    async def games_help(self, ctx):
        embed = discord.Embed(title="Game Commands", color=0x00ff00)
        commands = {
            "coinflip (cf) <amount>":
            "Bet on a coin flip\nUsage: `?coinflip 100`",
            "slots <amount>": "Play the slot machine\nUsage: `?slots 50`",
            "blackjack (bj) <amount>":
            "Play a game of blackjack\nUsage: `?blackjack 200`",
            "rps <amount>": "Play rock-paper-scissors\nUsage: `?rps 100`",
            "diceroll (dr) <amount>":
            "Play a game of dice roll\nUsage: `?dr 100`",
            "wheel_of_fortune (wof) <amount>":
            "Spin the wheel of fortune\nUsage: `?wof 100`",
            "russian_roulette (rr)":
            "Play Russian roulette (bet is your entire balance)\nUsage: `?rr`",
            "tic_tac_toe (ttt) <amount>":
            "Play tic-tac-toe\nUsage: `?ttt 100`",
            "poker <amount>": "Play a game of poker\nUsage: `?poker 100`"
        }
        for cmd, description in commands.items():
            embed.add_field(name=cmd, value=description, inline=False)
        await ctx.send(embed=embed)

    async def market_help(self, ctx):
        embed = discord.Embed(title="🏪 Market Commands 🏪", color=0x00ff00)
        commands = {
            "market":
            "View the current market listings\nUsage: `?market`",
            "market sell <item> <amount> <price>":
            "List an item for sale on the market\nUsage: `?market sell fish 5 100`",
            "market buy <listing_id>":
            "Buy an item from the market\nUsage: `?market buy 1234`",
            "market remove <listing_id>":
            "Remove your listing from the market\nUsage: `?market remove 1234`",
            "market search <item>":
            "Search for specific items on the market\nUsage: `?market search fish`"
        }
        for cmd, description in commands.items():
            embed.add_field(name=cmd, value=description, inline=False)

        market_explanation = (
            "The market allows you to buy and sell items with other players. "
            "You can list items for sale, browse available listings, and make purchases. "
            "Use the market to trade resources and make a profit!")
        embed.add_field(name="About the Market",
                        value=market_explanation,
                        inline=False)

        await ctx.send(embed=embed)

    async def utility_help(self, ctx):
        embed = discord.Embed(title="Utility Commands", color=0x00ff00)
        commands = {
            "help":
            "Show this help message\nUsage: `?help [category]`",
            "ping":
            "Check the bot's latency\nUsage: `?ping`",
            "prefix":
            "Change the bot's prefix\nUsage: `?prefix <new_prefix>`",
            "invite":
            "Get the bot's invite link\nUsage: `?invite`",
            "feedback":
            "Send feedback to the bot developers\nUsage: `?feedback <message>`"
        }
        for cmd, description in commands.items():
            embed.add_field(name=cmd, value=description, inline=False)
        await ctx.send(embed=embed)


bot.help_command = CustomHelpCommand()


@bot.command(name="balance")
async def balance(ctx):
    user_id = str(ctx.author.id)
    cash_balance = get_cash_balance(user_id)
    bank_balance = get_bank_balance(user_id)
    total_balance = cash_balance + bank_balance

    embed = discord.Embed(title="Balance", color=0x00ff00)
    embed.add_field(name="Cash", value=f"{cash_balance} melons", inline=False)
    embed.add_field(name="Bank", value=f"{bank_balance} melons", inline=False)
    embed.add_field(name="Total",
                    value=f"{total_balance} melons",
                    inline=False)

    await ctx.send(embed=embed)


bot.run(os.environ['BOT_TOKEN'])
