# DOCKER의 개념


## DOCKER

![docker-container](./img/docker-container.png)

`Docker`를 한줄로 요약하자면 **리눅스 컨테이너를 기반으로하는 오픈소스 가상화 플랫폼** 이다.  


## CONTAINER

> 컨테이너는 시스템의 나머지 부분과 격리된 프로세스 세트입니다.  
> 이러한 프로세스를 실행하는 데 필요한 모든 파일은 고유한 이미지에서 제공되므로, Linux 컨테이너는 개발 단계에서 테스트, 프로덕션에 이르기까지 이식성과 일관성을 유지할 수 있습니다.

컨테이너는 동일한 운영 체제 커널을 공유하고 시스템의 나머지 부분으로부터 애플리케이션 프로세스를 격리한다.  

가상화와는 비슷하면서도 다르다. 아래의 그림을 보자.

![vm-docker](./img/vm-docker2.png)

가상화는 `HYPERVISOR`를 이용하여 하드웨어를 에뮬레이션 한 뒤, 그 위에 각각의 GUEST OS를 올려서 애플리케이션을 실행하는 방법을 취하고 있다.

반면에 `컨테이너`는 `Docker Engine` 위에서 애플리케이션의 실행에 필요한 바이너리 파일들만 올라가게 된다.  

`컨테이너`는 가상화와는 달리 원래의 HOST OS위에서 동작하므로, HOST의 커널들을 공유한다. 커널을 공유하게 되면, IO처리가 쉽게되기 때문에 성능이 더 잘 나올 수 있다.  

즉 `컨테이너`는 HOST OS가 사용하는 자원을 분리하여 여러 환경을 만들 수 있도록 하는것 이다.



## IMAGE

도커의 이미지는 컨테이너 실행에 필요한 파일과 설정값을 포함하고 있는 것으로, Immutable하게 존재한다.  
컨테이너는 이미지를 실행한 상태라고 정의할 수 있다.  

이미지는 컨테이너를 실행하기 위한 모든 정보를 가지고 있기 때문에 더 이상 의존성 파일을 컴파일하고 이것저것 설치할 필요가 없다.  

새로운 서버가 추가되면 미리 만들어 놓은 이미지를 다운받고 컨테이너를 생성만 하면 된다.

개인적으로 도커의 가장 큰 장점이라고 생각한다.  

같은 프로그램을 실행하더라도 필요한 의존성 파일의 버전이 하나만 달라도 오류가 나기 태반인데, 이 문제를 이미지를 이용해서 간단하게 해결하였다.  

<br>
<br>


# 2주차 내용 분해하기


## 대략적 흐름

1. repository에 push
2. git action이 [deploy.yml](#deployyml) 설정대로 서버에서 동작
3. [deploy.sh](#deploysh) 실행
4. [docker-compose.prod.yml](#docker-composeprodyml) 설정대로 컨테이너 생성

<br>

## deploy.yml

git action에 `.github/workflows/deploy.yml` 이 저장된다.  

`deploy.yml`에 따르면 

```yaml
run: |
        touch .env
        echo "${{ secrets.ENV_VARS }}" >> .env
```

.env 라는 파일을 만들고, .env 파일에 ${{ secrets.ENV_VARS }} 을 추가한다.  

`ENV_VARS` 에 env.prod 내용들을 적어주었다. 

이 부분에서 DB를 붙인다. 처음에 로컬부분과 서버부분이 다른데, 인스턴스에 DB가 없어서 의아했었다.  

보안과 편의상의 이유로 인스턴스에 DB는 올리지 않고 rds를 사용한다.

```yaml
 name: create remote directory
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: mkdir -p /home/ubuntu/srv/ubuntu
```

그 뒤, ssh를 이용하여 /home/ubuntu/srv/ubuntu 라는 디렉토리를 만든다.  
ec2 서버에 ssh를 이용하여 접속할 수 있도록, secrets.KEY에 ssh key를 넣어놓았다.  

```yaml
name: copy source via ssh key
      uses: burnett01/rsync-deployments@4.1
      with:
        switches: -avzr --delete
        remote_path: /home/ubuntu/srv/ubuntu/
        remote_host: ${{ secrets.HOST }}
        remote_user: ubuntu
        remote_key: ${{ secrets.KEY }}
```

이 부분이 가장 이해가 안갔다. 먼저 [burnett01/rysnc-deployments](https://github.com/Burnett01/rsync-deployments) 를 찾아보았다.  

`Github Action`이 GITHUB_WORKSPACE에 있는 파일들을 `rsync`를 통해 배포할 수 있도록 해준다고 한다.

`rsync`란 간단하게 말하자면 원격에 있는 파일과 디렉토리를 복사하고 동기화 하기 위해서 사용하는 툴이다.  
remote-update protocol을 이용하여 차이가 있는 파일만 복사하고, 데이터를 압축하여 송/수신하기 때문에 더 적은 bandwidth를 사용한다는 장점이 있다.

따라서, `rsync`를 사용하여 ec2서버의 /home/ubuntu/srv/ubuntu/ 디렉토리에 있는 소스와 GITHUB_WORKSPACE에 있는 소스 중 차이가 있는 파일들만 ec2 서버의 /home/ubuntu/srv/ubuntu/에 올려준다는 것이다.

![docker-mkdir](img/docker-mkdir.png)
실제로 ec2 서버에 접속하여 해당경로로 들어가보면 github 소스코드가 그대로 올라가있는걸 볼 수 있다.

<br>

switches에 보면 -avzr --delete라는 옵션이 달려있다. 각각 옵션들의 뜻은 다음과 같다.  

a : archive 모드로 타임스탬프, 심볼릭링크, 퍼미션, 그룹, 소유자, 장치 등의 파일 보존  
v : 상세 정보 출력  
r : 하위 디렉토리까지 복사  
z : 데이터를 압축해서 전송. 단 destination에서는 압축이 해제되어 들어감  
--delete : 원본 소스에 없는 파일은 백업 서버에서 삭제

만약 --delete 옵션이 없다면, 파일을 삭제하고 push 하였을 때, repository와 서버의 싱크가 맞지않을 것이다.

```yaml
- name: executing remote ssh commands using password
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: |
          sh /home/ubuntu/srv/ubuntu/config/scripts/deploy.sh
```

마지막으로 ssh를 이용하여 ec2 서버 내에서 `deploy.sh`를 실행한다.

여기까지의 과정이 repository에 push를 할 때 생기는 일이다. 이러한 일련의 과정들을 거치므로 push할 때마다 서버에 push한 코드가 반영된다는 것을 알 수있다.

## deploy.sh

`deploy.yml`에서 서버내의 `deploy.sh`를 실행하고 끝났다.

```shell
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
```

docker가 없다면, docker를 설치해준다.

```shell
if ! type docker-compose > /dev/null
then
  echo "docker-compose does not exist"
  echo "Start installing docker-compose"
  sudo curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi
```

docker-compose가 없다면 docker-compose를 설치해준다.

```shell
echo "start docker-compose up: ubuntu"
sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d
```

`docker-compose.prod.yml`에 저장되어있는 모든 서비스를 실행한다.  
--build 옵션이 달려있기 때문에, 서비스 실행 전에 이미지들을 새로 만든다.

<br>

## docker-compose.prod.yml

`docker-compose`는 docker 컨테이너들의 설정과 관계들을 담은 파일이다.   
`docker-compose.prod.yml`엔 web이란 컨테이너와 nginx 컨테이너가 존재한다.

```yaml
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
```

web 이라는 컨테이너의 설정이다.  
컨테이너 생성에 필요한 이미지로 [Dockerfile.prod](#dockerfileprod)를 사용하였다.  

entrypoint를 보면 sh config/docker/entrypoint.prod.sh 명령어를 이용해 `entrypoint.prod.sh` 를 실행하라고 나와있다.

`entrypoint.prod.sh` 스크립트는 다음과 같다.

```shell
# entrypoint.prod.sh
#!/bin/sh

python manage.py collectstatic --no-input

exec "$@"
```

[`collectstatic`](#static-파일-처리)을 실행하라는 쉘스크립트이다.

```shell
> gunicorn django-rest-framework-14th.wsgi:application --bind 0.0.0.0:8000
```

`command`에 적힌 명렁어가 실행된다. wsgi인 `gunicorn`이 실행된다.

실제로 이 컨테이너에서 실행되는 command를 서버에 접속하여 찾아보면 다음과 같다.

![docker-ps](img/docker-full-comamnd.png)

```shell
> sh config/docker/entrypoint.prod.sh gunicorn django-rest-framework-14th.wsgi:application --bind 0.0.0.0:8000
```

<br>
<br>

다음으로 nginx 컨테이너의 설정이다.

```yaml
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

컨테이너 생성에 필요한 이미지로 config/nginx/Dockerfile 을 사용할 것이다.

nginx 컨테이너는 static과 media라는 volume 컨테이너를 생성했다.  

static volume의 경우 nginx 컨테이너 내의 /home/app/web/static 이라는 디렉토리가 서버 내부의 ~/var/lib/docker/volumes/static/_data 디렉토리에 마운트 된다.  

media volume의 경우도 마찬가지로 nginx 컨테이너 내의 /home/app/web/static 이라는 디렉토리가 서버 내부의 ~/var/lib/docker/volumes/media/_data 디렉토리에 마운트 된다.

![volume-directory](./img/volume-directory.png)

실제로 디렉토리가 있는지 ec2 서버에 접속하여 찾아보았다. volume 컨테이너들이 실제 서버의 ubuntu_media, ubuntu_static 으로 존재한다.

여기까지 서버가 올라가는 과정들을 샅샅히 파헤쳐 보았다!

<br>
<br>

# etc

## Dockerfile

```dockerfile
# 가져올 이미지 
FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

# 디렉토리 생성 및 설정
RUN mkdir /app
WORKDIR /app

# 필요한 프로그램 설치 (MariaDB, mysql)
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base

# 프로젝트에 필요한 라이브러리 설치
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# 모든 파일 복사
COPY . /app/
```

`Dockerfile`의 경우 컨테이너 내부의 리눅스 shell에서 실행될 명령어들을 담은 것이다.  

먼저 python:3.8.3-alpine 이란 이미지를 가져온다.

app이란 디렉토리를 만들고, WORKDIR을 /app으로 지정하였다.

apk add --no-cache mariadb-connector-c-dev,  
apk update &&   
apk add python3 python3-dev mariadb-dev build-base &&   
pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base 라는 명령어를 실행하여, 필요한 패키지들을 설치하고, 설치 한 뒤 필요없는 패키지들을 삭제하였다.

이후, COPY requirements.txt /app/requirements.txt  
RUN pip install -r requirements.txt 를 이용하여 requirements.txt를 복사한 뒤, 프로젝트에 필요한 파이썬 라이브러리들을 설치하였다.

COPY . /app/ 을 이용하여 Dockerfile이 있는 경로의 모든 파일들을 전부 도커 컨테이너 내의 /app/ 에 복사하였다.  

이렇게 `Dockerfile`은 실제 실행되는 명령어들을 담당한다. 리눅스에 익숙하다면 직관적으로 볼 수 있을 것이다.

## Dockerfile.prod
```dockerfile
# BUILDER #
###########

# pull official base image
FROM python:3.8.3-alpine as builder

# set work directory
WORKDIR /usr/src/app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.3-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install mysqlclient
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./config/docker/entrypoint.prod.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
```

`Dockerfile.prod`는 스테이지가 2개인 multi-stage dockerfile이다.  
multi-stage를 사용하는 이유는 스테이지를 나누어 빌드파일과 실행파일을 분리할 수 있기 때문에, docker 이미지를 더욱 가볍게 할 수 있기 때문이다.

위에 builder 부분은 Dockerfile과 비슷한 부분이 많다.   
먼저 python:3.8.3-alpine 이미지를 가져온 뒤 디렉토리들을 생성해주는데 /home/app과 /home/app/web을 환경변수로 각각 설정하였다.  

$APP_HOME/static, $APP_HOME/media 는 nginx 컨테이너에서 volume container를 마운트 할 실제 디렉토리들이다.  

의존적인 모듈들을 설치한다.
이 때
```dockerfile
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
```
이런식으로 builder 스테이지에 빌드를 하여 만들어진 whl파일들이 final 스테이지의 /wheels에 모두 복사될 것 이다.

```dockerfile
RUN pip install mysqlclient
RUN pip install --no-cache /wheels/*
```

![pip-wheel](img/pip-wheel-results.png)
`mysqlclient`와 /wheels/에 존재하는 모든 패키지들을 설치한다.  
여기서 의문점이 생겼다.  
~~1. 왜 mysqlclient를 설치하는데 필요했던 의존적 패키지들을 지우지 않을까?~~  
2. 왜 컨테이너 내의 /wheels 폴더를 삭제하지 않을까? 

코드를 내가 만든것이 아니므로 아직 답을 찾진 못했다.

그 뒤 `entrypoint.prod.sh` (collectstatic 실행 shell) 를 $APP_HOME 에 복사한다.

유저 설정을 하고 이미지 설정이 끝난다!

## docker-compose.yml

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

`docker-compose.yml`은 yaml파일 형식으로 도커 컨테이너들의 관계와 설정들을 담은 파일이다.

web과 db라는 `컨테이너` 들이 `docker-compose.yml`에 설정된 것을 볼 수 있다. 

web 컨테이너는 실행되면 migration하고, 서버를 실행시킨다. db에 연결하기 위해 유저 이름과 비밀번호, 포트등이 설정되어 있는 것을 볼 수 있다.

db 컨테이너는 이미지로 존재한다. 이 파일은 로컬에서의 실행만을 관장하기 때문에, db 컨테이너를 설정하였다.

## static 파일 처리

> Django 개발 서버를 시작했습니다. 개발 서버는 순수 Python으로 작성된 경량 웹 서버입니다. Django에 포함되어 있어 아무 설정 없이 바로 개발에 사용할 수 있습니다.  
 
> 이쯤에서 하나 기억할 것이 있습니다. 절대로 개발 서버를 운영 환경에서 사용하지 마십시요. 개발 서버는 오직 개발 목적으로만 사용하여야 합니다(우리는 웹 프레임워크를 만들지 웹 서버를 만들지는 않거든요).

실제 운영 환경에선 `nginx`, `apache`와 같은 static 파일만을 처리하는 웹 서버를 사용해야 한다.  
CEOS에선 웹 서버로 `nginx`, wsgi로 `gunicorn`을 사용한다. 

개발 환경에서 `django`만 사용한다면 runserver 실행 시 static 파일들을 /static/ 디렉토리로 모아준다.  
이것은 `django.contrib.staticfiles` 라는 모듈이 static 파일의 전송을 담당해서 그렇다.   
하지만, `DEBUG` 설정을 False로 설정하는 운영 환경에선 동작하지 않는다. (settings/dev.py, prod.py 참조)  

nginx도 사용해야하는 운영 환경에선 static 파일들을 수동으로 모아주고 어디에 있는지 설정도 해주어야 한다.  
이 때 수동으로 static 파일들을 모아주는 명령어가 `collectstatic` 이다. 

```shell
> python manage.py collectstatic
```

`collectstatic`을 실행하였을 때 어디로 모이게 될까?

```python
# settings/base.py
...
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

설정파일에 있는 `STATIC_ROOT`가 `collectstatic`이 실행되었을 때 static 파일들이 모이는 곳이다.

이제 `python manage.py collectstatic` 명령어를 실행하면 static 이란 폴더에 static 파일들이 전부 모인다!

웹서버인 nginx에도 `STATIC_ROOT`에 static 파일들이 있다는 것을 알려야 한다.

```
# config/nginx/nginx.conf

location /static/ {
alias /home/app/web/static/;
}
```

`nginx.conf`에 위와 같은 설정이 있으므로 `/static/` URL로 오는 static request들을 `web/static/`에서 찾은 뒤 response한다.


## COMMAND & ENTRYPOINT

> The `ENTRYPOINT` specifies a command that will always be executed when the container starts. The `CMD` specifies arguments that will be fed to the `ENTRYPOINT`.
> 
즉 `ENTRYPOINT`의 경우엔 항상 실행이 되는 명령어이고, `CMD`의 경우엔 default한 인자라고 생각할 수 있다.

이를 직접 보기 위해서 Dockerfile을 다음과 같이 작성하였다.

```Dockerfile
# Dockerfile
FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD test1.py /app
ADD test2.py /app

ENTRYPOINT ["python"]
CMD ["test1.py", "CMD gave args"]
```

컨테이너가 run되면, 인자로 주어진 파일을 실행하는 컨테이너를 만들었다.  
`CMD`을 test1.py CMD gave args 로 설정했으므로,  
인자를 아무것도 안주고 실행한다면 `test1.py`에 "CMD gave args"란 값이 인자로 전해지게 될 것이다.

이를 위해 `test1.py`, `test2.py`를 다음과 같이 작성하였다.
```python
# test1.py
import sys

args = sys.argv
length = len(args)
print("test1.py execute!")
for i in range(length):
    print(args[i])
```

```python
# test2.py
import sys

args = sys.argv
length = len(args)
print("test2.py execute!")
for i in range(length):
    print(args[i])
```

받은 인자들을 그대로 실행되는 간단한 프로그램을 만들었다.

### 결과

실행결과는 다음과 같다.

![docker-test-result1](./img/test1.png)
인자를 아무것도 주지 않았을 때  
**CMD gave args**가 출력된다.

<br>


![docker-test-result2](./img/test1-with-args.png)
인자를 test1.py ARGS 2개 주었을 때  
**ARGS**가 출력된다.

<br>

![docker-test-result3](./img/test2-with-args.png)
인자를 test2.py ARGSARGS! 2개 주었을 때  
**ARGSARGS!**가 출력된다.

<br>

앞서 예상했던 것과 같이 아무 인자도 주지 않았을 땐, `CMD`가 실행되어서 CMD gave args 라는 출력을 볼 수 있었다.  

인자를 주었을 땐, `CMD` 부분이 오버라이딩 되어서 출력되지 않고, 인자 부분이 출력되는 것을 볼 수 있다.

```yaml
#docker-compose.prod.yml
web:
    container_name: web
    build:
      context: ./
      dockerfile: Dockerfile.prod
    command: gunicorn django-rest-framework-14th.wsgi:application --bind 0.0.0.0:8000
    entrypoint:
      - sh
      - config/docker/entrypoint.prod.sh
      
    ...
    
```


## 서버 및 컨테이너에 접속하기

앞으로 서버에 접속하게될일이 많을 것 같아 간단하게 sheel script 파일로 만들었다.
![public-ip-dns](img/public-ip-dns.png)

```shell
#!/bin/bash

ssh -i {pem 파일 위치} ubuntu@{퍼블릭 IPv4 DNS}
```

ssh로 ec2 서버에 접속이 가능하다.

ec2 서버에 docker를 이용하여 서버를 구동하기 때문에, 먼저 터미널에
```shell
> sudo docker ps
```

를 입력하여 구동되고 있는 컨테이너들을 확인한다.

![containers](img/containers.png)

접속하고 싶은 컨테이너의 이름이 web이므로 다음과 같이 명령어를 입력한다.

```shell
> sudo docker exec -it web sh
```

접속완료!

# 결론
docker에 대해 굉장히 자세하게 알게되어서 굉장히 기분이 좋다.  
강해진 느낌이 든다.

<br>
<br>

# Reference
https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html  

https://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile

https://my-repo.tistory.com/31**

https://joont92.github.io/docker/volume-container-추가하기/

https://jay-ji.tistory.com/66

https://docs.docker.com/develop/develop-images/multistage-build/