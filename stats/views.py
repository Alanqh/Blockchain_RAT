

from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncDate
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from create.models import ResearchResult
from login.models import SiteUser
from records.models import TransactionRecords, ModificationRecords, ReviewRecords
from track.models import TrackedResearch


def get_stats(request):
    # Get the count of user
    user_count = SiteUser.objects.count()

    # Get user count by type
    user_count_by_type = SiteUser.objects.values('usertype').annotate(count=Count('id'))

    # Get recent user registration trend
    recent_users = SiteUser.objects.filter(create_time__gte=timezone.now()-timezone.timedelta(days=10))
    recent_user_count = recent_users.count()
    recent_user_trend = recent_users.annotate(date=TruncDay('create_time')).values('date').annotate(count=Count('id'))

    # Get the count of research result
    research_result_count = ResearchResult.objects.count()
    # Get the count of research results by type
    research_results_by_type = ResearchResult.objects.values('AchievementType').annotate(count=Count('AchievementID'))
    # Get the list of recently published research results

    recent_research_results = ResearchResult.objects.order_by('-UploadTime')[:5]  # adjust the number as needed
    total_research_results = ResearchResult.objects.all()
    # Prepare data for Chart.js


    # Calculate the approval rate
    total_reviews = ReviewRecords.objects.count()
    approved_reviews = ReviewRecords.objects.filter(ReviewResult='1').count()
    approval_rate = approved_reviews / total_reviews if total_reviews > 0 else 0

    # 计算成功交易量和交易总额
    recent_successful_transactions = TransactionRecords.objects.filter(TransactionStatus='2').order_by(
        '-TransactionTime')[:5]  # adjust the number as needed
    total_successful_transactions = TransactionRecords.objects.filter(TransactionStatus='2')
    successful_transactions = TransactionRecords.objects.filter(TransactionStatus='2').count()
    total_transaction_amount = TransactionRecords.objects.filter(TransactionStatus='2').aggregate(
        total_amount=Sum('TransactionAmount'))['total_amount']

    # 计算日活
    daily_activity = ModificationRecords.objects.filter(
        StatusUpdateTime__gte=timezone.now() - timezone.timedelta(days=10)).annotate(
        date=TruncDate('StatusUpdateTime')).values('date').annotate(count=Count('AchievementID'))

    data = {
        'user_count': user_count,
        'user_count_by_type': list(user_count_by_type),
        'recent_user_count': recent_user_count,
        'recent_user_trend': list(recent_user_trend),

        'research_result_count': research_result_count,
        'research_results_by_type': list(research_results_by_type),
        'recent_research_results': recent_research_results,
        'total_research_results': total_research_results,




        'approval_rate': approval_rate,
        'disapproval_rate': 1 - approval_rate,

        'recent_successful_transactions': recent_successful_transactions,
        'total_successful_transactions': total_successful_transactions,
        'successful_transactions': successful_transactions,
        'total_transaction_amount': int(total_transaction_amount),

        'daily_activity': list(daily_activity),

    }

    return render(request, 'stats/stats_board.html', data)

