from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from librarymanagement.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth.models import User


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})






def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterloginnew.html')
    else:
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbooknew.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'library/viewbook.html',{'books':books})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'library/bookissued.html')
    return render(request,'library/issuebook.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        duration = (ib.expirydate - ib.issuedate).days
        d=days.days
        fine= duration - d
        if(fine <= 0):
            fine = "Expried"
        else:
              fine = str(fine) + ' day'

        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        if len(books)!=0 and len(students)!=0:
            i=0
            for l in books:
                t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine,ib.id)
                i=i+1
                li.append(t)

    return render(request,'library/viewissuedbook.html',{'li':li})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

def aboutus_view(request):
    return render(request,'library/aboutus.html')

def contactus_view(request):
     student=models.StudentExtra.objects.filter(user_id=request.user.id)
     form=forms.ContactusForm()
     if request.method=='POST':
        #now this form have data from html
        form=forms.ContactusForm(request.POST)
        if form.is_valid():
            user = form.save()
            listcontact=models.Contact.objects.filter(enrollment=student[0].enrollment)
            return render(request, 'library/viewcontactstudent.html',{'listcontact':listcontact})
     return render(request,'library/contactstudent.html',{'form':form,'enrollment':student[0].enrollment})


def view_question_by_student(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    listcontact=models.Contact.objects.filter(enrollment=student[0].enrollment)
    return render(request, 'library/viewcontactstudent.html',{'listcontact':listcontact})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def view_question_by_admin(request):
    listquestion  = models.Contact.objects.all();
    return render(request,'library/viewquestionstudentbyadmin.html',{'listquestion':listquestion})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def feedback_question(request,id):
    question = models.Contact.objects.get(id = id);
    return render(request,'library/feedbackquestion.html', {'question':question})  

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_question(request,id):
    question = models.Contact.objects.get(id = id)
    form = forms.ContactusForm(request.POST, instance = question)  
    print(form)
    if form.is_valid():  
        form.save()  
        return redirect("/viewquestionstudentbyadmin")  
    return render(request, 'library/feedbackquestion.html', {'question': question})  

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_question(request,id):
    question = models.Contact.objects.get(id = id)
    question.delete()
    return redirect("/viewquestionstudentbyadmin")

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_book(request, id):
     book = models.Book.objects.get(id=id)
     book.delete()
     # After the operation was Deleted
     messages.success(request, 'Deleted successful!')
     return redirect("/viewbook")

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def edit_book(request, id):  
    book = models.Book.objects.get(id=id)
    return render(request,'library/editbook.html', {'book':book})  

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_book(request, id):  
    book = models.Book.objects.get(id=id)
    form = forms.BookForm(request.POST, instance = book)  
    print(form)
    if form.is_valid():  
        form.save()  
        return redirect("/viewbook")  
    return render(request, 'library/editbook.html', {'book': book})  


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student(request, id):
     student = models.StudentExtra.objects.get(id=id)
     student.delete()
     # After the operation was Deleted
     messages.success(request, 'Deleted successful!')
     return redirect("/viewstudent")


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def edit_student(request, id):  
    student = models.StudentExtra.objects.get(id=id)
    return render(request,'library/editstudent.html', {'student':student})  


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student(request, id):  
    student = models.StudentExtra.objects.get(id=id)
    form = forms.StudentExtraForm(request.POST, instance = student)  
    if form.is_valid():  
        form.save()  
        return redirect("/viewstudent")  
    return render(request, 'library/editstudent.html', {'student': student})  


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def edit_issued_book(request,id):
    issuedbook = models.IssuedBook.objects.get(id=id)
    return  render(request, 'library/editissuedbook.html',{'issuedbook':issuedbook})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_issued_book(request,id):
    issuedbook = models.IssuedBook.objects.get(id=id)
    form = forms.IssuedBookFormEdit(request.POST, instance = issuedbook)  
    print(issuedbook.issuedate)
    if form.is_valid():  
        form.save()  
        return redirect("/viewissuedbook")  
    return render(request, 'library/editissuedbook.html', {'issuedbook': issuedbook})  


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_issued_book(request,id):
    issuedbook = models.IssuedBook.objects.get(id=id)
    issuedbook.delete()
    messages.success(request, 'Deleted successful!')
    return redirect("/viewissuedbook")
    