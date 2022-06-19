FROM python:3.9

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./src ./src

HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1     
 
COPY .env .

CMD ["python", "./src/app.py"]
