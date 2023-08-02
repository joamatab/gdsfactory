"""Define names, clean values for names."""
from __future__ import annotations

import hashlib
from typing import Any

import pydantic

MAX_NAME_LENGTH = 32


@pydantic.validate_arguments
def get_name_short(name: str, max_name_length=MAX_NAME_LENGTH) -> str:
    """Returns a short name."""
    if len(name) > max_name_length:
        name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
        name = f"{name[:(max_name_length - 9)]}_{name_hash}"
    return name


def join_first_letters(name: str) -> str:
    """Join the first letter of a name separated with underscores.

    taper_length -> TL

    """
    return "".join([x[0] for x in name.split("_") if x])


# replace function_name prefix for some components
component_type_to_name = {"phidl": "phidl"}


def get_component_name(component_type: str, *args, **kwargs) -> str:
    """Returns concatenated kwargs Key_Value."""
    name = component_type + "_".join([clean_value(a) for a in args])
    for k, v in component_type_to_name.items():
        name = name.replace(k, v)
    if kwargs:
        name += f"_{dict2name(**kwargs)}"
    return name


def dict2hash(**kwargs) -> str:
    ignore_from_name = kwargs.pop("ignore_from_name", [])
    h = hashlib.sha256()
    for key in sorted(kwargs):
        if key not in ignore_from_name:
            value = kwargs[key]
            value = clean_value(value)
            h.update(f"{key}{value}".encode())
    return h.hexdigest()


def dict2name(prefix: str = "", **kwargs) -> str:
    """Returns name from a dict."""
    ignore_from_name = kwargs.pop("ignore_from_name", [])
    kv = []
    kwargs = kwargs.copy()
    kwargs.pop("layer_to_inclusion", "")

    for key in sorted(kwargs):
        if key not in ignore_from_name and isinstance(key, str):
            value = kwargs[key]
            if value is not None:
                kv += [f"{key}{clean_value(value)}"]
    label = prefix + "_".join(kv)
    return clean_name(label)


def assert_first_letters_are_different(**kwargs):
    """Assert that the first letters for each key are different.

    Avoids different args that start with the same first letter getting
    the same hash.

    """
    first_letters = [join_first_letters(k) for k in kwargs]
    if len(set(first_letters)) != len(first_letters):
        msg = f"Possible name collision! {kwargs.keys()} repeats first letters {first_letters}"
        raise ValueError(
            msg,
            "you can separate your arguments with underscores",
            " (delta_length -> DL, delta_width -> DW",
        )


def print_first_letters_warning(**kwargs) -> None:
    """Prints kwargs that have same cell."""
    first_letters = [join_first_letters(k) for k in kwargs]
    if len(set(first_letters)) != len(first_letters):
        print(
            f"Possible name collision! {kwargs.keys()} "
            f"repeats first letters {first_letters}"
            "you can separate your arguments with underscores"
            " (delta_length -> DL, delta_width -> DW",
        )


def clean_name(name: str, remove_dots: bool = False) -> str:
    """Return a string with correct characters for a cell name.

    [a-zA-Z0-9]

    FIXME: only a few characters are currently replaced.
        This function has been updated only on case-by-case basis

    """
    replace_map = {
        " ": "_",
        "!": "",
        "?": "",
        "#": "_",
        "%": "_",
        "(": "",
        ")": "",
        "*": "_",
        ",": "_",
        "-": "m",
        ".": "p",
        "/": "_",
        ":": "_",
        "=": "",
        "@": "_",
        "[": "",
        "]": "",
        "{": "",
        "}": "",
        "$": "",
    }

    if remove_dots:
        replace_map["."] = ""
    for k, v in list(replace_map.items()):
        name = name.replace(k, v)
    return name


def clean_value(value: Any) -> str:
    from gdsfactory.serialization import clean_value_json

    return str(clean_value_json(value))


# def testclean_value_json() -> None:


def test_clean_name() -> None:
    assert clean_name("wg(:_=_2852") == "wg___2852"


if __name__ == "__main__":
    import gdsfactory as gf

    d = {
        "X": gf.components.crossing45(port_spacing=40.0),
        "-": gf.components.compensation_path(
            crossing45=gf.components.crossing45(port_spacing=40.0),
        ),
    }
    d2 = clean_value(d)
    print(d2)
