import json
import datetime

class Musteri:
    def __init__(self, musteri_id, ad, telefon, ulke, notlar, eklenme_tarihi=None, borc=0.0):
        self.musteri_id = musteri_id
        self.ad = ad
        self.telefon = telefon
        self.ulke = ulke
        self.notlar = notlar
        self.eklenme_tarihi = eklenme_tarihi if eklenme_tarihi else datetime.datetime.now().isoformat()
        self.borc = borc

    def to_dict(self):
        return {
            "musteri_id": self.musteri_id,
            "ad": self.ad,
            "telefon": self.telefon,
            "ulke": self.ulke,
            "notlar": self.notlar,
            "eklenme_tarihi": self.eklenme_tarihi,
            "borc": self.borc
        }

class CRM:
    def __init__(self):
        self.musteriler = []
        self.sonraki_id = 1
        self.dosyadan_yukle()

    def dosyadan_yukle(self):
        try:
            with open("musteriler.json", "r") as dosya:
                veri = json.load(dosya)
                self.musteriler = [Musteri(**m) for m in veri["musteriler"]]
                self.sonraki_id = veri["sonraki_id"]
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Dosya bozuk veya hatalı formatta. Yeni dosya oluşturulacak.")
            self.musteriler = []
            self.sonraki_id = 1

    def dosyaya_kaydet(self):
        with open("musteriler.json", "w") as dosya:
            veri = {
                "musteriler": [m.to_dict() for m in self.musteriler],
                "sonraki_id": self.sonraki_id
            }
            json.dump(veri, dosya, indent=4)

    def musteri_ekle(self, ad, telefon, ulke, notlar, borc):
        musteri = Musteri(self.sonraki_id, ad, telefon, ulke, notlar, borc=borc)
        self.musteriler.append(musteri)
        self.sonraki_id += 1
        self.dosyaya_kaydet()
        print(f"Müşteri eklendi: {musteri.ad}")

    def musterileri_listele(self):
        return self.musteriler

    def musteri_sil(self, musteri_id):
        for musteri in self.musteriler:
            if musteri.musteri_id == musteri_id:
                self.musteriler.remove(musteri)
                self.dosyaya_kaydet()
                print(f"Müşteri silindi: {musteri.ad}")
                return
        print("Müşteri bulunamadı.")

    def musteri_ara(self, arama_terimi):
        sonuclar = [musteri for musteri in self.musteriler if arama_terimi.lower() in musteri.ad.lower() or arama_terimi.lower() in musteri.telefon.lower()]
        if sonuclar:
            return sonuclar
        else:
            return []

    def musteri_guncelle(self, musteri_id, ad=None, telefon=None, ulke=None, notlar=None, borc=None):
        for musteri in self.musteriler:
            if musteri.musteri_id == musteri_id:
                if ad:
                    musteri.ad = ad
                if telefon:
                    musteri.telefon = telefon
                if ulke:
                    musteri.ulke = ulke
                if notlar:
                    musteri.notlar = notlar
                if borc is not None:
                    musteri.borc = borc
                self.dosyaya_kaydet()
                print(f"Müşteri güncellendi: {musteri.ad}")
                return
        print("Müşteri bulunamadı.")
