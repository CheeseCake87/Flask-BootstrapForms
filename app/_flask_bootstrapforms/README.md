# Flask-BootstrapForms

Generate Bootstrap forms within flask routes

Generates:
- Input field
- Switches
- Selects
- Buttons
- Hidden inputs

Small example below:

```python
from flask import Flask, render_template
from app._flask_bootstrapforms.src.flask_bootstrapforms import BootstrapForm, Elements


def create_app():
    app = Flask(__name__)

    client_form = BootstrapForm(form_tags=True)
    address_form = BootstrapForm()
    additional = BootstrapForm(form_tags=True, method="POST")
    additional2 = BootstrapForm(form_tags=True, name="additional_form_2", method="POST", action="#")

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

    # Can join two forms into one, as long as the field names don't match
    client_form.join(address_form.all())

    @app.get("/")
    def home():
        render = "index.html"
        extend = "base.html"

        return render_template(
            render,
            extend=extend,
            client_form=client_form.all(),
            additional=additional.all(),
            additional2=additional2.all(),
        )

    return app

```

Template:
```jinja2
{% extends extend %}

{% block _main %}

    <div class="row py-4">
        <h2>Can output one by one</h2>
        <hr>
        {{ client_form.first_name }}
        {{ client_form.last_name }}
    </div>

    <div class="row py-4">
        <h2>Or loop over values</h2>
        <hr>
        {% for key, value in client_form.items() %}
            {{ value }}
        {% endfor %}
    </div>


    <div class="row py-4">
        <h2>Loop over other passed in forms</h2>
        <hr>
        {% for key, value in additional.items() %}
            {{ value }}
        {% endfor %}
    </div>

    <div class="row py-4">
        <h2>Can generate form tags</h2>
        <hr>
        {% for key, value in additional2.items() %}
            {{ value }}
        {% endfor %}
    </div>

{% endblock %}


```