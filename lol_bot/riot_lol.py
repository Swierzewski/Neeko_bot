from riotwatcher import LolWatcher, RiotWatcher, exceptions
from datetime import timedelta, datetime
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent / '.env')
token = os.getenv('RIOT_TOKEN')

region_lol = "EUW1"
region_riot = "EUROPE"
default_tag_line = "EUW"
print(f"The region set are: LOL={region_lol} and RIOT={region_riot}")
print(f"The default tagline is: {default_tag_line}")

watcher_lol = LolWatcher(token)
watcher_riot = RiotWatcher(token)

_champion_names: dict[int, str] = {}


def _get_champion_names() -> dict[int, str]:
    global _champion_names
    if _champion_names:
        return _champion_names
    try:
        from riotwatcher import DataDragon
        dd = DataDragon()
        versions = dd.versions_for_region(region_lol)
        champs = dd.champions(versions[0])
        _champion_names = {int(info['key']): name for name, info in champs['data'].items()}
    except Exception as e:
        print(f"Could not load champion names from DataDragon: {e}")
    return _champion_names


class RiotProfile:
    def __init__(self, summoner_name, tag_line=default_tag_line):
        self.watcher_lol = watcher_lol
        self.watcher_riot = watcher_riot
        self.region_lol = region_lol
        self.region_riot = region_riot
        self.summoner_name = summoner_name
        self.summoner_tag_line = tag_line
        self.summoner_info = self._get_summoner_by_puuid()

    def _get_summoner_by_puuid(self) -> dict:
        try:
            riot_account = self.watcher_riot.account.by_riot_id(
                self.region_riot, self.summoner_name, self.summoner_tag_line
            )
            return self.watcher_lol.summoner.by_puuid(self.region_lol, riot_account['puuid'])
        except exceptions.ApiError:
            print(f"User does not exist: {self.summoner_name}")
            return -1
        except Exception as err:
            print(err)
            return -1

    def get_ranked_stats(self) -> dict:
        try:
            summoner = self.summoner_info
            if summoner == -1:
                return -1

            all_queues = self.watcher_lol.league.by_summoner(self.region_lol, summoner['id'])

            solo_stats = next((q for q in all_queues if q['queueType'] == 'RANKED_SOLO_5x5'), None)
            flex_stats = next((q for q in all_queues if q['queueType'] == 'RANKED_FLEX_SR'), None)

            def _format(stats):
                if not stats:
                    return 'Unranked', 0, 0
                tier = f"{stats['tier']} {stats['rank']}"
                wr = round(stats['wins'] / (stats['wins'] + stats['losses']) * 100)
                return tier, stats['leaguePoints'], wr

            tier_solo, lp_solo, wr_solo = _format(solo_stats)
            tier_flex, lp_flex, wr_flex = _format(flex_stats)

            return {
                'tier_solo': tier_solo, 'tier_flex': tier_flex,
                'winrate_solo': wr_solo, 'winrate_flex': wr_flex,
                'lp_solo': lp_solo, 'lp_flex': lp_flex,
            }

        except Exception as err:
            print(err)
            return -1

    def get_last_game(self) -> dict:
        try:
            summoner = self.summoner_info
            if summoner == -1:
                return -1

            my_matches = self.watcher_lol.match.matchlist_by_puuid(self.region_riot, summoner['puuid'])
            last_match = self.watcher_lol.match.by_id(self.region_riot, my_matches[0])

            player_data = next(
                (p for p in last_match['info']['participants'] if p['puuid'] == summoner['puuid']),
                None,
            )
            if player_data is None:
                return -1

            deaths = player_data['deaths'] or 1
            kda = round((player_data['kills'] + player_data['assists']) / deaths, 2)

            return {
                'win': player_data['win'],
                'champion': player_data['championName'],
                'lane': player_data['lane'] if last_match['info']['gameMode'] != 'ARAM' else 'ARAM',
                'kills': player_data['kills'],
                'deaths': player_data['deaths'],
                'assists': player_data['assists'],
                'kda': kda,
            }

        except Exception as err:
            print(err)
            return -1

    def get_hours_played(self) -> dict:
        try:
            summoner = self.summoner_info
            if summoner == -1:
                return -1

            my_matches = self.watcher_lol.match.matchlist_by_puuid(self.region_riot, summoner['puuid'])

            today = datetime.today().date()
            monday = today - timedelta(days=today.isoweekday() - 1)

            time_today = 0
            time_week = 0

            for id_match in my_matches:
                game_info = self.watcher_lol.match.by_id(self.region_riot, id_match)['info']
                game_date = datetime.fromtimestamp(int(game_info["gameCreation"]) / 1000).date()

                if game_date < monday:
                    break

                time_week += game_info["gameDuration"]
                if game_date == today:
                    time_today += game_info["gameDuration"]

            return {
                'time_today': timedelta(seconds=time_today),
                'time_week': timedelta(seconds=time_week),
            }

        except exceptions.ApiError as err:
            print(err)
            return -2
        except Exception as err:
            print(err)
            return -1

    def get_winstreak(self) -> dict:
        try:
            summoner = self.summoner_info
            if summoner == -1:
                return -1

            my_matches = self.watcher_lol.match.matchlist_by_puuid(self.region_riot, summoner['puuid'])

            last_result = None
            count = 0

            for id_match in my_matches:
                game_info = self.watcher_lol.match.by_id(self.region_riot, id_match)['info']
                player_data = next(
                    (p for p in game_info['participants'] if p['puuid'] == summoner['puuid']),
                    None,
                )
                if player_data is None:
                    continue

                result = player_data['win']
                if last_result is None:
                    last_result = result

                if result == last_result:
                    count += 1
                else:
                    break

            return {'winstreak': count, 'bool': last_result}

        except Exception as err:
            print(err)
            return -1

    def get_match_history(self, count: int = 5) -> list:
        try:
            summoner = self.summoner_info
            if summoner == -1:
                return -1

            match_ids = self.watcher_lol.match.matchlist_by_puuid(
                self.region_riot, summoner['puuid'], count=count
            )

            games = []
            for match_id in match_ids:
                match = self.watcher_lol.match.by_id(self.region_riot, match_id)
                player_data = next(
                    (p for p in match['info']['participants'] if p['puuid'] == summoner['puuid']),
                    None,
                )
                if player_data is None:
                    continue

                deaths = player_data['deaths'] or 1
                kda = round((player_data['kills'] + player_data['assists']) / deaths, 2)
                mode = match['info']['gameMode']
                lane = 'ARAM' if mode == 'ARAM' else player_data['lane']

                games.append({
                    'win': player_data['win'],
                    'champion': player_data['championName'],
                    'lane': lane,
                    'kills': player_data['kills'],
                    'deaths': player_data['deaths'],
                    'assists': player_data['assists'],
                    'kda': kda,
                })

            return games

        except Exception as err:
            print(err)
            return -1

    def get_top_masteries(self, count: int = 5) -> list:
        try:
            summoner = self.summoner_info
            if summoner == -1:
                return -1

            masteries = self.watcher_lol.champion_mastery.top_on_summoner(
                self.region_lol, summoner['id'], count=count
            )
            champ_names = _get_champion_names()

            return [
                {
                    'champion_name': champ_names.get(m['championId'], f"#{m['championId']}"),
                    'mastery_level': m['championLevel'],
                    'mastery_points': m['championPoints'],
                }
                for m in masteries
            ]

        except Exception as err:
            print(err)
            return -1

    def get_live_game(self) -> dict | None:
        try:
            summoner = self.summoner_info
            if summoner == -1:
                return -1

            game = self.watcher_lol.spectator.by_summoner(self.region_lol, summoner['id'])

            participant = next(
                (p for p in game['participants'] if p.get('summonerId') == summoner['id']),
                None,
            )
            if participant is None:
                return -1

            champ_names = _get_champion_names()
            champion_name = champ_names.get(participant['championId'], f"#{participant['championId']}")

            return {
                'champion': champion_name,
                'game_mode': game.get('gameMode', 'Unknown'),
                'duration': timedelta(seconds=game.get('gameLength', 0)),
            }

        except exceptions.ApiError as e:
            if e.response.status_code == 404:
                return None
            print(e)
            return -1
        except Exception as err:
            print(err)
            return -1
