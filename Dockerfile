FROM python:3.8
RUN apt-get update -y

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["/bin/bash", "start.sh"]