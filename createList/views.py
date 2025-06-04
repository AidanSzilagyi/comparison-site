from django.shortcuts import render

# Create your views here.
def homepage_redirect(request):
    return render(request, 'createList/home.html')

def homepage(request):
    return render(request, 'createList/home.html')

def createListPage(request):
    return render(request, 'createList/createList.html')
    
# return render(request, 'mainmenu/profile.html', context)


# Head2Head (two arrows facing one another)