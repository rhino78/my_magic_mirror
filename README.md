## Magic mirror with mobile app

Built using Raspberry Pi, Python/Flask

```
sudo pip install flask
sudo pip install RPi.GPIO
sudo apt-get install upgrade
sudo apt-get install update
sudo apt-get install unclutter
```


#### On-boot stuff happens here
```sudo nano ~/.config/lxsession/LXDE-pi/autostart```

Add below other stuff:

```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xsscreensaver -no-splash
@xset s off
@xset -dpms
@xset s noblank
@unclutter -idle 1
@iwconfig wlan0 power off
@python3 my_magic_mirror/app.py
@sleep 50
@chromium-browser --incognito --disable-restore-session-state --noerrdialogs --kiosk http://0.0.0.0:8000/
```

#### Sources

[Source](http://michaelteeuw.nl/post/83188136918/magic-mirror-part-v-installing-the-raspberry-pi)