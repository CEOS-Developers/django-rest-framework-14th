# Docker와 Github Actions을 이용한 자동 배포

## Docker의 원리

**어떤 OS에서도 같은 환경을 만들어주는 원리**이다. 따라서 서버에 docker만 깔고 배포를 해도 된다.   
-> 서버에 접속해서 docker 실행, master에 푸시 된 커밋을 복사하는 역할을 Github Actions이 해준다   
-> 이 과정을 CD(Continuous Delivery)

## Docker와 docker-compose

docker는 위에서 말한 가상 컨테이너 기술이다. 애플리케이션을 신속하게 구축, 
테스트 및 배포할 수 있는 소프트웨어 플랫폼으로 Docker는 소프트웨어를 컨테이너라는 표준화된 유닛으로 패키징하며, 
이 컨테이너에는 라이브러리, 시스템 도구, 코드, 런타임 등 소프트웨어를 실행하는 데 필요한 모든 것이 포함되어 있다.

쉽게 말해서 docker는 Dockerfile을 실행시켜주고 docker-compose는 docker-compose.yml 파일을 실행시켜준다고 생각하면 된다.
### Dockerfile
```dockerfile
FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base


# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /app/
```
* Dockerfile은 하나의 이미지를 만들기 위한 과정으로 이 이미지를 사용하여 다른 컴퓨터에 동일한 환경 제공 가능
    * 이미지는: 내가 구축한 환경을 스냅샷
### docker-compose.yml
```yaml
version: '3'
services:

  db:
    container_name: db
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_ROOT_HOST: '%'
      MYSQL_ROOT_PASSWORD: mysql
    expose:
      - 3306
    ports:
      - "3307:3306"
    env_file:
      - .env
    volumes:
      - dbdata:/var/lib/mysql

  web:
    container_name: web
    build: .
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    environment:
      MYSQL_ROOT_PASSWORD: mysql
      DATABASE_NAME: mysql
      DATABASE_USER: 'root'
      DATABASE_PASSWORD: mysql
      DATABASE_PORT: 3306
      DATABASE_HOST: db
      DJANGO_SETTINGS_MODULE: django_docker.settings.dev
    restart: always
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      - db
volumes:
  app:
  dbdata:
```

* 이미지를 여러개 띄워서 서로 네트워크도 만들어주고 컨테이너의 밖의 호스트와도 어떻게 연결할지, 파일 시스템은 어떻게 공유할지(volumes) 제어해주는것이 docker-compose이다.
    * 위 파일에서는 db와 web 두개의 컨테이너를 정의하여 서로 소통할 수 있다.
## 컨테이너의 이점

## 서버 작동 원리

docker-compose.prod.yaml 파일은 서버에서 Github Actions가 실행시켜주는 파일이다.  

Github Actions가 실행시켜주는 파일의 맨 아래에 가면 이런게 있다.
```bash
sh /home/ubuntu/srv/ubuntu/config/scripts/deploy.sh
```

이때 config/scripts/deploy.sh는 Actions가 내 프로젝트에서 복사해갔다.
### config/scripts/deploy.sh
```python
#!/bin/bash

# Installing docker engine if not exists
if ! type docker > /dev/null #docker를 깔아주는 코드, EC2 인스턴스에는 아무것도 없기 때문에 직접 깔아줘야 한다.
then
  echo "docker does not exist"
  echo "Start installing docker"
  sudo apt-get update
  sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
  sudo apt update
  apt-cache policy docker-ce
  sudo apt install -y docker-ce
fi

# Installing docker-compose if not exists
if ! type docker-compose > /dev/null #docker-compose를 깔아주는 코드
then
  echo "docker-compose does not exist"
  echo "Start installing docker-compose"
  sudo curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

echo "start docker-compose up: ubuntu"
sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d
```


> `sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d`  
> 맨 마지막에 있는 코드가 결국 서버를 실행하는 코드이다. 이 스크립트 파일은 Github Actions가 수행했고, 이 스크립트 파일은 EC2 서버에서 실행되고 있구요, 결국은 이 command에 의해 서버가 build되고 실행 된다.
> * up : docker-compose.prod.yml에 정의된 컨테이너들을 모두 띄우라는 명령
> * --build : up할때마다 새로 build를 수행하도록 강제하는 파라미터
> * -d : daemon 실행

## docker-compose.prod.yml 
```yaml
version: '3'
services:

  web:
    container_name: web#!/bin/sh

python manage.py collectstatic --no-input

exec "$@"
    build:
      context: ./
      dockerfile: Dockerfile.prod
    command: gunicorn django_docker.wsgi:application --bind 0.0.0.0:8000
    environment:
      DJANGO_SETTINGS_MODULE: django_docker.settings.prod
    env_file:
      - .env
    volumes:
      - static:/home/app/web/static
      - media:/home/app/web/media
    expose:
      - 8000
    entrypoint:
      - sh
      - config/docker/entrypoint.prod.sh

  nginx:
    container_name: nginx
    build: ./config/nginx
    volumes:
      - static:/home/app/web/static
      - media:/home/app/web/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  static:
  media:
```
* docker-compose.yml와 다르게 db 컨테이너가 없고 nginx 컨테이너가 있다.
  

### db 컨테이너가 없는 이유

>* 데이터가 날아가고 유출 위험이 있다.
>* 서버는 여러 인스턴스를 띄우고 지울 수있는데 서버에 db를 띄운다면 다른 서버가 db에 붙지도 못하고, 인스턴스를 날리면 데이터도 날리게 된다.
> * 인스턴스의 자원을 같이 쓰기 때문에 효율적이지도 않다.
> * 서버가 해킹을 당하면 개인정보가 유출된다.


## nginx 컨테이너

### nginx란?

client -> Web Server(Nginx) -> WSGI(gunicorn) -> Application Server(django)

* nginx는 Application Server인 django에 접근하고 요청과 응답을 전달 할 수 있게 해준다.
* nginx는 동시 접속에 특화된 웹서버 프로그램으로 아래와 같은 두가지 역할을 수행한다.

![http](https://user-images.githubusercontent.com/79985974/135406938-0703d4e8-a4b1-4710-99ae-439bebb974b0.PNG)
1. HTML, CSS, Javascript, 이미지와 같은 정보를 웹 브라우저에 전송하는 역할을 수행한다.
   
![nginx](https://user-images.githubusercontent.com/79985974/135406735-e56dcae8-d338-4e62-8d82-a6ebaa1accee.PNG)
2. 응용프로그램 서버에 요청을 보내는 리버스 프록시로서의 역할을 수행한다.
    * 클라이언트는 가짜 서버에 요청(request)하면, 프록시 서버(nginx)가 reverse server(응용프로그램 서버)로부터 데이터를 가져오는 역할
  
* 웹 서버(nginx)가 따로 필요한 이유는 application을 여러대(process혹은 thread) 띄우고 웹 서버가 이를 적절하게 로드밸런싱 하기 위한 용도,보안상 위험한 요청을 차단하기 위한 용도 때문

### nginx Dockerfile
```docker
FROM nginx:1.19.0-alpine 
```
nginx:1.19.0-alpine라는 이미지는 이미 누군가가 만들어놨고, nginx 구동에 필요한 환경이 이 이미지 안에 다 들어가있다.
```
RUN rm /etc/nginx/conf.d/default.conf # default config 파일을 삭제
COPY nginx.conf /etc/nginx/conf.d #nginx.conf라는 파일을 옮겨준다
```
