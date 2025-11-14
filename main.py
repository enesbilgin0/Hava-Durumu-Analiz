import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("--- Aşama 1: Veri Yükleme ve Hazırlık ---")

file_path = 'munich.csv'
df = pd.read_csv(file_path, delimiter=';')
print(f"'{file_path}' dosyası okundu.")

df.rename(columns={
    'time': 'tarih',
    'precipitation_sum (mm)': 'yagis_mm',
    'snowfall_sum (cm)': 'kar_cm'
}, inplace=True)

df['tarih'] = pd.to_datetime(df['tarih'])
df.set_index('tarih', inplace=True)

original_count = len(df)
df.dropna(subset=['yagis_mm', 'kar_cm'], how='all', inplace=True)
print(f"Tamamen NaN olan {original_count - len(df)} satır kaldırıldı.")

df.fillna(0, inplace=True)
print("Kalan NaN değerler 0 ile dolduruldu.")

print("\n--- Temizlenmiş Veri Bilgisi ---")
df.info()

print("\n--- Temizlenmiş Veri (İlk 5 Satır) ---")
print(df.head())


print("\n--- Aşama 2: Keşifsel Veri Analizi (EDA) ---")

print("\nİstatistiksel Özet:")
print(df.describe())

total_yagis = df['yagis_mm'].sum()
total_kar = df['kar_cm'].sum()
print(f"\nİncelenen Periyottaki Toplam Yağış Miktarı: {total_yagis:.2f} mm")
print(f"İncelenen Periyottaki Toplam Kar Yağışı: {total_kar:.2f} cm")

yagisli_gun_sayisi = (df['yagis_mm'] > 0).sum()
print(f"Yağışlı Gün Sayısı (yağış > 0 mm): {yagisli_gun_sayisi} gün")

max_yagis_gunu = df['yagis_mm'].idxmax()
max_yagis_degeri = df['yagis_mm'].max()
print(f"En Yüksek Günlük Yağış: {max_yagis_degeri:.2f} mm (Tarih: {max_yagis_gunu.strftime('%Y-%m-%d')})")

monthly_totals = df['yagis_mm'].resample('M').sum()
print("\nAy Bazında Toplam Yağış (mm):")
print(monthly_totals)

print("\n--- Aşama 3: Veri Görselleştirme ---")

try:
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['yagis_mm'], label='Günlük Yağış', color='blue', alpha=0.8, linestyle='-')
    plt.title('Günlük Yağış Miktarı (Münih, 2024)', fontsize=16)
    plt.xlabel('Tarih', fontsize=12)
    plt.ylabel('Yağış (mm)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('daily_precipitation_timeseries.png')
    plt.clf() # Figürü temizle
    print("Grafik kaydedildi: daily_precipitation_timeseries.png")
except Exception as e:
    print(f"Grafik 1 oluşturulurken hata: {e}")


try:
    plt.figure(figsize=(10, 6))
    monthly_labels = monthly_totals.index.strftime('%Y-%B')
    plt.bar(monthly_labels, monthly_totals, color='skyblue', edgecolor='black')
    plt.title('Aylık Toplam Yağış Miktarı (Münih, 2024)', fontsize=16)
    plt.xlabel('Ay', fontsize=12)
    plt.ylabel('Toplam Yağış (mm)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('monthly_precipitation_barchart.png')
    plt.clf()
    print("Grafik kaydedildi: monthly_precipitation_barchart.png")
except Exception as e:
    print(f"Grafik 2 oluşturulurken hata: {e}")

print("\nAnaliz ve görselleştirme tamamlandı.")