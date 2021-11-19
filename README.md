## 6주차 과제
### Viewset으로 리팩토링하기
- `APIView` 를 이용한 코드 
  ```python
  class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request, format=None):
        try:
            profile_id = request.data.get('profile_id')
            images_data = request.FILES.getlist('image_files')
            post = Post.objects.create(
                profile=Profile.objects.get(pk=profile_id),
                caption=request.data.get('caption')
            )
            for image_data in images_data:
                Photo.objects.create(post=post, image_file=image_data)
            serializer = PostDetailSerializer(post, many=False)
        except Exception:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status.HTTP_200_OK)

  class PostDetail(APIView):
      def get(self, request, pk, format=None):
          post = Post.objects.get(pk=pk)
          serializer = PostDetailSerializer(post, many=False)
          return JsonResponse(serializer.data, safe=False)
      
      def delete(self, request, pk, format=None):
          post = Post.objects.get(pk=pk)
          post.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
      
      def patch(self, request, pk, format=None):
          post = Post.objects.get(pk=pk)
          serializer = PostDetailSerializer(post, data=request.data, partial=True)
          if serializer.is_valid():
              serializer.save()
              return JsonResponse(serializer.data, safe=False)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  ```
- `viewsets` 을 사용한 코드
  ```python
  class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    serializer_action_classes = {
        'list': PostSerializer,
    }
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
  ```

### filter 기능 구현하기
```python
class PostFilter(FilterSet):
	profile_id = filters.CharFilter(field_name='profile')
	class Meta:
		model = Post
		fields = ['profile_id']

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    serializer_action_classes = {
        'list': PostSerializer,
    }
    queryset = Post.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
```
![Screen Shot 2021-11-19 at 2 19 25 PM](https://user-images.githubusercontent.com/53527600/142569486-833d1e7c-a243-47c3-af94-1486fb790f36.png)
![Screen Shot 2021-11-19 at 2 19 35 PM](https://user-images.githubusercontent.com/53527600/142569494-b8b4ff8a-e577-4312-b668-3687f85bf72f.png)

### 공부한 내용 정리
이때까지 계속 `Post` 모델의 경우는 목록 반환을 위한 `PostSerializer`, `PostDetailSerializer` 두 가지를 사용했다. 이전까지는 요청 별로 처리 로직을 내가 직접 짜야 했기에 내 마음대로 요청에 맞는 `Serializer` 를 골라 사용할 수 있었지만, `viewsets` 은 그런 기능이 모두 내장되어 있어서 쉽지 않았다. 방법을 찾기 위해 검색을 하던 중 한 [포스트](!https://medium.com/aubergine-solutions/decide-serializer-class-dynamically-based-on-viewset-actions-in-django-rest-framework-drf-fb6bb1246af2)에서 `get_serializer_class` 메서드의 존재와 그 메서드의 오버라이딩 방법에 대해 정리되어 있는 것을 발견하게 되었다. 
```python
 class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    # action에 따라 반환될 serializer를 dict 형태로 정리한다
    serializer_action_classes = {
        # action 이름은 drf에서 사전 정의 된 것이어야 한다(list, retrieve 등)
        'list': PostSerializer,
    }
    queryset = Post.objects.all()

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
```
