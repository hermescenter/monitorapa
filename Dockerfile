FROM monitorapa-base

WORKDIR /usr/src/app/
RUN git clone https://github.com/hermescenter/monitorapa.git
WORKDIR /usr/src/app/monitorapa
RUN python3 -m venv .venv &&  . ./.venv/bin/activate && pip3 install -r ./cli/requirements.txt


CMD /bin/bash