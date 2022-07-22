from markupsafe import Markup
import inspect


class BootstrapForms:
    def __init__(self, form_tags: bool = False, name: str = None, method: str = None, action: str = None):
        self.form_tags = form_tags
        self.name = name
        self.method = method
        self.action = action
        self._all = {}
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        self.caller = inspect.getframeinfo(frame[0]).code_context[0].strip().split(" = ")[0]

    def all(self) -> dict:
        if self._all == {}:
            return {f"{self.caller}": f"{self.caller} form is empty"}
        if self.form_tags:
            _form = ['<form']
            if self.name is not None:
                _form.append(f" name={self.name}")
            if self.method is not None:
                _form.append(f" method={self.method}")
            if self.action is not None:
                _form.append(f" action={self.action}")
            _form.append(">")
            _form = {"__start__": Markup("".join(_form))}
            _form.update(self._all)
            _form.update({"__end__": Markup('</form>')})
            return _form
        return self._all

    def add(self, name: str, element: Markup = None, element_list: list = None) -> None:
        _null_marker = ":null:"
        if element is not None:
            if _null_marker in element:
                element = element.replace(_null_marker, name)
            tack = {name: element}
            self._all.update(tack)
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

    def join(self, join_dict):
        if "__start__" in join_dict:
            del join_dict['__start__']
            del join_dict['__end__']
        self._all.update(join_dict)

    def remove(self, name) -> None:
        self._all.pop(name)

    def update_value(self, name, update) -> None:
        if name in self._all:
            _escape_markup = self._all[name].unescape()
            if "-input-" in _escape_markup:
                _input_split = []
                _input_split = _escape_markup.split("-- ")
                print(_input_split)
                _input_split[1] = f'-- value="{update}" -- '
                _input_join = "".join(_input_split)
                self._all[name] = Markup(_input_join)

            if "-select-" in _escape_markup:
                _select_split = []
                _replace = _escape_markup.replace("selected", "--")
                _select_split = _replace.split("--")
                for i, value in enumerate(_select_split):
                    if i == len(_select_split) - 1:
                        break
                    if f'value="{update}"' in value:
                        _select_split[i] = f"{value}selected"
                    else:
                        _select_split[i] = f"{_select_split[i]}--"

                _select_join = "".join(_select_split)
                self._all[name] = Markup(_select_join)
                return

            if "-switch-" in _escape_markup:
                _true_markers, _false_markers = ["yes", "true", "checked"], ["no", "false", "unchecked"]
                if isinstance(update, bool):
                    if update:
                        self._all[name] = Markup(_escape_markup.replace("--", "checked"))
                        return
                    self._all[name] = Markup(_escape_markup.replace("checked", "--"))
                if update in _true_markers:
                    self._all[name] = Markup(_escape_markup.replace("--", "checked"))
                    return
                if update in _false_markers:
                    self._all[name] = Markup(_escape_markup.replace("--", "checked"))
                    return

        return

    def update_element(self, name, element) -> None:
        if isinstance(element, Markup):
            self._all[name] = element
            return
        self._all[name] = Markup(element)
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

        _constructor.append(f'<div class="input-group-append">')
        _constructor.append(
            f'<span class="input-group-text" id="inputGroup-sizing-default">{label}</span>')
        _constructor.append(f'</div>')
        return _constructor

    @classmethod
    def append_text_func(cls, _constructor: list, text: str, css: str = "") -> list:
        if css != "":
            css = f" {css}"
        if '<div class="input-group">' not in _constructor:
            print("fired")
            _constructor = cls.apply_input_group(_constructor)
        print(_constructor[-1:])
        if '</div>' in _constructor[-1:]:
            _constructor.insert(len(_constructor) - 1, f'<div class="input-group-append">')
            _constructor.insert(len(_constructor) - 1,
                                f'<span class="input-group-text" id="inputGroup-sizing-default">{text}</span>')
            _constructor.insert(len(_constructor) - 1, f'</div>')
            return _constructor

        _constructor.append(f'<div class="input-group-append">')
        _constructor.append(
            f'<span class="input-group-text{css}" id="inputGroup-sizing-default">{text}</span>')
        _constructor.append(f'</div>')
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
            _constructor.append(f'<div class="input-group-append">')
            _constructor.append(button_object)
            _constructor.append(f'</div>')
            _constructor = cls.apply_input_group(_constructor)
            return _constructor

        _constructor.insert(_constructor.__len__() - 1, f'<div class="input-group-append">')
        _constructor.insert(_constructor.__len__() - 1, button_object)
        _constructor.append(f'</div>')
        return _constructor

    @classmethod
    def hidden(cls,
               name: str = ":null:",
               value: str = "submit"
               ):
        return Markup(
            f'<input type="hidden" name="{cls.no_space(name)}" id="{cls.no_space(name)}" value="{value}" />')

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

        _construction = ['<div class="form-check form-switch">', '<input -switch- class="form-check-input']
        if input_class != "":
            _construction.append(f' {input_class}')
        _construction.append(f'" type="checkbox" name="{name}" id="{name}"')
        if onclick != "":
            _construction.append(f' onclick="{onclick}"')
        if checked:
            _construction.append(' checked')
        else:
            _construction.append(' --')
        if disabled:
            _construction.append(' disabled')
        if required:
            _construction.append(' required')
        if readonly:
            _construction.append(' readonly')
        _construction.append(' >')
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
        button_action: button , submit , rest
        Default element_type: button
        """

        _construction = []
        valid_button_action = ["button", "submit", "reset"]
        if button_class is not None:
            if "btn " not in button_class:
                button_class = "btn " + button_class
        else:
            button_class = "btn"

        if element_type == "a":
            _construction.append(f'<a href="{href}" ')
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
            _construction.append(f'<button type="{button_action}" ')
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
              value: str = "",
              mobile_picture: bool = False
              ) -> Markup:

        _name = cls.no_space(name)
        _label = cls.title(label)

        _construction = [
            f'<input -input- ',
            f'type="{input_type}" ',
            f'name="{_name}" ',
            'class="form-control',
        ]

        if input_class != "":
            _construction.append(f' {input_class}')

        _construction.append(f'" id="{_name}', )
        if input_id != "":
            _construction.append(f' {input_id}')
        _construction.append(f'" -- value="{value}" -- ')

        if placeholder != "":
            _construction.append(f' placeholder="{placeholder}"')

        if mobile_picture:
            _construction.append(f' capture="environment"')

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
            '<select -select- ',
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
                if value == selected:
                    _construction.append(f'<option value="{value}" selected >{value}</option>')
                    continue
                _construction.append(f'<option value="{value}" -- >{value}</option>')

        if values_dict:
            for key, value in values_dict.items():
                if value == selected:
                    _construction.append(f'<option value="{value}" selected >{key}</option>')
                    continue
                _construction.append(f'<option value="{value}" -- >{key}</option>')

        if values_group_dict:
            for group, group_dict in values_group_dict.items():
                _construction.append(f'<optgroup label="{group}">')
                for key, value in group_dict.items():
                    if value == selected:
                        _construction.append(f'<option value="{value}" selected >{key}</option>')
                    _construction.append(f'<option value="{value}" -- >{key}</option>')
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
