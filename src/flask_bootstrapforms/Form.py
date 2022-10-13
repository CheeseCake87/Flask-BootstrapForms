import inspect
import re

from markupsafe import Markup


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
                _unpack_list = ""
                for index, element in enumerate(element_list):
                    if _null_marker in element:
                        _unpack_list += f"{element.unescape().replace(_null_marker, f'{name}_{index}')}"
                    else:
                        _unpack_list += f"{element.unescape()}"
                tack = {name: Markup(_unpack_list)}
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
            if value is None:
                return

            _escape_markup = self._all[form_field].unescape().replace(":value:", str(value))

            if 'fbf-type="input"' in _escape_markup or 'fbf-type="hidden"' in _escape_markup:
                _value_p = r'input value="(.*?)"'
                _value_r = rf'input value="{value}"'
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
                _check_p = r'fbf-options="->" (.*?)/>'
                _find = re.search(_check_p, _escape_markup)

                def checked():
                    _rep = rf'fbf-options="->" {_find.group()[17:-2]}checked />'
                    self._all[form_field] = Markup(f"{re.sub(_check_p, _rep, _escape_markup)}")
                    return

                if isinstance(value, str):
                    if value in _true_markers:
                        if "checked" in _escape_markup:
                            return
                        checked()

                    if value in _false_markers:
                        if "checked" in _escape_markup:
                            self._all[form_field] = Markup(_escape_markup.replace(" checked", ""))
                            return

                if isinstance(value, bool):
                    if value:
                        if "checked" in _escape_markup:
                            return
                        checked()

                    if not value:
                        if "checked" in _escape_markup:
                            self._all[form_field] = Markup(_escape_markup.replace(" checked", ""))
                            return

            self._all[form_field] = Markup(_escape_markup)
            return

    def upnam(self, form_field, name, match_id=False) -> None:
        if name is None:
            return

        _escape_markup = self._all[form_field].unescape().replace(":name:", name)

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
        if group_name is None:
            return

        _escape_markup = self._all[form_field].unescape().replace(":group_name:", group_name)

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
        if element_id is None:
            return

        _escape_markup = self._all[form_field].unescape().replace(":id:", element_id)

        if isinstance(element_id, str) or isinstance(element_id, int):
            _element_id_p = r'id="(.*?)"'
            _element_id_r = rf'id="{element_id}"'

            self._all[form_field] = Markup(f"{re.sub(_element_id_p, _element_id_r, _escape_markup)}")

        self._all[form_field] = Markup(_escape_markup)
        return
