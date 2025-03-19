from clang.cindex import CompilationDatabase

# Charger la compilation database depuis le répertoire de build
cdb = CompilationDatabase.fromDirectory("/chemin/vers/le/repertoire/de/build")

compile_cmds = cdb.getCompileCommands("mon_fichier.cpp")
if compile_cmds is None:
    print("Aucune commande trouvée pour ce fichier.")
else:
    for cmd in compile_cmds:
        # Affiche la commande complète et les arguments
        print("Commande:", " ".join(cmd.arguments))
        print("Répertoire de travail:", cmd.directory)
        print("Fichier source:", cmd.filename)
        print("Fichier de sortie:", cmd.output)


from clang.cindex import Index

index = Index.create()
# Supposons que vous récupérez la première commande disponible
cmds = list(compile_cmds)
if cmds:
    args = list(cmds[0].arguments)[1:]  # On ignore le premier argument (l'exécutable)
    tu = index.parse("mon_fichier.cpp", args=args)
    print("AST généré pour mon_fichier.cpp")

# ajouter ceci aux files de scons 
env = Environment(COMPILATIONDB_USE_ABSPATH=True)
env.Tool('compilation_db')
env.CompilationDatabase()
