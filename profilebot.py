import discord
import requests
from time import time
import json
from discord.ext import commands

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

with open('credentials.json') as f:
    data = json.load(f)
api_key = data['api_key']
bot_token = data['bot_token']


def get_summoner_profile(name, tag):
    global api_key

    puuidUrl = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={api_key}'

    response = requests.get(puuidUrl)
    if response.status_code == 200:
        
        puuid = response.json()
        name = puuid["gameName"]
        tag = puuid["tagLine"]

        summoner_profile_url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid["puuid"]}?api_key={api_key}'

        response = requests.get(summoner_profile_url)

        if response.status_code == 200:
            summoner_profile = response.json()
            return summoner_profile, name, tag, puuid["puuid"]
        else:
            print(f'Erreur lors de la récupération du profil {name} #{tag}')
            return None
    else:
        print(f'Erreur lors de la récupération du profil {name} #{tag}')
        return None


def get_ranked_data(summoner_id):
    global api_key
    url = f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ranked_solo = None
        ranked_flex = None
        no_tier = ["MASTER", "GRANDMASTER", "CHALLENGER"]
        for i in data:
            if i['queueType'] == 'RANKED_SOLO_5x5':
                ranked_solo = {
                    'rank': i['tier'] + ((" " + i['rank']) if i['tier'] not in no_tier else ""),
                    'lp': i['leaguePoints'],
                    'wins': i['wins'],
                    'losses': i['losses'],
                    'winrate': round((i['wins'] / (i['wins'] + i['losses'])) * 100, 2)
                }
            elif i['queueType'] == 'RANKED_FLEX_SR':
                ranked_flex = {
                    'rank': i['tier'] + ((" " + i['rank']) if i['tier'] not in no_tier else ""),
                    'lp': i['leaguePoints'],
                    'wins': i['wins'],
                    'losses': i['losses'],
                    'winrate': round((i['wins'] / (i['wins'] + i['losses'])) * 100, 2)
                }
        if ranked_solo is None and ranked_flex is None:
            print("Le joueur n'a pas de classement")
            return None, None
        return ranked_solo, ranked_flex
    else:
        print('Erreur lors de la récupération du classement')
        return None, None
        
def get_mastery_score(puuid):
    global api_key

    url = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/scores/by-puuid/{puuid}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur de la récupération du score de maitrise")
        return None
        

def get_top3_champs(puuid):
    global api_key

    url = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count=3&api_key={api_key}"
    response = requests.get(url)
    result = []
    if response.status_code == 200:
        data = response.json()
        for i in data:
            result.append((i['championId'], i['championPoints']))
        return result
    else:
        print("Erreur de la récupération du score de maitrise")
        return None


def get_champion_name(champion_id, version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/fr_FR/champion.json"
    response = requests.get(url)
    if response.status_code == 200:
        champions = response.json()["data"]
        for champion_name, champion_data in champions.items():
            if champion_data["key"] == str(champion_id):
                return champion_name
    return None


def get_map_name(map_id, version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/fr_FR/map.json"
    response = requests.get(url)
    if response.status_code == 200:
        maps = response.json()["data"]
        return maps[str(map_id)]["MapName"]
    return None


def get_game_type(queue_id):

    if(queue_id == 0):
        return "Custom"

    url = "https://static.developer.riotgames.com/docs/lol/queues.json"
    response = requests.get(url)
    if response.status_code == 200:
        queues = response.json()
        for queue in queues:
            if queue["queueId"] == queue_id:
                return queue["description"]
    return None


def get_current_game(puuid):
    global api_key

    url = f"https://euw1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:

        data = response.json()

        game_type = data['gameQueueConfigId']
        game_map = data['mapId']
        game_start = data['gameStartTime']
        champion_id = None
        
        #Boucle foreach qui parcourt tous les participants jusqu'a trouvé le bon
        for participant in data['participants']:
            if participant['puuid'] == puuid:
                champion_id = participant['championId']
                break

        gameStartTimeMilliseconds = game_start
        currentTimeMilliseconds = time() * 1000
        timeElapsedMilliseconds = currentTimeMilliseconds - gameStartTimeMilliseconds

        timeElapsedSeconds = timeElapsedMilliseconds / 1000
        minutes = timeElapsedSeconds // 60 
        seconds = timeElapsedSeconds % 60

        timeElapsedFormatted = f"{int(minutes):02}:{int(seconds):02}"

        return {'gameType': game_type, 'gameMap': game_map, 'timeElapsedFormatted': timeElapsedFormatted, 'championId': champion_id}
    
    elif response.status_code == 404:
        print("Le joueur n'est pas en partie")
        return None
    else:
        print("Erreur de la récupération de la partie en cours")
        return None


@bot.command(name='profile', help='Affiche le profil League of Legends d\'un invocateur')
async def profile(ctx, *args):
    
    name_and_tag = " ".join(args)
    name_and_tag = name_and_tag.replace(" ", "")

    if "#" not in name_and_tag:
        await ctx.send("Veuillez saisir un nom au format suivant : pseudo#tag")
        return

    name = name_and_tag.split("#")[0]
    tag = name_and_tag.split("#")[1]

    summoner_profile = get_summoner_profile(name, tag)

    if summoner_profile is None:
        await ctx.send(f'Impossible de trouver le profil League of Legends pour {name}#{tag}')
        return

    current_game_info = get_current_game(summoner_profile[3])
    
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]

    embed = discord.Embed(title='Profil de ' + summoner_profile[1] + " #" + summoner_profile[2],
                          description='Informations du profil League of Legends',
                          color=0x00ff00)
    
    # Initial message
    message = await ctx.send(embed=embed)
    
    ranked_solo_data, ranked_flex_data = get_ranked_data(summoner_profile[0]['id'])
    mastery_score = get_mastery_score(summoner_profile[3])
    
    url = 'http://ddragon.leagueoflegends.com/cdn/' + version + f'/img/profileicon/{summoner_profile[0]["profileIconId"]}.png'
    response = requests.get(url)
    if response.headers.get('content-type').startswith('image'):
        embed.set_thumbnail(url=url)
    else:
        embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/9.23.1/img/profileicon/0.png")
    
    # Update with general information
    embed.add_field(name='Informations générales',
                    value="Niveau : " + str(summoner_profile[0]['summonerLevel']) +
                          "\n Solo/Duo : " + ((ranked_solo_data['rank'] + " " + str(ranked_solo_data['lp']) + " LP") if ranked_solo_data is not None else "Non classé") +
                          "\n Score de maitrise : " + str(mastery_score),
                    inline=True)
    
    # Update with top 3 champs
    top3 = get_top3_champs(summoner_profile[3])
    embed.add_field(name="Meilleure maitrise de Champions",
                    value="1 : " + get_champion_name(top3[0][0], version) + " - " + str(top3[0][1]) + " points" +
                          "\n2 : " + get_champion_name(top3[1][0], version) + " - " + str(top3[1][1]) + " points" +
                          "\n3 : " + get_champion_name(top3[2][0], version) + " - " + str(top3[2][1]) + " points",
                    inline=False)
    
    await message.edit(embed=embed)
    
    # Update with ranked solo/duo information
    if ranked_solo_data is not None:
        embed.add_field(name='Classés Solo/Duo',
                        value="Rang : " + ranked_solo_data['rank'] +
                              "\n LP : " + str(ranked_solo_data['lp']) +
                              "\n Victoires - Défaites : " + str(ranked_solo_data['wins']) + " - " + str(ranked_solo_data['losses']) +
                              "\n Winrate : " + str(ranked_solo_data['winrate']) + "%",
                        inline=True)
    else:
        embed.add_field(name='Classés Solo/Duo',
                        value="Non classé",
                        inline=True)
        
    await message.edit(embed=embed)
    
    # Update with current game information

    if current_game_info is not None:
        embed.add_field(name='Statut du joueur',
                        value="Mode : " + get_game_type(current_game_info['gameType']) +
                              "\n Map : " + get_map_name(current_game_info['gameMap'], version) +
                              "\n Durée : " + current_game_info['timeElapsedFormatted'] +
                              "\n Champion : " + get_champion_name(current_game_info['championId'], version),
                        inline=False)
    else:
        embed.add_field(name='Statut du joueur',
                        value='Pas en partie',
                        inline=False)
    
    await message.edit(embed=embed)
    
    # Update with ranked flex information
    if ranked_flex_data is not None:
        embed.add_field(name='Classés Flexible',
                        value="Rang : " + ranked_flex_data['rank'] +
                              "\n LP : " + str(ranked_flex_data['lp']) +
                              "\n Victoires - Défaites : " + str(ranked_flex_data['wins']) + " - " + str(ranked_flex_data['losses']) +
                              "\n Winrate : " + str(ranked_flex_data['winrate']) + "%",
                        inline=False)
    else:
        embed.add_field(name='Classés Flexible',
                        value="Non classé",
                        inline=False)
    
    await message.edit(embed=embed)


bot.run(bot_token)