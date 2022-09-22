import re

from markupsafe import Markup


class FlaskBootstrapFormsContext:
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
                if element is None:
                    return f"The element to have its value changed to >>{value}<< does not exist anymore"

                if value is None:
                    return Markup(element)

                element = element.replace(":value:", str(value))

                if 'fbf-type="input"' in element or 'fbf-type="hidden"' in element:
                    if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                        _value_p = r'input value="(.*?)"'
                        _value_r = rf'input value="{value}"'
                        return Markup(f"{re.sub(_value_p, _value_r, element)}")
                    return Markup(element)

                if 'fbf-type="select"' in element:
                    if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                        if value in element:
                            _strip = element.replace("selected", "")
                            _value_p = rf'value="{value}" (.*?)>'
                            _value_r = rf'value="{value}" selected>'
                            return Markup(f"{re.sub(_value_p, _value_r, _strip)}")
                    return Markup(element)

                if 'fbf-type="switch"' in element or 'fbf-type="radio"' in element:
                    _true_markers, _false_markers = ["yes", "true", "checked"], ["no", "false", "unchecked"]
                    _check_p = r'fbf-options="->" (.*?)/>'
                    _find = re.search(_check_p, element)

                    def checked():
                        _rep = rf'fbf-options="->" {_find.group()[17:-2]}checked />'
                        return Markup(f"{re.sub(_check_p, _rep, element)}")

                    if isinstance(value, str):
                        if value in _true_markers:
                            if "checked" in element:
                                return Markup(element)
                            return checked()

                        if value in _false_markers:
                            if "checked" in element:
                                return Markup(element.replace(" checked", ""))

                    if isinstance(value, bool):
                        if value:
                            if "checked" in element:
                                return Markup(element)
                            return checked()

                        if not value:
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
                if element is None:
                    return f"The element to have its name changed to >>{name}<< does not exist anymore"

                if name is None:
                    return Markup(element)

                element = element.replace(":name:", name)

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
                if element is None:
                    return f"The element to have its element_id changed to >>{element_id}<< does not exist anymore"

                if element_id is None:
                    return Markup(element)

                element = element.replace(":id:", element_id)

                if isinstance(element_id, str) or isinstance(element_id, int):
                    _name_p = r'id="(.*?)"'
                    _name_r = rf'id="{element_id}"'

                    return Markup(f"{re.sub(_name_p, _name_r, element)}")

                return Markup(element)

            return dict(upid=_upid)
