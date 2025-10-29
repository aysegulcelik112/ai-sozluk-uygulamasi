# 🤖 AI Destekli Sözlük Uygulaması

Google Gemini AI ve Google Translate API'lerini kullanan, çok dilli yapay zeka destekli sözlük uygulaması.

## 🎯 Proje Hakkında

Bu proje, staj sürecimde geliştirdiğim yapay zeka destekli sözlük uygulamasıdır. Kullanıcılar kelime ve cümleleri farklı dillere çevirebilir, AI ile üretilmiş örnek cümleler görebilir ve çoklu anlamları keşfedebilir.

## ✨ Özellikler

- 🌍 7 farklı dil desteği (Türkçe, İngilizce, Almanca, Fransızca, Arapça, Rusça, İspanyolca)
- 🤖 Google Gemini AI ile otomatik örnek cümle üretimi
- 📚 Çok anlamlı Türkçe kelimeler için özel anlam desteği
- 🎨 Modern ve renkli kullanıcı arayüzü
- ⚡ Hızlı ve doğru çeviri
- 📊 İlerleme göstergesi ile kullanıcı dostu deneyim

## 🛠️ Kullanılan Teknolojiler

- **Python 3.x** - Ana programlama dili
- **PyQt5** - GUI framework
- **Google Translate API** (googletrans) - Çeviri servisi
- **Google Gemini AI** - Örnek cümle üretimi
- **Requests** - API çağrıları

## 📋 Gereksinimler
```bash
Python 3.7+
PyQt5
googletrans==4.0.0rc1
requests
```

## 🚀 Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/KULLANICI_ADIN/ai-sozluk-uygulamasi.git
cd ai-sozluk-uygulamasi
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `config.py` dosyası oluşturun ve Gemini API anahtarınızı ekleyin:
```python
GEMINI_API_KEY = "sizin_api_anahtariniz"
```

4. Uygulamayı çalıştırın:
```bash
python main.py
```

## 💡 Kullanım

1. Kaynak dil ve hedef dili seçin
2. Çevirmek istediğiniz kelime veya cümleyi girin
3. "✨ ÇEVİR" butonuna basın
4. Çeviriyi, anlamları ve AI üretimli örnek cümleleri görün

## 🎨 Özellikler Detayı

### Çok Anlamlı Kelime Desteği
Uygulama, Türkçe'deki çok anlamlı kelimeleri (eş sesli kelimeler) tanır:
- "ay" → month, moon
- "yüz" → face, hundred, swim
- "dil" → tongue, language
- ve 30+ kelime daha!

### AI Destekli Örnek Cümleler
Her anlam için Gemini AI tarafından üretilmiş, doğal ve anlamlı örnek cümleler.

## 📸 Ekran Görüntüleri

<img width="760" height="691" alt="image" src="https://github.com/user-attachments/assets/2759dc9b-4960-4a03-9cb6-1dea0f208bc0" />


## 🔑 API Anahtarı Alma

1. [Google AI Studio](https://aistudio.google.com/) adresine gidin
2. Ücretsiz API anahtarı oluşturun
3. `config.py` dosyasına ekleyin

## 👨‍💻 Geliştirici

**[Ayşe Gül Çelik]**
- Staj Projesi - 
- Geliştirme Tarihi: [20.07.2025]

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## ⚠️ Önemli Notlar

- API anahtarlarınızı asla paylaşmayın
- `config.py` dosyasını `.gitignore`'a ekleyin
- Günlük API kullanım limitlerini kontrol edin

## 🐛 Bilinen Sorunlar

- Bazı diller için Gemini API yanıt süreleri uzun olabilir
- Çok uzun cümleler için çeviri süresi artabilir

---
⭐ Bu projeyi faydalı bulduysan yıldız vermeyi unutma!
```

