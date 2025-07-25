# PackScape-
Narzędzie do analizy i pakowania scenerii X-Plane: konwersja DSF, wykrywanie obiektów, generowanie raportów, budowanie paczek ZIP.

# ✈️ X-Plane Scenery Toolkit

Projekt w Pythonie służący do analizy, oczyszczania i pakowania scenerii dla symulatora lotu **X-Plane**. Automatyzuje wykrywanie zależności, generowanie raportów oraz tworzenie gotowej paczki ZIP ze scenerią.

## 📦 Funkcje aplikacji

- Inicjalizacja scenerii (walidacja struktury katalogów, `apt.dat`)
- Konwersja plików `.dsf` do formatu tekstowego za pomocą `DSFTool`
- Wydobycie ścieżek obiektów i tekstur
- Podział na obiekty lokalne i zewnętrzne
- Weryfikacja brakujących zasobów
- Automatyczne kopiowanie niezbędnych plików
- Generowanie paczki ZIP gotowej do dystrybucji
- Tworzenie raportu HTML i backupu danych

## ⚙️ Wymagania

- Python 3.9+
- Moduły: `fpdf2`, `pathlib`, `shutil`, `zipfile`
- Narzędzie `DSFTool` z pakietu `X-Plane SDK (XPTools)`
- Katalog `xptools/tools/DSFTool` (lokalizacja binarki)

## Zainstaluj zależności:

```bash
pip install fpdf2

🛠 Struktura projektu

projekt/
├── main.py                    # Główny plik uruchamiający cały pipeline
├── scenery_pipeline.py        # Moduł z funkcjami przetwarzania scenerii
├── xptools/tools/DSFTool      # Binarna aplikacja DSFTool (Linux/Windows)
├── tmp/                       # Dane tymczasowe (ścieżki, raporty cząstkowe)
├── raporty/                   # Raporty HTML i logi
├── release/                   # Gotowe spakowane paczki ZIP
├── backup/                    # Archiwalne logi i dane po pakowaniu

🚀 Użycie

1.Umieść katalog scenerii w folderze projektu.
2.Uruchom główny skrypt:

python main.py

3.Postępuj zgodnie z komunikatami w terminalu.
4.Spakowana paczka znajdzie się w release/, a logi w backup/.

📝 Przykładowy raport

Program generuje czytelny raport HTML z podsumowaniem zawartości scenerii i używanych zasobów.

🔐 Licencja

Projekt dostępny na licencji MIT. Używaj swobodnie, ale nie zapomnij o autorze 😉

Projekt hobbystyczny stworzony przez entuzjastę X-Plane i Pythona.


