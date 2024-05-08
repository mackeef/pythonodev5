import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3

def kelime_sikliklari(metin):
    kelimeler = metin.split()
    sikliklar = {}
    for kelime in kelimeler:
        sikliklar[kelime] = sikliklar.get(kelime, 0) + 1
    return sikliklar

def benzerlik_orani(metin1, metin2):
    karakterler1 = list(metin1)
    karakterler2 = list(metin2)
    
    toplam1 = sum(ord(karakter) for karakter in karakterler1)
    toplam2 = sum(ord(karakter) for karakter in karakterler2)
    
    benzerlik_orani = 1 - abs(toplam1 - toplam2) / max(toplam1, toplam2)
    
    return benzerlik_orani

def benzerlik_orani2(metin1, metin2):
    # Adım 1: Metinleri kelimelere ayır ve kelime sıklıklarını hesapla
    sikliklar1 = kelime_sikliklari(metin1)
    sikliklar2 = kelime_sikliklari(metin2)
    
    # Adım 2: Her iki metnin kelime sıklıklarını karşılaştırarak benzerlik oranını hesapla
    ortak_kelimeler = 0
    toplam_kelimeler = 0
    
    # Metin 1'deki ortak kelimelerin sayısını hesapla
    for kelime, siklik in sikliklar1.items():
        if kelime in sikliklar2:
            ortak_kelimeler += min(siklik, sikliklar2[kelime])
        toplam_kelimeler += siklik
    
    # Metin 2'deki yeni kelimelerin sayısını ekle
    for kelime, siklik in sikliklar2.items():
        if kelime not in sikliklar1:
            toplam_kelimeler += siklik
    
    # Benzerlik oranını hesapla
    if toplam_kelimeler == 0:
        return 0
    benzerlik_orani2 = ortak_kelimeler / toplam_kelimeler
    
    return benzerlik_orani2

class Uygulama(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Kullanıcı Girişi")
        self.geometry("300x150")

        self.giris_ekrani()

    def giris_ekrani(self):
        self.label_kadi = tk.Label(self, text="Kullanıcı Adı:")
        self.label_kadi.grid(row=0, column=0, padx=10, pady=5)
        self.entry_kadi = tk.Entry(self)
        self.entry_kadi.grid(row=0, column=1, padx=10, pady=5)

        self.label_sifre = tk.Label(self, text="Şifre:")
        self.label_sifre.grid(row=1, column=0, padx=10, pady=5)
        self.entry_sifre = tk.Entry(self, show="*")
        self.entry_sifre.grid(row=1, column=1, padx=10, pady=5)

        self.giris_btn = tk.Button(self, text="Giriş Yap", command=self.giris)
        self.giris_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        self.kaydol_btn = tk.Button(self, text="Kaydol", command=self.kaydol)
        self.kaydol_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def giris(self):
        kullanici_adi = self.entry_kadi.get()
        sifre = self.entry_sifre.get()

        if self.kullanici_dogrulama(kullanici_adi, sifre):
            self.menu_ekrani(kullanici_adi)
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı!")

    def kaydol(self):
        kullanici_adi = self.entry_kadi.get()
        sifre = self.entry_sifre.get()

        if self.kullanici_kaydet(kullanici_adi, sifre):
            messagebox.showinfo("Başarılı", "Kullanıcı kaydedildi.")
        else:
            messagebox.showerror("Hata", "Kullanıcı zaten var!")

    def kullanici_dogrulama(self, kullanici_adi, sifre):
        baglanti = sqlite3.connect('veritabani.db')
        imlec = baglanti.cursor()
        imlec.execute("SELECT * FROM Kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        kullanici = imlec.fetchone()
        baglanti.close()

        if kullanici:
            return True
        else:
            return False

    def kullanici_kaydet(self, kullanici_adi, sifre):
        baglanti = sqlite3.connect('veritabani.db')
        imlec = baglanti.cursor()
        imlec.execute("SELECT * FROM Kullanicilar WHERE kullanici_adi=?", (kullanici_adi,))
        kullanici = imlec.fetchone()

        if kullanici:
            baglanti.close()
            return False

        imlec.execute("INSERT INTO Kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (kullanici_adi, sifre))
        baglanti.commit()
        baglanti.close()

        return True

    def menu_ekrani(self, kullanici_adi):
        self.destroy()
        menu = MenuEkrani(kullanici_adi)
        menu.mainloop()

class MenuEkrani(tk.Tk):
    def __init__(self, kullanici_adi):
        super().__init__()

        self.title("Menü")
        self.geometry("300x150")
        self.kullanici_adi = kullanici_adi

        self.menu_olustur()

    def menu_olustur(self):
        self.karsilastir_btn = tk.Button(self, text="Metin Karşılaştır", command=self.metin_karsilastir)
        self.karsilastir_btn.pack(pady=10)

        self.sifre_btn = tk.Button(self, text="Şifre Değiştir", command=self.sifre_degistir)
        self.sifre_btn.pack(pady=10)

        self.cikis_btn = tk.Button(self, text="Çıkış", command=self.cikis)
        self.cikis_btn.pack(pady=10)

    def metin_karsilastir(self):
        self.destroy()
        karsilastir = MetinKarsilastirEkrani()
        karsilastir.mainloop()

    def sifre_degistir(self):
        self.destroy()
        sifre_degistir = SifreDegistirEkrani(self.kullanici_adi)
        sifre_degistir.mainloop()

    def cikis(self):
        self.destroy()

class MetinKarsilastirEkrani(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Metin Karşılaştır")
        self.geometry("400x200")

        self.metin1_label = tk.Label(self, text="Metin 1 Dosyası:")
        self.metin1_label.grid(row=0, column=0, padx=10, pady=5)

        self.metin2_label = tk.Label(self, text="Metin 2 Dosyası:")
        self.metin2_label.grid(row=1, column=0, padx=10, pady=5)

        self.metin1_entry = tk.Entry(self, width=30)
        self.metin1_entry.grid(row=0, column=1, padx=10, pady=5)

        self.metin2_entry = tk.Entry(self, width=30)
        self.metin2_entry.grid(row=1, column=1, padx=10, pady=5)

        self.metin1_sec_btn = tk.Button(self, text="Dosya Seç", command=self.metin1_sec)
        self.metin1_sec_btn.grid(row=0, column=2, padx=5, pady=5)

        self.metin2_sec_btn = tk.Button(self, text="Dosya Seç", command=self.metin2_sec)
        self.metin2_sec_btn.grid(row=1, column=2, padx=5, pady=5)

        self.karsilastir_btn = tk.Button(self, text="Karşılaştır", command=self.karsilastir)
        self.karsilastir_btn.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        self.sonuc_label = tk.Label(self, text="")
        self.sonuc_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    def metin1_sec(self):
        dosya = filedialog.askopenfilename(filetypes=(("Metin Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")))
        self.metin1_entry.delete(0, tk.END)
        self.metin1_entry.insert(0, dosya)

    def metin2_sec(self):
        dosya = filedialog.askopenfilename(filetypes=(("Metin Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")))
        self.metin2_entry.delete(0, tk.END)
        self.metin2_entry.insert(0, dosya)

    def karsilastir(self):
        dosya1 = self.metin1_entry.get()
        dosya2 = self.metin2_entry.get()

        try:
            with open(dosya1, 'r', encoding='utf-8') as file1, open(dosya2, 'r', encoding='utf-8') as file2:
                metin1 = file1.read()
                metin2 = file2.read()

                benzerlik_oran = benzerlik_orani(metin1, metin2)
                benzerlik_oran2 = benzerlik_orani2(metin1, metin2)

                sonuc = f"Oran1 Benzerlik Oranı: {benzerlik_oran:.2f}\n"
                sonuc += f"Oran2 Benzerlik Oranı: {benzerlik_oran2:.2f}"

                self.sonuc_label.config(text=sonuc)
        except FileNotFoundError:
            messagebox.showerror("Hata", "Dosya bulunamadı!")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

class SifreDegistirEkrani(tk.Tk):
    def __init__(self, kullanici_adi):
        super().__init__()

        self.title("Şifre Değiştir")
        self.geometry("300x150")
        self.kullanici_adi = kullanici_adi

        self.label_eski_sifre = tk.Label(self, text="Eski Şifre:")
        self.label_eski_sifre.grid(row=0, column=0, padx=10, pady=5)
        self.entry_eski_sifre = tk.Entry(self, show="*")
        self.entry_eski_sifre.grid(row=0, column=1, padx=10, pady=5)

        self.label_yeni_sifre = tk.Label(self, text="Yeni Şifre:")
        self.label_yeni_sifre.grid(row=1, column=0, padx=10, pady=5)
        self.entry_yeni_sifre = tk.Entry(self, show="*")
        self.entry_yeni_sifre.grid(row=1, column=1, padx=10, pady=5)

        self.sifre_degistir_btn = tk.Button(self, text="Şifreyi Değiştir", command=self.sifre_degistir)
        self.sifre_degistir_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def sifre_degistir(self):
        eski_sifre = self.entry_eski_sifre.get()
        yeni_sifre = self.entry_yeni_sifre.get()

        baglanti = sqlite3.connect('veritabani.db')
        imlec = baglanti.cursor()

        imlec.execute("SELECT * FROM Kullanicilar WHERE kullanici_adi=? AND sifre=?", (self.kullanici_adi, eski_sifre))
        kullanici = imlec.fetchone()

        if kullanici:
            imlec.execute("UPDATE Kullanicilar SET sifre=? WHERE kullanici_adi=?", (yeni_sifre, self.kullanici_adi))
            baglanti.commit()
            baglanti.close()
            messagebox.showinfo("Başarılı", "Şifre değiştirildi.")
            self.destroy()
        else:
            baglanti.close()
            messagebox.showerror("Hata", "Eski şifre hatalı!")

if __name__ == "__main__":
    baglanti = sqlite3.connect('veritabani.db')
    imlec = baglanti.cursor()
    imlec.execute('''CREATE TABLE IF NOT EXISTS Kullanicilar
                 (kullanici_adi TEXT PRIMARY KEY, sifre TEXT)''')
    baglanti.commit()
    baglanti.close()

    uygulama = Uygulama()
    uygulama.mainloop()
