import requests
import time
from pymavlink import mavutil

# ArduPilot bağlantısı
master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

# Sunucu bilgileri
server_url = 'http://127.0.0.25:5000/api'
team_username = 'xxx'
team_password = 'xxx'
team_number = 12345

def login_to_server():
    login_data = {
        "kadi": "xxx",
        "sifre": "xxxx"
    }
    response = requests.post(f'{server_url}/giris', json=login_data)
    if response.status_code == 200:
        print("Giriş başarılı")
    elif response.status_code == 204:
        print("Gönderilen paketin Formatı Yanlış")
    elif response.status_code == 400:
        print("İstek hatalı veya geçersiz")
    elif response.status_code == 401:
        print("Kimliksiz erişim denemesi")
    elif response.status_code == 403:
        print("Yetkisiz erişim denemesi")
    elif response.status_code == 404:
        print("Geçersiz URL")
    elif response.status_code == 500:
        print("Sunucu içi hata")
    

def send_telemetry_data():
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    telemetry_data = {
        "takim_numarasi": 12345,
        "iha_enlem": msg.lat / 1e7,
        "iha_boylam": msg.lon / 1e7,
        "iha_irtifa": msg.alt / 1000,
        "IHA_dikilme": msg.pitch / 100,
        "IHA_yonelme": msg.yaw / 100,
        "IHA_yatis": msg.roll / 100,
        "IHA_hiz": msg.vx / 100,
        "IHA_batarya": msg.battery_remaining,
        "IHA_otonom": 1 if msg.autopilot == 1 else 0,  # Otonom mod kontrolü
        "iha_kilitlenme": 1 if msg.lock else 0,  # Kilitlenme bilgisi ????
        "hedef_merkez_X": 0,  # Örnek hedef merkez X koordinatı görüntüden alınacak (piksel)
        "hedef_merkez_Y": 0,  # Örnek hedef merkez Y koordinatı görüntüden alınacak (piksel)
        "hedef_genislik": 0,  # Örnek hedef genişlik görüntüden alınacak (piksel)
        "hedef_yukseklik": 0,  # Örnek hedef yükseklik görüntüden alınacak (piksel)
        "gps_saati": { #Gpsten alınıyor 
            "saat": msg.time_boot_ms // 1000 // 3600,
            "dakika": msg.time_boot_ms // 1000 % 3600 // 60,
            "saniye": msg.time_boot_ms // 1000 % 60,
            "milisaniye": msg.time_boot_ms % 1000
        }
    }
    response = requests.post(f'{server_url}/telemetri_gonder', json=telemetry_data)
    if response.status_code == 200:
        print("Telemetri verisi başarıyla gönderildi")
    else:
        print("Telemetri verisi gönderilemedi", response.status_code)

def send_kilitlenme_data(kilitlenme_data):
    response = requests.post(f'{server_url}/kilitlenme_bilgisi', json=kilitlenme_data)
    if response.status_code == 200:
        print("Kilitlenme verisi başarıyla gönderildi")
    else:
        print("Kilitlenme verisi gönderilemedi", response.status_code)

def send_kamikaze_data(kamikaze_data):
    response = requests.post(f'{server_url}/kamikaze_bilgisi', json=kamikaze_data)
    if response.status_code == 200:
        print("Kamikaze verisi başarıyla gönderildi")
    else:
        print("Kamikaze verisi gönderilemedi", response.status_code)

def get_server_time():
    response = requests.get(f'{server_url}/sunucusaati')
    if response.status_code == 200:
        return response.json()
    else:
        print("Sunucu saatine erişilemedi", response.status_code)

def get_qr_koordinat():
    response = requests.get(f'{server_url}/qr_koordinati')
    if response.status_code == 200:
        return response.json()
    else:
        print("QR kodu koordinatlarına erişilemedi", response.status_code)

def get_hss_koordinat():
    response = requests.get(f'{server_url}/hss_koordinatlari')
    if response.status_code == 200:
        return response.json()
    else:
        print("Hava savunma sistemi koordinatlarına erişilemedi", response.status_code)


# Örnek kullanım
if __name__ == "__main__":
    #giriş
    login_to_server()

    #telemetri gönderme
    send_telemetry_data()

    #kilitleme gönder
    kilitlenme_data = {
        "kilitlenmeBaslangicZamani": {
            "saat": 11,
            "dakika": 40,
            "saniye": 51,
            "milisaniye": 478
        },
        "kilitlenmeBitisZamani": {
            "saat": 11,
            "dakika": 41,
            "saniye": 3,
            "milisaniye": 141
        },
        "otonom_kilitlenme": 1
    }
    send_kilitlenme_data(kilitlenme_data)

    #kamikaze gönder
    kamikaze_data = {
        "kamikazeBaslangicZamani": {
            "saat": 11,
            "dakika": 44,
            "saniye": 13,
            "milisaniye": 361
        },
        "kamikazeBitisZamani": {
            "saat": 11,
            "dakika": 44,
            "saniye": 27,
            "milisaniye": 874
        },
        "qrMetni": "teknofest2024"
    }
    send_kamikaze_data(kamikaze_data)

    #sunucu saati alma
    print(get_server_time())

    #QR koordinatı alma
    print(get_qr_koordinat())

    #hss koordinatı alma
    print(get_hss_koordinat())


#Çalıştırma Yöntemi

#>>>>FastAPI Sunucusunu Çalıştırma:<<<<
#FastAPISERVER çalıştırmak için, terminalde aşağıdakileri yazılmalı
  #bash
  #Kodu kopyala
  #uvicorn fast_api_server:Myapp --reload
  #Örneğin, dosya adı server.py ise:fast_api_server yerine server olacaktı


#client kodunu çalıştırmak için, direk derle ya da
    #bash
    #Kodu kopyala
    #python client.py 
