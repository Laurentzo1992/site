from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from  django.views.decorators.cache import cache_control 
from  django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mentors.models import *
from django.contrib.auth.models import Group
from datetime import datetime, timedelta
from datetime import date
from .forms import *
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count
from django.utils.translation import gettext as _
from django.utils.html import format_html

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    mentors = User.objects.filter(groups__name='mentors').count()
    mentores = User.objects.filter(groups__name='utilisateurs').count()
    politiques = Politique_Securite.objects.all().order_by('id')
    temoignages = Temoignage.objects.all()
    partenariats = Partenaire.objects.all().order_by('-created')
    debut = Presentation.objects.all().first()
    slides = Slideimage.objects.all()
    thirty_days_ago = datetime.now() - timedelta(days=30)
    ressources = Ressources.objects.filter(created__gte=thirty_days_ago)
    #Récupérer les événements dont la date est postérieure à aujourd'hui
    activites = Activite.objects.all().order_by('-id')
    #upcoming_events = Activite.objects.filter(date_even__gte=date.today()).order_by('date_even')
    
    data = Profiles.objects.all().exclude(niveau__isnull=True).values('niveau__libelle').annotate(user_count=Count('user')).order_by('niveau__libelle')
    levels = [entry['niveau__libelle'] for entry in data]
    counts = [entry['user_count'] for entry in data]
    
    context = {"mentores":mentores, "mentors":mentors, "data":data, "counts": counts, "levels": levels, "temoignages":temoignages, "politiques":politiques, "partenariats":partenariats, "debut":debut, "activites":activites, "slides":slides, "ressources":ressources}
    return render(request, 'mentors/home.html', context)


def boad(request):
    users = User.objects.all().count()
    demandes = Adession.objects.all()
    #mentorslists = User.objects.filter(groups__name='mentors')
    users_profiles = Profiles.objects.filter(user__groups__name='utilisateurs')
    mentorslists = Profiles.objects.filter(user__groups__name='mentors')
    mentors = User.objects.filter(groups__name='mentors').count()
    mentores = User.objects.filter(groups__name='utilisateurs').count()
    # Récupérer le groupe "mentor"
    mentor_group = Group.objects.get(name='mentors')
    # Récupérer le groupe "utilisateur"
    user_group = Group.objects.get(name='utilisateurs')
    # Exclure les superadmins et les utilisateurs appartenant aux groupes "mentor" et "utilisateur"
    sansmentores = User.objects.exclude(is_superuser=True).exclude(groups=mentor_group).exclude(groups=user_group).count()
    superadmins = User.objects.filter(is_superuser=True).count()
    
    # Récupérer les sessions actives dans la dernière minute
    derniere_minute = 1
    temps_limite = timezone.now() - timezone.timedelta(minutes=derniere_minute)
    sessions_actives = Session.objects.filter(expire_date__gte=temps_limite)

    # Extraire les IDs des utilisateurs connectés à partir des sessions actives
    ids_utilisateurs_connectes = [session.get_decoded().get('_auth_user_id') for session in sessions_actives if session.get_decoded().get('_auth_user_id') is not None]

    # Récupérer les utilisateurs connectés en excluant l'utilisateur anonyme
    utilisateurs_connectes = User.objects.filter(id__in=ids_utilisateurs_connectes)

    # Nombre d'utilisateurs connectés
    nombre_utilisateurs_connectes = utilisateurs_connectes.count()

    demandes_mentorats = Mentorat.objects.all().order_by('-id')
    
    sessions = demandes_mentorats.filter(statut__statut='valide')
    
    # Listes des demandeurs sans mentors
    # demandeurs_sans_mentor = Profiles.objects.filter(demandes_mentorat__mentor__isnull=True).distinct()
    demandeurs_sans_mentor = Mentorat.objects.filter(mentor__isnull=True)


    # Retrieve the activities for each session
    activities_by_session = {}
    for session in sessions:
        activities = ActiviteMentorat.objects.filter(mentorat=session)
        activities_by_session[session.id] = activities
    
    context = {
               "users_profiles":users_profiles,
               "mentorslists":mentorslists,
               "utilisateurs_connectes":utilisateurs_connectes,
               "nombre_utilisateurs_connectes":nombre_utilisateurs_connectes,
               "superadmins":superadmins, "sansmentores":sansmentores,
               "mentores":mentores, "mentors":mentors,
               "users":users,
               "demandes":demandes,
               "demandes_mentorats":demandes_mentorats,
               "sessions":sessions,
               "activities_by_session": activities_by_session,
               "demandeurs_sans_mentor":demandeurs_sans_mentor
               }
    return render(request, 'mentors/dashboard/boad.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createuser(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        try:
            can_be_mentor = int(request.POST.get('mentor'))
            if not 0<=can_be_mentor<=1:
                messages.error(request, _("Vous n'avez pas choisie d'etre mentor ou mentoré"))
                return redirect('login')
        except Exception as e:
            messages.error(request, _("Vous n'avez pas choisie d'etre mentor ou mentoré"))
            return redirect('login')
        
        if password == password2:
            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Ce nom d\'utilisateur est déjà pris.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Cet email est déjà utilisé.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                # Connexion automatique de l'utilisateur
                login(request, user)
                # Redirection vers la page de connexion
                profile = Profiles.objects.filter(user=user).first()
                if profile:
                    profile.can_be_mentor = True if can_be_mentor==1 else False
                    profile.save()
                    
                if profile.can_be_mentor:
                    group_name = 'mentors'  
                    Mentor.objects.create(profile=profile)
                else: 
                    group_name = 'utilisateurs'
                    Mentore.objects.create(profile=profile)
                    Mentorat.objects.create(demandeur=profile, statut=Mentorat_Statut.objects.filter(id=1).first())
                if group_name: 
                    group, created = Group.objects.get_or_create(name=group_name)
                    user.groups.add(group)
                messages.success(request, 'operation reussie!')
                return redirect('Mentors')
        else:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
    
    try:
        can_be_mentor = int(request.GET.get('mentor'))
        if not 0<=can_be_mentor<=1:
            messages.error(request, "Vous n'avez pas choisie d'etre mentor ou mentoré")
            return redirect('login')
    except:
        messages.error(request, "Vous n'avez pas choisie d'etre mentor ou mentoré")
        return redirect('login')
    return render(request, 'mentors/createuser.html',{'mentor': can_be_mentor})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Login(request):
    if request.user == None or request.user =="" or request.user.username == "":
        return render(request, "mentors/login.html")
    else:
        return HttpResponseRedirect(reverse('login'))
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        import re
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        if re.match(email_regex, username):
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                messages.error(request, "Aucun utilisateur trouvé avec cette adresse e-mail.")
                return HttpResponseRedirect(reverse('login'))
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "Connexion réussie !")
            return redirect('Mentors')
        else:
            messages.error(request, "Veuillez réessayer et saisir vos informations de connexion : utilisateur et mot de passe correctement.")
            return HttpResponseRedirect(reverse('login'))

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
    #deconnection du user avec la methode logout 
    logout(request)
    return redirect('home')





class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'mentors/password_reset.html'
    email_template_name = 'mentors/password_reset_email.html'
    subject_template_name = 'mentors/password_reset_subject.txt'
    success_message = "Nous vous avons envoye par e-mail des instructions pour définir votre mot de passe"
    success_url = reverse_lazy('home')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_profile(request):
    user_profile = Profiles.objects.get(user=request.user)
    # Accéder au mentor de l'utilisateur connecté
    # mentor = user_profile.mentor
    # Récupérer la liste des mentors
    # mentors = User.objects.filter(groups__name='mentors')
    # Vérifier si l'utilisateur appartient au groupe 'mentors'
    mentors_group = request.user.groups.filter(name='mentors').exists()
    # Vérifier si l'utilisateur appartient au groupe 'utilisateurs'
    user_group = request.user.groups.filter(name='utilisateurs').exists()
    
    nbr_res = Ressources.objects.filter(owner=request.user).count()
    
    nrb_forum = Forum.objects.filter(initiateur=request.user).count()
    
    nrb_even = Evenement.objects.filter(initiateur=request.user).count()
    
    temps_de_connxion = user_profile.formatted_total_time_on_platform()
    
    #nbr = Profiles.objects.filter(mentor=user_profile).count()
    context = {
               'nrb_even':nrb_even,
               'nrb_forum':nrb_forum,
               'nbr_res':nbr_res,
               'mentors_group': mentors_group,
               "user_group": user_group,
               "user_profile":user_profile,
               "temps_de_connxion":temps_de_connxion
               }
    return render(request, 'mentors/profile.html', context)



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editprofile(request, id):
    user_act = Profiles.objects.get(user=request.user)

    if request.method == "POST":
        user_act.telephone = request.POST.get('telephone')
        user_act.profile = request.POST.get('profile')
        user_act.objectif = request.POST.get('objectif')
        user_act.photo = request.FILES.get('photo')
        user_act.attente = request.POST.get('attente')
        user_act.village = request.POST.get('village')
        
        # Récupérer les IDs des clés étrangères (avec gestion des valeurs vides)
        niveau_id = request.POST.get('niveau')
        commune_id = request.POST.get('commune')
        domaine_id = request.POST.get('domaine')
        etablissement_id = request.POST.get('etablissement')
        type_mentorat_id = request.POST.get('type_mentorat')
        connaissance_id = request.POST.get('connaissance')
        frequesce_id = request.POST.get('frequesce')
        cannau_id = request.POST.get('cannau')
        ojectif_academique_id = request.POST.get('ojectif_academique')

        # Vérifier si les clés étrangères existent dans la base de données
        try:
            commune = Communes.objects.get(id=int(commune_id)) if commune_id else None
            domaine = CategorieFormation.objects.get(id=int(domaine_id)) if domaine_id else None
            etablissement = Etablissement.objects.get(id=int(etablissement_id)) if etablissement_id else None
            type_mentorat = Typementorat.objects.get(id=int(type_mentorat_id)) if type_mentorat_id else None
            niveau = Niveau_formation.objects.get(id=int(niveau_id)) if niveau_id else None
            
            connaissance = Cannaux_Connaissance.objects.get(id=int(connaissance_id)) if connaissance_id else None
            frequesce = Frequence_Echange.objects.get(id=int(frequesce_id)) if frequesce_id else None
            cannau = Cannaux_Communication.objects.get(id=int(cannau_id)) if cannau_id else None
            ojectif_academique = Objectif_Accademique.objects.get(id=int(ojectif_academique_id)) if ojectif_academique_id else None
        except (Communes.DoesNotExist, 
                CategorieFormation.DoesNotExist, 
                Etablissement.DoesNotExist, 
                Typementorat.DoesNotExist, 
                Niveau_formation.DoesNotExist,
                Cannaux_Connaissance.DoesNotExist,
                Frequence_Echange.DoesNotExist,
                Cannaux_Communication.DoesNotExist,
                Objectif_Accademique.DoesNotExist):
            
            # Gérer le cas où une des clés étrangères n'existe pas
            return HttpResponseBadRequest("Une ou plusieurs clés étrangères sont invalides")

        # Associer les objets aux clés étrangères s'ils existent
        if commune: user_act.commune = commune
        if domaine: user_act.domaine = domaine
        if etablissement: user_act.etablissement = etablissement
        if type_mentorat: user_act.type_mentorat = type_mentorat
        if niveau: user_act.niveau = niveau
        
        if connaissance: user_act.connaissance = connaissance
        if frequesce: user_act.frequesce = frequesce
        if cannau: user_act.cannaux = cannau
        if ojectif_academique: user_act.ojectif_academique = ojectif_academique
        
        # Sauvegarder le profil
        user_act.save()

        return redirect('user_profile')

    communes = Communes.objects.all()
    domaines = CategorieFormation.objects.all()
    etablissements = Etablissement.objects.all()
    types = Typementorat.objects.all()
    niveaux = Niveau_formation.objects.all()
    provinces = Provinces.objects.all()
    statuts = Status.objects.all()
    ojectifs = Objectif_Accademique.objects.all()
    cannaux = Cannaux_Communication.objects.all()
    frequesces = Frequence_Echange.objects.all()
    connaissances= Cannaux_Connaissance.objects.all()

    context = {
        "connaissances": connaissances,
        "frequesces": frequesces,
        "cannaux": cannaux,
        "ojectifs": ojectifs,
        "niveaux": niveaux,
        "types": types,
        "user_act": user_act,
        "communes": communes,
        "domaines": domaines,
        "etablissements": etablissements,
        "provinces": provinces,
        "statuts": statuts,
    }
    return render(request, 'mentors/editprofile.html', context)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def get_all_ressource(request):
    # Récupérer le profil de l'utilisateur connecté
    #user_profile = Profiles.objects.get(user=request.user)
    
    # Vérifier s'il a un mentor
    """ if user_profile.mentor:
        # Filtrer les ressources pour n'afficher que celles du mentor de l'utilisateur connecté
        ressources = Ressources.objects.filter(owner=user_profile.mentor.user)
    else:
        # Si l'utilisateur n'a pas de mentor, afficher toutes les ressources
        ressources = Ressources.objects.filter(owner=request.user) """
    ressources = Ressources.objects.all()
    context = {"ressources": ressources}
    return render(request, 'mentors/get_all_ressource.html', context)



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_all_even(request):
    # Récupérer le profil de l'utilisateur connecté
    """  user_profile = Profiles.objects.get(user=request.user)
    
    # Vérifier s'il a un mentor
    if user_profile.mentor:
        # Filtrer les evenements pour n'afficher que celles du mentor de l'utilisateur connecté
        evenements = Evenement.objects.filter(initiateur=user_profile.mentor.user)
    else:
        # Si l'utilisateur n'a pas de mentor, afficher toutes les evenements
        evenements = Evenement.objects.filter(initiateur=request.user) """
    evenements = Evenement.objects.all()
    context = {"evenements": evenements}
    return render(request, 'mentors/get_all_even.html', context)





@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_ressource(request):
    if request.method == 'POST':
        form = RessourcesForm(request.POST, request.FILES)
        if form.is_valid():
            ressource = form.save(commit=False)
            ressource.owner = request.user
            ressource.save()
            messages.success(request, "Nouvelle Ressource Ajoutée")
            return redirect('get_all_ressource')
    else:
        form = RessourcesForm()
    return render(request, 'mentors/add_ressource.html', {'form': form})



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_even(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            even = form.save(commit=False)
            even.initiateur = request.user
            even.save()

            # Envoyer un email à tous les utilisateurs
            subject = 'Nouveau Événement Ajouté'
            message = f'Un nouveau événement "{even.libelle}" a été ajouté par {even.initiateur.first_name} " " {even.initiateur.last_name}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = NewletterEmail.objects.values_list('useremail', flat=True)

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Nouveau Événement Ajouté et emails envoyés")
            except BadHeaderError:
                messages.error(request, "Erreur lors de l'envoi de l'email")
                return redirect('get_all_even')

            return redirect('get_all_even')
    else:
        form = EvenementForm()
    return render(request, 'mentors/add_even.html', {'form': form})






@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_forum(request):
    if request.method == 'POST':
        form = ForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.initiateur = request.user
            forum.save()
            messages.success(request, "Nouveau Forum Ajouté")
            return redirect('get_all_forum')
    else:
        form = ForumForm()
    return render(request, 'mentors/add_forum.html', {'form': form})





def add_comment(request, id):
    forum = Forum.objects.get(id=id)
    comments = ForumComment.objects.filter(forum=forum).order_by('-created')
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_comment = request.user
            comment.forum = forum
            comment.save()
            messages.info(request, 'Commentaire ajouté')
            return redirect('add_comment', id=id)
    else:
        form = CommentForm()
    return render(request, 'mentors/add_comment.html', {'form': form, 'forum': forum, 'page_obj': page_obj})



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_comment(request, id):
    comment = ForumComment.objects.get(id=id)
    
    # Vérifier si l'utilisateur actuel est l'auteur du commentaire
    if comment.user_comment != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce commentaire.")
        return redirect('add_comment', id=comment.forum.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Modification effectuée avec succès !")
            return redirect('add_comment', id=comment.forum.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'mentors/edit_comment.html', {'comment': comment, 'form': form})



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_all_forum(request):
    # Récupérer le profil de l'utilisateur connecté
    # user_profile = Profiles.objects.get(user=request.user)
    
    """ # Vérifier s'il a un mentor
    if user_profile.mentor:
        # Filtrer les forums pour n'afficher que celles du mentor de l'utilisateur connecté
        forums = Forum.objects.filter(initiateur=user_profile.mentor.user)
    else:
        # Si l'utilisateur n'a pas de mentor, afficher toutes les forums
        forums = Forum.objects.filter(initiateur=request.user) """
    forums = Forum.objects.all()
    context = {"forums": forums}
    return render(request, 'mentors/get_all_forum.html', context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def about(request):
    mots = Mot_du_Fondateur.objects.filter(statut='actif')
    presents = Presentation.objects.all().first()
    valeurs = Valeur.objects.all()
    categories = CategorieFormation.objects.all().order_by('-created')
    context = {"valeurs":valeurs, "categories":categories, "presents":presents, "mots":mots}
    return render(request, 'mentors/about.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def projet(request):
    projets = Projets.objects.all()
    context = {"projets":projets}
    return render(request, 'mentors/projet.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bourse_opportunite(request):
    bourses = Bourse_Opportinute.bourses_expirees()
    context = {'bourses':bourses}
    return render(request, 'mentors/bourse_opportunite.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Mentors(request):
    return HttpResponseRedirect(reverse('user_profile'))



# @login_required
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def Mentors(request):
#     if request.method == 'POST':
#         choix = request.POST.get('choix')
#         user = request.user
#         # Vérifier si l'utilisateur est déjà dans le groupe "utilisateurs"
#         if user.groups.filter(name='utilisateurs').exists():
#             messages.error(request, 'Vous êtes déja un mentoré')
#             return redirect('Mentors')
    
#         # Vérifier la valeur de l'input 'choix' et attribuer le groupe approprié
#         if choix == '1':
#             group_name = 'mentors'  
#         elif choix == '2':
#             group_name = 'utilisateurs'  
#         else:
#             group_name = '' 
#         # Récupérer ou créer le groupe
#         if group_name:  # S'assurer que le nom du groupe est défini
#             group, created = Group.objects.get_or_create(name=group_name)
#             # Ajouter l'utilisateur au groupe
#             user.groups.add(group)
#             return HttpResponseRedirect(reverse('user_profile'))
#         else:
#             return render(request, 'mentors/Mentors.html', {'error_message': 'Le choix n\'est pas valide'})
#     else:
#         # Récupérer le groupe "mentors"
#         mentors_group = Group.objects.get(name='mentors')
#         # Récupérer les utilisateurs qui sont dans le groupe "mentors"
#         mentors_users = mentors_group.user_set.all()
#         # Maintenant, vous pouvez récupérer les profils associés à ces utilisateurs
#         mentors_profiles = Profiles.objects.filter(user__in=mentors_users)
#         # Vérifier si l'utilisateur appartient au groupe 'mentors'
#         mentors_group = request.user.groups.filter(name='mentors').exists()
#         # Vérifier si l'utilisateur appartient au groupe 'utilisateurs'
#         user_group = request.user.groups.filter(name='utilisateurs').exists()
#         context = {'mentors_profiles': mentors_profiles, 'mentors_group': mentors_group, "user_group": user_group}
#         return render(request, 'mentors/Mentors.html', context)







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







def add_commune(request):
    if request.method == 'POST':
        nom_commune = request.POST.get('nom_commune')
        province_id = request.POST.get('province')
        try:
            # Vérifier si la province avec l'ID fourni existe
            province = Provinces.objects.get(id=province_id)
            # Créer une nouvelle instance de Commune avec les données reçues
            nouvelle_commune = Communes.objects.create(nom_commune=nom_commune, province=province)
            # Sauvegarder la nouvelle commune dans la base de données
            nouvelle_commune.save()
            # Rediriger l'utilisateur vers l'URL actuelle
            return HttpResponseRedirect('/')
        except Provinces.DoesNotExist:
            # Gérer le cas où la province avec l'ID fourni n'existe pas
            return HttpResponseBadRequest("La province sélectionnée est invalide")
        except Exception as e:
            # Gérer les autres exceptions éventuelles
            return HttpResponseBadRequest("Une erreur s'est produite lors de l'enregistrement de la commune : {}".format(str(e)))
    else:
        # Gérer le cas où la requête n'est pas de type POST
        return HttpResponseBadRequest("Cette vue ne prend en charge que les requêtes de type POST")




def add_etablissement(request):
    if request.method == 'POST':
        etablissement = request.POST.get('libelle')
        commune_id = int(request.POST.get('commune'))
        statut_id = int(request.POST.get('statut'))
        try:
            # Vérifier si la commune et le statut avec l'ID fourni existe
            commune = Communes.objects.get(id=commune_id)
            statut = Status.objects.get(id=statut_id)
            # Créer une nouvelle instance de Commune avec les données reçues
            nouvel_etablissement = Etablissement.objects.create(libelle=etablissement, statut=statut, commune=commune)
            # Sauvegarder la nouvelle commune dans la base de données
            nouvel_etablissement.save()
            # Rediriger l'utilisateur vers l'URL actuelle
            return HttpResponseRedirect('/')
        except Provinces.DoesNotExist:
            # Gérer le cas où la province avec l'ID fourni n'existe pas
            return HttpResponseBadRequest("La province sélectionnée est invalide")
        except Exception as e:
            # Gérer les autres exceptions éventuelles
            return HttpResponseBadRequest("Une erreur s'est produite lors de l'enregistrement de la commune : {}".format(str(e)))
    else:
        # Gérer le cas où la requête n'est pas de type POST
        return HttpResponseBadRequest("Cette vue ne prend en charge que les requêtes de type POST")
    
    



def faq(request):
    fqs = Faq.objects.all().order_by('id')
    context = {"fqs":fqs}
    return render(request, 'mentors/faq.html', context)



def search(request):
    context = {}
    return render(request, 'mentors/search.html', context)




def newletter(request):
    if request.method == 'POST':
        post_useremail = request.POST.get('email')
        if post_useremail:
            # Vérifier si l'email existe déjà
            if NewletterEmail.objects.filter(useremail=post_useremail).exists():
                messages.error(request, 'Cet email est déjà abonné.')
            else:
                new = NewletterEmail.objects.create(useremail=post_useremail)
                new.save()
                mail_person_newletter = MailsPersonnalisee.objects.filter(intituler='newsletter_abonnement').first()
                objet_abonnement = mail_person_newletter.objet if mail_person_newletter else 'Confirmation abonnement'
                message_abonnement = mail_person_newletter.message if mail_person_newletter else 'Vous êtes maintenant abonné à notre newsletter.'
                send_mail(
                    objet_abonnement,
                    message_abonnement,
                    settings.DEFAULT_FROM_EMAIL,
                    [post_useremail],
                    html_message=message_abonnement,
                    fail_silently=False,
                )
                messages.success(request, 'Abonnement réussi')
                return redirect('home')
        else:
            messages.error(request, 'Échec de l\'abonnement, veuillez vérifier votre email.')
    return redirect('home')





def equipe(request):
    equipes = Equipe.objects.all()
    context = {"equipes":equipes}
    return render(request, 'mentors/equipe.html', context)


def joint_us(request):
    context = {}
    return render(request, 'mentors/joint_us.html', context)


def storie(request):
    stories = Storie.objects.all()
    context = {"stories":stories}
    return render(request, 'mentors/storie.html', context)



def adesion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        motivation = request.POST.get('raison')
        if email and tel and motivation:
            # Vérifier si l'email existe déjà
            if Adession.objects.filter(email=email).exists():
                messages.warning(request, 'demande déja fait.')
                return redirect('joint_us')
            else:
                adde = Adession.objects.create(email=email, tel=tel, motivation=motivation)
                adde.save()
                send_mail(
                    'Confirmation de votre demaande',
                    'Votre demande pour nous rejoindre à été bien pris en compte.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message='Votre demande pour nous rejoindre à été bien pris en compte.',
                    fail_silently=False,
                )
                messages.success(request, 'Demande reussi!')
                return redirect('joint_us')
        else:
            messages.error(request, 'Échec , veuillez vérifier')
    return redirect('joint_us')





@login_required
def complete_profile(request):
    
    user_act = request.user.profiles

    if request.method == "POST":
        user_act.telephone = request.POST.get('telephone') if request.POST.get('telephone') else None
        user_act.profile = request.POST.get('profile') if request.POST.get('profile') else None
        user_act.objectif = request.POST.get('objectif')if request.POST.get('objectif') else None
        user_act.attente = request.POST.get('attente')  if request.POST.get('attente') else None
        user_act.village = request.POST.get('village') if request.POST.get('village') else None
        user_act.confirm_experience_mentore = request.POST.get('confirm_experience_mentore') if request.POST.get('confirm_experience_mentore') else None
        user_act.profile_mentorat = request.POST.get('profile_mentorat') if request.POST.get('profile_mentorat') else None
        user_act.objectif_terme = request.POST.get('objectif_terme') if request.POST.get('confirm_mentore') else None
        user_act.confirm_mentore = request.POST.get('confirm_mentore') if request.POST.get('confirm_mentore') else None
        user_act.poste_mentor = request.POST.get('poste_mentor') if request.POST.get('poste_mentor') else None
        user_act.secteur_mentor = request.POST.get('secteur_mentor') if request.POST.get('secteur_mentor') else None
        user_act.confirm_experience_mentor = request.POST.get('confirm_experience_mentor') if request.POST.get('confirm_experience_mentor') else None
        user_act.confirm_formation_mentore = request.POST.get('confirm_formation_mentore') if request.POST.get('confirm_formation_mentore') else None
        

        # Récupérer les IDs des clés étrangères
        niveau_id = int(request.POST.get('niveau')) if request.POST.get('niveau') else None
        commune_id = int(request.POST.get('commune')) if request.POST.get('commune') else None
        domaine_id = int(request.POST.get('domaine')) if request.POST.get('domaine') else None
        etablissement_id = int(request.POST.get('etablissement')) if request.POST.get('etablissement') else None
        type_mentorat_id = int(request.POST.get('type_mentorat')) if request.POST.get('type_mentorat') else None
        connaissance_id = int(request.POST.get('connaissance')) if request.POST.get('connaissance') else None
        frequesce_id = int(request.POST.get('frequesce')) if request.POST.get('frequesce') else None
        cannau_id = int(request.POST.get('cannau')) if request.POST.get('cannau') else None
        ojectif_academique_id = int(request.POST.get('ojectif_academique')) if request.POST.get('ojectif_academique') else None

        # Vérifier si les clés étrangères existent dans la base de données
        try:
            commune = Communes.objects.get(id=commune_id) if commune_id else None
            domaine = CategorieFormation.objects.get(id=domaine_id) if domaine_id  else None
            etablissement = Etablissement.objects.get(id=etablissement_id) if etablissement_id  else None
            type_mentorat = Typementorat.objects.get(id=type_mentorat_id) if type_mentorat_id  else None
            niveau = Niveau_formation.objects.get(id=niveau_id) if niveau_id  else None
            
            connaissance = Cannaux_Connaissance.objects.get(id=connaissance_id) if connaissance_id  else None
            frequesce = Frequence_Echange.objects.get(id=frequesce_id) if frequesce_id  else None
            cannau = Cannaux_Communication.objects.get(id=cannau_id) if cannau_id  else None
            ojectif_academique = Objectif_Accademique.objects.get(id=ojectif_academique_id) if ojectif_academique_id  else None
        except (Communes.DoesNotExist, 
                CategorieFormation.DoesNotExist, 
                Etablissement.DoesNotExist, 
                Typementorat.DoesNotExist, 
                Niveau_formation.DoesNotExist,
                Cannaux_Connaissance.DoesNotExist,
                Frequence_Echange.DoesNotExist,
                Cannaux_Communication.DoesNotExist,
                Objectif_Accademique.DoesNotExist):
            
            # Gérer le cas où une des clés étrangères n'existe pas
            return HttpResponseBadRequest("Une ou plusieurs clés étrangères sont invalides")

        # Associer les objets aux clés étrangères
        user_act.commune = commune
        user_act.domaine = domaine
        user_act.etablissement = etablissement
        user_act.type_mentorat = type_mentorat
        user_act.niveau = niveau
        
        user_act.connaissance = connaissance
        user_act.frequesce = frequesce
        user_act.cannaux = cannau
        user_act.ojectif_academique = ojectif_academique
        
        # Sauvegarder le profil
        user_act.save()
        # Vérifier si l'utilisateur courant appartient au groupe des mentors
        if request.user.groups.filter(name='mentors').exists():
            mail_welcome = MailsPersonnalisee.objects.filter(intituler='welcome_mentor').first()
        else:
            mail_welcome = MailsPersonnalisee.objects.filter(intituler='welcome_mentore').first()
        
        objet_inscription = mail_welcome.objet if mail_welcome else "Bienvenue sur OSER"
        message_inscription = mail_welcome.message if mail_welcome else "Bienvenue sur OSER"
        send_mail(
            objet_inscription,
             message_inscription,
             settings.DEFAULT_FROM_EMAIL,
             [request.user.email],
             html_message=message_inscription,
             fail_silently=False,
         )

        return redirect('Mentors')

    communes = Communes.objects.all()
    domaines = CategorieFormation.objects.all()
    etablissements = Etablissement.objects.all()
    types = Typementorat.objects.all()
    niveaux = Niveau_formation.objects.all()
    provinces = Provinces.objects.all()
    statuts = Status.objects.all()
    ojectifs = Objectif_Accademique.objects.all()
    cannaux = Cannaux_Communication.objects.all()
    frequesces = Frequence_Echange.objects.all()
    connaissances= Cannaux_Connaissance.objects.all()

    context = {
        "connaissances":connaissances,
        "frequesces":frequesces,
        "cannaux":cannaux,
        "ojectifs":ojectifs,
        "niveaux": niveaux,
        "types": types,
        "user_act": user_act,
        "communes": communes,
        "domaines": domaines,
        "etablissements": etablissements,
        "provinces":provinces,
        "statuts":statuts,
    }
    if request.user.groups.filter(name='mentors').exists():
        return render(request, 'mentors/complete_profile_mentor.html', context)
    return render(request, 'mentors/complete_profile_mentore.html', context)



@login_required
def demande_ment(request):
    # Vérifie si l'utilisateur a déjà une demande de mentorat en cours
    demande_existante = Mentorat.objects.filter(demandeur=request.user.profiles, statut__statut='demande').exists()
    
    if demande_existante:
        messages.warning(request, 'Vous avez déja une demande en cours patientez la validation est en cours')
         # Redirige ou affiche un message d'erreur
         # Remplacez par le nom de la vue appropriée ou affichez un message
        return redirect('home') 
    demande_existante = Mentorat.objects.filter(demandeur=request.user.profiles, statut__statut='valide').exists()
    if demande_existante:
        messages.warning(request, 'Vous avez déja une session en cours')
         # Redirige ou affiche un message d'erreur
         # Remplacez par le nom de la vue appropriée ou affichez un message
        return redirect('user_profile') 
   
    if request.method == 'POST':
        form = MentoratForm(request.POST)
        if form.is_valid():
            mentorat = form.save(commit=False)
            # Assurez-vous que le profil de l'utilisateur est accessible
            mentorat.demandeur = request.user.profiles
            # Récupère ou crée l'instance de MentoratStatut
            mentorat_statut, created = Mentorat_Statut.objects.get_or_create(statut='demande')
            # Assigner l'instance de MentoratStatut
            mentorat.statut = mentorat_statut  
            mentorat.save()
            # Remplacez 'home' par le nom de la vue à rediriger
            messages.success(request, 'Demande effectué avec succès')
            return redirect('home')
    else:
        form = MentoratForm()
    return render(request, 'mentors/demande_ment.html', {'form': form})




@login_required
def valider_mentorat(request, mentorat_id):
    mentorat = get_object_or_404(Mentorat, id=mentorat_id)
    if request.method == 'POST':
        form = MentoratValidationForm(request.POST, instance=mentorat)
        if form.is_valid():
            mentorat = form.save(commit=False)
            
            # Mise à jour du statut et assignation du mentor
            mentorat_statut, created = Mentorat_Statut.objects.get_or_create(statut='valide')
            mentorat.statut = mentorat_statut
            mentorat.mentor = form.cleaned_data['mentor']
            mentorat.date_debut = form.cleaned_data['date_debut']
            mentorat.date_fin = form.cleaned_data['date_fin']
            mentorat.save()

            # Vérification si le demandeur et le mentor ont des profils complets
            demandeur_profile = mentorat.demandeur
            mentor_profile = mentorat.mentor

            # Extraction sécurisée des données de profil du demandeur
            niveau = demandeur_profile.niveau.libelle if demandeur_profile.niveau else "Niveau non spécifié"
            objectif = demandeur_profile.objectif if demandeur_profile.objectif else "Objectif non spécifié"
            telephone = demandeur_profile.telephone if demandeur_profile.telephone else "Téléphone non spécifié"

            # Extraction des données du mentor
            poste_mentor = mentor_profile.poste_mentor if mentor_profile.poste_mentor else "Poste non spécifié"
            experience_mentor = mentor_profile.confirm_experience_mentor if mentor_profile.confirm_experience_mentor else "Expérience non spécifiée"
            telephone_mentor = mentor_profile.telephone if mentor_profile.telephone else "Téléphone non spécifié"

            # Préparation des emails
            objet = "Votre Jumelage de Mentorat est prêt !"

            # Format HTML avec justification
            message_mentor_html = format_html(f"""
            <div style="text-align: justify;">
            Chère/Cher {mentor_profile.user.first_name},<br><br>
            Nous avons le plaisir de vous annoncer que votre jumelage avec votre mentoré a été finalisé.<br>
            Vous allez accompagner {demandeur_profile.user.first_name} {demandeur_profile.user.last_name} dans son parcours académique et professionnel, 
            et nous sommes convaincus que votre expertise sera d'une grande valeur.<br><br>

            <b>Détails de votre Mentoré :</b><br>
            Nom : {demandeur_profile.user.last_name} {demandeur_profile.user.first_name}<br>
            Études/Parcours : {niveau}<br>
            Objectifs : {objectif}<br>
            Contact : {demandeur_profile.user.email}, {telephone}<br>
            Période : Du {mentorat.date_debut} au {mentorat.date_fin}<br><br>

            Nous vous encourageons à prendre contact avec votre mentoré pour organiser votre première rencontre. Voici un modèle de message que vous pouvez utiliser :<br><br>

            Bonjour [Nom du Mentoré],<br><br>

            Je m'appelle [Votre Nom] et je suis ravi(e) d'être jumelé(e) avec vous dans le cadre du programme de mentorat d'OSER. J'aimerais organiser notre première rencontre 
            pour discuter de vos objectifs et de la manière dont nous pourrions travailler ensemble.<br>
            Pouvez-vous me faire part de vos disponibilités pour une première discussion ?<br><br>

            Merci beaucoup et à bientôt,<br>
            [Votre Nom]<br><br>

            Avec nos meilleures salutations,<br>
            L’équipe de oser
            </div>
            """)

            message_mentore_html = format_html(f"""
            <div style="text-align: justify;">
            Chère/Cher {demandeur_profile.user.first_name},<br><br>
            Nous sommes ravis de vous informer que votre jumelage avec votre mentor a été finalisé !<br>
            Vous êtes maintenant prêt(e) à commencer cette excitante aventure de mentorat avec {mentor_profile.user.first_name} {mentor_profile.user.last_name}.<br><br>

            <b>Détails de votre Mentor :</b><br>
            Nom : {mentor_profile.user.first_name} {mentor_profile.user.last_name}<br>
            Poste : {poste_mentor}<br>
            Expérience : {experience_mentor}<br>
            Contact : {mentor_profile.user.email}, {telephone_mentor}<br>
            Période : Du {mentorat.date_debut} au {mentorat.date_fin}<br><br>

            Nous vous encourageons à prendre contact avec votre mentor dès que possible pour organiser votre première rencontre.<br>
            Vous pouvez utiliser le modèle de message ci-dessous pour initier la conversation.<br><br>

            Bonjour [Nom du Mentor],<br><br>

            Je m'appelle [Votre Nom] et je suis ravi(e) d'être jumelé(e) avec vous dans le cadre du programme de mentorat d'OSER.<br>
            J'aimerais organiser notre première rencontre pour discuter de mes objectifs et de la manière dont nous pourrions travailler ensemble.<br>
            Pouvez-vous me faire part de vos disponibilités pour une première discussion ?<br><br>

            Merci beaucoup et à bientôt,<br>
            [Votre Nom]<br><br>

            Avec nos meilleures salutations,<br>
            L’équipe de oser
            </div>
            """)

            # Envoi des emails avec HTML
            send_mail(
                objet,
                '',  # Le texte brut peut être vide si vous avez un message HTML
                settings.DEFAULT_FROM_EMAIL,
                [mentor_profile.user.email],
                fail_silently=False,
                html_message=message_mentor_html
            )
            send_mail(
                objet,
                '',  # Le texte brut peut être vide si vous avez un message HTML
                settings.DEFAULT_FROM_EMAIL,
                [demandeur_profile.user.email],
                fail_silently=False,
                html_message=message_mentore_html
            )

            messages.success(request, 'Le mentorat a été validé avec succès.')
            return redirect('boad')  # Redirection vers la vue appropriée après validation
    else:
        form = MentoratValidationForm(instance=mentorat)
    
    return render(request, 'mentors/valid_ment.html', {'form': form, 'mentorat': mentorat})







@login_required
def fermer_mentorat(request, mentorat_id):
    mentorat = get_object_or_404(Mentorat, id=mentorat_id)
    
    if request.method == 'POST':
        form = MentoratFrmerForm(request.POST, instance=mentorat)
        if form.is_valid():
            mentorat = form.save(commit=False)
            # Mise à jour du statut et assignation du statut 'fermé'
            mentorat_statut, created = Mentorat_Statut.objects.get_or_create(statut='fermer')
            mentorat.statut = mentorat_statut
            mentorat.save()
            messages.success(request, 'Session fermée')
            return redirect('boad')
    else:
        form = MentoratFrmerForm(instance=mentorat)
    
    return render(request, 'mentors/ferm_ment.html', {'form': form, 'mentorat': mentorat})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mails_personnalisee(request):
    mails = MailsPersonnalisee.objects.all()
    context = {"mails": mails}
    return render(request, 'mentors/dashboard/mails_personnaliser.html', context)




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mentore_activites(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    
    if user.is_superuser:
        activites = ActiviteMentorat.objects.all()
    else:
        activites = ActiviteMentorat.objects.filter(mentorat__mentor=request.user.profiles) or \
                    ActiviteMentorat.objects.filter(mentorat__demandeur=request.user.profiles)
                    
    context = {
        "activites": activites,
        "user_groups": user_groups,
    }
    
    return render(request, 'mentors/activites_mentorat.html', context)



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_activite(request):
    if request.method == "POST":
        form = ActiviteMentoratForm(request.POST, request.FILES)
        if form.is_valid():
            activite = form.save()
            mentorat = Mentorat.objects.filter(mentor=request.user.profiles).first()
            ActiviteMentorat.objects.filter(id=activite.id).update(mentorat=mentorat)
            messages.success(request, 'Activité ajoutée avec succès')
            return redirect('mentore_activites')
        return render(request, 'mentors/add_activites_mentorat.html', {'form': form})
    form = ActiviteMentoratForm()
    return render(request, 'mentors/add_activites_mentorat.html', {'form': form})




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_activite(request, id):
    activite = get_object_or_404(ActiviteMentorat, id=id)
    if request.method == "POST":
        form = ActiviteMentoratForm(request.POST, request.FILES, instance=activite)
        if form.is_valid():
            activite = form.save()
            if request.user.is_superuser:
                ActiviteMentorat.objects.filter(id=id).update(is_commun=True)
            messages.success(request, 'Activité modifiée avec succès')
            return redirect('mentore_activites')
        return render(request, 'mentors/edit_activites_mentorat.html', {'form': form})

    form = ActiviteMentoratForm(instance=activite)
    return render(request, 'mentors/edit_activites_mentorat.html', {'form': form})




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_activite(request, id):
    activite = get_object_or_404(ActiviteMentorat, id=id)
    activite.delete()
    messages.success(request, 'Activité supprimée avec succès')
    return redirect('mentore_activites')




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def annule_mentore_activite(request, id):
    ActiviteMentorat.objects.filter(id=id).update(etat='en_instance')
    messages.success(request, 'Activité annulée avec succès')
    return redirect('mentore_activites')




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def valid_mentore_activite(request, id):
    ActiviteMentorat.objects.filter(id=id).update(etat='en_cours')
    messages.success(request, 'Activité valide avec succès')
    return redirect('mentore_activites')




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def clos_mentore_activite(request, id):
    ActiviteMentorat.objects.filter(id=id).update(etat='cloture')
    messages.success(request, 'Activité clos avec succès')
    return redirect('mentore_activites')




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def factory_activite(activites):
    today = timezone.now().date()
    
    for activite in activites:
        if activite.debut <= today <= activite.fin and activite.etat != 'annuler':
            # Si la date actuelle est comprise entre la date de début et la date de fin
            if activite.etat != 'en_cours':  # Mettre à jour seulement si nécessaire
                activite.etat = 'en_cours'
                activite.save()
        elif today > activite.fin and  activite.etat != 'annuler':
            # Si la date actuelle est après la date de fin
            if activite.etat != 'cloture':  # Mettre à jour seulement si nécessaire
                activite.etat = 'cloture'
                activite.save()
                
                
                
