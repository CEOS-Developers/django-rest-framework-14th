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
    * 웹 응용프로그램 서버에 리버스 프록시(Nginx)를 두는 이유는 요청 에 대한 버퍼링이 있기 때문이다. 프록시 서버를 둠으로써 요청을 배분하는 역할을 한다.
  
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


# 모델링과 Django ORM

## 인스타그램 모델링
### 인스타그램 erd
![모델링erd](https://user-images.githubusercontent.com/79985974/136395720-bc89cc3f-c2d4-4e3b-accd-3c5d6e0382ce.PNG)

ERD 작성할때 mysql에서 테이블 칼럽을 조회하면 더 자세한 정보들을 알 수있어 참고하기 좋았다!
![참고](https://user-images.githubusercontent.com/79985974/136396776-1258f7b2-8a65-4161-a9e9-d050da08bab2.PNG)

### Profile
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40, unique=True)
    introduction = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="image")

    def __str__(self):
        return self.nickname

```
1. Profile 모델은 User 모델과 1:1관계로 설정    
2. 사용자의 프로필 이미지는 ImageField()을 이용하여 지정   
3. null, blank 둘다 기본값이 False이나 introduction은 비어 있어도 되기 때문에 blank=True로 지정하여 필드가 폼(입력 양식)에서 빈 채로 저장되는 것을 허용
### Post, File
```python
class Post(BaseModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{} : {}'.format(self.author, self.title)

class File(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.FileField(upload_to="file") #media/file/ 아래에 저장

```
1. null=True는 필드의 값이 NULL(정보 없음)로 저장되는 것을 허용
2. 사진이나 영상을 업로드할때 FileField을 사용하였다
    * 먼저 settings에서 MEDIA_ROOT을 지정해줌으로서 해당 경로에 이미지나 영상이 저장된다.
    * 또한 upload_to 옵션을 사용하여 구체ㅎ적인 디렉토리를 지정해 줄 수 있다.
    
3. auto_now=True와 auto_now_add=True의 차이점
    * 수정일자 : auto_now=True 사용   
    auto_now=True는 django model 이 save 될 때마다 현재날짜(date.today())로 갱신된다.(갱신 가능)
   * 생성일자 : auto_now_add=True 사용
    auto_now_add=True는 django model 이 최초 저장 시에만 현재날짜(date.today())를 적용한다.(갱신 불가능)
   
### Comment
```python
class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(blank=False)

    def __str__(self):
        return '{} commented {} post'.format(self.writer, self.post.title)
```
### Follow
```python
class Follow(BaseModel):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return '{} -> {}'.format(self.follower.nickname, self.following.nickname)
```

### Like
```python
class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return '{} liked {}'.format(self.user.nickname, self.post.title)

```

## Django ORM 적용해보기
### DB tables
![db](https://user-images.githubusercontent.com/79985974/136397254-ba690348-4a64-45b3-a333-9bcd98b9ca40.PNG)

```shell
>>> from api.models import User, Profile, Post, Comment
>>> Profile.objects.create(user_id =2, nickname ='chaeri', introduction = 'heyyyyyyy')
<Profile: chaeri>
>>> User.objects.create(username='김초코',password='1111')
<User: 김초코>
>>> Profile.objects.create(user_id =3, nickname ='choco', introduction = '멍멍')
<Profile: choco>
>>> User.objects.create(username='세오스',password='2222')
<User: 세오스>
>>> Profile.objects.create(user_id =4, nickname ='ceos', introduction = '후후')
<Profile: ceos>
>>> Profile.objects.all()
<QuerySet [<Profile: chaeri>, <Profile: choco>, <Profile: ceos>]>
```
![user](https://user-images.githubusercontent.com/79985974/136398222-a51fe438-3e16-456f-96a5-5eaa0621fcd6.PNG)
![profile](https://user-images.githubusercontent.com/79985974/136398211-2cdec88f-8e57-4f88-99c9-3f8337b64dad.PNG)
```shell
>>> user1 = Profile.objects.get(nickname='chaeri')
>>> Post.objects.create(author=user1, title='first',content = '신기하다', like_num = 2)
<Post: first>
>>> Post.objects.create(author=user1, title='second',content = '모델링 어렵다....ㅠ', like_num = 4)
<Post: second>
>>> user2 = Profile.objects.get(nickname='choco')
>>> Post.objects.create(author=user2, title='배고파',content = '간식 줘', like_num = 5)
<Post: 배고파>

>>> Post.objects.filter(title='first') # 필터 함수 적용해보기
<QuerySet [<Post: first>]>

```
![post](https://user-images.githubusercontent.com/79985974/136398218-5c2a7bc5-4308-447e-b2f0-0703b4533886.PNG)


## 간단한 회고
venv 가상환경 진입부터 shell에서 orm까지 거의 대부분의 과정에서 오류가 나서 꽤나 힘들었다.     
오류를 하나 해결하면 또하나가 생겨나서 굉장히 지쳤지만 해결해나가보면서 DB도 직접 설계해보면서 erd도 만드는 게 굉장히 흥미로웠다.   
이번에 새로 사용해보는 것들이 너무 많아서 굉장히 익숙치 않았지만 앞으로 과제들을 더 수행하면서 실력이 늘 수 있었으면 좋겠다ㅎㅎ

* * *

# DRF1 - Serializer

## DRF이란?

Django 안에서 RESTful API 서버를 쉽게 구축할 수 있도록 도와주는 오픈소스 라이브러리이다.

![DRF](https://user-images.githubusercontent.com/79985974/140630389-21449dcb-1547-4680-98f5-9734edd863cf.PNG)

* HTTP 요청에 맞는 url patterns가 Views로 전달된다.
* Serializer의 도움으로 Views는 HTTP 요청을 처리하고 HTTP 응답을 반환한다.
* Serializer는 모델 객체를 serialize/deserialize 한다. 
   * serialize : 직렬화, 프로그램의 객체에 담긴 데이터를 외부파일에 문자열 형태로 전송
   * deserialize : 역직렬화, 외부 파일의 데이터를 프로그램 내의 객체로 읽어오는 것
* 모델에는 DB와 함께 CRUD 작업을 위한 필수 필드 및 동작이 포함되어 있다.

## Serializer

![serializer](https://user-images.githubusercontent.com/79985974/140630639-67ac46e7-a74a-4d94-a1fd-3ba126f0f7dc.PNG)

Serializer는 우리가 Django 에서 사용하는 파이썬 객체나 queryset 같은 복잡한 객체들을 REST API에서 사용할 json 과 같은 형태로 변환해주는 어댑터 역할을 한다.

Serializer를 만들 때, 각 필드를 하나하나 정의해 주어야 한다. 마치 모델을 다시 한 번 작성하는 것 같은 불편함이 있었다. 이 문제를 해결해 주는 것이 ModelSerializer이다.

## ModelSerializer
ModelSerializer는 크게 아래와 같은 3가지 기능을 제공한다. 주는 편리함이 워낙 크기에 Base Serializer보다 훨씬 생산성을 높일 수 있다.
 * 의존하고 있는 모델에 기반해서 Serializer 필드를 자동으로 만들어 준다
 * Serializer를 위한 validator 제공
 * .create(), .update() 함수 기본으로 제공하여 다시 만들 필요 없다.

### ModelSerializer 사용 방법
1. class Meta 작성

    * model = 모델명
    * fields = __all__, exclude, 직접 명시 ('id', 'name')
    * read_only_field = ['id']
2) serializer로 정의해 줘야 되는 필드

    * 추가하고 싶은 필드가 있을 경우, serializer.SerializerMethodField()로 정의해 준다.
    * ForeginKey로 연결된 필드가 있을 경우, Nested Serializer를 사용하여 ForeignKey로 연결된 필드의 pk를 가져온다.


## ORM을 통해 데이터 조회
```shell
>>> from api.models import User, Profile,Post, Comment, Like
>>> Post.objects.all()
<QuerySet [<Post: chaeri : first>, <Post: chaeri : second>, <Post: choco : 배고파>, <Post: ceos : 세오스>]>
>>> Comment.objects.all()
<QuerySet [<Comment: choco commented ceos post>, <Comment: chaeri commented ceos post>, <Comment: choco commented ceos post>]>
>>> Like.objects.all()
<QuerySet [<Like: chaeri liked 세오스>, <Like: choco liked 세오스>, <Like: ceos liked 세오스>]>
```

## Serializers
```shell
from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    writer_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['post', 'writer', 'content', 'created_at', 'updated_at', 'writer_nickname']


    def get_writer_nickname(self,obj):
        return obj.writer.nickname


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    post_like = LikeSerializer(many=True, read_only=True, source="like_set")
    post_comment = CommentSerializer(many=True, read_only=True, source="comment_set")
    
    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'author_nickname',
                  'created_at', 'updated_at', 'post_like', 'post_comment']

    def get_author_nickname(self, obj):
        return obj.author.nickname


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'introduction']
```
### 마주한 에러
처음 api를 테스트 했을 때 몇몇 데이터들이 넘어오지 않았다. 구글링 해보니 source argument를 넣어주지 않아서 그랬다.   

예를 들어 Post객체 하나를 생성해보면
```shell
p = Post.objects.get(pk=1)
```
이제 이 post와 관련된 댓글들의 queryset은 다음과 같이 될것이다.
```shell
Comment.objects.filter(post=p)
```
이를 장고는 다음과 같이 단순화 할 수 있다.
```shell
p.comment_set
```
따라서 drf는 필드 이름에서 모델 속성을 찾기 때문에 source argument를 사용하여 Serializer가 데이터를 가져올 위치를 지정해주어야 한다.


## 모든 데이터를 가지고 오는 API
 * URL: api/posts/
 * METHOD: GET

```json

[
    {
        "author": 4,
        "title": "first",
        "content": "신기하다",
        "author_nickname": "chaeri",
        "created_at": "2021-10-07T21:55:46.046656+09:00",
        "updated_at": "2021-10-07T21:55:46.047794+09:00",
        "post_like": [],
        "post_comment": []
    },
    {
        "author": 4,
        "title": "second",
        "content": "모델링 어렵다....ㅠ",
        "author_nickname": "chaeri",
        "created_at": "2021-10-07T21:56:30.211834+09:00",
        "updated_at": "2021-10-07T21:56:30.211834+09:00",
        "post_like": [],
        "post_comment": []
    },
    {
        "author": 5,
        "title": "배고파",
        "content": "간식 줘",
        "author_nickname": "choco",
        "created_at": "2021-10-07T21:57:34.991820+09:00",
        "updated_at": "2021-10-07T21:57:34.991820+09:00",
        "post_like": [],
        "post_comment": []
    },
    {
        "author": 6,
        "title": "세오스",
        "content": "ㅎㅎ",
        "author_nickname": "ceos",
        "created_at": "2021-10-14T19:48:10.277414+09:00",
        "updated_at": "2021-10-14T19:48:10.277414+09:00",
        "post_like": [
            {
                "id": 1,
                "created_at": "2021-10-14T20:01:58.647086+09:00",
                "updated_at": "2021-10-14T20:01:58.647086+09:00",
                "post": 5,
                "user": 4
            },
            {
                "id": 2,
                "created_at": "2021-10-14T20:02:02.110654+09:00",
                "updated_at": "2021-10-14T20:02:02.110654+09:00",
                "post": 5,
                "user": 5
            },
            {
                "id": 3,
                "created_at": "2021-10-14T20:02:05.121339+09:00",
                "updated_at": "2021-10-14T20:02:05.121339+09:00",
                "post": 5,
                "user": 6
            }
        ],
        "post_comment": [
            {
                "post": 5,
                "writer": 5,
                "content": "세오스 짱",
                "created_at": "2021-10-14T19:59:40.169794+09:00",
                "updated_at": "2021-10-14T19:59:40.169794+09:00",
                "writer_nickname": "choco"
            },
            {
                "post": 5,
                "writer": 4,
                "content": "세오스 최고",
                "created_at": "2021-10-14T20:00:14.070063+09:00",
                "updated_at": "2021-10-14T20:00:14.070063+09:00",
                "writer_nickname": "chaeri"
            },
            {
                "post": 5,
                "writer": 5,
                "content": "백엔드 최고",
                "created_at": "2021-10-14T20:00:30.106336+09:00",
                "updated_at": "2021-10-14T20:00:30.106336+09:00",
                "writer_nickname": "choco"
            }
        ]
    }
]
```

## 새로운 데이터를 create하도록 요청하는 API 만들기
 * URL: api/posts/
 * Method: POST
 * Body
```json
{
    "author" : 6,
    "title" : "drf",
    "content" : "serializer"

}
```

```json
{
    "author": 6,
    "title": "drf",
    "content": "serializer",
    "author_nickname": "ceos",
    "created_at": "2021-10-14T23:49:38.218561+09:00",
    "updated_at": "2021-10-14T23:49:38.218561+09:00",
    "post_like": [],
    "post_comment": []
}
```

### 간단한 회고
시험 기간이라서 많은 시간을 쏟진 못해서 많이 아쉬웠다.
이번에 장고를 처음 사용해서 drf와 serializer가 정말 편리한 기능이라 생각했다. 앞으로 스터디를 하면서 또 어떤 기능들이 있을지 기대된다.

* * *

# 5주차 과제 (기한: 11/11 목요일까지)
## 모든 list를 가져오는 API
* URL: api/posts
* Method: GET
```json
[
    {
        "author": 1,
        "title": "first",
        "content": "신기하다",
        "author_nickname": "chaeri",
        "created_at": "2021-11-11T10:43:09.051113+09:00",
        "updated_at": "2021-11-11T10:43:09.051113+09:00",
        "post_like": [],
        "post_comment": [
            {
                "post": 1,
                "writer": 4,
                "content": "너무 신기하다",
                "created_at": "2021-11-11T10:59:43.817108+09:00",
                "updated_at": "2021-11-11T10:59:43.817108+09:00",
                "writer_nickname": "ceos"
            },
            {
                "post": 1,
                "writer": 3,
                "content": "와우우우",
                "created_at": "2021-11-11T11:00:12.168062+09:00",
                "updated_at": "2021-11-11T11:00:12.168062+09:00",
                "writer_nickname": "choco"
            }
        ]
    },
    {
        "author": 1,
        "title": "second",
        "content": "모델링 어렵다....ㅠ",
        "author_nickname": "chaeri",
        "created_at": "2021-11-11T10:43:19.266647+09:00",
        "updated_at": "2021-11-11T10:43:19.266647+09:00",
        "post_like": [],
        "post_comment": []
    },
    {
        "author": 3,
        "title": "배고파",
        "content": "간식 줘",
        "author_nickname": "choco",
        "created_at": "2021-11-11T10:43:38.681635+09:00",
        "updated_at": "2021-11-11T10:43:38.681635+09:00",
        "post_like": [],
        "post_comment": [
            {
                "post": 3,
                "writer": 1,
                "content": "1111",
                "created_at": "2021-11-11T11:01:39.024705+09:00",
                "updated_at": "2021-11-11T11:01:39.024955+09:00",
                "writer_nickname": "chaeri"
            },
            {
                "post": 3,
                "writer": 4,
                "content": "2222",
                "created_at": "2021-11-11T11:02:09.112316+09:00",
                "updated_at": "2021-11-11T11:02:09.112316+09:00",
                "writer_nickname": "ceos"
            }
        ]
    },
    {
        "author": 4,
        "title": "세오스 최고",
        "content": "백엔드 최고",
        "author_nickname": "ceos",
        "created_at": "2021-11-11T10:45:02.634218+09:00",
        "updated_at": "2021-11-11T10:45:02.634218+09:00",
        "post_like": [
            {
                "id": 1,
                "created_at": "2021-11-11T11:03:25.206561+09:00",
                "updated_at": "2021-11-11T11:03:25.206561+09:00",
                "post": 4,
                "user": 3
            },
            {
                "id": 2,
                "created_at": "2021-11-11T11:03:28.479015+09:00",
                "updated_at": "2021-11-11T11:03:28.479015+09:00",
                "post": 4,
                "user": 4
            },
            {
                "id": 3,
                "created_at": "2021-11-11T11:03:32.296073+09:00",
                "updated_at": "2021-11-11T11:03:32.296073+09:00",
                "post": 4,
                "user": 1
            }
        ],
        "post_comment": []
    }
]
```

## 특정 데이터를 가져오는 API
* URL: api/posts/2
* Method: GET
```json
{
    "author": 1,
    "title": "second",
    "content": "모델링 어렵다....ㅠ",
    "author_nickname": "chaeri",
    "created_at": "2021-11-11T10:43:19.266647+09:00",
    "updated_at": "2021-11-11T10:43:19.266647+09:00",
    "post_like": [],
    "post_comment": []
}
```
## 새로운 데이터를 생성하는 API
* URL: api/posts/
* Method: Post
* Body
```json
{
    "author" : 3,
    "title" : "view 작성",
    "content" : "view 작성하기 과제"
}
```
```json
{
    "author": 3,
    "title": "view 작성",
    "content": "view 작성하기 과제",
    "author_nickname": "choco",
    "created_at": "2021-11-12T01:01:58.749741+09:00",
    "updated_at": "2021-11-12T01:01:58.749741+09:00",
    "post_like": [],
    "post_comment": []
}
```

## 특정 데이터를 업데이트하는 API
* URL: api/posts/7
* Method: PUT
* Body
```json
{
    "author" : 3,
    "title" : "view update",
    "content" : "update, update"
}
```

```json
{
    "author": 3,
    "title": "view update",
    "content": "update, update",
    "author_nickname": "choco",
    "created_at": "2021-11-12T01:01:58.749741+09:00",
    "updated_at": "2021-11-12T01:14:05.158968+09:00",
    "post_like": [],
    "post_comment": []
}
```

## 특정 데이터를 삭제하는 API
* URL: api/posts/6
* Method: DELETE

![delete](https://user-images.githubusercontent.com/79985974/141332502-2e1233b2-c096-4b40-a3b6-4c3c408e90dc.PNG)
  

## 공부한 내용 정리

### FBV로 작성
```python

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import Post
from api.serializers import PostSerializer

@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
def post_detail(request, pk):
    try:
        post=Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse(status=404)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        post.delete()
        return JsonResponse(status=204)

```

### CBV로 작성
```python
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Post
from api.serializers import PostSerializer


class PostList(APIView):
    def get(self, request, format=None): # Post 전체 가지고 오기
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, safe=False)

    def post(self, request, format=None): # Post 작성하기
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None): # 특정 Post 삭제
        post = self.get_object(pk)
        post.delete()
        return Response(status=204)

```

            
1. get_object 함수    
>    pk값을 인자로 받아서 객체를 찾아서 존재하면 반환해주고 pk값에 해당하는 객체가 없으면 에러가 뜨게 해주는 함수이다.
> 반복되는 코드들을 줄여줘서 코드가 간결해지고 가독성이 높아지게 해주는 함수이다.
    
2. format=None
> 장고 공식 튜토리얼에 보면 CBV에서 필드로 항상 format=None을 작성해주는데 이게 하는 역할이 무엇인지 궁금했다
> 그래서 검색해 보니까 127.0.0.1:8000/api/posts/6.json과 같은 URL을 API에서 처리할 수 있게 해주며 또한 urls.py에
> urlpatterns = format_suffix_patterns(urlpatterns)를 추가해 주어야 적용이 된다.


### 간단한 회고
중간에 DB에 문제가 생겨서 mysql을 지웠다가 다시 깔았더니 그 다음은 다른 에러들이 자꾸 생겨서
힘들었다.ㅠㅠ 분명 view는 빨리 작성했는데 에러때문에 시간을 많이 잡아먹었다ㅜ

* * *

# 6주차 과제

## viewset으로 리팩토링하기

```python
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend] 
    filter_class = PostFilter


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = ProfileFilter
```
먼저 뷰를 viewset으로 리팩토링 해줬다. CRUD를 직접 정의안해줘도 알아서 장고에서 구현해줘서
너무나 편리하고 신기했다. 전에는 코드가 꽤 길었는데 viewset으로 사용하니까 두줄만 써도 POST, GET, PUT, DELETE
이 다 작동되었다.

## Filtering
```python
class PostFilter(FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr="icontains")#해당 문자열을 포함하는 queryset
    content_null = filters.BooleanFilter(field_name='content', method='is_content_null')#true 시에 content가 null인것만 출력

    class Meta:
        model = Post
        fields = ['title', 'content']

    def is_content_null(self, queryset, content, value):
        if value:
            return queryset.filter(content__isnull=True)
        else:
            return queryset.filter(content__isnull=False)


class ProfileFilter(FilterSet):
    nickname = filters.CharFilter(field_name='nickname')

    class Meta:
        model = Profile
        fields = ['nickname']
```
처음에는 꼭 전체 단어를 검색해야지 해당 queryset을 가져올 수 있었는데
lookup_expr="icontains"를 포함했더니 해당 단어의 특정 문자열만 검색해도 queryset을 반환할 수 있었다.
> lookup_expr는  필터링 할 때 필드를 가져온다. 장고에서 __구문 은 조회된 결과의 조건에 대한 변환을 지원 한다.
> 기본값은 'iexact'이고 이외에도 'isnull', 'in'도 있다.

### Postman 결과

[GET] http://127.0.0.1:8000/api/profiles
```json
[
    {
        "user": 1,
        "nickname": "chaeri",
        "introduction": "heyyyyyyy"
    },
    {
        "user": 2,
        "nickname": "choco",
        "introduction": "멍멍"
    },
    {
        "user": 3,
        "nickname": "ceos",
        "introduction": "후후"
    }
]
```

[GET] http://127.0.0.1:8000/api/profiles/?nickname=chaeri

```json
[
    {
        "user": 1,
        "nickname": "chaeri",
        "introduction": "heyyyyyyy"
    }
]
```

[GET] http://127.0.0.1:8000/api/posts/?title=choco
```json
[
    {
        "author": 3,
        "title": "chocolate",
        "content": "",
        "author_nickname": "choco",
        "created_at": "2021-11-19T01:24:00.405420+09:00",
        "updated_at": "2021-11-19T01:43:41.202731+09:00",
        "post_like": [],
        "post_comment": []
    },
    {
        "author": 3,
        "title": "chococo",
        "content": null,
        "author_nickname": "choco",
        "created_at": "2021-11-19T01:26:15.250002+09:00",
        "updated_at": "2021-11-19T01:26:15.250002+09:00",
        "post_like": [],
        "post_comment": []
    }
]
```

[GET] http://127.0.0.1:8000/api/posts/?content_null=true
```json
[
    {
        "author": 3,
        "title": "chococo",
        "content": null,
        "author_nickname": "choco",
        "created_at": "2021-11-19T01:26:15.250002+09:00",
        "updated_at": "2021-11-19T01:26:15.250002+09:00",
        "post_like": [],
        "post_comment": []
    },
    {
        "author": 1,
        "title": "hungry",
        "content": null,
        "author_nickname": "chaeri",
        "created_at": "2021-11-19T01:52:46.304923+09:00",
        "updated_at": "2021-11-19T01:52:46.304923+09:00",
        "post_like": [],
        "post_comment": []
    }
]
```

[GET] http://127.0.0.1:8000/api/posts/?content_null=true&title=choco
```json
[
    {
        "author": 3,
        "title": "chococo",
        "content": null,
        "author_nickname": "choco",
        "created_at": "2021-11-19T01:26:15.250002+09:00",
        "updated_at": "2021-11-19T01:26:15.250002+09:00",
        "post_like": [],
        "post_comment": []
    }
]
```

## Permission

### Permission이란?
> 어떠한 사용자가 API에 접근해 특정 작업을 수행하려 할 때, request에 담겨오는 
> user의 정보에 따라 작업의 권한을 줄지 말지 결정하는 것이다
> 
### Permission 종류

* AllowAny(default) : 무조건 허용
* IsAuthenticated : 인증된 사용자에 대한 작업 권한을 허용하고 인증되지 않은 사용에 대한 액세스를 거부
* IsAuthenticatedOrReadOnly : 인증된 사용자에게는 전체 액세스를 허용하지만 인증되지 않은 사용자에게는 읽기만 허용

```json
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = PostFilter
    permission_classes = [IsAuthenticatedOrReadOnly]
```

ViewSet 내부의 permission_classes 에 추가

## 간단한 회고

시간이 없어서 validation을 못해봤는데 다음에 시간 날 때 꼭 해보고 싶다. 그리고 아직
필터링에 대해서 완벽하게 이해하지 못한것 같은데 Filterset 특히 method에 대해서 더 자세히 공부해야겠다.