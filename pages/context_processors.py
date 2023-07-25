from books.models import Interest

def category_objs(request):
    print("ok")
    return {"category_objs":Interest.objects.all().order_by("-id")}