#! /usr/bin/env bash

# newest versions of docker includes compose, if compose
# is included in docker, we don't need to check for docker-compose
doesDockerIncludeCompose=0

check () {
  # check if docker is installed
  if ! docker > /dev/null 2>&1 ; then
    echo -e "\x1b[1m[\x1b[31mError\x1b[39m]\x1b[0m docker not found, aborting"
    exit 127
  fi

  # check if compose already is in docker executable
  if docker compose > /dev/null 2>&1 ; then
    doesDockerIncludeCompose=1
  fi

  # if compose is in the docker executable, we don't need to check for docker-compose
  # otherwise check that docker-compose is installed
  if [[ doesDockerIncludeCompose -eq 0 ]] && ! docker-compose > /dev/null 2>&1 ; then
    echo -e "\x1b[1m[\x1b[31mError\x1b[39m]\x1b[0m docker-compose not found, aborting"
    exit 127
  fi

  if ! pidof dockerd > /dev/null; then
    echo -e "\x1b[1m[\x1b[31mError\x1b[39m]\x1b[0m docker demon is not running, aborting"
    exit 127
  fi
}

printmenu() {
  echo -e "\x1b[1m1\x1b[0m) Create \x1b[1mmonitorapa-base\x1b[0m image from \x1b[1mDockerfile-base\x1b[0m"
  echo -e "\x1b[1m2\x1b[0m) Create \x1b[1mmonitor-base\x1b[0m    image from \x1b[1mDockerfile\x1b[0m"
  echo -e "\x1b[1m0\x1b[0m) Quit"
}

mainloop () {
  while [[ 0 ]]; do
    read -n1 -p ": "
    echo
    case $REPLY in  
      1)
        docker build -t monitorapa-base -f Dockerfile-base . 
        break
      ;; 

      2)
        docker build -t monitor-base -f Dockerfile . 
        break
      ;;

      0) exit 0 ;;
    esac
  done
}

main () {
  echo
  check
  printmenu
  mainloop

  # implements a ternary operator
  [[ doesDockerIncludeCompose -eq 1 ]] && \
    docker compose up -d --build && docker attach monitorapa \
  || \
    docker-compose up -d --build && docker attach monitorapa
  exit 0
}

main