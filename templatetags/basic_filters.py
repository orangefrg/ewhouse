from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='getmodelfield')
def getmodelfield(value, arg):
    return getattr(value, arg)

@register.filter(name='getdictvalue')
def getdictvalue(value, arg):
    return value[arg]

@register.filter(name='getrange')
def getrange(value):
    return range(int(value))

@register.filter(name='addtoend')
def addtoend(value, arg):
    return "{}{}".format(arg, value)
