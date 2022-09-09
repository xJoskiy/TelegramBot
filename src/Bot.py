import threading
import time
import datetime
import bs4
import telebot
import requests
import re


def getSchedule(groupsUrl):
    init_date = '2022-08-15'
    schedule = []
    for groupUrl in groupsUrl:
        for week in range(6):
            x = datetime.datetime.strptime(init_date, '%Y-%m-%d')
            y = datetime.timedelta(days=week * 7)
            groupWeekUrl = groupUrl + '/' + str((x + y).date())
            schedule.append(requests.get(groupWeekUrl))

    for i in range(len(schedule)):
        soup = bs4.BeautifulSoup(schedule[i].text, 'lxml')
        schedule[i] = soup.find("div", {"class": "panel-group"})

    return schedule


def info(bot, chatId):
    while True:
        bot.send_message(chatId, datetime.datetime.now())
        time.sleep(600)


def main():
    bot = telebot.TeleBot('5494880001:AAE4l1TYRosCH9OowEU1RatxOwnyLcnJ9FM')

    @bot.message_handler()
    def start(message):
        threading.Thread(target=info, args=(bot, message.chat.id)).start()
        response = requests.get('https://timetable.spbu.ru/MATH/StudyProgram/13858')
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        data = soup.find_all("div", {"class": "tile"})
        groups = ["https://timetable.spbu.ru" + re.findall(r'/\w+/\w+/\w+/\d+', str(string))[0] for string in data]
        schedule = getSchedule(groups)
        while True:
            if schedule != getSchedule(groups):
                bot.send_message(message.chat.id, "Новое расписание!")

    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()