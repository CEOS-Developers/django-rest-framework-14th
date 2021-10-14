from rest_framework import status
from rest_framework.test import APITestCase, DjangoClient
from django.contrib.auth.models import User
from .models import Profile


def temporary_images():
    import tempfile
    from PIL import Image

    images = []
    for i in range(5):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, 'jpeg')
        tmp_file.seek(0)
        images.append(tmp_file)
        
    return images


class PostTest(APITestCase):
    def setUp(self):
        self.client = DjangoClient()
        test_user = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.profile = Profile.objects.create(user=test_user, account_name='accountttt', bio='thisisbio')

    def test_photo(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {
            'profile_id': self.profile.id,
            'caption': 'photo test',
            'image_files': temporary_images()
        }
        response = self.client.post("/api/posts/", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CommentTest(APITestCase):
    def setUp(self):
        self.client = DjangoClient()
        test_user = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.profile = Profile.objects.create(user=test_user, account_name='accountttt', bio='thisisbio')

    def test_comment(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {
            'post_id': 2,
            'account_name': self.profile.account_name,
            'content': 'test value'
        }
        response = self.client.post("/api/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)