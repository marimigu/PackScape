PackScape.

# X-Plane Scenery Toolkit

Projekt w Pythonie służący do analizy, oczyszczania i pakowania scenerii dla symulatora lotu **X-Plane**. Automatyzuje wykrywanie zależności, generowanie raportów oraz tworzenie gotowej paczki ZIP ze scenerią.

A Python project for analyzing, cleaning, and packaging scenery for X-Plane flight simulator. It automates dependency detection, report generation, and the creation of a finished scenery ZIP package.

## Funkcje aplikacji

- Inicjalizacja scenerii (walidacja struktury katalogów, `apt.dat`)
- Konwersja plików `.dsf` do formatu tekstowego za pomocą `DSFTool`
- Wydobycie ścieżek obiektów i tekstur
- Podział na obiekty lokalne i zewnętrzne
- Automatyczne kopiowanie niezbędnych plików
- Generowanie paczki ZIP gotowej do dystrybucji
- Tworzenie raportu HTML i backupu danych

## Wymagania

- Python 3.9+
- Narzędzie `DSFTool` z pakietu `X-Plane SDK (XPTools)`
- Katalog `xptools/tools/DSFTool` (lokalizacja binarki)
- Działa na Windows, Debian

### Struktura projektu
```
projekt/
├── main.py                    # Główny plik uruchamiający cały pipeline
├── scenery_pipeline.py        # Moduł z funkcjami przetwarzania scenerii
├── xptools/tools/DSFTool      # Binarna aplikacja DSFTool (Linux/Windows)
├── tmp/                       # Dane tymczasowe (ścieżki, raporty cząstkowe)
├── raporty/                   # Raporty i logi
├── release/                   # Gotowe spakowane paczki ZIP
├── backup/                    # Archiwalne logi i dane po pakowaniu
```
## Użycie

1. Umieść katalog scenerii w folderze projektu.
2. Uruchom główny skrypt:
    > python main.py
3. Postępuj zgodnie z komunikatami w terminalu.
4. Spakowana paczka znajdzie się w release/, a logi w backup/.

## Usage

1. Place the scenery directory in the project folder.
2. Run the main script:
	> python main.py
3. Follow the prompts in the terminal.
4. The zipped package will be located in release/, and the logs will be located in backup/.

## Pomysły na rozwój
- Obsługa niestandardowych lokalizacji DSFTool
- Sprawdzanie brakujących tekstur
- Interfejs graficzny (GUI)
- Eksport raportu jak  HTML lub PDF

## Ideas for Future Development
- Support for custom DSFTool locations
- Missing texture detection
- Graphical User Interface (GUI)
- Report export as HTML or PDF


## Autor
Mariusz Migut

Repository: github.com/marimigu/PackScape

Inspired by: The [X-Plane.org](https://forums.x-plane.org/) community.

[The project has its own website](https://marimigu.github.io/PackScape/)

