# Products MVP

## Instalation

```
git clone https://github.com/jedelacarrera/...
```

Create a Postgres Database.

Create a new file called .env and copy all the information from .env.template.

Replace with your own database, user and password.

```
pip3 install -r requirements.txt
```

```
python3 seed.py
```

## Run

Open a terminal and run all the commands in .env (copy-paste in your terminal).

```
python3 -m flask run --host=0.0.0.0
```

## Run tests

Open a terminal and run all the commands in .env (copy-paste in your terminal).

```
pytest --cov=. tests/ -vv
```