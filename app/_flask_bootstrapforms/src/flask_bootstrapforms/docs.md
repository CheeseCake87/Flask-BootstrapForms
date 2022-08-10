#### @app.context_processor + method: upval

```text
!! This is used in Jinja2 template !!
Takes the form_field's name and changes the current value to the new value passed in
For example, if you have:
    client_form.add("first_name", Elements.input(label="First Name"))
                       ^ output ref + form value=""
This generates:
    <input name="first_name" value="" />

Doing:
    {{ upval("first_name", "Cheesecake") }}
Will generate:
    <input name="first_name" value="Cheesecake" />
                                        ^ updated

Is also able to work with selects, switches and radios.

For switches and radios: value = "yes" will added checked, value = "no" will removed checked

For selects: value = "ford" will remove selected from all other options and apply it
to the select with the value of ford

:param element:
:param value:
:return:
```


#### @app.context_processor + method: radgro
```text
!! This is used in Jinja2 template !!
This will update a radio tag to be part of a radio tag group.
For example, if you have:
    address_form.add("small_house", Elements.radio("house_type", label="Small House"))
    address_form.add("big_house", Elements.radio("house_type", label="Big House"))
                       ^ output ref + form value=""    ^ form name=""   ^ form Label
This generates:
    <input type="radio" id="small_house" name="house_type" value="small_house"><label for="small_house">Small House</label>
    <input type="radio" id="big_house" name="house_type" value="big_house"><label for="big_house">Big House</label>

Doing:
    {{ radgro("small_house", "using_this_elsewhere") }}
Will generate:
    <input type="radio" id="small_house" name="using_this_elsewhere" ...
                                                ^ updated
:param element:
:param group_name:
:return:
```

#### @app.context_processor + method: upnam
```text
Dose the same thing as upval, but for name
```

