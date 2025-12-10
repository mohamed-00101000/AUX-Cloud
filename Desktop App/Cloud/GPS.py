from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView


class GPSMapWidget(QWidget):
    """
    A widget to display live GPS coordinates on a map using Leaflet.js and PyQt.
    """

    def __init__(self, gps_coords_list):
        """
        Initialize the GPSMapWidget.

        :param gps_coords_list: List of (latitude, longitude) tuples
        """
        super().__init__()
        self.setWindowTitle("Live GPS Tracker")

        # Initialize the index for updating coordinates
        self.gps_coords_list = gps_coords_list
        self.current_index = 0

        # Create a lay  out
        layout = QVBoxLayout()

        # Create the map view (QWebEngineView)
        self.map_widget = QWebEngineView()
        layout.addWidget(self.map_widget)

        # Set the layout
        self.setLayout(layout)

        # Generate and load the initial map template
        if len(self.gps_coords_list) > 0:
            initial_coords = self.gps_coords_list[0]
        else:
            initial_coords = (0, 0)

        self.map_template = self.create_map_template(initial_coords)
        self.map_widget.setHtml(self.map_template)

        # Create a QTimer to update the map dynamically
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_map)
        # self.timer.start(800)  # Refresh every 0.8 seconds

    def create_map_template(self, initial_coords):
        """
        Generate the initial HTML template for the map.

        :param initial_coords: Tuple of (latitude, longitude)
        :return: HTML template as a string
        """
        lat, lon = initial_coords
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Live GPS Tracker</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
            <style>
                #map {{ height: 100vh; width: 100%; }}
                body {{ margin: 0; padding: 0; }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
            <script>
                // Initialize the map
                var map = L.map('map').setView([{lat}, {lon}], 17);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);

                // Initialize a circle marker for the current position
                var marker = L.circleMarker([{lat}, {lon}], {{
                    radius: 6,
                    color: 'blue',
                    fillColor: 'red',
                    fillOpacity: 1.0,
                    weight: 2
                }}).addTo(map);

                // Add a polyline to track the path
                var path = L.polyline([], {{ color: 'blue' }}).addTo(map);

                // Function to update the marker position and path
                function updateMarker(lat, lon) {{
                    marker.setLatLng([lat, lon]); // Move the marker
                    path.addLatLng([lat, lon]); // Extend the path
                    map.panTo([lat, lon]); // Pan the map to the new location
                }}

                // Expose the updateMarker function globally
                window.updateMarker = updateMarker;
            </script>
        </body>
        </html>
        """


    def update_vehicle_position(self, lat, lon):
        js_code = f"updateMarker({lat}, {lon});"
        self.map_widget.page().runJavaScript(js_code)

    # def update_map(self):
    #     """
    #     Update the map with the current GPS coordinates.
    #     """
    #     # Get the current GPS coordinates
    #     gps_coords = self.gps_coords_list[self.current_index]
    #     lat, lon = gps_coords

    #     # Call the JavaScript function to update the marker position
    #     js_code = f"updateMarker({lat}, {lon});"
    #     self.map_widget.page().runJavaScript(js_code)

    #     # Move to the next set of coordinates, loop back if at the end
    #     self.current_index = (self.current_index + 10) % len(self.gps_coords_list)


# Function to load GPS data from a tab-delimited CSV file
# def load_track_data(file_path):
#     gps_coords = []
#     try:
#         with open(file_path, mode='r', encoding='utf-8') as file:
#             for line in file:  # Read the file line by line
#                 row = line.strip().split('\t')  # Split line by tab
#                 try:
#                     # Extract latitude and longitude from the correct columns
#                     lat = float(row[1])  # Assuming latitude is in column 2
#                     lon = float(row[2])  # Assuming longitude is in column 3
#                     gps_coords.append((lat, lon))
#                 except (ValueError, IndexError):
#                     print(f"Skipping invalid row: {row}")  # Log invalid rows
#     except Exception as e:
#         print(f"Error reading file: {e}")
#     return gps_coords
