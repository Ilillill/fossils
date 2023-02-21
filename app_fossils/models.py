from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField
from django_resized import ResizedImageField

class DBSpecies(models.Model):
    class Meta:
        ordering = ('species_name', )
        verbose_name = "Species"
        verbose_name_plural = "Species"
    
    species_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='species_owner')
    species_name = models.CharField("Species name", max_length=150)
    species_image = ResizedImageField("Image", null=True, blank=True, upload_to="images")
    species_description = models.TextField("Description", blank=True, null=True)
    species_is_archived = models.BooleanField("Species archived", default=False)

    def get_absolute_url(self):
        return reverse('homepage') # once we have a designated page to list all species, we will update this method

    def __str__(self):
        return f"{self.species_name}"
    
    @property
    def average_fossil_value(self):
        fossils = self.fossil_set.all()
        values = [f.fossil_value for f in fossils if f.fossil_value is not None]
        if values:
            return sum(values) / len(values)
        else:
            return None
        
    @property
    def total_fossil_value(self):
        total = DBFossil.objects.filter(fossil_species=self).aggregate(total_value=models.Sum('fossil_value'))['total_value']
        return total or 0
    
    @property
    def calculate_number_of_fossils(self):
        return DBFossil.objects.filter(fossil_species=self).count()


class DBFossil(models.Model):
    class Meta:
        ordering = ('fossil_name', )
        verbose_name = 'Fossil'
        verbose_name_plural = "Fossils"

    class FossilstatusChoices(models.TextChoices):
        COLLECTION = 'Collection', 'Collection'
        SOLD = 'Sold', 'Sold'
        LOAN = 'Loan' , 'Loan'
        DONATED = 'Donated', 'Donated'
        LOST = 'Lost', 'Lost'
    
    class FossilConditionChoices(models.TextChoices):
        POOR = 'Poor', 'Poor'
        FAIR = 'Fair', 'Fair'
        GOOD = 'Good', 'Good'
        EXCELLENT = 'Excellent', 'Excellent'

    fossil_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fossil_owner')
    fossil_species = models.ForeignKey(DBSpecies, on_delete=models.SET_NULL, verbose_name="Species", related_name='species', limit_choices_to={'species_is_archived': False}, null=True)
    associated_fossils = models.ManyToManyField('self', verbose_name="Associated fossils", blank=True)

    fossil_status = models.CharField("Status", max_length=100, choices=FossilstatusChoices.choices, default="Collection")

    fossil_name = models.CharField("Fossil name", max_length=250)
    fossil_description_short = models.TextField("Short description", blank=True, null=True)
    fossil_description_detailed = HTMLField("Detailed description", blank=True, null=True)

    fossil_is_favourite = models.BooleanField("Add to favourites", default=False)

    fossil_age_in_years = models.DecimalField("Age in years", max_digits=15, decimal_places=0, blank=True, null=True)
    fossil_value = models.DecimalField("Fossil current value", max_digits=8, decimal_places=2, blank=True, null=True)

    fossil_condition = models.CharField(max_length=50, choices=FossilConditionChoices.choices, default="Good")

    fossil_date_acquired = models.DateField(default=timezone.now, blank=True, null=True)

    fossil_size = models.DecimalField("Size", max_digits=10, decimal_places=1, blank=True, null=True)
    fossil_weight = models.DecimalField("Weight", max_digits=10, decimal_places=2, blank=True, null=True)

    fossil_location = models.CharField("Location", max_length=500, blank=True, null=True)
    fossil_location_latitude = models.DecimalField("Latitude", max_digits=9, decimal_places=6, blank=True, null=True)
    fossil_location_longitude = models.DecimalField("Longitude", max_digits=9, decimal_places=6, blank=True, null=True)

    fossil_image = models.ImageField("Image", upload_to="images/", null=True, blank=True)
    fossil_image_resized = ResizedImageField("Image small", upload_to="images/", null=True, blank=True)

    fossil_public_url = models.URLField("URL", max_length=500, blank=True, null=True)
    fossil_collector_name = models.CharField("Collector name", max_length=250, blank=True, null=True)
    fossil_collector_email = models.EmailField("Collector email", max_length=254, blank=True, null=True)
    fossil_collector_phone = models.CharField("Collector phone", max_length=250, blank=True, null=True)

    fossil_entry_created = models.DateTimeField(auto_now_add=True)
    fossil_entry_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('homepage') # once we have a designated page to list all fossils, we will update this method

    def __str__(self):
        return f"{self.fossil_name}"
    
    @property
    def fossil_collector(self):
        name = self.fossil_collector_name or ''
        email = self.fossil_collector_email or ''
        phone = self.fossil_collector_phone or ''
        return f"{name} {email} {phone}"
    
    @property
    def fossil_age_mln(self):
        if self.fossil_age_in_years is not None:
            return f"{float(self.fossil_age_in_years / 1000000):.2f} million years ago"
        return None
    
    @property
    def fossil_collected_days_ago(self):
        try:
            return (timezone.now().date() - self.fossil_date_acquired).days
        except TypeError:
            return None
        

