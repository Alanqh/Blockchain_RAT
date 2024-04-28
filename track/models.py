from django.db import models
from login.models import SiteUser
from create.models import ResearchResult


class TrackedResearch(models.Model):
    TRACKING_STATUS_CHOICES = [
        ('1', '跟踪中'),
        ('0', '未跟踪'),
    ]

    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, verbose_name='用户')
    research_result = models.ForeignKey(ResearchResult, on_delete=models.CASCADE, verbose_name='科研成果')
    track_time = models.DateTimeField(auto_now_add=True, verbose_name='跟踪时间')
    track_status = models.CharField(
        max_length=1,
        choices=TRACKING_STATUS_CHOICES,
        default='1',
        verbose_name='跟踪状态',
    )

    class Meta:
        verbose_name = '跟踪研究'
        verbose_name_plural = '跟踪研究'
