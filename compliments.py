import random
import datetime

def compliment():
    currentTime = datetime.datetime.now()
    evening = ['Wow, you look hot!','You look nice!','Hi, sexy!', 'bruh, looking good!','I like your shirt','your hair is fabulous','your eyebrows are on fleek','you have good shoe game','what are thoooooooooooooooose?!?!','Ready to go?']
    afternoon=['Hello, beauty!','You look sexy!','Looking good today!','Nice Shirt','Need to change those pants','I like your hair','Maybe some different pants?','I like your ring','You look awesome','Thanks for the haircut','I love playing FIFA','I love playing PvZ Garden Warfare']
    morning=['Good morning, handsome!','Enjoy your day!','How was your sleep?','Good morning kids!']

    if currentTime.hour < 12:
        return str(morning[random.randint(0,len(morning)-1)]);
    elif 12 <= currentTime.hour < 18:
        return str(afternoon[random.randint(0,len(afternoon)-1)]);
    else:
        return str(evening[random.randint(0,len(evening)-1)]);
