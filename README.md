# support_bot
Бот, который связывает пользователя с агентом поддержки

support_bot for support by [vvsavva](https://t.me/vvsavva)

бот поддержки от [vvsavva](https://t.me/vvsavva)
# Settings Настройка 
Setting up the bot to work correctly

Настройка правильной работы бота

First of all, we need to install the necessary libraries

Прежде всего нам необходимо установить нужные библиотеки 

```

pip install -r requirements.txt

```
Must be executed in the project folder

Необходимо выполнять в папке с проектом

Next, fill in the information to launch the bot in config.py

Далее заполняем информацию для запуска бота в config.py

![image](https://github.com/vvsavva/support_bot/assets/63454532/ac95372c-1430-4473-b4d2-25f06a61a7e7)

Токен получаем у https://t.me/BotFather

We get the token from https://t.me/BotFather

Пишем приветственное сообщение для бота 

Writing a welcome message for the bot

Добавлям бота с правами администратора в группу модераторов и прописываем команду /id получаем id группы и вписываем его в GROUP_CHAT_ID

Add a bot with administrator rights to the moderators group and enter the /id command, get the group id and enter it in GROUP_CHAT_ID
