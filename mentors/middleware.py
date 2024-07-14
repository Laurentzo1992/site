from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class ProfileCompletionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            user_profile = request.user.profiles
            required_fields = [
                'telephone', 'niveau', 'commune', 'village', 'domaine', 
                'etablissement', 'profile', 'objectif', 'type_mentorat', 
                'ojectif_academique', 'cannaux', 'frequesce', 'connaissance', 
                'attente'
            ]
            missing_fields = [field for field in required_fields if not getattr(user_profile, field)]

            if missing_fields:
                 # Remplacez 'complete_profile' par le nom de votre vue
                if request.path not in [reverse('complete_profile')]:
                    # Redirigez vers la vue de complétion du profil
                    return redirect('complete_profile')
        return None
