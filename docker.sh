#/bin/bash
read -n1 -p "Did you want to refresh base image or run monitorapa Docker Image [y,n] ?" yn
case $yn in  
  y|Y) docker build -t monitorapa-base -f Dockerfile-base .;; 
  n|N) docker build -t monitor-base -f Dockerfile . ;; 
  *) echo type y or n ;; 
esac
docker-compose up