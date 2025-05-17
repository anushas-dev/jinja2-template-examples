# Python
"""This module demonstrates rendering a template with Jinja2 using sample data."""
from jinja2 import Template

numbers = [1,2,3,4,5,6,7,8]
TEMPLATE = """Hello {{name | title}},
Hope you are doing well!
Please confirm the following order:
{{quantity | unique | max}} {{type | replace ("books","NOTEBOOKS") | lower}}, {% for key, value in collection.items() %} 
{{ value }} {{key}} {% endfor %}
We'll initiate the delivery after your confirmation. 

{{note | upper}}

Yours sincerely,
{{dept}} """

data = {
    "name": "john doe",
    "note": "Offer: Until end of this month, we are offering 50% off on all our products",
    "type": "books",
    "dept": "Girija BookStore",
    "quantity": [2,4,5,2,2,8,9,9,10,2,2,6],
    "collection" : {"Pencils":"2","Pens":"3", "Stencils":"5", "Erasers":"5" }
}

j2_template = Template(TEMPLATE)

print(j2_template.render(data))
