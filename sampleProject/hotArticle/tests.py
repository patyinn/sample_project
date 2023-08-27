import os
import json
import base64
import logging

from datetime import datetime, date
from pprint import pprint

from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User

from rest_framework import status
from rest_framework.test import APIClient

from hotArticle.models import HotArticleModel, RankArticleModel
from hotArticle.views import (
    HotArticleView,
    HotArticleDetailView
)


# Create your tests here.
class AllViewsFunctionTests(TestCase):
    maxDiff = None

    def setUp(self):
        self.user_1 = User.objects.create_superuser(
            username='jacob',
            email='jacob@…',
            password='top_secret'
        )
        self.user_2 = User.objects.create_user(
            username='ccmmm',
            email='ccmmm@…',
            password='not_secret'
        )

        content_type = ContentType.objects.get_for_model(HotArticleModel)
        conditions = [
            "add_hotarticlemodel",
            "change_hotarticlemodel",
            "delete_hotarticlemodel",
            "view_hotarticlemodel"
        ]
        permissions = Permission.objects.filter(
            codename__in=conditions,
            content_type=content_type,
        )
        for perm in permissions:
            self.user_1.user_permissions.add(perm)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)

        self.no_perm_client = APIClient()
        self.no_perm_client.force_authenticate(user=self.user_2)

        self.image_path = os.path.join(".\\other\\測試\\", "3084.png_300.png")
        self.product_obj1 = HotArticleModel.objects.create(
            id="20230910HOT01",
            date=date(2023, 9, 10),
            title="熱門文章1",
            content="熱門文章1內容",
            cover=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            picture=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            url="http://127.0.0.1:8000/hot_article/1",
            user=self.user_1
        )
        self.product_obj2 = HotArticleModel.objects.create(
            id="20230910HOT03",
            date=date(2023, 9, 10),
            title="熱門文章2",
            content="熱門文章2內容",
            cover=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            picture=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            url="http://127.0.0.1:8000/hot_article/2",
            user=self.user_1
        )
        self.product_obj3 = HotArticleModel.objects.create(
            id="20230911HOT04",
            date=date(2023, 9, 11),
            title="熱門文章3",
            content="熱門文章3內容",
            cover=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            picture=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            url="http://127.0.0.1:8000/hot_article/3",
            user=self.user_1,
            valid=False,
        )
        self.product_obj4 = HotArticleModel.objects.create(
            id="20230927HOT01",
            date=date(2023, 9, 27),
            title="熱門文章4",
            content="熱門文章4內容",
            cover=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            picture=None,
            url="http://127.0.0.1:8000/hot_article/4",
            user=self.user_1
        )
        self.product_obj14 = HotArticleModel.objects.create(
            id="20230911HOT14",
            date=date(2023, 9, 11),
            title="熱門文章3",
            content="熱門文章3內容",
            cover=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            picture=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            url="http://127.0.0.1:8000/hot_article/3",
            user=self.user_1
        )
        self.rank_obj1 = RankArticleModel.objects.create(
            rank_id="20230910HOT01_1",
            rank=1,
            title="排名1標題",
            content="排名1內容",
            url="http://127.0.0.1:8000/rank_article/1",
            url_title="延伸閱讀1",
            hot_article=self.product_obj1,
        )
        self.rank_obj4 = RankArticleModel.objects.create(
            rank_id="20230910HOT01_4",
            rank=4,
            title="排名4標題",
            content="排名4內容",
            url="http://127.0.0.1:8000/rank_article/4",
            pic=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            url_title="延伸閱讀4",
            hot_article=self.product_obj1,
        )
        self.rank_obj1 = RankArticleModel.objects.create(
            rank_id="20230911HOT14_1",
            rank=1,
            title="排名1標題",
            content="排名1內容",
            url="http://127.0.0.1:8000/rank_article/1",
            url_title="延伸閱讀1",
            hot_article=self.product_obj14,
        )
        self.rank_obj_271 = RankArticleModel.objects.create(
            rank_id="20230927HOT01_1",
            rank=1,
            title="排名1標題",
            content="排名1內容",
            url="http://127.0.0.1:8000/rank_article/1",
            url_title="延伸閱讀1",
            hot_article=self.product_obj4,
        )
        self.rank_obj_272 = RankArticleModel.objects.create(
            rank_id="20230927HOT01_2",
            rank=2,
            title="排名2標題",
            content="排名2內容",
            url="http://127.0.0.1:8000/rank_article/2",
            pic=SimpleUploadedFile(name='3084.png_300.png', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
            url_title="延伸閱讀4",
            hot_article=self.product_obj4,
        )
        self.rank_obj_273 = RankArticleModel.objects.create(
            rank_id="20230927HOT01_5",
            rank=3,
            title="排名3標題",
            content="排名3內容",
            url="http://127.0.0.1:8000/rank_article/3",
            url_title="延伸閱讀3",
            hot_article=self.product_obj4,
        )
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_no_permission_user(self):
        expected_noprem_result = {
            "detail": "You do not have permission to manipulate object"
        }
        expected_result = {
            "id": "20230910HOT01",
            "date": "2023-09-10",
            "title": "熱門文章1",
            "content": "熱門文章1內容",
            "cover": self.product_obj1.cover.url,
            "picture": self.product_obj1.picture.url,
            "url": "http://127.0.0.1:8000/hot_article/1",
            "rank_list": [
                {
                    "rank_id": "20230910HOT01_1",
                    "rank": 1,
                    "title": "排名1標題",
                    "content": "排名1內容",
                    "pic": None,
                    "url": "http://127.0.0.1:8000/rank_article/1",
                    "url_title": "延伸閱讀1",
                },
                {
                    "rank_id": "20230910HOT01_4",
                    "rank": 4,
                    "title": "排名4標題",
                    "content": "排名4內容",
                    "pic": self.rank_obj4.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/4",
                    "url_title": "延伸閱讀4",
                }
            ],
            "valid": True,
            "user": self.user_1.username,
            "latest_edit_date": self.product_obj1.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        expected_list_result = [
            {
                "id": "20230910HOT01",
                "date": "2023-09-10",
                "title": "熱門文章1",
                "content": "熱門文章1內容",
                "cover": self.product_obj1.cover.url,
                "picture": self.product_obj1.picture.url,
                "url": "http://127.0.0.1:8000/hot_article/1",
                "valid": True,
                "user": self.user_1.username,
                "latest_edit_date": self.product_obj1.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
            {
                "id": "20230910HOT03",
                "date": "2023-09-10",
                "title": "熱門文章2",
                "content": "熱門文章2內容",
                "cover": self.product_obj2.cover.url,
                "picture": self.product_obj2.picture.url,
                "url": "http://127.0.0.1:8000/hot_article/2",
                "valid": True,
                "user": self.user_1.username,
                "latest_edit_date": self.product_obj2.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
            {
                "id": "20230911HOT14",
                "date": "2023-09-11",
                "title": "熱門文章3",
                "content": "熱門文章3內容",
                "cover": self.product_obj14.cover.url,
                "picture": self.product_obj14.picture.url,
                "url": "http://127.0.0.1:8000/hot_article/3",
                "valid": True,
                "user": self.user_1.username,
                "latest_edit_date": self.product_obj14.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
            {
                "id": "20230927HOT01",
                "date": "2023-09-27",
                "title": "熱門文章4",
                "content": "熱門文章4內容",
                "cover": self.product_obj4.cover.url,
                "picture": None,
                "url": "http://127.0.0.1:8000/hot_article/4",
                "valid": True,
                "user": self.user_1.username,
                "latest_edit_date": self.product_obj4.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
        ]

        response = self.no_perm_client.get("/hot/")

        self.assertEqual(json.loads(response.content), expected_list_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.no_perm_client.post("/hot/")

        self.assertEqual(json.loads(response.content), expected_noprem_result)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.no_perm_client.get("/hot/20230910HOT01/")

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.no_perm_client.post("/hot/20230910HOT01/")

        self.assertEqual(json.loads(response.content), expected_noprem_result)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        expected_noprem_result = {
            "detail": "You do not have permission to manipulate object"
        }
        response = self.no_perm_client.put("/hot/20230910HOT01/")

        self.assertEqual(json.loads(response.content), expected_noprem_result)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        expected_noprem_result = {
            "detail": "You do not have permission to manipulate object"
        }
        response = self.no_perm_client.delete("/hot/20230910HOT01/")

        self.assertEqual(json.loads(response.content), expected_noprem_result)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_existed_list_data(self):
        expected_result = [
            {
                "id": "20230910HOT01",
                "date": "2023-09-10",
                "title": "熱門文章1",
                "content": "熱門文章1內容",
                "cover": self.product_obj1.cover.url,
                "picture": self.product_obj1.picture.url,
                "url": "http://127.0.0.1:8000/hot_article/1",
                "valid": True,
                "user": self.user_1.username,
                "latest_edit_date": self.product_obj1.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
            {
                "id": "20230910HOT03",
                "date": "2023-09-10",
                "title": "熱門文章2",
                "content": "熱門文章2內容",
                "cover": self.product_obj2.cover.url,
                "picture": self.product_obj2.picture.url,
                "url": "http://127.0.0.1:8000/hot_article/2",
                "valid": True,
                "user": self.user_1.username,
                "latest_edit_date": self.product_obj2.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
            {
                "id": "20230911HOT14",
                "date": "2023-09-11",
                "title": "熱門文章3",
                "content": "熱門文章3內容",
                "cover": self.product_obj14.cover.url,
                "picture": self.product_obj14.picture.url,
                "url": "http://127.0.0.1:8000/hot_article/3",
                "valid": True,
                "user": self.user_1.username,
                "latest_edit_date": self.product_obj14.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
            {
                "id": "20230927HOT01",
                "date": "2023-09-27",
                "title": "熱門文章4",
                "content": "熱門文章4內容",
                "cover": self.product_obj4.cover.url,
                "picture": None,
                "url": "http://127.0.0.1:8000/hot_article/4",
                "valid": True,
                "user": self.user_1.username,
                "latest_edit_date": self.product_obj4.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
        ]
        response = self.client.get("/hot/")

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_new_hot_article_with_rank(self):
        b64_pic_4 = base64.b64encode(open(self.image_path, 'rb').read()).decode("UTF-8")
        payload = {
            "date": "2023-09-10",
            "title": "熱門文章4",
            "content": "熱門文章4內容",
            "cover": open(self.image_path, 'rb'),
            "picture": open(self.image_path, 'rb'),
            "url": "http://127.0.0.1:8000/hot_article/1",
            "ranks": [
                {
                    "rank": 1,
                    "title": "排名1標題",
                    "content": "排名1內容",
                    "url": "http://127.0.0.1:8000/rank_article/1",
                    "url_title": "延伸閱讀1",
                },
                {
                    "rank": 2,
                    "title": "排名2標題",
                    "content": "排名2內容",
                    "url": "http://127.0.0.1:8000/rank_article/2",
                },
                {
                    "rank": 4,
                    "title": "排名4標題",
                    "content": "排名4內容",
                    "pic": b64_pic_4,
                    "pic_name": "124.jpg",
                    "url": "http://127.0.0.1:8000/rank_article/4",
                    "url_title": "延伸閱讀4",
                },
                {
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "url_title": "延伸閱讀5",
                },
                {
                    "rank": 6,
                    "title": "排名6標題",
                    "content": "排名6內容",
                    "pic": b64_pic_4,
                    "url": "http://127.0.0.1:8000/rank_article/6",
                    "url_title": "延伸閱讀6",
                },
            ],
            "valid": True,
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.post("/hot/", data=payload, headers=headers)

        hot_obj = HotArticleModel.objects.prefetch_related("rankarticlemodel_set").get(pk="20230910HOT04")
        rank_4 = hot_obj.rankarticlemodel_set.get(rank=4)
        rank_6 = hot_obj.rankarticlemodel_set.get(rank=6)
        expected_result = {
            "id": "20230910HOT04",
            "date": "2023-09-10",
            "title": "熱門文章4",
            "content": "熱門文章4內容",
            "cover": hot_obj.cover.url,
            "picture": hot_obj.picture.url,
            "url": "http://127.0.0.1:8000/hot_article/1",
            "rank_list": [
                {
                    "rank_id": "20230910HOT04_1",
                    "rank": 1,
                    "title": "排名1標題",
                    "content": "排名1內容",
                    "pic": None,
                    "url": "http://127.0.0.1:8000/rank_article/1",
                    "url_title": "延伸閱讀1",
                },
                {
                    "rank_id": "20230910HOT04_2",
                    "rank": 2,
                    "title": "排名2標題",
                    "content": "排名2內容",
                    "pic": None,
                    "url": "http://127.0.0.1:8000/rank_article/2",
                    'url_title': None,
                },
                {
                    "rank_id": "20230910HOT04_4",
                    "rank": 4,
                    "title": "排名4標題",
                    "content": "排名4內容",
                    "pic": rank_4.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/4",
                    "url_title": "延伸閱讀4",
                },
                {
                    "rank_id": "20230910HOT04_5",
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "pic": None,
                    "url": None,
                    "url_title": "延伸閱讀5",
                },
                {
                    "rank_id": "20230910HOT04_6",
                    "rank": 6,
                    "title": "排名6標題",
                    "content": "排名6內容",
                    "pic": rank_6.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/6",
                    "url_title": "延伸閱讀6",
                },
            ],
            "valid": True,
            "user": self.user_1.username,
            "latest_edit_date": hot_obj.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertRegex(rank_4.pic.url, r"/media/related_pic/124[_0-9a-zA-Z]{0,}.jpg")
        self.assertRegex(rank_6.pic.url, r"/media/related_pic/6[_0-9a-zA-Z]{0,}.png")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_new_hot_article_without_rank(self):
        payload = {
            "date": "2023-09-12",
            "title": "熱門文章1",
            "content": "熱門文章1內容",
            "url": "http://127.0.0.1:8000/hot_article/1",
            "ranks": [],
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.post("/hot/", data=payload, headers=headers)

        hot_obj = HotArticleModel.objects.get(pk="20230912HOT01")
        expected_result = {
            "id": "20230912HOT01",
            "date": "2023-09-12",
            "title": "熱門文章1",
            "content": "熱門文章1內容",
            "cover": None,
            "picture": None,
            "url": "http://127.0.0.1:8000/hot_article/1",
            "rank_list": [],
            "valid": False,
            "user": self.user_1.username,
            "latest_edit_date": hot_obj.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_hot_article_1(self):
        payload = {
            "title": "熱門文章1",
            "content": "熱門文章1內容",
            "cover": "223",
            "picture": "123",
            "url": "127.0.0.1:8000/hot_article/1",
            "ranks": [],
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.post("/hot/", data=payload, headers=headers)

        expected_result = {
            "message": {
                "url": ["Enter a valid URL."],
                "date": ["This field is required."],
                "cover": ["The submitted data was not a file. Check the encoding type on the form."],
                "picture": ["The submitted data was not a file. Check the encoding type on the form."],
            }
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_invalid_hot_article_2(self):
        payload = {
            "date": "2023-09-13",
            "url": "http://127.0.0.1:8000/hot_article/1",
            "ranks": []
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.post("/hot/", data=payload, headers=headers)

        expected_result = {
            "message": {
                "title": ["title field is required in create mode."],
                "content": ["content field is required in create mode."],
            }
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_existed_data_1(self):
        expected_result = {
            "id": "20230910HOT01",
            "date": "2023-09-10",
            "title": "熱門文章1",
            "content": "熱門文章1內容",
            "cover": self.product_obj1.cover.url,
            "picture": self.product_obj1.picture.url,
            "url": "http://127.0.0.1:8000/hot_article/1",
            "rank_list": [
                {
                    "rank_id": "20230910HOT01_1",
                    "rank": 1,
                    "title": "排名1標題",
                    "content": "排名1內容",
                    "pic": None,
                    "url": "http://127.0.0.1:8000/rank_article/1",
                    "url_title": "延伸閱讀1",
                },
                {
                    "rank_id": "20230910HOT01_4",
                    "rank": 4,
                    "title": "排名4標題",
                    "content": "排名4內容",
                    "pic": self.rank_obj4.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/4",
                    "url_title": "延伸閱讀4",
                }
            ],
            "valid": True,
            "user": self.user_1.username,
            "latest_edit_date": self.product_obj1.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }

        response = self.client.get("/hot/20230910HOT01/")

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_existed_data_2(self):
        expected_result = {
            "id": "20230910HOT03",
            "date": "2023-09-10",
            "title": "熱門文章2",
            "content": "熱門文章2內容",
            "cover": self.product_obj2.cover.url,
            "picture": self.product_obj2.picture.url,
            "url": "http://127.0.0.1:8000/hot_article/2",
            "rank_list": [],
            "valid": True,
            "user": self.user_1.username,
            "latest_edit_date": self.product_obj2.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }

        response = self.client.get("/hot/20230910HOT03/")

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_existed_data(self):
        id = '20230910HOT99'
        expected_result = {
            "message": f"hot article id: {id} doesn't exist, don't assign primary key and post."
        }

        response = self.client.get(f"/hot/{id}/")

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_rank_article(self):
        b64_pic_4 = base64.b64encode(open(self.image_path, 'rb').read()).decode("UTF-8")

        payload = {
            "date": "2023-09-14",
            "title": "熱門文章4",
            "content": "熱門文章4內容",
            "url": "http://127.0.0.1:8000/hot_article/108",
            "ranks": [
                {
                    "rank": 1,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": b64_pic_4,
                    "url": "http://127.0.0.1:8000/rank_article/8",
                    "url_title": "延伸閱讀8",
                },
                {
                    "rank": 3,
                    "title": "排名3標題",
                    "content": "排名3內容",
                },
                {
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "url": "http://127.0.0.1:8000/rank_article/5",
                    "url_title": "延伸閱讀5",
                },
                {
                    "rank": 6,
                    "title": "排名6標題",
                    "content": "排名6內容",
                    "pic": b64_pic_4,
                    "url": "http://127.0.0.1:8000/rank_article/6",
                    "url_title": "延伸閱讀6",
                },
                {
                    "rank": 7,
                    "title": "排名7標題",
                    "content": "排名7內容",
                    "url_title": "延伸閱讀7",
                },
                {
                    "rank": 8,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": b64_pic_4,
                },
            ],
            "valid": True,
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.post("/hot/20230910HOT01/", data=payload, headers=headers)

        hot_obj = HotArticleModel.objects.prefetch_related("rankarticlemodel_set").get(pk="20230910HOT01")

        rank_6 = hot_obj.rankarticlemodel_set.get(rank=6)
        rank_8 = hot_obj.rankarticlemodel_set.get(rank=8)
        expected_result = {
            "id": "20230910HOT01",
            "date": "2023-09-10",
            "title": "熱門文章1",
            "content": "熱門文章1內容",
            "cover": self.product_obj1.cover.url,
            "picture": self.product_obj1.picture.url,
            "url": "http://127.0.0.1:8000/hot_article/1",
            "rank_list": [
                {
                    "rank_id": "20230910HOT01_1",
                    "rank": 1,
                    "title": "排名1標題",
                    "content": "排名1內容",
                    "pic": None,
                    "url": "http://127.0.0.1:8000/rank_article/1",
                    "url_title": "延伸閱讀1",
                },
                {
                    "rank_id": "20230910HOT01_3",
                    "rank": 3,
                    "title": "排名3標題",
                    "content": "排名3內容",
                    "pic": None,
                    "url": None,
                    'url_title': None,
                },
                {
                    "rank_id": "20230910HOT01_4",
                    "rank": 4,
                    "title": "排名4標題",
                    "content": "排名4內容",
                    "pic": self.rank_obj4.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/4",
                    "url_title": "延伸閱讀4",
                },
                {
                    "rank_id": "20230910HOT01_5",
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "pic": None,
                    "url": "http://127.0.0.1:8000/rank_article/5",
                    "url_title": "延伸閱讀5",
                },
                {
                    "rank_id": "20230910HOT01_6",
                    "rank": 6,
                    "title": "排名6標題",
                    "content": "排名6內容",
                    "pic": rank_6.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/6",
                    "url_title": "延伸閱讀6",
                },
                {
                    "rank_id": "20230910HOT01_7",
                    "rank": 7,
                    "title": "排名7標題",
                    "content": "排名7內容",
                    "pic": None,
                    "url": None,
                    "url_title": "延伸閱讀7",
                },
                {
                    "rank_id": "20230910HOT01_8",
                    "rank": 8,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": rank_8.pic.url,
                    "url": None,
                    "url_title": None,
                },
            ],
            "valid": True,
            "user": self.user_1.username,
            "latest_edit_date": self.product_obj1.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_not_exist_article(self):
        b64_pic_4 = base64.b64encode(open(self.image_path, 'rb').read()).decode("UTF-8")

        payload = {
            "date": "2023-09-14",
            "title": "熱門文章4",
            "content": "熱門文章4內容",
            "url": "http://127.0.0.1:8000/hot_article/108",
            "ranks": [
                {
                    "rank": 1,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": b64_pic_4,
                    "url": "http://127.0.0.1:8000/rank_article/8",
                    "url_title": "延伸閱讀8",
                },
                {
                    "rank": 3,
                    "title": "排名3標題",
                    "content": "排名3內容",
                },
                {
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "url": "http://127.0.0.1:8000/rank_article/5",
                    "url_title": "延伸閱讀5",
                },
                {
                    "rank": 6,
                    "title": "排名6標題",
                    "content": "排名6內容",
                    "pic": b64_pic_4,
                    "url": "http://127.0.0.1:8000/rank_article/6",
                    "url_title": "延伸閱讀6",
                },
                {
                    "rank": 7,
                    "title": "排名7標題",
                    "content": "排名7內容",
                    "url_title": "延伸閱讀7",
                },
                {
                    "rank": 8,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": b64_pic_4,
                },
            ],
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.post("/hot/20239910HOT01/", data=payload, headers=headers)

        expected_result = {
            "message": "hot article id: 20239910HOT01 doesn't exist, don't assign primary key and post."
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_invalid_rank_article(self):
        b64_pic_4 = base64.b64encode(open(self.image_path, 'rb').read()).decode("UTF-8")

        payload = {
            "date": "2023-09-14",
            "title": "熱門文章4",
            "content": "熱門文章4內容",
            "url": "http://127.0.0.1:8000/hot_article/108",
            "ranks": [
                {
                    "rank": 1,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": b64_pic_4,
                    "url": "http://127.0.0.1:8000/rank_article/8",
                    "url_title": "延伸閱讀8",
                },
                {
                    "rank": 3,
                    "title": "排名3標題",
                    "content": "排名3內容",
                },
                {
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "url": "http://127.0.0.1:8000/rank_article/5",
                    "url_title": "延伸閱讀5",
                },
                {
                    "rank": 6,
                    "title": "排名6標題",
                    "content": "排名6內容",
                    "pic": b64_pic_4,
                    "url": "http://127.0.0.1:8000/rank_article/6",
                    "url_title": "延伸閱讀6",
                },
                {
                    "rank": 7,
                    "title": "排名7標題",
                    "content": "排名7內容",
                    "url_title": "延伸閱讀7",
                },
                {
                    "rank": 8,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": b64_pic_4,
                },
            ],
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.post("/hot/20230910HOT01/", data=payload, headers=headers)

        hot_obj = HotArticleModel.objects.prefetch_related("rankarticlemodel_set").get(pk="20230910HOT01")
        rank_6 = hot_obj.rankarticlemodel_set.get(rank=6)
        rank_8 = hot_obj.rankarticlemodel_set.get(rank=8)
        expected_result = {
            "id": "20230910HOT01",
            "date": "2023-09-10",
            "title": "熱門文章1",
            "content": "熱門文章1內容",
            "cover": self.product_obj1.cover.url,
            "picture": self.product_obj1.picture.url,
            "url": "http://127.0.0.1:8000/hot_article/1",
            "rank_list": [
                {
                    "rank_id": "20230910HOT01_1",
                    "rank": 1,
                    "title": "排名1標題",
                    "content": "排名1內容",
                    "pic": None,
                    "url": "http://127.0.0.1:8000/rank_article/1",
                    "url_title": "延伸閱讀1",
                },
                {
                    "rank_id": "20230910HOT01_3",
                    "rank": 3,
                    "title": "排名3標題",
                    "content": "排名3內容",
                    "pic": None,
                    "url": None,
                    'url_title': None,
                },
                {
                    "rank_id": "20230910HOT01_4",
                    "rank": 4,
                    "title": "排名4標題",
                    "content": "排名4內容",
                    "pic": self.rank_obj4.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/4",
                    "url_title": "延伸閱讀4",
                },
                {
                    "rank_id": "20230910HOT01_5",
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "pic": None,
                    "url": "http://127.0.0.1:8000/rank_article/5",
                    "url_title": "延伸閱讀5",
                },
                {
                    "rank_id": "20230910HOT01_6",
                    "rank": 6,
                    "title": "排名6標題",
                    "content": "排名6內容",
                    "pic": rank_6.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/6",
                    "url_title": "延伸閱讀6",
                },
                {
                    "rank_id": "20230910HOT01_7",
                    "rank": 7,
                    "title": "排名7標題",
                    "content": "排名7內容",
                    "pic": None,
                    "url": None,
                    "url_title": "延伸閱讀7",
                },
                {
                    "rank_id": "20230910HOT01_8",
                    "rank": 8,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": rank_8.pic.url,
                    "url": None,
                    "url_title": None,
                },
            ],
            "user": self.user_1.username,
            "latest_edit_date": self.product_obj1.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_rank_article(self):
        payload = {
            "ranks": [
                {
                    "rank": 1,
                },
                {
                    "rank": 3,
                    "title": "排名3標題",
                },
                {
                    "rank": 4,
                    "url": "排名5內容",
                },
                {
                    "rank": 5,
                    "content": "排名5內容",
                },
                {
                    "title": "排名6標題",
                    "content": "排名6內容",
                    "pic": "",
                    "url": "http://127.0.0.1:8000/rank_article/6",
                    "url_title": "延伸閱讀6",
                },
            ],
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.post("/hot/20230910HOT01/", data=payload, headers=headers)

        expected_result = {
            "message": [
                {
                    "title": ["title field is required in create mode."],
                    "content": ["content field is required in create mode."],
                },
                {
                    "content": ["content field is required in create mode."],
                },
                {
                    "url": ["Enter a valid URL."],
                },
                {
                    "title": ["title field is required in create mode."],
                },
                {
                    "rank": ["This field is required."],
                    "pic": ["The submitted data was not a file. Check the encoding type on the form."],
                },
            ]
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid_hot_article(self):
        b64_pic_4 = base64.b64encode(open(self.image_path, 'rb').read()).decode("UTF-8")

        payload = {
            "date": "2023-09-30",
            "title": "熱門文章111",
            "content": "熱門文章111內容",
            "cover": "",
            "url": "http://127.0.0.1:8000/hot_article/111",
            "ranks": [
                {
                    "rank_id": "20230927HOT01_4",
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "url": "http://127.0.0.1:8000/rank_article/5",
                    "url_title": "延伸閱讀5",
                },
                {
                    "rank": 1,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": b64_pic_4,
                    "url": "http://127.0.0.1:8000/rank_article/8",
                    "url_title": "延伸閱讀8",
                },
                {
                    "rank_id": "20230927HOT01_16",
                    "rank": 2,
                    "title": "排名121標題",
                    "content": "排名121內容",
                },
                {
                    "rank": 3,
                    "title": "排名11標題",
                    "content": "排名11內容",
                    "url": "http://127.0.0.1:8000/rank_article/11",
                },
            ],
            "user": self.user_2,
            "latest_edit_date": datetime.now()
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.put("/hot/20230927HOT01/", data=payload, headers=headers)

        hot_obj = HotArticleModel.objects.prefetch_related("rankarticlemodel_set").get(pk="20230927HOT01")
        rank_1 = hot_obj.rankarticlemodel_set.get(rank=1)
        rank_2 = hot_obj.rankarticlemodel_set.get(rank=2)
        expected_result = {
            "id": "20230927HOT01",
            "date": "2023-09-27",
            "title": "熱門文章111",
            "content": "熱門文章111內容",
            "cover": None,
            "picture": None,
            "url": "http://127.0.0.1:8000/hot_article/111",
            "rank_list": [
                {
                    "rank_id": "20230927HOT01_1",
                    "rank": 1,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": rank_1.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/8",
                    "url_title": "延伸閱讀8",
                },
                {
                    "rank_id": "20230927HOT01_2",
                    "rank": 2,
                    "title": "排名121標題",
                    "content": "排名121內容",
                    "pic": rank_2.pic.url,
                    "url": "http://127.0.0.1:8000/rank_article/2",
                    'url_title': "延伸閱讀4",
                },
                {
                    "rank_id": "20230927HOT01_5",
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "pic": None,
                    "url": "http://127.0.0.1:8000/rank_article/5",
                    'url_title': "延伸閱讀5",
                },
            ],
            "valid": False,
            "user": self.user_1.username,
            "latest_edit_date": hot_obj.latest_edit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_invalid_hot_article_1(self):
        payload = {
            "date": "2023-09-30",
            "ranks": [
                {
                    "rank": 1,
                    "title": None,
                    "content": None,
                    "pic": None,
                    "url": None,
                    "url_title": None,
                },
                {
                    "rank_id": "20230927HOT01_16",
                    "rank": 2,
                },
                {
                    "rank": 3,
                    "title": "排名11標題",
                    "content": "排名11內容",
                    "url": "27.0.0.1:8000/rank_article/11",
                },
            ],
            "valid": True,
            "user": self.user_2,
            "latest_edit_date": datetime.now()
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.put("/hot/20230927HOT01/", data=payload, headers=headers)

        expected_result = r"""Error happens because of"""

        self.assertRegex(json.loads(response.content)["message"], expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_invalid_hot_article_2(self):
        payload = {
            "date": "2023-09-30",
            "ranks": [
                {
                    "rank": 1,
                    "title": "None",
                    "content": "None",
                    "pic": "None",
                    "url": "None",
                    "url_title": "",
                },
                {
                    "rank_id": "20230927HOT01_16",
                    "rank": 2,
                },
                {
                    "rank": 3,
                    "title": "排名11標題",
                    "content": "排名11內容",
                    "url": "27.0.0.1:8000/rank_article/11",
                },
            ],
            "valid": True,
            "user": self.user_2,
            "latest_edit_date": datetime.now()
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.put("/hot/20230927HOT01/", data=payload, headers=headers)
        expected_result = {
            "message": [
                {
                    "url": ["Enter a valid URL."],
                    "pic": ["Upload a valid image. The file you uploaded was either not an image or a corrupted image."],
                },
                {},
                {
                    "url": ["Enter a valid URL."],
                },
            ]
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_invalid_hot_article_3(self):
        payload = {
            "date": "",
            "title": "",
            "content": "",
            "cover": "fhdjdjfgj",
            "url": "h//127.0.0.1:8000/hot_article/111",
            "ranks": [],
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.put("/hot/20230927HOT01/", data=payload, headers=headers)

        expected_result = {
            'message': {
                'date': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.'],
                'cover': ['The submitted data was not a file. Check the encoding type on the form.'],
                'url': ['Enter a valid URL.']
            }
        }
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_not_exist_hot_article(self):
        b64_pic_4 = base64.b64encode(open(self.image_path, 'rb').read()).decode("UTF-8")

        payload = {
            "date": "2023-09-30",
            "ranks": [
                {
                    "rank_id": "20230927HOT01_4",
                    "rank": 5,
                    "title": "排名5標題",
                    "content": "排名5內容",
                    "url": "http://127.0.0.1:8000/rank_article/5",
                    "url_title": "延伸閱讀5",
                },
                {
                    "rank": 1,
                    "title": "排名8標題",
                    "content": "排名8內容",
                    "pic": b64_pic_4,
                    "url": "http://127.0.0.1:8000/rank_article/8",
                    "url_title": "延伸閱讀8",
                },
                {
                    "rank_id": "20230927HOT01_16",
                    "rank": 2,
                    "title": "排名121標題",
                    "content": "排名121內容",
                },
                {
                    "rank": 3,
                    "title": "排名11標題",
                    "content": "排名11內容",
                    "url": "http://127.0.0.1:8000/rank_article/11",
                },
            ],
            "valid": True,
            "user": self.user_2,
            "latest_edit_date": datetime.now()
        }
        headers = {
            "Content-Type": "multipart/form-data"
        }
        response = self.client.put("/hot/20230911HOT01/", data=payload, headers=headers)

        expected_result = {
            "message": "hot article id: 20230911HOT01 doesn't exist, don't assign primary key and post."
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_exist_article(self):
        response = self.client.delete(f"/hot/{self.product_obj14.pk}/")

        expected_result = {
            "message": f"delete entry: {self.product_obj14.pk} successfully"
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertQuerysetEqual(HotArticleModel.objects.filter(pk=self.product_obj14.pk), [])
        self.assertQuerysetEqual(RankArticleModel.objects.filter(hot_article__pk=self.product_obj14.pk), [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_not_exist_article(self):
        id = "20230991HOT14"

        response = self.client.delete(f"/hot/{id}/")

        expected_result = {
            "message": f"hot article id: {id} doesn't exist, don't assign primary key and post."
        }

        self.assertEqual(json.loads(response.content), expected_result)
        self.assertQuerysetEqual(HotArticleModel.objects.filter(pk=id), [])
        self.assertQuerysetEqual(RankArticleModel.objects.filter(hot_article__pk=id), [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)