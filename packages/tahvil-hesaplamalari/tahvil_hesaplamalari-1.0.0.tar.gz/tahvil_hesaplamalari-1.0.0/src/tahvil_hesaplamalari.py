"""
Tahvil Hesaplamaları Modülü

Bu modül, tahvil değerleme ve risk analizi için gerekli tüm hesaplamaları içerir.
Tüm fonksiyonlar Türkçe isimlendirilmiştir.
"""

import math
from typing import List, Optional


def tahvilin_bugunku_degeri(
    kupon_tutari: float,
    nominal_deger: float,
    piyasa_faiz_orani: float,
    vade: int
) -> float:
    """
    Tahvilin bugünkü değerini (fiyatını) hesaplar.
    
    Formül: P = Σ C/(1+i)^t + F/(1+i)^n
    
    Parametreler:
        kupon_tutari (float): Her dönem ödenen kupon tutarı
        nominal_deger (float): Nominal (itfa) değeri
        piyasa_faiz_orani (float): Piyasa faiz oranı (iskonto oranı)
        vade (int): Toplam vade (dönem sayısı)
    
    Döndürür:
        float: Tahvilin bugünkü fiyatı
    
    Örnek:
        >>> tahvilin_bugunku_degeri(50, 1000, 0.05, 10)
        1000.0
    """
    if piyasa_faiz_orani <= -1:
        raise ValueError("Faiz oranı -1'den büyük olmalıdır")
    
    if vade < 0:
        raise ValueError("Vade negatif olamaz")
    
    bugunku_deger = 0.0
    
    # Kupon ödemelerinin bugünkü değeri
    for t in range(1, vade + 1):
        bugunku_deger += kupon_tutari / ((1 + piyasa_faiz_orani) ** t)
    
    # Nominal değerin bugünkü değeri
    bugunku_deger += nominal_deger / ((1 + piyasa_faiz_orani) ** vade)
    
    return bugunku_deger


def annuite_faktoru(faiz_orani: float, vade: int) -> float:
    """
    Annüite faktörünü hesaplar.
    
    Formül: a(n|i) = [1 - (1+i)^(-n)] / i
    
    Parametreler:
        faiz_orani (float): Faiz oranı
        vade (int): Vade (dönem sayısı)
    
    Döndürür:
        float: Annüite faktörü
    
    Örnek:
        >>> annuite_faktoru(0.05, 10)
        7.721734929184812
    """
    if faiz_orani == 0:
        return vade
    
    if faiz_orani <= -1:
        raise ValueError("Faiz oranı -1'den büyük olmalıdır")
    
    if vade < 0:
        raise ValueError("Vade negatif olamaz")
    
    return (1 - (1 + faiz_orani) ** (-vade)) / faiz_orani


def kuponlu_tahvil_fiyati(
    kupon_tutari: float,
    nominal_deger: float,
    piyasa_faiz_orani: float,
    vade: int
) -> float:
    """
    Kuponlu tahvil fiyatını annüite faktörü kullanarak hesaplar.
    
    Formül: P = C * a(n|i) + F(1+i)^(-n)
    
    Parametreler:
        kupon_tutari (float): Her dönem ödenen kupon tutarı
        nominal_deger (float): Nominal (itfa) değeri
        piyasa_faiz_orani (float): Piyasa faiz oranı (iskonto oranı)
        vade (int): Toplam vade (dönem sayısı)
    
    Döndürür:
        float: Tahvilin fiyatı
    
    Örnek:
        >>> kuponlu_tahvil_fiyati(50, 1000, 0.05, 10)
        1000.0
    """
    a_n_i = annuite_faktoru(piyasa_faiz_orani, vade)
    fiyat = kupon_tutari * a_n_i + nominal_deger * ((1 + piyasa_faiz_orani) ** (-vade))
    return fiyat


def sifir_kuponlu_tahvil_fiyati(
    nominal_deger: float,
    piyasa_faiz_orani: float,
    vade: int
) -> float:
    """
    Sıfır kuponlu tahvil fiyatını hesaplar.
    
    Formül: P = F / (1 + i)^n
    
    Parametreler:
        nominal_deger (float): Nominal (itfa) değeri
        piyasa_faiz_orani (float): Piyasa faiz oranı (iskonto oranı)
        vade (int): Toplam vade (dönem sayısı)
    
    Döndürür:
        float: Tahvilin fiyatı
    
    Örnek:
        >>> sifir_kuponlu_tahvil_fiyati(1000, 0.05, 10)
        613.9132535407591
    """
    if piyasa_faiz_orani <= -1:
        raise ValueError("Faiz oranı -1'den büyük olmalıdır")
    
    if vade < 0:
        raise ValueError("Vade negatif olamaz")
    
    return nominal_deger / ((1 + piyasa_faiz_orani) ** vade)


def getiri_orani(
    kupon_tutari: float,
    nominal_deger: float,
    tahvil_fiyati: float,
    vade: int,
    baslangic_tahmini: float = 0.05,
    hata_payi: float = 1e-6,
    max_iterasyon: int = 1000
) -> float:
    """
    Tahvilin iç verim oranını (Yield to Maturity - YTM) hesaplar.
    
    Kapalı form yoktur. Newton-Raphson yöntemi kullanılarak bulunur.
    
    Parametreler:
        kupon_tutari (float): Her dönem ödenen kupon tutarı
        nominal_deger (float): Nominal (itfa) değeri
        tahvil_fiyati (float): Tahvilin piyasa fiyatı
        vade (int): Toplam vade (dönem sayısı)
        baslangic_tahmini (float): Başlangıç tahmini (varsayılan: 0.05)
        hata_payi (float): Hata payı (varsayılan: 1e-6)
        max_iterasyon (int): Maksimum iterasyon sayısı (varsayılan: 1000)
    
    Döndürür:
        float: İç verim oranı (YTM)
    
    Örnek:
        >>> getiri_orani(50, 1000, 1000, 10)
        0.05
    """
    if tahvil_fiyati <= 0:
        raise ValueError("Tahvil fiyatı pozitif olmalıdır")
    
    if vade < 0:
        raise ValueError("Vade negatif olamaz")
    
    y = baslangic_tahmini
    
    for _ in range(max_iterasyon):
        # Fiyat fonksiyonu
        fiyat_hesaplanan = kuponlu_tahvil_fiyati(kupon_tutari, nominal_deger, y, vade)
        fark = fiyat_hesaplanan - tahvil_fiyati
        
        if abs(fark) < hata_payi:
            return y
        
        # Türev (modified duration kullanarak yaklaşık)
        if y == 0:
            y = 0.001  # Sıfırdan kaçın
        
        # Modified duration ile türev yaklaşımı
        modified_duration = degistirilmis_duration(
            kupon_tutari, nominal_deger, y, vade
        )
        
        if abs(modified_duration) < 1e-10:
            y += 0.001
            continue
        
        # Newton-Raphson güncellemesi
        y = y - fark / (fiyat_hesaplanan * modified_duration)
        
        if y < -0.99:
            y = -0.99
        if y > 10:
            y = 10
    
    raise ValueError(f"YTM bulunamadı. Maksimum iterasyon sayısına ulaşıldı.")


def birikmis_faiz(
    kupon_tutari: float,
    gecen_gun_sayisi: int,
    toplam_kupon_gunu: int
) -> float:
    """
    Birikmiş faizi hesaplar.
    
    Formül: AI = C * (Geçen Gün Sayısı / Toplam Kupon Günü)
    
    Parametreler:
        kupon_tutari (float): Kupon tutarı
        gecen_gun_sayisi (int): Son kupon tarihinden bu yana geçen gün sayısı
        toplam_kupon_gunu (int): İki kupon tarihi arasındaki toplam gün sayısı
    
    Döndürür:
        float: Birikmiş faiz
    
    Örnek:
        >>> birikmis_faiz(50, 90, 180)
        25.0
    """
    if toplam_kupon_gunu <= 0:
        raise ValueError("Toplam kupon günü pozitif olmalıdır")
    
    if gecen_gun_sayisi < 0:
        raise ValueError("Geçen gün sayısı negatif olamaz")
    
    return kupon_tutari * (gecen_gun_sayisi / toplam_kupon_gunu)


def temiz_fiyat(
    kirli_fiyat: float,
    birikmis_faiz_tutari: float
) -> float:
    """
    Temiz fiyatı hesaplar.
    
    Formül: Temiz Fiyat = Kirli Fiyat - Birikmiş Faiz
    
    Parametreler:
        kirli_fiyat (float): Kirli fiyat (temiz fiyat + birikmiş faiz)
        birikmis_faiz_tutari (float): Birikmiş faiz tutarı
    
    Döndürür:
        float: Temiz fiyat
    
    Örnek:
        >>> temiz_fiyat(1025, 25)
        1000.0
    """
    return kirli_fiyat - birikmis_faiz_tutari


def kirli_fiyat(
    temiz_fiyat: float,
    birikmis_faiz_tutari: float
) -> float:
    """
    Kirli fiyatı hesaplar.
    
    Formül: Kirli Fiyat = Temiz Fiyat + Birikmiş Faiz
    
    Parametreler:
        temiz_fiyat (float): Temiz fiyat
        birikmis_faiz_tutari (float): Birikmiş faiz tutarı
    
    Döndürür:
        float: Kirli fiyat
    
    Örnek:
        >>> kirli_fiyat(1000, 25)
        1025.0
    """
    return temiz_fiyat + birikmis_faiz_tutari


def macaulay_duration(
    kupon_tutari: float,
    nominal_deger: float,
    piyasa_faiz_orani: float,
    vade: int
) -> float:
    """
    Macaulay Duration'ı hesaplar.
    
    Formül: D = Σ [t * CF(t) / (1+i)^t] / P
    
    Parametreler:
        kupon_tutari (float): Her dönem ödenen kupon tutarı
        nominal_deger (float): Nominal (itfa) değeri
        piyasa_faiz_orani (float): Piyasa faiz oranı
        vade (int): Toplam vade (dönem sayısı)
    
    Döndürür:
        float: Macaulay Duration
    
    Örnek:
        >>> macaulay_duration(50, 1000, 0.05, 10)
        8.107821675644049
    """
    if piyasa_faiz_orani <= -1:
        raise ValueError("Faiz oranı -1'den büyük olmalıdır")
    
    if vade < 0:
        raise ValueError("Vade negatif olamaz")
    
    tahvil_fiyati = kuponlu_tahvil_fiyati(
        kupon_tutari, nominal_deger, piyasa_faiz_orani, vade
    )
    
    if tahvil_fiyati == 0:
        raise ValueError("Tahvil fiyatı sıfır olamaz")
    
    agirlikli_toplam = 0.0
    
    # Kupon ödemeleri için (son dönem hariç)
    for t in range(1, vade):
        nakit_akisi = kupon_tutari
        bugunku_deger = nakit_akisi / ((1 + piyasa_faiz_orani) ** t)
        agirlikli_toplam += t * bugunku_deger
    
    # Son dönem: kupon + nominal değer
    son_donem_nakit_akisi = kupon_tutari + nominal_deger
    son_donem_bugunku_deger = son_donem_nakit_akisi / ((1 + piyasa_faiz_orani) ** vade)
    agirlikli_toplam += vade * son_donem_bugunku_deger
    
    return agirlikli_toplam / tahvil_fiyati


def degistirilmis_duration(
    kupon_tutari: float,
    nominal_deger: float,
    piyasa_faiz_orani: float,
    vade: int
) -> float:
    """
    Modified Duration'ı hesaplar.
    
    Formül: D* = D / (1+i)
    
    Parametreler:
        kupon_tutari (float): Her dönem ödenen kupon tutarı
        nominal_deger (float): Nominal (itfa) değeri
        piyasa_faiz_orani (float): Piyasa faiz oranı
        vade (int): Toplam vade (dönem sayısı)
    
    Döndürür:
        float: Modified Duration
    
    Örnek:
        >>> degistirilmis_duration(50, 1000, 0.05, 10)
        7.354033265890297
    """
    if piyasa_faiz_orani <= -1:
        raise ValueError("Faiz oranı -1'den büyük olmalıdır")
    
    macaulay = macaulay_duration(
        kupon_tutari, nominal_deger, piyasa_faiz_orani, vade
    )
    
    return macaulay / (1 + piyasa_faiz_orani)


def konveksite(
    kupon_tutari: float,
    nominal_deger: float,
    piyasa_faiz_orani: float,
    vade: int
) -> float:
    """
    Konveksite (Convexity) değerini hesaplar.
    
    Formül: C = Σ [t(t+1) * CF(t) / (1+i)^(t+2)] / P
    
    Parametreler:
        kupon_tutari (float): Her dönem ödenen kupon tutarı
        nominal_deger (float): Nominal (itfa) değeri
        piyasa_faiz_orani (float): Piyasa faiz oranı
        vade (int): Toplam vade (dönem sayısı)
    
    Döndürür:
        float: Konveksite değeri
    
    Örnek:
        >>> konveksite(50, 1000, 0.05, 10)
        64.93827160478968
    """
    if piyasa_faiz_orani <= -1:
        raise ValueError("Faiz oranı -1'den büyük olmalıdır")
    
    if vade < 0:
        raise ValueError("Vade negatif olamaz")
    
    tahvil_fiyati = kuponlu_tahvil_fiyati(
        kupon_tutari, nominal_deger, piyasa_faiz_orani, vade
    )
    
    if tahvil_fiyati == 0:
        raise ValueError("Tahvil fiyatı sıfır olamaz")
    
    konveksite_toplam = 0.0
    
    # Kupon ödemeleri için (son dönem hariç)
    for t in range(1, vade):
        nakit_akisi = kupon_tutari
        bugunku_deger = nakit_akisi / ((1 + piyasa_faiz_orani) ** (t + 2))
        konveksite_toplam += t * (t + 1) * bugunku_deger
    
    # Son dönem: kupon + nominal değer
    son_donem_nakit_akisi = kupon_tutari + nominal_deger
    son_donem_bugunku_deger = son_donem_nakit_akisi / ((1 + piyasa_faiz_orani) ** (vade + 2))
    konveksite_toplam += vade * (vade + 1) * son_donem_bugunku_deger
    
    return konveksite_toplam / tahvil_fiyati

