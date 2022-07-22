def test():
    from app._flask_bootstrapforms.src.flask_bootstrapforms import BootstrapForm, Elements

    test_form = BootstrapForm(form_tags=True, name="test_form", method="POST", action="google.com")

    values = ["this", "that"]

    test_form.add(
        "input",
        Elements.input(
            label="input",
        ))

    test_form.add(
        "select",
        Elements.select(
            label="Select",
            values_list=values
        ))

    test_form.add(
        "switch",
        Elements.switch(
            label="Switch",
        ))

    test_form.update_value("input", "new value")
    test_form.update_value("select", "this")
    test_form.update_value("switch", True)
    return


if __name__ == '__main__':
    import timeit

    print(timeit.timeit("test()", setup="from __main__ import test", number=1000))
