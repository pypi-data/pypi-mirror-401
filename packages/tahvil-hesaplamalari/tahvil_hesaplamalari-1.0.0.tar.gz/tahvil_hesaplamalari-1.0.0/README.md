# Tahvil Hesaplamaları

Tahvil değerleme ve risk analizi için kapsamlı Python kütüphanesi.

## Proje Geliştiricisi

Bu proje, aktüeryal hesaplamalar dersi kapsamında geliştirilmiştir.

## Projenin Amacı ve Kapsamı

Bu proje, tahvil yatırımları ile ilgili temel finansal hesaplamaları yapmak için geliştirilmiştir. Proje kapsamında şu hesaplamalar yer almaktadır:

- **Tahvil Fiyatlandırma**: Kuponlu ve sıfır kuponlu tahvillerin bugünkü değerinin hesaplanması
- **Getiri Analizi**: Tahvilin iç verim oranı (Yield to Maturity - YTM) hesaplama
- **Risk Ölçüleri**: Duration ve Convexity hesaplamaları
- **Fiyat Hesaplamaları**: Temiz ve kirli fiyat hesaplamaları
- **Birikmiş Faiz**: Kupon tarihleri arasındaki birikmiş faiz hesaplama

## Kurulum ve Çalıştırma Adımları

### Gereksinimler

- Python 3.7 veya üzeri
- math modülü (Python standart kütüphanesi)
- typing modülü (Python standart kütüphanesi)

### Kurulum

1. Projeyi indirin veya klonlayın:
```bash
git clone <repository-url>
cd tahvil-hesaplamalari
```

2. Proje dizinine gidin:
```bash
cd tahvil-hesaplamalari
```

3. Gerekli bağımlılıklar zaten Python standart kütüphanesinde olduğu için ek kurulum gerekmez.

### Çalıştırma

Projeyi kullanmak için Python'da modülü import edin:

```python
from src.tahvil_hesaplamalari import tahvilin_bugunku_degeri
```

## Örnek Kullanım

### Temel Tahvil Fiyatlandırma

```python
from src.tahvil_hesaplamalari import tahvilin_bugunku_degeri, kuponlu_tahvil_fiyati

# 10 yıl vadeli, yıllık %5 kupon ödemeli, %5 piyasa faiz oranı, 1000 TL nominal değerli tahvil
kupon_tutari = 50  # Yıllık kupon ödemesi
nominal_deger = 1000
piyasa_faiz_orani = 0.05  # %5
vade = 10  # 10 yıl

# Tahvilin bugünkü değeri
fiyat = tahvilin_bugunku_degeri(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)
print(f"Tahvil Fiyatı: {fiyat:.2f} TL")
# Çıktı: Tahvil Fiyatı: 1000.00 TL

# Alternatif olarak kuponlu tahvil fiyatı fonksiyonu
fiyat2 = kuponlu_tahvil_fiyati(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)
print(f"Tahvil Fiyatı (Alternatif): {fiyat2:.2f} TL")
```

### Sıfır Kuponlu Tahvil

```python
from src.tahvil_hesaplamalari import sifir_kuponlu_tahvil_fiyati

# 10 yıl vadeli, kupon ödemesi olmayan tahvil
nominal_deger = 1000
piyasa_faiz_orani = 0.05
vade = 10

fiyat = sifir_kuponlu_tahvil_fiyati(nominal_deger, piyasa_faiz_orani, vade)
print(f"Sıfır Kuponlu Tahvil Fiyatı: {fiyat:.2f} TL")
# Çıktı: Sıfır Kuponlu Tahvil Fiyatı: 613.91 TL
```

### Getiri Oranı (YTM) Hesaplama

```python
from src.tahvil_hesaplamalari import getiri_orani

# Piyasada 950 TL'ye işlem gören tahvil için YTM hesaplama
kupon_tutari = 50
nominal_deger = 1000
tahvil_fiyati = 950
vade = 10

ytm = getiri_orani(kupon_tutari, nominal_deger, tahvil_fiyati, vade)
print(f"İç Verim Oranı (YTM): {ytm*100:.2f}%")
```

### Risk Ölçüleri

```python
from src.tahvil_hesaplamalari import macaulay_duration, degistirilmis_duration, konveksite

kupon_tutari = 50
nominal_deger = 1000
piyasa_faiz_orani = 0.05
vade = 10

# Macaulay Duration
mac_duration = macaulay_duration(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)
print(f"Macaulay Duration: {mac_duration:.2f} yıl")

# Modified Duration
mod_duration = degistirilmis_duration(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)
print(f"Modified Duration: {mod_duration:.2f}")

# Konveksite
conv = konveksite(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)
print(f"Konveksite: {conv:.2f}")
```

### Birikmiş Faiz ve Fiyat Hesaplamaları

```python
from src.tahvil_hesaplamalari import birikmis_faiz, temiz_fiyat, kirli_fiyat

# Birikmiş faiz hesaplama
kupon_tutari = 50
gecen_gun = 90  # Son kupon tarihinden bu yana 90 gün geçmiş
toplam_gun = 180  # İki kupon arası 180 gün

birikmis = birikmis_faiz(kupon_tutari, gecen_gun, toplam_gun)
print(f"Birikmiş Faiz: {birikmis:.2f} TL")
# Çıktı: Birikmiş Faiz: 25.00 TL

# Temiz ve kirli fiyat
temiz = 1000
birikmis_faiz_tutari = 25

kirli = kirli_fiyat(temiz, birikmis_faiz_tutari)
print(f"Kirli Fiyat: {kirli:.2f} TL")
# Çıktı: Kirli Fiyat: 1025.00 TL

temiz_geri = temiz_fiyat(kirli, birikmis_faiz_tutari)
print(f"Temiz Fiyat: {temiz_geri:.2f} TL")
# Çıktı: Temiz Fiyat: 1000.00 TL
```

### Test Çalıştırma

Projeyi test etmek için:

```bash
python -m pytest tests/test_tahvil_hesaplamalari.py
```

veya

```bash
python -m unittest tests.test_tahvil_hesaplamalari
```

## Fonksiyonların Kısa Açıklaması ve Parametreleri

### 1. `tahvilin_bugunku_degeri(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)`

Tahvilin bugünkü değerini hesaplar. Tüm nakit akışlarının bugüne indirgenmiş değerini döndürür.

**Parametreler:**
- `kupon_tutari` (float): Her dönem ödenen kupon tutarı
- `nominal_deger` (float): Nominal (itfa) değeri
- `piyasa_faiz_orani` (float): Piyasa faiz oranı (iskonto oranı)
- `vade` (int): Toplam vade (dönem sayısı)

**Döndürür:** `float` - Tahvilin bugünkü fiyatı

---

### 2. `annuite_faktoru(faiz_orani, vade)`

Annüite faktörünü hesaplar. Kupon ödemelerinin bugünkü değerini hesaplamak için kullanılır.

**Parametreler:**
- `faiz_orani` (float): Faiz oranı
- `vade` (int): Vade (dönem sayısı)

**Döndürür:** `float` - Annüite faktörü

---

### 3. `kuponlu_tahvil_fiyati(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)`

Kuponlu tahvil fiyatını annüite faktörü kullanarak hesaplar.

**Parametreler:**
- `kupon_tutari` (float): Her dönem ödenen kupon tutarı
- `nominal_deger` (float): Nominal (itfa) değeri
- `piyasa_faiz_orani` (float): Piyasa faiz oranı
- `vade` (int): Toplam vade (dönem sayısı)

**Döndürür:** `float` - Tahvilin fiyatı

---

### 4. `sifir_kuponlu_tahvil_fiyati(nominal_deger, piyasa_faiz_orani, vade)`

Sıfır kuponlu tahvil fiyatını hesaplar. Bu tahvillerde kupon ödemesi yoktur.

**Parametreler:**
- `nominal_deger` (float): Nominal (itfa) değeri
- `piyasa_faiz_orani` (float): Piyasa faiz oranı
- `vade` (int): Toplam vade (dönem sayısı)

**Döndürür:** `float` - Tahvilin fiyatı

---

### 5. `getiri_orani(kupon_tutari, nominal_deger, tahvil_fiyati, vade, baslangic_tahmini, hata_payi, max_iterasyon)`

Tahvilin iç verim oranını (Yield to Maturity - YTM) hesaplar. Newton-Raphson yöntemi kullanılır.

**Parametreler:**
- `kupon_tutari` (float): Her dönem ödenen kupon tutarı
- `nominal_deger` (float): Nominal (itfa) değeri
- `tahvil_fiyati` (float): Tahvilin piyasa fiyatı
- `vade` (int): Toplam vade (dönem sayısı)
- `baslangic_tahmini` (float, opsiyonel): Başlangıç tahmini (varsayılan: 0.05)
- `hata_payi` (float, opsiyonel): Hata payı (varsayılan: 1e-6)
- `max_iterasyon` (int, opsiyonel): Maksimum iterasyon sayısı (varsayılan: 1000)

**Döndürür:** `float` - İç verim oranı (YTM)

---

### 6. `birikmis_faiz(kupon_tutari, gecen_gun_sayisi, toplam_kupon_gunu)`

Birikmiş faizi hesaplar. Kupon tarihleri arasında tahvil satılırsa, satıcının hak ettiği faizi hesaplar.

**Parametreler:**
- `kupon_tutari` (float): Kupon tutarı
- `gecen_gun_sayisi` (int): Son kupon tarihinden bu yana geçen gün sayısı
- `toplam_kupon_gunu` (int): İki kupon tarihi arasındaki toplam gün sayısı

**Döndürür:** `float` - Birikmiş faiz

---

### 7. `temiz_fiyat(kirli_fiyat, birikmis_faiz_tutari)`

Temiz fiyatı hesaplar. Piyasalarda genellikle temiz fiyat kullanılır.

**Parametreler:**
- `kirli_fiyat` (float): Kirli fiyat (temiz fiyat + birikmiş faiz)
- `birikmis_faiz_tutari` (float): Birikmiş faiz tutarı

**Döndürür:** `float` - Temiz fiyat

---

### 8. `kirli_fiyat(temiz_fiyat, birikmis_faiz_tutari)`

Kirli fiyatı hesaplar.

**Parametreler:**
- `temiz_fiyat` (float): Temiz fiyat
- `birikmis_faiz_tutari` (float): Birikmiş faiz tutarı

**Döndürür:** `float` - Kirli fiyat

---

### 9. `macaulay_duration(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)`

Macaulay Duration'ı hesaplar. Tahvilin ağırlıklı ortalama geri dönüş süresini ölçer.

**Parametreler:**
- `kupon_tutari` (float): Her dönem ödenen kupon tutarı
- `nominal_deger` (float): Nominal (itfa) değeri
- `piyasa_faiz_orani` (float): Piyasa faiz oranı
- `vade` (int): Toplam vade (dönem sayısı)

**Döndürür:** `float` - Macaulay Duration

---

### 10. `degistirilmis_duration(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)`

Modified Duration'ı hesaplar. Faiz değişimine karşı fiyat hassasiyetini gösterir.

**Parametreler:**
- `kupon_tutari` (float): Her dönem ödenen kupon tutarı
- `nominal_deger` (float): Nominal (itfa) değeri
- `piyasa_faiz_orani` (float): Piyasa faiz oranı
- `vade` (int): Toplam vade (dönem sayısı)

**Döndürür:** `float` - Modified Duration

---

### 11. `konveksite(kupon_tutari, nominal_deger, piyasa_faiz_orani, vade)`

Konveksite (Convexity) değerini hesaplar. Duration'un yakalayamadığı eğriliği ölçer.

**Parametreler:**
- `kupon_tutari` (float): Her dönem ödenen kupon tutarı
- `nominal_deger` (float): Nominal (itfa) değeri
- `piyasa_faiz_orani` (float): Piyasa faiz oranı
- `vade` (int): Toplam vade (dönem sayısı)

**Döndürür:** `float` - Konveksite değeri

---

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## Katkıda Bulunma

Bu proje bir ödev çalışmasıdır. Katkılarınız için teşekkür ederiz.

