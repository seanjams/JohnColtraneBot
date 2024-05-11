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

truncate_log:
	tail -c 1M ./johncoltranebot.log > /tmp/johncoltranebot.log && rm ./johncoltranebot.log && mv /tmp/johncoltranebot.log ./johncoltranebot.log
