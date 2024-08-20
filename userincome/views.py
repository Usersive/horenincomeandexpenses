
import datetime
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.forms import ProfileUpdateForm
from authentication.models import Profile
from userincome.models import Source, UserIncome
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreferences
import csv
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum


@login_required(login_url='/login')
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
    
    
    
@login_required(login_url='/login')
def income(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 10)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    
    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except UserPreferences.DoesNotExist:
        currency = 'Choose currency from settings' 
        
    context ={
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'income/income.html', context)


@login_required(login_url='/login')
def add_income(request):
    sources = Source.objects.all()
    context ={
        'sources': sources,
        'value': request.POST,
    }
    if request.method=="GET":
        return render(request, 'income/add_income.html', context)

    if request.method =="POST":
        amount = request.POST['amount']
        # pdb.set_trace()
        
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'income/add_income.html', context)
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'income/add_income.html', context)
        
        UserIncome.objects.create(owner=request.user, amount=amount, description=description, date=date, source=source)
        # user.save()
        messages.success(request, "Income saved successfully...")
        return redirect('income')
            
        
@login_required(login_url='/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context ={
        'income': income,
        'value':income,
        'sources': sources,
        
    }
    if request.method =="GET":
        return render(request, 'income/income_edit.html', context)
    
    if request.method =="POST":
        amount = request.POST['amount']
       
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'income/income_edit.html', context)
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'income/income_edit.html', context)
                
        income.owner=request.user
        income.amount = amount
        income.source=source
        income.description=description
        income.date=date
        income.save()
        messages.success(request, "Income updated successfully...")
        return redirect('income')

@login_required(login_url='/login')
def income_delete(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income was removed")
    return redirect('income')        


@login_required(login_url='/login')
def export_income_csv(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Income' + str(datetime.datetime.now()) + '.csv'  
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Source', 'Date'])
    incomes = UserIncome.objects.filter(owner=request.user)
    
    for income in incomes:
        writer.writerow([income.amount, income.description, income.source, income.date])
    return response


@login_required(login_url='/login')
def export_income_excel(request):
    response =HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Income' + str(datetime.datetime.now()) + '.xls' 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True
    
    columns = ['Amount', 'Description', 'Source', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()
    rows = UserIncome.objects.filter(owner=request.user).values_list('amount','description', 'source', 'date')
    
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response



@login_required(login_url='/login')
def export_income_pdf(request):
    response =HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Income' + str(datetime.datetime.now()) + '.pdf' 
    response['Content-Transfer-Encoding'] = 'binary'
    
    try:
        currency = UserPreferences.objects.get(user=request.user).currency
       
    except UserPreferences.DoesNotExist:
        currency = 'Choose currency from settings' 
       
    try:
        profile=request.user.profile
    except Profile.DoesNotExist:
        profile = None
        
    incomes = UserIncome.objects.filter(owner=request.user)
    sum = incomes.aggregate(Sum('amount'))
    
  
    
    html_string = render_to_string('income/export_income_pdf.html',{'incomes':incomes, 'total': sum['amount__sum'], 'currency': currency, 'profile':profile,})
    html =HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        temp_file_name = output.name
    
    # Reopen the file for reading and send it as the response
    with open(temp_file_name, 'rb') as f:
        response.write(f.read())
    
    # Remove the temporary file
    try:
        os.remove(temp_file_name)
    except OSError:
        pass
    
    return response




@login_required(login_url='/login')
def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    incomes = UserIncome.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_source(income):
        return income.source
    source_list = list(set(map(get_source, incomes)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount

    for x in incomes:
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)

    return JsonResponse({'income_source_data': finalrep}, safe=False)



@login_required(login_url='/login')
def income_stats_view(request):
    return render(request, 'income/income_stats.html')