### 4주차   

## 1️⃣ 데이터 삽입

- `ORM 쿼리`를 통해 `Post 모델`에 데이터 3개 삽입

![orm](https://user-images.githubusercontent.com/80563849/138105662-921d1b7b-3053-4f19-b11b-bc7c6a6afb95.PNG)

- 모델 선택 및 데이터 삽입

  ```python
  class Post(models.Model):
      post_author = models.ForeignKey(User, on_delete=models.CASCADE)
      location = models.TextField()
      post_content = models.TextField()
      is_comment = models.BooleanField()
      upload_time = models.DateTimeField(auto_now=True)
  
      def publish(self):
          self.upload_time = timezone.now()
          self.save()
  
      def __str__(self):
          return self.post_content
  
      class Meta:
          managed = True
          verbose_name = 'Post'
          verbose_name_plural = 'Posts'
          
          
  class User(AbstractBaseUser):
      username = models.CharField(max_length=100, unique=True)
      USERNAME_FIELD = 'username'
      instagram_id = models.CharField(max_length=100, unique=True)
      is_professional = models.BooleanField(default=False)
  
      objects = UserManager()
  
      class Meta:
          managed = True
          verbose_name = 'User'
          verbose_name_plural = 'Users'
  ```

  ![저장](https://user-images.githubusercontent.com/80563849/138125025-7c183c7a-cf45-4118-a872-88629275788a.PNG)

## 2️⃣ 모든 데이터를 가져오는 API 만들기

- 모든 'Post'의 list를 가져오는 API 요청 결과: `GET`  `api/posts`

![image](https://user-images.githubusercontent.com/80563849/138129310-d1e205e7-0b74-434c-b6f0-edcdbc75a96b.png)



## 3️⃣ 새로운 데이터를 create하도록 요청하는 API 만들기

- Post를 추가하는 API 요청 결과: `POST` `api/posts/` 

- Body: `{"post_content" : "happy", "location" : "Namyangju"}`

  ![image](https://user-images.githubusercontent.com/80563849/138139771-7500ec46-71c2-4fb7-b55d-6dfb525704cb.png)



## 4️⃣ 회고

가장 오래 걸렸던 과제였던 것 같다. 아직 완벽하게 이해가 된 것 같지 않아서 날 잡고 열심히 공부해야겠다..😥 erd와 변경된 model을 3주차 README에 반영해야겠다.



## ☑ 참고

- `django.db.utils.IntegrityError` 에러가 발생한 경우: 에러가 발생한 **필드가 null 값이 되지 않도록 값 필수로 설정**

- POSTMAN으로 POST api 작성 방법: [POST api - Body->raw](https://meetup.toast.com/posts/107) (param으로 값을 입력해서 호출한 경우, 

  `rest_framework.exceptions.parseerror: json parse error - expecting value: line 1 column 1 (char 0)` 에러가 발생했음)

- `'manager' object has no attribute 'get_by_natural_key'` 에러가 발생한 경우: User 클래스에 `objects = UserManager()` 추가 (**AbstractBaseUser로 custom user를 생성한 경우** **UserManager 필수**로 선언, 추가)

- [verbose name이란](https://djangojeng-e.github.io/2020/08/02/Django-Models-6%ED%8E%B8-Fields-verbose-field-names/)
