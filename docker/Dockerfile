FROM monitorapa-base

ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

VOLUME ["/usr/src/app/monitorapa"]
WORKDIR /usr/src/app/monitorapa
CMD python3 -m venv .venv &&  . ./.venv/bin/activate && pip3 install -r ./cli/requirements.txt && /bin/bash && source ./.venv/bin/activate


#CMD /bin/bash