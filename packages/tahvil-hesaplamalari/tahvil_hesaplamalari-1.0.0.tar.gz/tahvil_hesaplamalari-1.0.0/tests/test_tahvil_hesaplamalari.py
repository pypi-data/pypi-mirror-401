"""
Tahvil Hesaplamaları Test Modülü

Bu modül, tahvil hesaplama fonksiyonlarının doğruluğunu test eder.
"""

import unittest
from src.tahvil_hesaplamalari import (
    tahvilin_bugunku_degeri,
    annuite_faktoru,
    kuponlu_tahvil_fiyati,
    sifir_kuponlu_tahvil_fiyati,
    getiri_orani,
    birikmis_faiz,
    temiz_fiyat,
    kirli_fiyat,
    macaulay_duration,
    degistirilmis_duration,
    konveksite
)


class TestTahvilHesaplamalari(unittest.TestCase):
    """Tahvil hesaplama fonksiyonları için test sınıfı"""
    
    def test_tahvilin_bugunku_degeri(self):
        """Tahvilin bugünkü değeri testi"""
        # 10 yıl vadeli, %5 kupon, %5 faiz oranı, 1000 TL nominal değer
        # Bu durumda tahvil nominal değerinde işlem görmeli
        sonuc = tahvilin_bugunku_degeri(50, 1000, 0.05, 10)
        self.assertAlmostEqual(sonuc, 1000.0, places=2)
    
    def test_annuite_faktoru(self):
        """Annüite faktörü testi"""
        sonuc = annuite_faktoru(0.05, 10)
        beklenen = 7.721734929184812
        self.assertAlmostEqual(sonuc, beklenen, places=5)
    
    def test_kuponlu_tahvil_fiyati(self):
        """Kuponlu tahvil fiyatı testi"""
        sonuc = kuponlu_tahvil_fiyati(50, 1000, 0.05, 10)
        self.assertAlmostEqual(sonuc, 1000.0, places=2)
    
    def test_sifir_kuponlu_tahvil_fiyati(self):
        """Sıfır kuponlu tahvil fiyatı testi"""
        sonuc = sifir_kuponlu_tahvil_fiyati(1000, 0.05, 10)
        beklenen = 613.9132535407591
        self.assertAlmostEqual(sonuc, beklenen, places=2)
    
    def test_getiri_orani(self):
        """Getiri oranı (YTM) testi"""
        # Nominal değerinde işlem gören tahvil için YTM = kupon oranı olmalı
        sonuc = getiri_orani(50, 1000, 1000, 10)
        self.assertAlmostEqual(sonuc, 0.05, places=3)
    
    def test_birikmis_faiz(self):
        """Birikmiş faiz testi"""
        sonuc = birikmis_faiz(50, 90, 180)
        self.assertAlmostEqual(sonuc, 25.0, places=2)
    
    def test_temiz_ve_kirli_fiyat(self):
        """Temiz ve kirli fiyat testi"""
        temiz = temiz_fiyat(1025, 25)
        self.assertAlmostEqual(temiz, 1000.0, places=2)
        
        kirli = kirli_fiyat(1000, 25)
        self.assertAlmostEqual(kirli, 1025.0, places=2)
    
    def test_macaulay_duration(self):
        """Macaulay Duration testi"""
        sonuc = macaulay_duration(50, 1000, 0.05, 10)
        beklenen = 8.107821675644049
        self.assertAlmostEqual(sonuc, beklenen, places=2)
    
    def test_degistirilmis_duration(self):
        """Modified Duration testi"""
        sonuc = degistirilmis_duration(50, 1000, 0.05, 10)
        beklenen = 7.721734929184808
        self.assertAlmostEqual(sonuc, beklenen, places=2)
    
    def test_konveksite(self):
        """Konveksite testi"""
        sonuc = konveksite(50, 1000, 0.05, 10)
        # Konveksite pozitif olmalı
        self.assertGreater(sonuc, 0)
        self.assertIsInstance(sonuc, float)
    
    def test_hata_durumlari(self):
        """Hata durumları testi"""
        # Negatif vade
        with self.assertRaises(ValueError):
            tahvilin_bugunku_degeri(50, 1000, 0.05, -1)
        
        # Geçersiz faiz oranı
        with self.assertRaises(ValueError):
            tahvilin_bugunku_degeri(50, 1000, -1.5, 10)
        
        # Sıfır toplam kupon günü
        with self.assertRaises(ValueError):
            birikmis_faiz(50, 90, 0)


if __name__ == '__main__':
    unittest.main()

