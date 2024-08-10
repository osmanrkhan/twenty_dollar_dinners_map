import pandas as pd

restaurant_list_path = "../assets/restaurant_list.csv"

def generate_marker_js(restaurant_list_filepath=restaurant_list_path):
    articles_df = pd.read_csv(restaurant_list_filepath)
    marker_js = ""
    for index, row in articles_df.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            maps_link = f"https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}"
            marker_js += f"""
            L.marker([{row['Latitude']}, {row['Longitude']}], {{
                icon: L.icon({{
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                    iconSize: [25, 41], // size of the icon
                    iconAnchor: [12, 41], // point of the icon which will correspond to marker's location
                    popupAnchor: [1, -34], // point from which the popup should open relative to the iconAnchor
                    shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
                    shadowSize: [41, 41] // size of the shadow
                }})
            }}).bindPopup(`
                <a href="{row["Article Link"]}" target="_blank" style="color:#9C3127;">{row["Restaurant Name"]}</a><br>
                <a href="{maps_link}" target="_blank" style="color:#9e715f;">Open in Maps</a>
            `).addTo(map);
            """
    return marker_js

def generate_html(marker_js, output_html="../html/dinner_map.html"):
    custom_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HellGate $20 Dinner Restaurant Map</title>
        <style>
            body, html {{
                margin: 0;
                font-family: Arial, Helvetica, sans-serif;
                background-color: #000000;
                color: #FFFFFF;
            }}

            .landing {{
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                background-color: #000000;
                padding: 20px;
            }}

            .landing img {{
                width: 200px;
                margin-bottom: 20px;
            }}

            .landing .welcome-message {{
                font-size: 20px;
                margin-top: 20px;
            }}

            .landing .feedback {{
                font-size: 16px;
                margin-top: 20px;
            }}
            
            .landing .disclaimer-message {{
                font-size: 13px;
                margin-top: 15px;
                font-style: italic;
            }}
            
            .landing a {{
                color: #FFFFFF;
                text-decoration: none;
            }}

            .landing a:hover {{
                text-decoration: underline;
            }}

            .landing .dinner-link {{
                color: #FFA500;
            }}

            .scroll-button {{
                background-color: #9C3127;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                margin-top: 20px;
                font-size: 16px;
            }}

            .scroll-button:hover {{
                background-color: #7A2A22;
            }}

            .map-container {{
                height: 100vh;
                position: relative;
            }}

            #map {{
                height: 100%;
            }}

            .back-button {{
                position: absolute;
                bottom: 10px;
                left: 10px;
                background-color: #9C3127;
                color: white;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                font-size: 16px;
                z-index: 1000;
            }}

            .back-button:hover {{
                background-color: #7A2A22;
            }}
        </style>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    </head>
    <body>

    <div class="landing">
        <img src="../assets/hellgate.png" alt="HellGate Logo">
        <div class="welcome-message">
            Welcome to the HellGate $20 Dinner Map! If you're hungry in the five boroughs, this is the map for you.
        </div>
        <div class="feedback">
            Check out Scott Lynch's <a href="https://hellgatenyc.com/category/20-dinner" target="_blank" class="dinner-link">$20 Dinner column</a> for more!
        </div>
        <div class="feedback">
            And if you wish you could read the reviews, <a href="https://hellgatenyc.com/membership/" target="_blank" class="dinner-link">subscribe to HellGate here.</a>
        </div>
        <div class="disclaimer-message">
            This is in no way, shape, or form, affiliated with Hellgate. It was made by a hungry reader. Ignore the logo.
        </div>
        <div class="disclaimer-message">
            Unfortunately, AI was used to grab the addresses. There may be errors.
        </div>
        <div class="disclaimer-message">
             Enter feedback, musings, compliments, and AI/human errors  at this <a href="https://9cudo6covtz.typeform.com/to/PxZCI52S" target="_blank" class="dinner-link">form</a>
        </div>
        <button class="scroll-button" onclick="scrollToMap()">View Map</button>
    </div>
    <div class="map-container" id="map-container">
        <div id="map"></div>
        <button class="back-button" onclick="scrollToTop()">Back</button>
    </div>

    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script>
        function scrollToMap() {{
            document.getElementById('map-container').scrollIntoView({{ behavior: 'smooth' }});
        }}

        function scrollToTop() {{
            document.body.scrollIntoView({{ behavior: 'smooth' }});
        }}

        document.addEventListener('DOMContentLoaded', function () {{
            var map = L.map('map').setView([40.712776, -74.005974], 12);

            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }}).addTo(map);

            {marker_js}
        }});
    </script>

    </body>
    </html>
    """

    with open(output_html, "w") as file:
        file.write(custom_html)

def drawer(restaurant_list_filepath=restaurant_list_path):
    marker_js = generate_marker_js(restaurant_list_filepath)
    generate_html(marker_js)

# Call the drawer function to generate the HTML
drawer()
