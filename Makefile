install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
train:
	python train.py
run:
	FLASK_APP=app flask run
prod:
	gunicorn -w 2 -k gthread -t 120 -b 0.0.0.0:5000 wsgi:app
