from django.shortcuts import render, redirect
from .models import Thing, List
from .forms import ListForm, ThingForm
from django.forms import modelformset_factory
from django.http import HttpResponse

# Create your views here.
def homepage_redirect(request):
    return render(request, 'createList/home.html')

def homepage(request):
    return render(request, 'createList/home.html')


# return render(request, 'mainmenu/profile.html', context)
# Head2Head (two arrows facing one another)


def create_list(request):
    thing_form_set = modelformset_factory(Thing, form=ThingForm, extra=0, can_delete=True)
    print(request.method)
    if request.method == 'GET':
        
        list_form = ListForm()
        thing_forms = thing_form_set(queryset=Thing.objects.none())
        context = {'list_forms': list_form, 'thing_form': thing_forms}
        return render(request, 'createList/create-list.html', context)
    if request.method == 'POST':
        list_form = ListForm(request.POST, request.FILES)
        thing_forms = thing_form_set(request.POST, request.FILES, queryset=Thing.objects.none())
        if list_form.is_valid() and thing_forms.is_valid():
            things = [form for form in thing_forms if form.cleaned_data and not form.cleaned_data.get('DELETE')]
            print(things)
            if len(things) < 3:
                return render(request, 'createList/create-list.html', {
                    'list_form': list_form,
                    'thing_forms': thing_forms,
                    'empty_form': thing_forms.empty_form,
                    'error': 'You must include at least 3 things.'
                })
                
            list = list_form.save()
            for form in things:
                thing = form.save(commit=False)
                thing.list = list
                thing.save()
            
            # To actually delete forms (when editing)
            # for form in formset.deleted_forms:
            #    if form.instance.pk:
            #        form.instance.delete()

            return redirect('list_info', list.slug)
        return HttpResponse("Form is Invalid") 
    return HttpResponse("Neither GET nor POST")   
    
            
  
    
def list_info(request, slug):
    return render(request, 'createList/home.html')
def list_compare(request, slug):
    return render(request, 'createList/home.html')
def list_edit(request, slug):
    return render(request, 'createList/home.html')
