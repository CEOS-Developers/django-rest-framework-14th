# 2주차
"심화과정 - 무지성에서 지성 되기" 노션으로 공부를 진행했습니다!


# 원리 -> Docker + Github Actions

### => CD (Continuous Delivery) - 지속적 배포   
  
  


## Docker 용도 - 어떤 OS에서도 같은 환경을 만들어준다

> EC2에서 서버를 만들면 ubuntu OS로 아무것도 없는 인스턴스 생성 *( 인스턴스: 클라우드의 가상 서버 )*
>
> -> 서버를 띄우기 위해서는 python, git 등 일일히 설치를 해줘야함
>
> -> 만약 서버를 ubuntu가 아닌 다른 OS로 띄우는 경우, 설치 방법도 달라지기 때문에 일일이 대응 필요
>
> -> 서버와 로컬의 환경도 달라 배포하고 난 후에도 OS 차이로 문제가 생길 수도 있음
>
> => **어떤 OS에서도 같은 환경을 만들어주는 Docker** 사용



## Github Actions 용도 - 1) 서버 접속 후 Docker 실행, 2) master에 push된 commit 복사

> 서버에 접속해서 Docker를 실행
>
> master에 푸시된 커밋을 복사



## Docker vs Docker-compose

Docker: 가상 컨테이너 기술

(* 컨테이너: 도커가 띄운 가상 시스템/ 호스트: 도커를 실행시키고 있는 주체)

|     Docker      |        Docker-compose        |
| :-------------: | :--------------------------: |
| Dockerfile 실행 | docker-compose.yml 파일 실행 |



Dockerfile: 하나의 이미지(구축한 환경의 스냅샷)를 만들기 위한 과정

(이 이미지가 있다면 다른 컴퓨터에서도 똑같은 환경을 올릴 수 있음)

docker-compose: 이 이미지를 여러개 띄워서 네트워크 만들고, 컨테이너 밖의 호스트와 어떻게 연결할지, 파일 시스템은 어떻게 공유할지 제어



## 서버가 뜨는 과정 - GitHub Actions가 docker-compose.prod.yaml 파일을 실행

Github Actions가 실행시키는 파일(deploy.yml)의 마지막 줄의 config/scripts/deploy.sh 파일의 `sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d` 명령어로 서버가 빌드, 실행

(* docker-compose.prod.yaml: prod = production = live = real -> 로컬이 아닌 서버에서 Github Actions에 의해 실행되는 파일)



## docker-compose.prod.yml vs docker-compose.yml

| docker-compose.prod.yml |  docker-compose.yml   |
| :---------------------: | :-------------------: |
|   db 컨테이너가 없다    |  db 컨테이너가 있다   |
|  nginx 컨테이너가 있다  | nginx 컨테이너가 없다 |



## docker-compose.prod.yml 파일에 db 컨테이너가 없는 이유

- 데이터가 날아가거나, 유출될 위험이 있음

- 서버는 대개 상황에 따라 여러 인스턴스를 띄울수도 있고 지울수도 있는데, 서버에 db를 띄우면 다른 서버가 db에 붙지도 못하고 인스턴스를 날리면 데이터도 날아감
- 인스턴스의 자원을 서버와 db가 같이 쓰므로 비효율적
- 만약 서버를 해킹당한다면, 개인정보까지 유출되는 것임



## Nginx?

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



## docker-compose up 의미

최종 실행 코드: 

`sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d`

- up: docker-compose 파일에 정의된 모든 컨테이너를 띄우라는 명령

- --build: up을 할 때마다 새로 build를 강제 수행하도록 하는 파라미터

- -d: daemon 실행

  

up을 한다고 해서 서버가 뜨는 것이 아님! django가 실행되어야 하는데 docker-compose가 django를 어떻게 아는가

→ **<u>command</u>와 <u>entrypoint</u>를 정의**



 Entrypoint와 cmd: 해당 컨테이너가 수행하게 될 실행 명령을 정의하는 선언문

=> 컨테이너가 무슨 일을 하는지 결정하는 최종 단계를 정의하는 명령



## Command

Command를 사용하여 컨테이너 수행 명령을 정의한 경우, 컨테이너를 실행할 때 인자값을 주게 되면 Dockerfile에 지정된 cmd 값을 대신하여 지정한 인자값으로 변경하여 실행됨



## Entrypoint

Entrypoint를 사용하여 컨테이너 수행 명령을 정의한 경우, 해당 컨테이너가 수행될 때 반드시 Entrypoint에서 지정한 명령을 수행되도록 지정됨



## Cmd vs Entrypoint 예제

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



## Command와 Entrypoint의 올바른 사용 방법

1. 컨테이너가 수행될 때 변경되지 않을 실행 명령은 Entrypoint로 정의하는 것이 좋다.

   → 대부분의 컨테이너는 실행될 목적이 분명함

   

2. 메인 명령어 실행 시 default option 인자 값은 cmd로 정의하는 것이 좋다.

   

3. Entrypoint와 cmd는 리스트 포맷(["args1", "args2", ...])으로 정의하는 것이 좋다.



## Github Actions가 수행하는 것

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



## 요약

1. Github Actions가 코드를 서버에 올리고 deploy.sh를 실행

2. deploy.sh는 docker-compose를 실행

3. docker-compose는 web이라는 컨테이너와 nginx라는 컨테이너를 빌드하고 실행
4. web 컨테이너는 Dockerfile.prod를 기준으로 빌드, 이 도커 이미지는 django를 구동하기 위한 환경이 모두 갖춰져있음.



