from django import template

register = template.Library()


@register.filter(name='correct')
def correct(value):
    return f'correct{value}'


@register.filter(name='incorrect')
def incorrect(value):
    return f'incorrect{value}'


@register.filter(name='like')
def like(value):
    return f'like{value}'


@register.filter(name='dislike')
def dislike(value):
    return f'dislike{value}'
