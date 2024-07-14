from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
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
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    politiques = Politique_Securite.objects.all()
    temoignages = Temoignage.objects.all()
    partenariats = Partenaire.objects.all().order_by('-created')
    debut = Presentation.objects.all().first()
    slides = Slideimage.objects.all()
    thirty_days_ago = datetime.now() - timedelta(days=30)
    ressources = Ressources.objects.filter(created__gte=thirty_days_ago)
    #Récupérer les événements dont la date est postérieure à aujourd'hui
    activites = Activite.objects.all()
    #upcoming_events = Activite.objects.filter(date_even__gte=date.today()).order_by('date_even')
    
    data = Profiles.objects.all().exclude(niveau__isnull=True).values('niveau__libelle').annotate(user_count=Count('user')).order_by('niveau__libelle')
    levels = [entry['niveau__libelle'] for entry in data]
    counts = [entry['user_count'] for entry in data]
    
    context = {"data":data, "counts": counts, "levels": levels, "temoignages":temoignages, "politiques":politiques, "partenariats":partenariats, "debut":debut, "activites":activites, "slides":slides, "ressources":ressources}
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


    context = {"users_profiles":users_profiles,
               "mentorslists":mentorslists,
               "utilisateurs_connectes":utilisateurs_connectes,
               "nombre_utilisateurs_connectes":nombre_utilisateurs_connectes,
               "superadmins":superadmins, "sansmentores":sansmentores,
               "mentores":mentores, "mentors":mentors,
               "users":users,
               "demandes":demandes,
               }
    return render(request, 'mentors/boad.html', context)


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
        return HttpResponseRedirect(reverse('login'))
    
    
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
            return HttpResponseRedirect(reverse('login'))

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
        

        # Récupérer les IDs des clés étrangères
        niveau_id = int(request.POST.get('niveau'))
        commune_id = int(request.POST.get('commune'))
        domaine_id = int(request.POST.get('domaine'))
        etablissement_id = int(request.POST.get('etablissement'))
        type_mentorat_id = int(request.POST.get('type_mentorat'))
        connaissance_id = int(request.POST.get('connaissance'))
        frequesce_id = int(request.POST.get('frequesce'))
        cannau_id = int(request.POST.get('cannau'))
        ojectif_academique_id = int(request.POST.get('ojectif_academique'))

        # Vérifier si les clés étrangères existent dans la base de données
        try:
            commune = Communes.objects.get(id=commune_id)
            domaine = CategorieFormation.objects.get(id=domaine_id)
            etablissement = Etablissement.objects.get(id=etablissement_id)
            type_mentorat = Typementorat.objects.get(id=type_mentorat_id)
            niveau = Niveau_formation.objects.get(id=niveau_id)
            
            connaissance = Cannaux_Connaissance.objects.get(id=connaissance_id)
            frequesce = Frequence_Echange.objects.get(id=frequesce_id)
            cannau = Cannaux_Communication.objects.get(id=cannau_id)
            ojectif_academique = Objectif_Accademique.objects.get(id=ojectif_academique_id)
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
    presents = Presentation.objects.all().first()
    valeurs = Valeur.objects.all()
    categories = CategorieFormation.objects.all().order_by('-created')
    context = {"valeurs":valeurs, "categories":categories, "presents":presents}
    return render(request, 'mentors/about.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def projet(request):
    projets = Projets.objects.all()
    context = {"projets":projets}
    return render(request, 'mentors/projet.html', context)






@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Mentors(request):
    if request.method == 'POST':
        choix = request.POST.get('choix')
        user = request.user
        # Vérifier si l'utilisateur est déjà dans le groupe "utilisateurs"
        if user.groups.filter(name='utilisateurs').exists():
            messages.error(request, 'Vous êtes déja un mentoré')
            return redirect('Mentors')
    
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
            return HttpResponseRedirect(reverse('user_profile'))
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




""" @cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
    else:
        user_profile.mentor == mentor
        messages.warning(request, "vous avez déja un mentors")
        return redirect("user_profile") """
   


""" 
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
 """


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






@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def send_message(request):
    try:
        user_profile = Profiles.objects.get(user=request.user)
        #mentor_profile = user_profile.mentor
    except Profiles.DoesNotExist:
        # Gérer le cas où le profil de l'utilisateur n'existe pas
        messages.warning(request, "Verifier votre profile ou cherché un mentor")
        return redirect('home')

    """ if mentor_profile is None:
        # Gérer le cas où l'utilisateur n'a pas de mentor défini
        messages.warning(request, "Aucun mentor")
        return redirect('home') """

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            mentor_user = mentor_profile.user
            message = MessageMent.objects.create(sender=sender, recipient=mentor_user, content=content)
            # Ajouter le message à la boîte de réception du mentor
            recipient_inbox, created = Inbox.objects.get_or_create(user=mentor_user)
            recipient_inbox.messages.add(message)
            return redirect('message_thread')  # Rediriger vers la boîte de réception après l'envoi du message
    else:
        form = MessageForm()
    return render(request, 'mentors/send_message.html', {'form': form, 'mentor': mentor_profile})



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def send_message_to_users(request):
    try:
        mentor_profile = Profiles.objects.get(user=request.user)
    except Profiles.DoesNotExist:
        #Gérer le cas où le profil du mentor n'existe pas
        messages.warning(request, "Aucun mentor")
        return redirect('home')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            recipient_users = Profiles.objects.filter(mentor=mentor_profile)
            for user_profile in recipient_users:
                message = MessageMent.objects.create(sender=sender, recipient=user_profile.user, content=content)
                recipient_inbox, created = Inbox.objects.get_or_create(user=user_profile.user)
                recipient_inbox.messages.add(message)
            return redirect('mentor_messages')
    else:
        form = MessageForm()
    return render(request, 'mentors/send_message_to_users.html', {'form': form})



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def message_thread(request):
    try:
        user_profile = Profiles.objects.get(user=request.user)
        mentor_profile = user_profile.mentor
    except Profiles.DoesNotExist:
        # Gérer le cas où le profil de l'utilisateur n'existe pas
        messages.warning(request, "Verifier votre profile ou cherché un mentor")
        return redirect('home')

    if mentor_profile is None:
        # Gérer le cas où l'utilisateur n'a pas de mentor défini
        messages.warning(request, "Aucun mentor")
        return redirect('home')

    messages_sent = MessageMent.objects.filter(sender=user_profile.user, recipient=mentor_profile.user)
    messages_received = MessageMent.objects.filter(sender=mentor_profile.user, recipient=user_profile.user)
    #Concaténer les deux listes de messages et les trier par date de création
    mess = sorted(list(messages_sent) + list(messages_received), key=lambda msg: msg.timestamp)
    return render(request, 'mentors/message_thread.html', {'mess': mess, 'mentor_profile': mentor_profile})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mentor_messages(request):
    try:
        mentor_profile = Profiles.objects.get(user=request.user)
    except Profiles.DoesNotExist:
        # Gérer le cas où le profil du mentor n'existe pas
        messages.warning(request, "Aucun mentor")
        return redirect('home')

    user_profiles = Profiles.objects.filter(mentor=mentor_profile)
    
    # Récupérer à la fois les messages envoyés et reçus par le mentor
    messages_sent = MessageMent.objects.filter(sender=mentor_profile.user)
    messages_received = MessageMent.objects.filter(recipient=mentor_profile.user)
    mess = sorted(list(messages_sent) + list(messages_received), key=lambda msg: msg.timestamp)
    return render(request, 'mentors/mentor_messages.html', {'user_profiles': user_profiles, 'mess':mess})



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
    fqs = Faq.objects.all().order_by('-created')
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
                send_mail(
                    'Confirmation abonnement',
                    'Vous êtes maintenant abonné à notre newsletter.',
                    settings.DEFAULT_FROM_EMAIL,
                    [post_useremail],
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
                    fail_silently=False,
                )
                messages.success(request, 'Demande reussi!')
                return redirect('joint_us')
        else:
            messages.error(request, 'Échec , veuillez vérifier.')
    return redirect('joint_us')