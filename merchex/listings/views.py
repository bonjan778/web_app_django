from django.shortcuts import render, redirect
from django.http import HttpResponse
from listings.models import Band, Listing
from listings.forms import ContactUsForm, BandForm, ListingsForm
from django.core.mail import send_mail


def band_list(request):
    bands = Band.objects.all()
    return render(request,
                  'listings/band_list.html',
                  {'bands': bands})

def band_detail(request, id):
    band = Band.objects.get(id=id)
    return render(request,
                  "listings/band_detail.html",
                  {"band": band})

def band_create(request):
   if request.method == "POST":
       form = BandForm(request.POST)
       if form.is_valid():
           # Créer une nouvelle "Band" et la sauvegarder dans la DB
           band = form.save()
           # Redirige vers la page de détail du groupe que nous venons de créer
           # nous pouvons fournir les arguements du motif url  comme arguments à la fonction de redirection
           return redirect('band-detail', band.id)
   else:
       form = BandForm()

   return render(request,
            'listings/band_create.html',
            {'form': form})

def band_change(request, id):
    band = Band.objects.get(id=id)

    if request.method == "POST":
        form = BandForm(request.POST, instance=band)
        if form.is_valid():
            # Mettre à jour le groupe existant dans la DB
            form.save()
            # Rediriger vers la page détaillé du groupe
            return redirect("band-detail", band.id)
    else:
        form = BandForm(instance=band)

    return render(request,
                  'listings/band_update.html',
                  {"form": form})

def band_delete(request, id):
    band = Band.objects.get(id=id)

    if request.method == "POST":
        # Supprimer le groupe de la DB
        band.delete()
        # Rediriger vers la liste des groupes
        return redirect('band-list')

    return render(request,
                  'listings/band_delete.html',
                  {'band': band})

def about(request):
    return render(request,
                  'listings/about.html')


def listings_list(request):
    listing = Listing.objects.all()
    return render(request,
                  'listings/listings_list.html',
                  {'listing': listing})

def listings_detail(request, id):
    listing = Listing.objects.get(id=id)
    return render(request,
                  "listings/listings_detail.html",
                  {"listing": listing})

def listings_create(request):
    if request.method == 'POST':
        form = ListingsForm(request.POST)
        if form.is_valid():
            listing = form.save()
            return redirect('listings-detail', listing.id)
    else:
        form = ListingsForm()

    return render(request,
                  'listings/listings_create.html',
                  {"form": form})

def listings_change(request, id):
    listing = Listing.objects.get(id=id)

    if request.method == "POST":
        form = ListingsForm(request.POST, instance=listing)
        if form.is_valid():
            # Mettre à jour la liste existante dans la DB
            form.save()
            # Rediriger vers la page de la liste
            return redirect("listings-detail", listing.id)
    else:
        form = ListingsForm(instance=listing)

    return render(request,
                  'listings/listings_update.html',
                  {"form": form})

def listings_delete(request, id):
    listing = Listing.objects.get(id=id)

    if request.method == "POST":
        listing.delete()
        return redirect("listings-list")

    return render(request,
                  'listings/listings_delete.html',
                  {"listing": listing})

def contact(request):
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = ContactUsForm(request.POST)

        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@merchex.xyz'],
            )
            return redirect('email-sent')

    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).
    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm()

    return render(request,
                  'listings/contact.html',
                  {"form": form})

def email_sent(request):
    return render(request,
                  'listings/email_sent.html')

