# Python
"""This module demonstrates rendering a template with Jinja2 using sample data."""
from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("email.txt")

message = template.render(
    {
        "user": "Milo",
        "program": "Little Lamps Program",
        "date": "26-08-2022",
        "time": "10:00 AM",
        "manager": "Pakhi",
        "team": "Creative Division",
    }
)

print(message)
