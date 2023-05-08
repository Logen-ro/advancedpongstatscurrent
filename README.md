Youtube video link: https://youtu.be/SrnbR5ubN4Q

Intro:
    To create my project, I utilized the distribution code from Finance, since I was familiar with the code and it provided a great initial framework to build my project in. This project is a web based application which uses flask, jinja2, python, html, css, sqlite3, the cs50 library, and werkzeug.security.

Python Files:
    This project uses two python files, app.py and helpers.py. helpers.py allows me to use @login_required and apology, which are all the functions within the file. The second python file is app.py. This file has the following functions: login, register, logout, recordgames, recordshots, shotrecord, winrecord, and percentage. login, register, and logout do exactly what they say. recordgames and recordshots use db.execute to insert new data into the database, based on the logic of the surrounding python code. shotrecord, winrecord, and percentage get the data from the database for the templates to display, and perform the calculations neccesary to find the percentage of wins and shots.

Templates
    This project uses 10 templates. They are apology.html, gamerecords.html, index.html, layout.html, login.html, percentage.html, recordgames.html, recordshots.html, register.html, and shotrecord.html.

Database
    I used a single database file for this project, named userstats.db. This datbase contains three tables, one named shots, one named users, and one named winrecord. shots stores data related to shooting, users for users, and winrecord for games.

Running Project
    To run the project, extract the advancedpongstats.zip file and open the folder in vscode. After this is complete, execute "python -m flask run" to initiate a server. You must register and sign in in order to interact with the project. After this is done, you will have access to all the pages and will be able to record your stats. In order to record these stats, click the buttons that correspond to the value you want to input (ie miss button to add a miss, win button to add a win, button number 1 to add a make of cup number 1), and they will execute their associated command and automatically refresh the page. I designed this project to have a simple user interface, so it should be very straitforward to use.