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
    # **Space X  Falcon 9 First Stage Landing Prediction**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lab 2: Data wrangling
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Estimated time needed: **60** minutes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this lab, we will perform some Exploratory Data Analysis (EDA) to find some patterns in the data and determine what would be the label for training supervised models.

    In the data set, there are several different cases where the booster did not land successfully. Sometimes a landing was attempted but failed due to an accident; for example, <code>True Ocean</code> means the mission outcome was successfully  landed to a specific region of the ocean while <code>False Ocean</code> means the mission outcome was unsuccessfully landed to a specific region of the ocean. <code>True RTLS</code> means the mission outcome was successfully  landed to a ground pad <code>False RTLS</code> means the mission outcome was unsuccessfully landed to a ground pad.<code>True ASDS</code> means the mission outcome was successfully landed on  a drone ship <code>False ASDS</code> means the mission outcome was unsuccessfully landed on a drone ship.

    In this lab we will mainly convert those outcomes into Training Labels with `1` means the booster successfully landed `0` means it was unsuccessful.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Falcon 9 first stage will land successfully
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/landing_1.gif)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Several examples of an unsuccessful landing are shown here:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/crash.gif)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Objectives
    Perform exploratory  Data Analysis and determine Training Labels

    - Exploratory Data Analysis
    - Determine Training Labels
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ----
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Import Libraries and Define Auxiliary Functions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will import the following libraries.
    """)
    return


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Data Analysis
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Load Space X dataset, from last section.
    """)
    return


@app.cell
def _(pd):
    df=pd.read_csv("../data/dataset_part_1.csv")
    df.head(10)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Identify and calculate the percentage of the missing values in each attribute
    """)
    return


@app.cell
def _(df):
    df.isnull().sum()/len(df)*100
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Identify which columns are numerical and categorical:
    """)
    return


@app.cell
def _(df):
    df.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK 1: Calculate the number of launches on each site

    The data contains several Space X  launch facilities: <a href='https://en.wikipedia.org/wiki/List_of_Cape_Canaveral_and_Merritt_Island_launch_sites'>Cape Canaveral Space</a> Launch Complex 40  <b>VAFB SLC 4E </b> , Vandenberg Air Force Base Space Launch Complex 4E <b>(SLC-4E)</b>, Kennedy Space Center Launch Complex 39A <b>KSC LC 39A </b>.The location of each Launch Is placed in the column <code>LaunchSite</code>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, let's see the number of launches for each site.

    Use the method  <code>value_counts()</code> on the column <code>LaunchSite</code> to determine the number of launches  on each site:
    """)
    return


@app.cell
def _(df):
    df['LaunchSite'].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each launch aims to an dedicated orbit, and here are some common orbit types:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    * <b>LEO</b>: Low Earth orbit (LEO)is an Earth-centred orbit with an altitude of 2,000 km (1,200 mi) or less (approximately one-third of the radius of Earth),[1] or with at least 11.25 periods per day (an orbital period of 128 minutes or less) and an eccentricity less than 0.25.[2] Most of the manmade objects in outer space are in LEO <a href='https://en.wikipedia.org/wiki/Low_Earth_orbit'>[1]</a>.

    * <b>VLEO</b>: Very Low Earth Orbits (VLEO) can be defined as the orbits with a mean altitude below 450 km. Operating in these orbits can provide a number of benefits to Earth observation spacecraft as the spacecraft operates closer to the observation<a href='https://www.researchgate.net/publication/271499606_Very_Low_Earth_Orbit_mission_concepts_for_Earth_Observation_Benefits_and_challenges'>[2]</a>.

    * <b>GTO</b> A geosynchronous orbit is a high Earth orbit that allows satellites to match Earth's rotation. Located at 22,236 miles (35,786 kilometers) above Earth's equator, this position is a valuable spot for monitoring weather, communications and surveillance. Because the satellite orbits at the same speed that the Earth is turning, the satellite seems to stay in place over a single longitude, though it may drift north to south,” NASA wrote on its Earth Observatory website <a  href="https://www.space.com/29222-geosynchronous-orbit.html" >[3] </a>.

    * <b>SSO (or SO)</b>: It is a Sun-synchronous orbit  also called a heliosynchronous orbit is a nearly polar orbit around a planet, in which the satellite passes over any given point of the planet's surface at the same local mean solar time <a href="https://en.wikipedia.org/wiki/Sun-synchronous_orbit">[4] <a>.



    * <b>ES-L1 </b>:At the Lagrange points the gravitational forces of the two large bodies cancel out in such a way that a small object placed in orbit there is in equilibrium relative to the center of mass of the large bodies. L1 is one such point between the sun and the earth <a href="https://en.wikipedia.org/wiki/Lagrange_point#L1_point">[5]</a> .


    * <b>HEO</b> A highly elliptical orbit, is an elliptic orbit with high eccentricity, usually referring to one around Earth <a href="https://en.wikipedia.org/wiki/Highly_elliptical_orbit">[6]</a>.

    * <b> ISS </b> A modular space station (habitable artificial satellite) in low Earth orbit. It is a multinational collaborative project between five participating space agencies: NASA (United States), Roscosmos (Russia), JAXA (Japan), ESA (Europe), and CSA (Canada)<a href="https://en.wikipedia.org/wiki/International_Space_Station"> [7] </a>

    * <b> MEO </b> Geocentric orbits ranging in altitude from 2,000 km (1,200 mi) to just below geosynchronous orbit at 35,786 kilometers (22,236 mi). Also known as an intermediate circular orbit. These are "most commonly at 20,200 kilometers (12,600 mi), or 20,650 kilometers (12,830 mi), with an orbital period of 12 hours <a href="https://en.wikipedia.org/wiki/List_of_orbits"> [8] </a>

    * <b> HEO </b> Geocentric orbits above the altitude of geosynchronous orbit (35,786 km or 22,236 mi) <a href="https://en.wikipedia.org/wiki/List_of_orbits"> [9] </a>

    * <b> GEO </b> It is a circular geosynchronous orbit 35,786 kilometres (22,236 miles) above Earth's equator and following the direction of Earth's rotation <a href="https://en.wikipedia.org/wiki/Geostationary_orbit"> [10] </a>

    * <b> PO </b> It is one type of satellites in which a satellite passes above or nearly above both poles of the body being orbited (usually a planet such as the Earth <a href="https://en.wikipedia.org/wiki/Polar_orbit"> [11] </a>

    some are shown in the following plot:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/Orbits.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK 2: Calculate the number and occurrence of each orbit
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use the method  <code>.value_counts()</code> to determine the number and occurrence of each orbit in the  column <code>Orbit</code>
    """)
    return


@app.cell
def _(df):
    df['Orbit'].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK 3: Calculate the number and occurence of mission outcome of the orbits
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use the method <code>.value_counts()</code> on the column <code>Outcome</code> to determine the number of <code>landing_outcomes</code>.Then assign it to a variable landing_outcomes.
    """)
    return


@app.cell
def _(df):
    landing_outcomes=df['Outcome'].value_counts()
    landing_outcomes
    return (landing_outcomes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <code>True Ocean</code> means the mission outcome was successfully  landed to a specific region of the ocean while <code>False Ocean</code> means the mission outcome was unsuccessfully landed to a specific region of the ocean. <code>True RTLS</code> means the mission outcome was successfully  landed to a ground pad <code>False RTLS</code> means the mission outcome was unsuccessfully landed to a ground pad.<code>True ASDS</code> means the mission outcome was successfully  landed to a drone ship <code>False ASDS</code> means the mission outcome was unsuccessfully landed to a drone ship. <code>None ASDS</code> and <code>None None</code> these represent a failure to land.
    """)
    return


@app.cell
def _(landing_outcomes):
    for i,outcome in enumerate(landing_outcomes.keys()):
        print(i,outcome)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We create a set of outcomes where the second stage did not land successfully:
    """)
    return


@app.cell
def _(landing_outcomes):
    bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
    bad_outcomes
    return (bad_outcomes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK 4: Create a landing outcome label from Outcome column
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using the <code>Outcome</code>,  create a list where the element is zero if the corresponding  row  in  <code>Outcome</code> is in the set <code>bad_outcome</code>; otherwise, it's one. Then assign it to the variable <code>landing_class</code>:
    """)
    return


@app.cell
def _(bad_outcomes, df):
    landing_class=[0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]
    return (landing_class,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This variable will represent the classification variable that represents the outcome of each launch. If the value is zero, the  first stage did not land successfully; one means  the first stage landed Successfully
    """)
    return


@app.cell
def _(df, landing_class):
    df['Class']=landing_class
    df[['Class']].head(8)
    return


@app.cell
def _(df):
    df.head(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can use the following line of code to determine  the success rate:
    """)
    return


@app.cell
def _(df):
    df["Class"].mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now export it to a CSV for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <code>df.to_csv("dataset_part_2.csv", index=False)</code>
    """)
    return


@app.cell
def _(df):
    df.to_csv("../data/dataset_part_2.csv", index=False)
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
    <a href="https://www.linkedin.com/in/joseph-s-50398b136/">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a href="https://www.linkedin.com/in/nayefaboutayoun/">Nayef Abou Tayoun</a> is a Data Scientist at IBM and pursuing a Master of Management in Artificial intelligence degree at Queen's University.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!--
    ## Change Log
    -->
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!--
    | Date (YYYY-MM-DD) | Version | Changed By | Change Description      |
    | ----------------- | ------- | ---------- | ----------------------- |
    | 2021-08-31        | 1.1     | Lakshmi Holla    | Changed Markdown |
    | 2020-09-20        | 1.0     | Joseph     | Modified Multiple Areas |
    | 2020-11-04        | 1.1.    | Nayef      | updating the input data |
    | 2021-05-026       | 1.1.    | Joseph      | updating the input data |
    -->
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
