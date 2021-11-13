## 2주차 과제
"심화과정 - 무지성에서 지성 되기" 노션으로 공부를 진행했습니다!


## 원리 -> Docker + Github Actions

### => CD (Continuous Delivery) - 지속적 배포   
  
  


### Docker 용도 - 어떤 OS에서도 같은 환경을 만들어준다

> EC2에서 서버를 만들면 ubuntu OS로 아무것도 없는 인스턴스 생성 *( 인스턴스: 클라우드의 가상 서버 )*
>
> -> 서버를 띄우기 위해서는 python, git 등 일일히 설치를 해줘야함
>
> -> 만약 서버를 ubuntu가 아닌 다른 OS로 띄우는 경우, 설치 방법도 달라지기 때문에 일일이 대응 필요
>
> -> 서버와 로컬의 환경도 달라 배포하고 난 후에도 OS 차이로 문제가 생길 수도 있음
>
> => **어떤 OS에서도 같은 환경을 만들어주는 Docker** 사용



### Github Actions 용도 - 1) 서버 접속 후 Docker 실행, 2) master에 push된 commit 복사

> 서버에 접속해서 Docker를 실행
>
> master에 푸시된 커밋을 복사



### Docker vs Docker-compose

Docker: 가상 컨테이너 기술

(* 컨테이너: 도커가 띄운 가상 시스템/ 호스트: 도커를 실행시키고 있는 주체)

|     Docker      |        Docker-compose        |
| :-------------: | :--------------------------: |
| Dockerfile 실행 | docker-compose.yml 파일 실행 |



Dockerfile: 하나의 이미지(구축한 환경의 스냅샷)를 만들기 위한 과정

(이 이미지가 있다면 다른 컴퓨터에서도 똑같은 환경을 올릴 수 있음)

docker-compose: 이 이미지를 여러개 띄워서 네트워크 만들고, 컨테이너 밖의 호스트와 어떻게 연결할지, 파일 시스템은 어떻게 공유할지 제어



### 서버가 뜨는 과정 - GitHub Actions가 docker-compose.prod.yaml 파일을 실행

Github Actions가 실행시키는 파일(deploy.yml)의 마지막 줄의 config/scripts/deploy.sh 파일의 `sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d` 명령어로 서버가 빌드, 실행

(* docker-compose.prod.yaml: prod = production = live = real -> 로컬이 아닌 서버에서 Github Actions에 의해 실행되는 파일)



### docker-compose.prod.yml vs docker-compose.yml

| docker-compose.prod.yml |  docker-compose.yml   |
| :---------------------: | :-------------------: |
|   db 컨테이너가 없다    |  db 컨테이너가 있다   |
|  nginx 컨테이너가 있다  | nginx 컨테이너가 없다 |



### docker-compose.prod.yml 파일에 db 컨테이너가 없는 이유

- 데이터가 날아가거나, 유출될 위험이 있음

- 서버는 대개 상황에 따라 여러 인스턴스를 띄울수도 있고 지울수도 있는데, 서버에 db를 띄우면 다른 서버가 db에 붙지도 못하고 인스턴스를 날리면 데이터도 날아감
- 인스턴스의 자원을 서버와 db가 같이 쓰므로 비효율적
- 만약 서버를 해킹당한다면, 개인정보까지 유출되는 것임



### Nginx?

WAS(Web Application Server): web에서 application을 serving하는 것

=> application: django / server: nginx



> **nginx <-> gunicorn or uwsgi <-> wsgi <-> django**

(* wsgi: web server gateway interface)



웹 서버가 따로 필요한 이유

1. application을 여러대 띄우고 웹 서버가 이를 적절하게 로드밸런싱 하기 위함
2. 보안상 위험한 요청을 차단하기 위함



nginx Dockerfile

```dockerfile
FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```

- FROM nginx:1.19.0-alpine

  -> nginx의 1.19.0-alpine 버전 이미지 사용. 이 이미지는 누군가가 만들어놨고, nginx 구동에 필요한 환경이 이 이미지 안에 다 들어가있음

- RUN rm /etc/nginx/conf.d/default.conf

  -> 원하는 설정 파일로 바꾸기 위해 default config 파일 삭제.

- COPY nginx.conf /etc/nginx/conf.d

  -> nginx.conf 파일 옮김.



### docker-compose up 의미

최종 실행 코드: 

`sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d`

- up: docker-compose 파일에 정의된 모든 컨테이너를 띄우라는 명령

- --build: up을 할 때마다 새로 build를 강제 수행하도록 하는 파라미터

- -d: daemon 실행

  

up을 한다고 해서 서버가 뜨는 것이 아님! django가 실행되어야 하는데 docker-compose가 django를 어떻게 아는가

→ **<u>command</u>와 <u>entrypoint</u>를 정의**



 Entrypoint와 cmd: 해당 컨테이너가 수행하게 될 실행 명령을 정의하는 선언문

=> 컨테이너가 무슨 일을 하는지 결정하는 최종 단계를 정의하는 명령



### Command

Command를 사용하여 컨테이너 수행 명령을 정의한 경우, 컨테이너를 실행할 때 인자값을 주게 되면 Dockerfile에 지정된 cmd 값을 대신하여 지정한 인자값으로 변경하여 실행됨



### Entrypoint

Entrypoint를 사용하여 컨테이너 수행 명령을 정의한 경우, 해당 컨테이너가 수행될 때 반드시 Entrypoint에서 지정한 명령을 수행되도록 지정됨



### Cmd vs Entrypoint 예제

1. ### Cmd

```dockerfile
# Dockerfile 

FROM ubuntu 
CMD ["/bin/df", "-h"]
```

: CMD 를 사용하여 df -h 명령을 한번 수행하고 종료되는 이미지를 만드는 것



테스트를 위해 위 Dockerfile 을 사용해 jhsong/df 라는 이름을 가진 이미지를 빌드

```dockerfile
❯ docker build -t jhsong/df .

Sending build context to Docker daemon 2.048kB
Step 1/2 : FROM ubuntu 
---> 94e814e2efa8 
Step 2/2 : CMD ["/bin/df", "-h"] 
---> Running in c5f57fca1068
Removing intermediate container c5f57fca1068
---> 80eeec0ef7c0
Successfully built 80eeec0ef7c0 
Successfully tagged jhsong/df:latest
```



빌드된 jhsong/df 이미지를 컨테이너로 동작시켜 보면, Dockerfile 에서 정의된 대로 df -h 명령을 실행하고 종료

```dockerfile
❯ docker run --name jhsong-df jhsong/df
Filesystem Size Used Avail Use% Mounted on 
overlay 59G 5.6G 50G 11% / 
tmpfs 64M 0 64M 0% /dev 
tmpfs 1000M 0 1000M 0% /sys/fs/cgroup
/dev/sda1 59G 5.6G 50G 11% /etc/hosts
shm 64M 0 64M 0% /dev/shm
tmpfs 1000M 0 1000M 0% /proc/acpi 
tmpfs 1000M 0 1000M 0% /sys/firmware
```



컨테이너 실행시 **추가 인자 값**을 줘서 컨테이너가 수행할 명령 변경

docker run 으로 컨테이너 실행시 마지막에 ps 명령을 추가 인자를 주고 실행

```dockerfile
❯ docker run --name jhsong-df jhsong/df ps -aef

UID PID PPID C STIME TTY TIME CMD 
root 1 0 0 15:19 ? 00:00:00 ps -aef
```

=> **CMD 로 지정한 내용 대신 컨테이너 실행시 받은 인자로 대체하여 실행**



2. ### Entrypoint

```dockerfile
# Dockerfile

FROM ubuntu 
ENTRYPOINT ["/bin/df", "-h"]
```



이미지 빌드

```dockerfile
❯ docker build -t jhsong/df:entry .

Sending build context to Docker daemon 2.048kB
Step 1/2 : FROM ubuntu
---> 94e814e2efa8 
Step 2/2 : ENTRYPOINT ["/bin/df", "-h"]
---> Running in 61f6f8ad4f61
Removing intermediate container 61f6f8ad4f61
---> cc23a8719b6e 
Successfully built cc23a8719b6e 
Successfully tagged jhsong/df:entry
```



빌드된 jhsong/df:entry 이미지로 컨테이너를 실행

```dockerfile
❯ docker run --name jhsong-df jhsong/df:entry

Filesystem Size Used Avail Use% Mounted on 
overlay 59G 5.6G 50G 11% / 
tmpfs 64M 0 64M 0% /dev 
tmpfs 1000M 0 1000M 0% /sys/fs/cgroup 
/dev/sda1 59G 5.6G 50G 11% /etc/hosts
shm 64M 0 64M 0% /dev/shm 
tmpfs 1000M 0 1000M 0% /proc/acpi 
tmpfs 1000M 0 1000M 0% /sys/firmware
```



위에서 했던 작업과 같이 docker run 으로 수행시 인자를 추가로 넣어 컨테이너를 실행해 보면 Entrypoint 와 cmd의 확실한 차이를 볼 수 있음

```dockerfile
❯ docker run --name jhsong-df jhsong/df:entry ps -aef 

/bin/df: invalid option -- 'e'
Try '/bin/df --help' for more information.
```

=> 위와 같이 **에러를 출력하며 원하는 동작이 실행되지 않았음**을 볼 수 있음

→ 컨테이너 실행시 /bin/df 명령은 유지하고, 추가 인자를 CMD로 받아 처리



### Command와 Entrypoint의 올바른 사용 방법

1. 컨테이너가 수행될 때 변경되지 않을 실행 명령은 Entrypoint로 정의하는 것이 좋다.

   → 대부분의 컨테이너는 실행될 목적이 분명함

   

2. 메인 명령어 실행 시 default option 인자 값은 cmd로 정의하는 것이 좋다.

   

3. Entrypoint와 cmd는 리스트 포맷(["args1", "args2", ...])으로 정의하는 것이 좋다.



### Github Actions가 수행하는 것

```yaml
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

   push 될 때마다 이 workflow 수행

2. -name: create env file

   깃헙 설정에서 복사한 ENV_VARS의 값을 모두 .env file로 만듦

3. -name: create remote directory

   ec2 서버에 디렉토리를 하나 만듦

4. -name: copy source via ssh key

   ssh key를 이용하여 현재 푸쉬된 소스를 서버에 복사

5. -name: executiong remote ssh commands using password

   서버에 접속하여 deploy.sh 실행



### 요약

1. Github Actions가 코드를 서버에 올리고 deploy.sh를 실행

2. deploy.sh는 docker-compose를 실행

3. docker-compose는 web이라는 컨테이너와 nginx라는 컨테이너를 빌드하고 실행
4. web 컨테이너는 Dockerfile.prod를 기준으로 빌드, 이 도커 이미지는 django를 구동하기 위한 환경이 모두 갖춰져있음.








## 3주차 과제

### 모델링 해보기

#### 인스타그램 서비스

1. 사용자들은 각자 이름과 아이디로 누가 누구인지 구별할 수 있다. 공인의 경우(공식계정인 경우)는 이름 옆에 파란색 체크 무늬가 뜬다. 

   => User 클래스에 username(사용자 이름), instagram_id(아이디), is_professtional(공식계정인지 아닌지) 변수를 생성한다.

   => 한 id는 오직 하나만 존재해야 하기 때문에 unique=True 값을 주었다.

   => AbstractBaseUser를 사용한 이유는 Django가 제공하는 기본  User 모델의 필드들이 너무 과하기도 하고, 원하는 필드들로 유저 모델을 구성할 수 있기 때문입니다. (https://velog.io/@iedcon/AbstractBaseUser%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-Django-%EC%BB%A4%EC%8A%A4%ED%85%80-%EC%9C%A0%EC%A0%80-%EB%AA%A8%EB%8D%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0)

2. 사용자들의 프로필에는 사진, 자신의 이름과 사용자이름(id), 웹사이트 주소와 소개를 입력할 수 있다.

   => Profile 클래스(사용자의 세부 정보를 담는 모델)에 profile_picture(프로필 사진), user(사용자), profile_name(프로필에 설정한 이름), profile_website(프로필 웹사이트), profile_info(자기소개 내용) 변수를 생성한다.

   => 사용자 정보를 담는 user는 User 클래스를 ForeignKey로 받아온다.


3. 사용자들은 피드에 사진과 함께 게시물을 올린다. 게시물에는 작성자와 위치, 좋아요 수, 게시물 내용, 댓글, 업로드 시간 정보가 담겨있다.

   => Post 클래스(게시글을 담는 모델)에 post_author(게시물 작성자), location(위치), numOfLike(좋아요 수), post_content(게시물 내용), is_comment(댓글 작성 가능 여부), upload_time(업로드 시간) 변수를 생성한다.

   => post_author는 User 클래스를 ForeignKey로 받아온다.

   => 게시물 업로드 시 자동으로 현재 시간을 업로드 시간으로 담도록 한다. (auto_now=True)

   => Image 클래스(게시물의 사진을 담는 모델)를 생성하고, 그 안에 그 사진이 포함된 게시물과 이미지 url을 담는 변수를 생성한다. 

   => Image 클래스의 post는 Post 클래스를 ForeignKey로 받아온다.

4. 댓글은 작성자가 허용할 수도 있고 아닐 수도 있다. 즉, 댓글을 작성할 수 없는 게시글이 있다.

   => Comment 클래스(게시글의 댓글을 담는 모델)에 post(해당 게시글), comment_author(댓글 작성자), comment_content(댓글 내용), upload_time(업로드 시간) 변수를 생성한다.

   => post는 Post 클래스를 ForeignKey로 받아온다.

   => comment_author는 User 클래스를 ForeignKey로 받아온다.

   => is_comment가 False인 게시물이 댓글을 작성할 수 없는 게시물이다.

5. 사용자들은 피드에만 업로드할 수 있는 것이 아니라 스토리에도 글을 작성할 수 있다. 스토리에는 작성자와 스토리 내용, 스토리 업로드 시간 정보가 담겨있다.

   => Story(스토리를 담는 모델)클래스에 story_author(스토리 작성자), story_content(스토리 내용), upload_time(업로드 시간) 변수를 생성한다.

   => story_author는 User 클래스를 ForeignKey로 받아온다.   


### ORM 적용해보기

1. 객체 3개 넣기

![orm1](https://user-images.githubusercontent.com/80563849/136409070-04135b6d-6e0a-4bc4-a723-3463c6e9a3fe.PNG)

2. 쿼리셋으로 조회해보기 (hello world는 캡처하기 전에 삽입했던 게시글 입니다!)

![orm2](https://user-images.githubusercontent.com/80563849/136409190-fe77e595-1724-4d7f-9307-27b75ec5c089.PNG)

3. filter 함수 사용해보기

![orm3](https://user-images.githubusercontent.com/80563849/136409231-4f769df3-2845-42b1-b328-88b9e8e236b8.PNG)



### 간단한 회고

1. 데이터베이스 강의에서 mysql에 대한 내용을 배웠어서 그런지 매핑 관계 이해는 생각보다 괜찮았다.
2. models.py 파일에 한번에 여러 모델을 정의하는 것보단 models 디렉토리를 생성한 후에 파일을 세분화하는 것이 보기에도 편하다는 것을 알게 되었다. -> models/init 파일에 import 문을 작성해야한다는 것을 알게 되었다.
3. mysql 문을 작성할 때 끝의 세미콜론(;)을 꼭 쓰자.
4. github actions은 왜 에러가 나는걸까






## 4주차 과제

### 1️⃣ 데이터 삽입

- `ORM 쿼리`를 통해 `Post 모델`에 데이터 3개 삽입

![orm](https://user-images.githubusercontent.com/80563849/138105662-921d1b7b-3053-4f19-b11b-bc7c6a6afb95.PNG)

- 모델 선택 및 데이터 삽입

  ```python
  class Post(models.Model):
      post_author = models.ForeignKey(User, on_delete=models.CASCADE)
      location = models.TextField()
      post_content = models.TextField()
      is_comment = models.BooleanField()
      upload_time = models.DateTimeField(auto_now=True)
  
      def publish(self):
          self.upload_time = timezone.now()
          self.save()
  
      def __str__(self):
          return self.post_content
  
      class Meta:
          managed = True
          verbose_name = 'Post'
          verbose_name_plural = 'Posts'
          
          
  class User(AbstractBaseUser):
      username = models.CharField(max_length=100, unique=True)
      USERNAME_FIELD = 'username'
      instagram_id = models.CharField(max_length=100, unique=True)
      is_professional = models.BooleanField(default=False)
  
      objects = UserManager()
  
      class Meta:
          managed = True
          verbose_name = 'User'
          verbose_name_plural = 'Users'
  ```

  ![저장](https://user-images.githubusercontent.com/80563849/138125025-7c183c7a-cf45-4118-a872-88629275788a.PNG)

### 2️⃣ 모든 데이터를 가져오는 API 만들기

- 모든 'Post'의 list를 가져오는 API 요청 결과: `GET`  `api/posts`

![image](https://user-images.githubusercontent.com/80563849/138129310-d1e205e7-0b74-434c-b6f0-edcdbc75a96b.png)



### 3️⃣ 새로운 데이터를 create하도록 요청하는 API 만들기

- Post를 추가하는 API 요청 결과: `POST` `api/posts/` 

- Body: `{"post_content" : "happy", "location" : "Namyangju"}`

  ![image](https://user-images.githubusercontent.com/80563849/138139771-7500ec46-71c2-4fb7-b55d-6dfb525704cb.png)



### 4️⃣ 회고

가장 오래 걸렸던 과제였던 것 같다. 아직 완벽하게 이해가 된 것 같지 않아서 날 잡고 열심히 공부해야겠다..😥 erd와 변경된 model을 3주차 README에 반영해야겠다.



### ☑ 참고

- `django.db.utils.IntegrityError` 에러가 발생한 경우: 에러가 발생한 **필드가 null 값이 되지 않도록 값 필수로 설정**

- POSTMAN으로 POST api 작성 방법: [POST api - Body->raw](https://meetup.toast.com/posts/107) (param으로 값을 입력해서 호출한 경우, 

  `rest_framework.exceptions.parseerror: json parse error - expecting value: line 1 column 1 (char 0)` 에러가 발생했음)

- `'manager' object has no attribute 'get_by_natural_key'` 에러가 발생한 경우: User 클래스에 `objects = UserManager()` 추가 (**AbstractBaseUser로 custom user를 생성한 경우** **UserManager 필수**로 선언, 추가)

- [verbose name이란](https://djangojeng-e.github.io/2020/08/02/Django-Models-6%ED%8E%B8-Fields-verbose-field-names/)








## 5주차 과제

기존에 작성했던 views.py 를 **CBV인 API View**로 변경할 것이다.



### READ API (`GET`)

#### 1. views.py 작성하기

```python
# views.py
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import PostSerializer


class PostList(APIView):
    def get(self, request, format=None):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
```

`PostList`의 `get` 함수는 **모든 Post의 list를 가져오는 함수**이다.  

`queryset`에 모든 `Post` 데이터를 저장한 후 `PostSerializer`에 queryset을 `many=True`로 삽입하여 **serializer에 담긴 data를 반환**하는 형식이다.

```python
class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)    # get_object로 error check
        serializer = PostSerializer(post)
        return Response(serializer.data)
```

`PostDetail`의 `get` 함수는 특정 `id` (=pk)를 받아 **그 id값을 지닌 Post를 가져오는 함수**이다.

`get_object`는 **Error catch를 위한 함수**로, 요청을 보낸 id가 존재하지 않는 경우엔 `Http404`에러를 발생시킨다.

#### 2. urls.py 작성하기

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.PostList.as_view()),
    path('posts/<int:pk>', views.PostDetail.as_view())
]
```

view.py를 작성한 후 urls.py를 작성한다.



#### 결과

**1️⃣ 모든 데이터를 가져오는 API**

- URL: `api/posts`
- Method: `GET`

![모든포스트가져오기](https://user-images.githubusercontent.com/80563849/141237418-2afff7e9-e32e-4fb6-bb0a-1c2c259db18d.PNG)

**2️⃣ 특정 데이터를 가져오는 API**

- URL: `api/posts/\<int:pk>` (`api/posts/2`)
- Method: `GET`

![특정포스트가져오기](https://user-images.githubusercontent.com/80563849/141237490-a52ed993-ae7f-49dc-aa3b-36c1a114dbb8.PNG)

### CREATE API (`POST`)

#### views.py 작성하기

```python
# views.py

class PostList(APIView):
	def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
```

`PostList`의 `post` 함수는 **새 Post를 create하는 함수**이다. 

serializer의 값이 `valid` 하면, 즉 요청한 값이 `valid`하면 `Http201`을, `invalid`하다면 `Http400` error를 반환한다.   



#### 결과

**3️⃣ 새로운 데이터를 create하는 API** 

- URL: `api/posts`
- Method: `POST`
- Body: `{"필드명": 필드값, ... }`

![새로운데이터생성하기](https://user-images.githubusercontent.com/80563849/141237547-164620a5-b15c-47eb-80e7-e6a96fb6015e.PNG)



### UPDATE API (`PUT`)

#### views.py 작성하기

```python
# views.py

class PostDetail(APIView):
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

`PostDetail`의 `put` 함수는 특정 `id`(=pk)를 받아 **그 id값을 지닌 Post의 내용을 변경하는 함수**이다.

요청한 값이 `valid`하면 **변경된 값을 보여주고**, `invalid`하면 `Http400` error를 발생시킨다.

### 

#### 결과

**4️⃣ 특정 데이터를 업데이트하는 API**

- URL: `api/posts/<int:pk>` (`api/posts/3`)
- Method: `PUT`
- Body: `{"필드명": 업데이트 할 필드값, ... }` (`{"location": "Songdo"}`)

  ![특정데이터업데이트하기](https://user-images.githubusercontent.com/80563849/141237595-a49712c2-93f0-4bff-856f-e4f8548012db.PNG)



### DELETE API (`DELETE`)

#### views.py 작성하기

```python
class PostDetail(APIView):
	def delete(self, request, pk):
    	post = self.get_object(pk)
    	post.delete()
    	return Response(status=status.HTTP_204_NO_CONTENT)
```

`PostDetail`의 `delete` 함수는 특정 `id`(=pk)의 **Post를 삭제하는 함수**이다.

delete() 함수로 삭제를 한 후, `Http204`로 삭제가 완료되었음을 보여준다.



#### 결과

**5️⃣ 특정 데이터를 삭제하는 API**

- URL: `api/posts/\<int:pk>`
- Method: `DELETE`

아래 사진처럼 삭제 요청을 보내고,

![삭제요청보내기](https://user-images.githubusercontent.com/80563849/141237632-3de6d0cf-eadd-404a-8d8d-f19ca537d6b4.PNG)

요청을 보낸 후, GET api/post/3 으로 3번째 Post를 조회하면, 

![삭제하고다시조회하기](https://user-images.githubusercontent.com/80563849/141237654-b0dc8d41-3e64-4359-b1f2-2b274bb5acae.PNG)



### 간단한 회고

- 새로운 데이터를 생성하는 POST 함수에서 계속 에러가 난다. ForeignKey로 post_author의 id를 생성하면서 `IntegrityError` 가 떠서 해결을.. 얼른... 해야겠다..
- 확실히 지난주에 만들었던 view 보다 API view를 사용하는 것이 코드가 깔끔해보여서 좋았다.
