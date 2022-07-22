# Flask-BootstrapForms

Generate Bootstrap forms within flask routes

Generates:
- Input field
- Switches
- Selects
- Buttons
- Hidden inputs

```
pip install Flask-BootstrapForms
```

Small example below:

```python
from flask import Flask, render_template, redirect, url_for
from flask_bootstrapforms import BootstrapForm, Elements


def create_app():
    app = Flask(__name__)

    # placing form_tags=True will generate <form> tags in the dictionary as "__start__": "<form>", "__end__": "</form>"
    client_form = BootstrapForm(form_tags=True, name="client_form")
    address_form = BootstrapForm(form_tags=True)
    additional = BootstrapForm(form_tags=True, method="POST")
    additional2 = BootstrapForm(form_tags=True, name="additional_form_2", method="POST", action="#")

    # BoostrapForm() without form_tags=True defined it won't generate the <form> tags
    additional3 = BootstrapForm()

    client_form.add(
        "first_name",
        Elements.input(
            label="First Name",
        ))

    client_form.add(
        "last_name",
        Elements.input(
            label="Last Name",
            wrap_class="p-4",  # add bootstrap p-4 to a new div around the element
            wrap_inner_class="bg-danger p-1"  # add bootstrap background to a new div inside the wrap class
        ))

    address_form.add(
        "address",
        Elements.input(
            label="Address Line 1",
            disabled=True,  # disable input
        )
    )
    address_form.add(
        "town",
        Elements.input(
            label="Town"
        )
    )
    address_form.add(
        "staying_here_now",
        Elements.switch(
            label="Staying here now",
            wrap_class="py-2"
        )
    )

    additional.add(
        "append_prepend",
        Elements.input(
            append_label="Hello",
            wrap_class="p-2",
            prepend_button=Elements.button(
                label="Clicky Click",
                button_class="btn-primary"
            ),
        )
    )

    additional.add(
        "prepend_append",
        Elements.input(
            prepend_label="Hello",
            wrap_class="p-2",
            append_button=Elements.button(
                label="Clicky Click",
                button_class="btn-primary"
            ),
        )
    )

    additional2.add(
        "submit",
        Elements.button(
            label="Submit",
            button_class="btn-primary w-100",
            button_action="submit"
        )
    )

    additional3.add(
        "submit",
        Elements.button(
            label="Addition Submit",
            button_class="btn-primary w-100",
            button_action="submit"
        )
    )

    select_list = ["hello", "goodbye", "hello2"]

    client_form.add(
        "select_me",
        Elements.select(
            label="Select Me",
            values_list=select_list,
            selected="goodbye"
        )
    )

    # Can join two forms into one, as long as the field names don't match, joining also removes the form tags of the form passed in.
    client_form.join(address_form.all())

    @app.get("/")
    def home():
        render = "index.html"
        extend = "base.html"

        # Can update the values of elements
        client_form.update_value("first_name", "Cheese")
        client_form.update_value("last_name", "Cake")
        client_form.update_value("select_me", "hello2")
        client_form.update_value("staying_here_now", True)

        return render_template(
            render,
            extend=extend,
            client_form=client_form.all(),
            additional=additional.all(),
            additional2=additional2.all(),
            additional3=additional3.all(),
        )

    @app.post("/")
    def home_post():
        return redirect(url_for("home", post="posted"))

    return app


```

Template:
```jinja2
{% extends extend %}

{% block _main %}

    <div class="row py-4">
        <h2>Can output one by one</h2>
        <h5>client_form Form</h5>
        <hr>
        {{ client_form.__start__ }}{# Add <form> tag #}
        {{ client_form.first_name }}
        {{ client_form.last_name }}
        {{ client_form.__end__ }}{# Add </form> tag #}
    </div>


    <div class="row py-4">
        <h2>Loop over other passed in forms</h2>
        <h5>additional Form looped, with append and prepend examples</h5>
        <hr>
        {% for key, value in additional.items() %}
            {{ value }}
        {% endfor %}
    </div>

    <div class="row py-4">
        <h2>Form tags generated</h2>
        <h5>additional2 Form looped</h5>
        <hr>
        {% for key, value in additional2.items() %}
            {{ value }}
        {% endfor %}
    </div>

    <div class="row py-4">
        <h2>Form tags not generated</h2>
        <h5>additional3 Form looped</h5>
        <hr>
        {% for key, value in additional3.items() %}
            {{ value }}
        {% endfor %}
    </div>

    <div class="row py-4">
        <h2>Or loop over joined forms</h2>
        <h5>client_form.joined(address_form) Form looped (form tags removed from address_form due to join)</h5>
        <hr>
        {% for key, value in client_form.items() %}
            {{ value }}
        {% endfor %}
    </div>

{% endblock %}
```