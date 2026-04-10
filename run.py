import ast


# Provide custom ast.Str compatibility for Werkzeug routing
class Str(ast.Constant):
    def __init__(self, s, kind=None):
        super().__init__(value=s, kind=kind)
        self.s = s


ast.Str = Str

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
