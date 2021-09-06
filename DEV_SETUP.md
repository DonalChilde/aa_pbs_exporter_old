# Initial Project Setup

From the project directory, run

```bash
./scripts/run.sh venv:init:all
./scripts/run.sh git:init
# To set a github remote origin...
# https://docs.github.com/en/github/using-git/adding-a-remote
git remote add origin https://github.com/DonalChilde/aa_pbs_exporter.git
```

## Downloading project from github

From the parent directory of the project -

```bash
git clone git@github.com:DonalChilde/aa_pbs_exporter.git
```

TODO project setup from github

## Tips and fixes

To run git commit without git precommit hooks -

```bash
git commit -m "Some comments" --no-verify
```
