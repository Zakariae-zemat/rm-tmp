import os
import shutil

def get_temp_files(temp_dir):
    temp_files = []
    for dirpath, _, filenames in os.walk(temp_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                temp_files.append(fp)
    return temp_files

def get_temp_files_size(temp_files):
    return sum(os.path.getsize(f) for f in temp_files if os.path.exists(f))

def delete_temp_files(temp_files, exclude_files):
    for file_path in temp_files:
        if file_path in exclude_files:
            print(f"Exclusion: {file_path}")
            continue
        try:
            os.unlink(file_path)  # Supprimer fichier/symlink
        except Exception as e:
            print(f"Erreur en supprimant {file_path}: {e}")

def main():
    temp_dir = "/tmp"
    print("Analyse des fichiers temporaires...")
    temp_files = get_temp_files(temp_dir)
    temp_size_before = get_temp_files_size(temp_files)
    
    if not temp_files:
        print("Aucun fichier temporaire à gérer.")
        return
    
    print("Fichiers trouvés :")
    for idx, file in enumerate(temp_files):
        print(f"[{idx}] {file}")
    
    print("Options :")
    print("1. Supprimer tous les fichiers")
    print("2. Choisir des fichiers à ne pas supprimer")
    print("3. Choisir uniquement les fichiers à supprimer")
    print("4. Quitter")
    
    choice = input("Votre choix : ").strip()
    exclude_list = []
    include_list = []
    
    if choice == "2":
        exclude_files = input("Entrez les numéros des fichiers à ne pas supprimer, séparés par des virgules : ").strip()
        exclude_indices = exclude_files.split(',')
        for index in exclude_indices:
            try:
                exclude_list.append(temp_files[int(index.strip())])
            except (ValueError, IndexError):
                print(f"Index invalide ignoré: {index.strip()}")
    elif choice == "3":
        include_files = input("Entrez les numéros des fichiers à supprimer, séparés par des virgules : ").strip()
        include_indices = include_files.split(',')
        for index in include_indices:
            try:
                include_list.append(temp_files[int(index.strip())])
            except (ValueError, IndexError):
                print(f"Index invalide ignoré: {index.strip()}")
        exclude_list = [file for file in temp_files if file not in include_list]
    elif choice == "4":
        print("Opération annulée.")
        return
    
    confirm = input("Voulez-vous continuer la suppression ? (o/n): ").strip().lower()
    if confirm != 'o':
        print("Opération annulée.")
        return
    
    delete_temp_files(temp_files, exclude_list)
    
    temp_size_after = get_temp_files_size(get_temp_files(temp_dir))
    deleted_size = temp_size_before - temp_size_after
    
    print(f"Nettoyage terminé ! Taille des fichiers supprimés: {deleted_size / (1024 * 1024):.2f} Mo")

if __name__ == "__main__":
    main()
