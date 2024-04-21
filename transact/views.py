from django.shortcuts import render
from django.http import FileResponse, HttpResponseForbidden
from create.models import ResearchFile
from login.models import SiteUser

def download_file(request, file_id):
    file = ResearchFile.objects.get(id=file_id)
    user_id = request.session.get('user_id')
    try:
        user = SiteUser.objects.get(id=user_id)
    except SiteUser.DoesNotExist:
        return HttpResponseForbidden('You are not logged in.')
    print(file.research_result.Ownership)
    print(user.name)
    if (user.name != file.research_result.Ownership or file.research_result.Author) and user.usertype != '2':
        return render(request, 'transact/error.html', {'message': '你没有权限下载这个文件。请购买后再试。'})
    response = FileResponse(file.file)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.file.name)
    return response
