from django.shortcuts import render, redirect
from .models import Thing, List, Profile, Matchup
from .forms import ListForm, ThingForm, ProfileForm
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .rank_systems import generate_matchup_json, process_matchup_result
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
import uuid


def home(request):
    return render(request, 'createList/home.html')

def explore(request):
    return redirect('home')

def recent(request):
    return redirect('home')


# return render(request, 'mainmenu/profile.html', context)
# Head2Head (two arrows facing one another)
def start_login(request):
    logout(request)
    return redirect('social:begin', backend='google-oauth2')

def profile_check(request):
    next_url = request.session.get('next_url', '/')
    print("getattr:", getattr(request.user, 'profile', "No Profile"))

    if not getattr(request.user, 'profile', None):
        Profile.objects.create(user=request.user)
        #next_url = request.GET.get('next') or '/'
        #request.session['next_url'] = next_url
        return redirect('create_profile')
    elif not request.user.profile.username:
        #next_url = request.GET.get('next') or '/'
        #request.session['next_url'] = next_url
        return redirect('create_profile')
    return redirect(next_url)


def create_profile(request):
    if request.method == 'GET':
        profile_form = ProfileForm()
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile = profile_form.save()
            return redirect(request.session.pop('next_url', '/'))
    return render(request, 'createList/create-profile.html', {'profile_form': profile_form})

@login_required
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
            if len(things) < 3:
                return render(request, 'createList/create-list.html', {
                    'list_form': list_form,
                    'thing_forms': thing_forms,
                    'empty_form': thing_forms.empty_form,
                    'error': 'You must include at least 3 things.'
                })
            list = list_form.save()
            list.num_things = len(things)
            list.user = request.user
            list.save()
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
    list = List.objects.get(slug=slug)
    initial_things = generate_matchup_json(request.user, list)
    return render(request, 'createList/rank.html', {"initial_things": initial_things, "list_slug": slug})

def get_comparisons(request, slug):
    list = List.objects.get(slug=slug)
    if not list:
        return JsonResponse({'error': 'Unknown list slug'}, status=400)
    
    sent_matchups = []
    if request.GET.get("ids", ""):
        ids = request.GET.get("ids").split(",")
        if ids:
            uuids = [uuid.UUID(id) for id in ids if id]
            sent_matchups = Matchup.objects.filter(id__in=uuids)

    Matchup.objects.filter(id__in=ids)
    comparisons = generate_matchup_json(request.user, list, sent_matchups)
    return JsonResponse({'comparisons': comparisons})

def complete_comparison(request, slug):
    list = List.objects.get(slug=slug)
    if not list or not body.get('id'):
        return JsonResponse({'error': 'Unknown list slug'}, status=400)
    body = json.loads(request.body)
    process_matchup_result(request.user, list, body.get('id'), body.get('choice'))
    return HttpResponse(status=204)

def list_info(request, slug):
    list = List.objects.get(slug=slug)
    all_things = Thing.objects.filter(list=list).order_by('rating')
    top_five = all_things[0:5]
    bottom_five = all_things[list.num_things - 5:]
    
    # if <15 things, show the whole list
    context = {
        "list": list,
        "top_five": top_five,
        "bottom_five": bottom_five,
    }
    return render(request, 'createList/list-info.html', context)

@login_required
def my_profile(request):
    return redirect('home')

def view_profile(request, slug):
    profile = Profile.objects.get(slug=slug)
    if not list:
        not_found(request, "That user does not exist.")
    lists = List.objects.filter(user=profile.user)
    context = {
        "profile": profile,
        "recent_lists": None,
        "user_lists": lists,
    }
    return render(request, 'createList/profile.html', context)

def list_edit(request, slug):
    return render(request, 'createList/home.html')

def list_card_test(request):
    return render(request, 'createList/list-card-prototype.html')

def not_found(request, reason):
    if not reason:
        reason = "We could not find that page."
    return JsonResponse({'error': reason}, status=404)