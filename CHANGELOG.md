#  Changelog - PackScape

Wszystkie istotne zmiany w projekcie PackScape będą dokumentowane tutaj.

## [v1.0.0] - 2025-08-16

### Dodano
- Inicjalizacja scenerii: walidacja struktury katalogów, plik `apt.dat`
- Konwersja plików `.dsf` do formatu tekstowego za pomocą DSFTool
- Wydobycie ścieżek obiektów i tekstur
- Podział zasobów na lokalne i zewnętrzne
- Weryfikacja brakujących zasobów
- Automatyczne kopiowanie niezbędnych plików
- Generowanie paczki ZIP gotowej do dystrybucji
- Tworzenie raportu HTML i backupu danych

### Zmieniono
- Usprawniono strukturę katalogów projektu
- Zoptymalizowano działanie skryptu `main.py`

### Naprawiono
- Błąd przy konwersji plików `.dsf` na systemie Windows
- Problem z generowaniem raportu HTML przy braku niektórych zasobów

---

## Uwagi
- Projekt dostępny na licencji MIT.
- Wymaga Python 3.9+ oraz narzędzia DSFTool z pakietu X-Plane SDK.

---