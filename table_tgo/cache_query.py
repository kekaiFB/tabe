from .models import TGO
from django.core.cache import cache

def get_tgo():
    tgo = cache.get('tgo')
    if tgo is None:
        tgo = TGO.objects.all()
        cache.set('tgo', tgo, 300)
    return tgo 


