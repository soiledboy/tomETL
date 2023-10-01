###############################################################################
# configs
#
ENV ?= development

.PHONY: test

default: test


###############################################################################
# python environment
#
install:
	pip install -r requirements.txt


###############################################################################
# tests
#
test:
	@pytest -s .


###############################################################################
# db migrations
#
db.upgrade:
	ENV=${ENV} FLASK_APP=backend.app flask db upgrade

db.downgrade:
	ENV=${ENV} FLASK_APP=backend.app flask db downgrade

db.migrate:
	ENV=${ENV} FLASK_APP=backend.app flask db migrate


###############################################################################
# web processes
#
run.be:
	ENV=${ENV} python server.py
	
run.fe:
	yarn run start


###############################################################################
# jobs
#
run.job.api:
	ENV=${ENV} python run_tcg_api.py

run.job.html:
	ENV=${ENV} python run_tcg_html.py
