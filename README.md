# Docker와 Github Actions을 이용한 자동 배포

## Docker의 원리

**어떤 OS에서도 같은 환경을 만들어주는 원리**이다. 따라서 서버에 docker만 깔고 배포를 해도 된다.   
-> 서버에 접속해서 docker 실행, master에 푸시 된 커밋을 복사하는 역할을 Github Actions이 해준다   
-> 이 과정을 CD(Continuous Delivery)

## Docker와 docker-compose

docker는 위에서 말한 가상 컨테이너 기술이다. 애플리케이션을 신속하게 구축, 
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
## 컨테이너의 이점

