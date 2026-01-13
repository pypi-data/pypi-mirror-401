from gen.config import EXTENSION_MAP


# Prints the Language Templetes
def list_langtemplates():
    for ext, lang in EXTENSION_MAP.items():
        print(lang)
