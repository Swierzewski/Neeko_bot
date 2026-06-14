from utils import make_embed, load_feedback_data, save_feedback_data
import discord


async def help(ctx, category: str = None, bot_prefix: str = "&"):
    """Shows a list of commands."""
    if category is None:
        embed = discord.Embed(
            title="Fun Bot Help",
            description=f"Use `{bot_prefix}help <category>` to see commands.\n**Categories:** `other`",
            color=0xeee657,
        )
        await ctx.send(embed=embed)
        return

    category = category.lower()

    if category == "other":
        embed = discord.Embed(title="Other Commands", color=0x2ecc71)
        embed.add_field(name=f"{bot_prefix}blocus", value="Send a random motivational gif", inline=False)
        embed.add_field(name=f"{bot_prefix}blocus add <url>", value="Add a gif/image URL to the blocus list", inline=False)
        embed.add_field(name=f"{bot_prefix}réussite", value="Get your session success percentage", inline=False)
        embed.add_field(name=f"{bot_prefix}question <message>", value="Ask the bot a yes/no question", inline=False)
        embed.add_field(name=f"{bot_prefix}image <name>", value="Send a saved image by keyword", inline=False)
        embed.add_field(name=f"{bot_prefix}video <name>", value="Send a saved video by keyword", inline=False)
        embed.add_field(name=f"{bot_prefix}search <query>", value="Search and post an image from the web", inline=False)
        embed.add_field(name=f"{bot_prefix}trans <from> <to> <text>", value="Translate text with DeepL (e.g. EN FR Hello)", inline=False)
        embed.add_field(name=f"{bot_prefix}hello", value="Say hello to the bot", inline=False)
        embed.add_field(name=f"{bot_prefix}error <message>", value="Report a bug or send feedback", inline=False)
        embed.add_field(name=f"{bot_prefix}paypal", value="Get the PayPal link", inline=False)

    else:
        embed = make_embed("Error", "Invalid category. Please use `other`.", 0xFF0000)

    await ctx.send(embed=embed)


async def hello(ctx):
    await ctx.send(embed=make_embed("Hello!", "My name is Neeko!", 0xECF22C))


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
