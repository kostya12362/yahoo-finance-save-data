# yahoo-finance-save-data
```linux
$ git clone https://github.com/kostya12362/yahoo-finance-save-data.git
$ cd yahoo-finance-save-data/web
```

make file `.env.dev`</br>

```script
DB_NAME=<specify db name and include in docker-compose.yml>
DB_USER=<specify db usernmae and include in docker-compose.yml>
DB_PASSWORD=<specify db password and include in docker-compose.yml>
DB_HOST=db
DB_PORT=5432
```

```linux
$ docker-compose -f docker-compose.yml up -d --build
```
