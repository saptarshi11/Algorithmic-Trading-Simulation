# Price action mean reversion backtesting
import sys, os, json


from dash import Dash, html, dcc, Input, Output

import build as graph
import api.fetch as api

config = api.get_settings()

app = Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/cyborg/bootstrap.min.css"
    ],
)
server = app.server

# App layout
app.layout = html.Div(
    [
        dcc.Graph(id="candles", style={"height": "125vh"}),
        dcc.Interval(
            id="interval", interval=86400000
        ),  # Set this interval to something low if you want a live chart (2000 = updates every 2000ms)
    ]
)


@app.callback(
    Output("candles", "figure"),
    Input("interval", "n_intervals"),
)
# update_graph() will run every time the app is updated. App will automatically update when you save your code.
def update_graph(n_intervals):

    if config["general"]["simulate"] == True:
        try:
            return graph.simulate()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            print(
                f"\nGraph failed to load: {e} => {exc_type, fname, exc_tb.tb_lineno}\n"
            )
        if not Exception:
            print("\n<========== Graph updated successfully ==========>\n")
    else:
        try:
            return graph.build()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            print(
                f"\nGraph failed to load: {e} => {exc_type, fname, exc_tb.tb_lineno}\n"
            )
        if not Exception:
            print("\n<========== Graph updated successfully ==========>\n")


def main():
    app.run_server(debug=True)
