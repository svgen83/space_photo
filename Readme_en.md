# Space photo

This program is designed to download photos from the websites of SpaceX (flight images) and NASA (images of space objects) and then send them to the Telegram channel.

### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
#### Program settings

In order for the program to work correctly, create an .env file in the program folder containing a token for accessing NASA photos and a token for accessing a telegram bot.
Write them down as follows:
```
NASA_TOKEN="token"

TELEGRAM_TOKEN="token"
```
A token from NASA should be obtained from [website](https://api.nasa.gov/).

You receive a telegram token when registering a chat bot. It says here [how to register a chatbot](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram/).

#### How to run
The program runs from the command line. To run the program using the cd command, you first need to go to the program folder.
To download pictures in the command line, write:

```
python main.py
```
Pictures will be saved in directories located in the folder with program files.

In order to distribute pictures in telegrams, write in the command line:
```
python send_to_telegram.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
