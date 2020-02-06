FROM python:3.8.1-alpine3.11

LABEL maintainer MaxymVlasov

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY configuration.py main.py ./

CMD [ "python3", "main.py" ]
