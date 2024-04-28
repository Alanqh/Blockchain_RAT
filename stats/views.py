from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.utils import timezone
from create.models import ResearchResult
from records.models import TransactionRecords

from django.shortcuts import render


def index(request):
    total_research_results_data = total_research_results(request).content
    daily_research_output_data = daily_research_output(request).content
    approval_rate_data = approval_rate(request).content
    research_type_ratio_data = research_type_ratio(request).content
    transaction_stats_data = transaction_stats(request).content

    context = {
        'total_research_results_data': total_research_results_data,
        'daily_research_output_data': daily_research_output_data,
        'approval_rate_data': approval_rate_data,
        'research_type_ratio_data': research_type_ratio_data,
        'transaction_stats_data': transaction_stats_data,
    }

    return render(request, 'stats/stats_board.html', context)


def total_research_results(request):
    total = ResearchResult.objects.count()
    new_today = ResearchResult.objects.filter(UploadTime__date=timezone.now().date()).count()
    return JsonResponse({'total': total, 'new_today': new_today})


def daily_research_output(request):
    week_ago = timezone.now() - timezone.timedelta(days=7)
    data = (ResearchResult.objects.filter(UploadTime__gte=week_ago)
            .annotate(date=TruncDay('UploadTime'))
            .values('date')
            .annotate(count=Count('AchievementID'))  # Use 'AchievementID' instead of 'id'
            .order_by('date'))
    return JsonResponse(list(data), safe=False)

def approval_rate(request):
    total = ResearchResult.objects.count()
    approved = ResearchResult.objects.filter(ResearchStatus='4').count()  # Assuming '4' is the status for approved
    rate = approved / total if total else 0
    return JsonResponse({'rate': rate})


def research_type_ratio(request):
    data = (ResearchResult.objects.values('AchievementType')
            .annotate(count=Count('AchievementID'))  # Use 'AchievementID' instead of 'id'
            .order_by('AchievementType'))
    return JsonResponse(list(data), safe=False)


def transaction_stats(request):
    total_volume = TransactionRecords.objects.count()
    total_amount = TransactionRecords.objects.aggregate(total=Sum('TransactionAmount'))['total'] or 0
    today_volume = TransactionRecords.objects.filter(TransactionTime__date=timezone.now().date()).count()
    today_amount = (TransactionRecords.objects.filter(TransactionTime__date=timezone.now().date())
                    .aggregate(total=Sum('TransactionAmount'))['total'] or 0)
    return JsonResponse({'total_volume': total_volume, 'total_amount': total_amount,
                         'today_volume': today_volume, 'today_amount': today_amount})
