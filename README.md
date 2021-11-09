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

# 4주차 - DRF1 : Serializer

## 수행해야 할 과제

- 데이터 삽입
- 모든 데이터를 가져오는 API 만들기
- 새로운 데이터를 create하도록 요청하는 API 만들기

## 과제 수행기

### 시작에 앞서

우선 과제를 수행하기 전에 백엔드 천재 **'승우'** 의 조언을 바탕으로
github action에 빨간불을 초록불로 바꿨다.

그 후, 해당 과제를 수행하기 위해 필요한 패키지들을 `pip`를 통해 설치하였고,
새로운 패키지가 설치되었으니 `requirements.txt` 를 update해 주었다.

### 작성한 model 을 바탕으로 serializer 만들기

`serializer` 의 경우 어렵지 않게 작성했다. 
`ModelSerializer` 클래스를 사용하여 미리 `models.py`에 정의한 모델들을 가져왔다.
정말 무지성으로 코드를 따라했다. 필드를 전부 다 가져오려면 '__all__' 이렇게 하면 된다고 한다.
`Nested Serializer`라고 무섭게 생긴 이름을 가진 친구도 있는데, 실제로는 별로 안무섭다. (근데 다시 생각해 보니 조금 무섭다.)
그냥 동일하게 사용하면 된다. 가져오고 싶은 모델을 한 번 더 가져오는 차이?

`Serializer Method Field` 의 경우 `Nested serializer`와 유사하게 serializer의
field로 relationship을 가지는 다른 모델의 필드를 가져올 수 있다. 쉽게 말해 foreign key를
가지는 다른 테이블을 참조할 수 있다고 이해했다. 

사실 이 기능은 `Nested serializer`만을 사용하여 구현할 수 있다. 
그냥 새로 serializer를 만들고, 거기서 가져올 필드를 명시한 후, 그 `serializer`를 
가져올 field에 적어주면 참조가 된다.

나는 여기서 의문을 가졌다. '같은 기능인데, 왜 굳이 `Serializer Method Field`라는 걸 만들었을까?'
일단 차이점을 생각해 보았다.

### 일반적인 Nested serializer는 언제 사용할까?
 - 아예 class로 만들어 버리면 다른 필드에서 동일하게 사용할 수 있다.
 - 어떤 부분에서 문제가 생기거나 수정해야 한다면, 이 `serializer` 를 참조한 모든 곳이 바뀌므로, 일일히 번거롭게 수정할 필요가 없다. 

### Method Field라는 것은 언제 사용할까?
 - 여러 곳에서 참조해서 사용해야 하는데, 참조해야 하는 필드가 매번 다른 경우.
 - 오직 딱 한 곳에서만 사용해서 커스터마이징하여 원하는 값만 가져오고 싶을 경우.

내가 생각한 사용해야 하는 곳은 다음과 같다. 혹시 추가로 덧붙이거나, 틀린 부분이 있다면 말해주길 바랍니다.

### View, url

view를 만들고 url 설정을 해서 실제로 되는지 확인하기 위한 과정이다.
내가 정의하고 싶은 method들을 로직에 맞게 적으면 된다.
rest하게 잘 적어보도록 하자.
우선 예시 코드의 경우 `if`와 `elif`로 큰 블럭이 나뉘어져 있는데,
사실 `if` 두 개의 블럭으로 나누어도 되지 않았을까 싶어서 그렇게 했지만, 
굳이 별 차이가 없다고 느껴서 다시 원래대로 되돌렸다.

url의 경우 path 설정을 잘 해야 한다. 이름만 보고 어떤 동작을 하는지 알 수 있도록.
나의 경우는 `path('api/')`로 설정했고, api 내부에 모아 놓을 것 같다.
그리고 상위 url config를 잊지 않고 꼭 해주어야 하는데, 그렇지 않으면 
10월 14일의 나처럼 '왜 안되지' 라는 멍청한 생각을 할 수도 있다.

### 결과 확인하기

모든 유저의 정보를 가져왔다.
![get_user](/images/get_user.png)<br>

#### 1. DRF + 브라우저 활용

'rest_framework'를 `pip`로 설치하고, `INSTALLED_APP`에 추가했음에도 불구하고
왜인지 장고에서 제공해준다는 기능을 사용하지 못했다. 검색도 많이 해 봤는데 마땅한 해결책을 찾을 수 없었다.
경험상 뭔가 이런 문제는 매우 사소한 것을 놓친 건데, 경로가 잘못되었나...? 잘 모르겠다. 그냥 postman 써야겠다... 

#### 2. Postman 활용

postman은 정말 잘 만든 어플리케이션이다. 쓸 때마다 맘에 든다. 아이콘도 귀여운 것 같다. 
원래 코딩의 가장 어려운 부분이 네이밍이듯이, REST API의 이름을 짓는 것도 어렵다.
그래도 최대한 잘 지어보려고 노력했다.

두 개의 post method를 사용했는데, 새로운 user를 추가하는 것과 새로운 post(게시물)을 추가하는 API를 만들었다.
그리고 모든 유저 조회, 모든 게시물 조회, 해당 유저의 모든 게시물 조회를 하는 API를 만들었다.

### 과제

#### 데이터 삽입

1. ORM 쿼리 또는 django 관리자를 통해 모델에 적절한 **데이터 3개**를 넣은 후 그 결과 화면을 캡쳐해주세요.
2. **README.md**의 `**모델 선택 및 데이터 삽입**` 아래쪽에 선택한 모델의 구조와 데이터 삽입 결과를 캡쳐한 모습을 보여주세요.

*어드민 페이지 예쁘게 보기* <br>
원래는 그냥 기본으로 제공하는 어드민 페이지를 썼었다. 그냥 `admin.py`에 모델만 추가해주면 된다.
근데 경준이가 한 거 보니까 예쁘게 잘 해놔서 나도 저렇게 해야겠다 싶어서 따라했다.

[1번](https://teamlab.github.io/jekyllDecent/blog/tutorials/Django-Admin-%EC%BB%A4%EC%8A%A4%ED%84%B0%EB%A7%88%EC%9D%B4%EC%A7%95) <br>
[2번](https://hckcksrl.medium.com/django-admin-%EC%BB%A4%EC%8A%A4%ED%84%B0%EB%A7%88%EC%9D%B4%EC%A7%95-c933e68a205) <br>
[공식깃헙링크](https://github.com/silentsokolov/django-admin-rangefilter) <br>

*before*
![before admin setting](/images/adminbefore.png)<br>

*after*
![after admin setting](/images/adminafter.png)<br>


#### 모든 데이터를 가져오는 API 만들기

1. - **URL**: `api/items/`(URL은 그대로 사용하시기보단 자신의 모델에 맞는 이름을 사용해주세요!)
2. Method: `GET`

모든 user를 가져오는 api 실행.<br>
![get all user](/images/getuser.png)<br>

```json
[
    {
        "id": 1,
        "photo": "",
        "username": "pororo",
        "password": "password",
        "last_name": "뽀",
        "first_name": "로로",
        "email": "pororo@gmail.com"
    },
    {
        "id": 4,
        "photo": "",
        "username": "poby",
        "password": "qwer",
        "last_name": "포",
        "first_name": "비",
        "email": "poby@gamil.com"
    },
    {
        "id": 5,
        "photo": "",
        "username": "Eddy",
        "password": "1qaz",
        "last_name": "",
        "first_name": "",
        "email": ""
    },
    {
        "id": 7,
        "photo": null,
        "username": "nowkim",
        "password": "pbkdf2_sha256$180000$hDkcHgUBBFG3$L1TBZXUdAzeUtveERN3dysvn+7QJpm0FuuqgnxuItHA=",
        "last_name": "",
        "first_name": "",
        "email": "peterhyunjae@naver.com"
    }
]
```

모든 post와 user의 모든 post를 가져오는 api를 만들었다.
실제로 해당 유저의 모든 포스틀 불러오는 api는 필수로 있어야 한다고 생각했기 때문에 추가로 구현하게 되었다.
모든 포스트와 해당 유저의 모든 포스트를 가져오는 것은 전체를 가져온다는 점에서 동일하다고 판단하여,
새로운 url을 만들기보다 기존의 모든 포스트를 가져오는 url을 활용해야겠다고 생각했다.

```python
# urls.py
urlpatterns = [
    path('users/', user_list),
    path('posts/', post_list),
    # path('posts/<int:user_id>', post_list),
]
```

원래 url 구성을 `posts/` 대신에 주석처리 되어있는 친구를 사용했는데,
저렇게 구성하면 필수로 id를 받아야 하는 문제가 있어서 (parameter를 강제한다.)
url은 그대로 두고 다른 방법을 생각해야 했다.

[여기를](https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get) 참고하였다.
그래서 `/?q=''` 이런 식으로 url parameter에서 원하는 값을 찾을 수 있도록 하였다.

```python
# views.py
def post_list(request):
    if request.method == 'GET':
        queryset = request.GET.get('q', None)
        if queryset is not None:
            posts = Post.objects.filter(user__user_id=queryset).all()
            serializer = PostSerializer(posts, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return JsonResponse(serializer.data, safe=False)
```

결과는 성공. <br>
![get all user post](/images/get_all_users_post.png)<br>
```json
[
    {
        "id": 1,
        "images": [],
        "videos": [],
        "post_likes": [],
        "post_comments": [],
        "created_at": "2021-10-08T00:21:02.539778+09:00",
        "updated_at": "2021-10-28T20:52:51.599098+09:00",
        "text": "post1"
    },
    {
        "id": 4,
        "images": [],
        "videos": [],
        "post_likes": [
            {
                "id": 1,
                "created_at": "2021-10-28T23:36:33.711390+09:00",
                "updated_at": "2021-10-28T23:36:33.711458+09:00",
                "user": 2,
                "post": 4
            }
        ],
        "post_comments": [],
        "created_at": "2021-10-08T00:21:16.423336+09:00",
        "updated_at": "2021-10-28T20:52:51.599098+09:00",
        "text": "poby is the best"
    },
    {
        "id": 5,
        "images": [],
        "videos": [],
        "post_likes": [
            {
                "id": 2,
                "created_at": "2021-10-28T23:36:57.451609+09:00",
                "updated_at": "2021-10-28T23:37:03.801624+09:00",
                "user": 4,
                "post": 5
            },
            {
                "id": 3,
                "created_at": "2021-10-28T23:39:12.938142+09:00",
                "updated_at": "2021-10-28T23:39:12.938178+09:00",
                "user": 3,
                "post": 5
            }
        ],
        "post_comments": [
            {
                "id": 1,
                "created_at": "2021-10-28T23:37:54.359054+09:00",
                "updated_at": "2021-10-28T23:37:54.359119+09:00",
                "text": "공부해 뽀로로야",
                "user": 3,
                "post": 5
            },
            {
                "id": 2,
                "created_at": "2021-10-28T23:38:09.650375+09:00",
                "updated_at": "2021-10-28T23:38:09.650413+09:00",
                "text": "나도 노는게젤좋긴하지만",
                "user": 3,
                "post": 5
            }
        ],
        "created_at": "2021-10-28T23:35:14.699675+09:00",
        "updated_at": "2021-10-28T23:35:14.699766+09:00",
        "text": "노는게젤좋아"
    }
]
```

#### 새로운 데이터를 create하도록 요청하는 API 만들기

1. **URL**: `api/items/`
2. **Method**: `POST`
3. **Body**: `{"필드명": 필드값, ... }`

새로운 유저를 만드는 api와 새로운 post를 만드는 api를 만들었다.

```python
# views.py
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            u = User.objects.get(username=data['username'])
            p = Profile.objects.create(user=u, photo=data['photo'])
            p.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
```
그냥 `serializer.save()` 할 경우 auth_user에만 저장되고, profile에는 저장이 되지 않는 것을 발견하여
새로 만들어진 유저 객체를 가져와서 profile에도 새로 만들어 주었다.
사실 이렇게 하는게 아닌 것 같은데 어떻게 수정해야할지 모르겠어서 저렇게 했다.

post를 새로 만드는 api의 경우도 마찬가지로 user 객체가 필요한데,
이것도 새로 user_id를 통해 user 객체를 얻어와야 하는건가 했는데, 아무래도 아닌 것 같다.

로그를 보면 serializer까지는 잘 생성되는데, 그 이후에 <br>
'IntegrityError' <br>
'(1048, "Column 'user_id' cannot be null")' <br>
이런 오류가 나온다. 

그래서 결과적으로 새로운 post를 생성하는 api는 구현을 하지 못했다.

일단 유저 생성 결과 화면을 첨부한다.<br>
![createuser](/images/createuser.png)<br>
![result](/images/result.png)<br>


# 5주차 - DRF2 : API View

## 기본 자료 외에 참고한 사이트

[Django REST Framework-CBV](https://inma.tistory.com/88)
[Capturing URL parameters in request.GET](https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get)
[request에 대한 예외 처리하기](https://programmers.co.kr/learn/courses/6/lessons/515)
[HTTP 상태 코드](https://developer.mozilla.org/ko/docs/Web/HTTP/Status)

## 과제 리뷰

### 전체 데이터를 가져오는 API

#### 모든 유저 리스트를 가져오는 API

![get_all_user](/images/get_all_user.png)<br>
#### 모든 post 를 가져오는 API

![get_all_post](/images/get_all_post.png)<br>

### 특정 데이터를 가져오는 API

#### 특정 유저의 Profile을 가져오는 API

**올바른 요청일 경우** <br>
![get_specific_user](/images/get_specific_user.png)<br>
**존재하지 않는 id로 요청할 경우** <br>
![get_specific_user_invalid](/images/get_specific_user_invalid.png)<br>

#### 특정 유저의 전체 post를 가져오는 API

**올바른 요청일 경우** <br>
![get_all_post_specific_user](/images/get_all_post_specific_user.png)<br>
**존재하지 않는 id로 요청할 경우** <br>
![get_all_post_specific_user_invalid](/images/get_all_post_specific_user_invalid.png)<br>

### 새로운 데이터를 생성하는 API

#### 새로운 유저를 생성하는 API

**올바른 요청일 경우** <br>
![post_user](/images/post_new_user.png)<br>
**이미 존재하는 사용자의 이름으로 요청할 경우** <br>
![post_user_invalid](/images/post_user_invalid.png)<br>

#### 새로운 POST 를 생성하는 API

**올바른 요청일 경우** <br>
![post_post](/images/post_post.png)<br>
**존재하지 않는 사용자로 요청할 경우** <br>
![post_post_invalid](/images/post_post_invalid.png)<br>

### 특정 데이터를 업데이트하는 API

![put_specific_post](/images/put_specific_post.png)<br>

### 특정 데이터를 삭제하는 API
![delete_specific_post](/images/delete_specific_post.png)<br>

### 공부한 내용 정리

새로 알게 된 점 : <br>
 - url pattern 을 잘 설계하는 것이 직관적이고 관리하기 쉬운 API를 만드는 길이다.
 - 상태 코드를 API의 목적에 맞게 잘 사용하자.
 - CBV는 FBV를 완벽하게 대체할 수 없다. 상황에 따라 잘 사용하자.
 - 예외 처리나 오류 핸들링은 필수적이다. 추후에 로그인이나 인증 기능이 포함되면 그에 따른 분기 처리가 필수적일 것이다.

정리 하고 싶은 개념 : <br>
예외 처리가 특히 중요한 것 같다. object를 찾지 못했을 때, list가 비어 있을 때, 사용자에 대한 인증이 되어 있지 않을 때, <br>
데이터를 요청한 뒤 비동기적으로 처리해야 하는 로직일 때 등등 그에 따른 예외 처리가 필수적이라고 느꼈고,<br>
이번에 새로 알게 된 개념이나 중요한 개념을 정리하기보다 어떤 언어를 사용하더라도 근본이 되는 것은 이러한 문제라고 판단하였기 때문에<br>
이렇게 comment를 남깁니다.

### 간단한 회고

이번 주 수, 목요일에 아예 코드를 건드릴 시간이 없을 것 같아서 미리 제출합니다.<br>
그에 따라 코드의 퀄리티가 낮을 수도 있고,<br> 
완벽한 예외 처리를 구현하지는 못했습니다. <br>
(그러나 당장은 중요하지 않다고 판단하여 제출합니다.)<br>
평소에 하지 못했던 1등을 처음으로...?