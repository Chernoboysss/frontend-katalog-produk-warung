from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse


def index(request):
    # Endpoint backend Express.js
    api_url = "http://localhost:3000/products/all"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()  # Asumsikan backend mengembalikan data JSON
        products = data.get('products', [])  # Ambil list produk dari JSON response

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        products = []  # Jika gagal, tampilkan data kosong

    return render(request, 'frontend/index.html', {'products': products})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email atau password tidak boleh kosong!')
            return render(request, 'frontend/login.html')

        # Kirim permintaan login ke backend (API backend di server lain)
        api_url = 'http://localhost:3000/auth/login'
        response = requests.post(api_url, json={'email': email, 'password': password})

        if response.status_code == 200:
            token = response.json().get('token')
            response = JsonResponse({'message': 'Login berhasil!', 'token': token})
            return response
        else:
            messages.error(request, 'Email atau password salah!')
    
    return render(request, 'frontend/login.html')


def dashboard(request):
    return render(request, 'frontend/dashboard.html')

def logout(request):
    # Hapus token dari session
    if 'token' in request.session:
        del request.session['token']
    return redirect('login')