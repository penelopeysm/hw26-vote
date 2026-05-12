# Hack Week STV Vote

A simple web app for running an STV (Single Transferable Vote) election. Voters drag and rank candidates, protected by a shared password. Votes are stored in SQLite.

## Local development

```bash
make setup
VOTE_PASSWORD=secret make run
```

Open http://localhost:5468.

## Deploy to Fly.io

```bash
fly launch --copy-config --yes
fly volumes create votes_data --region lhr --size 1
fly secrets set VOTE_PASSWORD="secret"
make deploy
```

## Export votes

```bash
make export        # from the deployed Fly.io app (BLT format)
make export-local  # from the local votes.db
```

## Reset the remote database

```bash
make reset-db
```
