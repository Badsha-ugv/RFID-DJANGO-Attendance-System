from django.urls import path 
from .views import * 

urlpatterns = [
    path('api/receive_card_data/', receive_card_data, name='receive_card_data'),
    path('',register_user,name='register_user'),
    path('api/add_user/', add_user, name='add_user'),
    path('api/get_user_info/', get_user_info, name='get_user_info'),
    # path('api/save_daily_log/', save_daily_log, name='save_daily_log'),
    path('api/daily_user_log/', daily_user_log, name='daily_user_log'),

    path('api/new_url_for_card_data/', new_url_for_card_data, name='new_url_for_card_data'),
    path('api/get_last_rfid_card/', get_last_rfid_card, name='get_last_rfid_card'),
]