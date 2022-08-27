from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("table")

json_data = {
    "data": [{"Id": 1, "Number": 45, "Name": "Milk"},
    {"Id": 2, "Number": 46, "Name": "Cheese"},
    {"Id": 3, "Number": 47, "Name": "Butter"},
    {"Id": 4, "Number": 48, "Name": "Cream"},
    {"Id": 5, "Number": 49, "Name": "Curd"},
    {"Id": 6, "Number": 50, "Name": "Yogurt"}
    
    ]
}

message = template.render(json_data)
# w+ is to create a file if not present
with open("index.html", "w+") as f:
    f.write(message)
