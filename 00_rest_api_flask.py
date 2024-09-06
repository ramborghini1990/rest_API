from flask import Flask, request, jsonify
import geopandas as gpd
import pandas as pd

app = Flask(__name__)

# Load your geojson and SING data once (outside the route for efficiency)
primary_cabins = gpd.read_file(r"D:\dev\synthetic-grids\synth-grids\repositories\primary_cabins.geojson")
consumption_profiles =  pd.read_csv('consumption_profiles.csv')  # Assuming your SING data is in CSV format

# Example function to filter substations, borders, and buildings based on IDs
def get_filtered_data(substation_id, border_id, building_id):
    # Filter the geojson data (primary_cabins) based on input IDs
    filtered_geo = primary_cabins[
        (primary_cabins['substation_id'] == substation_id) &
        (primary_cabins['border_id'] == border_id) &
        (primary_cabins['building_id'] == building_id)
    ]
    
    # Lookup in the consumption profiles data
    consumption_data = consumption_profiles[consumption_profiles['substation_id'] == substation_id]

    return filtered_geo, consumption_data

@app.route('/api/process', methods=['POST'])
def process_data():
    # Get JSON data from the POST request
    data = request.get_json()
    
    substation_id = data.get('substation_id')
    border_id = data.get('border_id')
    building_id = data.get('building_id')
    
    if not all([substation_id, border_id, building_id]):
        return jsonify({"error": "Missing one or more required fields (substation_id, border_id, building_id)"}), 400
    
    # Get filtered data
    filtered_geo, consumption_data = get_filtered_data(substation_id, border_id, building_id)
    
    # Prepare response
    response = {
        "filtered_geo": filtered_geo.to_json(),
        "consumption_profile": consumption_data.to_dict(orient='records')
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
