FROM python:slim-bullseye

RUN apt-get update && apt-get install -y tini ca-certificates openssl && rm -rf /var/lib/apt/lists/*

# copy & install install required dependencies
# COPY requirements.txt requirements.txt
COPY . .
RUN pip3 install -r requirements.txt

COPY gclone /usr/local/bin/gclone

RUN chmod +x /usr/local/bin/gclone && chmod +x UnixCloneCord.py

# RUN chmod 0755 /usr/local/bin/gclone
# RUN chmod +x CloneCord.py # imagine setting permission for a completely different executable
CMD ["python3", "UnixCloneCord.py"]
