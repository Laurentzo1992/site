from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from mentors.models import Profiles

class ProfileCompletionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            user_profile, _ = Profiles.objects.get_or_create(user=request.user)
            required_fields = [
                'telephone', 'niveau', 'commune'
            ]
            missing_fields = [field for field in required_fields if not getattr(user_profile, field)]

            if missing_fields:
                if request.path not in [reverse('complete_profile')]:
                    # Redirigez vers la vue de complétion du profil
                    return redirect('complete_profile')
        return None
