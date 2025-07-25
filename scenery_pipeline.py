# scenery_pipeline.py
from pathlib import Path
import subprocess
from datetime import datetime
import sys
import shutil
import zipfile
import os

def init_scenery():
    sceneria = input("📦 Podaj nazwę katalogu scenerii: ").strip()
    katalog = Path(sceneria)
    if not katalog.exists():
        print(f"❌ Katalog '{sceneria}' nie istnieje.")
        return None
    Path("tmp").mkdir(exist_ok=True)
    Path("tmp/sceneria.txt").write_text(sceneria, encoding="utf-8")

    #apt_path = katalog / "apt.dat"
    apt_files = list(katalog.rglob("apt.dat"))
    if not apt_files:
        print(f"❌ Nie znaleziono pliku 'apt.dat' w katalogu '{sceneria}'")
        return None

    apt_path = apt_files[0]  # pierwszy znaleziony

    if not apt_path.exists():
        print(f"❌ Brak pliku 'apt.dat' w katalogu '{sceneria}'")
        return None

    try:
        lines = apt_path.read_text(encoding="utf-8").splitlines()
        wersja = lines[1].strip() if len(lines) > 1 else "BRAK"
    except Exception as e:
        print(f"❌ Błąd przy odczycie 'apt.dat': {e}")
        return None

    Path("raporty").mkdir(exist_ok=True)
    with Path("raporty/log.txt").open("a", encoding="utf-8") as log:
        log.write(f"Sceneria: {sceneria}, apt.dat wersja: {wersja}\n")

    if not wersja.startswith("1200"):
        print(f"⚠️ Nieobsługiwana wersja apt.dat: {wersja}. Zatrzymano działanie.")
        return None

    Path("tmp").mkdir(exist_ok=True)
    Path("tmp/sceneria.txt").write_text(sceneria, encoding="utf-8")
    print(f"✅ Sceneria '{sceneria}' zaakceptowana. Wersja apt.dat: {wersja}")

    return sceneria

def pobierz_sciezke_scenerii():
    sc_path = Path("tmp/sceneria.txt")
    if not sc_path.exists():
        print("❌ Nie znaleziono pliku tmp/sceneria.txt. Uruchom najpierw init_scenery()")
        return None
    return sc_path.read_text(encoding="utf-8").strip()

def konwertuj_dsf_na_tekst(scenery_path, output_path):
    Path("tmp").mkdir(parents=True, exist_ok=True)
    dsf_files = list(Path(scenery_path).rglob("*.dsf"))
    if not dsf_files:
        print("❌ Nie znaleziono plików DSF w:", scenery_path)
        return False

    with output_path.open("w", encoding="utf-8") as output_file:
        for dsf in dsf_files:
            temp_txt = Path("tmp") / f"{dsf.stem}.txt"
            command = [
                "xptools/tools/DSFTool",
                "--dsf2text",
                str(dsf),
                str(temp_txt)
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Przetworzono: {dsf.name}")
                text = temp_txt.read_text(encoding="utf-8")
                output_file.write(f"### {dsf.name} ###\n{text}\n\n")
            else:
                print(f"❌ Błąd dla pliku {dsf.name}:\n{result.stderr}")
    return True

def wypisz_i_zapisz_definicje():
    input_path = Path("tmp/output.txt")
    output_path = Path("tmp/output2.txt")

    if not input_path.exists():
        print("❌ Plik tmp/output.txt nie istnieje.")
        return

    with input_path.open(encoding="utf-8") as infile, output_path.open("w", encoding="utf-8") as outfile:
        for linia in infile:
            if linia.startswith("OBJECT_DEF") or linia.startswith("POLYGON_DEF"):
                outfile.write(linia)

    print("📄 Zapisano linie OBJECT_DEF i POLYGON_DEF do tmp/output2.txt")

def przetworz_output_do_output3():
    wejscie = Path("tmp/output2.txt")
    wyjscie = Path("tmp/output3.txt")

    if not wejscie.exists():
        print("❌ Nie znaleziono pliku:", wejscie)
        return

    wynik = []
    with wejscie.open("r", encoding="utf-8") as f:
        for linia in f:
            czesci = linia.strip().split()
            if len(czesci) > 1:
                oczyszczona = ''.join(czesci[1:])
                wynik.append(oczyszczona + "\n")
            else:
                wynik.append("\n")

    wyjscie.parent.mkdir(parents=True, exist_ok=True)
    with wyjscie.open("w", encoding="utf-8") as f:
        f.writelines(wynik)

    print("✅ Zapisano wynik do tmp/output3.txt")

def rozdziel_obiekty():
    input_file = Path("tmp/output3.txt")
    sceneria_file = Path("tmp/sceneria.txt")

    if not sceneria_file.exists():
        print("❌ Brak pliku tmp/sceneria.txt z nazwą katalogu scenerii.")
        return

    scenery_path = sceneria_file.read_text(encoding="utf-8").strip()
    scenery_folder = Path(scenery_path).name  # np. EPPG_Scenery_Pack_12

    lokalne = []
    zewnetrzne = []

    if not input_file.exists():
        print("❌ Brak pliku tmp/output3.txt")
        return

    with input_file.open("r", encoding="utf-8") as f:
        for linia in f:
            obiekt = linia.strip()
            lokalna_sciezka = Path(scenery_path) / obiekt
            if lokalna_sciezka.exists():
                
                lokalne.append(f"{scenery_folder}/{obiekt}")
                #lokalne.append(obiekt)
            else:
                zewnetrzne.append(obiekt)

    Path("tmp").mkdir(exist_ok=True)
    Path("tmp/lokalne.txt").write_text("\n".join(lokalne), encoding="utf-8")
    Path("tmp/zewnetrzne.txt").write_text("\n".join(zewnetrzne), encoding="utf-8")

    print(f"✅ Lokalnych obiektów: {len(lokalne)}")
    print(f"⚠️ Zewnętrznych obiektów: {len(zewnetrzne)}")
    print("📁 Zapisano raporty w folderze 'tmp'")   
     
def wypisz_tekstury(scenery_path):
    input_file = Path("tmp/lokalne.txt")
    output_file = Path("tmp/lokalne_tekstury.txt")
    output_file.parent.mkdir(exist_ok=True)

    if not input_file.exists():
        print("❌ Brak pliku:", input_file)
        return

    wynik = []

    with input_file.open("r", encoding="utf-8") as lista_obiektow:
        for linia in lista_obiektow:
            #sciezka_obj = Path(scenery_path) / linia.strip()
            sciezka_obj = Path(linia.strip())
            if sciezka_obj.exists():
                try:
                    with sciezka_obj.open("r", encoding="utf-8") as plik_obj:
                        for linia_obj in plik_obj:
                            if linia_obj.strip().startswith("TEXTURE"):
                                wynik.append(linia_obj.strip())
                except Exception as e:
                    wynik.append(f"❌ Błąd odczytu: {sciezka_obj} → {e}")
            else:
                wynik.append(f"❌ Nie znaleziono pliku: {sciezka_obj}")

    with output_file.open("w", encoding="utf-8") as f_out:
        f_out.write("\n".join(wynik))

    print(f"📄 Zapisano listę tekstur do: {output_file}")

def wyczysc_lokalne_tekstury():
    wejscie = Path("tmp/lokalne_tekstury.txt")
    wyjscie = Path("tmp/lokalne_tekstury_cleaned.txt")

    if not wejscie.exists():
        print("❌ Brak pliku:", wejscie)
        return

    tekstury = set()

    with wejscie.open("r", encoding="utf-8") as f:
        for linia in f:
            parts = linia.strip().split()
            if parts:
                tekstury.add(parts[-1].replace("\r", ""))  # ostatnie pole, bez \r

    wyjscie.parent.mkdir(parents=True, exist_ok=True)
    with wyjscie.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sorted(tekstury)) + "\n")

    print(f"✅ Zapisano oczyszczoną listę tekstur do: {wyjscie}")

def znajdz_tekstury(bazowa_sciezka):
    wejscie = Path("tmp/lokalne_tekstury_cleaned.txt")
    wyjscie = Path("tmp/file3.txt")
    wyjscie.parent.mkdir(exist_ok=True)

    if not wejscie.exists():
        print(f"❌ Brak pliku wejściowego: {wejscie}")
        return

    tekstury = [linia.strip() for linia in wejscie.read_text(encoding="utf-8").splitlines() if linia.strip()]
    znalezione = []

    bazowa = Path(bazowa_sciezka).resolve()

    for root, _, files in os.walk(bazowa):
        for nazwa in tekstury:
            if nazwa in files:
                pelna_sciezka = Path(root) / nazwa
                sciezka_wzgledna = pelna_sciezka.relative_to(Path.cwd())
                znalezione.append(str(sciezka_wzgledna))

    wyjscie.write_text("\n".join(sorted(znalezione)), encoding="utf-8")
    print(f"✅ Zapisano {len(znalezione)} ścieżek względnych do: {wyjscie}")

def buduj_i_pakuj(scenery_path):
    scenery_dir = Path(scenery_path).resolve()
    scenery_name = scenery_dir.name
    release_dir = Path("release") / scenery_name
    release_dir.mkdir(parents=True, exist_ok=True)

    # 1. Połącz pliki
    lokalne = Path("tmp/lokalne.txt")
    file3 = Path("tmp/file3.txt")
    obiekty = Path("tmp/obiekty_do_budowy.txt")

    if not lokalne.exists() or not file3.exists():
        print("❌ Brak plików tmp/lokalne.txt lub tmp/file3.txt")
        return

    linie = lokalne.read_text(encoding="utf-8").splitlines() + file3.read_text(encoding="utf-8").splitlines()
    obiekty.write_text("\n".join(sorted(set(linie))), encoding="utf-8")
    print("📄 Utworzono tmp/obiekty_do_budowy.txt")

    # 2. Kopiuj Earth nav data
    earth_src = scenery_dir / "Earth nav data"
    earth_dst = release_dir / "Earth nav data"
    if earth_src.exists():
        shutil.copytree(earth_src, earth_dst, dirs_exist_ok=True)
        print("✅ Skopiowano Earth nav data")

        # 3. Kopiuj pliki z listy
    for linia in obiekty.read_text(encoding="utf-8").splitlines():
        rel_path = Path(linia.strip())

        # 🛠️ Jeśli ścieżka zaczyna się od nazwy scenerii – obetnij ją
        try:
            if rel_path.parts[0] == scenery_name:
                rel_path = rel_path.relative_to(scenery_name)
        except IndexError:
            continue  # pomiń puste linie

        src = scenery_dir / rel_path
        dst = release_dir / rel_path

        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(src, dst)
                print(f"📁 Skopiowano: {rel_path}")
            except Exception as e:
                print(f"⚠️ Błąd kopiowania {rel_path}: {e}")
        else:
            print(f"⚠️ Nie znaleziono pliku: {src}")


    # 4. Pakuj do ZIP
    zip_path = Path("release") / f"{scenery_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in release_dir.rglob("*"):
            if file.is_file():
                zipf.write(file, arcname=file.relative_to(release_dir))

    print(f"📦 Spakowano paczkę do ZIP: {zip_path}")

from pathlib import Path
import shutil
import zipfile
from datetime import datetime

def sprzataj_i_backupuj():
    sceneria_file = Path("tmp/sceneria.txt")
    if not sceneria_file.exists():
        print("❌ Brak pliku tmp/sceneria.txt")
        return

    scenery_name = sceneria_file.read_text(encoding="utf-8").strip()

    backup_dir = Path("backup")
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_zip_name = f"backup-{scenery_name}_{timestamp}.zip"
    backup_zip_path = backup_dir / backup_zip_name

    # Co pakujemy
    katalogi_do_spakowania = ["tmp", "raporty"]

    with zipfile.ZipFile(backup_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for katalog in katalogi_do_spakowania:
            folder = Path(katalog)
            if folder.exists():
                for file in folder.rglob("*"):
                    if file.is_file():
                        zipf.write(file, arcname=file.relative_to("."))

    print(f"📦 Zrobiono backup do: {backup_zip_path}")

    # Usuwamy zawartość tmp/ i raporty/
    for katalog in katalogi_do_spakowania:
        folder = Path(katalog)
        if folder.exists():
            shutil.rmtree(folder)
            print(f"🧹 Usunięto katalog: {folder}")

