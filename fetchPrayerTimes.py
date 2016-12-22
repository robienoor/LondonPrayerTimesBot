import json
import pandas as pd
import datetime

def getPrayerTimes(mosque, timeShift):


    #r = requests.get(url)

    #data = r.text

    #soup = BeautifulSoup(data, "lxml")

    with open('prayerTimes/euston.json') as data_file:
        eustonPrayerTimes = json.load(data_file)

    if mosque == "DSM":
        eustonPrayerTimes = pd.DataFrame(eustonPrayerTimes)

        return getDrummondStTimes(eustonPrayerTimes, timeShift)

    else:
        return "say what?"


def getDrummondStTimes(eustonPrayerTimes, timeShift):

    #today = time.strftime("%m/%d/%Y")

    searchDate = datetime.date.today() + datetime.timedelta(days=timeShift)
    searchDate = searchDate.strftime("%m/%d/%Y")

    searchTimes = (eustonPrayerTimes.loc[eustonPrayerTimes['Date'] == searchDate]).iloc[0]

    print(searchTimes)

    prayerTimeMessage = constructDailyTimeString(searchTimes)

    return prayerTimeMessage


def getELMTimes(soup):

    prayerTimesDiv = soup.find_all("div", class_="salah-block-content")

    print(prayerTimesDiv)

    return "east coast"

def constructDailyTimeString(timeRow):

    message = "Drummond Street - Prayer Times %s\n" \
             "------------------------------------------------\n" \
             "|   PRAYER   |   START  |    END  |\n" \
             "|   Fajr       \t\t\t\t|\t%s |\t%s\n" \
             "|   Sunrise \t\t\t|\t%s |\t%s      \n" \
             "|   Dhuhr    \t\t\t|\t%s |\t%s\n" \
             "|   Asr       \t\t\t\t|\t%s |\t%s\n" \
             "|   Maghrib\t\t\t|\t%s |\t%s\n" \
             "|   Isha      \t\t\t\t|\t%s |\t%s\n" \
             "------------------------------------------------\n" \
             % (timeRow.loc["Date"], timeRow.loc["FajrStart"], timeRow.loc["FajrPray"], timeRow.loc["Sunrise"], "  ",
                timeRow.loc["DhuhrStart"], timeRow.loc["DhuhrPray"], timeRow.loc["AsrStart"], timeRow.loc["AsrPray"],
                timeRow.loc["MaghribStart"], timeRow.loc["MaghribPray"], timeRow.loc["IshaStart"], timeRow.loc["IshaPray"])

    print(message)

    return message

