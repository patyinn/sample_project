from abc import ABC

from django.contrib.auth.models import User
from rest_framework import serializers
from hotArticle.models import HotArticleModel, RankArticleModel


class RankArticleSerializer(serializers.ModelSerializer):
    pic_name = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = RankArticleModel
        fields = (
            "rank_id",
            "rank",
            "title",
            "content",
            "pic",
            "pic_name",
            "url",
            "url_title",
        )
        read_only_fields = ['rank_id']

    def validate(self, attrs):
        _is_create = not self.instance and not self.parent.instance
        if attrs:
            title = attrs.get('title')
            content = attrs.get('content')
            errors = {}
            if _is_create:
                if not title:
                    errors["title"] = "title field is required in create mode."
                if not content:
                    errors["content"] = "content field is required in create mode."
            if errors:
                raise serializers.ValidationError(errors)
        return attrs


class RankArticleListSerializer(serializers.ListSerializer, ABC):
    child = RankArticleSerializer()

    def save(self, **kwargs):
        hot_instance = kwargs.pop("hot_instance")
        # create rank data
        if self.instance is None:
            r_to_be_created = [
                RankArticleModel(
                    **r,
                    **{
                        "rank_id": f"""{hot_instance.id}_{r["rank"]}""",
                        "hot_article": hot_instance
                    }
                )
                for r in self.validated_data
            ]
            if r_to_be_created:
                RankArticleModel.objects.bulk_create(
                    r_to_be_created,
                    batch_size=len(r_to_be_created),
                    ignore_conflicts=True
                )
        # update or create rank instance
        else:
            r_to_be_update = {}
            for r in self.validated_data:
                r.pop("rank_id", None)
                r_to_be_update.update({
                    f"""{hot_instance.id}_{r["rank"]}""": r
                })

            rank_objs = RankArticleModel.objects.filter(rank_id__in=list(r_to_be_update.keys()))
            for obj in rank_objs:
                if r_to_be_update.get(obj.rank_id):
                    obj.update_data_to_db(**r_to_be_update[obj.rank_id])


class HotArticleSerializer(serializers.ModelSerializer):
    ranks = RankArticleListSerializer(allow_empty=True, required=False, write_only=True)
    rank_list = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")

    class Meta:
        model = HotArticleModel
        fields = (
            "id",
            "date",
            "title",
            "content",
            "cover",
            "picture",
            "url",
            "ranks",
            "rank_list",
            "valid",
            "user",
            "latest_edit_date"
        )
        read_only_fields = [
            "id",
            "latest_edit_date",
        ]

    def get_rank_list(self, obj):
        rank_objs = RankArticleModel.objects.filter(hot_article=obj).order_by("rank")
        return RankArticleListSerializer(rank_objs, allow_empty=True).data

    def save(self, **kwargs):
        _is_create = self.instance is None
        additional_input = {}
        if _is_create:
            additional_input["id"] = HotArticleModel.create_id(self.validated_data["date"])
        else:
            self.validated_data.pop("date", None)
        return super().save(**additional_input)

    def validate(self, attrs):
        _is_create = self.instance is None
        title = attrs.get('title')
        content = attrs.get('content')
        errors = {}
        if _is_create:
            if not title:
                errors["title"] = "title field is required in create mode."
            if not content:
                errors["content"] = "content field is required in create mode."
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class HotArticleSimpleSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")

    class Meta:
        model = HotArticleModel
        fields = "__all__"
