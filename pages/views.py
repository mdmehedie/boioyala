from django.shortcuts import render,redirect
from django.views import View 
from books.models import Book,PostedBook
from users.models import User ,Interest,Institute
from django.http import HttpResponse
from books.models import Interest,PostedBook
from django.db.models import Count
from django.contrib.auth import logout,authenticate,login
from django.http import JsonResponse


class DashboardView(View):
    def get(self,request):
        user=request.user
        books=Book.objects.filter(user=user).order_by("-id")
        institutes=Institute.objects.all()
        interests=Interest.objects.all()
        posted_book=PostedBook.objects.filter(book__user=user).order_by("-id")

        context={
            "books":books,
            "posted_books":posted_book,
            "institutes":institutes,
            "interests":interests,
        }
        return render(request,"pages/dashboard.html",context)



class HomeView(View):
    def get(self,request):
        if request.user.is_authenticated:
            users=User.objects.exclude(id=request.user.id).order_by("-id")
        else:
            users=User.objects.all().order_by("-id")
        books=Book.objects.all()
        
        context={
            "users":users,
            "books":books
        }
        return render(request,"pages/index.html",context)

class BookView(View):
    def get(self,request,slug=None):
        if slug:
            try:
                book=PostedBook.objects.get(slug=slug)
            except:
                return HttpResponse("Not found")
            
            return render(request,"pages/book_detail.html",{"book":book})
        if request.user.is_authenticated:
            books=PostedBook.objects.exclude(book__user=request.user).order_by("-id")
        else:
            books=PostedBook.objects.order_by("-id")
        
        context={
            "books":books
        }
        return render(request,"pages/books.html",context)

class DonateBookView(View):
    def post(self,request):
        name=request.POST.get("name")
        author=request.POST.get("author")
        quantity=request.POST.get("quantity")
        category=request.POST.get("categories")
        description=request.POST.get("description")
        district=request.POST.get("district")
        upazila=request.POST.get("upazila")
        cover=request.FILES["cover"]
        

        book=Book(
            name=name,
            author=author,
            categories=Interest.objects.get(id=category),
            description=description,
            cover=cover,
            user=request.user,
            iteration=quantity,
            district=district,
            upazila=upazila
        )
        book.save()
        for i in range(int(quantity)):
            post_book=PostedBook(
                book=book,
                donar=request.user,
                reader=request.user
                
            )
            post_book.save()
        return redirect("dashboard")

class ProfileView(View):
    def get(self,request,url=None):
        # if url:
        #     try:
        #         user=User.objects.get(url=url)
        #     except:
        #         return HttpResponse("Not found")
        #     books=Book.objects.filter(user=user).order_by("-id")
        #     context={
        #         "obj":user,
        #         "books":books,
            # }
            # return render(request,"pages/profile_detail.html",context)
        # return JsonResponse("Not found")
        

        users=User.objects.all().order_by("-id")
        context={
            "users":users
        }
        return render(request,"pages/profile.html",context)

 
def request_for_book(request,slug):
    if request.user.is_authenticated:
        try:
            post=PostedBook.objects.get(slug=slug)
        except:
            return HttpResponse("Not found")
        post.requestor=request.user 
        post.book_position="Requested"
        post.save()
        return redirect("books")
    return redirect("/?return_url=/books")



def post_status_view(request,slug):
    if request.user.is_authenticated:
        try:
            post=PostedBook.objects.get(slug=slug)
        except:
            return HttpResponse("Not found")
        post.book_position="Posted"
        post.save()
        return redirect("dashboard")
    return redirect("login")




#users views 

class LoginView(View):
    def post(self,request):
        email=request.POST.get("email")
        password=request.POST.get("password")
        error,success="",False 
        if not User.objects.filter(email=email).exists():
            email="Invalid email address"
        if email and password:
            user=authenticate(email=email,password=password)
            if user:
                login(request,user)
                success=True 
            else:
                error="Incorrect Credential!"

        return JsonResponse({"error":error,"success":success})

class SignUpView(View):
    def post(self,request):
        full_name=request.POST.get("full_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("email")
        error,success="",False
        if User.objects.filter(email=email).exists():
            error="This email address already exists"
       
        else:
            user=User(
                full_name=full_name,
                email=email,
                account_type="2",
               
            )
            user.set_password(password)
            user.save() 
            success=True
            login(request,user)

        return JsonResponse({"error":error,"success":success})
     

def logout_view(request):
    logout(request)
    return redirect("/")