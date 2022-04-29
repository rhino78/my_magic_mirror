"""a class to return the compliment text of the main page"""
import random
from datetime import datetime
import holidays
import api_interface


def compliment():
    """returns a random compliment to display"""
    complimentlist = api_interface.getquotes()
    usholidays = getholidays()

    if datetime.now() in usholidays:
        return "Happy " + str(usholidays.get(datetime.now()))

    return str(complimentlist[random.randint(0, len(complimentlist) - 1)])


def getholidays():
    """if today is a holiday, display that all day"""
    usholidays = holidays.UnitedStates()
    usholidays.append(
        {
            str(datetime.now().year)
            + "-08-29": "Birthday, Ryan! You are the best dad ever!!"
        }
    )

    usholidays.append({str(datetime.now().year) +
                      "-01-03": "Birthday, Carol!"})
    usholidays.append({str(datetime.now().year) +
                      "-02-09": "Birthday, Tia Carol"})
    usholidays.append({str(datetime.now().year) +
                      "-03-09": "Birthday, Thomas!"})
    usholidays.append({str(datetime.now().year) +
                      "-04-01": "Birthday, Tio Caio"})
    usholidays.append({str(datetime.now().year) +
                      "-05-10": "Birthday, Zeca!!"})
    usholidays.append({str(datetime.now().year) +
                      "-06-23": "Birthday, Frederico!"})
    usholidays.append({str(datetime.now().year) +
                      "-06-24": "Birthday, Auntie Jenny"})
    usholidays.append({str(datetime.now().year) +
                      "-07-11": "Birthday, Augie!"})
    usholidays.append({str(datetime.now().year) +
                      "-08-16": "Birthday, Uncle Ryan"})
    usholidays.append({str(datetime.now().year) +
                      "-09-15": "Birthday, Bella!"})
    usholidays.append({str(datetime.now().year) +
                      "-11-02": "Birthday, Luisa!"})
    usholidays.append({str(datetime.now().year) +
                      "-11-15": "Birthday, Vovo'!"})
    usholidays.append({str(datetime.now().year) +
                      "-11-22": "Birthday, Grammie"})
    usholidays.append({str(datetime.now().year) +
                      "-11-26": "Birthday, Marizilda"})
    usholidays.append({str(datetime.now().year) +
                      "-11-28": "Birthday, Carlao"})
    usholidays.append({str(datetime.now().year) +
                      "-11-29": "Birthday, Grampa"})

    return usholidays
