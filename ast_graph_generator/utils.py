# utils.py
import os
import platform
import clang.cindex
import config

def setup_for_os():
    system = platform.system()
    libclang_path = None

    library_paths = []

    if "Linux" in system:
        # Rechercher libclang.so sur Linux
        
        print(f"Seting includes paths and clang for Linux")

        library_paths += [
            #'/usr/include/c++/11/',
            'stdc++',
        ]

        libclang_path = "/usr/lib64/libclang.so.18.1.8"
        clang.cindex.Config.set_library_file(libclang_path)

    elif "Windows" in system:
        print(f"Seting includes paths and clang for Windows")

    
    return library_paths

def is_subpath(base_path, full_path):
    # Normalize the paths to remove any redundant separators.
    base_path = os.path.normpath(base_path)
    full_path = os.path.normpath(full_path)
    
    # Convert both paths to absolute paths for consistency.
    base_path = os.path.abspath(base_path)
    full_path = os.path.abspath(full_path)
    
    # Check if the full_path starts with the base_path
    return full_path.startswith(base_path + os.sep)

def get_correct_path(file_path):

    return_file_path = ""
    current_path = os.getcwd()

    TALIOS_PATH = config.TALIOS_PATH

    if os.path.isabs(file_path): 
        # le chemin correspond a un include d'un autre fichier
        if is_subpath(TALIOS_PATH, file_path):
            # Entitée d'un fichier du code talios
            abs_file_path = os.path.join(current_path,file_path)
            rel_file_path = os.path.relpath(abs_file_path, TALIOS_PATH)
            return_file_path = rel_file_path

        else:
            # Entitée d'une librairies externe
            return_file_path = file_path

    else : 
        # entitée declarée dans le fichier que l'on est entrain d'analyser 
        # Ou correspond au root node du fichier 
        abs_file_path = os.path.join(current_path,file_path)
        rel_file_path = os.path.relpath(abs_file_path, TALIOS_PATH)
        return_file_path = rel_file_path
        
    return return_file_path
    
