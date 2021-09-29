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