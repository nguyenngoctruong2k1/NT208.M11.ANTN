from django.shortcuts import redirect, render
import datetime
from icecream import ic

from TestApp.forms import CreateNewStudent

def home_view(request):
    return render(
        request,
        'home.html',
        {
            'now':datetime.datetime.now(),
        }
    )
def create_new_student_view(request):
    if request.method == 'POST':
        form = CreateNewStudent(request.POST)
        form.save()
        if form.is_valid():
            instance = form.save()
            instance.birth_place ='HCM'
            instance.save()
            # ok_url = reversed('new_student_form_ok')
            # return redirect('new_student_form_ok.html')
    else:
        form = CreateNewStudent

    return render(
        request,
        'new_student_form.html',
        {
            'form':form,
        }
    )

def new_student_form_ok():
    print('nguyenngoctruong')
    return render(
        'new_student_form_ok.html',
    )