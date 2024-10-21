mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

user:
	python3 manage.py createsuperuser

celery:
	celery -A root worker --loglevel=info

flush:
	python3 manage.py flush --no-input

loaddata:
	python3 manage.py loaddata country

