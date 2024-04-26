from create.models import ResearchResult
from django.db import models

from login.models import SiteUser


class ModificationRecords(models.Model):
    StatusUpdateRecordID = models.AutoField(primary_key=True, verbose_name="状态更新记录ID")
    AchievementID = models.ForeignKey(ResearchResult, on_delete=models.CASCADE, verbose_name="科研成果ID")
    StatusDescription = models.TextField(verbose_name="状态描述")
    StatusUpdateTime = models.DateTimeField(auto_now_add=True, verbose_name="状态更新时间")

    def __str__(self):
        return self.StatusDescription

    class Meta:
        verbose_name = "科研成果状态更新记录"
        verbose_name_plural = "科研成果状态更新记录"
        ordering = ['-StatusUpdateTime']


class ReviewRecords(models.Model):
    Review_Results= [
        ('1', '通过'),
        ('2', '未通过'),
        ('3', '未处理'),
        ]
    ReviewRecordID = models.AutoField(primary_key=True, verbose_name="审核记录ID")
    AchievementID = models.ForeignKey(ResearchResult, on_delete=models.CASCADE, verbose_name="科研成果ID")
    ReviewerID = models.ForeignKey(SiteUser, on_delete=models.CASCADE, verbose_name="审核人员ID")
    ReviewTime = models.DateTimeField(auto_now_add=True, verbose_name="审核时间")
    ReviewResult = models.CharField(max_length=200, choices= Review_Results, default='3',verbose_name="审核结果")
    ReviewComments = models.TextField(verbose_name="审核意见")

    class Meta:
        verbose_name = "科研成果审核记录"
        verbose_name_plural = "科研成果审核记录"
        ordering = ['-ReviewTime']


class TransactionRecords(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('1', '待处理'),
        ('2', '成功'),
        ('3', '失败'),
        # 可以根据需要添加更多状态
    ]
    TransactionID = models.AutoField(primary_key=True, verbose_name="交易ID")
    AchievementID = models.ForeignKey(ResearchResult, on_delete=models.CASCADE, verbose_name="成果ID")
    InitiatorID = models.ForeignKey(SiteUser, on_delete=models.CASCADE, verbose_name="交易发起者ID")
    TransactionTime = models.DateTimeField(auto_now_add=True, verbose_name="交易发起时间")
    TransactionAmount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="交易金额")
    TransactionStatus = models.CharField(max_length=200, choices=TRANSACTION_STATUS_CHOICES, default='1',
                                         verbose_name="交易状态")

    class Meta:
        verbose_name = "科研成果交易记录"
        verbose_name_plural = "科研成果交易记录"
        ordering = ['-TransactionTime']
