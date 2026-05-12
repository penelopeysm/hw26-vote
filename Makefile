APP = hack-week-vote

.PHONY: setup run deploy export export-local reset-db

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	VOTE_PASSWORD=$${VOTE_PASSWORD:-changeme} .venv/bin/python app.py

deploy:
	fly deploy

export:
	fly ssh sftp get /data/votes.db /tmp/votes-export.db --app $(APP)
	python3 export_votes.py /tmp/votes-export.db
	@rm -f /tmp/votes-export.db

export-local:
	python3 export_votes.py

reset-db:
	fly ssh console --app $(APP) -C "rm /data/votes.db"
	fly machine restart --select --app $(APP)
