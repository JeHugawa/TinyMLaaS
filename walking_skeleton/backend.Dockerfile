FROM python:3.10

WORKDIR /usr/src/app

COPY /backend /usr/src/app/

COPY ./requirements.txt /usr/src/app/

EXPOSE 8000

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app"]


 
