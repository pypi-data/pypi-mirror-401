HELP_TEXT = """
Gen-CLI: Generate boilerplate and framework templates for multiple programming languages.

Usage:
    gen <command> [options]

Commands:
    list                               List available languages and frameworks.
    doctor                             Check environment and configuration.
    help                               Show this help message.

Options (for `new` command):
    --dry-run                          Show what would be generated without writing files.
    --overwrite                        Overwrite existing files if they exist.
    --project-name <name>              Name to use in templates (default: myapp).
    --author <name>                    Author name to use in templates (optional).

Languages & Frameworks:
    Python:     flask, fastapi, django
    Go:         cli, web
    Rust:       actix, rocket
    C:          standard
    C++:        standard
    Java:       spring, standard
    JavaScript: node, react, vue
    HTML:       standard

Examples:
    # Generate a single file using Python Flask template
    gen new main.py python flask --project-name myapp

    # Generate a full FastAPI project
    gen new myapp python fastapi --dry-run

    # Generate a Go CLI project
    gen new app.go go cli

    # List all supported languages and frameworks
    gen list

    # Check environment
    gen doctor

Help:
    gen help                          Show this message.
"""


def help():
    print(HELP_TEXT)
