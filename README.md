# LET'S SCOUT! | CS50W CAPSTONE PROJECT
**Designing and implementing a web application of your own with Python and JavaScript.**

## Introduction
**Scout leaders waste lots of time creating new and engaging educational activities for their troops.**

However, creating new activities from scratch every time is not easy, especially when they must be in keeping with the educational goals that we want to achieve. Leaders often ask other leaders for help or search on the internet in the hopes of finding activities already prepared by others and that they can re-use with their troop. And the leaders have to go through this every time, for every activity and this, as well as taking up time, can also be very frustrating.

What if there were a single web portal for publishing all the activities of the leaders (with a standardised format that describes the activity and how to carry it out)? This would aid the leaders in the repetitive planning/researching/creating process, giving them access to all the information they need, when they need it.

The **LET'S SCOUT!** project stems from this very real need. **LET'S SCOUT!** is, therefore, a web portal where detailed scout activities can be created, shared and searched for.

The scout activity method in a non-formal education method with the aim of developing “good citizenship among young people by forming their character, training them in habits of observation, obedience and self-reliance” (Lord Baden-Powell).

Each activity sheet on **LET'S SCOUT!** will be standardised and will contain all the information necessary for the leader to reproduce the activity with their troop, including the recommended age range of the participants, the required materials, the characteristics and the educational objectives that the activity aims to achieve.

The **LET'S SCOUT!** project was inspired by the need of the Italian Scout Association to have a single, standardised database of activity sheets, which does not currently exist in any form. At the moment, the leaders do not have a dedicated place to search for inspiration for their activities and have improvise by searching online or asking each other for help each time. The **LET'S SCOUT!** portal, once the CS50W course has finished, will be implemented, in agreement with the Italian scout association, for use in all Italian groups.

## Distinctiveness and Complexity

### How this project differs from the others in the course: distinctiveness
This project differs from the others developed during the course as it is not an e-commerce, nor a social network, or anything similar to what was done previously. Rather it is a _knowledge-sharing_ platform, where users can create, share, organise, access and store the specific information they need, both for themselves and other users. **LET'S SCOUT!** is therefore a web application platform for creating, sharing and searching for a specific type of information (scout activities), responding to a specific informational need of scout leaders.

### How this project is more complex than the others in the course: complexity
To increase the complexity of this project compared to the other projects completed during the course, I took some of the functionalities already present in other projects, and I enriched them by expanding them and making them more complex. For example, the **information search** functionality is more complex.

During the course the information could essentially be searched for in one of two ways: **Consulting a list page** such as “latest”, “following”, “categories” (with reference to the Commerce and Network projects) or with a **simplified search with query string parameters** (with reference to the Wiki project).

In this project I used these two search functionalities but I made them more complex: infact I chose to implement a text search functionality that gives results in real time as the user types by using a tailor-made interrogation API (through the search bar at the top of every page).

The list page search is also more complex now: I added a new search functionality, **the tags search**. Those tags are essentially predefined characteristics, that the user can choose to attribute to the activity when creating it. The tags search adds the **Tags** page to the project with a list of all tags, and the single **Tag** page where all the activities with that specific characteristic are listed.

Two further examples of increased complexity are the **complexity of an activity sheet** and the **suggested activities functionality** (_similar activities_).

In this project the entity model for the activity sheet (_Activity_) requires more information than for the creation of a post in the Network project and even more information than in a product sheet in the Commerce project. This means more fields to manage in the model, in the database and in the frontend form of the application, further increasing the complexity in general. Furthermore, on the single activity page, at the bottom, a **suggested activities** box may appear. These are activities that have the some characteristics as the activity currently being viewed and that could be of interest to the user.

## Code structure and file contents
- `capstone/` capstone project's folder.
    - `asgi.py`
    - `settings.py` added some configuration information like static_url, login_url, etc.
    - `urls.py` the urls of the web application: administration url and all the urls contained in `scout/urls.py`
    - `wsgi.py`
- `scout/`
    - `static/`
        - `scout/`
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

## Installation
The application runs on the default port 8000. No additional Python package is necessary.

1. Make and run migrations:
    `python manage.py makemigrations scout`
    followed by 
    `python manage.py migrate`
2. (optional) Create the superuser to log in as admin:
    `python manage.py createsuperuser`
3. Run the server:
    `python manage.py runserver`

## Additional information

### Web application functionalities
A list of the main functionalities of this web application:
- user registration and login
- creation and modification of scout activity sheets
- activity sheets search with various possibilities:
    - search by age range
    - search by title (real time text search)
    - search by tag
    - search by popularity
    - search from the most recent to the least recent (latest page)
- possibility to save activity sheets in a “favourites” section
- suggested activities functionality (similar activities)

### Technology used
- Python
- Django
- JavaScript
- HTML
- CSS
- Bootstrap 5.3

### Future developments
- limit user registration to only scout leaders to improve the quality of the content created
- create a functionality: download the activity sheets in PDF by clicking a button
- add further tags if necessary

### Info and Contacts
Project created by **Carlo Feniello** in the year 2023 for the **CS50's Web Programming with Python and JavaScript** course of **Harvard University**.

- [official page of the course](https://cs50.harvard.edu/web/2020/ "CS50's Web Programming with Python and JavaScript")
- [Carlo Feniello, personal website](https://carlof.it "carlof.it")
- [Carlo Feniello, GitHub profile](https://github.com/Carlo-F "Carlo-F")
- [Carlo Feniello, Email](mailto:info@carlof.it "info@carlof.it")