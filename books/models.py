from django.db import models
from users.models import User,Interest

from django.utils.text import slugify
import random 

class BaseEntity(models.Model):
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract=True 

# Create your models here.
class Book(BaseEntity):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    cover=models.ImageField(upload_to="media/cover")
    author=models.CharField(max_length=255)
    categories=models.ForeignKey(Interest,on_delete=models.CASCADE,null=True)
    iteration=models.PositiveBigIntegerField()
    description=models.TextField()
    district=models.CharField(max_length=255)
    upazila=models.CharField(max_length=255)



    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(blank=True,null=True) 

    def __str__(self) -> str:
        return self.name 
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name+str(self.user.id)+"-"+str(random.randint(100,999)))
          
        return super().save(*args,**kwargs)
    
    def post_count(self):
        return PostedBook.objects.filter(book_id=self.id,status=True).count()


class PostedBook(BaseEntity):
    book=models.ForeignKey(Book,on_delete=models.CASCADE) 
    donar=models.ForeignKey(User,on_delete=models.CASCADE)
    book_position=models.CharField(choices=(
        ("Posted Now","Posted Now"),
        ("Posted","Posted"),
        ("Requested","Requested"),
    
        ("Accepted","Accepted"),
        ("Contract","Contract"),
         ("Sending","Sending"),
        ("Received","Received"),


    ),default="Posted Now",max_length=255)

   
    requestor=models.ForeignKey(User,on_delete=models.CASCADE,related_name="requestor",null=True,blank=True) 
    reader=models.ForeignKey(User,on_delete=models.CASCADE,related_name="reader")  

    slug=models.SlugField(blank=True,null=True) 
    status=models.BooleanField(default=False) 
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.book.name+self.donar.full_name+"-"+str(random.randint(1000,9999)))
        return super().save(*args,**kwargs)

    def __str__(self) -> str:
        return self.book.name 
    


class BookRequest(BaseEntity):
    posted_book=models.ForeignKey(PostedBook,on_delete=models.DO_NOTHING)
    requestor=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.posted_book.book

class BookReview(BaseEntity):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField()
    review=models.CharField(max_length=255)
    status=models.BooleanField(default=True) 
    reviewed_by=models.ForeignKey(User,on_delete=models.CASCADE) 


    def __str__(self) -> str:
        return self.book.name 
    