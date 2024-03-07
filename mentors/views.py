from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from  django.views.decorators.cache import cache_control 
from  django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mentors.models import *
from django.contrib.auth.models import Group
from datetime import datetime, timedelta
from datetime import date

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createuser(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Ce nom d\'utilisateur est déjà pris.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Cet email est déjà utilisé.')
            else:
                # Créer l'utilisateur
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                # Connexion automatique de l'utilisateur
                login(request, user)
                # Redirection vers la page de connexion
                messages.success(request, 'operation reussie!')
                return redirect('Mentors')
        else:
            messages.error(request, 'Les mots de passe ne correspondent pas.')

    return render(request, 'mentors/createuser.html')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Login(request):
    if request.user == None or request.user =="" or request.user.username == "":
        return render(request, "mentors/login.html")
    else:
        return HttpResponseRedirect('/')
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user != None:
            login(request, user)
            messages.info(request, "Connexion reussie !")
            return redirect('Mentors')
        else:
            messages.error(request, "Veuillez réssayer encore et saisir vos informations de connexion: utilisateur et mot de passe correctement.")
            return HttpResponseRedirect('login')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
    #deconnection du user avec la methode logout 
    logout(request)
    return redirect('home')



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_profile(request):
    user_profile = Profiles.objects.get(user=request.user)
    # Accéder au mentor de l'utilisateur connecté
    mentor = user_profile.mentor
    # Récupérer la liste des mentors
    mentors = User.objects.filter(groups__name='mentors')
    # Vérifier si l'utilisateur appartient au groupe 'mentors'
    mentors_group = request.user.groups.filter(name='mentors').exists()
    # Vérifier si l'utilisateur appartient au groupe 'utilisateurs'
    user_group = request.user.groups.filter(name='utilisateurs').exists()
    context = {'mentors': mentors, 'mentors_group': mentors_group, "user_group": user_group, "user_profile":user_profile, "mentor":mentor}
    return render(request, 'mentors/profile.html', context)



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editprofile(request, id):
    user_act = Profiles.objects.get(user=request.user)

    if request.method == "POST":
        user_act.telephone = request.POST.get('telephone')
        user_act.profile = request.POST.get('profile')
        user_act.ojectif = request.POST.get('ojectif')
        user_act.photo = request.FILES.get('photo')

        # Récupérer les IDs des clés étrangères
        niveau_id = int(request.POST.get('niveau'))
        commune_id = int(request.POST.get('commune'))
        domaine_id = int(request.POST.get('domaine'))
        etablissement_id = int(request.POST.get('etablissement'))
        type_mentorat_id = int(request.POST.get('type_mentorat'))

        # Vérifier si les clés étrangères existent dans la base de données
        try:
            commune = Communes.objects.get(id=commune_id)
            domaine = CategorieFormation.objects.get(id=domaine_id)
            etablissement = Etablissement.objects.get(id=etablissement_id)
            type_mentorat = Typementorat.objects.get(id=type_mentorat_id)
            niveau = Niveau_formation.objects.get(id=niveau_id)
        except (Communes.DoesNotExist, CategorieFormation.DoesNotExist, Etablissement.DoesNotExist, Typementorat.DoesNotExist, Niveau_formation.DoesNotExist):
            # Gérer le cas où une des clés étrangères n'existe pas
            return HttpResponseBadRequest("Une ou plusieurs clés étrangères sont invalides")

        # Associer les objets aux clés étrangères
        user_act.commune = commune
        user_act.domaine = domaine
        user_act.etablissement = etablissement
        user_act.type_mentorat = type_mentorat
        user_act.niveau = niveau
        
        # Sauvegarder le profil
        user_act.save()

        return redirect('user_profile')

    communes = Communes.objects.all()
    domaines = CategorieFormation.objects.all()
    etablissements = Etablissement.objects.all()
    types = Typementorat.objects.all()
    niveaux = Niveau_formation.objects.all()

    context = {
        "niveaux": niveaux,
        "types": types,
        "user_act": user_act,
        "communes": communes,
        "domaines": domaines,
        "etablissements": etablissements
    }

    return render(request, 'mentors/editprofile.html', context)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    slides = Slideimage.objects.all()
    thirty_days_ago = datetime.now() - timedelta(days=30)
    ressources = Ressources.objects.filter(created__gte=thirty_days_ago)
    #Récupérer les événements dont la date est postérieure à aujourd'hui
    upcoming_events = Evenement.objects.filter(date_even__gte=date.today()).order_by('date_even')
    context = {"upcoming_events":upcoming_events, "slides":slides, "ressources":ressources}
    return render(request, 'mentors/home.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_all_ressource(request):
    ressources = Ressources.objects.all()
    context = {"ressources":ressources}
    return render(request, 'mentors/get_all_ressource.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_all_even(request):
    evenements = Evenement.objects.all()
    context = {"evenements":evenements}
    return render(request, 'mentors/get_all_even.html', context)



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_ressource(request):
    return render(request, 'mentors/add_ressource.html')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_even(request):
    return render(request, 'mentors/add_even.html')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_forum(request):
    return render(request, 'mentors/add_forum.html')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_all_forum(request):
    return render(request, 'mentors/get_all_forum.html')



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def about(request):
    categories = CategorieFormation.objects.all().order_by('-created')
    context = {"categories":categories}
    return render(request, 'mentors/about.html', context)






@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Mentors(request):
    if request.method == 'POST':
        choix = request.POST.get('choix')
        user = request.user
        # Vérifier la valeur de l'input 'choix' et attribuer le groupe approprié
        if choix == '1':
            group_name = 'mentors'  
        elif choix == '2':
            group_name = 'utilisateurs'  
        else:
            group_name = '' 
        # Récupérer ou créer le groupe
        if group_name:  # S'assurer que le nom du groupe est défini
            group, created = Group.objects.get_or_create(name=group_name)
            # Ajouter l'utilisateur au groupe
            user.groups.add(group)
            return HttpResponseRedirect('user_profile')
        else:
            return render(request, 'mentors/Mentors.html', {'error_message': 'Le choix n\'est pas valide'})
    else:
        # Récupérer le groupe "mentors"
        mentors_group = Group.objects.get(name='mentors')
        # Récupérer les utilisateurs qui sont dans le groupe "mentors"
        mentors_users = mentors_group.user_set.all()
        # Maintenant, vous pouvez récupérer les profils associés à ces utilisateurs
        mentors_profiles = Profiles.objects.filter(user__in=mentors_users)
        # Vérifier si l'utilisateur appartient au groupe 'mentors'
        mentors_group = request.user.groups.filter(name='mentors').exists()
        # Vérifier si l'utilisateur appartient au groupe 'utilisateurs'
        user_group = request.user.groups.filter(name='utilisateurs').exists()
        context = {'mentors_profiles': mentors_profiles, 'mentors_group': mentors_group, "user_group": user_group}
        return render(request, 'mentors/Mentors.html', context)

  



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def abonnement(request, id):
    user = request.user
    mentor = Profiles.objects.get(pk=id)
    user_profile, created = Profiles.objects.get_or_create(user=user)
    
    # Vérifier si l'utilisateur actuel est déjà un mentor
    mentor_group = Group.objects.get(name='mentors')  # Assurez-vous que 'mentors' est le nom de votre groupe mentor
    if mentor_group in user.groups.all():
        messages.warning(request, "Vous êtes déjà un mentor. Vous ne pouvez pas vous abonner à un mentor.")
        return redirect("user_profile")
    
    # Si l'utilisateur n'a pas de mentor
    if not user_profile.mentor:
        user_profile.mentor = mentor
        user_profile.save()
        messages.success(request, "vous vous êtes abonné")
        return redirect('user_profile')
    # Si l'utilisateur est déjà abonné au même mentor
    elif user_profile.mentor == mentor:
        messages.warning(request, "Ce mentor est déja le votre")
        return redirect("user_profile")
    # Si l'utilisateur souhaite changer de mentor
    else:
        user_profile.mentor = mentor
        user_profile.save()
        messages.warning(request, "vous avez changer de mentors")
        return redirect('user_profile')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def desabonnement(request):
    user = request.user
    user_profile = Profiles.objects.get(user=user)

    # Vérifier si l'utilisateur est déjà désabonné
    if not user_profile.mentor:
        messages.warning(request, "Vous n'êtes pas actuellement abonné à un mentor.")
        return redirect("user_profile")

    # Effectuer le désabonnement
    user_profile.unsubscribe()
    messages.success(request, "Vous vous êtes désabonné de votre mentor avec succès.")
    return redirect('user_profile')



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def tableau_orientations(request):
    types_orientation = Type_oriention.objects.all()
    data = []
    
    for type_orientation in types_orientation:
        filieres = type_orientation.filiere_serie_set.all()
        type_data = {
            'type': type_orientation.libelle,
            'filieres': [],
        }
        for filiere in filieres:
            debouches = filiere.debouche_set.all()
            filiere_data = {
                'filiere': filiere.libelle,
                'debouches': [debouche.libelle for debouche in debouches],
            }
            type_data['filieres'].append(filiere_data)
        data.append(type_data)
    
    return render(request, 'mentors/orientation.html', {"data":data})

