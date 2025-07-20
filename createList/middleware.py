from django.shortcuts import redirect
from django.urls import reverse

#class RequireUsernameMiddleware:
#    def __init__(self, get_response):
#        self.get_response = get_response
#    def __call__(self, request):
#        print("here!")
#        if request.user.is_authenticated:
#            print("authenticated!")
#            profile = getattr(request.user, 'profile', None)
#            if profile and not profile.username and request.path != reverse('create-profile'):
#                print("redirect")
#                return redirect('create-profile')
#        return self.get_response(request)
    
class SaveURLBeforeAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and not request.user.is_authenticated and 'next_url' not in request.session:
            path = request.get_full_path()
            if not path.startswith(('/auth/', '/check-profile/', '/static/', '/media/')): # static/media for local
                request.session['next_url'] = path
        return self.get_response(request)

