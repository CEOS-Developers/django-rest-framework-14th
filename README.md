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

장고에서 도커 세팅을 할 때, 여러가지 파일을 만날 수 있는데, 각 파일이 어떤 역할을 하는지 한번 알아보자.

## Dockerfile vs Docker-compse

두 파일 내용이 되게 비슷하게 생겼는데, 무엇이 다른지 알아보자.

### Dockerfile

1.  목적 :
    - `bash image` 파일로 수정된 `image` 를 만드는 일련의 과정들을 정리해 놓은 파일이다.
    - 이 파일을 이용하여 손쉽게 동일한 이미지를 반복해서 만들 수 있다.
    

이미지가 뭐지?? 라는 생각이 들 수 있는데, 도커가 만드는 이미지에 대해서 이해를 하려면 도커의 전반적인 구동 방식을 이해하고 있어야 한다.

도커의 작동원리를 간단히 복습해보자.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9ac8afe7-46ad-4d7b-b933-0366e0cd1d60/Untitled.png)

도커는 가상 머신과 비슷하다고 생각하면 되지만, 큰 차이가 있다.

가상 머신은 OS위에 게스트 OS 전체를 가상화하여 사용하는 방식이기 때문에, 사용하는 컴퓨터의 리소스를 분할하여 사용하여 속도저하가 발생하고, 주변 장치들과 완벽한 호환이 어렵다.

이러한 단점을 개선하기 위해 프로세스를 격리하는 방식을 사용하게 되고, 그 방식을 사용하는 것이 도커이다.

도커는 이 격리 환경을 만들기 위해 리눅스의 `namespace`와 `cgroup` 이라는 기능을 사용한다. 그리고 이 기능들을 사용하며 만들어진 컨테이너를 `LXC`(리눅스 컨테이너) 라고 부른다. 이 기능들에 대한 자세한 설명은 여기로!

[Docker(container)의 작동 원리: namespaces and cgroups](https://tech.ssut.me/what-even-is-a-container/)

도커는 게스트 OS가 필요하긴 하지만, 전체 OS를 가상화하는 방식이 아니기 때문에, 호스트형 가상화 방식에 비해 성능이 많이 향상되었다.

- `컨테이너` : 이미지를 실행한 상태로 볼 수 있고, 변하는 값은 컨테이너에 저장된다.
- `이미지` : 컨테이너 실행에 필요한 파일과 설정 값 등을 포함하고 있는 것.(Immutable) 16진수 ID로 구분되며, 각각의 이미지는 독립적이다.

### Docker-compose

다중 컨테이너 도커 어플리케이션을 정의하고 동작하게 해주는 툴이다. `.yml` 파일로 작성되며, 모든 서비스들의 생성 및 시작을 하나의 명령어로 수행할 수 있게 해준다.

그러니까, 여러 컨테이너 실행을 관리할 수 있게 해주는 것이다.

핵심 명령어를 살펴보자.

- `services` : 하나의 어플리케이션에는 여러 개의 서비스들이 연결되어 사용된다. 예를 들면, 웹 서비스도 필요하고, `spring` 이나 `mysql` 과 같은 DB서버도 필요하다. 이러한 서비스들을 하위 항목에 작성하는 것이다.
- `db : image` :  내 `db` 항목 안에 이미지 설정이 있는데, 이게 왜 있는 거냐면, `docker hub` 에서 이미지를 받아와서 사용할 때 이 설정을 사용하는 것이다.
- `volumes` : 이 항목을 보면 로컬 환경의 경로가 있는데, 데이터베이스는 휘발성 데이터가 아니기 때문에 도커가 종료되거나 다시 실행되더라도 지워지면 안된다. 그러므로 로컬 환경의 폴더와 데이터를 연결하여 파일이 손실되는 것을 막기 위해 사용하는 명령어다.

## Github Actions

### 핵심 개념

소프트웨어 workflow를 자동화할 수 있도록 도와주는 도구.

이것을 이해하기 위해 알아야 하는 개념은 `Workflow` , `Event`, `Job`, `Step`, `Action`, `Runner` 등이 있음.

1. Workflow
- 여러 Job으로 구성되고, Event에 의해 트리거될 수 있는 자동화된 프로세스.
- 최상위 개념이고, `.yml` 이나 `.yaml` 으로 작성되며, 레포지토리의 `.github/workflows` 폴더 아래에 저장된다.

2. Event
- Workflow를 실행(Trigger)하는 특정 활동이나 규칙
- ex) `특정 branch로 Push`, `특정 branch로 Pull Request`, `특정 시간대에 반복(Cron)`, `Webhook을 사용해 외부 이벤트를 통해 실행` 등... 자세한 내용은 아래 링크 참고하자.

[Events that trigger workflows - GitHub Docs](https://help.github.com/en/actions/reference/events-that-trigger-workflows#external-events-repository_dispatch)

3. Job
- 여러 Step으로 구성되고, 가상 환경의 인스턴스에서 실행된다.
- 다른 Job에 의존 관계를 가질 수도 있고, 독립적으로 병렬 실행 할 수도 있다.

4. Step
- Task들의 집합. 커맨드를 날리거나 action을 실행할 수 있음.

5. Action
- Workflow의 가장 작은 블럭이다.
- Job을 만들기 위해 Step들을 연결할 수 있다.
- 재사용이 가능하다.
- 개인적으로 만든 Action을 사용할 수도, Github Marketplace에 있는 공용 Action을 사용할 수도 있다.

6. Runner
- Workflow가 실행될 인스턴스로, `Github Action Runner` 어플리케이션이 설치된 머신이다.
- 직접 호스팅하는 `Self-hosted runner`, 깃헙에서 호스팅해주는 `Github-hosted runner` 로 구분할 수 있다.
- Github-hosted runner는 Azure의 Standard_DS2_v2로 vCPU 2, 메모리 7GB, 임시 스토리지 14GB 이다.

### Workflow 이해하기.

Workflow안에 있는 `.yml` 파일을 하나하나씩 분석해보면서 이해해보자.

- `name` : Workflow의 이름을 지정
- `on` : Event에 대해 작성하는 부분으로, 어떤 조건에 workflow를 trigger할지 작성한다. 단일 event를 사용할 수도, array로 작성할 수도 있다.
- `jobs` : 여러 Job이 있을 경우, **병렬 실행이 Default**다. `runs-on` 은 어떤 OS에서 실행될지를 지정해 주는것이고, steps의 `uses` 는 어떤 액션을 사용할 지 지정하는데, 이미 만들어진 액션을 사용할 때 지정한다.