set -e
export PYTHONPATH="/opt/render/project/src"
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
