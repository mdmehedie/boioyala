from django.shortcuts import render
from django.views import View 
from .models import User ,Institute,Interest
import random 
from django.http import JsonResponse
from django.contrib.auth import logout,authenticate,login

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



class ProfileUpdateView(View):
    def post(self,request):
        user=request.user 
        action=request.POST.get('action')
        if action=="about_me":
            user.name=request.POST.get("name")
            user.occupation=request.POST.get("occupation")
            user.gender=request.POST.get("gender")
            user.district=request.POST.get("district")
            user.upazila=request.POST.get("upazila")
            user.city=str(request.POST.get("upazila"))+", " +str(request.POST.get("district"))
            user.address=request.POST.get("address") 
            user.save()
        elif action=="interest":
            interest=Interest.objects.get(id=request.POST.get("interest"))
            user.interest=interest
            user.save() 

        elif action=="password_change":
            old_password=request.POST.get("old_password")
            new_password=request.POST.get("new_password")
            confirm_password=request.POST.get("confirm_password")
            user=authenticate(email=user.email,password=old_password)
            error=""
            if not user:
                error="Incorrect password"
            elif new_password!=confirm_password:
                error="Doesn't match confirm password"
            
            if not error:
                error=""
                user.set_password(new_password)
                user.save()
                login(request,user)
                return JsonResponse({"msg":"change_password","error":""})
            return JsonResponse({"msg":"change_password","error":error})

        return JsonResponse({"data":"updated","msg":action})