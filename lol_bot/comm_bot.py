from utils import make_embed, load_user_data, save_user_data, load_feedback_data, save_feedback_data
import discord


async def help(ctx, category: str = None, bot_prefix: str = "."):
    """Shows a list of commands."""
    if category is None:
        embed = discord.Embed(
            title="LoL Bot Help",
            description=f"Use `{bot_prefix}help <category>` to see commands.\n**Categories:** `profile`, `lol`, `other`",
            color=0xeee657,
        )
        await ctx.send(embed=embed)
        return

    category = category.lower()

    if category == "profile":
        embed = discord.Embed(title="Profile Commands", color=0x7289DA)
        embed.add_field(name=f"{bot_prefix}register <Summoner> <Tag>", value="Link your Riot account to your Discord", inline=False)
        embed.add_field(name=f"{bot_prefix}unregister", value="Remove your linked account", inline=False)
        embed.add_field(name=f"{bot_prefix}profile", value="View your linked account", inline=False)

    elif category == "lol":
        embed = discord.Embed(title="League of Legends Commands", color=0x00c8ff)
        embed.add_field(name=f"{bot_prefix}rank [Summoner#TAG]", value="Show Solo/Duo and Flex rank", inline=False)
        embed.add_field(name=f"{bot_prefix}lastgame [Summoner#TAG]", value="Show the most recent game", inline=False)
        embed.add_field(name=f"{bot_prefix}history [count=5] [Summoner#TAG]", value="Show last N games as a compact list (max 10)", inline=False)
        embed.add_field(name=f"{bot_prefix}played [Summoner#TAG]", value="Show time played today and this week", inline=False)
        embed.add_field(name=f"{bot_prefix}streak [Summoner#TAG]", value="Show current win or loss streak", inline=False)
        embed.add_field(name=f"{bot_prefix}mastery [Summoner#TAG]", value="Show top 5 champion masteries", inline=False)
        embed.add_field(name=f"{bot_prefix}livegame [Summoner#TAG]", value="Show current in-game status and champion", inline=False)

    elif category == "other":
        embed = discord.Embed(title="Other Commands", color=0x2ecc71)
        embed.add_field(name=f"{bot_prefix}hello", value="Say hello to the bot", inline=False)
        embed.add_field(name=f"{bot_prefix}error_lol <message>", value="Report a bug or send feedback", inline=False)

    else:
        embed = make_embed("Error", "Invalid category. Please use `profile`, `lol`, or `other`.", 0xFF0000)

    await ctx.send(embed=embed)


async def unregister(ctx):
    users = load_user_data()
    author_id = str(ctx.author.id)

    if author_id not in users:
        await ctx.send(embed=make_embed("Error", "You are not registered.", 0xFF0000))
        return

    del users[author_id]
    save_user_data(users)
    await ctx.send(embed=make_embed("Success", "Your profile has been removed.", 0x00FF00))


async def hello(ctx):
    await ctx.send(embed=make_embed("Hello!", "My name is Neeko!", 0xECF22C))


async def register(ctx, summoner: str, tag_line: str):
    users = load_user_data()
    author_id = str(ctx.author.id)

    if author_id in users:
        await ctx.send(embed=make_embed("Error", "You are already registered.", 0xFF0000))
        return

    users[author_id] = {"summoner": summoner, "tag_line": tag_line}
    save_user_data(users)
    await ctx.send(embed=make_embed("Success", f"Registered {summoner}#{tag_line}", 0x00FF00))


async def profile(ctx):
    users = load_user_data()
    author_id = str(ctx.author.id)

    if author_id not in users:
        await ctx.send(embed=make_embed("Error", "You are not registered. Use &register <Summoner> <Tag Line>.", 0xFF0000))
        return

    user_data = users[author_id]
    profile_fields = [
        ("Summoner", user_data['summoner'], False),
        ("Tag Line", user_data['tag_line'], False),
    ]

    embed = make_embed(
        title=f"{ctx.author.name}'s Profile",
        description="Here is your registered profile information:",
        color=0x7289DA,
        thumbnail_url=ctx.author.avatar.url if ctx.author.avatar else None,
        fields=profile_fields,
    )
    await ctx.send(embed=embed)


async def error(ctx, *, message: str):
    feedback_data = load_feedback_data()

    new_feedback = {
        "user_id": str(ctx.author.id),
        "user": str(ctx.author),
        "timestamp": str(ctx.message.created_at),
        "message": message,
    }

    feedback_data.append(new_feedback)
    save_feedback_data(feedback_data)

    await ctx.send(embed=make_embed("Feedback Received", "Thank you! Your feedback has been recorded.", 0x00FF00))
