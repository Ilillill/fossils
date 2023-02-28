from django.contrib.auth.models import AnonymousUser
from .models import DBSpecies

def user_species(request):
    if isinstance(request.user, AnonymousUser):
        user_species = DBSpecies.objects.none()
    else:
        user_species = DBSpecies.objects.filter(species_owner=request.user)
    return {'user_species': user_species}