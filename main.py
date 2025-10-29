import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QProgressBar
)
from googletrans import Translator
import requests # API çağrıları için gerekli
import json     # JSON verilerini işlemek için gerekli
import time

# Google Translate için Translator objesi oluşturuluyor
translator = Translator()

# Desteklenen diller ve kodları
languages = {
    "Türkçe": "tr",
    "İngilizce": "en",
    "Almanca": "de",
    "Fransızca": "fr",
    "Arapça": "ar",
    "Rusça": "ru",
    "İspanyolca": "es"
}

class DictionaryApp(QWidget):
    def __init__(self):
        """Uygulamanın başlangıç ayarları ve UI bileşenlerinin oluşturulması."""
        super().__init__()
        self.initUI()
        
    def initUI(self):
        """Kullanıcı arayüzünü başlatır - Yenilenmiş Modern Tasarım"""
        self.setWindowTitle("🚀 Yapay Zeka Sözlük - Ayşe'nin Projesi")
        self.setGeometry(100, 100, 750, 650)
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FCE38A, stop:1 #F38181
                );
                font-family: 'Segoe UI';
                font-size: 15px;
            }
            QLabel {
                font-weight: bold;
                color: #2d3436;
            }
        """)

        self.source_lang = QComboBox()
        self.target_lang = QComboBox()
        for lang in languages:
            self.source_lang.addItem(lang)
            self.target_lang.addItem(lang)

        combo_style = """
            QComboBox {
                padding: 8px;
                border: 2px solid #dfe6e9;
                border-radius: 15px;
                background-color: #ffffff;
                font-weight: bold;
            }
            QComboBox:hover {
                background-color: #dfe6e9;
            }
        """
        self.source_lang.setStyleSheet(combo_style)
        self.target_lang.setStyleSheet(combo_style)

        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Kelime veya cümle girin")
        self.word_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ffffff;
                border-radius: 20px;
                background-color: #ffffff;
                font-size: 16px;
            }
        """)

        self.translate_button = QPushButton("✨ ÇEVİR")
        self.translate_button.clicked.connect(self.translate)
        self.translate_button.setStyleSheet("""
            QPushButton {
                background-color: #00b894;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #019875;
            }
        """)

        self.progress = QProgressBar()
        self.progress.hide()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #dfe6e9;
                border-radius: 10px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00cec9;
                width: 10px;
            }
        """)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("""
            QTextEdit {
                padding: 12px;
                border: 2px solid #ffffff;
                border-radius: 20px;
                background-color: #ffffff;
                font-size: 15px;
            }
        """)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("🌐 Kaynak Dil:"))
        hbox.addWidget(self.source_lang)
        hbox.addSpacing(20)
        hbox.addWidget(QLabel("🎯 Hedef Dil:"))
        hbox.addWidget(self.target_lang)

        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        vbox.setContentsMargins(30, 30, 30, 30)
        vbox.addLayout(hbox)
        vbox.addWidget(self.word_input)
        vbox.addWidget(self.translate_button)
        vbox.addWidget(self.progress)
        vbox.addWidget(self.result_area)

        self.setLayout(vbox)


    def translate(self):
        """Çeviri işlemini başlatır ve sonuçları görüntüler."""
        text = self.word_input.text().strip()
        if not text:
            self.result_area.setPlainText("Lütfen bir kelime veya cümle girin.")
            return
        
        # İşlem başlarken ilerleme çubuğunu göster ve butonu devre dışı bırak
        self.progress.show()
        self.progress.setRange(0, 0)  # Sonsuz ilerleme (belirli bir bitiş noktası yok)
        self.translate_button.setEnabled(False)
        
        # Seçilen kaynak ve hedef dillerin kodlarını al
        src = languages[self.source_lang.currentText()]
        dest_name = self.target_lang.currentText() # Hedef dilin adını al (örn: "İngilizce", "Almanca")
        dest_code = languages[dest_name] # Hedef dilin kodunu al (örn: "en", "de")
        
        try:
            # Google Translate kullanarak kelimeyi çevir
            translation = translator.translate(text, src=src, dest=dest_code)
            translated_word = translation.text
            
            result_text = f"🔤 Çeviri: {translated_word}\n"
            result_text += f"📝 Orijinal: {text}\n"
            result_text += "-" * 50 + "\n"
            
            # Kelimenin farklı anlamlarını belirle (şimdilik sabit liste kullanılıyor)
            # Not: Bu fonksiyon şu anda sadece İngilizce kelimeler için anlamlar içeriyor.
            # Diğer diller için genel bir çeviri döndürecektir.
            meanings = self.get_word_meanings(text.lower(), translated_word.lower())

            result_text += f"\n📚 Anlamlar ve Örnek Cümleler ({dest_name}):\n\n"
            
            for i, meaning in enumerate(meanings, 1):
                # Eğer hedef dil İngilizce değilse, anlamı hedef dile tekrar çevir
                display_meaning = meaning
                if dest_code != "en":
                    try:
                        translated_meaning = translator.translate(meaning, src="en", dest=dest_code)
                        display_meaning = translated_meaning.text
                    except:
                        pass  # Çevrilemezse İngilizce hali kalır

                # Örnek cümle AI ile oluşturulur
                example = self.generate_sentence_improved(meaning, dest_name, dest_code)
                result_text += f"{i}. {display_meaning}\n"
                result_text += f"    Örnek: {example}\n\n"

            self.result_area.setPlainText(result_text)
            
        except Exception as e:
            # Hata durumunda hata mesajını göster
            self.result_area.setPlainText(f"Hata oluştu: {e}")
            
        finally:
            # İşlem bittiğinde ilerleme çubuğunu gizle ve butonu etkinleştir
            self.progress.hide()
            self.translate_button.setEnabled(True)
            
    def get_word_meanings(self, original_word, translated_word):
        """
        Eş sesli Türkçe kelimeler için özel anlam listesi döndürür.
        Diğer kelimelerde yalnızca çeviri sonucunu verir.
        """
        multi_meaning_dict = {
            "ay": ["month", "moon"],
            "at": ["horse", "to throw"],
            "aç": ["open", "be hungry"],
            "alay": ["mock", "regiment"],
            "bin": ["thousand", "to ride"],
            "atlet": ["athlete", "tank top"],
            "bel": ["waist", "trouble"],
            "boğaz": ["throat", "Bosphorus"],
            "çay": ["tea", "stream"],
            "cilt": ["skin", "volume"],
            "bağ": ["vineyard", "tie", "connection"],
            "diz": ["knee", "sequence"],
            "dil": ["tongue", "language"],
            "dolu": ["hail", "full"],
            "ekmek": ["bread", "to spread"],
            "hayır": ["no", "charity"],
            "güç": ["power", "difficulty"],
            "koca": ["husband", "huge"],
            "kazan": ["boiler", "to win"],
            "koy": ["bay", "to put"],
            "iç": ["inside", "drink"],
            "in": ["cave", "go down"],
            "pazar": ["market", "Sunday"],
            "ocak": ["stove", "January"],
            "soluk": ["breath", "pale"],
            "satır": ["line", "cleaver"],
            "sağ": ["right", "alive"],
            "yaz": ["summer", "write"],
            "yat": ["yacht", "lie down"],
            "yaş": ["wet", "age"],
            "yar": ["lover", "wound"],
            "yüz": ["face", "hundred", "swim"],
            "sıra": ["row", "turn"]
        }

        src_lang = languages[self.source_lang.currentText()]

        if src_lang == "tr" and original_word.lower() in multi_meaning_dict:
            return multi_meaning_dict[original_word.lower()]
        else:
            return [translated_word]

            
    def generate_sentence_improved(self, word, target_language_name, target_language_code):
        """
        Gemini API kullanarak belirli bir kelime için, belirtilen hedef dilde örnek cümle oluşturur.
        Prompt, mentörünün önerdiği gibi sabit tutulmuştur ve hedef dil dinamik olarak eklenir.
        """
        # Sabit ve optimize edilmiş prompt
        prompt = f"""Create a simple, clear sentence in {target_language_name} using the word "{word}".
Rules:
- Use the word in its most common meaning.
- Keep the sentence under 12 words.
- Make it grammatically correct.
- Use simple, everyday vocabulary.
- Ensure the sentence sounds natural to a native speaker of {target_language_name}.
- Only return the sentence. Do NOT include any prefixes, labels, or extra text.
"""
        
        # Gemini API anahtarı (Kendi anahtarını buraya yapıştıracaksın!)
        # Google AI Studio'dan alabilirsin: https://aistudio.google.com/
        
        import config
        api_key = config.GEMINI_API_KEY
        
        # Gemini API uç noktası
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

        # API'ye gönderilecek payload (istek gövdesi)
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        }

        try:
            # API'ye POST isteği gönder
            response = requests.post(api_url, headers={'Content-Type': 'application/json'}, json=payload)
            response.raise_for_status() # HTTP hataları (4xx veya 5xx) için hata fırlat
            result = response.json() # Yanıtı JSON olarak ayrıştır

            # Hata ayıklama için ham yanıtı konsola yazdır
            print(f"Gemini API Response for '{word}' in {target_language_name}: {result}")

            # API yanıtından cümleyi çıkar
            if result.get("candidates") and len(result["candidates"]) > 0 and \
               result["candidates"][0].get("content") and \
               result["candidates"][0]["content"].get("parts") and \
               len(result["candidates"][0]["content"]["parts"]) > 0:
                sentence = result["candidates"][0]["content"].get("parts")[0].get("text", "").strip()

                # Oluşturulan cümlenin çok uzun olup olmadığını veya boş olup olmadığını kontrol et
                # Ayrıca, eğer model hala prompt'un bir kısmını döndürüyorsa veya anlamsızsa
                if len(sentence.split()) > 15 or not sentence or sentence.lower().startswith("create a simple"):
                    return self.create_simple_sentence(word) # Geçersizse basit bir cümle döndür
                
                return sentence
            else:
                # API'den beklenen yanıt gelmezse konsola hata yaz ve basit cümle döndür
                print(f"Gemini API'den beklenen yanıt gelmedi veya boş: {result}")
                return self.create_simple_sentence(word)

        except requests.exceptions.RequestException as e:
            # API isteği sırasında ağ hatası vb. oluşursa
            print(f"API isteği sırasında hata oluştu: {e}")
            return self.create_simple_sentence(word)
        except json.JSONDecodeError as e:
            # API yanıtı JSON olarak ayrıştırılamazsa
            print(f"API yanıtı JSON olarak ayrıştırılamadı: {e}")
            return self.create_simple_sentence(word)
        except Exception as e:
            # Diğer tüm beklenmedik hatalar için
            print(f"Beklenmedik bir hata oluştu: {e}")
            return self.create_simple_sentence(word)
            
    def create_simple_sentence(self, word):
        """
        Yapay zeka modelinden bir cümle alınamazsa kullanılacak basit cümle şablonları.
        Bu, bir yedek mekanizmadır ve şu an için İngilizce odaklıdır.
        """
        templates = {
            "month": "January is the first month of the year.",
            "moon": "The moon shines brightly at night.",
            "book": "I love reading a good book.",
            "light": "Please turn on the light.",
            "water": "Water is essential for life.",
            "house": "They live in a beautiful house.",
            "car": "He drives a red car.",
            "time": "Time passes very quickly.",
            "day": "Today is a beautiful day.",
            "night": "The night sky is full of stars."
        }
        
        if word.lower() in templates:
            return templates[word.lower()]
        else:
            return f"The word '{word}' is commonly used in English."

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DictionaryApp()
    ex.show()
    sys.exit(app.exec_())
