FROM ubuntu:22.04
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends python3.5 python3-pip gunicorn && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN apt-get update
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000 5003 5004
ENV FLASK_APP=run.py
#CMD [ "sudo", "rm", "/etc/nginx/sites-enabled/default"]
#COPY /nginx/flaskblog /etc/nginx/sites-enabled/flaskblog
#EXPOSE 80/tcp
#CMD [ "nginx" ]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port", "5000"]
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "run:app" ]
