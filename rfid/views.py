# views.py
from django.shortcuts import render 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import timedelta
from django.utils import timezone

from .models import RFIDCard, UserInfo, UserLog

@csrf_exempt  # Disable CSRF for simplicity. Ensure proper security measures in a production environment.
def receive_card_data(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        print('card is received, id is ',card_id) 
        
        # Process and save the card data as needed
        # Replace this with your actual implementation
        
        if card_id:
            RFIDCard.objects.create(card_number=card_id) 
            return JsonResponse({'msg':'card added'})
        else:
            return JsonResponse({'error':'no card number provided'},status=400)
        

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def register_user(request):
    return render(request,'register.html')

@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_id')
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Check if the card is already associated with a user
        existing_user = UserInfo.objects.filter(card_number=card_number).first()

        if existing_user:
            return JsonResponse({'status': 'error', 'message': 'Card already used by ' + existing_user.name})

        # Save user information to the database
        user_info = UserInfo.objects.create(card_number=card_number, name=name, email=email)
        user_info.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def get_last_rfid_card(request):
    last_card = RFIDCard.objects.last()
    if last_card:
        return JsonResponse({'card_number': last_card.card_number})
    else:
        return JsonResponse({'card_number': None})
    
def get_user_info(request):
    if request.method == 'GET':
        card_number = request.GET.get('card_number')
        user_info = UserInfo.objects.filter(card_number=card_number).first()

        if user_info:
            return JsonResponse({'status': 'success', 'user_info': {'name': user_info.name, 'email': user_info.email,'department':user_info.department,'contact':user_info.contact}})
        else:
            return JsonResponse({'status': 'error', 'message': 'User not found. Please register.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




@csrf_exempt
def new_url_for_card_data(request):
    card_data = request.POST.get('card_id')
    print('Received card data from the new URL:', card_data)

    try:
        # Check if the card_id exists in UserInfo
        user_info = UserInfo.objects.get(card_number=card_data)
        print('user info found',user_info) 
        # Check if there is an existing entry for today in UserLog
        today = timezone.now().date()
        existing_entry = UserLog.objects.filter(user=user_info, date=today).first()
        print('user exist',existing_entry) 
        if existing_entry:
            # 2nd swipe: Update leave time and save
            existing_entry.leave_time = timezone.now()
            existing_entry.save()
        else:
            # 1st swipe: Create a new entry with entry time
            new_entry = UserLog(user=user_info, entry_time=timezone.now(), date=today)
            print('new entry',new_entry) 
            new_entry.save()

        return JsonResponse({'status': 'success'})

    except UserInfo.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Card not registered.'})



def daily_user_log(request):
    today = timezone.now().date()
    user_log_entries = UserLog.objects.filter(date=today)

    log_list = []
    for entry in user_log_entries:
        stay_time = entry.stay_time.total_seconds() // 60 if entry.stay_time else None
        log_list.append({
            'user': entry.user.name,
            'card_id': entry.user.card_number,
            'date': entry.date,
            'entry_time': entry.entry_time.strftime('%H:%M:%S'),
            'leave_time': entry.leave_time.strftime('%H:%M:%S') if entry.leave_time else '',
            'stay_time': stay_time
        })

    return JsonResponse({'log_list': log_list})