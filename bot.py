import base64
import json
import os
import random
import sys
import time
from urllib.parse import parse_qs, unquote
import requests
from datetime import datetime, timedelta

from emoji import Emoji

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_query():
    try:
        with open('emoji_query.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File .txt not found.")
        return [  ]
    except Exception as e:
        print("Failed get Query :", str(e))
        return [  ]

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def print_delay(delay):
    print()
    while delay > 0:
        now = datetime.now().isoformat(" ").split(".")[0]
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        sys.stdout.write(f"\r[{now}] | Waiting Time: {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds")
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1
    print_("Waiting Done, Starting....\n")
       
def main():
    selector_game = input("auto play game ? y/n : ").strip().lower()
    selector_task = input("auto clear task ? y/n : ").strip().lower()
    while True:
        start_time = time.time()
        delay = 8*3750
        clear_terminal()
        queries = load_query()
        sum = len(queries)
        emoji = Emoji()
        total_points = 0
        for index, query in enumerate(queries, start=1):
            data_auth = emoji.auth(query)
            if data_auth is not None:
                user = data_auth.get('user')
                token = data_auth.get('token')
                username = user.get('username','')
                points = user.get('points',0)
                amountOfTickets = user.get('amountOfTickets')
                rewardStreakDay = user.get('rewardStreakDay')
                total_points += points
                print_(f"[SxG]===== Account {index}/{sum} | {username} =====[SxG]")
                print_(f"points : {points} | ticket : {amountOfTickets} | streak : {rewardStreakDay} days")
                emoji.check_elig(token)
                if selector_game == 'y':
                    if amountOfTickets > 0:
                        print_("Play Game")
                        for i in range(amountOfTickets):
                            emoji.play_game(token)
                
                if selector_task == 'y':
                    print_("Start Task")
                    emoji.get_tasks(token)

        
        end_time = time.time()
        total = delay - (end_time-start_time)
        print_(f"Total Account : {sum} | Total Points : {total_points}")
        if total > 0:
            print_delay(total)

if __name__ == "__main__":
     main()