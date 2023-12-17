"""
This module contains the main script for the Chegg bot.
"""

import sys
import yaml
from analyze import Analyze
from chegg import Chegg
from utils import clear_screen, random_long_wait, random_wait, welcome_banner, log

clear_screen()
welcome_banner()

CONFIG = ''
try:
    with open("config.yaml", "r", encoding="utf-8") as yamlfile:
        CONFIG = yaml.load(yamlfile, Loader=yaml.FullLoader)
        log("Reading config.yaml file successfully")
except FileNotFoundError:
    log("config.yaml file not found. Contact the developer or re-install!!")
    sys.exit()

if not CONFIG.get('cookie'):
    log('Set the cookie in config.yaml file')
headers = {'cookie': CONFIG.get('cookie')}
keywords = CONFIG.get('keywords', [])
try:
    while True:
        bot = Chegg(headers=headers, keywords=keywords)
        bot.fetch_question()
        random_wait()
        if not bot.question:
            log("No questions left.")
            random_long_wait()
            continue
        analyze = Analyze(
            keywords=bot.keywords,
            question=bot.question,
            transcript=bot.transcript,
            parse_images=bot.parse_images
        )
        if analyze.is_ques_good():
            bot.answer_question()
            skip = input(
                "Press enter to continue or press any other key to stop the script."
            )
            if skip == "":
                bot.skip_question()
                random_wait()
            else:
                break
        else:
            bot.skip_question()
            random_wait()
except KeyboardInterrupt:
    log("Script stopped by user.")
except FileNotFoundError as e:
    log(f"File not found: {e}")
except yaml.YAMLError as e:
    log(f"Error while parsing YAML: {e}")
except ValueError as e:
    log(f"ValueError occurred: {e}")
