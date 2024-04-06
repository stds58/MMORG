from django import template
from random import *
from appcore.models import OneTimeCode
from django.contrib.auth.models import User


register = template.Library()


def generate_code(user):
   while True:
      seed()
      code_random = str(randint(10000, 99999))
      if not OneTimeCode.objects.filter(code=code_random):
         if not user.username:
            return False
            break
         else:
            u1 = User.objects.get(username=user)
            OneTimeCode.objects.create(code=code_random, user=u1)
            return code_random
            break


@register.simple_tag(takes_context=True)
def usual_login_view(context, **kwargs):
   user = context['user']
   if user is not None:
      code_random = generate_code(user)
      context['activate_url'] = f'http://127.0.0.1:8000/activation/  your activation code is {code_random}'
   else:
      context['activate_url'] = 'your email is not registered'
   return context['activate_url']



