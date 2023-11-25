FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["main.py"]