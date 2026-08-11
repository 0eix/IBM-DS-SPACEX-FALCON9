import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <p style="text-align:center">
        <a href="https://skills.network" target="_blank">
        <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
        </a>
    </p>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **SpaceX  Falcon 9 first stage Landing Prediction**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 1: Collecting the data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Estimated time needed: **45** minutes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this capstone, we will predict if the Falcon 9 first stage will land successfully. SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against SpaceX for a rocket launch. In this lab, you will collect and make sure the data is in the correct format from an API. The following is an example of a successful and launch.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/lab_v2/images/landing_1.gif)
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
    ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/lab_v2/images/crash.gif)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Most unsuccessful landings are planned. Space X performs a controlled landing in the oceans.
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
    In this lab, you will make a get request to the SpaceX API. You will also do some basic data wrangling and formating.

    - Request to the SpaceX API
    - Clean the requested data
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
    We will import the following libraries into the lab
    """)
    return


@app.cell
def _():
    import requests

    import pandas as pd
    import numpy as np
    import datetime

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    return datetime, np, pd, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Below we will define a series of helper functions that will help us use the API to extract information using identification numbers in the launch data.

    From the <code>rocket</code> column we would like to learn the booster name.
    """)
    return


@app.cell
def _(BoosterVersion, requests):
    def getBoosterVersion(data):
        for x in data['rocket']:
           if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
            BoosterVersion.append(response['name'])

    return (getBoosterVersion,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From the <code>launchpad</code> we would like to know the name of the launch site being used, the logitude, and the latitude.
    """)
    return


@app.cell
def _(Latitude, LaunchSite, Longitude, requests):
    def getLaunchSite(data):
        for x in data['launchpad']:
           if x:
             response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
             Longitude.append(response['longitude'])
             Latitude.append(response['latitude'])
             LaunchSite.append(response['name'])

    return (getLaunchSite,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From the <code>payload</code> we would like to learn the mass of the payload and the orbit that it is going to.
    """)
    return


@app.cell
def _(Orbit, PayloadMass, requests):
    def getPayloadData(data):
        for load in data['payloads']:
           if load:
            response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])

    return (getPayloadData,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From <code>cores</code> we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, wheter the core is reused, wheter legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core.
    """)
    return


@app.cell
def _(
    Block,
    Flights,
    GridFins,
    LandingPad,
    Legs,
    Outcome,
    Reused,
    ReusedCount,
    Serial,
    requests,
):
    def getCoreData(data):
        for core in data['cores']:
                if core['core'] is not None:
                    response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                    Block.append(response['block'])
                    ReusedCount.append(response['reuse_count'])
                    Serial.append(response['serial'])
                else:
                    Block.append(None)
                    ReusedCount.append(None)
                    Serial.append(None)
                Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
                Flights.append(core['flight'])
                GridFins.append(core['gridfins'])
                Reused.append(core['reused'])
                Legs.append(core['legs'])
                LandingPad.append(core['landpad'])

    return (getCoreData,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's start requesting rocket launch data from SpaceX API with the following URL:
    """)
    return


@app.cell
def _():
    spacex_url="https://api.spacexdata.com/v4/launches/past"
    return (spacex_url,)


@app.cell
def _(requests, spacex_url):
    response = requests.get(spacex_url)
    return (response,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check the content of the response
    """)
    return


@app.cell
def _(response):
    print(response.content)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You should see the response contains massive information about SpaceX launches. Next, let's try to discover some more relevant information for this project.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 1: Request and parse the SpaceX launch data using the GET request
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To make the requested JSON results more consistent, we will use the following static response object for this project:
    """)
    return


@app.cell
def _():
    static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We should see that the request was successfull with the 200 status response code
    """)
    return


@app.cell
def _(response):
    response.status_code
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we decode the response content as a Json using <code>.json()</code> and turn it into a Pandas dataframe using <code>.json_normalize()</code>
    """)
    return


@app.cell
def _(pd, response):
    data = pd.json_normalize(response.json())
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using the dataframe <code>data</code> print the first 5 rows
    """)
    return


@app.cell
def _(data):
    data.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You will notice that a lot of the data are IDs. For example the rocket column has no information about the rocket just an identification number.

    We will now use the API again to get information about the launches using the IDs given for each launch. Specifically we will be using columns <code>rocket</code>, <code>payloads</code>, <code>launchpad</code>, and <code>cores</code>.
    """)
    return


@app.cell
def _(data, datetime, pd):
    data_1 = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

    data_1 = data_1[data_1['cores'].map(len) == 1]
    data_1 = data_1[data_1['payloads'].map(len) == 1]

    data_1['cores'] = data_1['cores'].map(lambda x: x[0])
    data_1['payloads'] = data_1['payloads'].map(lambda x: x[0])

    data_1['date'] = pd.to_datetime(data_1['date_utc']).dt.date
    data_1 = data_1[data_1['date'] <= datetime.date(2020, 11, 13)]
    return (data_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    * From the <code>rocket</code> we would like to learn the booster name

    * From the <code>payload</code> we would like to learn the mass of the payload and the orbit that it is going to

    * From the <code>launchpad</code> we would like to know the name of the launch site being used, the longitude, and the latitude.

    * **From <code>cores</code> we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, whether the core is reused, whether legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core.**

    The data from these requests will be stored in lists and will be used to create a new dataframe.
    """)
    return


@app.cell
def _():
    BoosterVersion = []
    PayloadMass = []
    Orbit = []
    LaunchSite = []
    Outcome = []
    Flights = []
    GridFins = []
    Reused = []
    Legs = []
    LandingPad = []
    Block = []
    ReusedCount = []
    Serial = []
    Longitude = []
    Latitude = []
    return (
        Block,
        BoosterVersion,
        Flights,
        GridFins,
        LandingPad,
        Latitude,
        LaunchSite,
        Legs,
        Longitude,
        Orbit,
        Outcome,
        PayloadMass,
        Reused,
        ReusedCount,
        Serial,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    These functions will apply the outputs globally to the above variables. Let's take a looks at <code>BoosterVersion</code> variable. Before we apply  <code>getBoosterVersion</code> the list is empty:
    """)
    return


@app.cell
def _(BoosterVersion):
    BoosterVersion
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's apply <code> getBoosterVersion</code> function method to get the booster version
    """)
    return


@app.cell
def _(data_1, getBoosterVersion):
    getBoosterVersion(data_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    the list has now been update
    """)
    return


@app.cell
def _(BoosterVersion):
    BoosterVersion[0:5]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    we can apply the rest of the  functions here:
    """)
    return


@app.cell
def _(data_1, getLaunchSite):
    getLaunchSite(data_1)
    return


@app.cell
def _(data_1, getPayloadData):
    getPayloadData(data_1)
    return


@app.cell
def _(data_1, getCoreData):
    getCoreData(data_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally lets construct our dataset using the data we have obtained. We we combine the columns into a dictionary.
    """)
    return


@app.cell
def _(
    Block,
    BoosterVersion,
    Flights,
    GridFins,
    LandingPad,
    Latitude,
    LaunchSite,
    Legs,
    Longitude,
    Orbit,
    Outcome,
    PayloadMass,
    Reused,
    ReusedCount,
    Serial,
    data_1,
):
    launch_dict = {'FlightNumber': list(data_1['flight_number']), 'Date': list(data_1['date']), 'BoosterVersion': BoosterVersion, 'PayloadMass': PayloadMass, 'Orbit': Orbit, 'LaunchSite': LaunchSite, 'Outcome': Outcome, 'Flights': Flights, 'GridFins': GridFins, 'Reused': Reused, 'Legs': Legs, 'LandingPad': LandingPad, 'Block': Block, 'ReusedCount': ReusedCount, 'Serial': Serial, 'Longitude': Longitude, 'Latitude': Latitude}
    return (launch_dict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Then, we need to create a Pandas data frame from the dictionary launch_dict.
    """)
    return


@app.cell
def _(launch_dict, pd):
    data_falcon9 = pd.DataFrame(launch_dict)
    return (data_falcon9,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Show the summary of the dataframe
    """)
    return


@app.cell
def _(data_falcon9):
    data_falcon9.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 2: Filter the dataframe to only include `Falcon 9` launches
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally we will remove the Falcon 1 launches keeping only the Falcon 9 launches. Filter the data dataframe using the <code>BoosterVersion</code> column to only keep the Falcon 9 launches. Save the filtered data to a new dataframe called <code>data_falcon9</code>.
    """)
    return


@app.cell
def _(data_falcon9):
    data_falcon9_1 = data_falcon9[data_falcon9['BoosterVersion'] != 'Falcon 1']
    return (data_falcon9_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have removed some values we should reset the FlgihtNumber column
    """)
    return


@app.cell
def _(data_falcon9_1):
    data_falcon9_1.loc[:, 'FlightNumber'] = list(range(1, data_falcon9_1.shape[0] + 1))
    data_falcon9_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Wrangling
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see below that some of the rows are missing values in our dataset.
    """)
    return


@app.cell
def _(data_falcon9_1):
    data_falcon9_1.isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before we can continue we must deal with these missing values. The <code>LandingPad</code> column will retain None values to represent when landing pads were not used.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 3: Dealing with Missing Values
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Calculate below the mean for the <code>PayloadMass</code> using the <code>.mean()</code>. Then use the mean and the <code>.replace()</code> function to replace `np.nan` values in the data with the mean you calculated.
    """)
    return


@app.cell
def _(data_falcon9_1, np):
    mean_payload = data_falcon9_1['PayloadMass'].mean()
    data_falcon9_1['PayloadMass'] = data_falcon9_1['PayloadMass'].replace(np.nan, mean_payload)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You should see the number of missing values of the <code>PayLoadMass</code> change to zero.
    """)
    return


@app.cell
def _(data_falcon9_1):
    data_falcon9_1['PayloadMass'].isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we should have no missing values in our dataset except for in <code>LandingPad</code>.
    """)
    return


@app.cell
def _(data_falcon9_1):
    data_falcon9_1.isnull().sum()
    return


@app.cell
def _(data_falcon9_1):
    data_falcon9_1['LandingPad'].isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now export it to a <b>CSV</b> for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <code>data_falcon9.to_csv('../data/dataset_part_1.csv', index=False)</code>
    """)
    return


@app.cell
def _(data_falcon9_1):
    data_falcon9_1.to_csv('../data/dataset_part_1.csv', index=False)
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
    ## Change Log
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    |Date (YYYY-MM-DD)|Version|Changed By|Change Description|
    |-|-|-|-|
    |2020-09-20|1.1|Joseph|get result each time you run|
    |2020-09-20|1.1|Azim |Created Part 1 Lab using SpaceX API|
    |2020-09-20|1.0|Joseph |Modified Multiple Areas|
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
