# !!! NO LONGER MAINTAINED OR AVAILABLE ON PYPI !!!

# Flask-BootstrapForms

Generate Bootstrap forms within flask routes

Generates:
- Form tags
- Input field
- Switches
- Radios
- Selects
- Buttons
- Hidden inputs

The main purpose of this extension is to provide a reusable way to work with Bootstrap Forms.
Holding all forms in a form file like forms.py in a global folder, to then import them into a route that needs access to the blank form.

You can then use the upval method to update the values in the route or in the template itself.

The upval method becomes very powerful inside query loops; saving a lot of time writing html inside jinja loops.


## Install
```
pip install Flask-BootstrapForms
```

## App Example:

```python
from flask import Flask, render_template, redirect, url_for
from flask_bootstrapforms import FBFContext, Form, Elements


def create_app():
    app = Flask(__name__)

    """
    Pass the app to FlaskBootstrapForms to gain access to the upval() method within templates """
    FBFContext(app)

    """
    The Form class constructs a dictionary that will accept any future Elements
    Adding form_tags=True will place <form> in the dictionary as __start__ and </form> as __end__
    -> See the template example to see this in action """
    client_form = Form(form_tags=True, name="client_form", method="POST", autocomplete=False)

    """
    Form() without form_tags=True defined it won't generate the <form> tags """
    address_form = Form()

    """
    When adding to a form, the first value passed in will be the name of the input field.
    This value is the name used to store the Element in. It is also used to set the name of the input
    field. The next value Element is used to build what field you would like to show """
    client_form.add("first_name", Elements.input(label="First Name"))

    """
    If you add name="" to the Element, it will not use the first value as the input field name, this is
    useful if you have requirements to have a different field name at POST """
    client_form.add("last_name", Elements.input(name="client_last_name", label="Last Name"))

    """
    You can use wrap_class and wrap_inner_class to generate div tags around the input field.
    This allows you to have a little more control over the input Element
    <div class="{wrap_class}"> <div class="{wrap_inner_class}"> {label} {input} </div> </div> """
    address_form.add("address_line_1", Elements.input(label="Address Line 1", wrap_class="p-4", wrap_inner_class="bg-danger p-1"))

    """
    Appending and prepending is also available. In this example I've appended a label to the end of the input
    and prepended a button to the start. Notice that prepending the button takes a button Element."""
    address_form.add("address_line_2",
        Elements.input(
            append_label="Hello",
            wrap_class="p-2",
            prepend_button=Elements.button(label="Clicky Click", button_class="btn-primary"), ))

    """
    There is also access to some standard input field settings like disable and required """
    address_form.add("town", Elements.input(label="Town", disabled=True, required=True, readonly=True))

    """
    This is an example of a switch Element """
    address_form.add("current_address", Elements.switch(label="This is clients current address", wrap_class="py-2"))

    """
    When creating a radio button the first value passed into .add( is the reference to the element
    but it is also used to set the value of the selected radio. You can override this by specifying a value of course
    The first value passed in to .radio( is the grouped by name. Setting this to the same as another
    radio will allow for the radio to switch between the group 
    !! Be careful with radios and joining forms, as the group name stays the same, it's best not to use
    radios in joined forms"""
    address_form.add("turn_direction_left", Elements.radio("turn_direction", label="Turn Left", wrap_class="py-2"))
    address_form.add("turn_direction_right", Elements.radio("turn_direction", label="Turn right", value="right", wrap_class="py-2"))

    """
    Here's an example of a select Element, you can either pass a list or dict of values.
    A list of values with generate the select with the dropdown value the same as the input value 
    Like this: <option value="{value}" selected>{value}</option>"""
    house_types = ["big", "small", "boat"]
    address_form.add(
        "house_type", Elements.select(label="House Type", wrap_class="py-2", values_list=house_types))

    """
    When passing a dict value, it uses the Key in the dropdown display.
    Like this: <option value="{value}" >{key}</option>
    You can also set a preselected value using selected="value" """
    house_types_dict = {"Big House": "big", "Small House": "small", "Boat House": "boat"}
    address_form.add(
        "house_type_dict", Elements.select(
            label="House Type Dict", wrap_class="py-2", values_dict=house_types_dict, selected="small"))


    """
    Here's an example of buttons you can generate, one <button> and the other <a>
    button action is how the button will behave in a form, submit / reset / button
    to create a <a> button you need to set the element type"""
    client_form.add(
        "submit", Elements.button(label="Submit", button_class="btn-primary w-100", button_action="submit", wrap_class="p-1"))
    client_form.add(
        "button_link", Elements.button(
            label="Go Somewhere", button_class="btn-primary w-100", element_type="a", href="https://google.com", target="_new", wrap_class="p-1"))

    """
    This is an example of a hidden Element """
    client_id = 10
    address_form.add("client_id", Elements.hidden(value=f"{client_id}"))
    address_form.add("hidden_client_id", Elements.hidden(name="client_id", value=f"{client_id}"))

    """
    Inserting html is also possible, if you do not specify a name after .add(
    it will automatically specify a name based on the current length of the dict
    __20__ for example.
    This use case for this is allowing you to loop over a form in jinja
    Building the form and inserting html Elements between, these will get looped out at the correct time"""
    client_form.add(Elements.html('<div class="card">'))
    client_form.add(Elements.html('<div class="card-body">'))
    client_form.add(Elements.html('<p class="m-0 p-4 text-center">Inside card</p>'))
    client_form.add(Elements.html('</div>'))
    client_form.add(Elements.html('</div>'))

    """
    You can also specify a name for the html Element, and reference it that way."""
    client_form.add("header", Elements.html('<h4 class="m-0 p-4 text-center">header element</h4>'))

    """
    Joining forms is also possible, the following takes all the fields from address_form and
    makes them available to the client_form """
    client_form.join(address_form.all())

    @app.get("/")
    def home():
        render = "index.html"
        extend = "base.html"

        """
        Values can be updated using the upval method"""
        client_form.upval("first_name", "Cheese")
        client_form.upval("last_name", "Cake")

        # The following values have been passed in from the address_form
        client_form.upval("current_address", True)
        client_form.upval("house_type", "boat")

        # Can also use strings to mark true yes / no or true / false or checked / unchecked
        client_form.upval("turn_direction_left", "yes")

        # here we will set some values to update form values in the template
        new_first_name = "Chicken"
        new_last_name = "Nuggets"

        # here we will set a dummy query and loop over it to update a form in the template
        dummy_query = {
            1: {
                "first_name": "Pepperoni",
                "last_name": "Pizza",
            },
            2: {
                "first_name": "Cheese",
                "last_name": "Pizza",
            }

        }
        
        """
        Now that we are in a flask route and we know that client_form includes form tags
        we can insert the action argument to the __start__ of the form by doing
        client_form=client_form.all(action=f"url_for('route')"),
        """
        return render_template(
            render,
            extend=extend,
            client_form=client_form.all(action=url_for("route_here")),
            address_form=address_form.all(),
            new_first_name=new_first_name,
            new_last_name=new_last_name,
            dummy_query=dummy_query,
        )

    @app.post("/")
    def home_post():
        return redirect(url_for("home", post="posted"))

    return app


```

## Template Example:
```jinja2
{% extends extend %}

{% block _main %}

    <h2>client_form</h2>

    <div class="row py-4">
        <h4>Output one by one</h4>
        <hr>
        {{ client_form.header }}
        {{ client_form.__start__ }}{# Add <form> tags #}
        {{ client_form.first_name }}
        {{ client_form.last_name }}
        {{ client_form.__end__ }}{# Add <form> tags #}
    </div>

    <div class="row py-4">
        <h4>Accessing the upval method in the template</h4>
        <hr>
        {{ client_form.__start__ }}{# Add <form> tags #}
        {{ upval(client_form.first_name, new_first_name) }}
        {{ upval(client_form.last_name, new_last_name) }}
        {{ client_form.__end__ }}{# Add <form> tags #}
    </div>

    <div class="row py-4">
        <h4>looping over upval method with dummy query</h4>
        <hr>

        {% for key, value in dummy_query.items() %}
            <div class="card m-1">
                <div class="card-body">
                    {{ client_form.__start__ }}{# Add <form> tags #}
                    {{ upval(client_form.first_name, value.first_name) }}
                    {{ upval(client_form.last_name, value.last_name) }}
                    {{ client_form.__end__ }}{# Add <form> tags #}
                </div>
            </div>
        {% endfor %}

    </div>


    <div class="row py-4">
        <h4>Loop over other client_form</h4>
        <hr>
        {% for key, value in client_form.items() %}
            {{ value }}
        {% endfor %}
    </div>

    <h2>address_form</h2>

    <div class="row py-4">
        <h4>Loop over other address_form</h4>
        <hr>
        {% for key, value in address_form.items() %}
            {{ value }}
        {% endfor %}
    </div>

{% endblock %}
```
