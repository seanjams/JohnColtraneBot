shell:
	pipenv run flask shell

clean:
	rm -rf instance && rm -f johncoltranebot.log

status:
	sudo systemctl status johncoltranebot.service

start:
	sudo systemctl start johncoltranebot.service

stop:
	sudo systemctl stop johncoltranebot.service
