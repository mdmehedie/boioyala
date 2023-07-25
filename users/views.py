from django.shortcuts import render
from django.views import View 
from .models import User ,Institute,Interest
import random 
from django.http import JsonResponse

class SetProfileView(View):
    def post(self,request):
        user=User.objects.get(id=request.user.id)
        action=request.POST.get("action")
        if action=="send_otp":
            phone=request.POST.get("phone")
            otp=random.randint(1111,9999)
            user.phone=phone 
            user.otp=otp
            user.save()
            print(phone,otp)
            return JsonResponse({"msg":"success","data":"send otp"})
        
        elif action=="verifiy_otp":
            phone=request.POST.get("phone")
            otp=request.POST.get("otp")
            print(phone,otp)
            user=User.objects.filter(id=request.user.id,phone=phone,otp=otp).last()
            if user:
                user.is_verified=True 
                user.save()
                return JsonResponse({"msg":"success","data":"verified"})
            else:
                return JsonResponse({"msg":"Invalid or Expired OTP","data":"un_verified"})
            
        elif action=="set_city":
            district=request.POST.get("district")
            upazila=request.POST.get("upazila")
            user.district=district
            user.upazila=upazila
            user.city=f"{upazila}, {district}"
            user.save()
           
            return JsonResponse({"msg":"success","data":"valid"})
        elif action=="set_institute":
            institute=request.POST.get("institute")
            inst_obj=Institute.objects.filter(name=institute).exists()
            obj=""
            if inst_obj:
                obj=Institute.objects.get(name=institute)
            else:
                obj=Institute.objects.create(name=institute)
            
            user.institute=obj
            user.save()
            return JsonResponse({"msg":"success","data":"valid"})
        
        elif action=="set_interest":
            interest=request.POST.get("interest")
            obj=Interest.objects.get(id=interest)
            user.interest=obj 
            user.save()
            return JsonResponse({"msg":"success","data":"valid"})
