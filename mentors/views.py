from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from  django.views.decorators.cache import cache_control 
from  django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mentors.models import *
from django.contrib.auth.models import Group





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createuser(request):
    if request.method == 'POST':
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
                user = User.objects.create_user(username=username, email=email, password=password)
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
    context = {"user_act":user_act}
    return render(request, 'mentors/editprofile.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    evenements = Evenement.objects.all().order_by('-created')
    context = {"evenements":evenements}
    return render(request, 'mentors/home.html', context)


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
        # Récupérer la liste des mentors
        mentors = User.objects.filter(groups__name='mentors')
        # Vérifier si l'utilisateur appartient au groupe 'mentors'
        mentors_group = request.user.groups.filter(name='mentors').exists()
        # Vérifier si l'utilisateur appartient au groupe 'utilisateurs'
        user_group = request.user.groups.filter(name='utilisateurs').exists()
        context = {'mentors': mentors, 'mentors_group': mentors_group, "user_group": user_group}
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

