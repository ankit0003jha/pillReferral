from django import template
  
register = template.Library()

@register.filter()
def mask(email):
    lo = email.find('@')
    if lo>0:
        return email[0:2]+"####"+email[lo-1:]
    else:
        return email
