from markupsafe import Markup
import re
import inspect


class FlaskBootstrapForms:
    _app = None

    def __init__(self, app=None):
        """
        init method, fires init_app if app name is passed in. This is usually used when NOT using create_app()
        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        """
        init method used when working with create_app()
        """
        if app is None:
            raise ImportError("No app passed into the FlaskBootstrapForms")
        self._app = app

        @app.context_processor
        def upval():
            def _upval(element, value):
                """
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
                """
                if value is None:
                    return element

                if 'fbf-type="input"' in element:
                    _value_p = r'value="(.*?)"'
                    _value_r = rf'value="{value}"'
                    return Markup(f"{re.sub(_value_p, _value_r, element)}")

                if 'fbf-type="select"' in element:
                    if value in element:
                        _strip = element.replace("selected", "")
                        _value_p = rf'value="{value}" (.*?)>'
                        _value_r = rf'value="{value}" selected>'
                        return Markup(f"{re.sub(_value_p, _value_r, _strip)}")
                    return element

                if 'fbf-type="switch"' in element or 'fbf-type="radio"' in element:
                    _true_markers, _false_markers = ["yes", "true", "checked"], ["no", "false", "unchecked"]
                    if "checked" not in element:
                        if isinstance(value, bool) or value in _true_markers:
                            _check_p = r'fbf-options="->" (.*?)/>'
                            _find = re.search(_check_p, element)
                            _r = rf'fbf-options="->" {_find.group()[17:-2]}checked />'
                            return f"{re.sub(_check_p, _r, element)}"
                    if value in _false_markers:
                        return element.replace(" checked", "")
                    return element

            return dict(upval=_upval)

        @app.context_processor
        def radgro():
            def _radgro(element, group_name):
                """
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
                """

                if group_name is None or element is None:
                    return
                if 'fbf-type="radio"' in element:
                    _name_p, _id_p, _for_p, _value_p = r'name="(.*?)"', r'id="(.*?)"', r'for="(.*?)"', r'value="(.*?)"'
                    _value_f = re.search(_value_p, element)
                    _name_r, _id_r, _for_r = rf'name="{group_name}"', rf'id="{group_name}_{_value_f.group()[7:-1]}"', rf'for="{group_name}_{_value_f.group()[7:-1]}"'
                    _final = re.sub(
                        _name_p, _name_r, re.sub(
                            _id_p, _id_r, re.sub(
                                _for_p, _for_r, element
                            )
                        )
                    )

                    return Markup(f"{_final}")

            return dict(radgro=_radgro)


class Form:

    def __init__(self, form_tags: bool = False, name: str = None, method: str = None, autocomplete: bool = True):
        self.form_tags = form_tags
        self.name = name
        self.method = method
        self.autocomplete = autocomplete
        self._all = {}
        _frame = inspect.currentframe()
        _frame = inspect.getouterframes(_frame)[1]
        self.caller = inspect.getframeinfo(_frame[0]).code_context[0].strip().split(" = ")[0]

    def all(self, action: str = None) -> dict:
        if self._all == {}:
            return {f"{self.caller}": f"{self.caller} form is empty"}
        if self.form_tags:
            _form = ['<form']
            if self.name is not None:
                _form.append(f' name="{self.name}"')
            if self.method is not None:
                _form.append(f' method="{self.method}"')
            if action is not None:
                _form.append(f' action="{action}"')
            if not self.autocomplete:
                _form.append(f' autocomplete="off"')
            _form.append(">")
            _form = {"__start__": Markup("".join(_form))}
            _form.update(self._all)
            _form.update({"__end__": Markup('</form>')})
            return _form
        return self._all

    def add(self, name, element: Markup = None, element_list: list = None) -> None:
        _null_marker = ":null:"

        # very cheating method to allow html to be inserted into forms
        if isinstance(name, Markup):
            _name = f"__{len(self._all) + 1}__"
            _tack = {_name: name}
            self._all.update(_tack)
            return

        if isinstance(name, str):
            if element is not None:
                if _null_marker in element:
                    _element = element.replace(_null_marker, name)
                    _tack = {name.lower().replace(" ", "_"): _element}
                    self._all.update(_tack)
                    return

            if element_list is not None:
                _unpack_list = []
                for index, element in enumerate(element_list):
                    if _null_marker in element:
                        _unpack_list.append(element.replace(_null_marker, f"{name}_{index}"))
                    else:
                        _unpack_list.append(element)
                tack = {name: _unpack_list}
                self._all.update(tack)
                return

            _tack = {name.lower().replace(" ", "_"): element}
            self._all.update(_tack)
            return

    def join(self, join_dict):
        if "__start__" in join_dict:
            del join_dict['__start__']
            del join_dict['__end__']
        self._all.update(join_dict)

    def remove(self, name) -> None:
        self._all.pop(name)

    def upval(self, form_field, value) -> None:
        """
        Takes the form_field's name and changes the current value to the new value passed in
        For example, if you have:
            client_form.add("first_name", Elements.input(label="First Name"))
                               ^ output ref + form value=""
        This generates:
            <input name="first_name" value="" />

        Doing:
            upval("first_name", "Cheesecake")
        Will generate:
            <input name="first_name" value="Cheesecake" />
                                                ^ updated

        Is also able to work with selects, switches and radios.

        For switches and radios: value = "yes" will added checked, value = "no" will removed checked

        For selects: value = "ford" will remove selected from all other options and apply it
        to the select with the value of ford

        :param form_field:
        :param value:
        :return:
        """
        if form_field in self._all:
            _escape_markup = self._all[form_field].unescape()
            self._all[form_field] = None

            if 'fbf-type="input"' in _escape_markup:
                _value_p = r'value="(.*?)"'
                _value_r = rf'value="{value}"'
                self._all[form_field] = Markup(f"{re.sub(_value_p, _value_r, _escape_markup)}")
                return

            if 'fbf-type="select"' in _escape_markup:
                _strip = _escape_markup.replace("selected", "")
                _value_p = rf'value="{value}" (.*?)>'
                _value_r = rf'value="{value}" selected>'
                self._all[form_field] = Markup(f"{re.sub(_value_p, _value_r, _strip)}")
                return

            if 'fbf-type="switch"' in _escape_markup or 'fbf-type="radio"' in _escape_markup:
                _true_markers, _false_markers = ["yes", "true", "checked"], ["no", "false", "unchecked"]
                if "checked" not in _escape_markup:
                    if isinstance(value, bool) or value in _true_markers:
                        _check_p = r'fbf-options="->" (.*?)/>'
                        _find = re.search(_check_p, _escape_markup)
                        if _find is None:
                            return
                        _r = rf'fbf-options="->" {_find.group()[17:-2]}checked />'
                        self._all[form_field] = Markup(f"{re.sub(_check_p, _r, _escape_markup)}")
                        return

                if value in _false_markers:
                    self._all[form_field] = Markup(form_field.replace(" checked", ""))
                    return

                self._all[form_field] = Markup(form_field)
                return
        return

    def radgro(self, form_field, group_name) -> None:
        """
        This will update a radio tag to be part of a radio tag group.
        For example, if you have:
            address_form.add("small_house", Elements.radio("house_type", label="Small House"))
            address_form.add("big_house", Elements.radio("house_type", label="Big House"))
                               ^ output ref + form value=""    ^ form name=""   ^ form Label
        This generates:
            <input type="radio" id="small_house" name="house_type" value="small_house"><label for="small_house">Small House</label>
            <input type="radio" id="big_house" name="house_type" value="big_house"><label for="big_house">Big House</label>

        Doing:
            upval("small_house", "using_this_elsewhere")
        Will generate:
            <input type="radio" id="small_house" name="using_this_elsewhere" ...
                                                        ^ updated
        :param form_field:
        :param group_name:
        :return:
        """

        if group_name is None:
            return
        if 'fbf-type="radio"' in form_field:
            _name_p, _id_p, _for_p, _value_p = r'name="(.*?)"', r'id="(.*?)"', r'for="(.*?)"', r'value="(.*?)"'
            _value_f = re.search(_value_p, form_field)
            _name_r, _id_r, _for_r = rf'name="{group_name}"', rf'id="{group_name}_{_value_f.group()[7:-1]}"', rf'for="{group_name}_{_value_f.group()[7:-1]}"'
            _final = re.sub(
                _name_p, _name_r, re.sub(
                    _id_p, _id_r, re.sub(
                        _for_p, _for_r, form_field
                    )
                )
            )
            self._all[form_field] = Markup(f"{_final}")
            return

    def upel(self, form_field, element) -> None:
        """
        This looks up the name of a form_field located in a Form and replaces its Element with the
        passed in new Element
        :param form_field:
        :param element:
        :return:
        """
        if isinstance(element, Markup):
            self._all[form_field] = element
            return
        self._all[form_field] = Markup(element)
        return


class Elements:

    @classmethod
    def no_space(cls, string: str) -> str:
        return string.replace(" ", "").lower()

    @classmethod
    def title(cls, string: str) -> str:
        return string.title()

    @classmethod
    def wrap_element(cls, _constructor: list, wrap_class: str = None, wrap_inner_class: str = None) -> list:
        if wrap_inner_class is not None:
            _constructor.insert(0, f'<div class="{wrap_inner_class}">')
            _constructor.append("</div>")
        if wrap_class is not None:
            _constructor.insert(0, f'<div class="{wrap_class}">')
            _constructor.append("</div>")
        return _constructor

    @classmethod
    def apply_input_group(cls, _constructor) -> list:
        _constructor.insert(0, '<div class="input-group">')
        _constructor.append('</div>')
        return _constructor

    @classmethod
    def prepend_label_func(cls, _constructor: list, label: str) -> list:
        if '<div class="input-group">' not in _constructor:
            _constructor = cls.apply_input_group(_constructor)
        _constructor.insert(1, f'</div>')
        _constructor.insert(1,
                            f'<span class="input-group-text" id="inputGroup-sizing-default">{label}</span>')
        _constructor.insert(1, f'<div class="input-group-prepend">')
        return _constructor

    @classmethod
    def append_label_func(cls, _constructor: list, label: str) -> list:
        if '<div class="input-group">' not in _constructor:
            _constructor = cls.apply_input_group(_constructor)

        if '</div>' in _constructor[-1:]:
            _constructor.insert(len(_constructor) - 1, f'<div class="input-group-append">')
            _constructor.insert(len(_constructor) - 1,
                                f'<span class="input-group-text" id="inputGroup-sizing-default">{label}</span>')
            _constructor.insert(len(_constructor) - 1, f'</div>')
            return _constructor

        _constructor.append('<div class="input-group-append">')
        _constructor.append(
            f'<span class="input-group-text" id="inputGroup-sizing-default">{label}</span>')
        _constructor.append('</div>')
        return _constructor

    @classmethod
    def append_text_func(cls, _constructor: list, text: str, css: str = "") -> list:
        if css != "":
            css = f" {css}"
        if '<div class="input-group">' not in _constructor:
            _constructor = cls.apply_input_group(_constructor)
        if '</div>' in _constructor[-1:]:
            _constructor.insert(len(_constructor) - 1, f'<div class="input-group-append">')
            _constructor.insert(len(_constructor) - 1,
                                f'<span class="input-group-text" id="inputGroup-sizing-default">{text}</span>')
            _constructor.insert(len(_constructor) - 1, f'</div>')
            return _constructor

        _constructor.append('<div class="input-group-append">')
        _constructor.append(
            f'<span class="input-group-text{css}" id="inputGroup-sizing-default">{text}</span>')
        _constructor.append('</div>')
        return _constructor

    @classmethod
    def prepend_button_func(cls, _constructor: list, button_object: str) -> list:
        if '<div class="input-group">' not in _constructor:
            _constructor = cls.apply_input_group(_constructor)
        _constructor.insert(1, f'</div>')
        _constructor.insert(1, button_object)
        _constructor.insert(1, f'<div class="input-group-prepend">')
        _constructor.insert(1, f'<div class="input-group">')
        _constructor.append('</div>')
        return _constructor

    @classmethod
    def append_button_func(cls, _constructor: list, button_object: str) -> list:
        if '<div class="input-group">' not in _constructor:
            _constructor.append('<div class="input-group-append">')
            _constructor.append(button_object)
            _constructor.append('</div>')
            _constructor = cls.apply_input_group(_constructor)
            return _constructor

        _constructor.insert(_constructor.__len__() - 1, f'<div class="input-group-append">')
        _constructor.insert(_constructor.__len__() - 1, button_object)
        _constructor.append('</div>')
        return _constructor

    @classmethod
    def html(cls, html: str) -> Markup:
        return Markup(html)

    @classmethod
    def hidden(cls,
               name: str = ":null:",
               value: str = "submit"
               ):
        return Markup(
            f'<input fbf-type="hidden" type="hidden" name="{cls.no_space(name)}" id="{cls.no_space(name)}" value="{value}" />')

    @classmethod
    def switch(cls,
               name: str = ":null:",
               label: str = "",
               label_class: str = "",
               input_class: str = "",
               onclick: str = "",
               wrap_class: str = None,
               wrap_inner_class: str = None,
               checked: bool = False,
               disabled: bool = False,
               required: bool = False,
               readonly: bool = False,
               ) -> Markup:

        _construction = [
            '<div class="form-check form-switch">',
            f'<input fbf-type="switch" type="checkbox" ',
            f'name="{name}" id="{name}" ',
            f'class="form-check-input',
        ]
        if input_class != "":
            _construction.append(f" {input_class}")
        _construction.append('" fbf-options="->"')
        if onclick != "":
            _construction.append(f' onclick="{onclick}"')
        if disabled:
            _construction.append(' disabled')
        if required:
            _construction.append(' required')
        if readonly:
            _construction.append(' readonly')
        if checked:
            _construction.append(' checked')
        _construction.append(' />')
        if label != "":
            if label_class != "":
                label_class = f" {label_class}"
            _construction.append(
                f'<label class="form-check-label{label_class}" for="{name}">{label}</label>'
            )
        _construction.append('</div>')
        final = cls.wrap_element(_construction, wrap_class, wrap_inner_class)
        return Markup("".join(final))

    @classmethod
    def radio(cls,
              grouped_name: str,
              value: str = ":null:",
              label: str = "",
              label_class: str = "",
              input_class: str = "",
              onclick: str = "",
              wrap_class: str = None,
              wrap_inner_class: str = None,
              checked: bool = False,
              disabled: bool = False,
              required: bool = False,
              readonly: bool = False,
              ) -> Markup:

        _id = value.lower().replace(" ", "")

        _frame = inspect.currentframe().f_back
        _caller = list(_frame.f_locals.keys())[-1]

        _construction = [
            '<div class="form-check">',
            f'<input fbf-type="radio" type="radio" ',
            f'name="{grouped_name}" id="{value}" value="{value}" ',
            f'class="form-check-input',
        ]
        if input_class != "":
            _construction.append(f" {input_class}")
        _construction.append('"')
        if onclick != "":
            _construction.append(f' onclick="{onclick}"')

        _construction.append(' fbf-options="->"')
        if disabled:
            _construction.append(' disabled')
        if required:
            _construction.append(' required')
        if readonly:
            _construction.append(' readonly')
        if checked:
            _construction.append(' checked')
        _construction.append(' />')
        if label != "":
            if label_class != "":
                label_class = f" {label_class}"
            _construction.append(
                f'<label class="form-check-label{label_class}" for="{value}">{label}</label>'
            )
        _construction.append('</div>')
        final = cls.wrap_element(_construction, wrap_class, wrap_inner_class)
        return Markup("".join(final))

    @classmethod
    def button(cls,
               label: str,
               element_type: str = "button",
               button_action: str = "button",
               button_class: str = None,
               href: str = "#",
               target: str = "",
               wrap_class: str = None,
               wrap_inner_class: str = None,
               disabled: bool = False,
               ) -> Markup:
        """
        Generates a Bootstrap button.
        element_type: button , a
        button_action: button , submit , reset
        Default element_type: button
        """

        _construction = []
        valid_button_action = ["button", "submit", "reset"]
        if button_class is not None:
            if "btn " not in button_class:
                button_class = f"btn {button_class}"
        else:
            button_class = "btn"

        if element_type == "a":
            _construction.append(f'<a fbf-type="a-button" href="{href}" ')
            _construction.append(f'class="{button_class}')
            if target != "":
                _construction.append(f'target="{target}')
            if disabled:
                _construction.append(' disabled')
            _construction.append(f'" role="button">{label}</a>')
            final = cls.wrap_element(_construction, wrap_class)
            return Markup("".join(final))

        if element_type == "button":
            if button_action not in valid_button_action:
                _construction.append("<p>Not a valid button_action type</p>")
                return Markup("".join(_construction))
            _construction.append(f'<button fbf-type="b-button" type="{button_action}" ')
            _construction.append(f'class="{button_class}" ')
            if disabled:
                _construction.append('disabled')
            _construction.append(f'>{label}</button>')
            final = cls.wrap_element(_construction, wrap_class, wrap_inner_class)
            return Markup("".join(final))

        _construction.append("<p>Not a valid element type</p>")
        return Markup("".join(_construction))

    @classmethod
    def input(cls,
              name: str = ":null:",
              label: str = "",
              prepend_label: str = "",
              append_label: str = "",
              prepend_button: Markup = None,
              append_button: Markup = None,
              append_text: str = "",
              append_text_css: str = "",
              placeholder: str = "",
              input_type: str = "text",
              input_class: str = "",
              input_id: str = "",
              wrap_class: str = None,
              wrap_inner_class: str = None,
              required: bool = False,
              readonly: bool = False,
              disabled: bool = False,
              multiple: bool = False,
              autofocus: bool = False,
              autocomplete: bool = True,
              value: str = "",
              mobile_picture: bool = False
              ) -> Markup:

        _name = cls.no_space(name)
        _label = cls.title(label)

        _construction = [
            f'<input fbf-type="input" ',
            f'type="{input_type}" ',
            f'name="{_name}" ',
            'class="form-control',
        ]

        if input_class != "":
            _construction.append(f' {input_class}')

        _construction.append(f'" id="{_name}', )
        if input_id != "":
            _construction.append(f' {input_id}')
        _construction.append(f'" value="{value}"')

        if placeholder != "":
            _construction.append(f' placeholder="{placeholder}"')

        if not autocomplete:
            _construction.append(' autocomplete="off"')

        if mobile_picture:
            _construction.append(' capture="environment"')

        if required:
            _construction.append(' required')

        if readonly:
            _construction.append(' readonly')

        if disabled:
            _construction.append(' disabled')

        if multiple:
            _construction.append(' multiple')

        if autofocus:
            _construction.append(' autofocus')

        _construction.append(" />")

        if mobile_picture:
            _construction.append("")

        if prepend_label != "" and prepend_button != None:
            return Markup("<p>Not able to prepend both a label and a button</p>")

        if append_label != "" and append_button != None:
            return Markup("<p>Not able to append both a label and a button</p>")

        if prepend_label != "":
            _construction = cls.prepend_label_func(_construction, prepend_label)

        if append_label != "":
            _construction = cls.append_label_func(_construction, append_label)

        if append_text != "":
            _construction = cls.append_text_func(_construction, append_text, append_text_css)

        if prepend_button != None:
            _construction = cls.prepend_button_func(_construction, prepend_button)

        if append_button != None:
            _construction = cls.append_button_func(_construction, append_button)

        if label != "":
            _construction.insert(0, f'<label for="{_name}" class="my-2">{_label}</label>')

        final = cls.wrap_element(_construction, wrap_class, wrap_inner_class)
        return Markup("".join(final))

    @classmethod
    def select(cls,
               name: str = ":null:",
               label: str = "",
               prepend_label: str = "",
               append_label: str = "",
               prepend_button: str = "",
               append_button: str = "",
               append_text: str = "",
               append_text_css: str = "",
               input_class: str = "",
               wrap_class: str = None,
               wrap_inner_class: str = None,
               selected: str = "",
               values_list: list = None,
               values_dict: dict = None,
               values_group_dict: dict = None,
               required: bool = False,
               readonly: bool = False,
               disabled: bool = False,
               multiple: bool = False,
               ):

        _name = cls.no_space(name)
        _label = cls.title(label)

        _construction = [
            '<select fbf-type="select" ',
            f'name="{_name}" ',
            f'id="{_name}" ',
            'style="-webkit-appearance: menulist;" ',
            f'class="form-control form-override {input_class}" ',
        ]

        if required:
            _construction.append(" required")

        if readonly:
            _construction.append(" readonly")

        if disabled:
            _construction.append(" disabled")

        if multiple:
            _construction.append(" multiple")

        _construction.append(">")

        if values_list:
            for value in values_list:
                if callable(value):
                    if value() == selected:
                        _construction.append(f'<option value="{value()}" selected>{value()}</option>')
                        continue
                    _construction.append(f'<option value="{value()}" >{value()}</option>')
                else:
                    if value == selected:
                        _construction.append(f'<option value="{value}" selected>{value}</option>')
                        continue
                    _construction.append(f'<option value="{value}" >{value}</option>')

        if values_dict:
            for key, value in values_dict.items():
                if value == selected:
                    _construction.append(f'<option value="{value}" selected>{key}</option>')
                    continue
                _construction.append(f'<option value="{value}" >{key}</option>')

        if values_group_dict:
            for group, group_dict in values_group_dict.items():
                _construction.append(f'<optgroup label="{group}">')
                for key, value in group_dict.items():
                    if value == selected:
                        _construction.append(f'<option value="{value}" selected >{key}</option>')
                    _construction.append(f'<option value="{value}" >{key}</option>')
                _construction.append('</optgroup>')

        _construction.append('</select>')

        if prepend_label != "":
            _construction = cls.prepend_label_func(_construction, prepend_label)

        if append_label != "":
            _construction = cls.append_label_func(_construction, prepend_label)

        if append_text != "":
            _construction = cls.append_text_func(_construction, append_text, append_text_css)

        if prepend_button != "":
            _construction = cls.prepend_button_func(_construction, prepend_button)

        if append_button != "":
            _construction = cls.append_button_func(_construction, append_button)

        if label != "":
            _construction.insert(0, f'<label for="{_name}" class="my-2">{_label}</label>')

        final = cls.wrap_element(_construction, wrap_class, wrap_inner_class)
        return Markup("".join(final))
