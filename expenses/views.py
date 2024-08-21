
import datetime
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import Profile
from expenses.models import Category, Expenses
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
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expenses.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expenses.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expenses.objects.filter(
            description__icontains=search_str, owner=request.user) | Expenses.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
    
    

@login_required(login_url='/login')
def expenses(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except UserPreferences.DoesNotExist:
        currency = 'Choose currency from settings'  # Set a default currency if user preferences do not exist

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'expenses/expenses.html', context)




@login_required(login_url='/login')
def add_expenses(request):
    categories = Category.objects.all()
    context ={
        'categories': categories,
        'value': request.POST,
    }
    if request.method=="GET":
        return render(request, 'expenses/add_expenses.html', context)

    if request.method =="POST":
        amount = request.POST['amount']
        # pdb.set_trace()
        
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/add_expenses.html', context)
        
        description = request.POST['description']
        date = request.POST['expenses_date']
        category = request.POST['category']
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/add_expenses.html', context)
        
        Expenses.objects.create(owner=request.user, amount=amount, description=description, date=date, category=category)
        # user.save()
        messages.success(request, "Expenses saved successfully...")
        return redirect('expenses')
            
        
@login_required(login_url='/login')
def expenses_edit(request, id):
    expense = Expenses.objects.get(pk=id)
    categories = Category.objects.all()
    context ={
        'expense': expense,
        'value':expense,
        'categories': categories,
        
    }
    if request.method =="GET":
        return render(request, 'expenses/expenses_edit.html', context)
    
    if request.method =="POST":
        amount = request.POST['amount']
       
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/expenses_edit.html', context)
        
        description = request.POST['description']
        date = request.POST['expenses_date']
        category = request.POST['category']
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/expenses_edit.html', context)
                
        expense.owner=request.user
        expense.amount = amount
        expense.category=category
        expense.description=description
        expense.date=date
        expense.save()
        messages.success(request, "Expenses updated successfully...")
        return redirect('expenses')

@login_required(login_url='/login')
def expense_delete(request, id):
    expenses = Expenses.objects.get(pk=id)
    expenses.delete()
    messages.success(request, "Expenses was removed")
    return redirect('expenses')  

      


@login_required(login_url='/login')
def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expenses.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

@login_required(login_url='/login')
def expenses_stats_view(request):
    return render(request, 'expenses/expenses_stats.html')


@login_required(login_url='/login')
def export_csv(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.csv'  
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])
    expenses = Expenses.objects.filter(owner=request.user)
    
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    return response


@login_required(login_url='/login')
def export_excel(request):
    response =HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.xls' 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True
    
    columns = ['Amount', 'Description', 'Category', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()
    rows = Expenses.objects.filter(owner=request.user).values_list('amount','description', 'category', 'date')
    
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response


@login_required(login_url='/login')
def export_pdf(request):
    response =HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses' + str(datetime.datetime.now()) + '.pdf' 
    response['Content-Transfer-Encoding'] = 'binary'
    
    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except UserPreferences.DoesNotExist:
        currency = 'Choose currency from settings' 
    
    try:
        profile=request.user.profile
    except Profile.DoesNotExist:
        profile = None
        
    expenses = Expenses.objects.filter(owner=request.user)
    sum = expenses.aggregate(Sum('amount'))
    
    html_string = render_to_string('expenses/export_pdf.html',{'expenses':expenses, 'total': sum['amount__sum'], 'currency': currency, 'profile':profile})
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