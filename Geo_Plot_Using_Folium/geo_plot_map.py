import os
import sys

def get_color(elevation: float) -> str:
    """Return marker color based on volcano elevation height."""
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

def generate_interactive_map(csv_path: str = None, output_html: str = "map.html") -> str:
    """Generate interactive Folium map with volcano elevation markers."""
    script_dir = os.path.dirname(__file__)
    if csv_path is None:
        csv_path = os.path.join(script_dir, "volcano.csv")

    if not os.path.exists(csv_path):
        print(f"Error: Volcano dataset not found at '{csv_path}'")
        return None

    try:
        import pandas as pd
        import folium
        folium_available = True
    except ImportError:
        folium_available = False

    if not folium_available:
        print("Notice: pandas/folium library not installed. Generating static HTML map fallback...")
        with open(output_html, "w", encoding="utf-8") as f:
            f.write("<html><body><h1>Geo Plot Map Fallback</h1><p>Install folium and pandas to view interactive maps.</p></body></html>")
        return output_html

    try:
        df = pd.read_csv(csv_path)

        # Center map on average lat/lon
        avg_lat = df['LAT'].mean() if 'LAT' in df.columns else 38.5
        avg_lon = df['LON'].mean() if 'LON' in df.columns else -99.0

        map_obj = folium.Map(location=[avg_lat, avg_lon], zoom_start=5, tiles="Stamen Terrain" if hasattr(folium.TileLayer, 'stamen') else "OpenStreetMap")

        fg_volcanoes = folium.FeatureGroup(name="Volcanoes")

        for _, row in df.iterrows():
            name = row.get('NAME', 'Volcano')
            elev = row.get('ELEV', 0)
            lat = row.get('LAT')
            lon = row.get('LON')

            if pd.notna(lat) and pd.notna(lon):
                fg_volcanoes.add_child(
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=6,
                        popup=f"<b>{name}</b><br>Elevation: {elev}m",
                        fill_color=get_color(elev),
                        color='grey',
                        fill_opacity=0.8
                    )
                )

        map_obj.add_child(fg_volcanoes)

        # Process world boundaries if available
        world_json = os.path.join(script_dir, "world.json")
        if os.path.exists(world_json):
            try:
                fg_population = folium.FeatureGroup(name="World Population")
                fg_population.add_child(
                    folium.GeoJson(
                        data=open(world_json, 'r', encoding='utf-8-sig').read(),
                        style_function=lambda x: {
                            'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                            else 'red'
                        }
                    )
                )
                map_obj.add_child(fg_population)
            except Exception as json_err:
                print(f"Notice: World boundaries overlay skipped ({json_err})")

        map_obj.add_child(folium.LayerControl())

        map_obj.save(output_html)
        print(f"Interactive Folium map generated successfully -> {output_html}")
        return output_html
    except Exception as e:
        print(f"Error generating Folium map: {e}")
        return None

def main():
    out_arg = sys.argv[1] if len(sys.argv) > 1 else "map.html"
    generate_interactive_map(output_html=out_arg)

if __name__ == '__main__':
    main()
