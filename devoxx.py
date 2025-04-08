import json

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from pathlib import Path

jour=1
jour=2
jour=3

if jour==1:
    file="devoxx1.html"
    url0="https://www.devoxx.fr/agenda-2025/Schedule/"
elif jour==2:
    file="devoxx2.html"
    url0 = "https://www.devoxx.fr/agenda-2025/Schedule/?id=Thursday"
elif jour==3:
    file="devoxx3.html"
    url0 = "https://www.devoxx.fr/agenda-2025/Schedule/?id=Friday"

contenu=""

a_dict = {}

my_file = Path(file)
if my_file.is_file():
    contenu=Path(my_file).read_text(encoding='utf-8')
    #with open(file) as f:
        #contenu = f.read()
else:
    # URL de l'agenda Devoxx 2025
    url = url0

    # Récupération de la page
    response = requests.get(url)

    my_file.write_text(response.text, encoding='utf-8')
    # with open("devoxx1.txt", "w") as text_file:
    #     text_file.write(response.text)
    contenu=response.text

soup = BeautifulSoup(contenu, 'html.parser')

# Extraction des conférences
conferences = []

a_dict['liste'] = []
a_dict['jour'] = jour

# Les sessions sont dans des éléments avec la classe "schedule-day" (à vérifier)
days = soup.find_all("div", class_="cfp-event",limit=500)  # Peut varier selon la structure HTML

for day in days:

    articles=day.find_all('article')
    for article in articles:
        #article = day.find('article')

        event_name = article.find(class_='cfp-name').text.strip()
        event_start = article['data-event-start']
        event_finish = article['data-event-finish']
        event_duration = article['data-event-duration']

        lien=''
        tmp=article.find(class_='cfp-a')
        if tmp:
            #lien=article.find(class_='cfp-a').attrs()['href'].text.strip()
            lien = article.find(class_='cfp-a')['href']

        times = article.find_all('time')
        datetime_start = times[0]['datetime']
        datetime_end = times[1]['datetime']

        speaker=''
        tmp=article.find(class_='cfp-speaker')
        if tmp:
            speaker=tmp.text.strip()

        favori=-1
        tmp = article.find(class_='cfp-favourite')
        if tmp:
            favori = int(tmp.text.strip())

        # if event_start.find("T")>=0:
        #     event_start=event_start[event_start.find('T')+1:]
        # if event_start.rfind("+")>=0:
        #     event_start=event_start[:event_start.rfind('+')]

        print("Nom :", event_name)
        print("Début :", event_start)
        print("Fin :", event_finish)
        print("Durée :", event_duration)
        print("Datetime start :", datetime_start)
        print("Datetime end :", datetime_end)
        print("speaker :", speaker)
        print("favori :", favori)
        print("lien :", lien)

        dict2={}
        dict2['event_name'] = event_name
        dict2['event_start'] = event_start
        dict2['event_finish'] = event_finish
        dict2['event_duration'] = event_duration
        dict2['datetime_start'] = datetime_start
        dict2['datetime_end'] = datetime_end
        dict2['speaker'] = speaker
        dict2['favori'] = favori
        dict2['lien'] = lien
        a_dict['liste'].append(dict2)

        if len(article.find_all(class_='cfp-name'))>1:
            nom2=article.find_all(class_='cfp-name')[1].text.strip()
            print("Nom2 :", nom2)
            dict2['nom'] = nom2

    # date_str = day.find("h2").get_text().strip()  # Ex: "Mercredi 9 Avril 2025"
    # date_obj = datetime.strptime(date_str, "%A %d %B %Y").date()  # Formatage de la date
    #
    # # Extraction des sessions (dépend de la structure HTML exacte)
    # sessions = day.find_all("div", class_="schedule-session")  # À adapter
    #
    # for session in sessions:
    #     time = session.find("span", class_="time").get_text().strip()  # Ex: "10:00 - 11:00"
    #     start_time, end_time = time.split(" - ")
    #
    #     title = session.find("h3").get_text().strip()
    #     description = session.find("div", class_="description").get_text().strip()
    #     speakers = session.find("span", class_="speakers").get_text().strip() if session.find("span",
    #                                                                                           class_="speakers") else "N/A"
    #
    #     conferences.append({
    #         "Date": date_obj,
    #         "Titre": title,
    #         "Description": description,
    #         "Début": start_time,
    #         "Fin": end_time,
    #         "Durée (min)": (datetime.strptime(end_time, "%H:%M") - datetime.strptime(start_time,
    #                                                                                  "%H:%M")).seconds // 60,
    #         "Intervenants": speakers,
    #         "Track": session.find("span", class_="track").get_text().strip() if session.find("span",
    #                                                                                          class_="track") else "N/A"
    #     })

# Export en CSV
with open("devoxx_2025_conferences"+str(jour)+".csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Date", "Titre", "Description", "Début", "Fin", "Durée (min)", "Intervenants", "Track"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(conferences)

print("Export terminé : devoxx_2025_conferences.csv")

with open('data_'+str(jour)+'.json', 'w') as outfile:
    json.dump(a_dict, outfile,indent=4)
