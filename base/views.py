from django.shortcuts import render
from .models import CitizenCard, PensionApplication
from django.http import JsonResponse
from .web3_config import contract, w3, owner_address, private_key
import random
import json

# Create your views here.
def save_wallet(request):
    if request.method == "POST":
        data = json.loads(request.body)
        wallet = data.get("wallet")

        # Save in session (simple way)
        request.session['wallet'] = wallet

        print("Wallet saved:", wallet)

        return JsonResponse({"status": "success"})


def home(request):
    request.session['application_submitted'] = False
    return render(request, 'transperancy_dashboard.html')


def pension_status(request):
    application_submitted = request.session.get('application_submitted', False)
    print("SET SESSION:", request.session.get('application_submitted'))
    context = {
        'application_submitted': application_submitted
    }
    return render(request, 'my-pension-status.html', context)

def send_otp(request):
    if request.method == 'POST':
        aadhaar_number = request.POST.get('aadhaar_number')
        # Here you would add logic to send the OTP to the user's registered mobile number
        # For demonstration, we will just return a success message
        request.session['aadhaar_number'] = aadhaar_number  # Store Aadhaar number in session for later verification
        context = {
            'otp_sent': True,
            'aadhaar_number': aadhaar_number
        }
        return render(request, 'apply-pension.html', context)
    
    return render(request, 'apply-pension.html', {'otp_sent': False})

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        aadhaar = request.POST.get('aadhaar_number')



        if otp == '123456':

            user_data = CitizenCard.objects.filter(card_number=aadhaar).first()

            return render(request, 'apply-pension.html', {
                'verified': True,
                'user_data': user_data
            })

        return render(request, 'apply-pension.html', {
            'otp_sent': True,
            'aadhaar_number': aadhaar,
            'error': 'Invalid OTP'
        })



def register_on_blockchain(user_wallet, age, pension_type,is_married, is_disabled):

    user_wallet = w3.to_checksum_address(user_wallet)

    nonce = w3.eth.get_transaction_count(owner_address)

    txn = contract.functions.registerUser(
        user_wallet,
        age,
        pension_type,
        is_married,
        is_disabled,
    ).build_transaction({
        'from': owner_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    return w3.to_hex(tx_hash)

def apply_pension(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        pension_type = request.POST.get('pension_type')

        application_id = 'APP' + random.randint(100000, 999999).__str__()

        citizen_card = request.session.get('aadhaar_number', 'Unknown')
        if not citizen_card:
            return JsonResponse({"error": "Session expired. Please verify Aadhaar again."})
        citizen_obj = CitizenCard.objects.get(card_number=citizen_card)
        
        print(citizen_card)
        PensionApplication.objects.create(
            application_id=application_id,
            citizen_card=citizen_obj,
            pension_type=pension_type,
        )


        context = {
            'success': True,
            'application_id': application_id,
            'application_submitted': True   # IMPORTANT for hiding form
        }

        pension_map = {
            "old_age": 1,
            "widow": 2,
            "disability": 3
        }

        pension_value = pension_map.get(pension_type, 0)

        age = citizen_obj.age
        widow_status = citizen_obj.is_widow
        disability_status = citizen_obj.is_disabled

        # Example wallet (you should store this in DB)
        user_wallet = request.session.get('wallet')
        print("User wallet from session:", user_wallet)
        if not user_wallet:
            return JsonResponse({"error": "Wallet not connected"})
        
        print("User wallet from session:", user_wallet)
        tx_hash = register_on_blockchain(
            user_wallet,
            age,
            pension_value,
            widow_status,
            disability_status,
        )
        
        request.session['aadhaar_number'] = None
        request.session['application_submitted'] = True

        print("Blockchain TX:", tx_hash)

        return render(request, 'apply-pension.html', context)
    return render(request, 'apply-pension.html', {'otp_sent': False})



def get_dashboard_stats(request):
    try:
        stats = contract.functions.getDashboardStats().call()
        print("Stats from contract:", stats)
        print("Length:", len(stats))
        total_fund = stats[0]
        remaining_fund = stats[1]
        active_users = stats[2]
        total_claimed = stats[3]

        events = contract.events.PensionClaimed.get_logs(
            from_block=0,
            to_block='latest'
        )

        tx_list = []
        for e in events[-5:]:  # last 5 tx
            tx_list.append({
                "user": e['args']['user'],
                "amount": w3.from_wei(e['args']['amount'], 'ether'),
                "txHash": e['transactionHash'].hex()
            })

        return JsonResponse({
            "totalFund": float(w3.from_wei(total_fund, 'ether')),
            "remainingFund": float(w3.from_wei(remaining_fund, 'ether')),
            "totalClaimed": float(w3.from_wei(total_claimed, 'ether')),
            "activeUsers": active_users,
            "transactions": tx_list
        })

    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({"error": "Failed to fetch stats"})

def claim_pension(request):
    return JsonResponse({"status": "Use MetaMask for claiming"})