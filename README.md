# Collatz Dengesi Tabanlı Rastgele Sayı Üretici

Bu proje, **Collatz sanrısını** temel alarak geliştirilmiş,
rastgele üretilen sayıların Collatz dizilerindeki
**çift ve tek adımların dağılımını analiz eden**
ve bu adımların mümkün olduğunca dengeli olduğu
sayıları seçen bir rastgele sayı üretme algoritmasını içermektedir.

Klasik rastgele sayı üreteçlerinden farklı olarak,
bu algoritma yalnızca sayı üretmekle kalmaz,
üretilen her sayıyı matematiksel bir yapı üzerinden
değerlendirerek filtreler.

---

## 1. Collatz Sanrısı

Collatz sanrısı, bir pozitif tam sayı üzerinde tanımlanan
basit fakat davranışı karmaşık bir matematiksel süreçtir.

Kurallar şu şekildedir:

- Sayı **çift** ise → `n / 2`
- Sayı **tek** ise → `3n + 1`

Bu işlemler sayı `1` olana kadar tekrar edilir.
Elde edilen sayı dizisi **Collatz dizisi** olarak adlandırılır.

---

## 2. Algoritmanın Amacı

Bu çalışmanın temel amacı:

- Rastgele sayılar üretmek
- Üretilen sayıların Collatz dizilerinde
  - çift adım sayısı
  - tek adım sayısı
  arasındaki farkı analiz etmek
- Bu farkın **belirli bir eşik değerin altında**
  olduğu sayıları kabul etmek

Bu yaklaşım sayesinde, rastgelelik ile
yapısal denge birlikte sağlanır.

---

## 3. Denge Ölçütü

Bir sayının Collatz dizisi için denge oranı aşağıdaki
formül ile hesaplanır:

denge = |çift_adım - tek_adım| / (çift_adım + tek_adım)


- `denge = 0` → tamamen dengeli
- `denge → 1` → tamamen dengesiz

Algoritma, yalnızca denge değeri
kullanıcı tarafından belirlenen eşik değerinin
altında kalan sayıları kabul eder.

---

## 4. Algoritmanın Çalışma Adımları

Algoritma aşağıdaki adımları izler:

1. Belirlenen aralıkta rastgele bir sayı üretilir
2. Sayının Collatz dizisi hesaplanır
3. Dizideki çift ve tek adımlar sayılır
4. Denge oranı hesaplanır
5. Denge oranı eşik değerinden küçükse sayı kabul edilir
6. Yeterli sayıda dengeli sayı elde edilene kadar işlem tekrarlanır

Bu yapı, algoritmanın hem rastgele
hem de kontrollü olmasını sağlar.

---

## 5. Görselleştirme ve Analiz

Algoritma çıktıları üç farklı grafik ile analiz edilir:

1. **Üretilen sayıların dağılımı**  
   Rastgele üretilen sayıların değer aralığındaki frekans dağılımı

2. **Çift ve tek adımların karşılaştırılması**  
   Her sayı için çift ve tek adımların karşılıklı gösterimi

3. **Denge oranlarının dağılımı**  
   Üretilen sayıların ne kadar dengeli olduğunu gösteren histogram

Bu grafikler, algoritmanın istatistiksel davranışını
görsel olarak değerlendirmeyi mümkün kılar.

---

## 6. Kullanım

Program çalıştırıldığında:

Dengeli rastgele sayılar üretilir

Çift ve tek adım istatistikleri hesaplanır

Denge oranları analiz edilir

Grafikler ekranda gösterilir

Projeyi çalıştırmak için Python 3 yüklü bir ortam yeterlidir.

```bash
python collatz_rastgele_sayi_üretici.py

