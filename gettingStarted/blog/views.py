from django.shortcuts import render


def home(request):
    return render(request, "blog/home.html") #context sender post-informasjonen inn til html filen
"""Enkel måte å sende html kode over til klienten, finner home.html i templates/blog og sender den"""


def about(request):
    return render(request, "blog/about.html", {"Title": "About"})
