FROM debian:11

WORKDIR /usr/src/app

COPY ./cli/requirements.txt ./cli/requirements.txt

RUN apt update
RUN apt install -y python3-pip python3-venv
RUN apt-get install -y chromium-driver
RUN apt-get install -y python3-selenium

RUN python3 -m venv .venv

RUN . ./.venv/bin/activate && pip3 install -r ./cli/requirements.txt

COPY ./cli/point4.py ./cli/point4.py
COPY ./cli/point2.py ./cli/point2.py
COPY ./cli/point4.cfg ./cli/point4.cfg
COPY ./cli/commons.py ./cli/commons.py
COPY ./out/2022-02-13/* ./out/2022-02-13/
COPY ./check/* ./check/
#COPY ./cli/requirements.txt ./cli/requirements.txt
#COPY ./cli/point1.py ./cli/point1.py
#COPY ./cli/commons.py ./cli/commons.py
COPY ./LICENSE.txt ./LICENSE.txt
COPY ./README.md ./README.md

#RUN pip3 install webdriver-manager

#RUN mkdir -p out

# CMD ["python3", "cli/point1.py"]
# CMD ["python3", "cli/point3.py"]

CMD . ./.venv/bin/activate && exec python3 cli/point2.py 2022-02-13 check/google_analytics.js
#CMD ["python3", "cli/point2.py", "check/google_analytics.js"]
#CMD ["python3", "cli/point4.py", "check/google_analytics.js", "2", "4"]
