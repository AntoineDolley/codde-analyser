import os
import subprocess
import clang
from ast_graph_generator.lib import create_ast_graph_from_file

def find_cpp_cxx_files(directory):
    # Liste pour stocker les chemins des fichiers trouvés
    found_files = []

    # Parcourir le répertoire et ses sous-répertoires
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.cxx'):
                found_files.append(os.path.join(root, file))
    return found_files

def split_path(found_files):
    split_files = []
    for path in found_files:
        # Utilisation de os.path.relpath pour enlever le ./ si présent
        dir_name = os.path.relpath(os.path.dirname(path), start='.')
        file_name = os.path.basename(path)
        split_files.append((dir_name, file_name))
    return split_files

def replace_extensions(files):
    replaced_files = []
    for dir_name, file_name in files:
        base_name, _ = os.path.splitext(file_name)  # Retirer l'extension existante

        # Ajouter les nouvelles extensions
        replaced_files.append((dir_name, f"{base_name}.o"))
        replaced_files.append((dir_name, f"{base_name}.os"))
        replaced_files.append((dir_name, f"{base_name}.dll"))
    return replaced_files

def execute_scons_command(dir_name, file_name):
    # Commande à exécuter
    command = f"sconsign -d {dir_name} -e {file_name} -i"

    # Exécuter la commande avec subprocess
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Retourner la sortie sans les espaces superflus
    return result.stdout.strip()

def parse_output(output):
    dependencies = []
    lines = output.split("\n")
    for line in lines:
        if line.strip() and not line.startswith("==="):
            dependencies.append(line.strip())
    return dependencies

def filter_dependencies(dependencies):
    filtered_dependencies = []
    for dep in dependencies:
        if not dep.endswith('.o:') and not dep.endswith('.os:') and os.path.splitext(dep)[1]:
            dep_no_colon = dep.rstrip(':')  # Enlever le ':' à la fin
            filtered_dependencies.append(dep_no_colon)
    return filtered_dependencies

def create_ast_graph_for_each_file(dependency_dict, export_format='graphml', output_prefix='graph_output'):
    libclang_path = "/usr/lib64/libclang.so.18.1.8"
    clang.cindex.Config.set_library_file(libclang_path)

    for file_info, dependencies in dependency_dict.items():
        dir_name, base_name = file_info
        source_file = os.path.join(dir_name, f"{base_name}.cpp")
        includes = [os.path.dirname(dep) for dep in dependencies]
        includes = list(set(includes))  # Remove duplicate include paths
        libraries = []  # If you have specific libraries, add them here.
        library_paths = []  # If you have specific library paths, add them here.
        export_file_prefix = f"{output_prefix}_{base_name}"

        if os.path.exists(source_file):  # Check if the source file exists
            print(f"Analyzing: {source_file}")
            create_ast_graph_from_file(source_file, export_format, export_file_name=export_file_prefix, include_paths=includes, library_paths=libraries)
        else:
            print(f"Source file {source_file} does not exist.")

# Spécifiez le répertoire que vous souhaitez parcourir
directory_to_search = '.'

# Trouver les fichiers et les découper en répertoire et nom de fichier
resulting_files = find_cpp_cxx_files(directory_to_search)
split_files = split_path(resulting_files)

# Remplacer les extensions des fichiers
replaced_files = replace_extensions(split_files)

# Dictionnaire pour stocker les dépendances
dependency_dict = {}

# Exécuter la commande scons pour chaque fichier et sauvegarder les dépendances
for dir_name, file_name in replaced_files:
    # Récupérer le nom de base original sans extension pour indexation
    base_name = os.path.splitext(file_name)[0]
    
    # Créer la clé dans le dictionnaire
    file_info = (dir_name, base_name)

    # Initialiser la clé dans le dictionnaire si elle n'existe pas
    if file_info not in dependency_dict:
        dependency_dict[file_info] = []

    # Exécuter la commande et capturer la sortie
    output = execute_scons_command(dir_name, file_name)
    
    # Extraire et filtrer les dépendances
    dependencies = parse_output(output)
    filtered_dependencies = filter_dependencies(dependencies)
    dependency_dict[file_info].extend(filtered_dependencies)

# Analyser chaque fichier source et exporter le graphe
create_ast_graph_for_each_file(dependency_dict)
