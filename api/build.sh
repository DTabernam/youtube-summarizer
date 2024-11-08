pip install -r requierements.txt
python api/manage.py collectstatic --no-input
python api/manage.py migrate 