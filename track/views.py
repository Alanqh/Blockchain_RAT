from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from login.models import SiteUser
from .models import TrackedResearch
from create.models import ResearchResult

from records.models import ModificationRecords

from django.core.paginator import Paginator


def index(request):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    research_results = ResearchResult.objects.filter(ResearchStatus__in=['4', '5', '6'])

    for result in research_results:
        result.is_tracked = TrackedResearch.objects.filter(user=user, research_result=result, track_status='1').exists()
    # Create a Paginator object
    paginator = Paginator(research_results, 9)  # Show 10 research_results per page
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
    return render(request, 'track/track_list.html', {'research_results': research_results})


def track_details(request, research_id):
    try:
        research = ResearchResult.objects.get(AchievementID=research_id)
    except ResearchResult.DoesNotExist:
        # Handle the case where the research does not exist
        return redirect('index')
    modification_records = ModificationRecords.objects.filter(AchievementID=research)
    return render(request, 'track/track_details.html',
                  {'research': research, 'modification_records': modification_records,'research_title': research.Title})
