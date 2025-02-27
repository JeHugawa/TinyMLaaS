FROM python:3.10

WORKDIR /usr/src/app

EXPOSE 8000

COPY /backend /usr/src/app/

COPY ./requirements.txt /usr/src/app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]