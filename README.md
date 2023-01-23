# Pipeline for scraping twitter posts for a given keyword.
This pipeline scrapes latest posts for a given keywords. In this repository "təhsil" and "iqtisadiyyat" keywords are used.
For accessing twitter posts "snscrape" library of Python is used where there is no need to have personalized token
that is given for twitter developer account. This pipeline takes the current date and scrapes the posts that are 
posted on the current day regarding the given keyword. This process is repeated in every hour.

## Docker
#### Creating network for containers to communicate.
```docker
docker network create myNetwork
```
#### PostgreSQL database (This part can be skipped if the database container is already created in previous projects)

Downloading PostgreSQL image
```docker
docker pull postgres 
```
Running PostgreSQL container from the postgres image in "myNetwork" network with below credentials.
```docker
docker run --name postgres-cnt-0 -e POSTGRES_USER=nurlan -e POSTGRES_PASSWORD=1234  --network="myNetwork" -d postgres
```
Creating "neurotime" database inside the "postgres-cnt-0" container.
```docker
docker exec -it postgres-cnt-0 bash
# psql -U nurlan
# create database neurotime;
```

#### Application dockerization
Building an image of the application
```docker
docker image build -t twitter:1.0 . 
```
Running a container from the image in "myNetwork" network.
```docker
docker run  --name twitter_cnt --network="myNetwork" -d  twitter:1.0
```
