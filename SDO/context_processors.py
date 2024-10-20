# sdo_dashboard/context_processors.py
from .models import Tariff

def tariff_processor(request):
    # Get the first tariff or return None if no tariffs exist
    
    tariff = Tariff.objects.first()  
    return {'tariff': tariff}
    
# context_processors.py (or wherever you keep your context processors)
from .models import sdo_profile  # or whichever model applies

def user_profile(request):
    if request.user.is_authenticated:
        profile = sdo_profile.objects.filter(user=request.user).first()
        return {'profile': profile}
    return {}
