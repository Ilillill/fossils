from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField
from django_resized import ResizedImageField
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify


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
        return reverse('homepage')

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


class DBFossilGathering(models.Model):
    class Meta:
        ordering = ('-gathering_date', )

    gathering_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gathering_name = models.CharField("Name", max_length=250)
    gathering_date = models.DateField("Date")
    gathering_image = ResizedImageField("Image", upload_to="images/", null=True, blank=True)

    gathering_description = models.TextField("Description", blank=True) # There is no need to specify null=True for CharField and TextField as if left empty in a form, they will have an empty string
    gathering_location = models.CharField("Location", max_length=500, blank=True)
    gathering_location_geological_time = models.CharField("Geological time", max_length=500, blank=True)
    
    gathering_duration = models.DurationField("Duration", null=True, blank=True)
    gathering_pdf = models.FileField("Upload PDF", upload_to='dosuments', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])

    gathering_slug = models.SlugField("Your unique URL", unique=True)

    def save(self, *args, **kwargs):
        now = timezone.now().strftime("%Y%m%d%H%M%S")
        slug = slugify(f"{self.gathering_name}-{self.gathering_owner.id}-{now}")
        self.gathering_slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.gathering_date} | {self.gathering_name}"


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
    fossil_species = models.ForeignKey(DBSpecies, on_delete=models.SET_NULL, verbose_name="Species", related_name='species', limit_choices_to={'species_is_archived': False}, null=True, blank=True)
    fossil_gathered = models.ForeignKey(DBFossilGathering, on_delete=models.SET_NULL, verbose_name="Obtained from fossil collecting event", related_name='gathered', null=True, blank=True) # thanks to using related_name we can get all fossils gathered during this event simply using: fossils = gathering.gathered.all(), there is no need to use select_related: fossils = gathering.gathered.select_related('fossil_gathered').all()
    associated_fossils = models.ManyToManyField('self', verbose_name="Associated fossils", blank=True)

    fossil_status = models.CharField("Status", max_length=100, choices=FossilstatusChoices.choices, default="Collection")

    fossil_name = models.CharField("Fossil name", max_length=250)
    fossil_description_short = models.TextField("Short description", blank=True, null=True)
    fossil_description_detailed = HTMLField("Detailed description", blank=True, null=True)

    fossil_is_favourite = models.BooleanField("Add to favourites", default=False)

    fossil_age_in_years = models.DecimalField("Age in years", max_digits=15, decimal_places=0, blank=True, null=True)
    fossil_value = models.DecimalField("Fossil current value", max_digits=12, decimal_places=2, blank=True, null=True)

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
            return f"{float(self.fossil_age_in_years / 1000000):.2f} mln years"
        return None
    
    @property
    def fossil_collected_days_ago(self):
        try:
            return (timezone.now().date() - self.fossil_date_acquired).days
        except TypeError:
            return None

##############################################################################################
##########    M A N Y    T O    M A N Y    W I T H    T H R O U G H    M O D E L    ##########
##############################################################################################

# Many to many relationship between fossils and events, each fossil can be lent to multiple events, and each event can include multiple fossils
class DBEvent(models.Model):
    class Meta:
        ordering = ('-event_date',)
        verbose_name = "Event"

    event_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_owner')
    fossils = models.ManyToManyField(DBFossil, through='FossilEvent') # FossilEvent isn't defined yet so we have to use '' to indicate lazy reference
    event_name = models.CharField("Event name", max_length=500)
    event_date = models.DateTimeField("Event date")
    event_notes = models.TextField("Notes", blank=True)

    def __str__(self):
        return str(self.event_name)

# Through model. For each fossil lending I can add extra information like date of lending and return or notes.
class FossilEvent(models.Model):
    class Meta:
        ordering = ('-fossil_lending_date',)
        verbose_name = "Lending a fossil"
        verbose_name_plural = "Lending fossils"

    fossil = models.ForeignKey(DBFossil, on_delete=models.CASCADE)
    event = models.ForeignKey(DBEvent, on_delete=models.CASCADE, related_name='fossil_events') # related name, so we can access this from DBEvent in an easy way
    fossil_lending_date = models.DateField("Date")
    fossil_lending_date_returned = models.DateField("Date fossil returned", null=True, blank=True)
    fossil_lending_notes = models.TextField("Notes", blank=True)

    def __str__(self):
        return str(self.fossil_lending_date)

###################################################################
##########    C U S T O M    U S E R    P R O F I L E    ##########
###################################################################

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    user_avatar = ResizedImageField("Avatar", null=True, blank=True, upload_to="images/", force_format='PNG')
    user_additional_email = models.EmailField("Additional email, unrelated to authentication settings", max_length=254, blank=True, null=True)
    user_website = models.URLField("Website", max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse('profile')
    
