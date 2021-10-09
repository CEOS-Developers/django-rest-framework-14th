## 원리 = docker + Github Actions의 콜라보

## docker
* 어떤 OS에서도 같은 환경을 만들어주는 것입니다
* 그래서 서버에 Docker만 깔고 배포를 해도 됩니다

## container
컨테이너(container): 기본적으로 호스트(host) 컴퓨터에서 돌아가고 있는 하나의 프로세스입니다.  
하지만, 일반 프로세스와는 다르게 container는 host 컴퓨터와 그 위에서 돌아가는 다른 프로세스들로부터  
**격리**되도록 설계되어 있습니다.

## virtual environment vs. container
|VM|Container|
|------|---|
|자체적인 운영체제를 포함하고 있어서|VM처럼 격리된 환경에서도|
|하드웨어 리소스를 많이 잡아 먹어서|일반 프로세스처럼 빠르고 가볍게 돌아감|
|느리고 무거움||


## Image
이미지(image) = container image
: 애플리케이션 코드 뿐만 아니라 애플리케이션 실행에 필요한 최소한의 환경(언어 런타임, 라이브러리 패키지 등)을
  포함하고 있는 바이너리(binary) 파일입니다.   
  * 하나의 image로 부터 동일한 container를 계속해서 만들어낼 수 있으며,
      동시에 여러 개의 container를 띄울 수도 있어서 확장성(scalability)이 좋습니다.   
  * 즉, 어떤 컴퓨터에서든지 Docker만 깔려 있다면 이 image를 내려받아 container로 구동하면
      동일하게 작동하는 애플리케이션을 얻을 수 있습니다.
      
      
## Container vs. Image
Image는 container의 스냅샷을 떠놓은 것으로 생각하면 됩니다.
반대로 container는 컴퓨터에서 살아서 돌아가고 있는 image의 한 인스턴스(instance)라고 생각할 수 있습니다.

image를 실행시키면(run) 이미지가 container가 되고, 컨테이너가 실행되면서   
컨테이너 안에 포함되어 있는 실행되도록 조치되어있는 프로그램이 실행되게 됩니다.   

|program|image|
|------|---|
|process|container|


## 컨테이너 기술이란
![컨테이너 기술](https://postfiles.pstatic.net/MjAyMTA5MzBfMTcz/MDAxNjMyOTkzMjU1NTk5.57VkOyE72Kk9o0REtVeOVEzQlMnYlWelJ-u57ewgqGAg.awuRnNn68gJWoZBMZzG44RnwOeIfYVCgTipjBJ0D9WYg.PNG.sssssjin99/image.png?type=w966)   

<용어>   
호스트(host): 운영체제가 설치된 컴퓨터

컨테이너(container): 호스트에서 실행되는 격리된 각각의 실행환경   
* 각각의 컨테이너에는 운영체제 전체가 설치되어 있는 것이 아니고   
   앱을 실행하는 데 필요한 라이브러리와 실행 파일들만 포함되어 있습니다.   
   각각의 앱은 이렇게 컨테이너라는 격리된 공간에서 실행됩니다.

* 이미 존재하는 운영체제를 공유하니까 무엇인가를 설치할 필요도 없고,   
운영체제가 하나니까 속도도 느려지지 않고, 저장장치의 용량을 줄일수도 있습니다.   
컨테이너 기술을 이용해서 이런 일을 쉽게 해주는 소프트웨어들 중 가장 많이 이용하는 제품이   
"도커" 입니다.


### 지난주에 실습해 본 도커를 구조화한 그림입니다.
![도커 구조화](https://postfiles.pstatic.net/MjAyMTA5MzBfMjYz/MDAxNjMyOTk2NjgwNzA2.rrxmFQv3RxdaTke7TO9t-hewgMNW4q_uBF7L8GE_ElQg.gAzC525-ZrqJf8FDUbuo9m5nvI2pjt5ZljZmQFtK97wg.PNG.sssssjin99/image.png?type=w966)   



## 도커 네트워크 -- 포트 포워딩이란(Portforwarding)
포트(port)에 대해 우리는 도커를 공부하기 이전까지 웹 서버의 포트번호에 대해서만 알고 있었을 것입니다.   
저도 이전까지는 컴퓨터에 몇만개의 포트가 있고,   
이것이 컴퓨터에 설치되어 있는 여러 소프트웨어들을 네트워크적으로 구분해준다는 것,   
그리고 일반적으로 웹 서버는 80번 포트를 이용한다 이정도만 알고 있었는데,   

도커에서는 호스트와 컨테이너가 각각의 포트를 이용한다는 것을 알게 되었습니다.   
그래서 도커의 네트워크에 관해 찾아보게 되었습니다.   

![도커 네트워크](https://postfiles.pstatic.net/MjAyMTA5MzBfMjkx/MDAxNjMyOTk0OTU0Mjg0.NR8klPQn2moZrb4wIGgdM5IM-bUSx5z2NWr8inXxuKQg.4ylF6z6DU8coOt-gCEVJ4ubrHhgLLJwrH-DUF1U2O4wg.PNG.sssssjin99/image.png?type=w966)   

* 도커 호스트(docker host) = 컨테이너가 설치된 운영 체제    
하나의 도커 호스트에는 여러 개의 컨테이너가 만들어질 수 있습니다

*  컨테이너와 호스트 모두 독립적인 실행환경이기 때문에   
  각자 독립적인 포트와 파일 시스템을 가지고 있습니다.

위 그림과 같은 예시에서, 웹 브라우저로 웹 서버에 접속하려면   
호스트의 80번 포트와 컨테이너의 80번 포트를 연결해주어야 합니다.      
명령어: ```$ docker run -p 80:80 httpd``` (httpd apache 서버를 이용하였다고 가정)   
-> 이 명령어를 통해서 호스트의 80번으로 들어온 신호가 컨테이너의 80번 포트로 전송됩니다.   
== 이렇게 연결된 포트로 신호를 전송하는 것 **"포트 포워딩(port forwarding)"** 이라고 합니다.  



## Github Actions가 해주는것   
①서버에 접속해서 docker를 실행시킨다.   
②그리고 방금 master에 푸시된 커밋을 복사한다.   
####--> 이 전 과정: CD(Continuous Delivery)   


## Docker와 docker-compose
용어 정리)   
- 컨테이너: 도커가 띄운 가상 시스템 (-->django project가 뜨고 있는 시스템)   
- 호스트: 도커를 실행시키고 있는 주체 (-->본인의 서버 혹은 로컬 컴퓨터)   

#### "docker --(실행시킴)--> Dockerfile"


## Dockerfile
컨테이너화된 소프트웨어 프로젝트에서는 모든 개발 작업이 Docker 컨테이너 안에서 이루어집니다.   
따라서 개발자의 로컬 컴퓨터에서 파이썬을 설치하거나 프로젝트에 필요한    
패키지를 설치할 필요가 없습니다.   

대신 Docker 컨테이너 안에서 해당 어플리케이션이 돌아갈 수 있는 환경을 이미지(image)를   
떠 놓아야 합니다. 이렇게 이미지를 떠 놓으면 개발자들은 번거로운 사전 세팅을 생략하고   
바로 해당 이미지를 컨테이너 안에서 실행할 수 있습니다.   


#### 여기서 Dockerfile이란?   
: 하나의 이미지(내가 구축한 환경을 스냅샷 찍어둔 것)를 만들기 위한 과정으로   
(==> Docker 이미지가 빌드(build)될 때 거쳐야하는 단계를 정의하고 있음)   
이 '이미지'만 있으면 다른 컴퓨터에서도 똑같은 환경을 올릴 수 있다.   

*  프로젝트 최상위 디렉터리에 Dockerfile을 생성한다.   
* Docker는 이 Dockerfile에 나열된 명령문을 차례로 수행하며 이미지를 생성한다.   
* 하나의 Docker 이미지는 base 이미지부터 시작해서 기존 이미지위에 새로운 이미지를   
 중첩해서 여러 단계의 이미지 층(layer)을 쌓아가며 만들어진다.   



```buildoutcfg
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

* FROM 명령문   

    FROM <이미지>   
    FROM <이미지>:<태그>   

   ```FROM python:3.8.3-alpine #Python 3.8``` (alpine 리눅스 기반)을 base 이미지로 사용



* WORKDIR 명령문
    WORKDIR <이동할 경로>   

   WORKDIR 명령문은 쉘(shell)의 cd 명령문처럼 컨테이너 상에서 작업 디렉토리로 전환을 위해서   
사용됩니다. WORKDIR 명령문으로 작업 디렉터리를 전환하면 그 이후에 등장하는 모든   
RUN, ENTRYPOINT, COPY, ADD 명령문은 해당 디렉터리를 기준으로 실행됩니다.   
    
    ```WORKDIR /app ```  # /app 으로 디렉터리 전환
    
    
* COPY 명령문

   COPY <src>... <dest>
   COPY ["<src>",... "<dest>"]

   COPY 명령문은 호스트 컴퓨터에 있는 디렉터리나 파일을 Docker 이미지의 파일 시스템으로   
   복사하기 위해서 사용됩니다.

   ```COPY requirements.txt /app/requirements.txt```   
   ```COPY . /app/``` # 이미지를 빌드한 디렉터리의 모든 파일을 컨테이너의 app/ 디렉터리로 복사   
   
   
 
 
#### Dockerfile 명령어 정리


|<명령어>|<용도>|
|-------|-----|
|FROM|base 이미지 설정|   
|WORKDIR|	 작업 디렉터리 설정|
|RUN|	이미지 빌드 시 커맨드 실행|   
|ENTRYPOINT|이미지 실행 시 항상 실행되야 하는 커맨드 설정 |  
|CMD|	이미지 실행 시 디폴트 커맨드 또는 파라미터 설정|
|EXPOSE|	컨테이너가 리스닝할 포트 및 프로토콜 설정| 
|COPY/ADD|	이미지의 파일 시스템으로 파일 또는 디렉터리 복사|   
|ENV|	환경 변수 설정|
|ARG|	빌드 시 넘어올 수 있는 인자 설정|


이렇게 작성한 Dockerfile를 이용해서 이미지 빌드하기

```$ docker build .```

마지막에 Successfully built <이미지ID>가 출력되었다면 제대로 이미지가 빌드가 된 것입니다.   




##docker-compose

docker-compose --(실행시킴)--> docker-compose.yml   

* docker-compose: 여러 개의 도커 이미지들을 한번에 실행할 수 있고,    
  관리할 수 있게 도와주는 틀   
  즉, 여러 개의 컨테이너(container)로 이루어진 애플리케이션을 하나의 YAML 파일에 정의해놓고   
  한 번에 올리거나 내릴 수 있습니다.  
  (여러 개의 컨테이너로 구성된 애플리케이션을 관리하기 위한 도구)   

docker-compose.yml은 프로젝트 최상위 디렉터리에 생성하고,   
우리가 작성한 코드에서는,   
web 서비스로 Django 애플리케이션을 / db 서비스로 mysql 데이터베이스를 정의해주었습니다.

docker-compose.yml 파일 구조   
```
version: "3.5"   
services:   
  web:   
     웹 애플리케이션 설정   
  db:   
    데이터베이스 설정   
  networks:   
   네트워크 설정   
  volumes:   
   볼륨 설정   
```   


```buildoutcfg
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
      DJANGO_SETTINGS_MODULE: django-rest-framework-14th.settings.dev
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

```command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"```   
- Django 애플리케이션을 구동하기 위해서 python manage.py runserver 0:8000 커맨드 실행

``` ports: "8000:8000" ```
- 호스트의 8000 포트와 컨테이너의 8000 포트를 바인드(bind)시키기   
   --> 포트 포워딩(port forwarding)

```volumes: - .:/app```
 - 현재 디렉터리를 컨테이너의 /app 디렉터리로 마운트(mount)하고 있음   

```depends_on: - db```
- web 서비스가 돌아가기 전에 db 서비스가 반드시 먼저 돌아갈 수 있도록 depends-on 설정이
되어 있음   


## 여러 환경을 대상으로 지정 
일반적인 사용 사례는 프로덕션, 준비, CI 또는 개발과 같은 여러 환경을 대상으로   
지정할 수 있도록 여러 compose 파일을 정의하는 경우입니다. 이러한 차이를   
지원하기 위해 다음 그림에 나와 있는 것처럼 Compose 구성을 여러 파일로 분할할 수 있습니다.   

![이미지 이름](https://docs.microsoft.com/ko-kr/dotnet/architecture/microservices/multi-container-microservice-net-applications/media/multi-container-applications-docker-compose/multiple-docker-compose-files-override-base.png)
(설명: 기본 docker-compose.yml 파일에서 값을 재정의하는 다중 docker-compose 파일)

## docker-compose.prod.yaml
-> 로컬이 아닌 서버에서 실행되는 파일
-> 배포를 위한 파일 (prod -> 배포를 위한 것)



## docker-compose.prod.yaml
- 로컬이 아닌 서버에서 실행되는 파일   
- 배포를 위한 파일 (prod -> 배포를 위한 것)



```buildoutcfg
version: '3'
services:

  web:
    container_name: web
    build:
      context: ./
      dockerfile: Dockerfile.prod
    command: gunicorn django-rest-framework-14th.wsgi:application --bind 0.0.0.0:8000
    environment:
      DJANGO_SETTINGS_MODULE: django-rest-framework-14th.settings.prod
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


|docker-compose.yml|docker-compose.prod.yml|
|---|---|
|db 컨테이너가 O | db 컨테이너가 X |
|nginx 컨테이너 X| nginx 컨테이너 O|


## docker-compose.prod.yml
- db 컨테이너가 없음 (데이터가 날아갈까 위험하고, 데이터를 털릴까봐 위험함)   
- 서버에 db를 띄운다면 다른 서버가 db에 붙지도 못하고, 인스턴스를 날리면 데이터도 날아가는거고,   
    인스턴스의 자원(메모리, cpu 등)을 서버와 db가 같이 쓰니까 효율적이지도 않기 때문이다.   
- (slack 설명 참고) prod.yml 파일은 배포를 위한 파일이나 마찬가지이다.   
   배포 시에는 디비를 rds로 따로 빼서 사용합니다.   
   ec2 인스턴스 안에 도커 안에 db 컨테이너를 받아주게 되면 인스턴스의 자원을 서버와 디비가 같이 사용하게 되어서   
   비효율적이고, 보안상으로도 위험하다고 한다.   
   따라서, prod.yml 에는 db 컨테이너를 빼는 것이다! (배포할때?를 위해서)     
   
   

## nginx 컨테이너의 구성

### Nginx와 웹서버

application과 server 구분하기!   
application-django <----------> server-nginx

* 백엔드 개발자가 코드를 짜는 일-> 비즈니스를 구현하는 것 -> django가 이를 대신함 = application   
* nginx : 이 application(=여기서는 django)에 접근하고 요청과 응답을 전달할 수 있게 해줌   

   nginx <-> gunicorn or uwsgi <-> wsgi <-> django

## nginx의 Dockerfile 살펴보기
.config/nginx/ 경로에 dockerfile이 있는 것을 확인할 수 있다.   


```buildoutcfg
FROM nginx:1.19.0-alpine
# nginx의 1.19.0-alpine 버전 이미지를 사용합니다.
# 이 이미지는 이미 누군가가 만들어놨고, nginx 구동에 필요한 환경이 이 이미지 안에 다 들어가있어요.

RUN rm /etc/nginx/conf.d/default.conf
# default config 파일을 삭제합니다. 아래에서 우리가 원하는 설정파일로 바꿔줄 생각이에요.

COPY nginx.conf /etc/nginx/conf.d
# nginx.conf라는 파일을 옮겨줍니다.
```


여기서의 nginx.conf 파일을 확인해 보면 다음과 같습니다.   
nginx.conf도 위의 nginx Dockerfile과 같은 경로에 놓여 있습니다.   


```buildoutcfg
upstream django_docker {   # django_docker라는 upstream 서버를 정의합니다.
  server web:8000;     # web의 8000포트에 연결합니다. web은 docker container에요.
}

server {   # nginx server를 정의합니다.

  listen 80;  # 80포트를 열어줍니다 (http)

  location / {   # "/" 도메인에 도달하면 아래 proxy를 수행합니다.
    proxy_pass http://django_docker;   # django_docker라는 upstream으로 요청을 전달
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # header 설정
    proxy_set_header Host $host;  
    proxy_redirect off;
  }

  location /static/ {  # "/static/" 도메인에 도달하면 아래 alias를 수행합니다.
    alias /home/app/web/static/;   # 아래 디렉토리 (서버의 파일시스템)을 맵핑합니다.
  }

  location /media/ {
    alias /home/app/web/media/;
  }
}
```


## upstream 서버
  일반적인 프록시 구조에서, 요청을 받는 쪽을 upstream,   
  응답을 받는 쪽을 downstream이라고 한다.   
  
  
  
## 서버가 뜨는 방법
Github Actions 가 -------(실행)------->> "docker-compose.prod.yaml"   

.github/workflows/deploy.yml 을 확인해보면(Github Actions가 실행시켜주는 파일)   
```sh /home/ubuntu/srv/ubuntu/config/scripts/deploy.sh``` 를 확인할 수 있습니다.   

config/scripts/deploy.sh 를 확인하면 다음과 같습니다.   


```
#!/bin/bash

# Installing docker engine if not exists
if ! type docker > /dev/null
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
if ! type docker-compose > /dev/null
then
  echo "docker-compose does not exist"
  echo "Start installing docker-compose"
  sudo curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

echo "start docker-compose up: ubuntu"
sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d
```


## 여기서 확인해야 할 주요 코드  

```if ! type docker > /dev/null, if ! type docker-compose > /dev/null```   
*  이는 docker와 docker-compose를 깔아주는 코드이다.
    EC2 인스턴스에는 아무것도 없기 때문에 직접 깔아줘야 한다.

```sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d```   
* 결국 실행해야 할 코드   
* 결국 이 스크립트 파일은 Github Actions가 수행했고, 이 스크립트 파일은 EC2 서버에서 실행된다.
* 결국 이 command에 의해 서버가 build되고 실행된다.

* (의미): up이 docker-compose 파일(여기선 f 파라미터가 가리키는)에 정의된 모든 컨테이너를 띄우라는
         명령어이다.   
--build: up할때마다 새로 build를 수행하도록 강제하는 파라미터이다.     
          이것이 없으면 코드 변경사항이 제대로 반영이 안될 수 있다.      
-d: daemon 실행. 로컬에서도 이 파라미터를 붙이면 background에서 docker-compose가 돌고,   
    터미널 창에서도 계속 뜨고 있다.   
    
    
    
--> 그러면 up을 한다고 서버가 뜰까?   
docker-compose가 django를 알고 서버를 띄워주는 것이 아니다.   
docker-compose는 django를 모른다.   
그래서 우리는 up이 되었을때 django를 실행시키기 위해 command와 entrypoint를 정의합니다.   

docker-compose.prod.yml을 보면 다음과 같은 코드를 확인할 수 있습니다.   
```
web:
	command: gunicorn django_docker.wsgi:application --bind 0.0.0.0:8000

web:
	entrypoint:
	  - sh
	  - config/docker/entrypoint.prod.sh
```


## Github Actions -  깃헙 액션이 무엇을 수행하는지 살펴보기

```
name: Deploy to EC2
on: [push]
jobs:

  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
    - name: checkout
      uses: actions/checkout@master

    - name: create env file
      run: |
        touch .env
        echo "${{ secrets.ENV_VARS }}" >> .env

    - name: create remote directory
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: mkdir -p /home/ubuntu/srv/ubuntu

    - name: copy source via ssh key
      uses: burnett01/rsync-deployments@4.1
      with:
        switches: -avzr --delete
        remote_path: /home/ubuntu/srv/ubuntu/
        remote_host: ${{ secrets.HOST }}
        remote_user: ubuntu
        remote_key: ${{ secrets.KEY }}

    - name: executing remote ssh commands using password
      uses: appleboy/ssh-action@master
      env:
        DEPLOY_USERNAME: hanqyu
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: |
          sh /home/ubuntu/srv/ubuntu/config/scripts/deploy.sh
```


1. on: [push]
    push 될 때 마다 이 workflow를 수행합니다.   
    
2. - name: create env file   
    깃헙 설정에 복사한 ENV_VARS의 값을 모두 .env file로 만듭니다.   
    
3. - name: create remote directory   
    ec2 서버에 디렉토리를 하나 만들어줍니다.   
    
4. - name: copy source via ssh key   
    ssh key를 이용해 현재 푸시된 소스를 서버에 복사합니다.   
    
5. - name: executing remote ssh commands using password   
    서버에 접속하여 deploy.sh 를 실행시킵니다.   
    
    
## 총정리
1. Github Actions가 우리의 코드를 서버에 올리고 deploy.sh를 실행한다.   
2. deploy.sh는 docker-compose를 실행한다.   
3. docker-compose는 web이라는 컨테이너와 nginx라는 컨테이너를 빌드하고 실행한다.   
4. web 컨테이너는 Dockerfile.prod를 기준으로 빌드되며, 이 도커 이미지는 django를 구동하기 위한
   환경이 모두 갖춰져있다.   
   
   
   
   
   

>  제가 추가로 궁금했었던 점이 있어 Slack에 올려 질문한 내용이 있는데, 여기에도 공유하겠습니다   
>> Q:   
github actions를 이용하지 않고 그냥 바로 docker-compose명령어를 터미널에서 치고   
컨테이너를 빌드해서 서버를 실행해도 되지 않나요?   
로컬에서 수정한 변경사항을 따로 입력하지 않아도 github actions를 수행함으로써 바로바로 push가 되니까      
그 편리함 때문에 github actions로 docker-compose를 수행하는 건가요?   
즉 github actions를 같이 쓰는 명확한 이유가 궁금합니다!   
찾아보니까 docker를 이용할 때 github actions를 꼭 같이 쓰지 않는 경우도 있어서요   

>>A:   
바로 docker-compose.prod를 올리는 명령어로 서버 배포를 진행할 수도 있지만,   
푸쉬도 하고 도커컴포즈도 입력하는 그 작업을 반복하다보면 생각보다 일이 될 수가 있어요.   
그래서 푸쉬를 하면 자동으로 배포가 될 수 있게 자동화를 목표로 github actions, travis, jenkins 등을 이용합니다!   
참고로 깃헙액션에서는 푸쉬할때 말고도 다른 원하는 행위나 다른 브랜치 대해 workflow를 다양하게 정의해서 사용할 수도 있어요   
예를들어 .github/workflows 및에 dev.yml prod.yml 나눠서 개발과 운영을 분리한 후   
서로 다른 작업을 수행하게끔 정의할 수 있는 걸로 알고 있습니다!   
(개인적으로 로컬에서의 테스트 말고 개발용 서버와 디비를 따로 또 판 경우에 이렇게 하면 좋을 것 같네용)   
또 깃헙 액션만의 장점이 있다면 코드가 배포에 문제가 없는지 확인하고,   
에러가 난다면 어디서 나는지 빌드 로그를 볼 수 있는 등   
배포관련된 작업들을 외부의 다른 툴 없이 저희가 기존에 사용하던 github이라는 코드 관리 공간에서   
같이 할 수 있다는 점이 이점이 되겠네요   
