import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")


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
    # **Space X  Falcon 9 First Stage Landing Prediction**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Web scraping Falcon 9 and Falcon Heavy Launches Records from Wikipedia
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
    In this lab, you will be performing web scraping to collect Falcon 9 historical launch records from a Wikipedia page titled `List of Falcon 9 and Falcon Heavy launches`

    https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_1_L2/images/Falcon9_rocket_family.svg)
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
    More specifically, the launch records are stored in a HTML table shown below:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_1_L2/images/falcon9-launches-wiki.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Objectives
    Web scrap Falcon 9 launch records with `BeautifulSoup`:
    - Extract a Falcon 9 launch records HTML table from Wikipedia
    - Parse the table and convert it into a Pandas data frame
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First let's import required packages for this lab
    """)
    return


@app.cell
def _():
    import requests
    from bs4 import BeautifulSoup
    import unicodedata
    import pandas as pd

    return BeautifulSoup, pd, requests, unicodedata


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    and we will provide some helper functions for you to process web scraped HTML table
    """)
    return


@app.cell
def _(unicodedata):
    def date_time(table_cells):
        """
        This function returns the data and time from the HTML  table cell
        Input: the  element of a table data cell extracts extra row
        """
        return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

    def booster_version(table_cells):
        """
        This function returns the booster version from the HTML  table cell 
        Input: the  element of a table data cell extracts extra row
        """
        out=''.join([booster_version for i,booster_version in enumerate( table_cells.strings) if i%2==0][0:-1])
        return out

    def landing_status(table_cells):
        """
        This function returns the landing status from the HTML table cell 
        Input: the  element of a table data cell extracts extra row
        """
        out=[i for i in table_cells.strings][0]
        return out


    def get_mass(table_cells):
        mass=unicodedata.normalize("NFKD", table_cells.text).strip()
        if mass:
            mass.find("kg")
            new_mass=mass[0:mass.find("kg")+2]
        else:
            new_mass=0
        return new_mass


    def extract_column_from_header(row):
        """
        This function returns the landing status from the HTML table cell 
        Input: the  element of a table data cell extracts extra row
        """
        if (row.br):
            row.br.extract()
        if row.a:
            row.a.extract()
        if row.sup:
            row.sup.extract()
    
        colunm_name = ' '.join(row.contents)

        # Filter the digit and empty names
        if not(colunm_name.strip().isdigit()):
            colunm_name = colunm_name.strip()
            return colunm_name

    return (
        booster_version,
        date_time,
        extract_column_from_header,
        get_mass,
        landing_status,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To keep the lab tasks consistent, you will be asked to scrape the data from a snapshot of the  `List of Falcon 9 and Falcon Heavy launches` Wikipage updated on
    `9th June 2021`
    """)
    return


@app.cell
def _():
    static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
    return (static_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, request the HTML page from the above URL and get a `response` object
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK 1: Request the Falcon9 Launch Wiki page from its URL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, let's perform an HTTP GET method to request the Falcon9 Launch HTML page, as an HTTP response.
    """)
    return


@app.cell
def _(requests, static_url):
    response = requests.get(static_url)
    return (response,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Create a `BeautifulSoup` object from the HTML `response`
    """)
    return


@app.cell
def _(BeautifulSoup, response):
    soup = BeautifulSoup(response.content, 'html.parser')
    return (soup,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Print the page title to verify if the `BeautifulSoup` object was created properly
    """)
    return


@app.cell
def _(soup):
    print(soup.title)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK 2: Extract all column/variable names from the HTML table header
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we want to collect all relevant column names from the HTML table header
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's try to find all tables on the wiki page first. If you need to refresh your memory about `BeautifulSoup`, please check the external reference link towards the end of this lab
    """)
    return


@app.cell
def _(soup):
    html_tables = soup.find_all("table")
    return (html_tables,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Starting from the third table is our target table contains the actual launch records.
    """)
    return


@app.cell
def _(html_tables):
    first_launch_table = html_tables[2]
    print(first_launch_table)
    return (first_launch_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You should able to see the columns names embedded in the table header elements `<th>` as follows:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
    <tr>
    <th scope="col">Flight No.
    </th>
    <th scope="col">Date and<br/>time (<a href="/wiki/Coordinated_Universal_Time" title="Coordinated Universal Time">UTC</a>)
    </th>
    <th scope="col"><a href="/wiki/List_of_Falcon_9_first-stage_boosters" title="List of Falcon 9 first-stage boosters">Version,<br/>Booster</a> <sup class="reference" id="cite_ref-booster_11-0"><a href="#cite_note-booster-11">[b]</a></sup>
    </th>
    <th scope="col">Launch site
    </th>
    <th scope="col">Payload<sup class="reference" id="cite_ref-Dragon_12-0"><a href="#cite_note-Dragon-12">[c]</a></sup>
    </th>
    <th scope="col">Payload mass
    </th>
    <th scope="col">Orbit
    </th>
    <th scope="col">Customer
    </th>
    <th scope="col">Launch<br/>outcome
    </th>
    <th scope="col"><a href="/wiki/Falcon_9_first-stage_landing_tests" title="Falcon 9 first-stage landing tests">Booster<br/>landing</a>
    </th></tr>
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we just need to iterate through the `<th>` elements and apply the provided `extract_column_from_header()` to extract column name one by one
    """)
    return


@app.cell
def _(extract_column_from_header, first_launch_table):
    column_names = []

    for th in first_launch_table.find_all('th'):
        name = extract_column_from_header(th)
        if name is not None and len(name) > 0:
            column_names.append(name)
    return (column_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check the extracted column names
    """)
    return


@app.cell
def _(column_names):
    print(column_names)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## TASK 3: Create a data frame by parsing the launch HTML tables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will create an empty dictionary with keys from the extracted column names in the previous task. Later, this dictionary will be converted into a Pandas dataframe
    """)
    return


@app.cell
def _(column_names):
    launch_dict= dict.fromkeys(column_names)

    # Remove an irrelvant column
    del launch_dict['Date and time ( )']

    # Let's initial the launch_dict with each value to be an empty list
    launch_dict['Flight No.'] = []
    launch_dict['Launch site'] = []
    launch_dict['Payload'] = []
    launch_dict['Payload mass'] = []
    launch_dict['Orbit'] = []
    launch_dict['Customer'] = []
    launch_dict['Launch outcome'] = []

    # Added some new columns
    launch_dict['Version Booster']=[]
    launch_dict['Booster landing']=[]
    launch_dict['Date']=[]
    launch_dict['Time']=[]
    return (launch_dict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we just need to fill up the `launch_dict` with launch records extracted from table rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Usually, HTML tables in Wiki pages are likely to contain unexpected annotations and other types of noises, such as reference links `B0004.1[8]`, missing values `N/A [e]`, inconsistent formatting, etc.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To simplify the parsing process, we have provided an incomplete code snippet below to help you to fill up the `launch_dict`. Please complete the following code snippet with TODOs or you can choose to write your own logic to parse all launch tables:
    """)
    return


@app.cell
def _(booster_version, date_time, get_mass, landing_status, launch_dict, soup):
    extracted_row = 0
    #Extract each table 
    for table_number,table in enumerate(soup.find_all('table',"wikitable plainrowheaders collapsible")):
        # get table row
        for rows in table.find_all("tr"):
            #check to see if first table heading is as number corresponding to launch a number 
            if rows.th:
                if rows.th.string:
                    flight_number=rows.th.string.strip()
                    flag=flight_number.isdigit()
            else:
                flag=False
            #get table element 
            row=rows.find_all('td')
            #if it is number save cells in a dictonary 
            if flag:
                extracted_row += 1
                # Flight Number value
                launch_dict['Flight No.'].append(flight_number)
                datatimelist=date_time(row[0])
        
                # Date value
                date = datatimelist[0].strip(',')
                launch_dict['Date'].append(date)
        
                # Time value
                time = datatimelist[1]
                launch_dict['Time'].append(time)

                # Booster version
                bv=booster_version(row[1])
                if not(bv):
                    bv=row[1].a.string
                launch_dict['Version Booster'].append(bv)
        
                # Launch Site
                launch_site = row[2].a.string
                launch_dict['Launch site'].append(launch_site)
        
                # Payload
                payload = row[3].a.string
                launch_dict['Payload'].append(payload)
        
                # Payload Mass
                payload_mass = get_mass(row[4])
                launch_dict['Payload mass'].append(payload_mass)
        
                # Orbit
                orbit = row[5].a.string
                launch_dict['Orbit'].append(orbit)
        
                # Customer
                if row[6].a:
                    customer=row[6].a.string
                else:
                    customer=row[6].string
                launch_dict['Customer'].append(customer)
        
                # Launch outcome
                launch_outcome = list(row[7].strings)[0]
                launch_dict['Launch outcome'].append(launch_outcome)
        
                # Booster landing
                booster_landing = landing_status(row[8])
                launch_dict['Booster landing'].append(booster_landing)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After you have fill in the parsed launch record values into `launch_dict`, you can create a dataframe from it.
    """)
    return


@app.cell
def _(launch_dict, pd):
    df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now export it to a <b>CSV</b> for the next section, but to make the answers consistent and in case you have difficulties finishing this lab.

    Following labs will be using a provided dataset to make each lab independent.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <code>df.to_csv('spacex_web_scraped.csv', index=False)</code>
    """)
    return


@app.cell
def _(df):
    df.to_csv('../data/spacex_web_scraped.csv', index=False)
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
    <a href="https://www.linkedin.com/in/yan-luo-96288783/">Yan Luo</a>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a href="https://www.linkedin.com/in/nayefaboutayoun/">Nayef Abou Tayoun</a>
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
    | Date (YYYY-MM-DD) | Version | Changed By | Change Description      |
    | ----------------- | ------- | ---------- | ----------------------- |
    | 2021-06-09        | 1.0     | Yan Luo    | Tasks updates           |
    | 2020-11-10        | 1.0     | Nayef      | Created the initial version |
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
