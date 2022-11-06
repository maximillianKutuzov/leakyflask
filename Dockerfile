FROM ubuntu:jammy-20211029

LABEL name="Flask Leaky API CTF"
LABEL version="1.0"
LABEL tag="leakyflask"

WORKDIR /app
ADD app.db /app
ADD app.py /app
ADD static /app/static
ADD requirements.txt /app

# Install requirements
RUN apt update && apt install python3.10 python3-pip -y
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python3.10"]
CMD ["/app/app.py"]
EXPOSE 8085