"""
Collatz Dizilerinde Dengeli Sayı Üreteci

Bu algoritma, Collatz varsayımına göre diziler üretirken
0 (çift sayılar) ve 1 (tek sayılar) işlemlerinin sayısını
olabildiğince eşit tutan rastgele sayılar üretir.

Collatz Varsayımı:
- Başlangıç sayısı n olsun
- n çift ise: n = n / 2
- n tek ise: n = 3n + 1
- n = 1 olana kadar devam et

Bu algoritma, Collatz dizilerindeki çift ve tek adımların
dengesini optimize eden sayıları bulur.
"""

import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict
import json
import time


class CollatzDengeliUretici:
    """
    Collatz dizilerinde dengeli sayılar üreten sınıf.
    
    Attributes:
        min_sayi (int): Üretilecek minimum sayı
        max_sayi (int): Üretilecek maksimum sayı
        denge_esigi (float): Kabul edilebilir denge eşiği
        istatistikler (Dict): Üretim istatistikleri
    """
    
    def __init__(self, min_sayi: int = 1, max_sayi: int = 10000, denge_esigi: float = 0.7):
        """
        Dengeli sayı üreteci başlatıcı.
        
        Args:
            min_sayi: Üretilecek minimum sayı değeri
            max_sayi: Üretilecek maksimum sayı değeri
            denge_esigi: Denge kabul eşiği (0-1 arası, düşük değer daha sıkı)
        """
        self.min_sayi = min_sayi
        self.max_sayi = max_sayi
        self.denge_esigi = denge_esigi
        self.istatistikler = {
            'toplam_deneme': 0,
            'kabul_edilen': 0,
            'reddedilen': 0,
            'baslama_zamani': time.time(),
            'tamamlanma_zamani': None,
            'uretilen_sayilar': []
        }
    
    def collatz_dizisi(self, n: int) -> List[int]:
        """
        Bir sayının Collatz dizisini hesaplar.
        
        Args:
            n: Başlangıç sayısı
            
        Returns:
            Collatz dizisi listesi
        """
        dizi = []
        while n != 1:
            dizi.append(n)
            if n % 2 == 0:  # Çift sayı
                n = n // 2
            else:  # Tek sayı
                n = 3 * n + 1
        dizi.append(1)  # Sonunda her zaman 1'e ulaşır
        return dizi
    
    def dizideki_0_1_dengesi(self, dizi: List[int]) -> Tuple[int, int, float]:
        """
        Collatz dizisindeki çift (0) ve tek (1) adımların dengesini hesaplar.
        
        Args:
            dizi: Collatz dizisi
            
        Returns:
            (cift_sayisi, tek_sayisi, denge_orani) tuple'ı
        """
        cift_sayisi = 0
        tek_sayisi = 0
        
        for i in range(len(dizi) - 1):
            if dizi[i] % 2 == 0:  # Çift sayı (0)
                cift_sayisi += 1
            else:  # Tek sayı (1)
                tek_sayisi += 1
        
        # Denge oranı: 1'e ne kadar yakınsa o kadar dengeli
        toplam = cift_sayisi + tek_sayisi
        if toplam > 0:
            denge_orani = abs(cift_sayisi - tek_sayisi) / toplam
        else:
            denge_orani = 1.0
        
        return cift_sayisi, tek_sayisi, denge_orani
    
    def dengeli_sayi_uret(self, adet: int = 100) -> Tuple[List[int], List[float], List[int], List[int]]:
        """
        Dengeli rastgele sayılar üretir.
        
        Args:
            adet: Üretilecek sayı adedi
            
        Returns:
            (sayilar, denge_oranlari, cift_adimlar, tek_adimlar) tuple'ı
        """
        dengeli_sayilar = []
        denge_oranlari = []
        cift_adimlar = []
        tek_adimlar = []
        
        print(f"Collatz Dengeli Sayı Üreteci Başlatıldı")
        print(f"Parametreler: Sayı aralığı [{self.min_sayi}, {self.max_sayi}], Hedef: {adet} sayı")
        print(f"Denge eşiği: {self.denge_esigi}")
        print("-" * 50)
        
        self.istatistikler['baslama_zamani'] = time.time()
        
        try:
            while len(dengeli_sayilar) < adet:
                # Rastgele bir sayı üret
                sayi = random.randint(self.min_sayi, self.max_sayi)
                self.istatistikler['toplam_deneme'] += 1
                
                # Collatz dizisini hesapla
                dizi = self.collatz_dizisi(sayi)
                
                # 0 ve 1 dengesini ölç
                cift, tek, denge_orani = self.dizideki_0_1_dengesi(dizi)
                
                # Kabul kriteri
                if denge_orani <= self.denge_esigi:
                    dengeli_sayilar.append(sayi)
                    denge_oranlari.append(denge_orani)
                    cift_adimlar.append(cift)
                    tek_adimlar.append(tek)
                    self.istatistikler['kabul_edilen'] += 1
                    
                    # İlerleme göstergesi
                    if self.istatistikler['kabul_edilen'] % max(1, adet // 10) == 0:
                        ilerleme = self.istatistikler['kabul_edilen'] / adet * 100
                        print(f"  İlerleme: %{ilerleme:.1f} ({self.istatistikler['kabul_edilen']}/{adet})")
                else:
                    self.istatistikler['reddedilen'] += 1
            
            self.istatistikler['tamamlanma_zamani'] = time.time()
            self.istatistikler['uretilen_sayilar'] = dengeli_sayilar.copy()
            
        except KeyboardInterrupt:
            print("\nKullanıcı tarafından durduruldu.")
            self.istatistikler['tamamlanma_zamani'] = time.time()
        
        # İstatistikleri yazdır
        self._istatistikleri_yazdir()
        
        return dengeli_sayilar, denge_oranlari, cift_adimlar, tek_adimlar
    
    def _istatistikleri_yazdir(self):
        """Üretim istatistiklerini yazdırır."""
        sure = self.istatistikler['tamamlanma_zamani'] - self.istatistikler['baslama_zamani']
        
        print("\n" + "="*50)
        print("ÜRETİM İSTATİSTİKLERİ")
        print("="*50)
        print(f"Toplam süre: {sure:.2f} saniye")
        print(f"Toplam deneme: {self.istatistikler['toplam_deneme']}")
        print(f"Kabul edilen: {self.istatistikler['kabul_edilen']}")
        print(f"Reddedilen: {self.istatistikler['reddedilen']}")
        
        if self.istatistikler['toplam_deneme'] > 0:
            kabul_orani = self.istatistikler['kabul_edilen'] / self.istatistikler['toplam_deneme'] * 100
            print(f"Kabul oranı: %{kabul_orani:.2f}")
        
        if self.istatistikler['kabul_edilen'] > 0:
            hiz = self.istatistikler['toplam_deneme'] / sure if sure > 0 else 0
            print(f"Ortalama hız: {hiz:.1f} deneme/saniye")
    
    def istatistikleri_kaydet(self, dosya_adi: str = "collatz_istatistikler.json"):
        """
        İstatistikleri JSON formatında kaydeder.
        
        Args:
            dosya_adi: Kaydedilecek dosya adı
        """
        kayit_verisi = {
            'parametreler': {
                'min_sayi': self.min_sayi,
                'max_sayi': self.max_sayi,
                'denge_esigi': self.denge_esigi
            },
            'istatistikler': self.istatistikler.copy(),
            'zaman_damgasi': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Liste verilerini dönüştür
        kayit_verisi['istatistikler']['uretilen_sayilar'] = self.istatistikler['uretilen_sayilar']
        
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            json.dump(kayit_verisi, f, indent=4, ensure_ascii=False)
        
        print(f"\nİstatistikler '{dosya_adi}' dosyasına kaydedildi.")


def sonuclari_goruntule(sayilar: List[int], denge_oranlari: List[float], 
                       cift_adimlar: List[int], tek_adimlar: List[int]):
    """
    Üretilen sayıların istatistiklerini görselleştirir.
    
    Args:
        sayilar: Üretilen sayılar
        denge_oranlari: Denge oranları
        cift_adimlar: Çift adım sayıları
        tek_adimlar: Tek adım sayıları
    """
    if not sayilar:
        print("Görselleştirme için veri bulunamadı.")
        return
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Collatz Dengeli Sayı Üreteci - Analiz Sonuçları', fontsize=16, fontweight='bold')
    
    # 1. Üretilen sayıların dağılımı
    axes[0, 0].hist(sayilar, bins=20, edgecolor='black', alpha=0.7, color='skyblue')
    axes[0, 0].set_title('Üretilen Sayıların Dağılımı')
    axes[0, 0].set_xlabel('Sayı Değeri')
    axes[0, 0].set_ylabel('Frekans')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Denge oranlarının dağılımı
    axes[0, 1].hist(denge_oranlari, bins=20, edgecolor='black', alpha=0.7, color='lightgreen')
    axes[0, 1].set_title('Denge Oranlarının Dağılımı')
    axes[0, 1].set_xlabel('Denge Oranı (0=en iyi)')
    axes[0, 1].set_ylabel('Frekans')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Çift ve tek adımların karşılaştırması
    axes[0, 2].scatter(cift_adimlar, tek_adimlar, alpha=0.6, color='purple')
    axes[0, 2].plot([0, max(cift_adimlar)], [0, max(cift_adimlar)], 'r--', alpha=0.5, label='İdeal Denge')
    axes[0, 2].set_title('Çift vs Tek Adımlar')
    axes[0, 2].set_xlabel('Çift Adım Sayısı')
    axes[0, 2].set_ylabel('Tek Adım Sayısı')
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)
    
    # 4. Çift ve tek adımların toplam dağılımı
    indices = list(range(len(sayilar)))
    axes[1, 0].bar(indices[:20], cift_adimlar[:20], alpha=0.7, label='Çift Adımlar', color='blue')
    axes[1, 0].bar(indices[:20], tek_adimlar[:20], alpha=0.7, label='Tek Adımlar', color='red', 
                   bottom=cift_adimlar[:20])
    axes[1, 0].set_title('İlk 20 Sayının Adım Dağılımı')
    axes[1, 0].set_xlabel('Sayı Indexi')
    axes[1, 0].set_ylabel('Adım Sayısı')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 5. Çift/Tek oranı
    oranlar = []
    for c, t in zip(cift_adimlar, tek_adimlar):
        if t > 0:
            oranlar.append(c / t)
        else:
            oranlar.append(c)
    
    axes[1, 1].hist(oranlar, bins=20, edgecolor='black', alpha=0.7, color='orange')
    axes[1, 1].axvline(x=1, color='red', linestyle='--', label='İdeal Denge (1:1)')
    axes[1, 1].set_title('Çift/Tek Adım Oranı Dağılımı')
    axes[1, 1].set_xlabel('Çift/Tek Oranı')
    axes[1, 1].set_ylabel('Frekans')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    # 6. Collatz uzunluğu vs denge oranı
    uzunluklar = [c + t for c, t in zip(cift_adimlar, tek_adimlar)]
    scatter = axes[1, 2].scatter(uzunluklar, denge_oranlari, c=oranlar, 
                                cmap='viridis', alpha=0.6, s=50)
    axes[1, 2].set_title('Collatz Uzunluğu vs Denge Oranı')
    axes[1, 2].set_xlabel('Collatz Dizisi Uzunluğu')
    axes[1, 2].set_ylabel('Denge Oranı')
    axes[1, 2].grid(True, alpha=0.3)
    
    # Renk barı ekle
    plt.colorbar(scatter, ax=axes[1, 2], label='Çift/Tek Oranı')
    
    plt.tight_layout()
    plt.savefig('collatz_analiz_grafikleri.png', dpi=300, bbox_inches='tight')
    plt.show()


def ornek_analiz(sayilar: List[int], uretici: CollatzDengeliUretici):
    """
    Örnek sayılar için detaylı Collatz analizi yapar.
    
    Args:
        sayilar: Analiz edilecek sayılar
        uretici: CollatzDengeliUretici nesnesi
    """
    if not sayilar:
        print("Analiz için veri bulunamadı.")
        return
    
    print("\n" + "="*60)
    print("ÖRNEK SAYILARIN DETAYLI COLLATZ ANALİZİ")
    print("="*60)
    
    for i, sayi in enumerate(sayilar[:5]):  # İlk 5 sayıyı analiz et
        dizi = uretici.collatz_dizisi(sayi)
        cift, tek, denge_orani = uretici.dizideki_0_1_dengesi(dizi)
        
        print(f"\n{i+1}. Sayı: {sayi}")
        print(f"   Collatz dizisi uzunluğu: {len(dizi)}")
        print(f"   Çift adımlar (0): {cift}")
        print(f"   Tek adımlar (1): {tek}")
        print(f"   Denge oranı: {denge_orani:.4f} (0=en iyi)")
        print(f"   Çift/Tek oranı: {cift/tek if tek > 0 else 'sonsuz':.2f}")
        
        # Adım türlerini göster
        adim_turleri = []
        for num in dizi[:-1]:
            if num % 2 == 0:
                adim_turleri.append('0')
            else:
                adim_turleri.append('1')
        
        print(f"   Adım türleri (ilk 20): {''.join(adim_turleri[:20])}{'...' if len(adim_turleri) > 20 else ''}")
        print(f"   Toplam adım: {len(adim_turleri)}")


def ana_program():
    """Ana program akışı."""
    print("🎯 COLLATZ DENGELİ SAYI ÜRETECİ 🎯")
    print("="*40)
    
    # Kullanıcı parametreleri
    try:
        adet = int(input("Üretilecek sayı adedi (varsayılan: 100): ") or "100")
        min_sayi = int(input("Minimum sayı değeri (varsayılan: 1): ") or "1")
        max_sayi = int(input("Maksimum sayı değeri (varsayılan: 10000): ") or "10000")
        denge_esigi = float(input("Denge eşiği (0-1 arası, varsayılan: 0.7): ") or "0.7")
    except ValueError:
        print("Geçersiz giriş! Varsayılan değerler kullanılıyor.")
        adet, min_sayi, max_sayi, denge_esigi = 100, 1, 10000, 0.7
    
    # Üreticiyi oluştur ve çalıştır
    uretici = CollatzDengeliUretici(min_sayi, max_sayi, denge_esigi)
    sayilar, denge_oranlari, cift_adimlar, tek_adimlar = uretici.dengeli_sayi_uret(adet)
    
    if sayilar:
        # Sonuçları görselleştir
        sonuclari_goruntule(sayilar, denge_oranlari, cift_adimlar, tek_adimlar)
        
        # Örnek analiz
        ornek_analiz(sayilar, uretici)
        
        # İstatistikleri kaydet
        uretici.istatistikleri_kaydet()
        
        # Ek bilgiler
        print("\n" + "="*60)
        print("GENEL DEĞERLENDİRME")
        print("="*60)
        
        toplam_cift = sum(cift_adimlar)
        toplam_tek = sum(tek_adimlar)
        
        if toplam_tek > 0:
            genel_oran = toplam_cift / toplam_tek
            print(f"Toplam çift adım: {toplam_cift}")
            print(f"Toplam tek adım: {toplam_tek}")
            print(f"Genel Çift/Tek oranı: {genel_oran:.4f}")
            print(f"İdeal dengeden sapma: {abs(1 - genel_oran)*100:.2f}%")
            
            if genel_oran < 1.2 and genel_oran > 0.8:
                print("✅ Sonuç: İyi derecede dengeli sayılar üretildi!")
            else:
                print("⚠️  Sonuç: Denge oranı ideale yakın değil, parametreleri ayarlamayı deneyin.")
    
    print("\nProgram sonlandı. Çıkmak için herhangi bir tuşa basın...")
    input()


if __name__ == "__main__":
    ana_program()
