import json
import os
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load user data
with open(os.path.join(BASE_DIR, "templates/data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# Jinja2 setup
env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")), autoescape=True)
template = env.get_template("template.j2")

# Render with data
rendered_html = template.render(data)

# Save rendered email for preview
output_file = os.path.join(BASE_DIR, "rendered_email.html")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(rendered_html)

print(f"✅ Email template rendered! Open {output_file} in a browser to preview.")
