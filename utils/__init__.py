import typing

if typing.TYPE_CHECKING:
    from core.db import BaseModel
    from sqlalchemy import Column


def get_model_fields(model: typing.Type['BaseModel']) -> list['Column']:
    return list(model.metadata.tables[model.__tablename__].columns)


def get_model_field_names(model: typing.Type['BaseModel']) -> set[str]:
    return {c.name for c in get_model_fields(model)}


def to_dict(model: 'BaseModel',
            includes: typing.Sequence[str] = None,
            excludes: typing.Sequence[str] = None):
    if includes:
        fields = set(includes)
    else:
        fields = get_model_field_names(model)

    fields -= set(excludes)
    return {
        f: getattr(model, f)
        for f in fields
    }
