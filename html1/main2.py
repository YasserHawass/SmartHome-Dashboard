import dash_dangerously_set_inner_html
import dash
from dash import html
# import dash_html_components as html

app = dash.Dash('')

app.scripts.config.serve_locally = True

app.layout = html.Div([
    dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
        <script type="text/javascript">alert('If you see this alert, then your custom JavaScript script has run!')</script>
    '''),
])

if __name__ == '__main__':
    app.run_server(debug=True)

