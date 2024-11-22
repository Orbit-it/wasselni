# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect
from datetime import date
from datetime import time
from django.urls import reverse
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Car




@csrf_exempt  # Permet les requêtes POST AJAX
def add_car_ajax(request):
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        marque = request.POST.get('marque')
        modele = request.POST.get('modele')
        places = request.POST.get('place')
        age = request.POST.get('age')

        # Vérifier les données reçues
        if matricule and marque and modele and places and age:
            # Ajouter la voiture dans la base de données
            car = Car.objects.create(
                car_matricule=matricule,
                car_marque=marque,
                car_modele=modele,
                car_nombre_place=int(places),
                car_age=int(age),
                owner = request.user
            )
            car.save()

            # Retourner une réponse JSON
            return JsonResponse({"message": "Voiture ajoutée avec succès", "status": "success",
                'matricule': matricule,
                'marque': marque,
                'places': places,
            })
        else:
            return JsonResponse({"message": "Données invalides", "status": "error"})
    return JsonResponse({"message": "Requête non valide", "status": "error"})

@csrf_exempt  # Permet les requêtes POST AJAX
def add_trajet_ajax(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        prix = request.POST.get('prix')
        passagers = request.POST.get('passagers')
        places = request.POST.get('nombre_places')
        heure = request.POST.get('heure')
        minute = request.POST.get('minute')
        jour = request.POST.get("jour") 
        mois = request.POST.get("mois") 
        annee = request.POST.get("annee")

        if jour and mois and annee:
            complete_date = date(int(annee), int(mois), int(jour))

        if heure and minute:
            complete_heure = time(int(heure), int(minute))    

        # Vérifier les données reçues
        if source and destination and prix and places and passagers and heure:
            # Ajouter la voiture dans la base de données
            trajet = Trajet.objects.create(
                source = source,
                destination = destination,
                price_per_seat = prix, 
                passengers_sex = passagers,
                bagage = request.user.bagage,
                date = complete_date,
                heure = complete_heure,
                driver = request.user,
                places = places,
                status = "Lancé",
            )
            trajet.save()

            # Retourner une réponse JSON
            return JsonResponse({"message": "Trajet ajouté avec succès", "status": "success"})
        else:
            return JsonResponse({"message": "Données invalides", "status": "error"})
    return JsonResponse({"message": "Requête non valide", "status": "error"})

# add Trip function

@csrf_exempt  # Permet les requêtes POST AJAX
def add_trip_ajax(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        prix = request.POST.get('prix')
        driver = request.POST.get('driver')
        heure_min = request.POST.get('heure_min')
        heure_max = request.POST.get('heure_max')
        jour = request.POST.get("jour") 
        mois = request.POST.get("mois") 
        annee = request.POST.get("annee")

        if jour and mois and annee:
            complete_date = date(int(annee), int(mois), int(jour))   

        # Vérifier les données reçues
        if source and destination and prix and driver and heure_min and heure_max:
            # Ajouter la voiture dans la base de données
            trip = Trip.objects.create(
                passenger = request.user,
                source = source,
                destination = destination,
                driver_sexe = driver,
                price_max = prix,
                date = complete_date,
                heure_min = heure_min,
                heure_max = heure_max,
                bagage = request.user.bagage
            )
            trip.save()

            # Retourner une réponse JSON
            return JsonResponse({"message": "Trip ajouté avec succès", "status": "success"})
        else:
            return JsonResponse({"message": "Données invalides", "status": "error"})
    return JsonResponse({"message": "Requête non valide", "status": "error"})



@login_required(login_url="/login/")
def index(request):

     # Objects for admin view =======================================================
    list_users = User.objects.all() 
    list_passenger = User.objects.filter(type = "Passenger")
    list_driver = User.objects.filter(type = "Driver")

    # End =====================================================================

    # Objects for users =======================================================
    trajets = Trajet.objects.filter(driver = request.user.id)
    trips = Trip.objects.filter(passenger = request.user.id)
    cars = Car.objects.filter(owner = request.user.id)
    user_cars = Car.objects.filter(owner=request.user)

    user_bagage = request.user.bagage

    
    user_abonnement = request.user.abonnement

    abonnement = user_abonnement.date_expiration > date.today()
    
    no_car = False
    if not user_cars:
        # Si l'utilisateur n'a pas de voiture, afficher un message d'erreur
        no_car = True
        car_places = 0
        place_options = 0
    else:    
        car = user_cars.first()
        car_places = car.car_nombre_place
        # Passer cette information au template sous forme de liste
        place_options = list(range(1, car_places + 1))


    # End =====================================================================

    
    context = {'segment': 'index',
            "list_users": list_users,
            "list_passenger": list_passenger,
            "list_driver": list_driver,
            "trajets": trajets,
            "trips": trips,
            "cars": cars,
            "no_car": no_car,
            'car_places': car_places,
            'place_options': place_options,
            'user_bagage': user_bagage,
            'abonnement': abonnement,
            'user_abonnement': user_abonnement,
           
               }

    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):

    context = {}


    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



@csrf_exempt
def add_trajet(request):
    if request.method == 'POST':
        driver = request.POST.get("driver"),
        source = request.POST.get("source"),
        destination = request.POST.get("destination"),
        price = request.POST.get("price"),
        date = request.POST.get("date"),
        heure = request.POST.get("heure"),
        passengers = request.POST.get("passengers"),

        Trajet.objects.create(
            driver = driver,
            source = source,
            destination = destination,
            price_per_seat = price,
            date = date,
            heure = heure,
            passengers_sex = passengers
        )    


@csrf_exempt
def update_bagage(request):
    if request.method == 'POST':
        bagage_type = request.POST.get('bagage')

        # Ensure bagage type is valid
        if not bagage_type:
            return JsonResponse({'status': 'error', 'message': 'Bagage type is required'}, status=400)

        # Update the user's bagage (assuming you have a user object)
        user = request.user
        user.bagage = bagage_type
        user.save()

        # Optionally, update the Trajet objects where the user is the driver
        Trajet.objects.filter(driver=user).exclude(status='complet').update(bagage=bagage_type)
        # Ooptionaly, update the Trip objects where the user is Passenger
        Trip.objects.filter(passenger=user).exclude(is_confirmed=True).update(bagage=bagage_type)


        return JsonResponse({'status': 'success', 'bagage': bagage_type})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)