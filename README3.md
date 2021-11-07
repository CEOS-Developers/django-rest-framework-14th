# 3주차

## 모델링 해보기

### 인스타그램 서비스

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
