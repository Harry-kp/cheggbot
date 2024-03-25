
<div align="center">
  <h1>Cheggbot</h1>
  <img src="https://github.com/Harry-kp/cheggbot/assets/55315065/0d9746aa-f100-4eac-9ed7-b76bd46d01e6" width="500" alt="Cheggbot Logo">
  <p>Bored of skipping questions and "No more questions in queue" message and looking for an automation script? Congrats, you are in the right place.</p>
</div>

---

<p align="center">
    <a href="https://www.python.org/">
    	<img src="https://img.shields.io/badge/built%20with-Python3-red.svg" alt="Built with Python3">
    </a>
</p>

---

## Table of Contents

- [Subscribe to Our Channel](#subscribe-to-our-channel)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
- [FAQ](#faq)
- [Contributing](#contributing)
- [Future Plans](#future-plans)
- [Disclaimer](#disclaimer)

---

## Subscribe to Our Channel

If you find this script useful, please consider subscribing to our channel for more updates. We need your support to grow our channel.

[**Subscribe Here**](https://www.youtube.com/channel/UCYrIyQDF2t29T49KM0IYb1A?sub_confirmation=1)

[![Subscribe on YouTube](https://user-images.githubusercontent.com/55315065/221374382-106e9c23-6029-47cb-a365-eb22003b5f69.png)](https://www.youtube.com/watch?v=FtE64YC9XqA)

## Features

- Keyword-based skipping of questions.
- Randomization in time while skipping to prevent getting blocked.
- Sends alerts on Telegram when an answerable question is found.
- Sleeps for a longer period when the queue becomes empty.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- [Clone the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
- Install Python in your system. [Instructions](https://topictrick.com/install-python-on-any-platform/)
- Install pip. [Instructions](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)

### Setup

To set up the project:

1. Open the terminal and navigate to the `cheggbot` directory.
   
   ```bash
   cd path/to/cheggbot
   ```

2. (Optional) Create a virtual environment for this project. [Instructions](https://docs.python.org/3/tutorial/venv.html)

3. Install the project's dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Open the `config.yaml` file in a text editor and fill in the required details:

   - `keywords`: List of keywords to skip.
   - `cookie`: Your browser's cookie (See [How to get a cookie](#how-to-get-cookie)).
   - `wait_time`: Time in seconds to wait before skipping a question.
   - `wait_after_queue_is_empty`: Time in seconds to wait when the queue becomes empty.
   - `telegram`: If you want Telegram notifications (See [How to get chat_id and token](#how-to-get-chat_id-and-token)).

## Usage

To run the script:

1. Open the terminal and navigate to the `cheggbot` directory.

2. Run the script using Python 3.

   ```bash
   python3 script.py
   ```

3. If everything is set up correctly, the script will start running.
<div align="center">
  <img src="./images/Script%20Running.png" alt="Script Running">
</div>

## FAQ

### How to Get a Cookie?

1. Open the link [https://expert.chegg.com/expertqna](https://expert.chegg.com/expertqna).
2. Log in to your account.
3. Open the network tab and refresh the page.
   ![Network Tab](./images/Find%20Cookie.png)
4. Click on any `graphql` request.
5. Under `Request Headers`, you will find the cookie. Copy and paste it into `config.yaml`.

### How to Get `chat_id` and `token`?

Check this guide: [How to Make an API Call to the Telegram Channel](https://help.nethunt.com/en/articles/6253243-how-to-make-an-api-call-to-the-telegram-channel)

## Contributing

To contribute to this project:

1. Fork the repository.

2. Create a new branch.

3. Make your changes.

4. Create a pull request.

5. Wait for review and approval.

## Future Plans

- Better ways to identify good questions and bad questions.
- Support for auto-refreshing the cookie.
- Add support for different notification methods.

## Disclaimer

This is a research project. The developer is not responsible for any usage of this tool. Use it on your own behalf. The developer is also not responsible if your accounts get banned due to extensive use of this tool.

> If you encounter any issues or have questions, please open an issue on this repository.
