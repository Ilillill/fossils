from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import json
from django.db.models import Min, Max, Avg
from django.core.mail import send_mail

from .models import DBFossil, DBSpecies, Profile
from .forms import FormSpecies, FormFossil, FormAccount, FormProfile, FormEmail

@login_required
def home(request):
    species = DBSpecies.objects.filter(species_owner=request.user)
    fossils_without_specie = DBFossil.objects.filter(fossil_owner=request.user, fossil_species__isnull=True)    
    return render(request, 'app_fossils/home.html', {
        'species': species,
        'fossils_without_specie': fossils_without_specie,
    })

@login_required
def species_add(request):
    forms_species_add = FormSpecies(request.user)
    if request.method == "POST":
        forms_species_add = FormSpecies(request.user, request.POST, request.FILES)
        if forms_species_add.is_valid():
            new_species = forms_species_add.save(commit=False)
            new_species.species_owner = request.user
            new_species.save()
            messages.success(request, f"{new_species.species_name} added successfuly")
            return redirect('homepage')
    return render(request, "app_fossils/species_add.html", {'form_species_add': forms_species_add,})

@login_required
def species_update(request, pk):
    species_to_update = get_object_or_404(DBSpecies, id=pk)
    if species_to_update.species_owner != request.user:
        messages.error(request, "This data belongs to a different user.")
        return redirect('account_logout')
    if request.method == "POST":
        form_species_update = FormSpecies(request.user, request.POST, request.FILES, instance=species_to_update)
        if form_species_update.is_valid():
            form_species_update.save(commit=False)
            form_species_update.species_owner = request.user
            form_species_update.save()
            messages.success(request, f"{species_to_update.species_name} updated successfuly")
            return redirect('homepage')
    else:
        form_species_update = FormSpecies(request.user, instance=species_to_update)
    
    return render(request, 'app_fossils/species_update.html', {
        'form_species_update': form_species_update,
        'species_to_update': species_to_update,
    })

@login_required
def species_delete(request, pk):
    species_to_delete = get_object_or_404(DBSpecies, id=pk)
    if species_to_delete.species_owner != request.user:
        messages.error(request, "This data belongs to a different user.")
        return redirect('account_logout')
    if request.method == "POST":
        species_to_delete.delete()
        messages.success(request, f"{species_to_delete.species_name} deleted successfully")
        return redirect('homepage')
    return render(request, 'app_fossils/species_delete.html', {'species_to_delete': species_to_delete,})

@login_required
def fossil_add(request):
    forms_fossil_add = FormFossil(request.user)
    if request.method == "POST":
        forms_fossil_add = FormFossil(request.user, request.POST, request.FILES)
        if forms_fossil_add.is_valid():
            new_fossil = forms_fossil_add.save(commit=False)
            new_fossil.fossil_owner = request.user
            new_fossil.save()
            forms_fossil_add.save_m2m()
            return redirect('fossil-selected', pk=new_fossil.id)
    return render(request, "app_fossils/fossils_add.html", {'forms_fossil_add': forms_fossil_add,})

@login_required
def fossil_update(request, pk):
    fossil_to_update = get_object_or_404(DBFossil, id=pk)
    if fossil_to_update.fossil_owner != request.user:
        messages.error(request, "This data belongs to a different user.")
        return redirect('account_logout')
    if request.method == "POST":
        form_fossil_update = FormFossil(request.user, request.POST, request.FILES, instance=fossil_to_update)
        if form_fossil_update.is_valid():
            fossil_to_update = form_fossil_update.save(commit=False)
            fossil_to_update.fossil_owner = request.user
            fossil_to_update.save()
            messages.success(request, f"{fossil_to_update.fossil_name} updated successfuly")
            return redirect('fossil-selected', pk=fossil_to_update.id)
    else:
        form_fossil_update = FormFossil(request.user, instance=fossil_to_update)

    return render(request, 'app_fossils/fossils_update.html', {
        'form_fossil_update': form_fossil_update,
        'fossil_to_update': fossil_to_update,
    })

@login_required
def fossil_delete(request, pk):
    fossil_to_delete = get_object_or_404(DBFossil, id=pk)
    if fossil_to_delete.fossil_owner != request.user:
        messages.error(request, "This data belongs to a different user.")
        return redirect('account_logout')
    if request.method == "POST":
        fossil_to_delete.delete()
        messages.success(request, f"{fossil_to_delete.fossil_name} deleted successfully")
        if fossil_to_delete.fossil_species:
            return redirect('species-selected', pk=fossil_to_delete.fossil_species.id)
        else:
            return redirect('homepage')
    return render(request, 'app_fossils/fossils_delete.html', {'fossil_to_delete': fossil_to_delete,})


@login_required
def species(request, pk):
    specie = get_object_or_404(DBSpecies, id=pk)
    if request.user != specie.species_owner:
        messages.error(request, "This data belongs to a different user.")
        return redirect('account_logout')
    fossils = DBFossil.objects.filter(fossil_species=specie)
    return render(request, 'app_fossils/species.html', {
        'specie': specie,
        'fossils': fossils,
    })

@login_required
def fossil(request, pk):
    fossil = get_object_or_404(DBFossil, id=pk)

    if fossil.fossil_owner != request.user:
        messages.error(request, "This data belongs to a different user.")
        return redirect('account_logout')
    
    if request.method == "POST" and "fossil_delete" in request.POST:
        fossil.delete()
        messages.success(request, f"{fossil.fossil_name} deleted successfully")
        if fossil.fossil_species:
            return redirect('species-selected', pk=fossil.fossil_species.id)
        else:
            return redirect('homepage')
    
    if request.method == "POST" and "fossil_update" in request.POST:
        form_fossil_update = FormFossil(request.user, request.POST, request.FILES, instance=fossil)
        if form_fossil_update.is_valid():
            fossil = form_fossil_update.save(commit=False)
            fossil.fossil_owner = request.user
            fossil.save()
            messages.success(request, f"{fossil.fossil_name} updated successfuly")
            return redirect('fossil-selected', pk=fossil.id)
    else:
        form_fossil_update = FormFossil(request.user, instance=fossil)
    
    if request.method == "POST" and "fossil_favourite" in request.POST:
        if fossil.fossil_is_favourite:
            fossil.fossil_is_favourite = False
            messages.success(request, f"{fossil.fossil_name} removed from favourites")
        else:
            fossil.fossil_is_favourite = True
            messages.success(request, f"{fossil.fossil_name} added to favourites")
        fossil.save()

    if request.method == "POST" and "send_email" in request.POST:
        form_send_email = FormEmail(request.POST)
        if form_send_email.is_valid():
            subject = fossil.fossil_name

            text_note = ''
            note = form_send_email.cleaned_data['email_note']
            if note:
                text_note = f'<p>{text_note}</p>'

            text_price = ''
            price = form_send_email.cleaned_data['include_price']
            if price and fossil.fossil_value:
                text_price = f'<p>{fossil.fossil_value}</p>'

            text_description = ''
            if fossil.fossil_description_short:
                text_description += fossil.fossil_description_short
            if fossil.fossil_description_detailed:
                text_description += fossil.fossil_description_detailed

            html = f'''
                    <html>
                        <body>
                            <div>
                            <h1>{subject}</h1>
                            {note}
                            {text_price}
                            {text_description}
                            </div>
                        </body>
                    </html>'''
            
            from_email = "app@sharedprojects.co.uk"
            email = form_send_email.cleaned_data['email']
            to_email = (email, )
            try:
                send_mail(subject=subject, message="", from_email=from_email, recipient_list=to_email, html_message=html)
                messages.success(request, f"Email to {email} sent successfully.")
            except Exception as e:
                messages.error(request, f"Error, email not sent. {e}")

            return redirect('fossil-selected', pk=fossil.id)
        else:
            messages.error(request, f"Error, email not sent.")
            return redirect('fossil-selected', pk=fossil.id)
    else:
        form_send_email = FormEmail()

    return render(request, 'app_fossils/fossil.html', {
        'fossil': fossil,
        'form_fossil_update': form_fossil_update,
        'form_send_email': form_send_email,
        })


@login_required
def user_profile(request):
    return render(request, 'app_fossils/user_profile.html')

@login_required
def user_account_update(request):
    if request.method == "POST":
        form = FormAccount(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = FormAccount(instance=request.user)

    return render(request, 'app_fossils/user_account_update.html', {'form': form,})

@login_required
def user_profile_create_update(request):
    # Use Django get_or_create method to handle form submission depending whether the profile already exists or not
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = FormProfile(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('profile')
    else:
        form = FormProfile(instance=user_profile)

    option = 'Update' if not created else 'Create'

    return render(request, 'app_fossils/user_profile_create_update.html', {'form': form, 'option': option,})

@login_required
def search_result_get(request):
    species = DBSpecies.objects.filter(species_owner=request.user)
    fossils = DBFossil.objects.filter(fossil_owner=request.user)

    query = request.GET.get('search_get')
    species_result, fossils_result = None, None
    if species:
        species_result = species.filter(Q(species_name__icontains=query.strip().lower()) | Q(species_description__icontains=query.strip().lower()))
    if fossils:
        fossils_result = fossils.filter(Q(fossil_name__icontains=query.strip().lower()) | Q(fossil_description_short__icontains=query.strip().lower()))

    return render(request, 'app_fossils/search_result.html', {
        'species_result': species_result,
        'fossils_result': fossils_result,
        'search_type': 'GET',
    })

@login_required
def search_result_post(request):
    species = DBSpecies.objects.filter(species_owner=request.user)
    fossils = DBFossil.objects.filter(fossil_owner=request.user)

    query = request.POST.get('search_post')
    species_result, fossils_result = None, None
    if species:
        species_result = species.filter(Q(species_name__icontains=query.strip().lower()) | Q(species_description__icontains=query.strip().lower()))
    if fossils:
        fossils_result = fossils.filter(Q(fossil_name__icontains=query.strip().lower()) | Q(fossil_description_short__icontains=query.strip().lower()))

    return render(request, 'app_fossils/search_result.html', {
        'species_result': species_result,
        'fossils_result': fossils_result,
        'search_type': 'POST',
    })


@login_required
def chart_simple(request):
    species = DBSpecies.objects.filter(species_owner=request.user)
    labels = [specie.species_name for specie in species]
    labels.append('NO SPECIE')
    data = [DBFossil.objects.filter(fossil_species=specie).count() for specie in species]
    data.append(DBFossil.objects.filter(fossil_owner=request.user, fossil_species__isnull=True).count())

    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Number of fossils in species',
            'data': data,
            'backgroundColor': '#00ADB5',
            'borderColor': '#EEEEEE',
            'pointBackgroundColor': 'white',
            'pointBorderColor': '#000000'
        }
        ]
    }

    return render(request, 'app_fossils/chart_simple.html', {'chart_data': json.dumps(chart_data)})

@login_required
def chart_multi(request):
    species = DBSpecies.objects.filter(species_owner=request.user)
    fossil_ages = {'youngest': [], 'oldest': [],'average': []}

    for specie in species:
        fossils = DBFossil.objects.filter(fossil_species=specie)

        youngest_fossil = fossils.filter(fossil_age_in_years=fossils.aggregate(Min('fossil_age_in_years'))['fossil_age_in_years__min'])
        if youngest_fossil:
            fossil_ages['youngest'].append(float(youngest_fossil.first().fossil_age_in_years))
        else:
            fossil_ages['youngest'].append(None)

        oldest_fossil = fossils.filter(fossil_age_in_years=fossils.aggregate(Max('fossil_age_in_years'))['fossil_age_in_years__max'])
        if oldest_fossil:
            fossil_ages['oldest'].append(float(oldest_fossil.first().fossil_age_in_years))
        else:
            fossil_ages['oldest'].append(None)

        average_age = fossils.aggregate(Avg('fossil_age_in_years'))['fossil_age_in_years__avg']
        if average_age:
            fossil_ages['average'].append(float(average_age))
        else:
            fossil_ages['average'].append(None)

    labels = [specie.species_name for specie in species]

    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Oldest age',
            'data': fossil_ages['oldest'],
            'borderColor': '#0081C9',
            'backgroundColor': '#0081C9',
            'yAxisID': 'y',
        },
        {
            'label': 'Average age',
            'data': fossil_ages['average'],
            'borderColor': '#5BC0F8',
            'backgroundColor': '#5BC0F8',
            'yAxisID': 'y',
        },
        {
            'label': 'Youngest age',
            'data': fossil_ages['youngest'],
            'borderColor': '#86E5FF',
            'backgroundColor': '#86E5FF',
            'yAxisID': 'y',
        }
        ]
    }

    return render(request, 'app_fossils/chart_multi.html', {'chart_data': json.dumps(chart_data)})