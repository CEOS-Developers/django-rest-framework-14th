# Data Modeling

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
