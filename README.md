# Docker와 Github Action을 이용한 자동 배포하기



## Docker 의 필요성

[생활코딩 Docker 강의](https://www.youtube.com/playlist?list=PLuHgQVnccGMDeMJsGq2O-55Ymtx0IdKWf)
을 바탕으로 정리한 내용입니다\
앱을 실행하는 여러 방식 중 우리가 사용하는 `컨테이너(Container)` 방식\
컨테이너 기술은 `리눅스` 운영체제에서 동작한다.
- 리눅스 컨테이너(Container) 방식 구조
```
OS
    APP                 # 내가 만든 서비스
    Container           # 웹 서버를 실행하기 위한 컨테이너. 운영체제와는 다른 개념
        Web Server
        lib             # 웹 서버 실행을 위한 라이브러리들
        bin             # 웹 서버 실행을 위한 실행파일들
    Container           # 데이터베이스를 실행하기 위한 컨테이너.
        Database
        lib             # 데이터베이스 실행을 위한 라이브러리들
        bin             # 데이터베이스 실행을 위한 실행파일들
```
- 가상화(ex. VMWare) vs 컨테이너
```
가상화
    운영체제 내 여러 운영체제를 설치 및 실행
    
컨테이너
    동일한 운영체제를 공유
    각 컨테이너는 나머지 부분으로부터 격리되어 실행
    빠른 실행 속도 + 가벼운 환경 유지
```
- 컨테이너화 소프트웨어
```
Docker
AWS Fargate
Google Kubernetes Engine
아마존 ECS
LXC
...등등
```
우리가 개발한 서비스, 환경 등을 개별 컨테이너 이미지로 만들어주는 소프트웨어인 듯 하다.\
이 중 가장 널리 쓰이는 소프트웨어는 `Docker`


## Dockerfile
어떤 단계를 거쳐 `이미지(image)`가 `빌드(build)` 되는지 담고있는 파일

```Dockerfile
# 명령어(INSTRUCTION) 인자(arguments) 구성

# python 이미지를 기반으로 시작. Docker hub에 가면 python image 공개되어 있음.
FROM python:3.8.3-alpine    
ENV PYTHONUNBUFFERED 1      # 환경변수 설정

RUN mkdir /app      # shell 커맨드처럼 RUN 명령문 사용
WORKDIR /app        # 작업 디렉토리 설정

# RUN 명령문을 통해 필요한 소프트웨어 설치
# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base



# 호스트 컴퓨터에 있는 requirements.txt 파일을 도커 이미지 내 파일 시스템에 복사
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt     # 필요한 패키지 설치

# Now copy in our code, and run it
COPY . /app/
```

## docker-compose.yml
여러개의 컨테이너를 정의하고 공유할 수 있도록 내용을 정의해놓은 파일

```yml
version: '3'
services:

  db:       # 독립된 컨테이너 1
    container_name: db      # 컨테이너 이름
    image: mariadb:latest   # 사용할 이미지
    restart: always
    environment:            # 환경변수 설정
      MYSQL_ROOT_HOST: '%'
      MYSQL_ROOT_PASSWORD: mysql
    expose:
      - 3306                # 컨테이너 내부에만 공개하는 포트
    ports:
      - "3307:3306"         # 호스트의 포트번호: 컨테이너의 포트번호
    env_file: 
      - .env                
    volumes:                # 볼륨 설정. 데이터를 컨테이너가 아닌 호스트에 저장
      - dbdata:/var/lib/mysql

  web:      # 독립된 컨테이너 2
    container_name: web
    build: .        # Dockerfile 이용해서 이미지 빌드
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    environment:    # 환경변수 설정
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
    depends_on:     # 의존 관계 지정. db 컨테이너가 먼저 올라오고 나서 web 컨테이너 빌드
      - db
volumes:
  app:
  dbdata:

```

## Docker Compose 명령어
> 배포의 마지막 단계에서 Github actions를 통해\
> EC2 서버 내에서 아래 명령을 수행
```commandline
$ sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d
```

- `-f` \
  docker-compose 의 설정 파일 명시
- `up` \
  docker-compose에 정의되어 있는 모든 컨테이너를 한번에 생성하고 실행
- `-d` \
  컨테이너를 백그라운드에서 띄우기
- `--build` \
  서비스 시작 전 이미지를 항상 새로 생성

***
## Nginx
> Django로 서버를 만들어 놓고 왜 배포할 때 Nginx를 새로 설치해서 사용할까?
> Nginx는 무엇이고 왜 사용할까

참고 - [우리밋IT - Nginx 영상](https://www.youtube.com/watch?v=ZJpT-Wa-pZ8)

### Nginx 란?
```text
# 프론트엔드와 백엔드의 통신
Client  <-> Web Server <-> WAS <-> Database
브라우저        Nginx       Django      MySQL
```
>Nginx는 위에서 Web Server에 해당하는 소프트웨어의 일종

### `Web Server` vs `WAS(Web Application Server)`
- Web Server\
단순히 정적 파일을 응답 (HTML, CSS, JS)
- WAS(Web Application Server)\
클라이언트 요청에 대해 `동적인 처리`가 이뤄진 후 응답 (로그인 처리, 회원가입 처리 등 ...)

> Django는 Web Server로의 역할, WAS로의 역할도 수행 가능

### Nginx와 같은 Web Server를 사용하는 이유?
> 단순 정적 파일을 응답하는 작업에 대한 부담을 줄여주기 위해!!

### Nginx의 장점
- 빠르다
- 리버스 프록시
  ```text
  # 클라이언트와 인터넷 사이에 있는 포워드 프록시 (우리가 흔히 아는 프록시)
                                    WAS1
  client    proxy    internet       WAS2
                                    WAS3
  
  # 인터넷과 백엔드 사이에 있는 리버스 프록시
                                    WAS1
  client    internet    Nginx       WAS2
                                    WAS3
  ```
  - 로드 밸런싱 (load-balancing)\
    클라이언트의 요청을 받아 적절한 WAS에 전달
  - 캐싱 서버로의 역할\
    같은 자원에 대한 반복적인 요청을 직접 처리
- SSL 지원\
  HTTPS 인증서를 제공. 자세한 내용은 추후 공부해야지..
- 웹페이지 접근 인증
- 압축
- 비동기 처리
- 