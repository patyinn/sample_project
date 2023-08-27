import copy
import json
import logging
import base64
from functools import wraps

from django.http import QueryDict
from django.http.response import JsonResponse
from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import BasePermission

from hotArticle.models import HotArticleModel, RankArticleModel
from hotArticle.serializer import HotArticleSerializer, RankArticleListSerializer, HotArticleSimpleSerializer

logger = logging.getLogger(__name__)


class CustomPermission(BasePermission):
    message = "You do not have permission to manipulate object"

    def has_permission(self, request, view):
        condition_list = [
            "hotArticle.add_hotarticlemodel",
            "hotArticle.change_hotarticlemodel",
            "hotArticle.delete_hotarticlemodel",
        ]
        if request.method == "GET" or (
            request.method != "GET" and all(request.user.has_perm(c) for c in condition_list)):
            return True
        return False


def _process_data(func):
    @wraps(func)
    def wrap(*args, **kwargs):

        content, status_code = func(*args, **kwargs)

        response = JsonResponse(content, status=status_code, safe=False)
        return response
    return wrap


# Create your views here.
class HotArticleView(APIView):
    permission_classes = [CustomPermission]

    @_process_data
    def get(self, request, **kwargs):
        try:
            if request.GET.get("all") == "true":
                hot_objs = HotArticleModel.objects.all().order_by("-date", "id")
            else:
                hot_objs = HotArticleModel.objects.filter(valid=True).order_by("-date", "id")
            if not hot_objs:
                return (
                    {
                        "message": "No data"
                    },
                    status.HTTP_200_OK
                )
            hot_serializer = HotArticleSimpleSerializer(hot_objs, many=True)
            return (
                hot_serializer.data,
                status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error happens because of {e}")
            return (
                {
                    "message": f"Error happens because of {e}"
                },
                status.HTTP_400_BAD_REQUEST
            )

    @_process_data
    def post(self, request, **kwargs):
        try:
            request_data_rank = []
            if isinstance(request.data, QueryDict):
                for data in request.data.getlist("ranks", []):
                    data = json.loads(data.replace("'", "\""))
                    if data.get("pic"):
                        data["pic"] = ContentFile(
                            base64.b64decode(data["pic"]),
                            name=data.pop("pic_name", f"{data['rank']}.png")
                        )
                    request_data_rank.append(data)
            ranks_serializer = RankArticleListSerializer(data=request_data_rank)
            if not ranks_serializer.is_valid():
                logger.warning(ranks_serializer.errors)
                return (
                    {
                        "message": ranks_serializer.errors
                    },
                    status.HTTP_400_BAD_REQUEST
                )
            data_input = copy.copy(request.data)
            data_input["user"] = request.user

            hot_serializer = HotArticleSerializer(
                data=data_input,
            )
            if hot_serializer.is_valid():
                hot_instance = hot_serializer.save()
                ranks_serializer.save(hot_instance=hot_instance)
                return (
                    hot_serializer.data,
                    status.HTTP_201_CREATED
                )
            else:
                return (
                    {
                        "message": hot_serializer.errors
                    },
                    status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error happens because of {e}")
            return (
                {
                    "message": f"Error happens because of {e}"
                },
                status.HTTP_400_BAD_REQUEST
            )


class HotArticleDetailView(APIView):
    permission_classes = [CustomPermission, ]

    @_process_data
    def get(self, request, pk, **kwargs):
        try:
            hot_objs = HotArticleModel.objects.get(pk=pk)
            hot_serializer = HotArticleSerializer(hot_objs)
            return (
                hot_serializer.data,
                status.HTTP_200_OK
            )
        except HotArticleModel.DoesNotExist:
            logger.warning(f"hot article id: {pk} doesn't exist, don't assign primary key and post.")
            return (
                {
                    "message": f"hot article id: {pk} doesn't exist, don't assign primary key and post."
                },
                status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error happens because of {e}")
            return (
                {
                    "message": f"Error happens because of {e}"
                },
                status.HTTP_400_BAD_REQUEST
            )

    @_process_data
    def post(self, request, pk, **kwargs):
        try:
            hot_obj = HotArticleModel.objects.prefetch_related("rankarticlemodel_set").get(pk=pk)
            hot_serializer = HotArticleSerializer(hot_obj)

            request_data_rank = []
            if isinstance(request.data, QueryDict):
                for data in request.data.getlist("ranks", []):
                    data = json.loads(data.replace("'", "\""))
                    if data.get("pic"):
                        data["pic"] = ContentFile(
                            base64.b64decode(data["pic"]),
                            name=data.get("pic_name", f"{data['rank']}.png")
                        )
                    request_data_rank.append(data)
            ranks_serializer = RankArticleListSerializer(data=request_data_rank)
            if ranks_serializer.is_valid():
                ranks_serializer.save(hot_instance=hot_obj)
                hot_obj.user = request.user
                hot_obj.save()
                return (
                    hot_serializer.data,
                    status.HTTP_201_CREATED
                )
            else:
                return (
                    {
                        "message": ranks_serializer.errors
                    },
                    status.HTTP_400_BAD_REQUEST
                )
        except HotArticleModel.DoesNotExist:
            logger.warning(f"hot article id: {pk} doesn't exist, don't assign primary key and post.")
            return (
                {
                    "message": f"hot article id: {pk} doesn't exist, don't assign primary key and post."
                },
                status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error happens because of {e}")
            return (
                {
                    "message": f"Error happens because of {e}"
                },
                status.HTTP_400_BAD_REQUEST
            )

    @_process_data
    def put(self, request, pk, **kwargs):
        try:
            hot_obj = HotArticleModel.objects.prefetch_related("rankarticlemodel_set").get(pk=pk)

            data_input = copy.copy(request.data)
            data_input["user"] = request.user

            hot_serializer = HotArticleSerializer(hot_obj, data=data_input)
            if hot_serializer.is_valid():
                instance = hot_serializer.save()
                request_data_rank = []
                if isinstance(request.data, QueryDict):
                    for data in request.data.getlist("ranks", []):
                        data = json.loads(data.replace("'", "\""))
                        if data.get("pic"):
                            data["pic"] = ContentFile(
                                base64.b64decode(data["pic"]),
                                name=data.get("pic_name", f"{data['rank']}.png")
                            )
                        request_data_rank.append(data)
                    ranks_serializer = RankArticleListSerializer(
                        hot_obj.rankarticlemodel_set.all(),
                        data=request_data_rank,
                    )
                    if not ranks_serializer.is_valid():
                        return (
                            {
                                "message": ranks_serializer.errors
                            },
                            status.HTTP_400_BAD_REQUEST
                        )
                    ranks_serializer.save(hot_instance=instance)
                return (
                    hot_serializer.data,
                    status.HTTP_200_OK
                )
            else:
                return (
                    {
                        "message": hot_serializer.errors
                    },
                    status.HTTP_400_BAD_REQUEST
                )
        except HotArticleModel.DoesNotExist:
            logger.warning(f"hot article id: {pk} doesn't exist, don't assign primary key and post.")
            return (
                {
                    "message": f"hot article id: {pk} doesn't exist, don't assign primary key and post."
                },
                status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error happens because of {e}")
            return (
                {
                    "message": f"Error happens because of {e}"
                },
                status.HTTP_400_BAD_REQUEST
            )

    @_process_data
    def delete(self, request, pk, **kwargs):
        try:
            hot_obj = HotArticleModel.objects.get(id=pk)
            rank_objs = RankArticleModel.objects.filter(hot_article__id=pk)
            if hot_obj:
                rank_objs.delete()
                hot_obj.delete()
            return (
                {
                    "message": f"delete entry: {pk} successfully"
                },
                status.HTTP_200_OK
            )
        except HotArticleModel.DoesNotExist:
            logger.warning(f"hot article id: {pk} doesn't exist, don't assign primary key and post.")
            return (
                {
                    "message": f"hot article id: {pk} doesn't exist, don't assign primary key and post."
                },
                status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error happens because of {e}")
            return (
                {
                    "message": f"Error happens because of {e}"
                },
                status.HTTP_400_BAD_REQUEST
            )
