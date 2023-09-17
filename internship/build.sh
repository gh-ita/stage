set -o errexit
pip install --upgrade pip
pip install -r internship/requirements.txt

python internship/manage.py collectstatic --no-input
python internship/manage.py migrate
