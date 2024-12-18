from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import base64
from dash.exceptions import PreventUpdate
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('graphs', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    
    dcc.Upload(
        id='upload-data',  # This ID will be used in the callback to retrieve the uploaded file
        children=html.Div(['Glisser-Déposer ou ', html.A('Choisir un fichier')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.Div(id='charts-container'),
    html.Div(id='dummy-input', children='')
])

# Your Django view URL
url = 'http://127.0.0.1:8000/dash/upload_datasets/'

def fetch_json_data(url, files):
    # Make the POST request with the files
    response = requests.post(url, files=files)

    if response.status_code == 200:
        try:
            # Parse the JSON data from the response
            processed_data = response.json()

            # If the processed_data is a list, assume the first element contains the relevant data
            if isinstance(processed_data, list):
                processed_data = processed_data[0]

            return processed_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
            return None
    else:
        print(f"Error: Failed to upload and process data. Status code: {response.status_code}")
        return None



def generate_chart(chart_data):
    charts = chart_data.get('charts', [])
    chart_divs = []  # Store chart divs in a list
    print('salam')
    for chart in charts:
        chart_type = chart.get('chartType', None)
        if chart_type != 'pie':
            x_axis = chart['xAxis']
            y_axis = chart['yAxis']

        if chart_type == 'bar':
            categories = [value for value in x_axis['categories'] if value is not None]
            plot = dcc.Graph(
                figure={
                    'data': [go.Bar(x=categories, y=y_axis['values'])],
                    'layout': go.Layout(title=f"{x_axis['label']} vs {y_axis['label']}")
                }
            )
        elif chart_type == 'line':
            plot = dcc.Graph(
                figure={
                    'data': [go.Scatter(x=chart['xAxis']['categories'], y=chart['yAxis']['values'], mode='lines')],
                    'layout': go.Layout(title=f"{chart['xAxis']['label']} vs {chart['yAxis']['label']}")
                }
            )
        
        elif chart_type == 'pie':
            if isinstance(chart['values'], dict):
                print('ok')
            else:
    # Handle the case when chart['values'] is not a list of dictionaries
                print("empty")
            plot = dcc.Graph(
                figure={
                    'data': [go.Pie(labels=chart['values']['labels'], values=chart['values']['percentage'])],
                    'layout': go.Layout(title=f"{chart['label']} Distribution")
                }
            )
        elif chart_type == 'scatter':
            plot = dcc.Graph(
                figure={
                    'data': [go.Scatter(x=chart['xAxis']['values'], y=chart['yAxis']['values'], mode='markers')],
                    'layout': go.Layout(title=f"{chart['xAxis']['label']} vs {chart['yAxis']['label']}")
                }
            )
        else:
            continue

        chart_divs.append(html.Div(plot))  # Append each chart div to the list
        print('salam2')
    return chart_divs

# ... (existing code)



@app.callback(
    Output('charts-container', 'children'),
    [Input('upload-data', 'contents'), Input('upload-data', 'filename')]  # Use the uploaded file contents and filename as inputs
)
def update_charts(contents, filenames):
    print("Callback triggered.")

    if contents is None:
        raise PreventUpdate

    for content, filename in zip(contents, filenames):
        # Assuming you have a single file upload, use index 0
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            # Save the file temporarily on the server-side
            temp_dir = 'path/to/temp/'   #Update this with the desired temporary directory
            os.makedirs(temp_dir, exist_ok=True)  # Create the temporary directory if it doesn't exist
            temp_filepath = os.path.join(temp_dir, filename)  # Full path to the temporary file
            with open(temp_filepath, 'wb') as f:
                f.write(decoded)
            # The file is directly received as a parameter in the callback function
            files = {'dataset_files': open(temp_filepath, 'rb')}
            # Fetch the processed JSON data from the Django view
            print('salam')
            data = fetch_json_data(url, files)
            print('salam')
            print(data)

            try:
                print('me')
                
            except json.JSONDecodeError:
                return html.Div("Table contient des données éronnées, veuillez réctifier votre table.")
            

            if data:
                # Generate charts using the fetched JSON data
                print(data)
                return generate_chart(data)
            else:
                return html.Div("Error: Failed to fetch JSON data")

        except Exception as e:
            print(f"Error during file processing: {e}")

    # If there's no uploaded file or an error occurred during processing
    return html.Div("Error: Please upload a file and try again.")

if __name__ == '__main__':
    print("Starting the server...")
    app.run_server(debug=True)

