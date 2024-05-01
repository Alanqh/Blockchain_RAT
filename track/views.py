from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from login.models import SiteUser
from .models import TrackedResearch
from create.models import ResearchResult

from records.models import ModificationRecords, TransactionRecords

from django.core.paginator import Paginator


def index(request):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    research_results = ResearchResult.objects.filter(ResearchStatus__in=['4', '5', '6'])

    for result in research_results:
        result.is_tracked = TrackedResearch.objects.filter(user=user, research_result=result, track_status='1').exists()
    # Create a Paginator object
    paginator = Paginator(research_results, 3)  # Show 10 research_results per page
    # Get the page number from the query string
    page_number = request.GET.get('page')
    # Get the Page object for the current page
    page_obj = paginator.get_page(page_number)
    return render(request, 'track/research_results.html', {'page_obj': page_obj})


def start_tracking(request, research_id):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    try:
        research = ResearchResult.objects.get(AchievementID=research_id)
    except ResearchResult.DoesNotExist:
        # Handle the case where the research does not exist
        return redirect('index')
    tracked_research = TrackedResearch.objects.filter(user=user, research_result=research)
    if tracked_research.exists():
        # If the research is already tracked but the status is '0', update it to '1'
        tracked_research.update(track_status='1')
    else:
        TrackedResearch.objects.create(user=user, research_result=research)
    ModificationRecords.objects.create(AchievementID=research, StatusDescription=f'{user}开始跟踪{research}')
    return redirect('index')


def stop_tracking(request, research_id):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    try:
        research = ResearchResult.objects.get(AchievementID=research_id)
    except ResearchResult.DoesNotExist:
        # Handle the case where the research does not exist
        return redirect('index')
    tracked_research = TrackedResearch.objects.filter(user=user, research_result=research)
    if tracked_research.exists():
        # If the research is already tracked and the status is '1', update it to '0'
        tracked_research.update(track_status='0')
        ModificationRecords.objects.create(AchievementID=research, StatusDescription=f'{user}停止跟踪{research}')
    return redirect('index')


def my_tracked_research(request):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    tracked_researches = TrackedResearch.objects.filter(user=user, track_status='1')
    research_results = [tracked_research.research_result for tracked_research in tracked_researches]

    # 创建一个Paginator对象
    paginator = Paginator(research_results, 3)  # 每页显示10个科研成果

    # 从查询字符串中获取页码
    page_number = request.GET.get('page')

    # 获取当前页的Page对象
    page_obj = paginator.get_page(page_number)

    return render(request, 'track/track_list.html', {'page_obj': page_obj})


def track_details(request, research_id):
    try:
        research = ResearchResult.objects.get(AchievementID=research_id)
    except ResearchResult.DoesNotExist:
        # Handle the case where the research does not exist
        return redirect('index')
    modification_records = ModificationRecords.objects.filter(AchievementID=research)
    return render(request, 'track/track_details.html',
                  {'research': research, 'modification_records': modification_records,
                   'research_title': research.Title})


def track_stats_details(request, research_id):
    # 获取科研成果
    research_result = ResearchResult.objects.get(AchievementID=research_id)

    # 获取统计数据
    transaction_count = TransactionRecords.objects.filter(AchievementID=research_result).count()
    tracking_count = TrackedResearch.objects.filter(research_result_id=research_result,track_status='1').count()
    read_count = research_result.ReadingCount
    cite_count = research_result.CitingCount

    # 获取修改记录
    modification_records = ModificationRecords.objects.filter(AchievementID=research_result)

    data = {
        'result': research_result,
        'modification_records': modification_records,
        'transaction_count': transaction_count,
        'tracking_count': tracking_count,
        'read_count': read_count,
        'citation_count': cite_count,
    }

    return render(request, 'track/track_stats_details.html', data)
