FROM alpine:3.15.0
RUN apk add build-base
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
WORKDIR /app
COPY . /app/
EXPOSE 5000
RUN pip3 --no-cache-dir install -r requeriments.txt
RUN python -m nltk.downloader punkt
CMD ["python3","src/app.py"]
