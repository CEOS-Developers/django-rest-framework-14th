### **1\. Docker의 개요**

**\- docker란?**: 가상 컨테이너 기술.

**\- 컨테이너 기술?** 

네트워크, 스토리지, 보안 등 각 영역에서의 정책이 모두 다르기 때문에 프로그램들은 환경이 바뀔 때마다 각종 오류가 발생하는 문제에 직면 -> 소프트웨어가 다른 환경으로 이동하더라도 안정적으로 실행되도록 하기 위한 기술이 필요했음. -> 컨테이너 기술 등장

**\- 컨테이너**: 모듈화되고 격리된 컴퓨팅 공간(환경). Host OS 상에 어플리케이션을 구동시키기 위해 필요한 라이브러리, 파일 등을 하나로 패키징 해, 마치 별도의 서버인 것처럼 사용할 수 있게 만든 것.

**\- 컨테이너 기술:** 리눅스 기반 Host OS를 공유하며, 여러개의 컨테이너들이 격리되어 서로 영향을 미치지 않고 독립적으로 실행하게 하는 기술.

**\- VM과 Container 가상화 비교**

| **VM** | **Container** |
| --- | --- |
| 하이퍼바이저가 여러개의 VM을 띄우고 실행. OS 전체를 가상화하는 방식.(전가상화의 경우) | 같은 OS를 공유하고(OS의 리소스를 컨테이너들이 공유) 프로세스만 격리하는 방법. |
| VM마다 독립적인 실행환경 제공 -> 많은 용량 차지 | os의 자원을 컨테이너들이 공유 -> 부팅시간 짧고, 공간 차지 적음 |
| 속도 저하(리소스 분할 및 퍼포먼스 오버헤드), CI/CD 어려움 | 빠른 속도, 효율성, 이식성 좋음. CI/CD, MSA와 조화 |

![image](https://user-images.githubusercontent.com/77983074/135456938-32daee35-ecf6-409e-9048-d2fb63fd435e.png)

참고자료: [https://www.redhat.com/ko/topics/containers/containers-vs-vms]

**\- docker 구조**

>1) docker client와 docker server(engine)
>
>2) docker image
>
>  -**Dockerfile**: 내가 생성하고자 하는 컨테이너, 그 환경을 만들기 위해 필요한 패키지를 설치하고 동작하기 위한 설정을 담은 파일. Dockerfile을 빌드하면 자동으로 Docker image가 생성됨. 
>
>  -**Docker Image**: 서비스 운영에 필요한 서버 프로그램, 소스 코드, 컴파일된 실행 파일 등을 묶은 형태로 컨테이너를 생성하는 템플릿 역할. <- 이미지는 변경 불가능. 컨테이너의 비저장성은 >컨테이너 내용을 일관되게 한다.
>
>3) docker registry: docker image를 저장하는 repostory. docker hub.
>
>4) docker container: docker image를 run하여 docker container를 생성한다. 

---

### **2\. docker-compose란?**

\- **docker compose**: 다중 컨테이너 도커 애플리케이션을 정의하고 동작하게 해주는 툴. (여러 컨테이너의 실행을 한 번에 관리할 수 있게 하는 것!)

\- **왜 사용하는지?**

**docker로 개발환경 구성 시 불편한 점**

>**1) 장황한 옵션**
>
>도커 명령어는 간단하지 않고 옵션이 많아 장황하다.   
>
>**2) 앱 컨테이너와 데이터베이스 컨테이너의 실행 순서**
>
>기본적으로 도커 컨테이너들은 각각 격리된 환경에서 실행되므로 별도의 옵션을 지정하지 않으면 다른 컨테이너의 존재를 알 수 없다. 따라서 반드시 데이터베이스 컨테이너를 실행한 다음에 앱 컨테이>너를 실행하며 db 컨테이너를 연결해줘야 한다. 그렇지 않으면 앱 컨테이너에서 데이터베이스 컨테이너를 찾을 수 없다. -> 만약 앱컨테이너를 먼저 실행했다면 종료하고 순서를 맞춰 다시 실행해야하는 >불편함이 존재.

**\->** **도커 컴포즈를 사용하면 컨테이너 실행에 필요한 옵션을 docker-compose.yml이라는 파일에 적어둘 수 있고, 컨테이너 간 실행 순서나 의존성도 관리할 수 있다.**

\- **docker-compose.yml**

```
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

\- db와 web, 2개의 컨테이너를 정의하고 있고, 이 두 컨테이너는 서로 소통할 수 있음.

참고자료: [https://www.44bits.io/ko/post/almost-perfect-development-environment-with-docker-and-docker-compose#docker-compose.yml-%ED%8C%8C%EC%9D%BC](https://www.44bits.io/ko/post/almost-perfect-development-environment-with-docker-and-docker-compose#docker-compose.yml-%ED%8C%8C%EC%9D%BC)

---

### **3\. 서버가 실행되는 과정**

**Github actions를 이용한 배포 자동화**
>
>- 수정사항이 생길 때마다 ssh key로 인스턴스에 접근해서 git pull command를 입력하는 건 매우 귀찮다! 이런 번거로운 작업을 해야하다보면 자연스럽게 업데이트 주기가 늦어지고, 소스 코드에 큰 >변화가 있을 때만 배포를 하게 되니 서비스에 대한 관심도도 떨어지게 된다. 이러한 불편함을 개선하기 위해 Github Actions로 aws서비스에 배포하는 프로세스를 자동화해보자!

**.github/worksflow/deploy.yml**

1) repository에 \[push\]가 되면 github actions이 deploy.yml의 workflow 단계를 수행한다.

```
name: Deploy to EC2
on: [push]
```

2) 빌드 머신 준비 / 빌드 머신의 repository에 checkout

```
build:
    name: Build
    runs-on: ubuntu-latest
    steps:
    - name: checkout
      uses: actions/checkout@master
```

3) .env 파일 생성 후 secretes.ENV\_VARS 내용 추가

```
 - name: create env file
      run: |
        touch .env
        echo "${{ secrets.ENV_VARS }}" >> .env
```

4) ssh를 이용해 ec2 서버에 접속하여 directory 만들기

```
- name: create remote directory
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: mkdir -p /home/ubuntu/srv/ubuntu
```

5) Github workspace에 있는 파일을 ssh를 통한 rsync를 통해 원격 폴더에 배포

```
  - name: copy source via ssh key
      uses: burnett01/rsync-deployments@4.1
      with:
        switches: -avzr --delete
        remote_path: /home/ubuntu/srv/ubuntu/
        remote_host: ${{ secrets.HOST }}
        remote_user: ubuntu
        remote_key: ${{ secrets.KEY }}
```

![image](https://user-images.githubusercontent.com/77983074/135457134-3046920a-dde8-41aa-b59e-cb20afe43bef.png)

참고자료: [https://github.com/Burnett01/rsync-deployments](https://github.com/Burnett01/rsync-deployments)

6) 서버에 접속하여 deploy.sh 실행

```
   - name: executing remote ssh commands using password
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: |
          sh /home/ubuntu/srv/ubuntu/config/scripts/deploy.sh
```

\-> Actions가 5번에서 push된 소스를 서버에 복사해 갔기 때문에 해당 경로에 deploy.sh 파일 확인 가능

**config/scripts/deploy.sh**

```
#!/bin/bash

# Installing docker engine if not exists
if ! type docker > /dev/null
then
  # 중략. ec2 인스턴스에는 아무것도 없으므로 설치가 필요.
fi

# Installing docker-compose if not exists
if ! type docker-compose > /dev/null
then
  # 중략
fi

echo "start docker-compose up: ubuntu"
sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d
```

`sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d`

`-> 실행되길 기대하는 코드`

이 스크립트 파일은 Github Actions가 수행했고, EC2 서버에서 실행되고 있음. 이 command에 의해 서버가 build되고 실행되는 것!

**docker-compose.prod.yml**

docker-compose.yml 과의 차이점은

>1) db 컨테이너가 없다.
>
>이유: 데이터 유출의 위험성, 인스턴스의 자원을 서버와 db가 같이 쓰면 비효율적임. 만약 서버가 해킹당했다면, 서버의 코드 뿐 아니라 개인정보까지 유출될 위험성.
>
>2) nginx 컨테이너가 있다. 

(application: Django / server: nginx)

docker-compose.prod.yml

```
 nginx:
    container_name: nginx
    build: ./config/nginx
```

해당 ./config/nginx path에 있는 Dockerfile을 찾아 실행해줌. 

/config/nginx/Dockerfile

```
FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```

-   FROM nginx:1.19.0-alpine: nginx 구동에 필요한 환경이 해당 이미지 안에 모두 들어가 있음. 

-   RUN rm /etc/nginx/conf.d/default.conf: default config 파일을 삭제. 원하는 설정파일로 변경 가능.

-   COPY nginx.conf /etc/nginx/conf.d: nginx.conf 파일 옮김.

#### **\- Docker compose up이란?**

`sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d`

-   up: docker-compose 파일에 정의된 모든 컨테이너를 띄우라는 명령.
-   \--build: up할때마다 새로 build를 수행하도록 강제하는 파라미터(코드 변경사항 반영을 위함)
-   \-d: 백그라운드 실행

docker-compose는 django를 모르기때문에 up이 되었을 때 django를 실행시키기 위해서 command와 entrypoint 정의 필요.

\- entrypoint와 cmd는 해당 컨테이너가 수행하게 될 실행명령을 정의하는 선언문.

docker-compose.prod.yml

```
web:
    command: gunicorn django-rest-framework-14th.wsgi:application --bind 0.0.0.0:8000

    entrypoint:
      - sh
      - config/docker/entrypoint.prod.sh
```

\- command: 해당 프로젝트가 사용하는 gunicorn을 실행시킨다.

\- entrypoint: entypoint.prod.sh를 실행한다.

config/docker/entrypoint.prod.sh

```
#!/bin/sh

python manage.py collectstatic --no-input

exec "$@"
```

\-django의 collectstatic을 수행한다.

#### \- **collectstatic은?**: static 파일들을 한 곳에 모아주는 명령어

#### \- 왜 static 파일들을 모아야 하는데?

>하나의 프로젝트에서 사용하는 정적 파일들(css, image, javascript 등)은 여기저기에 분산되어 있기 때문에 요청이 들어왔을 때 필요한 정적 파일을 돌려주려면 많은 경로를 탐색해야 하므로 매우 비>효율적이다. 그래서 사용하는 모든 정적 파일을 하나의 경로로 모아주는 작업이 필요하다. 개발 중에는 runserver를 하면 이 작업을 알아서 해주지만, 실제로 Production 환경에서는 Apache나 Nginx>와 같은 웹서버를 사용해야 하므로 직접 모아주는 작업을 위해 collectstatic 명령을 사용한다. 

\-settings/base.py

```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

Django 프로젝트 홈 디렉토리 밑에 static 라는 폴더를 생성하고 그곳으로 모든 정적 파일들을 모으도록 설정한 것을 볼 수 있다.

runserver는 STATIC\_URL 에 지정된 URL을 통해 정적 파일 요청을 받아오지만 서버에 배포를 하고나면 Nginx가 요청을 받게되므로 정적 파일 요청을 처리할 수 있도록 정적 파일 URL을 지정해주어야 한다.

![image](https://user-images.githubusercontent.com/77983074/135457325-58195efc-1f40-499a-afac-68e4a34b8d1a.png) 

이제 /static/ URL로 정적 파일 요청이 들어오면 모든 정적 파일을 모아놓은 폴더인 web/static/ 폴더에서 찾아 되돌려보낸다.

참고자료: [https://crynut84.github.io/2016/11/14/django-static-file/](https://crynut84.github.io/2016/11/14/django-static-file/), [https://nachwon.github.io/django-deploy-4-static/](https://nachwon.github.io/django-deploy-4-static/)

#### \- cmd와 entrypoint의 차이점은?

**컨테이너 시작시 실행 명령에 대한 Default 지정 여부**  

만약 ENTRYPOINT 를 사용하여 컨테이너 수행 명령을 정의한 경우, 해당 컨테이너가 수행될 때 반드시 ENTRYPOINT 에서 지정한 명령을 수행되도록 지정된다. 하지만, CMD를 사용하여 수행 명령을 한 경우, 컨테이너를 실행할때 인자값을 주게 되면 Dockerfile에 지정된 CMD 값 대신 지정한 인자값으로 변경하여 실행되게 된다.

참고자료: [https://bluese05.tistory.com/77](https://bluese05.tistory.com/77)
