FROM python:3.10

WORKDIR /usr/src/app

EXPOSE 8501

COPY /frontend /usr/src/app

COPY ./requirements.txt /usr/src/app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD  ["streamlit", "run", "main_page.py"]

 
