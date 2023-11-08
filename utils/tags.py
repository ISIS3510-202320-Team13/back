"""
File: tags.py
* @author Juan Lugo Sánchez
* jd.lugo@uniandes.edu.co

Here you can find the groups of the docs route
to group a method into one of this you should change the tag "Users" at main.py -- @app.put("/users", tags=["Users"])
"""

info = [
    {
        "name": "Users",
        "description": "Operations with Users.",
    },
    {
        "name": "Reservations",
        "description": "Operations with Reservations.",
    },
    {
        "name": "Parkings",
        "description": "Operations with Parkings.",
    },
    {
        "name": "Utils",
        "description": "Wildcards and non-persistence related",
    },
]