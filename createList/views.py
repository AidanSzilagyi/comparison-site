from django.shortcuts import render, redirect
from .models import Thing, List
from .forms import ListForm, ThingForm
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import json

# Create your views here.
def homepage_redirect(request):
    return render(request, 'createList/home.html')

def homepage(request):
    return render(request, 'createList/home.html')


# return render(request, 'mainmenu/profile.html', context)
# Head2Head (two arrows facing one another)


def create_list(request):
    thing_form_set = modelformset_factory(Thing, form=ThingForm, extra=0, can_delete=True)
    if request.method == 'GET':
        
        list_form = ListForm()
        thing_forms = thing_form_set(queryset=Thing.objects.none())
        context = {'list_form': list_form, 
                   'thing_forms': thing_forms,
                   'empty_form': thing_forms.empty_form,
                   }
        return render(request, 'createList/create-list.html', context)
    if request.method == 'POST':
        list_form = ListForm(request.POST, request.FILES)
        thing_forms = thing_form_set(request.POST, request.FILES, queryset=Thing.objects.none())
        if thing_forms.is_valid() and list_form.is_valid():
            things = [form for form in thing_forms if form.cleaned_data and not form.cleaned_data.get('DELETE')]
            print("Raw POST data:", request.POST)
            print("\n", [form for form in thing_forms if form.cleaned_data])
            print(thing_forms.data)
            print(form for form in thing_forms)
            print("\nManagement forms:",thing_forms.management_form.errors)
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
        
        return render(request, 'createList/create-list.html', {
            'list_form': list_form,
            'thing_forms': thing_forms,
            'empty_form': thing_forms.empty_form,
        }) 
    return HttpResponse("Neither GET nor POST")   

def all_lists(request):
    all_lists = List.objects.all()
    return render(request, 'createList/all-lists.html', {"all_lists": all_lists})

def list_rank(request, slug):
    List.objects.get(slug=slug)
    initial_things = json.dumps(generate_comparisons(request.user, slug, limit=10))
    print(initial_things)
    return render(request, 'createList/rank.html', {"initial_things": initial_things, "list_slug": slug})

@require_GET
def get_comparisons(request, slug):
    list_slug = slug
    if not list_slug:
        return JsonResponse({'error': 'Missing list_id'}, status=400)

    comparisons = generate_comparisons(request.user, list_slug=list_slug, limit=5)
    return JsonResponse({'comparisons': comparisons})

def generate_comparisons(user, list_slug, limit):
    total = limit * 2
    list = List.objects.get(slug=list_slug)
    things = Thing.objects.filter(list=list)
    if len(things) > total:
        things = things[:total]
    else:
        total = len(things)
    comparisonJSON = []
    for i in range(0, total - 1, 2):
        first_thing = things[i]
        second_thing = things[i + 1]
        print(first_thing)
        comparisonJSON.append({
            "thing1": {
                "name": first_thing.name,
                "image":first_thing.image.url if first_thing.image else None
            },
            "thing2": {
                "name": second_thing.name,
                "image":second_thing.image.url if second_thing.image else None
            }
        })
    return comparisonJSON

def complete_comparison(request, slug):
    print("wow", slug)
    return HttpResponse(status=204)


def list_info(request, slug):
    return render(request, 'createList/home.html')
def list_edit(request, slug):
    return render(request, 'createList/home.html')
