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
from django.utils.http import urlencode
import json
import uuid
import random
import csv
from io import TextIOWrapper
from django.db.models import Q

NUM_STARTING_FORMS = 10
NUM_MATCHUPS_SENT = 20
NUM_LOADED_THINGS_PER_REQUEST = 3

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

@login_required
def start_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile_check(request):
    user = request.user
    next_url = request.GET.get('next')
    #next_url = request.session.pop('next_url', '/')
    try:
        profile = user.profile
        if not profile.username:
            raise Profile.DoesNotExist
    except Profile.DoesNotExist:
        social = user.social_auth.get(provider='google-oauth2')
        extra = social.extra_data

        username =  user.first_name or 'user' + str(random.randint(1, 99999999))
        pfp_colors = ["blue", "cyan", "green", "purple", "red", "yellow"]
        picture_url = "media/profile_images/default-pfp/" + random.choice(pfp_colors) + ".png"

        profile = Profile.objects.create(
            user=user,
            username=username,
            image=picture_url
        )
        
        if next_url:
            query = urlencode({'next': next_url})
            return redirect(f'/create-profile/?{query}')
        return redirect('create_profile')
    return redirect(next_url)

@login_required
def create_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('my_profile')
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'createList/create-profile.html', {'profile_form': profile_form})

@login_required
def edit_profile(request):
    return create_profile(request)

@login_required
def list_type_choices(request):
    if request.method == 'POST' and 'file-input' in request.FILES:
        input_file = request.FILES['file-input']
        file_wrapper = TextIOWrapper(input_file.file, encoding='utf-8')
        file_data = []
        if input_file.name.endswith('.csv') or input_file.name.endswith('.txt'):
            for line in file_wrapper:
                file_data.append({"name": line.strip(), "image": None})
        else:
            return render(request, 'createList/list-type-choices.html', {"error": "You may only upload a .csv or .txt file"})
        list_form = ListForm()
        blank_forms_needed = NUM_STARTING_FORMS if len(file_data) < NUM_STARTING_FORMS else len(file_data)
        thing_form_set = modelformset_factory(Thing, form=ThingForm, extra=blank_forms_needed, can_delete=True)
        thing_forms = thing_form_set(queryset=Thing.objects.none(), initial=file_data)
        return render(request, 'createList/create-list.html', {
            'list_form': list_form, 
            'thing_forms': thing_forms,
            'new_list': True,
            'list_type': "text", 
        })
    return render(request, 'createList/modify_list/list-type-choices.html')

@login_required
def create_text_list(request, slug=None):
    return create_or_edit_list(request, 'text', slug)

@login_required
def create_images_list(request, slug=None):
    return create_or_edit_list(request, 'image', slug)
    
@login_required
def list_edit(request, slug):
    list = List.objects.get(slug=slug)
    if not list:
        return not_found(request, "That list does not exist")
    return create_or_edit_list(request, list.type, slug)

@login_required
def create_or_edit_list(request, list_type, slug=None):
    list = List.objects.get(slug=slug) if slug else None
    existing_things = Thing.objects.filter(list=list) if list else Thing.objects.none()
        
    thing_form_set = modelformset_factory(Thing, form=ThingForm, extra=0, can_delete=True)
    if request.method == 'GET':
        list_form = ListForm(instance=list)
        thing_forms = thing_form_set(queryset=existing_things)
    if request.method == 'POST':
        list_form = ListForm(request.POST, request.FILES, instance=list)
        thing_forms = thing_form_set(request.POST, request.FILES, queryset=existing_things)
        for i, form in enumerate(thing_forms):
            if not form.is_valid():
                print(f"Form {i} errors:", form.errors)
        print("Form may be valid")
        print(list_form.is_valid())
        print(thing_forms.is_valid())
        if thing_forms.is_valid() and list_form.is_valid():
            print("form maybebe valid")
            things = [form for form in thing_forms if form.cleaned_data and not form.cleaned_data.get('DELETE')]
            if len(things) < 3:
                return render(request, 'createList/modify_list/create-list.html', {
                    'list_form': list_form,
                    'thing_forms': thing_forms,
                    'new_list': list == None,
                    'list_type': list_type,
                    'error': 'You must include at least 3 things.'
                })
            print("form is valid!")
            
            list = list_form.save(commit=False)
            list.user = request.user
            list.num_things = len(things)
            list.type = list_type
            list.save()
            print("List Saved", list)
            for form in things:
                thing = form.save(commit=False)
                thing.list = list
                thing.save()
            
            for form in thing_forms.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            
            return redirect('list_info', list.slug)
        
    return render(request, 'createList/modify_list/create-list.html', {
        'list_form': list_form,
        'thing_forms': thing_forms,
        'new_list': list == None,
        'list_type': list_type,
    }) 
    return HttpResponse("Neither GET nor POST")

@login_required
def images_only_create_list(request):
    return render(request, 'createList/home.html')

# @login_required
# def list_edit(request, slug):
#     list = List.objects.get(slug=slug)
#     thing_form_set = modelformset_factory(Thing, form=ThingForm, extra=0, can_delete=True)
#     thing_forms = thing_form_set(queryset=Thing.objects.filter(list=list))
#    
#     list_form = ListForm(instance=list)
#     return render(request, 'createList/create-list.html', {
#             'list_form': list_form,
#             'thing_forms': thing_forms,
#             'empty_form': thing_forms.empty_form,
#         }) 

def all_lists(request):
    all_lists = List.objects.all()
    return render(request, 'createList/all-lists.html', {"all_lists": all_lists})

def list_rank(request, slug):
    #matchups = Matchup.objects.all()
    #notdone = True
    #for matchup in matchups:
    #    if not matchup.loser and notdone:
    #        print(matchup.winner.name)
    #        matchup.delete()
    #        notdone = False
    
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
    body = json.loads(request.body)
    if not body.get('id'):
        return JsonResponse({'error': 'Missing matchup ID'}, status=400)
    process_matchup_result(request.user, list, body.get('id'), body.get('choice'))
    return HttpResponse(status=204)

# Note the slicing and list() calls. Allowing lazy evaluation can lead to incorrect results
def list_info(request, slug):
    tlist = List.objects.get(slug=slug)
    all_things = Thing.objects.filter(list=tlist)  
    top_five = list(all_things.order_by('-rating')[:5])
    bottom_five = list(all_things.order_by('rating')[:5])[::-1] 
    
    top_five_matchups = [get_matchups(thing) for thing in top_five]
    bottom_five_matchups = [get_matchups(thing) for thing in bottom_five]
    
    # if <15 things, show the whole list
    context = {
        "list": tlist,
        "top_five": list(zip(top_five, top_five_matchups)),
        "bottom_five": list(zip(bottom_five, bottom_five_matchups)),
    }
    return render(request, 'createList/list-info.html', context)

def get_all_things(request, slug):
    list = List.objects.get(slug=slug)
    num_things_loaded = int(request.GET.get("loaded"))
    if num_things_loaded + NUM_LOADED_THINGS_PER_REQUEST >= list.num_things:
        things = Thing.objects.filter(list=list).order_by("-rating")[num_things_loaded:]
    else:
        things = Thing.objects.filter(list=list).order_by("-rating")[num_things_loaded:num_things_loaded + NUM_LOADED_THINGS_PER_REQUEST]
    
    things_array = []
    for thing in things:
        things_array.append({
                "name": thing.name if thing.name else None,
                "image": thing.image.url if thing.image else None,
                "wins": thing.wins,
                "losses": thing.losses,
            },
        )
    return JsonResponse({"things": things_array})


def get_matchups(thing):
    matches = Matchup.objects.filter(awaiting_response=False, winner_id=thing.id) | \
              Matchup.objects.filter(awaiting_response=False, loser_id=thing.id)
    matches = matches.order_by('date_created')
    if len(matches) > NUM_MATCHUPS_SENT:
        return matches[0:NUM_MATCHUPS_SENT]
    return matches
        

@login_required
def my_profile(request):
    lists = List.objects.filter(user=request.user)
    context = {
        "profile": request.user.profile,
        "recent_lists": None,
        "user_lists": lists,
        "owner": True,
    }
    return render(request, 'createList/profile.html', context)

def view_profile(request, slug):
    profile = Profile.objects.get(slug=slug)
    if not profile:
        not_found(request, "That user does not exist.")
    lists = List.objects.filter(user=profile.user)
    context = {
        "profile": profile,
        "recent_lists": None,
        "user_lists": lists,
    }
    return render(request, 'createList/profile.html', context)

def list_card_test(request):
    return render(request, 'createList/list-card-prototype.html')

def not_found(request, reason):
    if not reason:
        reason = "We could not find that page."
    return JsonResponse({'error': reason}, status=404)