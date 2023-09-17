set -o errexit
pip install --upgrade pip
pip install -r internship/requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
