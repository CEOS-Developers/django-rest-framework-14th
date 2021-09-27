# Docker와 Github Action을 이용한 자동 배포하기



## Docker 의 필요성

[생활코딩 Docker 강의](https://www.youtube.com/playlist?list=PLuHgQVnccGMDeMJsGq2O-55Ymtx0IdKWf)
을 바탕으로 정리한 내용입니다\
앱을 실행하는 여러 방식 중 우리가 사용하는 `컨테이너(Container)` 방식\
컨테이너 기술은 `리눅스` 운영체제에서 동작한다.
- 리눅스 컨테이너(Container) 방식 구조
```
OS
    APP                 # 내가 만든 서비스
    Container           # 웹 서버를 실행하기 위한 컨테이너. 운영체제와는 다른 개념
        Web Server
        lib             # 웹 서버 실행을 위한 라이브러리들
        bin             # 웹 서버 실행을 위한 실행파일들
    Container           # 데이터베이스를 실행하기 위한 컨테이너.
        Database
        lib             # 데이터베이스 실행을 위한 라이브러리들
        bin             # 데이터베이스 실행을 위한 실행파일들
```
- 가상화(ex. VMWare) vs 컨테이너
```
가상화
    운영체제 내 여러 운영체제를 설치 및 실행
    
컨테이너
    동일한 운영체제를 공유
    각 컨테이너는 나머지 부분으로부터 격리되어 실행
    빠른 실행 속도 + 가벼운 환경 유지
```
- 컨테이너화 소프트웨어
```
Docker
AWS Fargate
Google Kubernetes Engine
아마존 ECS
LXC
...등등
```
우리가 개발한 서비스, 환경 등을 개별 컨테이너 이미지로 만들어주는 소프트웨어인 듯 하다.\
이 중 가장 널리 쓰이는 소프트웨어는 `Docker`


