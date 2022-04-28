from django.urls import path
from . import views
from dashboard.dash_apps.finished_apps.coins_component import app


# URL patterns are in alphabetical order
urlpatterns = [
    path('', views.index, name = 'index'),
    path('blockchain', views.blockchain, name = 'blockchain'),
    path('coins', views.coins, name = 'coins'),
    path('defi', views.defi, name = 'defi'),
    path('exchanges', views.exchanges, name = 'exchanges'),
    path('fin_indexes', views.fin_indexes, name = 'fin_indexes'),        
    path('global_stats', views.global_stats, name = 'global_stats'),
    path('markets', views.markets, name = 'markets'),
    path('nft', views.nft, name = 'nft'),
    path('sign_up', views.sign_up, name = 'sign_up'),
]