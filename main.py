from app import app
from callbacks import get_callbacks
from dash import html
from layout import serve_layout


if __name__ == "__main__":
    app.layout = serve_layout
    get_callbacks(app)
    app.run(debug=True)
