from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class HotArticleModel(models.Model):
    id = models.CharField("文章編號", max_length=13, primary_key=True, blank=True)
    date = models.DateField("文章日期")
    title = models.CharField("標題", max_length=30, blank=True)
    content = models.TextField("內容", max_length=300, blank=True)
    cover = models.ImageField("封面照片", upload_to='cover', null=True, blank=True)
    picture = models.ImageField("內部照片", upload_to='photos', null=True, blank=True)
    url = models.URLField("頁面連結", max_length=50, blank=True)
    valid = models.BooleanField("是否有效", default=True, blank=True)
    user = models.ForeignKey(User, verbose_name="最後編輯者", on_delete=models.SET_NULL, null=True)
    latest_edit_date = models.DateTimeField("最後編輯日期", auto_now_add=True)

    @classmethod
    def create_id(cls, date):
        obj = HotArticleModel.objects.filter(date=date).order_by("pk").last()
        length = obj.id if obj else "00"
        return f"{date.strftime('%Y%m%d')}HOT{(int(length[-2:])+1):02d}"


class RankArticleModel(models.Model):
    rank_id = models.CharField("排名編號", primary_key=True, max_length=16, blank=True)
    rank = models.PositiveSmallIntegerField("排名", validators=[MinValueValidator(0), MaxValueValidator(10)])
    title = models.CharField("標題", max_length=30, blank=True)
    content = models.TextField("內容", max_length=300, blank=True)
    pic = models.ImageField("相關照片", upload_to='related_pic', null=True, blank=True)
    url = models.URLField("延伸閱讀連結", max_length=50, null=True, blank=True)
    url_title = models.CharField("延伸閱讀標題", max_length=30, null=True, blank=True)

    hot_article = models.ForeignKey(
        HotArticleModel,
        on_delete=models.CASCADE,
    )

    @classmethod
    def create_rank_id(cls):
        return f"{cls.hot_article.id}_{cls.rank}"

    def update_data_to_db(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, "{}".format(k), v)
        self.save()