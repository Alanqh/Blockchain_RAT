from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from create.models import ResearchResult
from login.models import SiteUser
from records.models import ModificationRecords, ReviewRecords
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from random import choice


# Create your views here.
def index(request):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    research_results_list = ResearchResult.objects.filter(ResearchStatus__in=['1', '2'], Author=user)
    paginator = Paginator(research_results_list, 9)  # 每页显示 9 个科研成果

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'review/review_apply.html', {'page_obj': page_obj})


def submit_result(request, result_id):
    result = get_object_or_404(ResearchResult, AchievementID=result_id)
    if request.session.get('is_login', None):  # Check if the user is logged in
        result.ResearchStatus = '3'  # 将科研成果更改为审核中
        result.save()
        user_id = request.session.get('user_id')
        user = SiteUser.objects.get(id=user_id)
        # Record the status update
        ModificationRecords.objects.create(AchievementID=result,
                                           StatusDescription=f"{user.name}提出审核申请，其科研成果正在审核中")

        # Assign a reviewer to the research result
        reviewers = SiteUser.objects.filter(usertype='2')
        reviewer = choice(reviewers)  # Choose a reviewer randomly

        # Create a review record
        ReviewRecords.objects.create(AchievementID=result, ReviewerID=reviewer)

        messages.success(request, "科研成果已成功提交并分配给审核者，请耐心等待审核")
        return HttpResponseRedirect(reverse('review_apply'))  # Redirect back to the index page
    else:
        messages.error(request, "请先登录")
        return HttpResponseRedirect(reverse('login'))  # Redirect to the login page


def review_deal(request):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    if user.usertype != '2':
        return render(request, 'review/review_deal.html', {'no_permission': True})

    # Get all unprocessed review records for the current user
    unprocessed_records = ReviewRecords.objects.filter(ReviewerID=user, ReviewResult='3')

    # Get the research results associated with these records
    research_results = [record.AchievementID for record in unprocessed_records]

    # Create a Paginator object
    paginator = Paginator(research_results, 9)  # Show 9 research results per page

    # Get the page number from the request
    page_number = request.GET.get('page')

    # Get the Page object for the given page number
    page_obj = paginator.get_page(page_number)

    return render(request, 'review/review_deal.html', {'page_obj': page_obj})


from .forms import ReviewForm


def review_result_confirm(request, result_id):
    review_record = get_object_or_404(ReviewRecords, AchievementID=result_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_result = form.cleaned_data['review_result']
            review_comments = form.cleaned_data['review_comments']
            review_record.ReviewResult = review_result
            review_record.ReviewComments = review_comments
            review_record.save()

            user_id = request.session.get('user_id')
            user = SiteUser.objects.get(id=user_id)
            ModificationRecords.objects.create(AchievementID=review_record.AchievementID,
                                               StatusDescription=f"{user.name}审核了科研成果，审核结果为：{'通过' if review_result == '1' else '未通过'}")

            # If the review result is '1' (passed), update the research result status to '待交易'
            if review_result == '1':
                research_result = review_record.AchievementID
                research_result.ResearchStatus = '4'  # '4' represents '待交易'
                research_result.save()
                ModificationRecords.objects.create(AchievementID=research_result,
                                                   StatusDescription=f"{user.name}审核通过，科研成果状态更新为待交易")
            if review_result == '2':
                research_result = review_record.AchievementID
                research_result.ResearchStatus = '1' # '1' represents '未审核'
                research_result.save()
                ModificationRecords.objects.create(AchievementID=research_result,
                                                   StatusDescription=f"{user.name}审核未通过，科研成果状态更新为未审核")

            return redirect(reverse('review_deal'))
    else:
        form = ReviewForm()
    return render(request, 'review/review_result_confirm.html', {'form': form})