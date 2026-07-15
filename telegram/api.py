import requests
import configparser
from pathlib import Path
from models import Player

config = configparser.ConfigParser()
config.read('config.ini')
BACKEND_URL = f"http://{config['DEFAULT']['BACKHOST']}:{config['DEFAULT']['BACKPORT']}/api"

def _make_request(method, endpoint, data=None, params=None):
    url = f"{BACKEND_URL}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, params=params)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, params=params)
        elif method == "DELETE":
            response = requests.delete(url, json=data, headers=headers, params=params)
        else:
            return None
        
        if response.status_code >= 400:
            print(f"Ошибка {response.status_code}: {response.text}")
            return None
        return response.json()
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return None

#Игроки 

def get_player(chat_id, user_id):
    data = _make_request("GET", f"person/id/{chat_id}")
    if not data:
        return None
    
    for player_data in data:
        if player_data.get('userId') == user_id or player_data.get('user_id') == user_id:
            return Player(
                chat_id=chat_id,
                user_id=user_id,
                name=player_data.get('name', 'Unknown'),
                photo=player_data.get('photo', 'default.jpg'),
                exp=player_data.get('experience', 0),
                money=player_data.get('money', 100),
                hp=player_data.get('hp', 100),
                damage=player_data.get('damage', 20),
                luck=player_data.get('luck', 20) / 100,
                level=player_data.get('level', 1)
            )
    return None

def create_player(player):
    data = {
        'user_id': player.user_id,
        'chat_id': player.chat_id,
        'name': player.name,
        'photo': player.photo,
        'experience': player.exp,
        'money': player.money,
        'hp': player.hp,
        'damage': player.damage,
        'luck': int(player.luck * 100),
        'level': player.level
    }
    return _make_request("POST", "person/create_alt", data)

def update_player(player):
    data = {
        'name': player.name,
        'experience': player.exp,
        'money': player.money,
        'hp': player.hp,
        'damage': player.damage,
        'luck': int(player.luck * 100),
        'level': player.level
    }
    params = {'chat_id': player.chat_id, 'user_id': player.user_id}
    return _make_request("PUT", "person/update", data, params)

def get_all_players():
    data = _make_request("GET", "person/all")
    if not data:
        return []
    
    players = []
    for p in data:
        players.append(Player(
            chat_id=p.get('chatId', 0),
            user_id=p['userId'],
            name=p['name'],
            photo=p['photo'],
            exp=p.get('experience', 0),
            money=p.get('money', 100),
            hp=p.get('hp', 100),
            damage=p.get('damage', 20),
            luck=p.get('luck', 20) / 100,
            level=p.get('level', 1)
        ))
    return players