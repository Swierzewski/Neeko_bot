from riot_lol import *
from utils import *


async def get_lol_profile_data(ctx, summoner_input: str = None):
    if summoner_input is None:
        users = load_user_data()
        author_id = str(ctx.author.id)
        
        if author_id in users:
            user_data = users[author_id]
            name, tag = user_data['summoner'], user_data['tag_line']
            
            return name, tag
        else:
            await ctx.send(embed=make_embed(
                "Not Registered",
                "Please register your account with `$register YourName#TAG REGION` or provide a summoner name to look up.",
                0xFF5733
            ))
            return None, None, None, None
    else:
        return user_data['summoner'], user_data['tag_line']
    

async def streak(ctx, summoner_input: str = None):
    name, tag= await get_lol_profile_data(ctx, summoner_input)
    if not name: return

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
    if not name: return

    await ctx.send(f"Computing time played for `{name}#{tag}`...")
    profile = RiotProfile(name, tag)
    data = profile.get_hours_played()

    if data == -1 or data is None:
        await ctx.send(embed=make_embed("Error", "Could not calculate time played.", 0xFF5733))
        return

    description = (f"Today you played: {data['time_today']}\n"
                   f"This week you played: {data['time_week']}")
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
    description = (f"You {result} with **{data['champion']}** ({data['lane']}): "
                   f"{data['kills']}/{data['deaths']}/{data['assists']} ({data['kda']} KDA)")
                   
    await ctx.send(embed=make_embed(f"{name}'s Last Game", description, color))


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
    solo_lp = data.get('lp_solo', '')
    solo_wr = data.get('winrate_solo', '')
    
    flex_tier = data.get('tier_flex', 'Unranked')
    flex_lp = data.get('lp_flex', '')
    flex_wr = data.get('winrate_flex', '')
    
    description = (f"**Solo/Duo**: {solo_tier} {solo_lp}LP ({solo_wr}% WR)\n"
                   f"**Flex**: {flex_tier} {flex_lp}LP ({flex_wr}% WR)")
                   
    await ctx.send(embed=make_embed(f"{name}'s Ranked Stats", description, 0xECF22C))