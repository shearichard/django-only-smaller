from django import forms
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect
from nanodjango import Django

app = Django(
    STYLE_THEME = "bootstrap",
    STYLE_IS_APP = True
    )

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


@app.route("/countries/")
def country_list(request):
    countries = Country.objects.all().order_by("name")

    rows = "".join(
        f"""
        <tr>
            <td>{country.name}</td>
            <td>{country.population:,}</td>
            <td>{country.area_sq_km:,}</td>
        </tr>
        """
        for country in countries
    )

    if not rows:
        rows = '<tr><td colspan="3">No countries have been added yet.</td></tr>'

    return HttpResponse(
        f"""
        <!doctype html>
        <html>
        <head>
            <title>Countries</title>
        </head>
        <body>
            <h1>Countries</h1>

            <p>
                <a href="/countries/new/">Add a country</a>
            </p>

            <table border="1" cellpadding="6">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Population</th>
                        <th>Area (km²)</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </body>
        </html>
        """
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




