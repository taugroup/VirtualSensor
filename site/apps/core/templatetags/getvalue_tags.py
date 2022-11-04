from django import template

register = template.Library()


@register.simple_tag
def get_value(instance, field):
    # Field = type(instance)._meta.get_field(field)
    # return (Field.value_to_string(instance))
    return (getattr(instance, field))
