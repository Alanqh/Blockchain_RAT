import os

from django.db import models

from login.models import SiteUser


class ResearchResult(models.Model):
    ACHIEVEMENT_TYPE_CHOICES = [
        ('1', '论文'),
        ('2', '专利'),
        ('3', '软件'),
        ('4', '技术报告'),
        # 可以根据需要添加更多类型
    ]
    STATUS_CHOICES = [
        ('1', '未审核'),
        ('2', '已修改'),
        ('3', '审核中'),
        ('4', '待交易'),
        ('5', '交易中'),
        ('6', '已交易'),
        # 可以根据需要添加更多状态
    ]
    AchievementID = models.AutoField(primary_key=True, verbose_name="成果ID")
    UserID = models.ForeignKey(SiteUser, on_delete=models.CASCADE, verbose_name="用户ID")
    Title = models.CharField(max_length=200, verbose_name="标题")
    Author = models.CharField(max_length=200, verbose_name="作者")
    Ownership = models.CharField(max_length=200, verbose_name="所有权归属")
    Abstract = models.TextField(verbose_name="摘要")
    Keywords = models.CharField(max_length=200, verbose_name="关键词")
    AchievementType = models.CharField(max_length=200, choices=ACHIEVEMENT_TYPE_CHOICES, default='1',
                                       verbose_name="成果类型")
    ResearchStatus = models.CharField(max_length=200, choices=STATUS_CHOICES, default='1', verbose_name="成果状态")

    # 定价,2位小数

    Price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="定价")
    UploadTime = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    ReadingCount = models.IntegerField(default=0, verbose_name="被查看次数")
    CitingCount = models.IntegerField(default=0, verbose_name="被引用次数")

    def __str__(self):
        return self.Title + ' by ' + self.Author

    class Meta:
        verbose_name = "科研成果"
        verbose_name_plural = "科研成果"
        ordering = ['-UploadTime']


def get_upload_to(instance, filename):
    return '{0} by {1}/{2}'.format(instance.research_result.Title, instance.research_result.Author, filename)


class ResearchFile(models.Model):
    file = models.FileField(upload_to=get_upload_to, verbose_name="附件")
    research_result = models.ForeignKey(ResearchResult, related_name='files', on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        verbose_name = "科研成果附件"
        verbose_name_plural = "科研成果附件"
        ordering = ['-id']
