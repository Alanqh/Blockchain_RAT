# Generated by Django 5.0.4 on 2024-04-20 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('create', '0001_initial'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModificationRecords',
            fields=[
                ('StatusUpdateRecordID', models.AutoField(primary_key=True, serialize=False, verbose_name='状态更新记录ID')),
                ('ResearchStatus', models.CharField(choices=[('1', '未审核'), ('2', '已修改'), ('3', '审核中'), ('4', '待交易'), ('5', '交易中'), ('6', '已交易')], default='1', max_length=200, verbose_name='成果状态')),
                ('StatusDescription', models.TextField(verbose_name='状态描述')),
                ('StatusUpdateTime', models.DateTimeField(auto_now_add=True, verbose_name='状态更新时间')),
                ('AchievementID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create.researchresult', verbose_name='科研成果ID')),
            ],
            options={
                'verbose_name': '科研成果状态更新记录',
                'verbose_name_plural': '科研成果状态更新记录',
                'ordering': ['-StatusUpdateTime'],
            },
        ),
        migrations.CreateModel(
            name='ReviewRecords',
            fields=[
                ('ReviewRecordID', models.AutoField(primary_key=True, serialize=False, verbose_name='审核记录ID')),
                ('ReviewTime', models.DateTimeField(auto_now_add=True, verbose_name='审核时间')),
                ('ReviewResult', models.CharField(choices=[('1', '通过'), ('2', '驳回')], default='1', max_length=200, verbose_name='审核结果')),
                ('ReviewComments', models.TextField(verbose_name='审核意见')),
                ('AchievementID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create.researchresult', verbose_name='科研成果ID')),
                ('ReviewerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.siteuser', verbose_name='审核人员ID')),
            ],
            options={
                'verbose_name': '科研成果审核记录',
                'verbose_name_plural': '科研成果审核记录',
                'ordering': ['-ReviewTime'],
            },
        ),
        migrations.CreateModel(
            name='TransactionRecords',
            fields=[
                ('TransactionID', models.AutoField(primary_key=True, serialize=False, verbose_name='交易ID')),
                ('TransactionTime', models.DateTimeField(auto_now_add=True, verbose_name='交易发起时间')),
                ('TransactionAmount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='交易金额')),
                ('TransactionStatus', models.CharField(choices=[('1', '待处理'), ('2', '已完成'), ('3', '失败')], default='1', max_length=200, verbose_name='交易状态')),
                ('AchievementID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create.researchresult', verbose_name='成果ID')),
                ('InitiatorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.siteuser', verbose_name='交易发起者ID')),
            ],
            options={
                'verbose_name': '科研成果交易记录',
                'verbose_name_plural': '科研成果交易记录',
                'ordering': ['-TransactionTime'],
            },
        ),
    ]
