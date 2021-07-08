# INSTALLING:
## Either run script with sudo or add user to i2c user-group:
- sudo groupadd i2c
- sudo chown :i2c /dev/i2c-1
- sudo chmod g+rw /dev/i2c-1
- sudo usermod -aG i2c <user>
- sudo reboot

Now, you should be able to execute without sudo:
python servo_controller.py

