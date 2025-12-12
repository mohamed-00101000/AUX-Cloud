from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer
import traceback


class GPSMapWidget(QWidget):
    """
    Clean, stable GPS map widget using Leaflet + PyQt
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # WebEngine map widget
        self.map_widget = QWebEngineView()
        layout.addWidget(self.map_widget)
        self.setLayout(layout)

        # State control
        self.map_ready = False

        # Load map HTML
        self.load_map_html()

        # Delay binding updateMarker() to ensure JS is fully loaded
        QTimer.singleShot(1000, self.enable_updates)

    # -------------------------------------------------------
    # Load leaflet map
    # -------------------------------------------------------
    def load_map_html(self):
        lat = 0
        lon = 0

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>GPS Map</title>
            <meta charset="utf-8" />
            <link rel="stylesheet"
                href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
            <style>
                html, body {{ margin: 0; height: 100%; overflow: hidden; }}
                #map {{ height: 100%; width: 100%; }}
            </style>
        </head>

        <body>
            <div id="map"></div>

            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
            <script>

                // Initialize the map
                var map = L.map('map').setView([{lat}, {lon}], 17);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);

                // Marker
                var marker = L.circleMarker([{lat}, {lon}], {{
                    radius: 7,
                    color: 'blue',
                    fillColor: 'red',
                    fillOpacity: 1.0,
                    weight: 2
                }}).addTo(map);

                // Path polyline
                var path = L.polyline([], {{ color: 'blue' }}).addTo(map);

                // Update function
                function updateMarker(lat, lon) {{
                    marker.setLatLng([lat, lon]);
                    path.addLatLng([lat, lon]);
                    map.panTo([lat, lon]);
                }}

                window.updateMarker = updateMarker;
            </script>
        </body>
        </html>
        """

        self.map_widget.setHtml(html)

    # -------------------------------------------------------
    # Map is ready to receive updates after initial load
    # -------------------------------------------------------
    def enable_updates(self):
        self.map_ready = True
        print("[GPS] Map is ready for updates.")

    # -------------------------------------------------------
    # Called by back.py to update vehicle position
    # -------------------------------------------------------
    def update_vehicle_position(self, lat, lon):
        if not self.map_ready:
            print("[GPS] Map not ready yet, skipping update...")
            return

        try:
            js = f"updateMarker({lat}, {lon});"
            self.map_widget.page().runJavaScript(js)
        except Exception as e:
            print(f"[GPS ERROR] {e}")
            traceback.print_exc()
