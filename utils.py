import logging
import random
from os import system
from time import sleep

from colorama import Fore
from tqdm import trange
import yaml

logging.getLogger().setLevel(logging.INFO)
config = ''
with open("config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)


def welcome_banner():
    print(Fore.RED + """

 ▄████▄   ██░ ██ ▓█████   ▄████   ▄████     ▄▄▄       █    ██ ▄▄▄█████▓ ▒█████   ███▄ ▄███▓ ▄▄▄      ▄▄▄█████▓ ██▓ ▒█████   ███▄    █
▒██▀ ▀█  ▓██░ ██▒▓█   ▀  ██▒ ▀█▒ ██▒ ▀█▒   ▒████▄     ██  ▓██▒▓  ██▒ ▓▒▒██▒  ██▒▓██▒▀█▀ ██▒▒████▄    ▓  ██▒ ▓▒▓██▒▒██▒  ██▒ ██ ▀█   █
▒▓█    ▄ ▒██▀▀██░▒███   ▒██░▄▄▄░▒██░▄▄▄░   ▒██  ▀█▄  ▓██  ▒██░▒ ▓██░ ▒░▒██░  ██▒▓██    ▓██░▒██  ▀█▄  ▒ ▓██░ ▒░▒██▒▒██░  ██▒▓██  ▀█ ██▒
▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ░▓█  ██▓░▓█  ██▓   ░██▄▄▄▄██ ▓▓█  ░██░░ ▓██▓ ░ ▒██   ██░▒██    ▒██ ░██▄▄▄▄██ ░ ▓██▓ ░ ░██░▒██   ██░▓██▒  ▐▌██▒
▒ ▓███▀ ░░▓█▒░██▓░▒████▒░▒▓███▀▒░▒▓███▀▒    ▓█   ▓██▒▒▒█████▓   ▒██▒ ░ ░ ████▓▒░▒██▒   ░██▒ ▓█   ▓██▒  ▒██▒ ░ ░██░░ ████▓▒░▒██░   ▓██░
░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░ ░▒   ▒  ░▒   ▒     ▒▒   ▓▒█░░▒▓▒ ▒ ▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ░  ░ ▒▒   ▓▒█░  ▒ ░░   ░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒
  ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░   ░   ░   ░      ▒   ▒▒ ░░░▒░ ░ ░     ░      ░ ▒ ▒░ ░  ░      ░  ▒   ▒▒ ░    ░     ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
░         ░  ░░ ░   ░   ░ ░   ░ ░ ░   ░      ░   ▒    ░░░ ░ ░   ░      ░ ░ ░ ▒  ░      ░     ░   ▒     ░       ▒ ░░ ░ ░ ▒     ░   ░ ░
░ ░       ░  ░  ░   ░  ░      ░       ░          ░  ░   ░                  ░ ░         ░         ░  ░          ░      ░ ░           ░
░
                                                                                    Made with ❤️️ by """ + Fore.GREEN + "harrykp\n")

def log(message):
    logging.info(message+'..............')

def random_wait() -> None:
    min_time,max_time = config.get('wait_time',[10,20])
    tym = random.randint(min_time,
                         max_time)
    log(f"Waiting for {tym} seconds")
    for _ in trange(tym):
      sleep(1)

def random_long_wait(min_time = 5 ,max_time = 10):
    '''
      Sleep the executon of scripts for x minutes where x is random value b/w [min_time,max_time]
    '''
    min_time,max_time = config.get('wait_after_queue_is_empty',[5,10])
    tym = random.randint(min_time,max_time) * 60
    log(f"Waiting for {tym} seconds")
    for _ in trange(tym):
      sleep(1)

def clear_screen():
    system('clear')
