from django.shortcuts import render, redirect, HttpResponseRedirect
from rest_framework.views import APIView
from authentication.models import User
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes
from .forms import *
import time
from course.models import *
from .models import mony
from datetime import datetime

from django.template import RequestContext
# Create your views here.
@login_required
def index(request):
    print(request.user)
    try:
        if True == True:
            
            p = 0
            y = mony.objects.filter(date__year =datetime.now().year).filter(date__month = datetime.now().month) 
            d = mony.objects.filter(date__year =datetime.now().year).filter(date__month = datetime.now().month).filter(date__day = datetime.now().day) 
            o = 0
            
            for i in y:
                p = p + i.price
            for l in d:
                o = o + l.price    
            context = {
                'bannars':Banars.objects.all(),
                'usercount': User.objects.all().count(),
                'course': CatCourses.objects.all(),
                "teacher":Teacher.objects.all(),
                "videos":Courses.objects.all(),
                "cart": mony.objects.all().count(),
                "priceInMonth":int (p),
                'priceInDay':int(o),
                "soldLast1":mony.objects.filter(date__year=datetime.now().year -1 , date__month='1').count(),
                "sold1":mony.objects.filter(date__year=datetime.now().year , date__month='1').count(),
                "soldLast2":mony.objects.filter(date__year=datetime.now().year -1 , date__month='2').count(),
                "sold2":mony.objects.filter(date__year=datetime.now().year , date__month='2').count(),
                "soldLast3":mony.objects.filter(date__year=datetime.now().year -1 , date__month='3').count(),
                "sold3":mony.objects.filter(date__year=datetime.now().year , date__month='3').count(),
                "soldLast4":mony.objects.filter(date__year=datetime.now().year -1 , date__month='4').count(),
                "sold4":mony.objects.filter(date__year=datetime.now().year , date__month='4').count(),
                "soldLast5":mony.objects.filter(date__year=datetime.now().year -1 , date__month='5').count(),
                "sold5":mony.objects.filter(date__year=datetime.now().year , date__month='5').count(),
                "soldLast6":mony.objects.filter(date__year=datetime.now().year -1 , date__month='6').count(),
                "sold6":mony.objects.filter(date__year=datetime.now().year , date__month='6').count(),
                "soldLast7":mony.objects.filter(date__year=datetime.now().year -1 , date__month='7').count(),
                "sold7":mony.objects.filter(date__year=datetime.now().year , date__month='7').count(),
                "soldLast8":mony.objects.filter(date__year=datetime.now().year -1 , date__month='8').count(),
                "sold8":mony.objects.filter(date__year=datetime.now().year , date__month='8').count(),
                "soldLast9":mony.objects.filter(date__year=datetime.now().year -1 , date__month='9').count(),
                "sold9":mony.objects.filter(date__year=datetime.now().year , date__month='9').count(),
                "soldLast10":mony.objects.filter(date__year=datetime.now().year -1 , date__month='10').count(),
                "sold10":mony.objects.filter(date__year=datetime.now().year , date__month='10').count(),
                "soldLast11":mony.objects.filter(date__year=datetime.now().year -1 , date__month='11').count(),
                "sold11":mony.objects.filter(date__year=datetime.now().year , date__month='11').count(),
                "soldLast12":mony.objects.filter(date__year=datetime.now().year -1 , date__month='12').count(),
                "sold12":mony.objects.filter(date__year=datetime.now().year , date__month='12').count(),
                'UserOne': User.objects.filter(year__id = 1  ).count(),
                'UserTwo': User.objects.filter(year__id = 2  ).count(),
                'UserThree': User.objects.filter(year__id = 3  ).count(),
                'UserFour': User.objects.filter(year__id = 4  ).count(),

            }
            return render( request, 'index.html', context=context)
        else:
            return redirect('pages:login')
    except:
        pass

def Login(request):
    if request.method == 'GET':
        return render(request, 'pages/login.html')

    else:
        email = request.POST.get('email').lower().strip()
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request,'pages/login.html',{"message":"incorrect email"})

        if not user.check_password(password):
            return render(request,'pages/login.html',{"message":"incorrect password"})
        if not user.is_staff:
            return render(request,'pages/login.html',{"message":"غير مصرح لك"})


        
        user1 = auth.authenticate(request,email = email , password = password)
        auth.login(request,user1)
        # request.headers['Authorization']=str(refresh.access_token)
        # request.
        if request.GET.get('next'):
            response= redirect(request.GET.get('next'))
        else:
            response = redirect('pages:index')
        return response


def Logout(request):
    try:

        response = redirect('pages:login')

        # deleting cookies
        auth.logout(request)

        return response
    except:
        return redirect('pages:login')
class RestPassword(APIView):
    def get(self, request, uidb64,token):

        return render (request,"pages/forgot-password.html")
    def post(self,request, uidb64 ,token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            password = request.data['password']
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                context = {
                    'message':'link had ended'}

                return render (request,"pages/forgot-password.html", context)
            user.set_password(password)
            user.save()
            context = {
                'message':' password changed'
            }
            return render (request,"pages/forgot-password.html", context)
        except:
            context = {
                    'message':'invalid link'
                }

            return render (request,"pages/forgot-password.html", context)
        
@login_required
def Forms(request):
    if request.method =='GET':
        context = {
            "forms": TeacherForms(),
            "dd":"create"
        }
        return render( request,'forms.html', context=context)
    else: 
        add_course = TeacherForms(request.POST, request.FILES)
        if add_course.is_valid():
            add_course.save()
            context={
                "message":"done",
                "forms": TeacherForms(),
                "dd":"create"
            }
            return render(request,'forms.html', context=context)
        else:
            
            context={
                "message":"تأكد من كتابة كل العناصر",
                "forms": TeacherForms(),
                "dd":"create"
            }
            return render(request, 'forms.html', context=context)
        


@login_required
def CatCoursesForm(request):
    if request.method =='GET':
        context = {
            "forms": CoursesForms(),
            "dd":"create",
        }
        return render( request,'charts.html', context=context) 
    else:
        add_course = CoursesForms(request.POST, request.FILES)
        if add_course.is_valid():
            add_course.save()
            context={
                "message":"done",
                "forms": CoursesForms(),
                "dd":"create"
            }
            return render(request, 'charts.html', context=context)
        else:
            context={
                "message":"تأكد من كتابة كل العناصر",
                "forms": CoursesForms(),
                "dd":"create"
            }
            return render(request, 'charts.html', context=context)
           

@login_required
def Phone (request):
    if request.method == 'GET':

                
        return render( request,'pages/blank.html')
            
        
    else:
    
        i = request.POST.get('email')
        try:
            User.objects.get(email = i)
            y = User.objects.get(email = i )
            y.device = None
            y.save()
            context = {
                "message":"done"
            }
            return render( request,'pages/blank.html', context=context)
        except:
            context = {
                "message":"email is incorrect"
            }
            return render( request,'pages/blank.html', context=context)
            
@login_required
def updateCatCoursesForm(request, id):
    if request.method == 'GET' :
        bb = CatCourses.objects.get(id = id)
        context = {
            "forms": CoursesForms(instance=bb),
            "dd":"update"
        }
        return render( request,'charts.html', context=context)            
    else: 
        bb = CatCourses.objects.get(id = id)
        if request.method == "POST":
            add_course = CoursesForms(request.POST, request.FILES, instance=bb)
            if add_course.is_valid():
                add_course.save()
                context={
                    "message":"done",
                    "forms": add_course,
                    "dd":"update"
                }
                return render(request, 'charts.html', context=context)
            else:
                
                context={
                    "message":"تأكد من كتابة كل العناصر",
                    "forms": add_course,
                    "dd":"update"
                }
                return render(request, 'charts.html', context=context)
            
@login_required       
def updateTeacher(request, id):
    if request.method == 'GET':
        bb = Teacher.objects.get(id = id)
        
        context = {
            "forms": TeacherForms(instance=bb),
            "dd":"update"
        }
        return render( request,'forms.html', context=context)
            
            
    else:
        bb = Teacher.objects.get(id = id)
        if request.method == "POST":
            add_course = TeacherForms(request.POST, request.FILES, instance=bb)
            if add_course.is_valid():
                add_course.save()
                context={
                    "message":"done",
                    "forms": add_course,
                    "dd":"update"
                }
                return render(request, 'charts.html', context=context)
            else:
                
                context={
                    "message":"تأكد من كتابة كل العناصر",
                    "forms": add_course,
                    "dd":"update"
                }
                return render(request, 'charts.html', context=context)
    
@login_required
def VideoView(request):
    if request.method == 'GET':
        
        context = {
            "forms": VideoForms(),
            "dd":"create"

        }
        return render( request,'forms.html', context=context)
            
    else:
        
        if request.method == "POST":
            add_course = VideoForms(request.POST, request.FILES)
            if add_course.is_valid():
                add_course.save()
                
                
            
                context={
                    "message":"done",
                    "forms": VideoForms(),
                    "dd":"create"
                }
                return render(request,'forms.html', context=context)
            else:
                
                context={
                    "message":"تأكد من كتابة كل العناصر",
                    "forms": VideoForms(),
                    "dd":"create"
                }
                return render(request, 'forms.html', context=context)
            
@login_required
def updateVideo(request, id):
    if request.method == 'GET':
        bb = Courses.objects.get(id = id)
        context = {
            "forms": VideoForms(instance=bb),
            "dd":"update"
        }
        return render( request,'forms.html', context=context)
            
            
    else: 

        bb = Courses.objects.get(id = id)
        if request.method == "POST":
            add_course = VideoForms(request.POST, request.FILES, instance=bb)
            if add_course.is_valid():
                add_course.save()
                
                
            
                context={
                    "message":"done",
                    "forms": add_course,
                    "dd":"update"
                }
                return render(request, 'charts.html', context=context)
            else:
                
                context={
                    "message":"تأكد من كتابة كل العناصر",
                    "forms": add_course,
                    "dd":"update"
                }
                return render(request, 'charts.html', context=context)
@login_required            
def DeleteTeacher(request, id):
    if request.method == 'GET':
        bb = Teacher.objects.get(id = id)
        
        context = {
            "forms": TeacherForms(instance=bb),
            "dd":"delete"
        }
        return render( request,'forms.html', context=context)
            
            
    else:
        
        bb = Teacher.objects.get(id = id)
        bb.delete()
        context = {
            "messagee":"deleted done",
            "dd":"delete"
        }
        return redirect ('pages:index' )
@login_required    
def DeleteCatCourse(request, id):
    if request.method == 'GET':
        bb = CatCourses.objects.get(id = id)

        context = {
            "forms": CoursesForms(instance=bb),
            "dd":"delete"
        }
        return render( request,'forms.html', context=context)
    
            
    else:
        
        bb = CatCourses.objects.get(id = id)
        bb.delete()
        context = {
            "messagee":"deleted done",
            "dd":"delete"
        }
        return redirect ('pages:index' )
@login_required         
def DeleteVideo(request, id):
    if request.method == 'GET':
        bb = Courses.objects.get(id = id)
        
        context = {
            "forms": VideoForms(instance=bb),
            "dd":"delete"
        }
        return render( request,'forms.html', context=context)
            
    else: 
        
        bb = Courses.objects.get(id = id)
        bb.delete()
        context = {
            "messagee":"deleted done",
            "dd":"delete"
        }
        return redirect ('pages:index' )
            
    
from django.shortcuts import render
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def page_not_found_view_505(request, exception):
    return render(request, '500.html', status=505)


@login_required
def bay(request,id):
    if request.method == 'GET':
        
        pp = Cart.objects.get(id = id)
        y = CartItem.objects.filter(cart = pp).all()
        context = {
            "cartItem":y,
            "price":pp.totlaPrice
        }
        
        return render(request, 'pages/blank1.html', context=context)
    else:
        
        ly = request.POST.get('serial')
        if mony.objects.filter(serial = ly).exists():
            context = {
            "mm":"this serial is exist"
            }

            return render(request, 'pages/blank1.html', context=context)
        pp = Cart.objects.get(id = id)
        y = CartItem.objects.filter(cart = pp).all()
        
        user = pp.userCart
        for p in y:
            p.Courses.users.add(user)
            p.delete()
        mony.objects.create(cart = pp, price = pp.totlaPrice, serial = ly)

        pp.totlaPrice = int (00)
        pp.save()
        
        context = {
            "cartItem":y,
            "price":pp.totlaPrice,
            "mm":"pay done"
        }

        return render(request, 'pages/blank1.html', context=context)


@login_required

def BannarView(request):
    if request.method == 'GET':
        
        context = {
            "forms": BannarForms(),
            "dd":"create"

        }
        return render( request,'forms.html', context=context)
            
    else:
        if request.method == "POST":
            add_course = BannarForms(request.POST, request.FILES)
            if add_course.is_valid():
                add_course.save()
                
                
            
                context={
                    "message":"done",
                    "forms": BannarForms(),
                    "dd":"create"
                }
                return render(request,'forms.html', context=context)
            else:
                
                context={
                    "message":"تأكد من كتابة كل العناصر",
                    "forms": BannarForms(),
                    "dd":"create"
                }
                return render(request, 'forms.html', context=context)
@login_required

def DeleteBanars(request, id):
    if request.method == 'GET':
        bb = Banars.objects.get(id = id)
        
        context = {
            "forms": BannarForms(instance=bb),
            "dd":"delete"
        }
        return render( request,'forms.html', context=context)
            
            
    else:
        bb = Banars.objects.get(id = id)
        bb.delete()
        context = {
            "messagee":"deleted done",
            "dd":"delete"
        }
        return redirect ('pages:index' )