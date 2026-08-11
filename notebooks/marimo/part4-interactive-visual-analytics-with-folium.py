import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <p style="text-align:center">
        <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork865-2023-01-01">
        <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo"  />
        </a>
    </p>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Launch Sites Locations Analysis with Folium**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Estimated time needed: **40** minutes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The launch success rate may depend on many factors such as payload mass, orbit type, and so on. It may also depend on the location and proximities of a launch site, i.e., the initial position of rocket trajectories. Finding an optimal location for building a launch site certainly involves many factors and hopefully we could discover some of the factors by analyzing the existing launch site locations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the previous exploratory data analysis labs, you have visualized the SpaceX launch dataset using `matplotlib` and `seaborn` and discovered some preliminary correlations between the launch site and success rates. In this lab, you will be performing more interactive visual analytics using `Folium`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Objectives
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This lab contains the following tasks:
    - **TASK 1:** Mark all launch sites on a map
    - **TASK 2:** Mark the success/failed launches for each site on the map
    - **TASK 3:** Calculate the distances between a launch site to its proximities

    After completed the above tasks, you should be able to find some geographical patterns about launch sites.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's first import required Python packages for this lab:
    """)
    return


@app.cell
def _():
    import folium
    import wget
    import pandas as pd

    return folium, pd


@app.cell
def _():
    from folium.plugins import MarkerCluster
    from folium.plugins import MousePosition
    from folium.features import DivIcon

    return DivIcon, MarkerCluster, MousePosition


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you need to refresh your memory about folium, you may download and refer to this previous folium lab:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Generating Maps with Python](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/DV0101EN-3-5-1-Generating-Maps-in-Python-py-v2.0.ipynb)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 1: Mark all launch sites on a map
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, let's try to add each site's location on a map using site's latitude and longitude coordinates
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following dataset with the name `spacex_launch_geo.csv` is an augmented dataset with latitude and longitude added for each site.
    """)
    return


@app.cell
def _(pd):
    # Download and read the `spacex_launch_geo.csv`
    # spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')

    spacex_csv_file = "../../data/spacex_launch_geo.csv"
    spacex_df=pd.read_csv(spacex_csv_file)
    return (spacex_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, you can take a look at what are the coordinates for each site.
    """)
    return


@app.cell
def _(spacex_df):
    spacex_df_1 = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
    launch_sites_df = spacex_df_1.groupby(['Launch Site'], as_index=False).first()
    launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
    launch_sites_df
    return launch_sites_df, spacex_df_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Above coordinates are just plain numbers that can not give you any intuitive insights about where are those launch sites. If you are very good at geography, you can interpret those numbers directly in your mind. If not, that's fine too. Let's visualize those locations by pinning them on a map.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We first need to create a folium `Map` object, with an initial center location to be NASA Johnson Space Center at Houston, Texas.
    """)
    return


@app.cell
def _():
    nasa_coordinate = [29.559684888503615, -95.0830971930759]
    return (nasa_coordinate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _TODO:_  Create and add `folium.Circle` and `folium.Marker` for each launch site on the site map
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An example of folium.Circle:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `folium.Circle(coordinate, radius=1000, color='#000000', fill=True).add_child(folium.Popup(...))`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An example of folium.Marker:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `folium.map.Marker(coordinate, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'label', ))`
    """)
    return


@app.cell
def _(DivIcon, folium, launch_sites_df, nasa_coordinate):
    _site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

    for _, _launch_site in launch_sites_df.iterrows():
        _site_coordinate = [_launch_site["Lat"], _launch_site["Long"]]

        # 1. Circle layer
        _site_circle = folium.Circle(
            _site_coordinate, radius=1000, color="#d35400", fill=True
        )
        _site_circle.add_child(folium.Popup(_launch_site["Launch Site"]))

        # 2. Text Label Marker (offset to the right of the circle)
        _site_marker = folium.map.Marker(
            _site_coordinate,
            icon=DivIcon(
                icon_size=(200, 20),  # Expanded width so text won't line-break
                icon_anchor=(
                    -15,
                    10,
                ),  # Negative X shifts text to the right of the circle center
                html='<div style="font-size: 12px; color:#d35400; white-space: nowrap;"><b>%s</b></div>'
                     % _launch_site["Launch Site"],
            ),
        )

        _site_map.add_child(_site_circle)
        _site_map.add_child(_site_marker)

    _site_map
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The generated map with marked launch sites should look similar to the following:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <center>
        <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_markers.png">
    </center>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, you can explore the map by zoom-in/out the marked areas
    , and try to answer the following questions:
    - Are all launch sites in proximity to the Equator line?
    - Are all launch sites in very close proximity to the coast?

    Also please try to explain your findings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Task 2: Mark the success/failed launches for each site on the map
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates.
    Recall that data frame spacex_df has detailed launch records, and the `class` column indicates if this launch was successful or not
    """)
    return


@app.cell
def _(spacex_df_1):
    spacex_df_1.tail(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, let's create markers for all launch records.
    If a launch was successful `(class=1)`, then we use a green marker and if a launch was failed, we use a red marker `(class=0)`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that a launch only happens in one of the four launch sites, which means many launch records will have the exact same coordinate. Marker clusters can be a good way to simplify a map containing many markers having the same coordinate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _TODO:_ Create a new column in `launch_sites` dataframe called `marker_color` to store the marker colors based on the `class` value
    """)
    return


@app.cell
def _(spacex_df):
    COLOR_SUCCESS = "#009E73"  
    COLOR_FAILURE = "#D55E00"
    COLOR_BARPLOT = "#2B5C8F"
    COLOR_TRENDLINE = "#1F1F1F"

    LINEWIDTH_TRENDLINE = 2.5

    spacex_df["marker_color"] = spacex_df["class"].map(
        {1: COLOR_SUCCESS, 0: COLOR_FAILURE}
    )
    return COLOR_BARPLOT, LINEWIDTH_TRENDLINE


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _TODO:_ For each launch result in `spacex_df` data frame, add a `folium.Marker` to `marker_cluster`
    """)
    return


@app.cell
def _(MarkerCluster, folium, nasa_coordinate, spacex_df):
    _site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
    _marker_cluster = MarkerCluster()

    for _index, _record in spacex_df.iterrows():
        _site_coordinate = [_record["Lat"], _record["Long"]]
        _marker = folium.Marker(
            _site_coordinate,
            icon=folium.Icon(
                color="white", icon_color=_record["marker_color"]
            ),
        )
        _marker_cluster.add_child(_marker)
    _site_map.add_child(_marker_cluster)
    _site_map
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Your updated map may look like the following screenshots:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <center>
        <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_marker_cluster.png">
    </center>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <center>
        <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_marker_cluster_zoomed.png">
    </center>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From the color-labeled markers in marker clusters, you should be able to easily identify which launch sites have relatively high success rates.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # TASK 3: Calculate the distances between a launch site to its proximities
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we need to explore and analyze the proximities of launch sites.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's first add a `MousePosition` on the map to get coordinate for a mouse over a point on the map. As such, while you are exploring the map, you can easily find the coordinates of any points of interests (such as railway)
    """)
    return


@app.cell
def _(MousePosition, folium, nasa_coordinate):
    site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
    # Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
    formatter = 'function(num) {return L.Util.formatNum(num, 5);};'
    mouse_position = MousePosition(position='topright', separator=' Long: ', empty_string='NaN', lng_first=False, num_digits=20, prefix='Lat:', lat_formatter=formatter, lng_formatter=formatter)
    site_map.add_child(mouse_position)
    site_map
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can calculate the distance between two points on the map based on their `Lat` and `Long` values using the following method:
    """)
    return


@app.cell
def _(COLOR_BARPLOT, DivIcon, LINEWIDTH_TRENDLINE, folium):
    from math import sin, cos, sqrt, atan2, radians

    def calculate_distance(lat1, lon1, lat2, lon2):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    def draw_distance_line(site_map, launch_site, closest_point, name):
        distance = calculate_distance(*launch_site, *closest_point)
        distance_marker = folium.Marker(
            closest_point,
            icon=DivIcon(
                icon_size=(200, 20),  # Expanded width so text won't line-break
                icon_anchor=(
                    -15,
                    10,
                ),  # Negative X shifts text to the right of the circle center
                html=f'<div style="font-size: 12; color:{COLOR_BARPLOT}; white-space: nowrap;"><b>{distance:10.2f} KM</b></div>',
            ),
        )
        coordinates = [launch_site, closest_point]
        lines = folium.PolyLine(
            locations=coordinates, weight=LINEWIDTH_TRENDLINE
        )
        site_map.add_child(lines)
        site_map.add_child(distance_marker)

    return (draw_distance_line,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _TODO:_ Draw a `PolyLine` between a launch site to the selected coastline point
    """)
    return


@app.cell
def _(draw_distance_line, folium):
    _launch_site = [28.56325, -80.576]
    _closest_coastline = [28.56327, -80.567]
    _closest_city = [28.38758, -80.605]
    _closest_highway = [28.56349, -80.570]
    _closest_railway = [28.57114, -80.585]

    _site_map = folium.Map(location=_launch_site, zoom_start=11)

    draw_distance_line(_site_map, _launch_site, _closest_city, "City")
    draw_distance_line(_site_map, _launch_site, _closest_highway, "Highway")
    draw_distance_line(_site_map, _launch_site, _closest_railway, "Railway")
    _site_map
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Your updated map with distance line should look like the following screenshot:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <center>
        <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_marker_distance.png">
    </center>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _TODO:_ Similarly, you can draw a line betwee a launch site to its closest city, railway, highway, etc. You need to use `MousePosition` to find the their coordinates on the map first
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A railway map symbol may look like this:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <center>
        <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/railway.png">
    </center>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A highway map symbol may look like this:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <center>
        <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/highway.png">
    </center>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A city map symbol may look like this:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After you plot distance lines to the proximities, you can answer the following questions easily:
    - Are launch sites in close proximity to railways?
    - Are launch sites in close proximity to highways?
    - Are launch sites in close proximity to coastline?
    - Do launch sites keep certain distance away from cities?

    Also please try to explain your findings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Next Steps:

    Now you have discovered many interesting insights related to the launch sites' location using folium, in a very interactive way. Next, you will need to build a dashboard using Ploty Dash on detailed launch records.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Authors
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Yan Luo](https://www.linkedin.com/in/yan-luo-96288783/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork865-2023-01-01)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Other Contributors
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Joseph Santarcangelo
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Change Log
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    |Date (YYYY-MM-DD)|Version|Changed By|Change Description|
    |-|-|-|-|
    |2021-05-26|1.0|Yan|Created the initial version|
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Copyright © 2021 IBM Corporation. All rights reserved.
    """)
    return


if __name__ == "__main__":
    app.run()
