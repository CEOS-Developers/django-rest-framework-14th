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
| 속도 저하(리소스 분할 및 퍼포먼스 오버헤드), CI/CD 어려움 | 빠른 속도, 효율성, 이식성 좋음 |

![image](https://user-images.githubusercontent.com/77983074/135456938-32daee35-ecf6-409e-9048-d2fb63fd435e.png)

참고자료: [https://www.redhat.com/ko/topics/containers/containers-vs-vms]

**\- docker 구조**

>1. docker client와 docker server(engine)
>
>2. docker image
>
>  -**Dockerfile**: 내가 생성하고자 하는 컨테이너, 그 환경을 만들기 위해 필요한 패키지를 설치하고 동작하기 위한 설정을 담은 파일. Dockerfile을 빌드하면 자동으로 Docker image가 생성됨. 
>
>  -**Docker Image**: 서비스 운영에 필요한 서버 프로그램, 소스 코드, 컴파일된 실행 파일 등을 묶은 형태로 컨테이너를 생성하는 템플릿 역할. <- 이미지는 변경 불가능. 컨테이너의 비저장성은 >컨테이너 내용을 일관되게 한다.
>
>3. docker registry: docker image를 저장하는 repostory. docker hub.
>
>4. docker container: docker image를 run하여 docker container를 생성한다. 

**\- docker를 쓰는 이유?**


>**1. control이 쉽다.** OS 위의 사용자 단에 client를 제공하여 CLI로 쉽게 컨트롤 할 수 있다.
>
>**2. 경량화.** 커널을 직접 컨트롤하는 container 기반 가상화로 리소스와 기능이 제한되어 있는 환경에서도 배포 가능하도록 경량화된 애플리케이션을 제공한다.
>
>**3. CI/CD.** 지속적인 통합과 자동 배포를 진행하기 위해 필요한 서비스 운영 환경에 대한 패키징을 Docker image를 통해 구현 가능하다. 

<details>
<summary>CI/CD?</summary>
  
<div markdown="1">
<br>
  <b>CI(Continuous Integration)</b>: 지속적 통합. 새로운 소스코드의 빌드, 테스트, 병합. MSA(Micro Service Architecture) 환경에서 CI의 적용은 기능 충돌 방지 등의 benefit을 제공해줄 수 있다. 
  
  <b>CD(Continuous Delivery/Deployment)</b>: 지속적 배포(서비스 제공). 변경 사항이 고객의 production 환경까지 릴리즈 되는 것.
  
![image](https://user-images.githubusercontent.com/90975718/135703973-2c53a451-7328-4a66-82a5-842b4780166c.png)
  
  <출처: redhat>

</div>
</details>

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
>기본적으로 도커 컨테이너들은 각각 격리된 환경에서 실행되므로 별도의 옵션을 지정하지 않으면 다른 컨테이너의 존재를 알 수 없다. 따라서 반드시 데이터베이스 컨테이너를 실행한 다음에 앱 컨테이너를 실행하며 db 컨테이너를 연결해줘야 한다. 그렇지 않으면 앱 컨테이너에서 데이터베이스 컨테이너를 찾을 수 없다. -> 만약 앱컨테이너를 먼저 실행했다면 종료하고 순서를 맞춰 다시 실행해야하는 불편함이 존재.

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

>하나의 프로젝트에서 사용하는 정적 파일들(css, image, javascript 등)은 여기저기에 분산되어 있기 때문에 요청이 들어왔을 때 필요한 정적 파일을 돌려주려면 많은 경로를 탐색해야 하므로 매우 비효율적이다. 그래서 사용하는 모든 정적 파일을 하나의 경로로 모아주는 작업이 필요하다. 개발 중에는 runserver를 하면 이 작업을 알아서 해주지만, 실제로 Production 환경에서는 Apache나 Nginx와 같은 웹서버를 사용해야 하므로 직접 모아주는 작업을 위해 collectstatic 명령을 사용한다. 

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

***

## **1\. 모델 설계**
  
![image](https://user-images.githubusercontent.com/90975718/136202036-9814e47f-c57e-4d92-b3e5-50a3a5d8d849.png)

#### **1) User: Django에서 지원하는 AbstractBaseUser를 상속** 

-   AbstractBaseUser: password, last\_login, is\_active 필드 제공. django가 제공해주는 필드를 이용하면서 사용자 정의 field 추가를 위해 사용. (AbstractUser보다 제공 필드가 적어 더 유연성이 있다)
-   login id로 username이 아닌 nickname 사용. (USERNAME\_FIELD='nickname'으로 변경. 애초에 username을 nickname 처럼 받아써도 되겠으나 헷갈리지않도록 구분했다.)
-   공식문서: [https://docs.djangoproject.com/en/dev/topics/auth/customizing/#a-full-example](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#a-full-example) 
-   is\_active, is\_admin 필드는 django user 모델의 필수 필드.

>\- nickname: 처음 계정 생성 시 쓰는 userid(중복 불가값으로 unique)
>
>\- username: user의 이름
>
>\- is\_professional: professional 계정인지 확인. default 값 False.
>
>\- is\_private: 비공개 계정인지 확인. default 값 False. 
>
>\- phone\_num: 핸드폰 번호
>
>\- email: 이메일
>
>\- password: 비밀번호
>
>권한 설정
>
>\- is\_active: 활성 계정인지 확인. default 값 True.
>
>\- is\_staff: admin 접근 가능 계정인지 확인. default 값 False.
>
>\- is\_superuser: superuser인지 확인. default 값 False.
>
>\- is\_admin: admin인지 확인. default 값 False. 

#### **2) Profile: User 모델과 1:1로 연결해 사용자 세부 정보를 저장**

>\- id: PK
>
>\- user\_id: FK(User)
>
>\- image: 프로필 이미지
>
>\- info: 소개글
>
>\- website: 웹사이트
>
>\- profile\_name: 프로필 설정 이름
>
>\- gender: 성
>
>\- birth\_date: 생일

#### **3) Post: User 모델과 1:N의 관계.**

>\- id: PK
>
>\- content: 내용
>
>\- created\_time: 작성 시간
>
>\- updated\_time: 수정 시간
>
>\- comment\_available: 댓글 작성 가능한지. default 값 True.
>
>\- author\_id: FK(User)
>
>\- location: 위치 

#### **4) Comment: User, Post와 1:N의 관계**

>\- id: PK
>
>\- author\_id: FK. 댓글 작성자 (erd에 author 잘못들어감)
>
>\- post\_id: FK(Post)
>
>\- created\_time: 작성 시간
>
>\- updated\_time: 수정 시간

#### **5) File: Post 모델과 1:N의 관계**

>\- id: PK
>
>\- file: image/vedio
>
>\- post\_id: FK(Post)

#### **6) Like: User, Post와 1:N의 관계**

>\- id: PK
>
>\- post\_id: FK(Post)
>
>\- user\_id: FK(User)

#### **7) Follow: Follower:Follwing = N:M의 관계**

>\- id: PK
>
>\- follower: FK
>
>\- following: FK

## **2\. ORM 테스트**

**1) Post 객체 조회, Follow 객체 조회**
  
![image](https://user-images.githubusercontent.com/90975718/136202400-76534447-6f04-4fa3-9747-6812e87eb37d.png)

\- related\_name 이용해서 likes(해당 user의 Like) , post\_likes(해당 post에 대한 Like) 조회

![image](https://user-images.githubusercontent.com/90975718/136202468-75db9c47-34d9-4766-acf7-05a0ddf98266.png)

\- related\_name 이용해서 user의 follwers(user를 follow하는 관계), followings(user가 follow하는 관계) 조회

![image](https://user-images.githubusercontent.com/90975718/136202543-a47f3642-68c3-4f99-89a4-f8ea154e5373.png)

**2) Filter 사용**

![image](https://user-images.githubusercontent.com/90975718/136202712-6102a69f-0e7d-434d-b89f-9f03afe034d5.png)

※ get()과 filter()의 차이

\- get()은 쿼리에 맞는 객체 하나만 반환. 쿼리에 맞는 결과가 없을 시 DoesNotExist 에러가 발생. 여러 객체가 조회되면 MultipleObjectsReturned 에러가 발생. 

\- 쿼리에 맞는 결과가 없다면

![image](https://user-images.githubusercontent.com/90975718/136202788-e5476fd6-cf93-425e-ab62-112682fa2df5.png)

\- 여러 객체가 조회된다면

![image](https://user-images.githubusercontent.com/90975718/136202869-6c7f65fd-b652-4a93-ae5f-c28cafdc3a95.png)

\- filter()는 새로운 쿼리셋 생성 후, 필터 조건에 부합하는 객체들을 넣은 후 리턴. (필터 조건에 부합하는 객체가 없다면 빈 쿼리셋 반환)

\- 여러 객체 조회 시

![image](https://user-images.githubusercontent.com/90975718/136202970-4dd40d58-3aca-496d-b361-b6d596084451.png)

\- 빈 객체 조회 시

![image](https://user-images.githubusercontent.com/90975718/136203007-90a0633d-73ea-4385-ad28-b7d89a10af3f.png)

3\. 간단한 회고

>django의 user 모델 확장 방법을 찾아보면 4가지가 나오는데, 아는 게 없으니 이것저것 다 사용해보자!는 마음으로 섞어서 사용했다. AbstractBaseUser을 이용한 custom user도 만들고 추가적인 내용인 Profile 모델에 넣어 onetoone으로 연결해줬는데 두개를 섞어쓴 것에 대해서는 딱히 별 의미 없다... custom user에 대해서는 계속 찾아봤는데도 아직 감이 잘 안온다. 그래서 프로젝트 중간에 custom을 하려고 하면 migration 충돌 때문에 골치아프다고 하니 혹시 몰라서 처음부터 custom user를 쓰기로 했다.(django에서도 권장하는 방법이라고...?) User 제공 필드도 써보려고 다 넣다보니 filed가 너무 많아져서 Profile로 세부 사항은 분리를 해야지 정도로 생각한 것 같다. 나중에 데이터베이스를 드롭하거나 모델을 뒤집어 엎어야 하는 일만 안생겼으면 좋겠다..

***
## DRF1: Serializer
  
### **모델 선택 및 데이터 삽입**

선택한 모델: **Post 모델**. (Post 모델과 1:N 관계를 갖는 Comment, Like, File 모델)

```
class Post(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=500, blank=True)
    comment_available = models.BooleanField(default=True)
    location = models.CharField(max_length=150, null=True, blank=True)

class Comment(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

class File(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_files')
    file = models.FileField(upload_to='post_files')
    type = models.BooleanField(default=0)  # 0:image, 1:video

class Like(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
```

데이터 삽입 결과
  
![image](https://user-images.githubusercontent.com/90975718/136799423-5018e5d4-a01b-4974-975f-94e7961df55b.png)


### **Serializer**

-   Nested Serializer로 post와 post\_likes, comments, post\_files 관계 표현.
-   Serializer method field로 author(User 모델)의 field인 nickname을 가져와 사용.

```
class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    post_likes = LikeSerializer(many=True, read_only=True)   # read_only: 요청 파라미터에 포함되지 않음.
    comments = CommentSerializer(many=True, read_only=True)
    post_files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['author_name', 'author', 'content', 'created_date', 'updated_date', 'post_likes', 'comments', 'post_files']

    def get_author_name(self, obj):
        return obj.author.nickname
```


### **모든 데이터를 가져오는 API 만들기**

-   URL: api/posts/
-   METHOD: GET

![image](https://user-images.githubusercontent.com/90975718/136799559-61866a1d-b85b-4979-a8c9-11f76fb028b4.png)

**Response**

```
[
    {
        "author_name": "pika_so_hee",
        "author": 3,
        "content": "그림 그리는 중~",
        "created_date": "2021-10-05T19:51:55.927811+09:00",
        "updated_date": "2021-10-05T19:51:55.927811+09:00",
        "post_likes": [
            {
                "id": 1,
                "created_date": "2021-10-11T14:26:53.791390+09:00",
                "updated_date": "2021-10-11T14:26:53.972385+09:00",
                "user": 1,
                "post": 1
            },
            {
                "id": 2,
                "created_date": "2021-10-11T14:26:53.791390+09:00",
                "updated_date": "2021-10-11T14:26:53.972385+09:00",
                "user": 2,
                "post": 1
            },
            {
                "id": 4,
                "created_date": "2021-10-11T14:26:53.791390+09:00",
                "updated_date": "2021-10-11T14:26:53.972385+09:00",
                "user": 3,
                "post": 1
            }
        ],
        "comments": [],
        "post_files": []
    },
    {
        "author_name": "heryunzzx",
        "author": 1,
        "content": "시험 일주일 전~",
        "created_date": "2021-10-05T19:52:16.109273+09:00",
        "updated_date": "2021-10-05T19:52:16.109273+09:00",
        "post_likes": [
            {
                "id": 3,
                "created_date": "2021-10-11T14:26:53.791390+09:00",
                "updated_date": "2021-10-11T14:26:53.972385+09:00",
                "user": 1,
                "post": 2
            },
            {
                "id": 5,
                "created_date": "2021-10-11T14:26:53.791390+09:00",
                "updated_date": "2021-10-11T14:26:53.972385+09:00",
                "user": 2,
                "post": 2
            }
        ],
        "comments": [],
        "post_files": []
    },
    {
        "author_name": "hyejinnnnyyyy",
        "author": 2,
        "content": "노래 듣는 중~",
        "created_date": "2021-10-05T19:52:33.103979+09:00",
        "updated_date": "2021-10-05T19:52:33.103979+09:00",
        "post_likes": [
            {
                "id": 6,
                "created_date": "2021-10-11T14:26:53.791390+09:00",
                "updated_date": "2021-10-11T14:26:53.972385+09:00",
                "user": 3,
                "post": 3
            }
        ],
        "comments": [],
        "post_files": []
    },
    {
        "author_name": "hyejinnnnyyyy",
        "author": 2,
        "content": "나는 휴학생~",
        "created_date": "2021-10-05T19:52:52.716996+09:00",
        "updated_date": "2021-10-05T19:52:52.716996+09:00",
        "post_likes": [],
        "comments": [],
        "post_files": []
    },
    {
        "author_name": "pika_so_hee",
        "author": 3,
        "content": "실습 나가는 길~",
        "created_date": "2021-10-05T19:53:08.781585+09:00",
        "updated_date": "2021-10-05T19:53:08.781585+09:00",
        "post_likes": [],
        "comments": [
            {
                "author_name": "heryunzzx",
                "author": 1,
                "post": 5,
                "content": "헐 벌써?",
                "created_date": "2021-10-05T19:55:05.360616+09:00"
            },
            {
                "author_name": "hyejinnnnyyyy",
                "author": 2,
                "post": 5,
                "content": "오마이갓",
                "created_date": "2021-10-05T19:56:16.509982+09:00"
            },
            {
                "author_name": "pika_so_hee",
                "author": 3,
                "post": 5,
                "content": "시간 빠르다~",
                "created_date": "2021-10-05T19:57:03.714520+09:00"
            }
        ],
        "post_files": []
    },
    {
        "author_name": "heryunzzx",
        "author": 1,
        "content": "drfdrfdrf",
        "created_date": "2021-10-11T16:19:28.760878+09:00",
        "updated_date": "2021-10-11T16:19:28.760878+09:00",
        "post_likes": [],
        "comments": [],
        "post_files": []
    },
    {
        "author_name": "heryunzzx",
        "author": 1,
        "content": "시험기간이야~~",
        "created_date": "2021-10-11T17:36:09.038490+09:00",
        "updated_date": "2021-10-11T17:36:09.038490+09:00",
        "post_likes": [],
        "comments": [],
        "post_files": []
    }
]
```


### **새로운 데이터를 Create하도록 요청하는 API 만들기**

-   URL: api/posts/
-   Method: POST
-   Body:

{

    "author": 2,

    "content": "밖에 비가 와서 짜증나"

}

![image](https://user-images.githubusercontent.com/90975718/136799740-c84a253f-9667-4fee-9dcb-ede45a8b60b5.png)

**Response**

```
{
    "author_name": "hyejinnnnyyyy",
    "author": 2,
    "content": "밖에 비가 와서 짜증나",
    "created_date": "2021-10-11T22:30:20.357470+09:00",
    "updated_date": "2021-10-11T22:30:20.357470+09:00",
    "post_likes": [],
    "comments": [],
    "post_files": []
}
```

***
### User api 추가
  
- user 정보와 추가 profile 정보 입력 후 계정이 생성될 수 있도록 create() 함수 추가
```
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
```
  
-   URL: api/users/
-   METHOD: Post
-   Body:  
  
```
{
    "nickname": "testuser3",
    "username": "testuser3",
    "password": "password",
    "profile":{
        "info":"hi im a testuser3.",
        "profile_name":"testuser3"
    }
}  
```
**Response**
  
```
{
    "nickname": "testuser3",
    "username": "testuser3",
    "password": "password",
    "email": null,
    "profile": {
        "id": 8,
        "image": null,
        "info": "hi im a testuser3.",
        "profile_name": "testuser3"
    },
    "followers_count": 0,
    "followings_count": 0,
    "posts_count": 0,
    "posts": [],
    "followers": [],
    "followings": []
}
```
  
-   URL: api/users/
-   METHOD: GET
  
**Response**
```
[
    {
        "nickname": "heryunzzx",
        "username": "yoonji",
        "password": "password",
        "email": "str@ewhain.net",
        "profile": {
            "id": 1,
            "image": null,
            "info": "hi i'm yoonji",
            "profile_name": "yoonji"
        },
        "followers_count": 0,
        "followings_count": 2,
        "posts_count": 3,
        "posts": [
            {
                "author_name": "heryunzzx",
                "author": 1,
                "content": "시험 일주일 전~",
                "created_date": "2021-10-05T19:52:16.109273+09:00",
                "updated_date": "2021-10-05T19:52:16.109273+09:00",
                "comments_count": 0,
                "likes_count": 2,
                "post_likes": [
                    {
                        "id": 3,
                        "created_date": "2021-10-11T14:26:53.791390+09:00",
                        "updated_date": "2021-10-11T14:26:53.972385+09:00",
                        "user": 1,
                        "post": 2
                    },
                    {
                        "id": 5,
                        "created_date": "2021-10-11T14:26:53.791390+09:00",
                        "updated_date": "2021-10-11T14:26:53.972385+09:00",
                        "user": 2,
                        "post": 2
                    }
                ],
                "comments": [],
                "post_files": []
            },
            {
                "author_name": "heryunzzx",
                "author": 1,
                "content": "drfdrfdrf",
                "created_date": "2021-10-11T16:19:28.760878+09:00",
                "updated_date": "2021-10-11T16:19:28.760878+09:00",
                "comments_count": 0,
                "likes_count": 0,
                "post_likes": [],
                "comments": [],
                "post_files": []
            },
            {
                "author_name": "heryunzzx",
                "author": 1,
                "content": "시험기간이야~~",
                "created_date": "2021-10-11T17:36:09.038490+09:00",
                "updated_date": "2021-10-11T17:36:09.038490+09:00",
                "comments_count": 0,
                "likes_count": 0,
                "post_likes": [],
                "comments": [],
                "post_files": []
            }
        ],
        "followers": [],
        "followings":[
            {
                "follower": "heryunzzx",
                "following": "hyejinnnnyyyy"
            },
            {
                "follower": "heryunzzx",
                "following": "pika_so_hee"
            }
        ]
    },
    
    ...중략...
]
```
  
>user의 save() 실행 이후 profile이 db에 저장되지 않는다는 것을 뒤늦게 깨닫고 django가 제공하는 signals의 post_save() 기능을 사용하여 profile이 자동 생성 및 저장되도록 수정하였다. 근데 serializer에서도 create() 함수를 만들어 profile을 저장하다보니 django.db.utils.IntegrityError: (1062, "Duplicate entry '9' for key 'api_profile.user_id'") 오류가 발생했다. db에는 저장이 되긴 하는데, 똑같은 정보를 중복으로 저장하려고 시도하나보다... post_save만 남기면 Write an explicit `.create()` method for serializer `api.serializers.UserSerializer`, or set `read_only=True` on nested serializer fields. 라는 error가 발생한다. post api도 comments count와 likes count를 추가로 제공하도록 수정했다.
  
  
