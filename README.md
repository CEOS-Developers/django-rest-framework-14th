# 목차

- 파일 뜯어보기
  - Dockerfile
  - docker-compose.yml
- Github action을 이용한 자동배포
- 개발환경과 배포환경 일치시키기
- Reference

# 파일 뜯어보기

## 파일 구조

```text
# docker, 배포 관련 파일만 표시
.
├── .github
│   └── workflows
│       └── deploy.yml
├── config
│   ├── docker
│   │   └── entrypoint.prod.sh
│   ├── nginx
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── scripts
│       └── deploy.sh
├── django-rest-framework-14th
├── .env
├── .env.prod
├── doker-compose.prod.yml
├── doker-compose.yml
├── Dockerfile
├── Dockerfile.prod
└── requirements.txt
```

## Dockerfile, docker-compose.yml 의 역할

### 기본적인 이해

도커는 컨테이너 기반의 오픈소스 가상화 플랫폼이다.<br>
도커에 대해서 검색하면 기존의 VM과 Docker의 차이점을 말하면서 설명할텐데,<br>
쉽게 말하면 '컨테이너' 라는 개념을 사용하여 '프로세스를 격리'하는 방식으로 '더 가볍고 빠르다'<br>
정도로 이해하면 사용하는 데 무리는 없을 것 같다.<br>

`Dockerfile`로 이미지를 만들고, `docker-compose.yml`로 컨테이너를 만든다.<br>
간단한 서버 이미지를 만들고 run 하는데는 커맨드라인 몇 줄이면 가능하겠지만,<br>
컨테이너 조합이 많아지고 여러가지 설정이 추가되면 명령어가 금방 복잡해지므로,<br>
도커는 복잡한 설정을 쉽게 관리하기 위해 YAML방식의 설정파일을 이용한 Docker Compose라는 툴을 제공한다.

여러 장점들이 있지만, 도커를 사용하는 이유가 되는 장점은 크게 다음과 같다.
1. 개발환경, 배포환경을 일치시킬 수 있다.
   1. 프로젝트를 개발하는 환경은 참여하는 모두가 일치할 수 없다. (매번 새로운 팀원이 들어왔을 때 세팅하는데 시간을 쓸 필요가 없다. 코드에만 집중 가능)
   2. 배포환경에서 개발을 진행하기 때문에 배포에 대한 스트레스를 줄일 수 있다.
   3. 테스트 환경을 위한 VM 구축이나 새로운 컴퓨터를 사지 않아도 된다.
2. Layer 개념으로 유니온 파일 시스템을 이용하여 여러개의 레이어를 하나의 파일시스템으로 사용할 수 있다.
   1. 이미지나 컨테이너를 처음 만들 때와, 다시 만들 때 만들어지는 속도만 봐도 알 수 있다. 기존에 쓰던 파일 중 교체할 필요가 없는 것들은 놔두고 교체가 필요한 파일만 바꿔치기한다.
   2. 여러 개의 컨테이너로 이루어진 앱의 경우 하나의 컨테이너만 교체하는 식으로 서비스 전체를 내렸다가 올리지 않아도 된다.
3. 도커 이미지를 `Docker hub` 로 무료로 관리할 수 있다.
   1. 도커 이미지는 보통 수백 메가에서 크게는 몇 기가까지 용량이 큰데, 서버에 저장하고 관리하기 쉽지 않다.
4. 커뮤니티(생태계)가 크다.
   1. Google을 필두로 사용자가 많다.
   2. 지원되는 다양한 툴들이 많다.
   3. 오픈소스 프로젝트들이 다양하다.
5. 로고가 귀엽다.

### Dockerfile

도커파일은 **이미지**를 만드는 파일이다. 코드를 살펴보자.

```dockerfile
# 베이스가 될 이미지를 고른다.
FROM python:3.8.3-alpine
# 환경변수 세팅
ENV PYTHONUNBUFFERED 1

# /app 디렉토리를 만든다.
RUN mkdir /app
# 작업을 수행할 WORKDIR를 지정한다.
WORKDIR /app

# dependencies for psycopg2-binary
# 패키지 설치 커맨드
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base


# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
# requirements.txt의 내용을 가져온다.
COPY requirements.txt /app/requirements.txt
# pip install로 requirements.txt에 있는 목록들을 설치한다.
RUN pip install -r requirements.txt

# Now copy in our code, and run it
# 우리가 작성한 코드 전체 (.)를 /app/ 에 복사한다.
COPY . /app/
```
왜 올리고 바로 지움?

### docker-compose.yml

docker-compose 파일은 **컨테이너**를 만드는 파일이다.<br>
`ports:` 에서 포트를 연결하는 것과 `volumes`에서 디렉토리를 연결하는 것 모두<br>
`:` 를 사이에 두고 사용된다. 구조는 `<host>`:`<container>` 이다.<br>
`db: ports: ` 부분에 있는 `"3307":"3306"`는 <br>
`host`의 3307번 포트와 `container`의 3306포트를 연결한다는 뜻이다. 

```yaml
# 버전 명시
version: '3'

# 컨테이너 정의 
services:
  # db 컨테이너 생성, image는 이미 만들어진 이미지 사용(dockerhub)
  # 컨테이너 내에서 root 계정 정의
  # 3306 포트로 expose, 3307:3306으로 포트 매핑
  # .env 가져와서 환경 정의
  # 볼륨 매핑
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

  # web 컨테이너 생성
  # db migrate, 0.0.0.0:8000에서 server run.
  # 위에서 설정한 mysql 연결
  # 8000:8000으로 포트 매핑
  # .:/app 으로 볼륨 매핑
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

# 볼륨 정의
volumes:
  app:
  dbdata:
```

### Dockerfile.prod

위의 Dockerfile과 전체적인 흐름은 동일하다.<br>
패키지 설치하고, `requirements.txt` 설치하고, src 복사하는 과정을 거친다.<br>
차이점이 있다면, 환경변수 세팅과 user를 만들어주는 점이다.<br>

### docker-compose.prod.yml

역시 위의 docker-compose.yml과 전체적인 흐름은 동일하다.<br>
차이점은 db 컨테이너 대신 nginx 컨테이너를 생성한다는 점이다.<br>
똑같이 db 컨테이너를 만들게 되면 ec2 인스턴스의 자원을 서버와 디비가 같이 사용하게 되어서 비효율적이고,<br>
또, db와 같은 data는 container의 휘발성 때문에 volume을 사용해야 하는데, 보안상으로도 위험하다고 한다.<br>

두 가지 의문이 생길 수 있다.
1. `web:` 에서 `env_file`:은 `.env`인데, 왜 `env.prod`를 쓰지 않지?
2. `web:`에서 분명 8000포트로 expose했는데, 왜 `nginx`에서는 `80:80`으로 매핑하지?

1번 질문은 사실은 .env.prod 파일이다. `.github/workflows/deploy.yml`의 코드를 보자. 
```text
- name: create env file
      run: |
        touch .env
        echo "${{ secrets.ENV_VARS }}" >> .env
```
우리는 `github`의 `settings` 탭에서 `.env.prod`를 `ENV_VARS`로 정의해 두었다.<br>
미리 정의한 `secrets` 안의 `ENV_VARS`를<br>
우분투 내에 `.env` 라는 이름으로 만들어 준다.<br>

2번 질문은 `/config/nginx/nginx.conf`를 보면 알 수 있다.
```text
upstream django-rest-framework-14th {
  server web:8000;
}
```
여기서 8000 포트와 이미 매핑되어있고, 그 밑에서
```text
server {

  listen 80;

  location / {
    proxy_pass http://django-rest-framework-14th;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $host;
    proxy_redirect off;
  }

  location /static/ {
    alias /home/app/web/static/;
  }

  location /media/ {
    alias /home/app/web/media/;
  }
}
```
80번 포트를 사용하는 것을 볼 수 있다.

# Github action을 이용한 자동배포

`Github`에서 특정 action이 일어났을 때를 감지하여 미리 지정해놓은 ec2 인스턴스에 배포하는 과정을 다뤘다.<br>
로직은 'Actions 실행시 감지' -> 'SSH 접속' -> '외부서버에서 커맨드 실행' 이다.
ssh 액션을 도와주는 
[애플보이](https://github.com/appleboy/ssh-action) 를 사용했다.<br>
ssh를 사용하여 remote한 folder로 deploy를 도와주는
[rsync deployments](https://github.com/Burnett01/rsync-deployments) 를 사용했다.  

```yaml
# github/workflows/deploy.yml
name: Deploy to EC2
# push 액션을 감지.
on: [push]
jobs:

  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
    - name: checkout
      # master branch 에서만 감지
      uses: actions/checkout@master

      # secrets 에 미리 정의한 ENV_VARS 를 .env 로 만들어 줌
    - name: create env file
      run: |
        touch .env
        echo "${{ secrets.ENV_VARS }}" >> .env

      # secrets 에 미리 정의한 HOST, KEY 를 이용해 ssh 접속 후 dir 생성
    - name: create remote directory
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: mkdir -p /home/ubuntu/srv/ubuntu
      
      # secrets 에 미리 정의한 HOST, KEY 를 이용해 ssh deploy.
    - name: copy source via ssh key
      uses: burnett01/rsync-deployments@4.1
      with:
        switches: -avzr --delete
        remote_path: /home/ubuntu/srv/ubuntu/
        remote_host: ${{ secrets.HOST }}
        remote_user: ubuntu
        remote_key: ${{ secrets.KEY }}

      # secrets 에 미리 정의한 HOST, KEY 를 이용해 ssh 접속 후 script 실행.
    - name: executing remote ssh commands using password
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: |
          sh /home/ubuntu/srv/ubuntu/config/scripts/deploy.sh
```
위에서 마지막에 실행한 `script`를 보자.
```bash
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
`docker`가 없으면 설치, `docker-compose`가 없으면 설치, 그 후 `docker-compose`를 이용해 `build`한다.<br>
여기서 -f 옵션으로 `docker-compose.prod.yml`을 이용하는 것을 볼 수 있다! (prod version)

# 개발환경과 배포환경 일치시키기

도커의 장점을 살려보자. 개발 또한 컨테이너 내부에서 진행할 수 있다.<br>
물론 로컬로 컨테이너를 실행하고 개발해도 된다.<br>
하지만 개발 환경이 하나도 세팅되지 않은 상태에서 바로 개발을 할 때를 생각해보자.<br>
python 설치, db 세팅부터 requirements.txt install 등등 할 것이 많다.<br>

## 무식한 방법

프로젝트의 docker 컨테이너를 실행시키고, cli를 열어서 vim으로 작업한다.<br>
작업이 끝나면 소스코드를 복사해서 local에 붙여넣기한다.<br>
(간단한 테스트를 할 때는 괜찮은 방법일지도...?)<br>

> 다음과 같이 `cli`버튼을 누르면 `terminal`이 열린다.<br>
![docker_desktop.png](/images/docker_desktop.png)<br>

> code가 완벽히 동일하게 같은 걸 볼 수 있다.<br>
`docker-compose.yml`에서 volume을 /app으로 매핑했기 때문에<br>
root directory가 app인 것도 확인할 수 있다.<br>
![local_web.png](/images/local_web.png)<br>
![local_web1.png](/images/local_web_1.png)<br>

>`db container`에 들어가서 돌아다니는 모습.<br>
사용자 이름은 'root', pw는 mysql이다. <br>
`docker-compose.yml`에서 그렇게 만들었기 때문.<br>
![local_db.png](/images/local_db.png)<br>
![local_db1.png](/images/local_db_1.png)<br>
![local_db2.png](/images/local_db_2.png)<br>

## Visual Studio 를 사용하는 방법

프로젝트의 docker 컨테이너를 실행시키고, <br>
우선 extention 탭에서 remote-containers를 설치한다.<br>
원격 탐색기 탭에서 현재 실행하고 있는 컨테이너와 연결한다.<br>
컨테이너 내부에서 작업하고 저장을 할 경우 <br>
local editor에서도 동일하게 적용됨을 볼 수 있다.<br>
예전에 블로그에 정리한 글을 참고하면 사진과 함께 더 자세히 알 수 있다.<br>
[벨로그 글](https://velog.io/@n0wkim/Docker-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EC%84%B8%ED%8C%85)

## 파이참을 사용하는 방법

파이참이 아직 익숙하지 않아 적용하지 못했다.<br>
[참고](https://soundprovider.tistory.com/entry/%EB%94%A5%EB%9F%AC%EB%8B%9D-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EC%84%B8%ED%8C%85%EA%B8%B0Docker-PyCharm-2) <br>
뭔가 복잡하다...ㅠ 나중에 시도해보자.

# Reference

https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html <br>
https://docs.docker.com/get-started/overview/ <br>
https://github.com/appleboy/ssh-action <br>
https://github.com/Burnett01/rsync-deployments <br>
https://soundprovider.tistory.com/entry/%EB%94%A5%EB%9F%AC%EB%8B%9D-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EC%84%B8%ED%8C%85%EA%B8%B0Docker-PyCharm-2

---

# 3주차 - Django 모델링

우선 시작에 앞서, **경준님**과 **승우님**에게 무한한 감사를 드립니다.
경준님의 리드미를 많이 참고했고, 승우님께 자문을 구했습니다.

## 인스타그램 ERD

![erd](/images/erd.png)<br>

장고 모델 모음 필드이다.<br>
[모델모음](https://donis-note.medium.com/장고-모델-필드-django-model-fields-정리-4297d1bad65b)<br>

Profile 테이블은 `django`에서 제공하는 one-to-one을 이용해서 사용하기로 했다.
`django`에서 제공하는 테이블은 다음과 같다.
![erd](/images/auth_user.png)<br>

따라서, 프로필에 추가할 사진이 들어갈 필드만 직접 넣어주기로 했다.
자세한 코드는 `models.py`를 참고해 주세요.

그리고 정말 놀라운 기능 중 하나가 **이미지 필드** 인데,
[이미지필드](https://docs.djangoproject.com/en/3.2/topics/files/)

```python
from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to='cars')
```

```shell
>>> car = Car.objects.get(name="57 Chevy")
>>> car.photo
<ImageFieldFile: cars/chevy.jpg>
>>> car.photo.name
'cars/chevy.jpg'
>>> car.photo.path
'/media/cars/chevy.jpg'
>>> car.photo.url
'http://media.example.com/cars/chevy.jpg'
```
위와 같이 참조할 수 있다는게 너무 놀랍다. 갓갓...

새로운 profile을 만드는 과정.
![usershell](/images/usershell.png)<br>
포비와 에디도 만들어주자.
![user](/images/user.png)<br>

mysql에서 실제로 값이 들어갔는지 확인해보자. 
![api_profile](/images/mysql_api_profile.png)<br>
장고가 기본으로 제공하는 User 테이블.
![auth_user](/images/mysql_auth_user.png)<br>

이렇게 object를 가져올 수 있다.
~~![object](/images/object.png)<br>

user 객체를 받아 post에 넘겨줌으로써 새로운 게시물을 만들 수 있다.
![post](/images/post.png)<br>
생성된 post를 받아보는 과정이다. 첫 번째와 마지막 object를 보면 둘 다 1번 id가 작성한 것을 볼 수 있다.
![poby](/images/poby.png)<br>

필터를 사용하여 객체를 가져오는~~ 모습.
![filter](/images/filter.png)<br>

# 3주차 과제 회고

일단 시간이 너무 촉박했다.
그래서 퀄리티가 좀 떨어지는 것 같다...
그리고 원래 모델을 설계하는 것을 잘 못하기도 했고 이번이 두 번째라
어느 정도 처음보다 낫겠지 하고 자신감이 있었는데, 자만하면 안된다...

ERD 툴을 처음 써 봐서 그것에 관해서도 공부를 했어야 했고,
Profile, User의 one to one 관계에 대해서 서로의 테이블을 참조하는 과정이 어려웠었고,
과제를 진행하면서 만난 오류들도 많아서 많이 힘들었다.

행 삭제, auto increment key 초기화 <br>
테스트 할 때 너무 필요 없는 값들이 많이 들어가서 삭제하고 primary key를 초기화해 주는데 사용했다.
[https://lightblog.tistory.com/151](https://lightblog.tistory.com/151) <br>
[https://amaze9001.tistory.com/28](https://amaze9001.tistory.com/28) <br>

shell 안에서 save() 안했을 경우 오류 <br>
save()를 하지 않으면 다음과 같이 오류가 생겼었다.
[https://stackoverflow.com/questions/33838433/save-prohibited-to-prevent-data-loss-due-to-unsaved-related-object](https://stackoverflow.com/questions/33838433/save-prohibited-to-prevent-data-loss-due-to-unsaved-related-object)
