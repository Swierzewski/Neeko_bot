from riot_lol import RiotProfile
from utils import make_embed, load_user_data


async def get_lol_profile_data(ctx, summoner_input: str = None):
    """Returns (name, tag) from a registered user or a parsed 'Name#TAG' string."""
    if summoner_input is not None:
        if '#' not in summoner_input:
            await ctx.send(embed=make_embed(
                "Invalid Format",
                "Provide a summoner in the format `Name#TAG`.",
                0xFF5733,
            ))
            return None, None
        name, tag = summoner_input.split('#', 1)
        return name.strip(), tag.strip()

    users = load_user_data()
    author_id = str(ctx.author.id)

    if author_id in users:
        user_data = users[author_id]
        return user_data['summoner'], user_data['tag_line']

    await ctx.send(embed=make_embed(
        "Not Registered",
        "Register with `&register YourName TAG` or pass a summoner like `Name#TAG`.",
        0xFF5733,
    ))
    return None, None


async def streak(ctx, summoner_input: str = None):
    name, tag = await get_lol_profile_data(ctx, summoner_input)
    if not name:
        return

    await ctx.send(f"Checking streak for `{name}#{tag}`...")
    profile = RiotProfile(name, tag)
    data = profile.get_winstreak()

    if data == -1 or data is None:
        await ctx.send(embed=make_embed("Error", "Could not determine winstreak.", 0xFF5733))
        return

    streak_type = 'win' if data['bool'] else 'losing'
    description = f"You have a **{streak_type} streak** of: **{data['winstreak']}**"
    await ctx.send(embed=make_embed(f"{name}'s Current Streak", description, 0xECF22C))


async def played(ctx, summoner_input: str = None):
    name, tag = await get_lol_profile_data(ctx, summoner_input)
    if not name:
        return

    await ctx.send(f"Computing time played for `{name}#{tag}`...")
    profile = RiotProfile(name, tag)
    data = profile.get_hours_played()

    if data in (-1, -2) or data is None:
        await ctx.send(embed=make_embed("Error", "Could not calculate time played.", 0xFF5733))
        return

    description = (
        f"Today you played: {data['time_today']}\n"
        f"This week you played: {data['time_week']}"
    )
    await ctx.send(embed=make_embed(f"{name}'s Playtime Stats", description, 0xECF22C))


async def lastgame(ctx, summoner_input: str = None):
    name, tag = await get_lol_profile_data(ctx, summoner_input)
    if not name:
        return

    await ctx.send(f"Searching last game for `{name}#{tag}`...")

    profile = RiotProfile(name, tag)
    data = profile.get_last_game()
    if data == -1 or data is None:
        await ctx.send(embed=make_embed("Error", "Could not find a recent game for this player.", 0xFF5733))
        return

    result = "won" if data['win'] else "lost"
    color = 0x7CFC00 if data['win'] else 0xFF0000
    description = (
        f"You {result} with **{data['champion']}** ({data['lane']}): "
        f"{data['kills']}/{data['deaths']}/{data['assists']} ({data['kda']} KDA)"
    )
    await ctx.send(embed=make_embed(f"{name}'s Last Game", description, color))


async def history(ctx, count: int = 5, *, summoner_input: str = None):
    name, tag = await get_lol_profile_data(ctx, summoner_input)
    if not name:
        return

    count = max(1, min(count, 10))
    await ctx.send(f"Fetching last {count} games for `{name}#{tag}`...")
    profile = RiotProfile(name, tag)
    data = profile.get_match_history(count)

    if data == -1 or data is None:
        await ctx.send(embed=make_embed("Error", "Could not fetch match history.", 0xFF5733))
        return

    if not data:
        await ctx.send(embed=make_embed("No Games", f"No recent games found for {name}.", 0xFF5733))
        return

    lines = []
    for game in data:
        icon = "✅" if game['win'] else "❌"
        lines.append(
            f"{icon} **{game['champion']}** ({game['lane']}) — "
            f"{game['kills']}/{game['deaths']}/{game['assists']} ({game['kda']} KDA)"
        )

    await ctx.send(embed=make_embed(f"{name}'s Last {len(data)} Games", "\n".join(lines), 0x3498DB))


async def mastery(ctx, summoner_input: str = None):
    name, tag = await get_lol_profile_data(ctx, summoner_input)
    if not name:
        return

    await ctx.send(f"Fetching masteries for `{name}#{tag}`...")
    profile = RiotProfile(name, tag)
    data = profile.get_top_masteries()

    if data == -1 or data is None:
        await ctx.send(embed=make_embed("Error", "Could not fetch champion masteries.", 0xFF5733))
        return

    lines = [
        f"**{i}.** {champ['champion_name']} — Level {champ['mastery_level']} ({champ['mastery_points']:,} pts)"
        for i, champ in enumerate(data, 1)
    ]
    await ctx.send(embed=make_embed(f"{name}'s Top Masteries", "\n".join(lines), 0x9B59B6))


async def livegame(ctx, summoner_input: str = None):
    name, tag = await get_lol_profile_data(ctx, summoner_input)
    if not name:
        return

    await ctx.send(f"Checking live game for `{name}#{tag}`...")
    profile = RiotProfile(name, tag)
    data = profile.get_live_game()

    if data == -1:
        await ctx.send(embed=make_embed("Error", "Could not check live game status.", 0xFF5733))
        return

    if data is None:
        await ctx.send(embed=make_embed(f"{name} is not in a game", "Currently offline or in lobby.", 0x808080))
        return

    description = (
        f"Playing **{data['champion']}** in **{data['game_mode']}**\n"
        f"Game duration: {data['duration']}"
    )
    await ctx.send(embed=make_embed(f"{name} is in a game!", description, 0x1ABC9C))


async def rank(ctx, summoner_input: str = None):
    name, tag = await get_lol_profile_data(ctx, summoner_input)
    if not name:
        return

    await ctx.send(f"Searching ranks for `{name}#{tag}`...")

    profile = RiotProfile(name, tag)
    data = profile.get_ranked_stats()
    if data == -1 or data is None:
        await ctx.send(embed=make_embed("Error", "Could not find player or their ranked stats.", 0xFF5733))
        return

    solo_tier = data.get('tier_solo', 'Unranked')
    solo_lp = data.get('lp_solo', 0)
    solo_wr = data.get('winrate_solo', 0)

    flex_tier = data.get('tier_flex', 'Unranked')
    flex_lp = data.get('lp_flex', 0)
    flex_wr = data.get('winrate_flex', 0)

    description = (
        f"**Solo/Duo**: {solo_tier} {solo_lp}LP ({solo_wr}% WR)\n"
        f"**Flex**: {flex_tier} {flex_lp}LP ({flex_wr}% WR)"
    )
    await ctx.send(embed=make_embed(f"{name}'s Ranked Stats", description, 0xECF22C))
