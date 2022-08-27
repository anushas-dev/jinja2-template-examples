from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("sample_index.html")

message = template.render(
    {
        "title": "HASHNODE JINJA DEMO",
        "about": "Using Template Examples",
        "description": "In step wise approach of templating, with scenarios from day to day life",
    }
)

# w+ is to create a file if not present
with open("index.html",'w+') as f:
    f.write(message)