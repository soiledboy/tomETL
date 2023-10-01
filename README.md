# Tier1Marketspace

## Development Environment

### Python
The python part of the dev environment requires,
- python, 3.7.x
- pip
- packages listed in the `requirments.txt` file

To install the python packages run this,

```
pip install -r requimrents.txt
# 
```

### Javascript
The Javscript part of the environment requires,
- Node.js, 12.x?
- Yarn
- packages listed in the `yarn.lock` file

To install the javascript packages,

```
yarn install
```

### Database / Postgres

1. Create a postgres database named, `tier1marketspace_development`. eg, `createdb tier1marketspace_development`
2. Download a backup from heroku and then run this, `pg_restore --verbose --clean --no-acl --no-owner -h localhost -d tier1marketspace_development heroku-backup.dump`
3. Confirm that the Postgresql connection credentials in `.env.development` match those of your current Postgresql instance.
4. To test everything, run `make db.migrate` and `make db.upgrade`. These should run without error.

### Jobs
To run the TCG Price and Listings jobs, all you need to do is,

```sh
ENV={{environment_name}} python run_tcg_api.py
ENV={{environment_name}} python run_tcg_html.py
```

### Deployment steps on PythonAnywhere.com

1. ssh into vm
2. activate pythonn virtualenv. `workon tier1marketspace`
3. install any new python modules. `make install`
4. apply DB migrations. `ENV=production make db.upgrade`


### Data Arch

1. Category = name of card game. This will always be `YuGiOh`.
2. Groups = CardSets (change th schema to reflect this). Not possible to search for a group by extended group data.
3. Products =  Cards
# tier1marketspace
