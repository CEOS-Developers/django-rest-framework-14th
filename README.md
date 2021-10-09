# [2주차 스터디] Docker

## Linux Container??

> Container는 소프트웨어와 해당 소프트웨어를 실행하는 데 필요한 모든 환경을 하나의 패키지로 분리하는 리눅스 기술이다.
> 

컨테이너 이미지는 runtime, code, system tools, system libraries, dependencies 등 서버에 설치되는 모든 것을 포함하고 있다. 따라서 하나의 완전한 어플리케이션을 하나의 패키지로 담아낼 수 있다.

### 컨테이너를 사용하는 이유

- 소프트웨어가 다른 플랫폼이나 OS에서도 동일하게 작동하도록 한다.
- 개발, 배포, 통합, 자동화를 쉽고 빠르게 할 수 있도록 한다.

개발자는 자신의 컴퓨터 환경에 맞춰진 소프트웨어를 개발한다. 이를 다른 컴퓨터에서 동작시키려면 서버 환경을 동일하게 재구축해야할 수도 있다. 하지만 컨테이너(환경+소프트웨어)를 사용하면 쉽게 작동시킬 수 있다.

어플리케이션 실행에 필요한 모든 파일이 컨테이너에 포함된 이미지에 존재하기 때문에 개발/테스트/배포 모든 단계에서 일관성을 유지할 수 있다.

대규모 어플리케이션을 여러개의 컨테이너로 나누어 쉽게 관리할 수 있다.

따라서 새로운 아이디어를 신속하게 개발하고 배포할 수 있단 점이 핵심 장점이다.

### Container와 VM의 차이점

**Virtualization(가상화)의 특징**

- 하나의 하드웨어에서 여러 운영 체제를 동시에 실행
- Hypervisor를 기반으로 하드웨어 에뮬레이션 → 그 위에 여러 OS 실행
- 추가적인 OS를 설치해야 하므로 무거움

**Container의 특징**

- 하나의 운영 체제에서 여러 컨테이너를 동시에 실행
- 단순히 프로세스를 격리하는 것이기 때문에 가볍고 빠름

사실 컨테이너 이미지는 리눅스 배포를 설치하는 것과 비슷하다. 하지만 이미지 배포를 설치하는 것이 새로운 OS를 설치하는 것보다 간편하기 때문에 컨테이너가 가상화보다 좋을 수 있다.

## Docker??

Docker는 Linux Container를 기반으로 Container의 생성, 관리, 실행, 배포를 돕는 툴이다.


### Docker와 Linux Container의 차이점

**LXC(Linux Container)의 특징**

- 1개의 앱 == 1개의 컨테이너
- 여러 컨테이너를 하나의 전체적인 어플로 실행할 수 있음

**Docker의 특징**

- 1개의 앱 == 1개의 컨테이너
- 하지만 LXC와 다르게 컨테이너 내부에서 어플을 개별 프로세스로 세분화할 수 있음

도커는 LXC 기반으로 시작하였지만 추후에 자체 기술을 사용하게 되었다.

## Docker의 구조

Docker의 구조는 Client와 Server(Docker Host)로 구성되어 있다.

- **Client**: 서버에 전송될 명령어를 입력한다.
- **Docker daemon**: docker api 요청을 수신하고, 이를 처리한다.
따라서 docker object(image, container, network 등)를 관리하며 다른 docker daemon과 통신할 수 있다.
- **Docker Registry(Docker Hub)**: docker의 공식 이미지 저장소이다.
- **Image**: 컨테이너 실행에 필요한 파일과 설정값 등을 포함하고 있는 데이터이다. (공식 이미지는 이러한 필요 요소들이 사전에 구축되어 있는 것)

## Docker의 동작

1. Client는 Docker Host(Server)에 명령어를 전송한다. (`docker run <image-name>`)
2. Docker daemon은 local에서 image를 찾는다.
3. 로컬에 해당 이미지가 없으면, Docker daemon은 Docker Hub.에서 image를 가져온다(pull).
4. Docker daemon은 이미지를 바탕으로 새 컨테이너를 만든다.
5. Docker daemon은 Client에게 결과를 출력한다.

## Docker Compose??

Docker Compose는 YAML file을 사용하여 앱을 구성하는 서비스를 관리한다. 서비스를 설정, 빌드, 실행, 중지할 수 있다.

### **Docker vs Docker Compose**

Docker는 `Dockerfile`을 실행시키고, Docker Compose는 `docker-compose.yml`을 실행시킨다.

- **`Dockerfile`**: 앱의 이미지를 정의함
- **`docker-compose.yml`**: 앱을 구성하는 서비스(ex: web, db)를 설정한다. 
(사용하는 Docker image, 연결 방법, 파일 시스템 공유 방법, 사용하는 포트 번호 등을 설정)

### **Docker Compose를 사용하는 3단계**

1. `Dockerfile`을 이용해 앱의 환경을 정의한다.
2. `docker-compose.yml`을 이용해 서비스들을 정의한다. 
3. `docker compose up` 혹은 `docker-compose up` 명령어로 전체 앱을 동작시킨다.

## **Github Actions를 이용한 배포**

Github Actions는 소프트웨어의 워크플로우를 자동화해주는 도구이다. 깃허브 액션을 사용해 배포 버전 관리를 쉽게 할 수 있다.

```yaml
name: Deploy to EC2
on: [push] # push될 때마다 자동으로 워크플로우 수행
jobs:

  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
    - name: checkout
      uses: actions/checkout@master

    # Action Secret에 설정한 ENV_VARS 값을 .env 파일로 만듦
    - name: create env file
      run: |
        touch .env
        echo "${{ secrets.ENV_VARS }}" >> .env
		
    # EC2 서버에 디렉토리 생성
    - name: create remote directory
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        script: mkdir -p /home/ubuntu/srv/ubuntu

    # ssh key를 이용해 push된 소스를 서버에 복사
    - name: copy source via ssh key
      uses: burnett01/rsync-deployments@4.1
      with:
        switches: -avzr --delete
        remote_path: /home/ubuntu/srv/ubuntu/
        remote_host: ${{ secrets.HOST }}
        remote_user: ubuntu
        remote_key: ${{ secrets.KEY }}

    # 서버에 접속한 뒤 deploy.sh를 실행
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

commit → push 하면, 깃허브 액션이 자동으로 위 파일을 재실행하고, 마지막에서 서버를 빌드하는 스크립트 파일(`config/scripts/deploy.sh`)을 실행시켜준다.

## config/scripts/deploy.sh

```bash
# 서버를 빌드하는 명령어
sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d
```

`config/scripts/deploy.sh`는 EC2 인스턴스에 docker와 docker-compose를 설치하고, 서버를 빌드하는 역할을 한다.

- `docker-compose up`: 전체 앱을 동작시키는 명령어
- `-f <file-name>`: 동작시킬 컨테이너가 정의된 파일
- `--build`: 명령어가 실행될 때마다 새로 빌드를 수행
- `-d`: daemon을 실행하는 명령어
⇒ 백그라운드에서도 docker-compose를 동작시킴

## docker-compose.prod.yaml

prod는 production을 의미한다. 따라서 `docker-compose.prod.yaml`는 `docker-compose.yml`과 달리 서버에서 실행된다. 그리고 db container 대신 nginx container를 포함하고 있다.

### **DB container를 포함하지 않는 이유**

서버에 DB를 정의한다면

- 다른 서버가 해당 DB를 사용할 수 없음
- 인스턴스가 날아가면 데이터도 함께 날아가게 됨
- 인스턴스의 자원을 서버와 DB가 함께 쓰게되어 비효율적
- 서버 해킹 시 데이터가 유출될 수 있음

## nginx??

nginx는 웹 서버 프로그램으로

- 클라이언트의 요청을 받고 어플리케이션에 전달해준다.
- 어플리케이션에게 받은 정적 파일을 클라이언트에게 전송한다.

따라서 요청을 적절히 분배하고, 보안상 위험한 요청을 차단하기 위해서 필요하다. `/config/nginx/nginx.conf` 에서 nginx에 대한 설정을 할 수 있다.

---

# [3주차 스터디] Data Modeling

## 데이터 모델링이란??

참고: [데이터 모델링 개요](https://dataonair.or.kr/db-tech-reference/d-guide/da-guide/?mod=document&uid=276)

데이터 모델링은 다음과 같이 3단계로 나뉜다.

1. 개념 데이터 모델링

핵심 요소를 뽑아내고, 요소 간의 관계를 찾아내는 단계이다. ERD(Entity-Relationsion Diagram)을 작성한다.

2. 논리 데이터 모델링

요구되는 데이터를 더욱 상세하고 명확하고 논리적으로 적어내는 단계이다.

3. 물리 데이터 모델링

실질적으로 스키마를 설계 및 구현하는 단계이다.

## 인스타그램 모델링 해보기

- 인스타그램 모델 ERD

![Untitled](https://user-images.githubusercontent.com/71026706/136278982-1802ee85-cc3c-443a-b513-5b9a2d210f89.png)

우선, 인스타그램의 핵심 기능을 다음과 같이 생각하였다.

1. 사용자 생성하기
2. 포스트 작성하기
3. 포스트에 좋아요 누르기
4. 포스트에 댓글 작성하기

따라서 Entity와 Relation을 다음과 같이 정의하였다.

### Entities

- **User:** 사용자(Django에서 제공해주는 User 모델과 필드를 사용함)
    - username: 계정 아이디
    - email: 사용자 이메일
    - password: 계정 비밀번호
- **Profile:** 사용자 확장(User에 추가로 필요한 데이터들)
    - user_id: User FK(ForeignKey)
    - name: 프로필 이름
    - bio: 자기소개
    - profile_photo: 프로필 사진
- **Post:** 포스트
    - user_id: User FK
    - created_at: 업로드 날짜
    - caption: 게시글 문구
- **Video:** 포스트의 비디오
    - post_id: Post FK
    - video_url: 비디오 파일 url
- **Image:** 포스트의 이미지
    - post_id: Post FK
    - image_url: 이미지 파일 url
- **Comment:** 댓글
    - post_id: Post FK
    - user_id: User FK
    - content: 댓글 내용
    - created_at: 작성 날짜
- **Like:** 좋아요
    - post_id: Post FK
    - user_id: User FK

### Relations

- User - Profile : 1 대 1. 한 유저는 하나의 프로필만 가지고 있음
- User - Post : 1 대 다. 한 유저는 여러 개의 포스트를 작성할 수 있음
- User - Comment : 1 대 다. 한 유저가 여러 개의 댓글을 작성할 수 있음
- User - Like : 1 대 다. 한 유저가 여러 개의 좋아요를 표시할 수 있음
- Post - Video : 1 대 다. 하나의 게시글에 여러 개의 영상이 포함될 수 있음
- Post - Image : 1 대 다. 하나의 게시글에 여러 개의 사진이 포함될 수 있음
- Post - Comment : 1 대 다. 하나의 게시글에 여러 개의 댓글이 작성될 수 있음
- Post - Like : 1 대 다. 하나의 게시글에 여러 개의 좋아요가 표시될 수 있음

## ORM 이용해보기

### 1. 데이터베이스에 ForeignKey 필드를 포함하는 모델 객체 넣기

- User 및 Profile 객체 생성

![Untitled (1)](https://user-images.githubusercontent.com/71026706/136279065-c4a4dc9f-d89b-4469-ba85-f4da11879e28.png)

- User 객체 불러오기, Post 객체 생성

![Untitled (2)](https://user-images.githubusercontent.com/71026706/136279069-5c3a1060-5028-42d4-a3a6-53e46b444e43.png)

### 2. 삽입한 객체들을 쿼리셋으로 조회해보기

- 전체 Post 객체 쿼리셋으로 조회

![Untitled (3)](https://user-images.githubusercontent.com/71026706/136279157-d4920da2-e804-468f-82d8-fbde8ee2f876.png)

- Like 객체 생성 및 조회

![Untitled (4)](https://user-images.githubusercontent.com/71026706/136279162-977a97d0-4783-4cd5-adda-9a9fe292ca05.png)

### 3. filter 함수 사용해보기

- filter 함수 사용 비교

![Untitled (5)](https://user-images.githubusercontent.com/71026706/136279159-c9bb30d9-40bd-42ee-85fe-652e1d20d3bb.png)

## 회고

제대로 ERD를 그려가면서 데이터 모델링을 해본 적이 처음이라 하면서도 계속 의문이 들고 어려웠다. 데이터 모델링에 대해 자세히 알아보면서 개념적, 논리적 데이터 모델링의 중요성을 깨달을 수 있었다. ORM을 사용해 SQL문을 사용하지 않고 객체지향 형식으로 데이터에 접근할 수 있단 점이 기억에 남는다. 친숙한 방법을 사용하니까 좋았다..🙃🙃
