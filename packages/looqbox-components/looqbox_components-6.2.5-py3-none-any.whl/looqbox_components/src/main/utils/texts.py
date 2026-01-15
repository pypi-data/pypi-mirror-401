from looqbox import ObjColumn, ObjText


def obj_texts_from(text: str, text_size: int = 5) -> ObjColumn:
    splitted = text.split("<br>")
    splitted = list(filter(lambda it: it != "", splitted))
    return ObjColumn(list(map(lambda s: ObjText(s).set_as_title(text_size), splitted)))
