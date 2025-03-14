import os
import platform
import clang.cindex

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

