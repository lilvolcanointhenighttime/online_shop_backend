FROM python:3.11
ENV PATH="/root/.cache/pypoetry/virtualenvs/online-shop-XzbsNiWk-py3.11/bin/celery:${PATH}"

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV VIRTUAL_ENV=/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


WORKDIR /online_shop_backend
COPY . .


RUN pip install -r requirements.txt
CMD python ./secretkey.py

EXPOSE 8000

WORKDIR /online_shop_backend/src/store_management
CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python run_server.py