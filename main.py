# main.py
from pathlib import Path
from scenery_pipeline import (
    init_scenery,
    konwertuj_dsf_na_tekst,
    wypisz_i_zapisz_definicje,
    przetworz_output_do_output3,
    rozdziel_obiekty,
    wypisz_tekstury,
    wyczysc_lokalne_tekstury,
    znajdz_tekstury,
    buduj_i_pakuj,
    znajdz_nieuzywane_pliki,
    generuj_raport_html,
    sprzataj_i_backupuj
)

def run_pipeline():
    sceneria = init_scenery()
    if not sceneria:
        print("❌ Nie udało się zainicjować scenerii, przerywam pipeline.")
        return

    output_txt = Path("tmp/output.txt")

    if konwertuj_dsf_na_tekst(sceneria, output_txt):
        wypisz_i_zapisz_definicje()
        przetworz_output_do_output3()
        rozdziel_obiekty()
        wypisz_tekstury(sceneria)
        wyczysc_lokalne_tekstury()
        znajdz_tekstury(sceneria)
        buduj_i_pakuj(sceneria)
        znajdz_nieuzywane_pliki()
        generuj_raport_html()
        sprzataj_i_backupuj()
    else:
        print("❌ Konwersja DSF nie powiodła się, pipeline zatrzymany.")

if __name__ == "__main__":
    run_pipeline()
