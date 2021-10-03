# Docker와 Github Actions을 이용한 자동 배포

## Docker의 원리

**어떤 OS에서도 같은 환경을 만들어주는 원리**이다. 따라서 서버에 docker만 깔고 배포를 해도 된다.   
-> 서버에 접속해서 docker 실행, master에 푸시 된 커밋을 복사하는 역할을 Github Actions이 해준다   
-> 이 과정을 CD(Continuous Delivery)

## Docker와 docker-compose

Docker는 위에서 말한 가상 컨테이너 기술이다. 애플리케이션을 신속하게 구축, 
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
  
## 이미지란?
>이미지는 컨테이너 실행에 필요한 파일과 설정값등을 포함하고 있는 것으로 상태값을 가지지 않고 변하지 않는다. 컨테이너는 이미지를 실행한 상태라고 볼 수 있고 추가되거나 변하는 값은 컨테이너에 저장된다. 
같은 이미지에서 여러개의 컨테이너를 생성할 수 있고 컨테이너의 상태가 바뀌거나 컨테이너가 삭제되더라도 이미지는 변하지 않고 그대로 남아있다.
## 컨테이너란?

>운영체계를 기반으로 만들어진 대부분의 Software는 그 실행을 위하여 OS와 Library를 포함, Software가 필요로 하는 파일 등으로 구성된 실행환경이 필요한데, 
하나의 시스템 위에서 둘 이상의 Software를 동시에 실행하려고 한다면 문제가 발생할 수 있다.   
>
> 예를 들어 두 소프트웨어가 동일한 Library를 사용하고 있지만 서로 다른 버전을 사용하는 경우에 문제가 발생한다.   
> 이러한 문제점의 가장 간단한 해결책은 두 Software를 위한 시스템을 각각 준비하는 것인데, 이럴 경우 비용의 문제가 생긴다.  
> 
> 위와 같은 문제점들을 효율적으로 해결하는 것이 바로 컨테이너이다.
> 컨테이너는 개별 소프트웨어의 실행에 필요한 실행환경을 독립적으로 운용할 수 있도록 기반환경 또는 다른 실행환경과의 간섭을 막고 실행의 독립성을 확보해주는 운영체계 수준의 격리 기술을 말한다. 


### 컨테이너 vs 가상 머신(Virtual Machine)
우선 가상머신이란 호스트 운영체제에서 구동되며 그 바탕이 되는 하드웨어에 가상으로 액세스하는 Linux, Windows 등의 게스트 운영체제를 의미한다.
* 유사점: 컨테이너는 가상 머신과 마찬가지로 애플리케이션을 관련 라이브러리 및 종속 항목과 함께 패키지로 묶어 소프트웨어 서비스 구동을 위한 격리 환경을 마련해 준다.
* 차이점: 가상 머신은 하드웨어 스택을 가상화합니다. 컨테이너는 이와 달리 운영체제 수준에서 가상화를 실시하여 다수의 컨테이너를 OS 커널에서 직접 구동하므로 컨테이너는 훨씬 가볍고 운영체제 커널을 공유하며, 시작이 훨씬 빠르고 운영체제 전체 부팅보다 메모리를 훨씬 적게 차지한다.

![VMvsContainer](https://user-images.githubusercontent.com/79985974/135488158-e9fdecb6-7854-4d5d-92d7-be65881b286a.PNG)

### 컨테이너의 이점
#### 1. 모듈성
Docker의 컨테이너화 접근 방식은 전체 애플리케이션을 분해할 필요 없이 애플리케이션의 일부를 분해하고, 업데이트 또는 복구하는 능력에 집중되어 있다.
#### 2. 계층 및 이미지 버전 제어
각 Docker 이미지 파일은 일련의 계층으로 이루어져 있으며 이 계층들은 단일 이미지로 결합된다. 이미지가 변경될 때 계층이 생성되고, 
사용자가 실행 또는 복사와 같은 명령을 지정할 때마다 새 계층이 생성된다.   
Docker는 새로운 컨테이너를 구축할 때 이러한 계층을 재사용하므로 구축 프로세스가 훨씬 더 빨라지고  계층화에는 버전 관리가 내재되어 있으며 새로운 변경 사항이 발생할 때마다 내장 변경 로그가 기본적으로 적용되므로 컨테이너 이미지를 완전히 제어할 수 있다.
#### 3. 롤백
모든 이미지에는 계층이 있으며, 현재의 이미지 반복이 적절하지 않은 경우 이전 버전으로 롤백하면 된다.
#### 4. 신속한 배포
Docker 기반 컨테이너는 배포 시간을 몇 초로 단축할 수 있다. 각 프로세스에 대한 컨테이너를 생성함으로써 사용자는 유사한 프로세스를 새 앱과 빠르게 공유할 수 있다. 
또한, 컨테이너를 추가하거나 이동하기 위해 OS를 부팅할 필요가 없으므로 배포 시간이 크게 단축된다. 이뿐만 아니라 배포 속도가 빨라 컨테이너에서 생성된 데이터를 효율적으로 쉽게 생성하고 삭제할 수 있다.

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
> 맨 마지막에 있는 코드가 결국 서버를 실행하는 코드이다. 이 스크립트 파일은 Github Actions가 수행했고, 이 스크립트 파일은 EC2 서버에서 실행되고 있으며, 결국은 이 command에 의해 서버가 build되고 실행 된다.
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
## Github Actions

```yaml
name: Deploy to EC2
on: [push] # push 될 때 마다 이 workflow를 수행
jobs:

  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
    - name: checkout
      uses: actions/checkout@master

    - name: create env file #깃헙 설정에 복사한 ENV_VARS의 값을 모두 .env file로 만든다.
      run: |
        touch .env
        echo "${{ secrets.ENV_VARS }}" >> .env

    - name: create remote directory # ec2 서버에 디렉토리를 하나 만들어준다.
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: mkdir -p /home/ubuntu/srv/ubuntu

    - name: copy source via ssh key # ssh key를 이용해 현재 푸시된 소스를 서버에 복사한다.
      uses: burnett01/rsync-deployments@4.1
      with:
        switches: -avzr --delete
        remote_path: /home/ubuntu/srv/ubuntu/
        remote_host: ${{ secrets.HOST }}
        remote_user: ubuntu
        remote_key: ${{ secrets.KEY }}

    - name: executing remote ssh commands using password # 서버에 접속하여 deploy.sh 를 실행시킨다.
      uses: appleboy/ssh-action@master
      env:
        DEPLOY_USERNAME: hanqyu
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: |
          ****sh /home/ubuntu/srv/ubuntu/config/scripts/deploy.sh

```
## 요약
1.  branch main으로 push를 한다.
2. Github Actions이 코드를 서버에 올리고 deploy.sh를 실행시킨다.
3. deploy.sh는 docker-compose.prod.yml 파일을 실행시킨다.
4. docker-compose.prod.yml에서 web이라는 컨테이너와 nginx라는 컨테이너 생성하고 실행한다.
