import os
import clang
from pathlib import Path
import logging
from clang.cindex import CompilationDatabase
from ast_graph_generator.lib import create_ast_graph_from_file_with_args
from tqdm import tqdm



def main():

    
    libclang_path = "/usr/lib64/libclang.so.18.1"
    clang.cindex.Config.set_library_file(libclang_path)

    directory = "/users/t0315611/Documents/codde-analyser-refactoring"
    os.chdir(directory)

    export_dir = '.'

    source_file = "sep_test_2/TestClass.cpp"
    args = "-c -I./sep_test_2"

    source_file = "test_code/src/main.cpp"
    args = "-c -I./test_code/Include"

    # source_file = "test_code/src/test_code.cpp"
    # args = "-c -I./test_code/Include"

    source_file = "sep_test/Actions.cpp"
    args = "-c -I./sep_test/"

    args = args.split()

    filtered_args = []
    for arg in args:
        if not (arg.startswith('-o')): # or arg.startswith('-W')
            filtered_args.append(arg)

    logging.basicConfig(level=logging.DEBUG)

    create_ast_graph_from_file_with_args(source_file, filtered_args, export_dir)
    

if __name__ == "__main__":
    main()
