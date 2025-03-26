import os
from pathlib import Path
import logging
from clang.cindex import CompilationDatabase
from ast_graph_generator.lib import create_ast_graph_from_file_with_args
from tqdm import tqdm



def main():

    directory = "/home/antoine/Documents/codde-analyser"
    os.chdir(directory)

    export_dir = '.'

    source_file = "sep_test/Actions.cpp"
    args = "-c -I./sep_test"
    args = args.split()

    filtered_args = []
    for arg in args:
        if not (arg.startswith('-o')): # or arg.startswith('-W')
            filtered_args.append(arg)

    logging.basicConfig(level=logging.DEBUG)

    create_ast_graph_from_file_with_args(source_file, filtered_args, export_dir)
    

if __name__ == "__main__":
    main()
