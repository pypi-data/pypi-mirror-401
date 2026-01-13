import os

from gen.config import EXTENSION_MAP

working_dir = os.getcwd()


def gen_langtemplate(file, extension, flag=None):
    if file and extension:
        lang = EXTENSION_MAP.get(extension)
        filename = file + extension

        current_dir = os.path.dirname(__file__)  # Gets the parent dir of lib
        template_name = f"main{extension}"
        template_path = os.path.join(
            current_dir, "..", "templates", lang, template_name
        )

        abs_path = os.path.join(working_dir, filename)  # Gives absolute path

        # print(template_path)
        with open(template_path, "r") as template:
            # Reads the template (main.*)
            content = template.read()
        if flag is None:
            if os.path.isfile(abs_path):  # check weather file exists
                print("File is already exists")
            else:
                with open(abs_path, "w") as file:
                    file.write(content)
                    print(f"{filename} created!")
        else:
            if flag == "--dryrun":
                print(content)
            elif flag == "--overwrite":
                with open(abs_path, "w") as file:
                    file.write(content)
                    print(f"{filename} overwrited!")
    else:
        pass
