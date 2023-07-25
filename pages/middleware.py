from django.shortcuts import redirect

def auth_middleware(get_response):
    def middleware(request):
        if not request.user.is_authenticated:
            return_url=request.META["PATH_INFO"]
            return redirect(f"/?return_url={return_url}")

        response = get_response(request)
        return response

    return middleware