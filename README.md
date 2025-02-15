# John Coltrane
John Coltrane

For RaspberryPi, adjust as needed for mac setup.
```bash
sudo nano /lib/systemd/system/johncoltranebot.service
```

Copy the following contents and save.
```
[Unit]
Description=John Coltrane Bot
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c "PATH=$PATH:/home/pi/.local/bin exec /home/pi/Documents/code/JohnColtraneBot/run.sh"
Restart=on-failure
RestartSec=60
WorkingDirectory=/home/pi
User=pi
Environment=REDDIT_CLIENT_ID=<Your Reddit Oauth Client ID>
Environment=REDDIT_CLIENT_SECRET=<Your Reddit Oauth Client Secret>
Environment=REDDIT_USER_AGENT=<console:JOHNCOLTRANE:1.0>
Environment=REDDIT_USERNAME=<Reddit Bot User's Username>
Environment=REDDIT_PASSWORD=<Reddit Bot User's Password>
Environment=LOGGING_VERBOSE=False

[Install]
WantedBy=network.target
```

Then reload the daemon and enable the service. This will call `./run.sh` on system boot:
```bash
sudo systemctl daemon-reload
sudo systemctl enable johncoltranebot.service
```

Trigger the job manually with:
```bash
sudo systemctl start johncoltranebot.service
sudo systemctl status johncoltranebot.service
sudo systemctl stop johncoltranebot.service
```
