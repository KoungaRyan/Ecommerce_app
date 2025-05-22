from django.shortcuts import render, redirect
from .models import Product, Commande
from django.core.paginator import Paginator
from shop.forms import  UserProfileForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Create your views here.
def index(request):
    product_object = Product.objects.all()
    item_name = request.GET.get('item-name')
    if item_name !='' and item_name is not None:
        product_object = Product.objects.filter(title__icontains = item_name)
    paginator = Paginator(product_object, 16)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)    
    return render(request, 'shop/index.html', {'product_object': product_object }) 

def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'shop/detail.html',{'product':product_object})

def checkout(request):
    if request.method == "POST":
        items = request.POST.get('items')
        total = request.POST.get('total')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode = request.POST.get('zipcode')
        com = Commande(items = items, total = total, nom=nom, email=email, address=address, ville=ville, pays=pays, zipcode=zipcode)
        com.save()
        return redirect('confirmation')

    return render(request, 'shop/checkout.html') 

def confirmation(request):
    info = Commande.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'shop/confirmation.html', {'name' : nom})


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)  # Formulaire pour l'utilisateur
        profile_form = UserProfileForm(request.POST)  # Formulaire pour les champs supplémentaires

        if user_form.is_valid() and profile_form.is_valid():
            # Crée l'utilisateur
            user = user_form.save()

            # Met à jour les champs supplémentaires du profil créé automatiquement
            profile = UserProfile.objects.get(user=user)  # Récupère le profil existant
            profile_form = UserProfileForm(request.POST, instance=profile)
            profile_form.save()  # Sauvegarde les données supplémentaires

                        
            # Ajoutez un message de succès
            messages.success(request, 'Votre compte a été créé avec succès !')
            

            return redirect('register')
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()

    return render(request, 'shop/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


