from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.response import Response
# Create your views here.
def authenticate( request):
    token = request.META.get('HTTP_AUTH_TOKEN')
    if token == None:
        return {
            'status': False,
            'message': 'يجب عليك تسجيل الدخول اولا'
            
        }
    elif Token.objects.filter(key = token).exists():
      if Token.objects.filter(key = token).get().user.is_active == False:
        return {
            'status': False,
            'message': 'This user is inactive'}
      return {
          'status' : True,
          'message': 'All is Done ',
          'user': Token.objects.filter(key = token).get().user

      }
    else:
        return {
            'status': False,
            'message': 'you should login again'
            
        }

class teacherView (generics.GenericAPIView):
    serializer_class = teacherSerializers
    
    def get (self,request):
        yy = authenticate(request=request)
        if yy.get('status') == False:
            return Response (yy, status=status.HTTP_200_OK)
        if request.query_params:
            id1 = request.query_params['id']
            d = Teacher.objects.get(id=id1)
            serializers = teacherSerializers1(d)
            
        else:
            d = Teacher.objects.all()
            serializers = teacherSerializers(d , many=True)
        return Response({"data":serializers.data},status=status.HTTP_200_OK)

class Star(generics.GenericAPIView):
    serializer_class = CatCourseSerializers
    permission_classes = [HasAPIKey]
    def get (self, request):
        yy = authenticate(request=request)
        if yy.get('status') == False:
            return Response (yy, status=status.HTTP_200_OK)
        user = yy.get('user')
        if request.query_params:                
            id1 = request.query_params['id']
            d = CatCourses.objects.get(id=id1)
            d.myCourseIcon = False
            d.save()
            ls = CartItem.objects.filter(userCartItem = user).all()
            for op in ls:
                op.Courses.cartIcon = False
                
            

            if user in d.users.all():
                d.myCourseIcon = True
                
            else:
                d.myCourseIcon = False
                
            serializers = CatCourseSerializers(d)
            
        else:
            d = CatCourses.objects.filter(star = True).filter(active = True).all()
            
            
            
                
                
            for i in d:
                if user in i.users.all():
                    i.myCourseIcon = True
                    i.cartIcon = False
                    if CartItem.objects.filter(Courses = i).filter(userCartItem = user).exists():
                        i.cartIcon = True
                    


                    
                else:
                    i.myCourseIcon = False
                    i.cartIcon = False
                    
                    if CartItem.objects.filter(Courses = i).filter(userCartItem = user).exists():
                        i.cartIcon = True
                    
            
                
            serializers = CatCourseSerializers(d , many=True)
        return Response({"data":serializers.data},status=status.HTTP_200_OK)

class CoursesViews(generics.GenericAPIView):
    serializer_class = YearSerializerswithCatCourses
    
    def get(self,request):
        yy = authenticate(request=request)
        if yy.get('status') == False:
            return Response (yy, status=status.HTTP_200_OK)
        user = yy.get('user')
        if request.query_params:
                            
            id1 = request.query_params['CollegeId']
            d = year.objects.filter(college = id1).all()
            serializers = yearSerializers(d, many = True)
            try:
                if request.query_params:
                    ii = request.query_params['YearId']
                    oo = request.query_params['Term']
                    yy = CatCourses.objects.filter(year = ii)
                    
                    oooo = yy.filter(term = oo).filter(active = True).all()
                    for i in oooo:
                        if user in i.users.all():
                            i.myCourseIcon = True
                            i.cartIcon = False
                            if CartItem.objects.filter(Courses = i).filter(userCartItem = user).exists():
                                i.cartIcon = True
                            i.save()
                        else:
                            i.myCourseIcon = False
                            i.cartIcon = False
                            if CartItem.objects.filter(Courses = i).filter(userCartItem = user).exists():
                                i.cartIcon = True
                            i.save()
                    serializers = CatCourseSerializers(oooo, many = True)
                    

                    try:
                        if request.query_params:
                            iii = request.query_params['CourseId']
                            ll = CatCourses.objects.get(id = iii)

                            for i in ll:
                                if user in i.users.all():
                                    i.myCourseIcon = True
                                    i.cartIcon = False
                                    if CartItem.objects.filter(Courses = i).filter(userCartItem = user).exists():
                                        i.cartIcon = True
                                    i.save()

                                else:
                                    i.myCourseIcon = False
                                    i.cartIcon = False
                                    if CartItem.objects.filter(Courses = i).filter(userCartItem = user).exists():
                                        i.cartIcon = True
                                    i.save()
                            serializers = CatCourseSerializers(ll)
                            
                        
                    except:
                        pass
            except:
                pass
        else:
            d = college.objects.all()
            serializers = collegeSerializers(d , many=True)
        return Response({"data":serializers.data},status=status.HTTP_200_OK)


class AddToCArt(generics.GenericAPIView):
    serializer_class = CartItemSerilaizers
    permission_classes = [HasAPIKey]
    def post(self,request):
        yy = authenticate(request=request)
        if yy.get('status') == False:
            return Response (yy, status=status.HTTP_200_OK)
        user = yy.get('user')
        course = request.data.get('CourseId')
        try:
            id =CatCourses.objects.get(id = course)
            car = Cart.objects.get(userCart = user)
            try:
                CartItem.objects.filter(userCartItem = user).get(Courses = id)
                return Response({"message":"this course in cart"},status=status.HTTP_200_OK)
            except:
                CartItem.objects.create(userCartItem = user,cart= car, Courses=id, price=int(id.price))
                carr = Cart.objects.get(userCart= user)
                r = CartItem.objects.filter(cart = carr)
                carr.totlaPrice = 0
                carr.save()
                for i in r:
                
                    carr.totlaPrice = carr.totlaPrice + i.price
                    carr.save()
                return Response({"message":"done"},status=status.HTTP_200_OK)
        except:
            
            return Response({"message":"None id"},status=status.HTTP_200_OK)
    def delete(self,request):
        yy = authenticate(request=request)
        if yy.get('status') == False:
            return Response (yy, status=status.HTTP_200_OK)
        user = yy.get('user')
        course = request.data.get('CourseId')
        try:
            id =CartItem.objects.get(id = course)
            id.delete()
            carr = Cart.objects.get(userCart= user)

            r = CartItem.objects.filter(cart = carr)
            carr.totlaPrice = 0
            carr.save()
            for i in r:
                
                carr.totlaPrice = carr.totlaPrice + i.price
                carr.save()
            return Response({"message":"deleted"},status=status.HTTP_200_OK)
        except:
            
            return Response({"message":"None id"},status=status.HTTP_200_OK)

class CartView(generics.GenericAPIView):
    serializer_class = CartSerializers11
    permission_classes = [HasAPIKey]

    def get(self, request):
        yy = authenticate(request=request)
        if yy.get('status') == False:
            return Response (yy, status=status.HTTP_200_OK)
        user = yy.get('user')

        cartt = Cart.objects.filter(userCart = user).all()
        s = CartSerializers11(cartt, many=True)
        return Response({"data":s.data}, status=status.HTTP_200_OK)
            
class MyCoursesView(generics.GenericAPIView):
    serializer_class = CatCourseSerializers
    permission_classes = [ HasAPIKey]
    def get(self,request):
        yy = authenticate(request=request)
        if yy.get('status') == False:
            return Response (yy, status=status.HTTP_200_OK)
        user = yy.get('user')
        if request.query_params:
            pp = request.query_params['CourseId']
            y = CatCourses.objects.get(id = pp)
            serializers = CatWithvideSerializers(y)
            try:
                if request.query_params:
                    ll = request.query_params['VideoId']
                    yy = Courses.objects.get(id = ll)
                    serializers = CourseSerializers(yy)
            except:
                pass
        else:
            d = CatCourses.objects.filter(users = user).all()
            serializers = CatCourseSerializers(d , many = True)
        return Response({"data":serializers.data},status=status.HTTP_200_OK)

    
class BanarsView(generics.GenericAPIView):
    serializer_class = BannarsSerializers
    permission_classes = [ HasAPIKey]
    def get (self , request):
        qq = Banars.objects.all()
        serializers = self.serializer_class(qq , many = True)
        return Response({"data":serializers.data},status=status.HTTP_200_OK)

class RecomendedView(generics.GenericAPIView):
    serializer_class = CatCourseSerializers
    permission_classes = [HasAPIKey]
    def get (self , request):
        yy = authenticate(request=request)
        if yy.get('status') == False:
            return Response (yy, status=status.HTTP_200_OK)
        user = yy.get('user')
        if request.query_params:
            pp = request.query_params['CourseId']
            yy = CatCourses.objects.get(id = pp)
            if user in yy.users.all():
                yy.myCourseIcon = True
                yy.cartIcon = False
                if CartItem.objects.filter(Courses = yy).filter(userCartItem = user).exists():
                    yy.cartIcon = True
                yy.save()
            else:
                yy.myCourseIcon = False
                yy.cartIcon = False
                if CartItem.objects.filter(Courses = yy).filter(userCartItem = user).exists():
                    yy.cartIcon = True
                yy.save()
            serializers = self.serializer_class(yy)
        else:
            ll = CatCourses.objects.filter(year = user.year).filter(active = True).all()
            for i in ll:
                if user in i.users.all():
                    i.myCourseIcon = True
                    i.cartIcon = False
                    if CartItem.objects.filter(Courses = i).filter(userCartItem = user).exists():
                        i.cartIcon = True
                    i.save()
                    
                else:
                    i.myCourseIcon = False
                    i.cartIcon = False
                    if CartItem.objects.filter(Courses = i).filter(userCartItem = user).exists():
                        i.cartIcon = True
                    i.save()
            serializers = self.serializer_class(ll, many = True)
        return Response({"data":serializers.data}, status= status.HTTP_200_OK)


class applePay(generics.GenericAPIView):
    serializer_class = CartItemSerilaizers
    def post(self , request):
        yy = authenticate(request=request)
        if yy.get('status') == False:
            return Response (yy, status=status.HTTP_200_OK)
        user = yy.get('user')
        if yy.get('status'):
            user = request.user
            if payy.objects.filter()[0].active == False:
                return Response({'status':False , 'message':'error in payment'}, status=status.HTTP_200_OK)
            pp = Cart.objects.get(userCart = user)
            y = CartItem.objects.filter(cart = pp).all()
            for p in y:
                p.Courses.users.add(user)
                p.delete()
            pp.totlaPrice = int (00)
            pp.save()
            return Response({'status':True, 'message':'payment done '}, status=status.HTTP_200_OK)
        else:
            return Response({'status':False , 'message':'you are not login'}, status=status.HTTP_200_OK)
