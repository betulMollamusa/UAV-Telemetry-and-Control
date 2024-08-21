from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

Myapp = FastAPI()

class Kullanici(BaseModel):
    kadi: str
    sifre: str 

class SunucuSaati(BaseModel):
    gun: int
    saat: int
    dakika: int
    saniye: int
    milisaniye: int

class GpsSaati(BaseModel):
    saat: int
    dakika: int
    saniye: int
    milisaniye: int

class TelemetryData(BaseModel):
    takim_numarasi: int
    iha_enlem: float
    iha_boylam: float
    iha_irtifa: float
    iha_dikilme: float
    iha_yonelme: float
    iha_yatis: float
    iha_hiz: float
    iha_batarya: float
    iha_otonom: int
    iha_kilitlenme: int
    hedef_merkez_X: float
    hedef_merkez_Y: float
    hedef_genislik: float
    hedef_yukseklik: float
    gps_saati: GpsSaati

class KilitlenmeData(BaseModel):
    kilitlenmeBaslangicZamani: SunucuSaati
    kilitlenmeBitisZamani: SunucuSaati
    otonom_kilitlenme: int

class KamikazeData(BaseModel):
    kamikazeBaslangicZamani: SunucuSaati
    kamikazeBitisZamani: SunucuSaati
    qrMetni: str

class QRKoordinat(BaseModel):
    qrEnlem: float
    qrBoylam: float

class HSSKoordinat(BaseModel):
    id: int
    hssEnlem: float
    hssBoylam: float
    hssYaricap: float

class HSSData(BaseModel):
    sunucusaati: SunucuSaati
    hss_koordinat_bilgileri: List[HSSKoordinat]

@Myapp.post("/api/giris")
def giris(data: Dict[str, str]):
    return {"message": "Giriş başarılı"}

@Myapp.post("/api/telemetri_gonder")
def telemetri_gonder(data: TelemetryData):
    return {"message": "Telemetri verisi başarıyla alındı"}

@Myapp.post("/api/kilitlenme_bilgisi")
def kilitlenme_gonder(data: KilitlenmeData):
    return {"message": "Kilitlenme verisi başarıyla alındı"}

@Myapp.post("/api/kamikaze_bilgisi")
def kamikaze_gonder(data: KamikazeData):
    return {"message": "Kamikaze verisi başarıyla alındı"}

@Myapp.get("/api/sunucusaati")
def sunucusaati():
    return SunucuSaati(gun=1, saat=12, dakika=0, saniye=0, milisaniye=0)

@Myapp.get("/api/qr_koordinati")
def qr_koordinat():
    return QRKoordinat(qrEnlem=41.51238882, qrBoylam=36.11935778)

@Myapp.get("/api/hss_koordinatlari")
def hss_koordinat():
    return HSSData(
        sunucusaati=SunucuSaati(gun=19, saat=15, dakika=51, saniye=43, milisaniye=775),
        hss_koordinat_bilgileri=[
            HSSKoordinat(id=0, hssEnlem=40.23260922, hssBoylam=29.00573015, hssYaricap=50),
            HSSKoordinat(id=1, hssEnlem=40.23351019, hssBoylam=28.99976492, hssYaricap=50),
            HSSKoordinat(id=2, hssEnlem=40.23105297, hssBoylam=29.00744677, hssYaricap=75),
            HSSKoordinat(id=3, hssEnlem=40.23090554, hssBoylam=29.00221109, hssYaricap=150)
        ]
    )
