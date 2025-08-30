import cfscrape
import requests as req
from riotwatcher import LolWatcher, RiotWatcher, exceptions
from datetime import timedelta, datetime
from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv('RIOT_TOKEN')
scraper = cfscrape.create_scraper()

region_lol = "EUW1"
region_riot = "EUROPE"
tag_line = "EUW"
print(f"The region set are: LOL={region_lol} and RIOT={region_riot}")
print(f"The default tagline is: {tag_line}")

watcher_lol = LolWatcher(token)
watcher_riot = RiotWatcher(token)


class RiotProfile():
    def __init__(self, summoner_name, tag_line=tag_line):
        self.watcher_lol = watcher_lol
        self.watcher_riot = watcher_riot
        self.region_lol = region_lol
        self.region_riot = region_riot
        self.summoner_name = summoner_name
        self.summoner_tag_line = tag_line
        self.summoner_info = self.get_summoner_by_puuid()


    def get_info_riot(self) -> dict:
        try:
            return self.watcher_riot.account.by_riot_id(region_riot, self.summoner_name, self.summoner_tag_line)
        except exceptions.ApiError:
            print(f"user does not exist: {self.summoner_name}")
            return -1
        except Exception as err:
            print(err)
            return -1


    def get_summoner_by_puuid(self) -> dict:
        try:
            riot_account = self.watcher_riot.account.by_riot_id(region_riot, self.summoner_name, self.summoner_tag_line)
            return self.watcher_lol.summoner.by_puuid(self.region_lol, riot_account['puuid'])
        except exceptions.ApiError:
            print(f"user does not exist: {self.summoner_name}")
            return -1
        except Exception as err:
            print(err)
            return -1
    

    def get_ranked_stats(self) -> dict:
        try:
            summoner = self.summoner_info
            my_ranked_stats = self.watcher_lol.league.by_summoner(self.region_lol, summoner['id'])
            print(my_ranked_stats)
            my_ranked_stats_solo = my_ranked_stats[0]
            my_ranked_stats_flex = my_ranked_stats[1]

            tier_solo = str(my_ranked_stats_solo['tier']) + " " + str(my_ranked_stats_solo['rank'])
            tier_flex = str(my_ranked_stats_flex['tier']) + " " + str(my_ranked_stats_flex['rank'])

            winrate_solo = int(my_ranked_stats_solo["wins"]) / (int(my_ranked_stats_solo["wins"]) + int(my_ranked_stats_solo["losses"]))
            winrate_flex = int(my_ranked_stats_flex["wins"]) / (int(my_ranked_stats_flex["wins"]) + int(my_ranked_stats_flex["losses"]))
            
            return {'tier_solo': tier_solo, 'tier_flex': tier_flex,
            'winrate_solo': round(winrate_solo*100), 'winrate_flex': round(winrate_flex*100),
            'lp_solo': my_ranked_stats_solo['leaguePoints'], 'lp_flex': my_ranked_stats_flex['leaguePoints']}
        
        except Exception as err:
            print(err)
            return -1
        

    def get_last_game(self) -> dict:
        try:
            summoner = self.summoner_info
            my_matches = watcher_lol.match.matchlist_by_puuid(self.region_lol, summoner['puuid']) # 20 matches
            last_match = watcher_lol.match.by_id(self.region_lol, my_matches[0])

            player_data = None
            for player in last_match['info']['participants']:
                if player['puuid'] == summoner['puuid']:
                    player_data = player

            return {'win': player_data['win'], 
                    'champion': player_data['championName'],
                    'lane': player_data['lane'] if last_match['info']['gameMode'] != 'ARAM' else 'ARAM',
                    'kills': player_data['kills'],
                    'deaths': player_data['deaths'],
                    'assists': player_data['assists'],
                    'kda': round((player_data['kills'] + player_data['assists']) / player_data['deaths'] if player_data['deaths'] != 0 else (player_data['kills'] + player_data['assists']) / 1, 2)
                    }
        
        except Exception as err:
            print(err)
            return -1


    def get_hours_played(self) -> dict:
        try:
            summoner = self.summoner_info
            my_matches = watcher_lol.match.matchlist_by_puuid(self.region_lol, summoner['puuid']) # 20 matches
            
            today = datetime.today().strftime("%d/%m/%Y")
            monday = (datetime.today() - timedelta(days=int(datetime.today().isoweekday())-1)).strftime("%d/%m/%Y")
            print(monday)

            time_today = 0
            time_week = 0


            for id_match in my_matches:
                game_info = watcher_lol.match.by_id(self.region_lol, id_match)['info']
                game_creation = datetime.fromtimestamp(int(game_info["gameCreation"])/1000).strftime("%d/%m/%Y")

                if game_creation == today:
                    time_today += game_info["gameDuration"]
                    time_week += game_info["gameDuration"]
                else:
                    if monday > game_creation:
                        break
                    if game_creation != monday:
                        time_week += game_info["gameDuration"]
                    else:
                        break

            return {'time_today': timedelta(seconds=time_today), 'time_week': timedelta(seconds=time_week)}
        except exceptions.ApiError as err:
            print(err)
            return -2
        except Exception as err:
            print(err)
            return -1


    # get last game played of summoner
    def get_last_game_free(self) -> dict:
        try:
            summoner = self.summoner_info
            my_matches = watcher_lol.match.matchlist_by_puuid(self.region_lol, summoner['puuid']) # 20 matches

            today = datetime.today().strftime("%H:%M:%S")
            game_info = watcher_lol.match.by_id(self.region_lol, my_matches[0])['info']
            game_creation = datetime.fromtimestamp(int(game_info["gameCreation"])/1000).strftime("%H:%M:%S")
            s1 = datetime.strptime(today, "%H:%M:%S")
            s2 = datetime.strptime(game_creation, "%H:%M:%S")

            boolean = True if abs(s1 - s2).seconds >= 86400 else False

            today = datetime.today().strftime("%d/%m/%Y")
            game_info = watcher_lol.match.by_id(self.region_lol, my_matches[0])['info']
            game_creation = datetime.fromtimestamp(int(game_info["gameCreation"])/1000).strftime("%d/%m/%Y")
            d1 = datetime.strptime(today, "%d/%m/%Y")
            d2 = datetime.strptime(game_creation, "%d/%m/%Y")


            return {'free': boolean, 'days': abs(d1 - d2).days}

        except Exception as err:
            print(err)
            return -1


    # get winstreak of summoner
    def get_winstreak(self) -> dict:
        try:
            summoner = self.summoner_info
            my_matches = watcher_lol.match.matchlist_by_puuid(self.region_lol, summoner['puuid']) # 20 matches

            last_boolean = False
            count = 0

            for id_match in my_matches:
                game_info = watcher_lol.match.by_id(self.region_lol, id_match)['info']
                player_data = None
                for player in game_info['participants']:
                    if player['puuid'] == summoner['puuid']:
                        player_data = player
                boolean = player_data['win']

                if count == 0:
                    last_boolean = boolean

                if boolean == last_boolean:
                    count += 1
                else:
                    break
                
            return {'winstreak': count, 'bool': last_boolean}

        except Exception as err:
            print(err)
            return -1


# TESTING
# rp = RiotProfile("Vic", "KCWIN")
# print(rp.get_info_riot())
# print(rp.get_summoner_by_puuid())

# print(rp.get_ranked_stats())
# print(rp.get_last_game())

# print(rp.get_hours_played())
# print(rp.get_last_game_free())

# print(rp.get_winstreak())