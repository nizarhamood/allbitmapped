from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# Create your views here.
def index(request): 
    return render(request, 'index.html') # Will look for the index.html in the templates folder

def coins(request):
    return render(request, 'coins.html') # Will look for the portfolio details.html in the templates folder

def blockchain(request):
    return render(request, 'blockchain.html') # Will look for the blockchain.html in the templates folder

def nft(request):
    return render(request, 'nft.html') # Will look for the nft.html in the templates folder

def defi(request):
    return render(request, 'defi.html') # Will look for the defi.html in the templates folder

def exchanges(request):
    return render(request, 'exchanges.html') # Will look for the exchanges.html in the templates folder

def global_stats(request):
    return render(request, 'global_stats.html') # Will look for the global_stats.html in the templates folder

def fin_indexes(request):
    return render(request, 'fin_indexes.html') # Will look for the fin_indexes.html in the templates folder

def markets(request):
    return render(request, 'markets.html') # Will look for the markets.html in the templates folder

def sign_up(request):
    return render(request, 'sign_up.html') # Will look for the sign_up.html in the templates folder
