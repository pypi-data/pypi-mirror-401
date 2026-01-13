# Dosya Konumu: mletahmin/__main__.py

from .mle import DagilimAnalizcisi
import os
import sys

def main():
    print("--- AKTÜERYA MLE TAHMİN SİSTEMİ ---")

    # Kullanıcıdan veri alma
    dosya_yolu = input("Dosya Adı (örn: Kitap1.csv): ").strip()
    dagilim_tercihi = input("Dağılım Adı (gamma, pareto, lomax): ").lower().strip()

    # Dosya kontrolü
    if not os.path.exists(dosya_yolu):
        print(f"HATA: '{dosya_yolu}' dosyası bulunamadı.")
        sys.exit()

    # Analiz işlemi
    try:
        analizci = DagilimAnalizcisi(dosya_yolu)

        if dagilim_tercihi == "gamma":
            sonuc = analizci.gamma_MLE()
        elif dagilim_tercihi == "pareto":
            sonuc = analizci.pareto_MLE()
        elif dagilim_tercihi == "lomax":
            sonuc = analizci.lomax_MLE()
        else:
            print("Geçersiz dağılım ismi! (gamma, pareto, lomax)")
            sys.exit()

        # Sonuçları Yazdırma
        print("-" * 35)
        # Eğer sonuçta hata döndüyse 'Dagilim' anahtarı olmayabilir, kontrol edelim
        print(f"SONUÇLAR ({sonuc.get('Dagilim', 'Bilinmiyor')})")
        print("-" * 35)
        
        for k, v in sonuc.items():
            if isinstance(v, float):
                print(f"{k:<20}: {v:.4f}")
            else:
                print(f"{k:<20}: {v}")
        print("-" * 35)

    except Exception as e:
        print(f"BEKLENMEDİK BİR HATA: {e}")

if __name__ == "__main__":
    main()