## Magic mirror with mobile app and English Premier League Live table
I really liked all the [magic mirrors](https://www.reddit.com/r/raspberry_pi/comments/3oktfu/magic_mirror_how_to/) I saw on reddit, so I decided to make my own. It has a moble app (which allows you to take selfies, and hide data you don't want pesky neighbors to know about), an English Premier League table that features arsenal previous match and next match data for Arsenal, the team I follow.


I hadn't worked with the [raspberry pi](https://www.raspberrypi.org/) before, but it was suprisingly really fun. I am constantly being asked by friends and neighbors, 'wow cool! what is that thing!'

edit --2/5/2018--
been having a lot of SD card issues and adding some of my setup scripts here to speed up the process in case I have to do this again 
:(

--python packages--
pip3 install flask_socketio
pip3 install icalendar
pip3 install holidays
pip3 install bs4
pip3 install redis

--setup stuff--
After we setup all the python stuff, we need to [clone](https://www.raspberrypi-spy.co.uk/2015/02/how-to-autorun-a-python-script-on-raspberry-pi-boot/) the my_magic_mirror repo to the root directory (this will create the necessary folders as well)

then we add "python3 /my_magic_mirror/app.py" [to the etc/profile dir](https://www.raspberrypi-spy.co.uk/2015/02/how-to-autorun-a-python-script-on-raspberry-pi-boot/)

lastly, we add the startup script to the boot sequence
