mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	python3 manage.py createsuperuser

app:
	python3 manage.py startapp apps


dish:
	python manage.py loaddata apps/dishes/fixtures/dishes.json
#python manage.py loaddata restaurants/fixtures/restaurants.json
#python manage.py loaddata restaurants/fixtures/categories.json
