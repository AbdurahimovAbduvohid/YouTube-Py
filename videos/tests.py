from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from videos.models import Video, Comment, LikeDislike
from django.core.files.uploadedfile import SimpleUploadedFile


class VideoAPITest(APITestCase):
    @staticmethod
    def check_email(email):
        if '@' not in email or '.' not in email:
            raise ValueError("failed email")
        return email

    @staticmethod
    def check_password(password):
        if len(password) < 4:
            raise ValueError("password must be at least 4 characters.")
        return password

    @staticmethod
    def check_text(field_name, value, max_length=255):
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be less than {max_length} characters")
        return value

    @classmethod
    def setUpTestData(cls):
        print("\n=== enter user details ===")
        email = cls.check_email(input("Email: ").strip())
        password = cls.check_password(input("Password: ").strip())
        name = cls.check_text("Name", input("Name: ").strip())
        surname = cls.check_text("Surname", input("Surname: ").strip())

        # create user
        cls.user = CustomUser.objects.create_user(
            email=email,
            password=password,
            name=name,
            surname=surname
        )

        print("\n=== enter video details ===")
        title = input("Video title: ").strip() or "Test Video"
        description = input("Video description: ").strip() or "Test Description"

        # create video
        cls.video = Video.objects.create(
            user=cls.user,
            title=title,
            description=description,
            file=SimpleUploadedFile(
                "360p.mp4",
                b"test_content",
                content_type="video/mp4",

            ),
            low_quality=SimpleUploadedFile(
                "144p.mp4",
                b"test_content",
                content_type="video/mp4",

            ),
            high_quality=SimpleUploadedFile(
                "1080p.mp4",
                b"test_content",
                content_type="video/mp4",

            ),
        )
        print("\n=== starting test ===")

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_all_video_operations(self):
        # video create
        url = reverse('video-list')
        data = {
            'title': 'New ' + self.video.title,
            'description': 'New ' + self.video.description,
            'file': SimpleUploadedFile("360p.mp4", b"test_content", content_type="video/mp4"),
            'low_quality': SimpleUploadedFile("144p.mp4", b"test_content", content_type="video/mp4"),
            'high_quality': SimpleUploadedFile("1080p.mp4", b"test_content", content_type="video/mp4")
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("✓ Video creation test passed")

        # video listing
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Original + New video
        print("✓ Video list test passed")

        # video detail
        url = reverse('video-detail', args=[self.video.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✓ Video detail test passed")

        print("\n=== success ===")
