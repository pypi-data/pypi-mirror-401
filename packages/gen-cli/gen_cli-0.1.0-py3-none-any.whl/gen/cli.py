import sys

from gen.commands import helper, list_, template


def main():
    if len(sys.argv) < 2:
        helper.help()
        return

    cmd = sys.argv[1]

    if cmd in ("--list", "list"):
        list_.list_langtemplates()
    elif cmd in ["-h", "--help", "help"]:
        helper.help()
    elif "." in cmd:
        parts = sys.argv[1].split(".")

        filename, extension = parts[0], "." + parts[1]

        flag = sys.argv[2] if len(sys.argv) > 2 else None

        if flag:
            template.gen_langtemplate(filename, extension, flag=flag)
        else:
            template.gen_langtemplate(filename, extension)
    else:
        helper.help()
