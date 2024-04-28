# Generated by Django 5.0.4 on 2024-04-27 14:14

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
            name='TrackedResearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_time', models.DateTimeField(auto_now_add=True, verbose_name='跟踪时间')),
                ('track_status', models.CharField(choices=[('1', '跟踪中'), ('0', '未跟踪')], default='1', max_length=1, verbose_name='跟踪状态')),
                ('research_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create.researchresult', verbose_name='科研成果')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.siteuser', verbose_name='用户')),
            ],
            options={
                'verbose_name': '跟踪研究',
                'verbose_name_plural': '跟踪研究',
            },
        ),
    ]