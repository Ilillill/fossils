from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import DBFossil, DBSpecies
from .forms import FormSpecies, FormFossil

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
            return redirect('homepage')
    return render(request, "app_fossils/species_add.html", {'form_species_add': forms_species_add,})

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
def species(request, pk):
    specie = get_object_or_404(DBSpecies, id=pk)
    print(specie.species_owner)
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
    return render(request, 'app_fossils/fossil.html', {'fossil': fossil,})
