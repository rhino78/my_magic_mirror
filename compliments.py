import random
import datetime
import holidays

def compliment():
    currentTime = datetime.datetime.now()
    #evening = ['Wow, you look hot!','You look nice!','Hi, sexy!', 'bruh, looking good!','I like your shirt','your hair is fabulous','your eyebrows are on fleek','you have good shoe game','what are thoooooooooooooooose?!?!','Ready to go?']
    #afternoon=['Hello, beauty!','You look sexy!','Looking good today!','Nice Shirt','Need to change those pants','I like your hair','Maybe some different pants?','I like your ring','You look awesome','Thanks for the haircut','I love playing FIFA','I love playing PvZ Garden Warfare']
    #morning=['Good morning, handsome!','Enjoy your day!','How was your sleep?','Good morning kids!']
    evening = ['Good Morning', 'boa noite', 'ready for bed?', 'what\'s for dinner?', 'boa noite', 'Luisa is awesome', 'Hello, Handsome', 'You look awesome', 'you have good shoe game']
    afternoon = ['Good afternoon', 'boa tarde', 'Lets go to the pool', 'saude', 'Am I a cool mirror, or what?', 'its too hot to go on', 'No Touching!']
    morning = ['bacon and eggs', 'bom dia', 'Thomas, take a SHOWER!', 'Good morning, beauty', 'Good Morning, Kids!', 'what are thoooooooooooooooose?!?!']

    us = holidays.UnitedStates()
    us.append({"2016-08-29":"Birthday, Ryan!"})
    us.append({"2016-01-03":"Birthday, Carol!"})
    us.append({"2016-09-15":"Birthday, Bella!"})
    us.append({"2016-11-02":"Birthday, Luisa!"})
    us.append({"2016-03-09":"Birthday, Thomas!"})
    us.append({"2016-11-15":"Birthday, Vovo'"})
    us.append({"2016-11-22":"Birthday, Grammie"})
    us.append({"2016-11-29":"Birthday, Grampa"})
    us.append({"2016-11-28":"Birthday, Carlao"})
    us.append({"2016-08-16":"Birthday, Uncle Ryan"})
    us.append({"2017-06-24":"Birthday, Auntie Jenny"})
    us.append({"2017-07-11":"Birthday, Augie"})
    us.append({"2017-04-01":"Birthday, Tio Caio"})
    us.append({"2017-02-09":"Birthday, Tia Carol"})
    us.append({"2016-11-26":"Birthday, Marizilda"})
    us.append({"2017-05-10":"Birthday, Zeca"})

    if currentTime in us:
        return 'Happy ' + str(us.get(currentTime))

    if currentTime.hour <= 11:
        return str(morning[random.randint(0,len(morning)-1)]);
    elif 12 <= currentTime.hour < 17:
        return str(afternoon[random.randint(0,len(afternoon)-1)]);
    else:
        return str(evening[random.randint(0,len(evening)-1)]);
