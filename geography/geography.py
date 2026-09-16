from django import forms
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect
from nanodjango import Django

app = Django(
    STYLE_THEME = "bootstrap",
    STYLE_IS_APP = True,
    EXTRA_APPS = ["django.contrib.humanize"])


@app.admin
class Country(models.Model):
    """
    Represents a Country.
    """

    population = models.IntegerField()
    area_sq_km = models.IntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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

def count(request):
    return f"<p>Geography Home Page</p>"

@app.api.get("/country/add")
def add_country(request):
    # Django Ninja API support built in
    Country.objects.create()
    return {"count": Country.objects.count()}




