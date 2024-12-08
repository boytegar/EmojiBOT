import base64
import json
import os
import random
import time
from urllib.parse import parse_qs, unquote
import requests
from datetime import datetime



class Emoji:
    def __init__(self):
        self.headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Microsoft Edge;v=131, Chromium;v=131, Not_A Brand;v=24, Microsoft Edge WebView2;v=131"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Referer": "https://emojiapp.xyz/?tgWebAppStartParam=7671403792",
        "Referrer-Policy": "strict-origin-when-cross-origin"
        }
    
    def print_(self, word):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"[{now}] | {word}")
    
    def make_request(self, method, url, headers, json=None, data=None):
        retry_count = 0
        while True:
            time.sleep(2)
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, json=json)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json, data=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=json, data=data)
            else:
                raise ValueError("Invalid method.")
            
            if response.status_code >= 500:
                if retry_count > 5:
                    self.print_(f"Status Code: {response.status_code} | {response.text}")
                    return None
                retry_count += 1
            elif response.status_code >= 400:
                self.print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            elif response.status_code >= 200:
                return response
    
    def auth(self, query):
        url = "https://emojiapp.xyz/api/auth"
        payload = {
        "initData": query,
        "refererId":"7671403792"
        }
        headers = {
            **self.headers
        }
        response = self.make_request('post',url, headers=headers, json=payload)
        if response is not None:
            jsons = response.json()
            return jsons
    
    def check_elig(self, token):
        url = "https://emojiapp.xyz/api/users/free-tickets-eligibility"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        response = self.make_request('post',url, headers=headers)

        if response is not None:
            jsons = response.json()
            canClaim = jsons.get('canClaim', False)
            nextClaim = jsons.get('nextClaim', 'Not available')
            if canClaim:
                self.print_(f"Get Free Ticket")
                self.claim_ticket(token)
            return jsons
    
    def claim_ticket(self, token):
        url = "https://emojiapp.xyz/api/users/claim-free-tickets"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        response = self.make_request('post',url, headers=headers)
        if response is not None:
            self.print_("Claim ticket Done")
        else:
            self.print_("Claim ticket Failed")
    
    def get_tasks(self, token):
        url = "https://emojiapp.xyz/api/quests"
    
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        response = self.make_request('get',url, headers=headers)
        if response is not None:
            data = response.json()
            quests = data.get('quests', {})
            main_quest = list(quests.values())
            for quest_items in main_quest:
                for quest in quest_items:
                    id = quest.get('id')
                    text = quest.get('text')
                    completed = quest.get('completed')
                    if text in ["Make a TON transaction", "Purchase Telegram Stars", "One-time Stars purchase","One-time TON transaction", "Boost Emoji"]:
                        self.print_(f"Quest: {text} Skip")
                        continue
                    else:
                        if completed:
                            self.print_(f"Task {text} Completed")
                        else:
                            self.verify_task(token, id, text)
    
    def verify_task(self, token, id, text):
        url = f"https://emojiapp.xyz/api/quests/verify?questId={id}"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        response = self.make_request('get',url, headers=headers)
        if response is not None:
            data = response.json()
            message = data.get('message')
            user = data.get('user')
            amountOfTickets = user.get('amountOfTickets')
            self.print_(f"Task {text}")
            self.print_(f"{message} | total reward ticket : {amountOfTickets}")
    
    def play_game(self, token):
        url = "https://emojiapp.xyz/api/play"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        list_games = ["Basketball", "Football", "Darts"]
        games = random.choice(list_games)
        self.print_(f"Playing Games {games}")
        payload = {"gameName": games}
        response = self.make_request('post' ,url, headers=headers, json=payload)
        if response is not None:
            data = response.json()
            message = data.get('message','')
            pointsWon = data.get('pointsWon',0)
            self.print_(f"{message}, get point : {pointsWon}")

        
   