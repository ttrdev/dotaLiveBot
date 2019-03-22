import os
from flask import Flask, request
import telebot

TOKEN = "722609891:AAFwK2SXbq5Kj9UlTKxFp0_6FzKq8KQmN1U"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

url = 'http://esportlivescore.com/l_ru_g_dota.html'
headers = {'Accept': '*/*', 'Cookie': 'timezone=Asia/Samarkand','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

live_games = []
end_games = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет, ' + message.from_user.first_name)

def parse(url, headers):
    s = requests.Session()
    r = s.get(url, headers=headers)
    if r.status_code == 200:
        print("OK")
        soup = bs(r.content, 'html.parser')
        upcoming = soup.find(attrs={"id": "upcomingDiv"})
        end = soup.find(attrs={"id": "finishedDiv"})
        div_up = upcoming.find_all(attrs={"class": "match-event"})
        div_end = end.find_all(attrs={"class": "match-event"})
        for div in div_up:
            event_time = div.find(attrs={"class": "event_date_hour_minutes"}).text
            event_date = div.find(attrs={"class": "event_date_day_month"}).text
            event_info = div.find(attrs={"class": "event-tournament-info"}).text
            team_home = div.find(attrs={"class": "team-home"}).find('a').text
            team_away = div.find(attrs={"class": "team-away"}).find('a').text
            team_home_score = \
                div.find(attrs={"class": "event-main-scores"}).find(attrs={"class": "team-home"}).find("span").text
            team_score_away = \
                div.find(attrs={"class": "event-main-scores"}).find(attrs={"class": "team-away"}).find("span").text
            live_games.append({
                "title": "Ближайшие матчи",
                "event_time": event_time,
                "event_date": event_date,
                "event_info": event_info,
                "team_home": team_home,
                "team_away": team_away,
                "team_home_score": team_home_score,
                "team_score_away": team_score_away
            })
        for div in div_end:
            event_time = div.find(attrs={"class": "event_date_hour_minutes"}).text
            event_date = div.find(attrs={"class": "event_date_day_month"}).text
            event_info = div.find(attrs={"class": "event-tournament-info"}).text
            team_home = div.find(attrs={"class": "team-home"}).find('a').text
            team_away = div.find(attrs={"class": "team-away"}).find('a').text
            team_home_score = \
                div.find(attrs={"class": "event-main-scores"}).find(attrs={"class": "team-home"}).find("span").text
            team_score_away = \
                div.find(attrs={"class": "event-main-scores"}).find(attrs={"class": "team-away"}).find("span").text
            end_games.append({
                "event_time": event_time,
                "event_date": event_date,
                "event_info": event_info,
                "team_home": team_home,
                "team_away": team_away,
                "team_home_score": team_home_score,
                "team_score_away": team_score_away
            })
    else:
        print("Error")


@bot.message_handler(commands=['gstart'])
def live_g(message):
    for game in live_games:
        gg = \
            game['event_date'] + " " + \
            game['event_time'] + " " + \
            game['event_info'].strip() + " " + \
            game['team_home'] + " " + \
            game['team_home_score'] + "-" + \
            game['team_score_away'] + " " + \
            game['team_away']
        bot.send_message(message.chat.id, gg)


@bot.message_handler(commands=['gend'])
def end_g(message):
    for game in end_games:
        gg = \
            game['event_date'] + " " + \
            game['event_time'] + " " + \
            game['event_info'].strip() + " " + \
            game['team_home'] + " " + \
            game['team_home_score'] + "-" + \
            game['team_score_away'] + " " + \
            game['team_away']
        bot.send_message(message.chat.id, gg)


@bot.message_handler(content_types=['text'])
def txt(message):
    text = "??"
    bot.send_message(message.chat.id, text)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dota2ls.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    parse(url, headers)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))