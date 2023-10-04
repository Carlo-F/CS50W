## LET'S SCOUT! | CS50W CAPSTONE PROJECT
**Designing and implementing a web application of your own with Python and JavaScript.**

### Introduction
**Scout leaders waste lots of time creating new and engaging educational activities for their troops.**

However, creating new activities from scratch every time is not easy, especially when they must be in keeping with the educational goals that we want to achieve. Leaders often ask other leaders for help or search on the internet in the hopes of finding activities already prepared by others and that they can re-use with their troop. And the leaders have to go through this every time, for every activity and this, as well as taking up time, can also be very frustrating.

What if there were a single web portal for publishing all the activities of the leaders (with a standardised format that describes the activity and how to carry it out)? This would aid the leaders in the repetitive planning/researching/creating process, giving them access to all the information they need, when they need it.

The **LET'S SCOUT!** project stems from this very real need. **LET'S SCOUT!** is, therefore, a web portal where detailed scout activities can be created, shared and searched for.

The scout method in a non-formal education method with the aim of developing “good citizenship among young people by forming their character, training them in habits of observation, obedience and self-reliance” (Lord Baden-Powell).

Each activity sheet on **LET'S SCOUT!** will be standardised and will contain all the information necessary for the leader to reproduce the activity with their troop, including the recommended age range of the participants, the required materials, the characteristics and the educational objectives that the activity aims to achieve.

The **LET'S SCOUT!** project was inspired by the need of the Italian Scout Association to have a single, standardised database of activity sheets, which does not currently exist in any form. At the moment, the leaders do not have a dedicated place to search for inspiration for their activities and have improvise by searching online or asking each other for help each time. The **LET'S SCOUT!** portal, once the CS50W course has finished, will be implemented, in agreement with the Italian scout association, for use in all Italian groups.

### Distinctiveness and Complexity

#### Come questo progetto si distingue dagli altri del corso: distinctiveness
Questo progetto si distingue dagli altri sviluppati durante il corso in quanto non è un e-commerce, ne un social network, ne nient'altro di simile gia' fatto. E' piuttosto una piattaforma di tipo _knowledge-sharing_, in cui gli utenti can create, share, organize, access and store le specifiche informazioni di cui hanno bisogno, sia loro che altri utenti come loro. **LET'S SCOUT!** e' pertanto una piattaforma web di creazione, condivisione e ricerca di una specifica tipologia di informazione, per rispondere ad una specifica esigenza informativa di conoscenza degli educatori scout.

#### In cosa questo progetto e' piu complesso degli altri del corso: complexity
Per aumentare la complessita' di questo progetto rispetto agli altri progetti portati a termine durante il corso, ho ripreso alcune funzionalita' gia' presenti negli altri progetti, e ho proceduto quindi ad arricchirle, espanderle e a renderle piu' complesse. Ad esempio, c'e' maggiore complessita' nella funzionalita' di **ricerca delle informazioni**. 

Durante il corso le informazioni potevano essere ricercate sostanzialmente in due modi: **consultando delle pagine-elenco** come "latest", "following", "categories" (riferimento a progetti Commerce e Network) oppure con una **ricerca semplificata** con parametro in query string (riferimento a progetto Wiki).

In questo progetto ho voluto implementare queste due funzionalita' di ricerca ma le ho anche rese piu' complesse: ho scelto infatti di implementare una nuova funzionalita' di ricerca testuale che restituisce risultati in tempo reale durante la digitazione dell'utente tramite interrogazione di API creata ad hoc (tramite la searchbar posta in alto in ogni pagina).

La ricerca per pagine-elenco e' anche questa piu' complessa: ho aggiunto una nuova funzionalita' di ricerca, **la ricerca per tags**. I tag sono essenzialmente delle caratteristiche predefinite (quindi gia' fissate in origine) che l'utente puo' o meno attribuire alle attivita' in fase di creazione. La ricerca per etichette aggiunge al progetto la pagina **Tags** con elenco di tutti i tag, e la pagina del singolo **Tag** dove sono elencate tutte le attivita' che possiedono quella specifica caratteristica.

Due ulteriori esempi della maggior complessita' riguardano la **complessita' di una scheda attivita'** e la funzionalita' di **attivita' suggerite** (_similar activities_).

In questo progetto, infatti, il modello dell'entita' per la scheda attivita' (_Activity_) richiede piu' informazioni rispetto alla creazione di un post nel progetto Network e anche piu' informazioni di una scheda prodotto del progetto Commerce. Questo ha implicato piu' campi da gestire sia nel modello, sia nel database, sia nel form nel frontend dell'applicativo aumentando ulteriormente la complessita' generale. Inoltre, nella pagina della singola attivita', in basso, possono comparire delle **attivita' suggerite**. Sono attivita' che condividono delle caratteristiche con l'attivita' attualmente visualizzata e che potrebbero quindi interessare all'utente.

### Struttura del codice e contenuto dei file
- `capstone/` capstone project's folder. 
    - `asgi.py`
    - `settings.py` added some configuration informations like static_url, login_url, etc.
    - `urls.py` the urls of the web application: administration url and all the urls contained in `scout/urls.py`
    - `wsgi.py`
- `scout/`
    - `migrations/`
    - `static/`
        - `scout/`
            - `images/` images used in the `README.md` file
            - `custom.js` script to handle front end events (like button, searchbar, etc.)
            - `styles.css` custom CSS style
    - `templates/`
        - `scout/`
            - `activity-card-small.html` compact card layout for a single activity
            - `activity-card.html` standard card layout for a single activity
            - `activity.html` single activity page
            - `category.html` category page (scout age range)
            - `edit_activity.html` edit activity page
            - `favourites.html` favourites page
            - `index.html` homepage
            - `latest.html` latest page
            - `layout.html` general app layout
            - `login.html` user login page
            - `my_activities.html` user's activities page
            - `navbar.html` navbar template
            - `new_activity.html` new activity creation page
            - `popular.html` popular page
            - `register.html` user register page
            - `searchbar.html` searchbar template
            - `sidebar.html` sidebar template
            - `sub_header.html` tags menu template (position: sub header)
            - `tag.html` single tag page
            - `tags.html` all tags page
    - `admin.py` models admin registration file
    - `apps.py` application configuration file
    - `models.py` models classes definition (User, EducationalGoal, Activity, Like)
    - `tests.py` 
    - `urls.py` default URL configuration file
    - `utils.py` application's utility (containing a function that formats activities before sending them to the view)
    - `views.py` default views configuration file
- `db.sqlite3`
- `manage.py`
- `README.md`

### Installazione
L'applicazione runs sulla porta di default 8000. Non e' necessario installare alcun pacchetto di Python aggiuntivo.

1. Make and apply migrations:
    `python manage.py makemigrations` seguito da 
    `python manage.py migrate`
2. Create the superuser to log in as an admin:
    `python manage.py createsuperuser`
3. Run the server:
    `python manage.py runserver`

### Informazioni addizionali

#### Funzionalità dell'applicazione web
Elenco delle principali funzionalita' del progetto:

- registrazione e login utente
- creazione e modifica di schede attivita' scout
- ricerca di schede attivita' con differenti possibilita':
    - ricerca per age range
    - ricerca per titolo (ricerca testuale in tempo reale)
    - ricerca per tag
    - ricerca per popolarita'
    - ricerca dal piu' recente al meno recente (latest)
- possibilita' di salvare le schede attivita' in una sezione "favoriti"
- funzionalita' di suggerimento attivita' (similar activities)

#### Tecnologie utilizzate

- Python
- Django
- JavaScript
- HTML
- CSS
- Bootstrap 5.3

#### Sviluppi futuri

- limitare la registrazione degli utenti ai soli educatori scout
- poter scaricare in PDF la scheda di un'attivita'
- aggiungere ulteriori tag se necessario

#### Info e Contatti
Progetto realizzato da **Carlo Feniello** nell'anno 2023 per il corso **CS50's Web Programming with Python and JavaScript** rilasciato da **Harward University**.

- [pagina ufficiale del corso](https://cs50.harvard.edu/web/2020/ "CS50's Web Programming with Python and JavaScript")
- [Carlo Feniello, sito personale](https://carlof.it "carlof.it")
- [Carlo Feniello, profilo GitHub](https://github.com/Carlo-F "Carlo-F")
- [Carlo Feniello, Email](mailto:info@carlof.it "info@carlof.it")
