import pandas as pd
import numpy as np

df = pd.read_csv('anket_verileri.csv')

with open('analiz_sonuclari.txt', 'w', encoding='utf-8') as f:
    
    f.write("=== NUMERİK SÜTUN ANALİZİ ===\n")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    for col in numeric_cols:
        f.write(f"\n* {col}:\n")
        f.write(f"  - Min: {df[col].min()}\n")
        f.write(f"  - Max: {df[col].max()}\n")
        f.write(f"  - Ortalama: {df[col].mean():.2f}\n")
        f.write(f"  - Medyan: {df[col].median()}\n")
        f.write(f"  - Eksik Değer: {df[col].isnull().sum()}\n")
    
    f.write("\n\n=== KATEGORİK SÜTUN ANALİZİ ===\n")
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    for col in categorical_cols:
        f.write(f"\n* {col}:\n")
        f.write(f"  - Benzersiz değer sayısı: {df[col].nunique()}\n")
        f.write(f"  - En sık 5 değer:\n")
        for val, count in df[col].value_counts().head(5).items():
            f.write(f"    - {val}: {count} (%{count/len(df)*100:.1f})\n")
        f.write(f"  - Eksik Değer: {df[col].isnull().sum()}\n")
    
    f.write("\n\n=== BOOLEAN SÜTUNLAR ===\n")
    bool_cols = [col for col in df.columns if df[col].dropna().isin([0,1]).all()]
    for col in bool_cols:
        f.write(f"\n* {col}:\n")
        f.write(f"  - Evet (1): {df[col].sum()} (%{df[col].mean()*100:.1f})\n")
        f.write(f"  - Hayır (0): {len(df)-df[col].sum()} (%{(1-df[col].mean())*100:.1f})\n")
    
    f.write("\n\n=== ÇOKLU SEÇİM SÜTUNLARI ===\n")
    multiselect_cols = [col for col in df.columns if 'Birden fazla seçeneği işaretleyebilirsiniz' in str(df[col].name)]
    for col in multiselect_cols:
        f.write(f"\n* {col}\n")
    
    f.write("\n\n=== SÜTUN TİP ÖZET TABLOSU ===\n")
    column_types = pd.DataFrame({
        'Sütun': df.columns,
        'Tip': df.dtypes,
        'Benzersiz Değer': [df[col].nunique() for col in df.columns],
        'Eksik Değer': df.isnull().sum()
    })
    f.write("\n" + column_types.to_string(index=False))
    
    f.write("\n\n=== VERİ KALİTESİ ÖZETİ ===\n")
    f.write(f"Toplam Satır Sayısı: {len(df)}\n")
    f.write(f"Toplam Eksik Değer: {df.isnull().sum().sum()} (%{df.isnull().sum().sum()/(len(df)*len(df.columns))*100:.1f})\n")

print("Analiz sonuçları 'analiz_sonuclari.txt' dosyasına kaydedildi.")