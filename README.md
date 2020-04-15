<div align="center">
    <img src="/website/static/website/images/strikkit_med_tekst.png" align="center" height="150">
</div>

## Intro

Strikkit er platformen som forener Norges strikkere. Her kan du dele dine siste strikkeprosjekter, finne mestrende utfordringer, eller oppdage kurs og andre eventer å delta på.

[Wiki-link](https://gitlab.stud.idi.ntnu.no/tdt4140-2020/14/-/wikis/home)

## 🛠 Forhåndskrav

Følgende trengs for å kunne kjøre og utvikle Strikkit:

- **Python 3.7.0** eller nyere
    - Sjekk versjon:`python --version`
    - Hvis mangler: [Installasjonsguide](https://www.python.org/downloads/)
- **Pip 18.1** eller nyere
    - Sjekk versjon: `pip --version`
    - Hvis mangler: [Installasjonsguide](https://pypi.org/project/pip/)
- **Crispy Forms 1.9** eller nyere
    - Sjekk versjon: `pip list`
    - Hvis mangler: [Installasjonsguide](https://django-crispy-forms.readthedocs.io/en/latest/install.html) 
- **Django 3.0.3** eller nyere
    - Sjekk versjon:
        - Åpne en python console i terminalen med: `python`
        - Importer Django: `import django`
        - Sjekk version: `django.VERSION`
    - Hvis mangler: [Installasjonsguide](https://www.djangoproject.com/download/) 
- **Git 2.20** eller nyere
    - Sjekk versjon: `git --version`
    - Hvis mangler: [Installasjonsguide](https://git-scm.com/downloads) 


## 🚀 Kom i gang

#### Hent prosjekt
- Naviger til ønsket plassering lokalt.
- `git clone https://gitlab.stud.idi.ntnu.no/tdt4140-2020/14.git`
#### Sett opp database
- `python manage.py makemigrations`
- `python manage.py migrate`
#### Lag en adminbruker
- `python manage.py createsuperuser`
#### Kjør Strikkit server lokalt
- `python manage.py runserver`
- Strikkit vil kjøre lokalt på: http://127.0.0.1:8000/
- Åpne administrasjonssiden på: http://127.0.0.1:8000/admin
- Stopp serveren med: `ctrl + c`
#### Brukerguide
- Brukerguide for Strikkit finnes [her](https://gitlab.stud.idi.ntnu.no/tdt4140-2020/14/-/wikis/Brukermanual).


## 🤝 Bidra

Oversikt over sprinter, brukerhsitorier, og krav finnes på vårt [Taskboard](https://docs.google.com/spreadsheets/d/15qQ-gtJjxQj-VVuyxZlJJvFn6olqX0QQGfVPgQUNHMY/edit?usp=sharing). Her blir sprinter planlagt, mål satt opp, og brukerhistorer delt opp i mindre tasks. Vi bruker taskboardet aktivt for å holde oversikt over oppgaver som er planlagt, under arbeid eller utført.

Prosedyre for ???delegering??? av task.
- Flytt task til "blir behandlet" kolonnen.
- Pull nyeste versjon av prosjektet.
- Opprett branch med beskrivende navn for tasken.
- Skriv kode.
- Push når ferdig testet.
- Merge etter godkjenning.
- Flytt task til "ferdig" kolonnen.


## 🐞 Rapportering av bugs

- Ved oppdagelse av bugs, rapporter [her](mailto:eivind.dovland@gmail.com).
- Legg gjerne med skjermdump av feilmelding og beskrivelse av brukssituasjon.

## 🗃 Dokumentasjon

- [GitLab dokumentajson]()
- [Python](https://docs.python.org/3/)
- [Django](https://docs.djangoproject.com/en/3.0/)
- [Pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/doc)
- [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/#)


## 👥 Community?/Kom i kontakt?

- Diskusjon på [Slack](https://join.slack.com/t/tdt4140progra-qcl9717/shared_invite/zt-dd8adjty-c8auLq9xqrPlg4GmfkdHkg)
- Kontakt på [e-post](mailto:eivind.dovland@gmail.com)
- Ressursside på [Google Drive](https://drive.google.com/drive/folders/1t935WvVLRR06sRqwpEmIcmaG9hHxzESI?usp=sharing)


## 📝 Lisens

[MIT](https://gitlab.stud.idi.ntnu.no/tdt4140-2020/14/-/blob/master/LICENSE) © tdt4140-2020/14