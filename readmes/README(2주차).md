# Docker와 GitHub Actions를 이용한 자동배포
### 컨테이너 VS 가상머신
- 가상머신: 하드웨어를 소프트웨어로 에뮬레이션
  - 시스템 분리를 통한 프로세스 격리 관점에서는 장점을 가짐
  - 단순히 프로세스를 실행하기 위한 환경으로서는 성능을 비롯한 여러 단점을 가짐
- 컨테이너: 하드웨어를 소프트웨어로 재구현하는 가상머신과는 달리 프로세스의 실행 환경을 격리함
  - 컨테이너가 실행되고 있는 호스트(서버) 입장에서 컨테이너는 단순히 **프로세스** 에 불과
  - 그러나 사용자나 컨테이너 입장에서는 호스트와는 무관하게 동작하는 가상머신처럼 보임
  - 따라서 **컨테이너형 가상화** 라고 불리기도 함
## Docker
- 2013년에 등장한 컨테이너형 가상화 도구
- 운영체제 상에서 지원하는 방법을 통해서 하나의 프로세스(컨테이너)를 실행하기 위한 별도의 환경을 구축
- 프로세스를 격리시켜 실행해주는 도구라고 할 수 있음
### Docker의 구조
- Client: user가 `docker run` 등의 명령어를 입력하면 이를 Server 쪽에 전송하고, 이를 Docker daemon이 수행
- Docker daemon: docker api 요청을 수신하고 image, container, network, volume과 같은 docker object를 관리하며, 다른 docker daemon과의 통신을 통해 서비스를 관리할 수 있음
- Docker Registry: Docker 이미지 저장소
- Image: 컨테이너 실행에 필요한 파일과 설정값 등을 포함하고 있음(공식 이미지의 경우 해당 이미지를 실행하기 위한 모든 것이 세팅되어 있음)
### 이미지
- 어떤 애플리케이션을 실행하기 위한 환경(= 파일들의 집합)
- 도커에서는 어플리케이션을 실행하기 위한 파일들을 모아놓고, 해당 모아놓은 파일들을 어플리케이션과 함께 이미지로 만들 수 있음
- 이렇게 만든 이미지를 기반으로 어플리케이션을 바로 배포할 수도 있음
### 이미지 VS 컨테이너
- 이미지: 미리 구성된 환경을 저장해 놓은 파일들의 집합
- 컨테이너: 이러한 이미지를 기반으로 실행된 격리된 프로세스
- 컨테이너를 사용, 수정해도 이미지에는 영향을 미치지 않음
  - 윈도우 CD로 윈도우를 설치해서 사용한다고 설치한 윈도우 CD에 어떤 변화가 생기지는 않는 것과 같은 이치
  - 도커에서 이미지는 immutable한 저장 매체
  - 대신 도커에서는 이 이미지 위에 무언가를 더해서 새로운 이미지를 만들어내는 일이 가능
## 왜 굳이 컨테이너를 써야 하나?
- 컨테이너를 간단히 설명하면 애플리케이션을 환경에 구애 받지 않고 실행하는 기술이라고 할 수 있음
- 똑같은 일을 하는 두 서버가 있다 해도, A 서버는 한 달 전에 구성했고 B 서버는 이제 막 구성했다면 운영체제부터 컴파일러와 설치된 패키지까지 완벽하게 같기는 쉽지 않음 → 이러한 차이점들이 장애를 야기할 수 있음
- 따라서 서버의 운영 기록을 코드화하려는 다양한 시도들이 등장 → Ansible 등
### Ansible VS Docker
1. imagemagick 을 설치하는 Ansible Playbook 코드
    ```yaml
    # code by https://github.com/treetips/ansible-playbook-imagemagick/blob/master/main.yml
    ---
    # ansible v2.0.0.2
    - hosts: all
      become: no
      vars:
        - autoconf_dir_name: "autoconf-latest"
        - autoconf_archive_name: "{{ autoconf_dir_name }}.tar.gz"
        - autoconf_dl_url: "http://ftp.gnu.org/gnu/autoconf/{{ autoconf_archive_name }}"
        - imageMagick_dir_name: "ImageMagick-latest"
        - imageMagick_archive_name: "ImageMagick.tar.gz"
        - imageMagick_dl_url: "http://www.imagemagick.org/download/{{ imageMagick_archive_name }}"
      tasks:
    
    (중략)
    
        - block:
          - name: downlaod imagemagick
            get_url: url={{ imageMagick_dl_url }}  dest=/usr/local/src/{{ imageMagick_archive_name }}
    
          - name: unarchive imagemagick archive
            shell: chdir=/usr/local/src mkdir -p {{ imageMagick_dir_name }} && tar xzvf {{ imageMagick_archive_name }} -C {{ imageMagick_dir_name }} --strip-components 1
    
          # see configure options http://www.imagemagick.org/script/advanced-unix-installation.php
          - name: configure imagemagick
            shell: chdir=/usr/local/src/{{ imageMagick_dir_name }} ./configure
    
          - name: make imagemagick
            shell: chdir=/usr/local/src/{{ imageMagick_dir_name }} make
    
          - name: make imagemagick
            shell: chdir=/usr/local/src/{{ imageMagick_dir_name }} make install
          when: imagemagick_archive.stat.exists == False
          become: yes
    ```
2. imagemagick 을 설치하는 이미지를 만드는 Dockerfile
    ```dockerfile
      FROM debian:stretch-slim
    
      RUN apt-get update \
          && apt-get install -y \
          imagemagick
    ```
- 도커 파일 = 서버 운영 기록 코드화
- 도커 이미지 = 도커 파일 + 실행 시점
- 앞서 살펴본 Ansible Playbook 으로 서버에 imagemagick을 설치한다고 가정
  - 작업자가 1년 전에 이 Playbook 으로 서버 A를 구성했고, 오늘 서버 B를 구성한다면, 두 서버에 대해 이미지매직이 설치된 시점은 1년의 차이가 발생
- 도커를 통해 imagemagick을 설치한다고 가정
  - 도커에서는 앞서 살펴본 도커 파일로 이미지를 만들어 두면 서버가 구성되는 시점이 이미지를 만든 시점으로 고정됨 → 이 이미지를 사용해 1년 전에 A 서버에 컨테이너를 배포하고 오늘 B 서버에 컨테이너를 배포한다고 해도 두 컨테이너 모두 imagemagick이 설치된 시점은 같음
- 도커의 타 서버 구성 도구와의 차별점: 다른 도구들은 모두 도구를 실행하는 시점에 서버의 상태가 결정되는 데 비해 도커는 작업자가 그 시점을 미리 정해둘 수 있음 → 덕분에 **서버를 항상 똑같은 상태로 만들 수 있음**
### 결론: 도커를 쓰는 이유
- 서버 제작 과정에 견고함과 유연성을 더함
- 다른 이가 만든 서버를 소프트웨어 사용하듯 가져다 쓸 수 있음
- 여러 대에 배포할 수 있는 확장성을 갖춤
- 담당자가 바뀌었을 때 서버 운영 기록을 인계하는 데에 소비되는 시간이 줄어듦
## Docker와 docker-compose
- 도커로 개발 환경을 구성하는 데에 존재했던 불편한 부분들
  - 장황한 옵션: 개발 서버를 실행할 때마다 장황한 도커 명령어의 옵션들을 적어야 함
  - 앱 컨테이너와 데이터베이스 컨테이너의 실행 순서: 반드시 데이터베이스 컨테이너를 실행한 다음에 앱 컨테이너를 실행해야 함 → 그렇지 않으면 앱 컨테이너에서 데이터베이스 컨테이너를 찾을 수 없음
- 도커 컴포즈: 독립된 개발 환경을 빠르게 구성할 수 있음
  - 도커 컴포즈를 사용하면 컨테이너 실행에 필요한 옵션을 `docker-compose.yml` 이라는 파일에 적어둘 수 있고 컨테이너 간 실행 순서나 의존성도 관리할 수 있음
## Github Actions
- Github Actions: Github에서 제공하는 워크플로우(workflow)를 자동화하도록 도와주는 도구 → 테스트, 빌드, 배포 등의 다양한 작업들을 자동화하여 처리
### Github Actions의 구성
- 워크 플로우(workflows)
  - 저장소에 추가하는 자동화된 프로세스
  - 하나 이상의 job으로 이루어져 있으며 이벤트에 의해 실행
- 이벤트(Events)
  - 워크 플로우를 실행하는 특정 활동이나 규칙
  - 커밋의 push, pull request가 생성되었을 때뿐만 아니라 [저장소 dispatch event](https://docs.github.com/en/rest/reference/repos#create-a-repository-dispatch-event)를 통해 Github 외부에서 발생하는 활동으로도 이벤트를 발생시킬 수도 있음
  - schedule에 POSIX cron 문법으로 스케쥴 이벤트를 발생시킬 수도 있음
- 러너(runners)
  - Github 액션 러너 애플리케이션이 설치된 서버
  - Github에서 호스팅 하는 러너를 사용할 수도 있고 직접 호스팅 할 수도 있음
  - Github에서 호스팅 하는 러너는 Ubuntu Linux, Windows, macOS 환경을 기반으로 하며 워크 플로우의 각 작업은 새로운 가상 환경에서 실행함
- 작업(jobs)
  - 워크플로우의 기본 단위
  - 더 작은 단위인 스텝(step)으로 이루어져 있음 
  - 기본적으로 워크 플로우는 여러 작업을 병렬적으로 실행하며, 순차적으로 실행하도록 설정할 수도 있음
- 스텝(steps)
  - 작업에서 커맨드를 실행하는 독립적인 단위
  - 한 작업(job)의 각 스텝들은 동일한 러너에서 실행되므로 해당 작업의 액션들은 서로 데이터를 공유함
- 액션(actions)
  - 워크 플로우의 가장 작은 요소
  - 직접 만들어 사용할 수도 있고 마켓에 등록된 이미 만들어진 것을 가져와 사용할 수도 있음
### 워크 플로우 관리
- 민감한 정보 저장: 워크 플로우가 비밀번호나 인증서 같은 민감한 정보를 사용한다면 Github에 secret으로 저장하여 환경 변수로 사용 가능
  ```yaml
  jobs:
    example-job:
      runs-on: unbuntu-latest
      steps:
        - name: Retrieve secret
          # 환경변수로 저장하고
          env:
            super_secret: ${{ secrets.SUPERSECRET }}
          # 저장한 환경변수를 활용한다.
          run: |
            example-command "$super_secret"
  ```
- 의존적인 작업 구성: 기본적으로 작업은 병렬적으로 수행 → 다른 작업이 완전히 끝난 후에 작업을 실행시키고 싶다면 needs 키워드를 통해 작업이 의존성을 갖도록 지정하면 됨
    ```yaml
    # needs 키워드를 통해 build, test 작업이 각각 이전 작업인 setup, build 작업이 끝난 후에 실행되도록 설정
    jobs:
      setup:
        runs-on: ubuntu-latest
        steps:
          - run: ./setup_server.sh
      build:
        needs: setup
        runs-on: ubuntu-latest
        steps:
          - run: ./build_server.sh
      test:
        needs: build
        runs-on: ubuntu-latest
        steps:
          - run: ./test_server.sh
    ```
- 빌드 매트릭스 활용: 워크 플로우가 다양한 OS, 플랫폼, 언어의 여러 조합에서 테스트를 실행하려는 경우 빌드 매트릭스를 활용하면 됨 → 빌드 옵션을 배열로 받는 strategy 키워드 사용
    ```yaml
    jobs:
      build:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            # 다양한 버전의 Node.js를 이용하여 작업을 여러번 실행
            node: [6, 8, 10]
        steps:
          - uses: actions/setup-node@v1
            with:
              node-version: ${{ matrix.node }}
    ```
- 종속성 캐싱: Github의 러너는 각 작업에서 새로운 환경으로 실행되므로 작업들이 종속성을 재사용하는 경우 파일들을 캐싱하여 성능을 높일 수 있음(캐시를 생성하면 해당 저장소의 모든 워크 플로우에서 사용 가능)
    ```yaml
    jobs:
      example-job:
        steps:
          - name: Cache node modules
            uses: actions/cache@v2
            env:
              cache-name: cache-node-modules
            with:
              # `~/.npm` 디렉토리를 캐시해 성능을 높인다
              path: ~/.npm
              key: ${{ runner.os }}-build-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}
              restore-keys: |
                ${{ runner.os }}-build-${{ env.cache-name }}-
    ```
### 참고 자료
- [Docker의 이해 - KT Cloud 매뉴얼](https://cloud.kt.com/portal/user-guide/education-eduadvanced-edu_adv_2)
- [도커(Docker) 입문편 - 컨테이너 기초부터 서버 배포까지](https://www.44bits.io/ko/post/easy-deploy-with-docker)
- [왜 굳이 도커(컨테이너)를 써야 하나요? - 눈송이 서버의 한계를 넘어 컨테이너를 사용해야 하는 이유](https://www.44bits.io/ko/post/why-should-i-use-docker-container)
- [도커 컴포즈를 활용하여 완벽한 개발 환경 구성하기 - 컨테이너 시대의 Django 개발환경 구축하기](https://www.44bits.io/ko/post/almost-perfect-development-environment-with-docker-and-docker-compose)
- [Github Actions으로 배포 자동화하기](https://meetup.toast.com/posts/286)