import os
from pathlib import Path
from clang.cindex import CompilationDatabase
from ast_graph_generator.lib import create_ast_graph_from_file_with_args
from tqdm import tqdm
import config

def find_compile_commands(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        if 'compile_commands.json' in files:
            result.append(os.path.join(root, 'compile_commands.json'))
    return result

def parse_args(args):
    filtered_args = []
    args = args[4:]
    args = args[:-1]
    for arg in args:
        if not (arg.startswith('-T') or arg.startswith('-c') or arg.startswith('-o') or arg == '-fPIC'): # or arg.startswith('-W')
            filtered_args.append(arg)
    return filtered_args

def main():
    talios_path = config.TALIOS_PATH
    graph_save_root = "/users/t0315611/Documents"
    export_root = "ast_gen"
    export_root_path = os.path.join(graph_save_root, export_root)

    try:
        list_json = find_compile_commands(talios_path)
    except Exception as e:
        print(f"Erreur lors de la recherche des fichiers compile_commands.json dans {talios_path}: {e}")
        return

    if not list_json:
        print(f"Aucun fichier 'compile_commands.json' trouvé dans {talios_path}")
        return

    # Utiliser tqdm pour la boucle principale sur les fichiers compile_commands.json
    for compile_commands_json in tqdm(list_json, desc="Traitement des fichiers compile_commands.json"):
        try:
            compile_commands_json_dir = os.path.dirname(compile_commands_json)
            cdb = CompilationDatabase.fromDirectory(compile_commands_json_dir)
            compile_cmds = cdb.getAllCompileCommands()

            if compile_cmds is None:
                print(f"{compile_commands_json} est vide")
                continue

            # Utiliser tqdm pour la boucle interne sur les commandes de compilation
            for comp in tqdm(compile_cmds, desc=f"Traitement des commandes de compilation ({compile_commands_json})"):
                try:
                    args = [arg for arg in comp.arguments]
                    args = parse_args(args)
                    source_file = comp.filename
                    cmd_exec_folder = comp.directory

                    try:
                        os.chdir(cmd_exec_folder)
                    except Exception as e:
                        print(f"Erreur lors du changement de répertoire vers {cmd_exec_folder}: {e}")
                        continue

                    rel_cmd_exec_folder = os.path.relpath(cmd_exec_folder, talios_path).replace("/", "#").replace("\\", "#")
                    
                    export_path = os.path.join(export_root_path, rel_cmd_exec_folder)
                    export_dir = os.path.join(source_file.replace("/", "#").replace("\\", "#"), export_path)
                    #out_name = source_file.replace("/", "#").replace("\\", "#")

                    abs_path = cmd_exec_folder + source_file
                    rel_path_cpp_file = os.path.relpath(abs_path, talios_path)
                    out_name = rel_path_cpp_file.replace("/", "#").replace("\\", "#")

                    try:
                        create_ast_graph_from_file_with_args(source_file, args, export_dir, out_name=out_name)
                    except Exception as e:
                        print(f"Erreur lors de la création du graphe AST pour le fichier {source_file}: {e}")
                        continue  # Continue with the next command despite errors
                except Exception as e:
                    print(f"Erreur lors du traitement des commandes de compilation pour {compile_commands_json}: {e}")
                    continue  # Continue with the next compile command despite errors
        except Exception as e:
            print(f"Erreur lors de la tentative de lecture {compile_commands_json}: {e}")
            continue  # Continue with the next compile_commands.json file despite errors

if __name__ == "__main__":
    main()
