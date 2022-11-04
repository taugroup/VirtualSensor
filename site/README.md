# Dashboard
## Create docker image
```
docker build -t dash .
```
## Spin up a container
```
docker run -p 8989:8000 -d dash
```
## Visit the website
```
http://localhost:8989
user: jtao
passwd: t
```
