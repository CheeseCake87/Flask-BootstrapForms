import inspect

from markupsafe import Markup


class Elements:
    """
    Elements are built using lists, each argument you pass in controls how the lists are built.
    """

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
                            f'<span class="input-group-text">{label}</span>')
        _constructor.insert(1, f'<div class="input-group-prepend">')
        return _constructor

    @classmethod
    def append_label_func(cls, _constructor: list, label: str) -> list:
        if '<div class="input-group">' not in _constructor:
            _constructor = cls.apply_input_group(_constructor)

        if '</div>' in _constructor[-1:]:
            _constructor.insert(len(_constructor) - 1, f'<div class="input-group-append">')
            _constructor.insert(len(_constructor) - 1,
                                f'<span class="input-group-text">{label}</span>')
            _constructor.insert(len(_constructor) - 1, f'</div>')
            return _constructor

        _constructor.append('<div class="input-group-append">')
        _constructor.append(
            f'<span class="input-group-text">{label}</span>')
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
                                f'<span class="input-group-text">{text}</span>')
            _constructor.insert(len(_constructor) - 1, f'</div>')
            return _constructor

        _constructor.append('<div class="input-group-append">')
        _constructor.append(
            f'<span class="input-group-text{css}">{text}</span>')
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
            f'<input value="{value}" fbf-type="hidden" type="hidden" name="{cls.no_space(name)}" id="{cls.no_space(name)}" />')

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

        _construction.append('"')

        if onclick != "":
            _construction.append(f' onclick="{onclick}"')

        if manual_tags != "":
            _construction.append(f' {manual_tags}')

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
                f'<label class="form-check-label{label_class}" for="{name}">{label}</label>'
            )
        _construction.append('</div>')

        final = cls.wrap_element(_construction, wrap_class, wrap_inner_class)
        r = Markup("".join(final))
        _construction.clear()
        return r

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
            f'<input value="{value}" fbf-type="radio" type="radio" ',
            f'name="{grouped_name}" id="{value}" ',
            f'class="form-check-input',
        ]

        if input_class != "":
            _construction.append(f" {input_class}")
        _construction.append('"')
        if onclick != "":
            _construction.append(f' onclick="{onclick}"')

        if manual_tags != "":
            _construction.append(f' {manual_tags}')

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
        r = Markup("".join(final))
        _construction.clear()
        return r

    @classmethod
    def button(cls,
               label: str,
               element_type: str = "button",
               button_action: str = "button",
               button_class: str = None,
               href: str = "#",
               target: str = "",
               onclick: str = "",
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
            _construction.append(f'<a fbf-type="a-button" role="button" href="{href}"')
            _construction.append(f' class="{button_class}"')
            if target != "":
                _construction.append(f' target="{target}"')

            if onclick != "":
                _construction.append(f' onclick="{onclick}"')

            if manual_tags != "":
                _construction.append(f' {manual_tags}')

            _construction.append(' fbf-options="->"')
            if disabled:
                _construction.append(' disabled')

            _construction.append(f'>{label}</a>')

            final = cls.wrap_element(_construction, wrap_class)
            r = Markup("".join(final))
            _construction.clear()
            return r

        if element_type == "button":
            if button_action not in valid_button_action:
                _construction.append("<p>Not a valid button_action type</p>")
                r = Markup("".join(_construction))
                _construction.clear()
                return r
            _construction.append(f'<button fbf-type="b-button" type="{button_action}" ')
            _construction.append(f'class="{button_class}" ')
            if onclick != "":
                _construction.append(f' onclick="{onclick}"')

            if manual_tags != "":
                _construction.append(f' {manual_tags}')

            _construction.append(' fbf-options="->"')
            if disabled:
                _construction.append(' disabled')
            _construction.append(f'>{label}</button>')

            final = cls.wrap_element(_construction, wrap_class, wrap_inner_class)
            r = Markup("".join(final))
            _construction.clear()
            return r

        _construction.append("<p>Not a valid element type</p>")
        r = Markup("".join(_construction))
        _construction.clear()
        return r

    @classmethod
    def input(cls,
              name: str = ":null:",
              label: str = "",
              value: str = "",
              onclick: str = "",
              manual_tags: str = "",
              prepend_label: str = "",
              append_label: str = "",
              prepend_button: Markup = None,
              append_button: Markup = None,
              append_text: str = "",
              append_text_css: str = "",
              placeholder: str = "",
              input_type: str = "text",
              input_class: str = "",
              input_id: str = None,
              wrap_class: str = None,
              wrap_inner_class: str = None,
              required: bool = False,
              readonly: bool = False,
              disabled: bool = False,
              multiple: bool = False,
              autofocus: bool = False,
              autocomplete: bool = True,
              datalist: list = None,
              ) -> Markup:

        _name = cls.no_space(name)
        _label = cls.title(label)

        _construction = [
            f'<input value="{value}" fbf-type="input" ',
            f'type="{input_type}" ',
            f'name="{_name}" ',
            'class="form-control',
        ]

        if input_class != "":
            _construction.append(f' {input_class}')

        _construction.append(f'" id="{input_id or _name}"', )

        if placeholder != "":
            _construction.append(f' placeholder="{placeholder}"')

        if not autocomplete:
            _construction.append(' autocomplete="off"')

        if onclick != "":
            _construction.append(f' onclick="{onclick}"')

        if datalist is not None:
            _construction.append(f' list="{name}_datalist"')

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

        if datalist is not None:
            if isinstance(datalist, list):
                _construction.append(f'<datalist id="{name}_datalist">')
                for value in datalist:
                    _construction.append(f'<option value="{value}"/>')
                _construction.append(f'</datalist>')

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
        r = Markup("".join(final))
        _construction.clear()
        return r

    @classmethod
    def select(cls,
               name: str = ":null:",
               label: str = "",
               onclick: str = "",
               manual_tags: str = "",
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
            f'<select fbf-type="select" name="{_name}" id="{_name}" style="-webkit-appearance: menulist;" class="form-control form-override {input_class}"']

        if onclick != "":
            _construction.append(f' onclick="{onclick}"')

        if manual_tags != "":
            _construction.append(f' {manual_tags}')

        _construction.append(' fbf-options="->"')

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
        r = Markup("".join(final))
        _construction.clear()
        return r
