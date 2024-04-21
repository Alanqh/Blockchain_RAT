from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse
from .models import ResearchResult
from records.models import ModificationRecords
from .forms import ResearchResultForm, ResearchFileForm
from .models import ResearchFile

from login.models import SiteUser

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
            ModificationRecords.objects.create(AchievementID=research_result, ResearchStatus='1' ,
                                               StatusDescription='首次提交科研成果信息，尚未审核')
            return redirect(reverse('research_result_detail', args=[research_result.pk]))
    else:
        form = ResearchResultForm()
        file_form = ResearchFileForm()
    return render(request, 'create/create_research_result.html', {'form': form, 'file_form': file_form})


def research_result_detail(request, pk):
    research_result = get_object_or_404(ResearchResult, pk=pk)
    return render(request, 'create/research_result_detail.html', {'research_result': research_result})