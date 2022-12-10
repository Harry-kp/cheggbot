<p align="center">
  <img src="./images/icon.png" width="154" />
  <h1 align="center">Cheggbot</h1>
  <p align="center">Bored of skipping questions and "No more questions in queue" message and looking for a automation script. Congrats, you are at a right place.</p>
  <p align="center">
    <a href="https://www.python.org/">
    	<img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
    </a>
  </p>
</p>

## Highlight
https://user-images.githubusercontent.com/55315065/205429850-a86df710-2a6d-4058-a813-cc38f06e10b9.mov


## Features
- [x] Keyword based skipping of questions
- [x] Randomisation in time while skipping (Protect you from getting blocked)
- [x] Sends alert on telegram when answerable question found
- [x] Sleeps for a longer period of time when queue becomes empty


## Working
### Prerequisite
- Clone the repository. Check [this](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
 - Install python in your system.Check [this](https://topictrick.com/install-python-on-any-platform/)
 - Install pip. Check [this](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)

### Setup
- Open terminal and go to cheggbot directory. You find this directory wherever you clone this in the first place.
- Type ```ls``` in the terminal and if output looks something like this , than you are in the right place.
![Home Directory](./images/Home%20Directory.png)
- Optional - You can create a virtual environment for this project. Check [this](https://docs.python.org/3/tutorial/venv.html) and [this](https://www.geeksforgeeks.org/python-virtual-environment/).
- Run ```pip install -r requirements.txt``` in the terminal. This will install all the dependencies required for this project.
- Open ```config.yaml``` file in any text editor and fill the details.
  - ```keywords``` : List of keywords you want to skip. You can add as many as you want.
  - ```cookie``` : This is the most important part. You need to get this from your browser.
  - ```wait_time``` : This is the time in seconds you want to wait before skipping a question. This is to prevent you from getting blocked.
  - ```wait_after_queue_is_empty``` : This is the time in seconds you want to wait when queue becomes empty.
  - telegram - If you want to get alert on telegram when answerable question found.
    - ```token``` : This is the token of your telegram bot.
    - ```chat_id``` : This is the chat id of your telegram bot.

### Run
- Open terminal and go to cheggbot directory.
- Run ```python script.py``` in the terminal. In some system python2 is default. In that case run ```python3 script.py```.
- If everything goes well , you will see something like this.
!["Script Running"](./images/Script%20Running.png)
- If you had setted up the telegram notification, you would get a message like this when you get a suitable question
!["Telegram Notification"](./images/Telegram%20Notification.png)

## FAQ
- How to get cookie?
  - Open the link https://expert.chegg.com/expertqna
  - Log in to your account
  - Open the network tab and refresh the page
  - !["Network Tab](./images/Find%20Cookie.png)
  - Now click on any ```graphql``` request.
  - Under ```Request Headers``` section , you will find the cookie.
  - Copy and paste that in the config.yaml file

- How to get chat_id and token?
  - Check [this](https://help.nethunt.com/en/articles/6253243-how-to-make-an-api-call-to-the-telegram-channel)


## Contributing
- Fork the repository.
- Create a new branch.
- Make changes.
- Create a pull request.
- Wait for review.
- If everything goes well , your changes will be merged.

## Future Plans
- [ ] Better ways to identify good questions and bad questions.
- [ ] Support for auto refershing of cookie as cookie get expired in roughly 25 days.
- [ ] Add support for different notification medium.

---

> **Disclaimer**<a name="disclaimer" />: Please Note that this is a research project. I am by no means responsible for any usage of this tool. Use on your own behalf. I'm also not responsible if your accounts get banned due to extensive use of this tool.

