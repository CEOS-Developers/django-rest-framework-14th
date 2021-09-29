도커를 설치하고, 세팅하고 AWS랑 연동을 해보기.
먼저 스터디에서 도커 세팅을 했던 것을 복습해보자.


## 사전 준비

먼저, 도커를 설치해야한다.

[MAC 설치](https://docs.docker.com/desktop/mac/install/)
[Window 설치](https://docs.docker.com/desktop/windows/install/)

위에 사이트에서 설치를 하고, 프로젝트 최상단에 `.env.exmaple`파일의 값을 복사해서 `.env` 파일을 만들어 준 후,

```
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
DJANGO_SECRET_KEY={django secret key}
```
[Django Secret Key Generator](https://djecrety.ir)에서 시크릿 키를 생성 후, 중괄호를 지우고 붙여 넣는다.

## 도커 실행

`Pycharm` 터미널 에서 명령어를 수행하기 전에, **`docker-compose.yml` 파일이 있는 폴더에 와 있는지 확인해야한다.**

### 서버와 db 실행

1. 터미널에 `docker-compose -f docker-compose.yml up --build` 명령어를 실행하면, 처음 빌드하는 거면 막 뭐 설치를 오래 할것이고, 아니라면 서버 구동됐다고 뜰것이다.

2. 브라우저에서 `127.0.0.1:8000` 접속 되는지 테스트를 한다. 뒤에 포트번호는 설정에 따라 바뀔 수 있다.

3. `CONTROL-C` 명령어로 서버를 종료하고, `docker-compose -f docker-compose.yml down -v` 명령어를 실행하면 완전히 종료된다.

## 배포

`AWS EC2` 서버와 `RDS DB`와 연동을 할 것인데, 사전 설정은  알아서 잘하기..ㅎㅎ

### `.env.prod` 만들기
프로젝트 최상단에 `.env.prod`를 만들고, 이 내용을 복사해서 넣는다.

```
DATABASE_HOST={RDS db 주소}
DATABASE_DB=mysql
DATABASE_NAME={RDS 기본 database 이름}
DATABASE_USER={RDS User 이름}
DATABASE_PASSWORD={RDS master 비밀번호}
DATABASE_PORT=3306
DEBUG=False
DJANGO_ALLOWED_HOSTS={EC2 서버 ip 주소}
DJANGO_SECRET_KEY={django secret key}
```
안에 보면 `RDS db 주소`랑 `DB 이름`, `User 이름`, `master 비밀번호`, `서버 IP 주소`, `시크릿 키` 를 입력하는 공간이 있다.

미리 설정했던 EC2 서버와 RDS DB에서 이러한 것들을 설정하거나 정보가 있다. 다 찾아서 붙여넣으면 된다.

### Github Action 설정

1. Github Action을 들어가는 방법 : `Settings -> Secrets -> New Repository secrets`  을 들어간다.

2. 설정해야 하는 값들 
 - `ENV_VARS` : `.env.prod`안에 있는 전부 복사하여 붙여넣는다.
 - `HOST` : 배포할 EC2 서버 퍼블릭 DNS(IPv4) 주소. 아까 `.env.prod`에 작성한 주소다.
 - `KEY` : EC2 서버 설정할 때 사용한 `ssh key` (키페어) 값이다.
 
 
 3. `EC2 DNS` 주소로 접속했을 때 Not Found가 뜨면 정상이다. 아니면 주소/admin 을 쳤을때 관리자 페이지가 나오면 정상이다.

## Dockerfile

`Dockerfile`에 대해 알아보자. 이번에 생성한 도커파일은 다음과 같다.
```python
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

### .dockerignore

`dockerfile`을 이용해 Image를 생성 시 동일한 path안에 있는 모든 파일과 디렉토리를 도커 데몬에 전송한다.

그렇다면 불필요한 파일이나 디렉토리가 전송 될 수 있으므로, 깃에 올릴때 `.gitignore` 을 사용하는 것과 같이 도커에도 `.dockerignore`을 사용한다.

#### 사용 방법 
`Dockerfile`과 같은 경로에 `.dockerignore`를 생성하고, 불필요하다고 생각되는 파일과 디렉들을 넣는다.
`Docker`는 `Golang`으로 작성되어, 파일 매칭도 `Golang` 규칙을 따른다고 하니 주의한다.


### FROM
`Docker Daemon`으로 부터 `Image`를 당겨온다.
양식은 
```Python
FROM <image>:<tag> 	// tag가 없는 경우에는 생략 가능
ex ) FROM myubuntu:latest
```

규칙은
1.  FROM절 하나당 image하나만 당겨올 수 있다.
2. build 명령시에 -- 옵션을 사용하면, 마지막 FROM에만 적용된다고 한다.

### RUN

FROM에서 생성한 `Image` 위에서 스크립트 혹은 명령을 실행한다.

#### bash 파일이 있는 경우
```Python
RUN <Instruction>
ex) RUN apt-get install telnet
ex) RUN git clone https://apl.hongik.ac.kr/gitea/Moscato/django_test.git
```
#### bash 파일이 없는 경우
```Python
RUN ["<실행파일>", "<매개 변수1>", ...]
ex) RUN ["apt-get", "install", "telnet"]
ex) RUN ["git", "clone", "https://www.ceos.or.kr"]
```

1. `RUN`으로 실행한 결과는 새 `Image`로 생성되고, 실행내역은 `Histroy`에 기록된다.
2. 해당 명령은 `cache`되어 재사용된다. -> 비슷한 명령 구문끼리 뭉쳐놓으면 속도가 향상될 수 있다.


### ADD vs COPY
파일을 이미지에 추가한다.
```Python
ADD <복사할 파일> <이미지에서 파일을 복사할 경로>

1. <복사할 파일> 이 File 인 경우
ADD hello.txt /
해당 파일을 복사합니다.

2. <복사할 파일> 이 Dir 인 경우
해당 디렉토리의 하위의 모든 파일을 복사합니다.
ADD ./ /hello

3. <이미지에서 파일을 복사할 경로> 이 / 로 끝나는 경우
해당 경로에 파일을 복사합니다.
ADD *.txt /root/

4. <이미지에서 파일을 복사할 경로> 이 이름으로 끝나는 경우
<복사할 파일> 의 이름을 해당 이름으로 변경하여 복사합니다.
ADD hello.sh /copy_hello.sh

5. <이미지에서 파일을 복사할 경로> 를 URL로 설정 가능합니다.
ADD http://test.com/hello.txt /copy_hello.txt

6. <이미지에서 파일을 복사할 경로> 가 .tar.gz 등의 압축파일인 경우
압축을 풀고 tar도 푼 후에 추가합니다.
ADD hello.tar.gz

단, URL인 경우 압축만 풀고 tar 파일 그대로 추가합니다.
ADD http://zlib.net/zlib-1.2.8.tar.gz /
(추가된 파일의 이름은 .tar.gz 이지만 파일내용은 .tar 입니다.)

7. <이미지에서 파일을 복사할 경로> 은 절대경로만 인자로 받습니다.
```
```Python
Error 1)
ADD ../hello.txt /home/hello (X)
COPY /home/hello/hello.txt /home/hello (X)

Why)
1. <복사할 파일> 는 DockerFile과 같은 위치에 존재해야 합니다.
2. <복사할 파일> 는 절대경로를 인자로 받지 않습니다.
```

여기까지는 둘 다 똑같은데, **`COPY`의 다른점**은
```python
COPY <복사할 파일> <이미지에서 파일을 복사할 경로>

기본적인 문법은 ADD와 동일하나, 압축파일을 복사할 때 그대로 옮길 수 있으며, URL을 인자로 받지 못합니다.
```
라고 한다.

