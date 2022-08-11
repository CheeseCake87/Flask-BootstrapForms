import inspect
import re

from markupsafe import Markup


class FlaskBootstrapForms:
    _app = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        if app is None:
            raise ImportError("No app passed into the FlaskBootstrapForms")
        self._app = app

        @app.context_processor
        def upval():
            def _upval(element, value):

                if value is None:
                    return Markup(element)

                if element is None:
                    return f"The element to have value its changed to >>{value}<< does not exist anymore"

                if 'fbf-type="input"' in element or 'fbf-type="hidden"' in element:
                    if isinstance(value, str) or isinstance(value, int):
                        _value_p = r'value="(.*?)"'
                        _value_r = rf'value="{value}"'
                        return Markup(f"{re.sub(_value_p, _value_r, element)}")
                    return Markup(element)

                if 'fbf-type="select"' in element:
                    if isinstance(value, str) or isinstance(value, int):
                        if value in element:
                            _strip = element.replace("selected", "")
                            _value_p = rf'value="{value}" (.*?)>'
                            _value_r = rf'value="{value}" selected>'
                            return Markup(f"{re.sub(_value_p, _value_r, _strip)}")
                    return Markup(element)

                if 'fbf-type="switch"' in element or 'fbf-type="radio"' in element:
                    _true_markers, _false_markers = ["yes", "true", "checked"], ["no", "false", "unchecked"]

                    value_found = False

                    if isinstance(value, str) or isinstance(value, int):
                        _value_p = r'value="(.*?)"'
                        _value_f = re.search(_value_p, element)
                        if _value_f:
                            value = True
                            value_found = True
                        else:
                            if value in _true_markers:
                                value = True
                            if value in _false_markers:
                                value = False

                    if isinstance(value, bool):
                        if value_found and "checked" in element:
                            return Markup(element)
                        if value_found and "checked" not in element:
                            _check_p = r'fbf-options="->" (.*?)/>'
                            _find = re.search(_check_p, element)
                            if _find is None:
                                return Markup(element)
                            _r = rf'fbf-options="->" {_find.group()[17:-2]}checked />'
                            return Markup(f"{re.sub(_check_p, _r, element)}")

                        if "checked" in element:
                            return Markup(element.replace(" checked", ""))

                return Markup(element)

            return dict(upval=_upval)

        @app.context_processor
        def radgro():
            def _radgro(element, group_name):
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
                return Markup(element)

            return dict(radgro=_radgro)

        @app.context_processor
        def upnam():
            def _upnam(element, name, match_id=False):

                if name is None:
                    return Markup(element)

                if element is None:
                    return f"The element to have its name changed to >>{name}<< does not exist anymore"

                if isinstance(name, str) or isinstance(name, int):
                    _name_p = r'name="(.*?)"'
                    _name_r = rf'name="{name}"'
                    if match_id:
                        _id_p = r'id="(.*?)"'
                        _id_r = rf'id="{name}"'
                        return Markup(f"{re.sub(_name_p, _name_r, re.sub(_id_p, _id_r, element))}")

                    return Markup(f"{re.sub(_name_p, _name_r, element)}")

                return Markup(element)

            return dict(upnam=_upnam)

        @app.context_processor
        def upid():
            def _upid(element, element_id):

                if element_id is None:
                    return Markup(element)

                if element is None:
                    return f"The element to have its id changed to >>{element_id}<< does not exist anymore"

                if isinstance(element_id, str) or isinstance(element_id, int):
                    _name_p = r'id="(.*?)"'
                    _name_r = rf'id="{element_id}"'

                    return Markup(f"{re.sub(_name_p, _name_r, element)}")

                return Markup(element)

            return dict(upid=_upid)


class NoContext:
    @classmethod
    def upval(cls, element, value):
        if value is None:
            return Markup(element)

        if element is None:
            return f"The element to have its value changed to >>{value}<< does not exist anymore"

        if 'fbf-type="input"' in element or 'fbf-type="hidden"' in element:
            if isinstance(value, str) or isinstance(value, int):
                _value_p = r'value="(.*?)"'
                _value_r = rf'value="{value}"'
                return Markup(f"{re.sub(_value_p, _value_r, element)}")
            return Markup(element)

        if 'fbf-type="select"' in element:
            if isinstance(value, str) or isinstance(value, int):
                if value in element:
                    _strip = element.replace("selected", "")
                    _value_p = rf'value="{value}" (.*?)>'
                    _value_r = rf'value="{value}" selected>'
                    return Markup(f"{re.sub(_value_p, _value_r, _strip)}")
            return Markup(element)

        if 'fbf-type="switch"' in element or 'fbf-type="radio"' in element:
            _true_markers, _false_markers = ["yes", "true", "checked"], ["no", "false", "unchecked"]

            value_found = False

            if isinstance(value, str) or isinstance(value, int):
                _value_p = r'value="(.*?)"'
                _value_f = re.search(_value_p, element)
                if _value_f:
                    value = True
                    value_found = True
                else:
                    if value in _true_markers:
                        value = True
                    if value in _false_markers:
                        value = False

            if isinstance(value, bool):
                if value_found and "checked" in element:
                    return Markup(element)
                if value_found and "checked" not in element:
                    _check_p = r'fbf-options="->" (.*?)/>'
                    _find = re.search(_check_p, element)
                    if _find is None:
                        return Markup(element)
                    _r = rf'fbf-options="->" {_find.group()[17:-2]}checked />'
                    return Markup(f"{re.sub(_check_p, _r, element)}")

                if "checked" in element:
                    return Markup(element.replace(" checked", ""))

        return Markup(element)

    @classmethod
    def radgro(cls, element, group_name):
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

        return Markup(element)

    @classmethod
    def upnam(cls, element, name, match_id=False):

        if name is None:
            return Markup(element)

        if element is None:
            return f"The element to have its name changed to >>{name}<< does not exist anymore"

        if isinstance(name, str) or isinstance(name, int):
            _name_p = r'name="(.*?)"'
            _name_r = rf'name="{name}"'
            if match_id:
                _id_p = r'id="(.*?)"'
                _id_r = rf'id="{name}"'
                return Markup(f"{re.sub(_name_p, _name_r, re.sub(_id_p, _id_r, element))}")

            return Markup(f"{re.sub(_name_p, _name_r, element)}")

        return Markup(element)

    @classmethod
    def upid(cls, element, element_id):

        if element_id is None:
            return Markup(element)

        if element is None:
            return f"The element to have its element_id changed to >>{element_id}<< does not exist anymore"

        if isinstance(element_id, str) or isinstance(element_id, int):
            _element_id_p = r'id="(.*?)"'
            _element_id_r = rf'id="{element_id}"'

            return Markup(f"{re.sub(_element_id_p, _element_id_r, element)}")

        return Markup(element)


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

    def upel(self, form_field, element) -> None:
        if isinstance(element, Markup):
            self._all[form_field] = element
            return
        self._all[form_field] = Markup(element)
        return

    def upval(self, form_field, value) -> None:
        if form_field in self._all:
            _escape_markup = self._all[form_field].unescape()

            if value is None:
                self._all[form_field] = Markup(_escape_markup)
                return

            if 'fbf-type="input"' in _escape_markup or 'fbf-type="hidden"' in _escape_markup:
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
                value_found = False

                if isinstance(value, str) or isinstance(value, int):
                    _value_p = r'value="(.*?)"'
                    _value_f = re.search(_value_p, _escape_markup)
                    if _value_f:
                        value = True
                        value_found = True
                    else:
                        if value in _true_markers:
                            value = True
                        if value in _false_markers:
                            value = False

                if isinstance(value, bool):
                    if value_found and "checked" in _escape_markup:
                        self._all[form_field] = Markup(_escape_markup)
                        return
                    if value_found and "checked" not in _escape_markup:
                        _check_p = r'fbf-options="->" (.*?)/>'
                        _find = re.search(_check_p, _escape_markup)
                        if _find is None:
                            self._all[form_field] = Markup(_escape_markup)
                            return
                        _r = rf'fbf-options="->" {_find.group()[17:-2]}checked />'
                        self._all[form_field] = Markup(f"{re.sub(_check_p, _r, _escape_markup)}")
                        return

                    if "checked" in _escape_markup:
                        self._all[form_field] = Markup(_escape_markup.replace(" checked", ""))
                        return

            self._all[form_field] = Markup(_escape_markup)
            return

    def upnam(self, form_field, name, match_id=False) -> None:
        _escape_markup = self._all[form_field].unescape()

        if name is None:
            self._all[form_field] = Markup(_escape_markup)
            return

        _name_p = r'name="(.*?)"'
        _name_r = rf'name="{name}"'
        if match_id:
            _id_p = r'id="(.*?)"'
            _id_r = rf'id="{name}"'
            self._all[form_field] = Markup(f"{re.sub(_name_p, _name_r, re.sub(_id_p, _id_r, _escape_markup))}")
            return
        self._all[form_field] = Markup(f"{re.sub(_name_p, _name_r, _escape_markup)}")
        return

    def radgro(self, form_field, group_name) -> None:
        _escape_markup = self._all[form_field].unescape()

        if group_name is None:
            return

        if 'fbf-type="radio"' in _escape_markup:
            _name_p, _id_p, _for_p, _value_p = r'name="(.*?)"', r'id="(.*?)"', r'for="(.*?)"', r'value="(.*?)"'
            _value_f = re.search(_value_p, _escape_markup)
            _name_r, _id_r, _for_r = rf'name="{group_name}"', rf'id="{group_name}_{_value_f.group()[7:-1]}"', rf'for="{group_name}_{_value_f.group()[7:-1]}"'
            _final = re.sub(
                _name_p, _name_r, re.sub(
                    _id_p, _id_r, re.sub(
                        _for_p, _for_r, _escape_markup
                    )
                )
            )
            self._all[form_field] = Markup(f"{_final}")
            return

        self._all[form_field] = Markup(_escape_markup)
        return

    def upid(self, form_field, element_id) -> None:
        _escape_markup = self._all[form_field].unescape()

        if element_id is None:
            self._all[form_field] = Markup(_escape_markup)
            return

        if isinstance(element_id, str) or isinstance(element_id, int):
            _element_id_p = r'id="(.*?)"'
            _element_id_r = rf'id="{element_id}"'

            self._all[form_field] = Markup(f"{re.sub(_element_id_p, _element_id_r, _escape_markup)}")

        self._all[form_field] = Markup(_escape_markup)
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
               manual_tags: str = "",
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

        if onclick != "":
            _construction.append(f' onclick="{onclick}"')

        if manual_tags != "":
            _construction.append(f' {manual_tags}')

        _construction.append('" fbf-options="->"')
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
              manual_tags: str = "",
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
               manual_tags: str = "",
               wrap_class: str = None,
               wrap_inner_class: str = None,
               disabled: bool = False,
               ) -> Markup:

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
            _construction.append(f'" role="button">{label}</a>')

            if manual_tags != "":
                _construction.append(f' {manual_tags}')

            _construction.append(' fbf-options="->"')
            if disabled:
                _construction.append(' disabled')
            final = cls.wrap_element(_construction, wrap_class)
            return Markup("".join(final))

        if element_type == "button":
            if button_action not in valid_button_action:
                _construction.append("<p>Not a valid button_action type</p>")
                return Markup("".join(_construction))
            _construction.append(f'<button fbf-type="b-button" type="{button_action}" ')
            _construction.append(f'class="{button_class}" ')
            if manual_tags != "":
                _construction.append(f' {manual_tags}')
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
              value: str = "",
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
              manual_tags: str = "",
              wrap_class: str = None,
              wrap_inner_class: str = None,
              required: bool = False,
              readonly: bool = False,
              disabled: bool = False,
              multiple: bool = False,
              autofocus: bool = False,
              autocomplete: bool = True,
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

        if manual_tags != "":
            _construction.append(f' {manual_tags}')

        _construction.append(' fbf-options="->"')

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
            f'<select fbf-type="select" name="{_name}" id="{_name}" style="-webkit-appearance: menulist;" class="form-control form-override {input_class}" fbf-options="->"']

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
