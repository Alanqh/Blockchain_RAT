from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from decorator import login_required
from .models import ResearchResult
from records.models import ModificationRecords
from .forms import ResearchResultForm, ResearchFileForm
from .models import ResearchFile

from login.models import SiteUser


@login_required
def create_research_result(request):
    if request.method == 'POST':
        form = ResearchResultForm(request.POST)
        file_form = ResearchFileForm(request.POST, request.FILES)
        if form.is_valid() and file_form.is_valid():
            research_result = form.save(commit=False)
            user_id = request.session.get('user_id')
            user = SiteUser.objects.get(id=user_id)
            research_result.UserID = user
            research_result.Author = user.name
            research_result.Ownership = research_result.Author
            research_result.save()
            for f in request.FILES.getlist('file'):
                ResearchFile.objects.create(file=f, research_result=research_result)
            # 创建一条新的记录
            ModificationRecords.objects.create(AchievementID=research_result,
                                               StatusDescription=f"{user.name}首次提交科研成果信息，尚未审核")
            return redirect(reverse('research_result_detail', args=[research_result.pk]))
    else:
        form = ResearchResultForm()
        file_form = ResearchFileForm()
    return render(request, 'create/create_research_result.html', {'form': form, 'file_form': file_form})


def research_result_detail(request, pk):
    research_result = get_object_or_404(ResearchResult, pk=pk)
    return render(request, 'create/research_result_detail.html', {'research_result': research_result})


def results_created_list(request):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    research_results_list = ResearchResult.objects.filter(Author=user)
    paginator = Paginator(research_results_list, 9)  # 每页显示 9 个科研成果

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'create/results_created_list.html', {'page_obj': page_obj})


def modify_result(request, result_id):
    result = get_object_or_404(ResearchResult, pk=result_id)
    original_result = ResearchResult.objects.get(pk=result_id)  # 获取原始的科研成果信息
    if request.method == 'POST':
        form = ResearchResultForm(request.POST, instance=result)
        file_form = ResearchFileForm(request.POST, request.FILES)
        if form.is_valid() and file_form.is_valid():
            research_result = form.save(commit=False)
            research_result.ResearchStatus = '2'
            research_result.save()
            for f in request.FILES.getlist('file'):
                ResearchFile.objects.create(file=f, research_result=research_result)
            user_id = request.session.get('user_id')
            user = SiteUser.objects.get(id=user_id)
            # 创建一条新的记录
            changes = []
            for field in ResearchResult._meta.fields:
                original_value = getattr(original_result, field.name)
                new_value = getattr(research_result, field.name)
                if original_value != new_value:
                    changes.append(f"{field.verbose_name}: {original_value} -> {new_value}")
            changes_description = "; ".join(changes)
            ModificationRecords.objects.create(AchievementID=research_result,
                                               StatusDescription=f"{user.name}修改了科研成果信息，尚未审核。修改内容：{changes_description}")
            return redirect(reverse('research_result_detail', args=[research_result.pk]))
    else:
        form = ResearchResultForm(instance=result)
        file_form = ResearchFileForm()
    return render(request, 'create/modify_result.html', {'form': form, 'file_form': file_form, 'result': result})
