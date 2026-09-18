from django import forms
from django.db import models
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
#
from nanodjango import Django
#
from model_static_data import COUNTRY_ISO_CODES, HIGHEST_POINT_ON_LAND, LOWEST_POINT_ON_LAND


app = Django(
    STYLE_THEME = "bootstrap",
    STYLE_IS_APP = True,
    EXTRA_APPS = ["django.contrib.humanize"])


@app.admin
class Country(models.Model):
    """
    Represents a Country.
    """

    COUNTRIES = COUNTRY_ISO_CODES

    country_iso_code = models.CharField(max_length=3, choices = COUNTRIES)
    population = models.IntegerField()
    area_sq_km = models.IntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.country_iso_code


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ["name", "population", "area_sq_km"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "population": forms.NumberInput(attrs={
                "class": "form-control",
            }),
            "area_sq_km": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "1",
                "min": "0",
            }),
        }


class CityManager(models.Manager):
    def get_queryset(self):
        # Annotate the queryset with the country_iso_code from the related Country model
        return super().get_queryset().annotate(
            country_iso_code=F('country__country_iso_code')
        )


@app.admin
class City(models.Model):
    '''
    Represents a City.
    '''
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255)
    mayor_name = models.CharField(max_length=255)
    date_of_last_mayoral_election = models.DateField(null=True, blank=True)
    population = models.IntegerField()
    area_sq_km = models.IntegerField(null=True, blank=True)
    elevation_metres = models.IntegerField(null=True, blank=True)

    objects = CityManager()

    def clean(self):

        if (self.elevation_metres is not None):
            if (self.elevation_metres > HIGHEST_POINT_ON_LAND):
                raise ValidationError("Elevation is higher than any point on earth.")

        if (self.elevation_metres is not None):
            if (self.elevation_metres < LOWEST_POINT_ON_LAND):
                raise ValidationError("Elevation is lower than any point on earth.")

        today = date.today()

        if (self.date_of_last_mayoral_election is not None):
            if (self.date_of_last_mayoral_election > today):
                raise ValidationError("Date of Last Mayoral Election is after today. If provided, it must be today, or earlier")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city_name} ({self.country.country_iso_code})"


class CityForm(forms.ModelForm):
    mayor_name = forms.CharField(
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Enter the name of the current mayor.",
        error_messages={
            "min_length": "The mayor's name must be at least 3 characters long.",
            "max_length": "The mayor's name cannot be longer than 30 characters.",
            "required": "Please enter the mayor's name.",
        },
    )

    class Meta:
        model = City
        fields = "__all__"
        widgets = {
            "country": forms.Select(attrs={"class": "form-select"}),
            "city_name": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_last_mayoral_election": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "population": forms.NumberInput(attrs={"class": "form-control"}),
            "area_sq_km": forms.NumberInput(attrs={"class": "form-control"}),
            "elevation_metres": forms.NumberInput(attrs={"class": "form-control"}),
            "some_number": forms.NumberInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "country": "Select the country this city belongs to.",
            "city_name": "Enter the name of the city.",
            "date_of_last_mayoral_election": "Date of the last mayoral election (if known).",
            "population": "Enter the population of the city.",
            "area_sq_km": "Enter the land area in square kilometres.",
            "elevation_metres": "Enter the elevation in metres above sea level.",
            "some_number": "Optional: provide a number for testing purposes.",
        }

@app.route("/countries/")
def country_list(request):

    countries = Country.objects.all().order_by("name")

    return app.render(
        request,
        "country_list.html",
        {
            "countries": countries,
        },
    )

@app.route("/countries/new/")
def country_new(request):
    if request.method == "POST":
        form = CountryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/countries/")
    else:
        form = CountryForm()

    return app.render(
        request,
        "country_new.html",
        {"form": form},
    )


@app.route("/countries/<int:country_id>/edit/")
def country_edit(request, country_id):
    country = get_object_or_404(Country, pk=country_id)

    if request.method == "POST":
        form = CountryForm(request.POST, instance=country)

        if form.is_valid():
            form.save()
            return redirect("/countries/")
    else:
        form = CountryForm(instance=country)

    return app.render(
        request,
        "country_edit.html",
        {
            "form": form,
            "country": country,
        },
    )


@app.route("/countries/<int:country_id>/delete/")
def country_delete(request, country_id):
    country = get_object_or_404(Country, pk=country_id)

    if request.method == "POST":
        country.delete()
        return redirect("/countries/")

    return app.render(
        request,
        "country_delete.html",
        {
            "country": country,
        },
    )


@app.route("/cities/")
def city_list(request):

    cities = City.objects.all().order_by("city_name")
    print("city_list called:", cities.count())

    return app.render(
        request,
        "city_list.html",
        {
            "cities": cities,
        },
    )

def count(request):
    return f"<p>Geography Home Page</p>"






@app.api.get("/country/add")
def add_country(request):
    # Django Ninja API support built in
    Country.objects.create()
    return {"count": Country.objects.count()}




