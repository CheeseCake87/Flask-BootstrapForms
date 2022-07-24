from flask import Flask, render_template, redirect, url_for
from app._flask_bootstrapforms.src.flask_bootstrapforms import FlaskBootstrapForms, Form, Elements


def create_app():
    app = Flask(__name__)

    """
    Pass the app to FlaskBootstrapForms to gain access to the upval() method within templates """
    FlaskBootstrapForms(app)

    """
    Form() without form_tags=True defined it won't generate the <form> tags """
    form_example_one = Form()

    """
    The Form class constructs a dictionary that will accept any future Elements
    Adding form_tags=True will place <form> in the dictionary as __start__ and </form> as __end__
    -> See the template example to see this in action """
    client_form = Form(form_tags=True, name="client_form", method="POST", action="/url")

    """
    You can also turn off form autocomplete """
    address_form = Form(form_tags=True, name="client_form", method="POST", action="/url", autocomplete=False)

    """
    When adding to a form, the first value passed in will be the name of the input field.
    This value is the name used to store the Element in. It is also used to set the name of the input
    field. The next value Element is used to build what field you would like to show """
    client_form.add("first_name", Elements.input(label="First Name"))

    """
    If you add name="" to the Element, it will not use the first value as the input field name, this is
    useful if you have requirements to have a different field name at POST """
    client_form.add("last_name", Elements.input(name="client_last_name", label="Last Name"))


    address_form.add("address_line_1", Elements.input(label="Address Line 1", disabled=True, wrap_class="p-4", wrap_inner_class="bg-danger p-1"))
    address_form.add(
        "town",
        Elements.input(label="Town"))
    address_form.add(
        "staying_here_now",
        Elements.switch(label="Staying here now", wrap_class="py-2"))

    additional.add(
        "append_prepend",
        Elements.input(append_label="Hello", wrap_class="p-2", prepend_button=Elements.button(label="Clicky Click", button_class="btn-primary"), ))

    additional.add("prepend_append",
                   Elements.input(prepend_label="Hello", wrap_class="p-2", append_button=Elements.button(label="Clicky Click", button_class="btn-primary"), ))
    additional2.add("submit", Elements.button(label="Submit", button_class="btn-primary w-100", button_action="submit"))
    additional3.add("submit", Elements.button(label="Addition Submit", button_class="btn-primary w-100", button_action="submit"))

    client_form.add(Elements.html('</div>'))

    # Can join two forms into one, as long as the field names don't match, joining also removes the form tags of the form passed in.
    client_form.join(address_form.all())

    @app.get("/")
    def home():
        render = "index.html"
        extend = "base.html"

        # Can update the values of elements
        client_form.update_value("first_name", "Cheese")
        client_form.update_value("last_name", "Cake")
        client_form.update_value("staying_here_now", True)
        client_form.update_value("select_me", "hello")

        client_form.update_value("gender", "Female")

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
