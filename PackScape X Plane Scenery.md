PackScape – X-Plane Scenery Packaging Pipeline

PackScape to narzędzie w Pythonie do automatycznej analizy, porządkowania i pakowania scenerii dla symulatora lotniczego X-Plane.
Umożliwia przekształcenie surowego folderu scenerii w gotową do dystrybucji paczkę .zip, z pełnym raportem i kopią zapasową.
Co robi PackScape?

- Przetwarza pliki DSF (DSFTool)
- Wykrywa i rozdziela lokalne i zewnętrzne obiekty
- Identyfikuje tekstury powiązane z obiektami
- Buduje strukturę finalnej paczki
- Tworzy raporty tekstowe i HTML
- Pakuje do ZIP i wykonuje backup

Przykładowe użycie

python main.py

Aplikacja poprosi o podanie ścieżki do katalogu scenerii, następnie krok po kroku:

    Odczyta wersję apt.dat

    Zdekompiluje DSF do tekstu

    Wydzieli obiekty i tekstury

    Skopiuje potrzebne pliki do katalogu release/

    Spakuje scenerię do ZIP

    Wygeneruje raport i przeniesie logi do backup/

Struktura projektu

PackScape/
├── main.py                   # Główna funkcja uruchamiająca pipeline
├── scenery_pipeline.py       # Zbiór funkcji przetwarzających
├── tmp/                      # Pliki tymczasowe i robocze
├── raporty/                  # Raporty tekstowe i HTML
├── release/                  # Gotowe paczki scenerii
└── backup/                   # Backup logów i plików pomocniczych

Wymagania

    Python 3.8+

    fpdf2 (do generowania raportów PDF/HTML)

    DSFTool (do konwersji .dsf na tekst)

TODO (pomysły na rozwój)

    Obsługa niestandardowych lokalizacji DSFTool

    Sprawdzanie brakujących tekstur

    Interfejs graficzny (GUI)

    Eksport raportu jako PDF

Autor

Mariusz Migut
Repozytorium: github.com/marimigu/PackScape
Inspiracja: Społeczność X-Plane.org
