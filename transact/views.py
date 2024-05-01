from random import choice
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

from create.models import ResearchFile, ResearchResult
from login.models import SiteUser
from records.models import ModificationRecords, ReviewRecords, TransactionRecords
from transact.forms import TransactForm


def download_file(request, file_id):
    file = ResearchFile.objects.get(id=file_id)
    user_id = request.session.get('user_id')
    try:
        user = SiteUser.objects.get(id=user_id)
    except SiteUser.DoesNotExist:
        return HttpResponseForbidden('You are not logged in.')

    if (
            user.name == file.research_result.Ownership or user.name == file.research_result.Author) or user.usertype == '2':
        response = FileResponse(file.file)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.file.name)
        return response
    else:
        return render(request, 'transact/error.html', {'message': '你没有权限下载这个文件。请购买后再试。'})


def index(request):
    research_results_list = ResearchResult.objects.filter(ResearchStatus__in=['4'])
    paginator = Paginator(research_results_list, 3)  # 每页显示 9 个科研成果

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'transact/transact_results_display.html', {'page_obj': page_obj})


def submit_result(request, result_id):
    result = get_object_or_404(ResearchResult, AchievementID=result_id)
    user_id = request.session.get('user_id')
    buyer = SiteUser.objects.get(id=user_id)
    form = TransactForm(request.POST or None)
    # 企业才能发起交易
    #TODO：这里的逻辑需要修改，因为只有企业才能发起交易，故其他类型用户点击申请交易会进入错误页面
    if buyer.usertype != '3':
        messages.error(request, "您当前的身份不能参与交易")
        return render(request, 'transact/transact_results_display.html', {'no_permission': True})
    else:
        if request.method == 'POST':
            if form.is_valid():
                amount = form.cleaned_data['TransactionAmount']
                seller = SiteUser.objects.get(name=result.Ownership)
                result.ResearchStatus = '5'  # 将科研成果更改为交易中
                result.save()

                # Record the status update
                ModificationRecords.objects.create(AchievementID=result,
                                                   StatusDescription=f"{buyer}提出交易申请，科研成果正在交易中")

                TransactionRecords.objects.create(AchievementID=result, Buyer=buyer, Seller=seller,
                                                  TransactionAmount=amount)

                # Send a notification to the seller
                # You can use the Django messages framework to send a one-time notification to the seller
                messages.success(request, "科研成果已成功提交并进入交易中，请耐心等待交易")

                return redirect(reverse('transact_results_display'))  # Redirect back to the index page
        return render(request, 'transact/submit_result.html', {'form': form, 'result': result, 'user': buyer})


def transact_deal(request):
    user_id = request.session.get('user_id')  # 获取当前登录用户的 ID
    user = SiteUser.objects.get(id=user_id)  # 获取当前登录用户的信息
    research_results_list = ResearchResult.objects.filter(ResearchStatus='5',
                                                          Ownership=user)  # 查询科研成果状态为交易中且所有者是当前登录用户的科研成果
    paginator = Paginator(research_results_list, 3)  # 每页显示 9 个科研成果

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transact/transact_deal.html', {'page_obj': page_obj})


from .forms import ConfirmTransactionForm


def transact_confirm(request, result_id):
    result = get_object_or_404(ResearchResult, AchievementID=result_id)
    transaction_record = TransactionRecords.objects.get(AchievementID=result_id, TransactionStatus='1')
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = ConfirmTransactionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['agree_to_transact'] == 'True':
                # 用户同意交易
                result.ResearchStatus = '6'  # '6' represents '已交易'
                # 更新科研成果定价
                result.Price = transaction_record.TransactionAmount
                transaction_record.TransactionStatus = '2'  # '2' represents '成功'
                # 更新双方账户金额
                seller = SiteUser.objects.get(name=result.Ownership)
                buyer = transaction_record.Buyer
                if buyer.balance < transaction_record.TransactionAmount:
                    result.ResearchStatus = '4'  # '4' represents '待交易'
                    transaction_record.TransactionStatus = '3'  # '3' represents '失败'
                    status_description = f"{user.name}余额不足，交易失败"
                else:
                    buyer.balance -= transaction_record.TransactionAmount
                    seller.balance += transaction_record.TransactionAmount
                    buyer.save()
                    seller.save()
                    status_description = f"{user.name}同意交易，交易完成"
                    # 更新科研成果所有权归属
                    result.Ownership = transaction_record.Buyer.name  # Use the name of the buyer
            else:
                # 用户不同意交易
                result.ResearchStatus = '4'  # '4' represents '待交易'
                transaction_record.TransactionStatus = '3'  # '3' represents '失败'
                status_description = f"{user.name}不同意交易，交易失败"
            result.save()
            transaction_record.save()
            ModificationRecords.objects.create(AchievementID=result, StatusDescription=status_description)
            return redirect(reverse('transact_deal'))  # Redirect back to the index page
    else:
        form = ConfirmTransactionForm()
    return render(request, 'transact/transact_confirm.html', {'form': form, 'result': result,
                                                              'buyer': transaction_record.Buyer,
                                                              'TransactionAmount': transaction_record.TransactionAmount})


def transact_records(request):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)

    if user.usertype == '3':  # 如果用户是企业
        records = TransactionRecords.objects.filter(Q(Buyer=user) | Q(Seller=user))
    elif user.usertype == '1':  # 如果用户是科研工作者
        records = TransactionRecords.objects.filter(Seller=user)
    else:
        records = []

    return render(request, 'transact/transact_records.html', {'records': records})


def bought_results(request):
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    records = TransactionRecords.objects.filter(Buyer=user, TransactionStatus='2')
    research_results = [record.AchievementID for record in records]

    paginator = Paginator(research_results, 3)  # 每页显示 9 个科研成果

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transact/bought_results.html', {'page_obj': page_obj})


from .forms import SecondTransactForm


def second_transact(request, result_id):
    result = get_object_or_404(ResearchResult, AchievementID=result_id)
    user_id = request.session.get('user_id')
    user = SiteUser.objects.get(id=user_id)
    if result.Ownership == user.name and result.ResearchStatus == '6':
        if request.method == 'POST':
            form = SecondTransactForm(request.POST)
            if form.is_valid():
                result.ResearchStatus = '4'  # '4' represents '待交易'
                result.Price = form.cleaned_data['new_price']
                result.save()
                ModificationRecords.objects.create(AchievementID=result,
                                                   StatusDescription=f"{user.name}进行转移交易，并修改了科研成果的价格为{result.Price}")

                return redirect(reverse('bought_results'))  # Redirect back to the bought results page
        else:
            form = SecondTransactForm()
        return render(request, 'transact/second_transact.html', {'form': form, 'result': result})
    else:
        return HttpResponseForbidden('You do not have permission to sell this research result.')
