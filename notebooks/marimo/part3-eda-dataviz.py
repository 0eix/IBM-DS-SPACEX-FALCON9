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
    # **SpaceX  Falcon 9 First Stage Landing Prediction**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Assignment: Exploring and Preparing Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Estimated time needed: **70** minutes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this assignment, we will predict if the Falcon 9 first stage will land successfully. SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is due to the fact that SpaceX can reuse the first stage.

    In this lab, you will perform Exploratory Data Analysis and Feature Engineering.
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
    Most unsuccessful landings are planned. Space X performs a controlled landing in the oceans.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Objectives
    Perform exploratory Data Analysis and Feature Engineering using `Pandas` and `Matplotlib`

    - Exploratory Data Analysis
    - Preparing Data  Feature Engineering
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
    ### Import Libraries and Define Auxiliary Functions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will import the following libraries the lab
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    return pd, plt, sns


@app.cell
def _():
    import plotly.express as px
    import plotly.graph_objects as go

    import numpy as np

    from scipy import stats

    return go, np, px, stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exploratory Data Analysis
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, let's read the SpaceX dataset into a Pandas dataframe and print its summary
    """)
    return


@app.cell
def _():
    #df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

    # If you were unable to complete the previous lab correctly you can uncomment and load this csv

    # df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv')
    return


@app.cell
def _(pd):
    df = pd.read_csv(
        "../data/dataset_part_2.csv",
        dtype={
            "FlightNumber": "int64",
            "Class": "int64",
            "Flights": "int64",
            "ReusedCount": "int64",
            "PayloadMass": "float64",
            "Serial": "category",
            "LaunchSite": "category",
            "Block": "category",
            "Outcome": "category",
            "Orbit": "category",
        },
    )

    df = df.dropna(subset=["Date"])
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Year"] = df["Date"].dt.year

    df["Result"] = df["Class"].map({1: "Succeeded", 0: "Failed"})
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, let's try to see how the `FlightNumber` (indicating the continuous launch attempts.) and `Payload` variables would affect the launch outcome.

    We can plot out the <code>FlightNumber</code> vs. <code>PayloadMass</code>and overlay the outcome of the launch. We see that as the flight number increases, the first stage is more likely to land successfully. The payload mass is also important; it seems the more massive the payload, the less likely the first stage will return.
    """)
    return


@app.cell
def _(df, plt, sns):
    sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
    plt.xlabel("Flight Number",fontsize=20)
    plt.ylabel("Pay load Mass (kg)",fontsize=20)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, let's drill down to each site visualize its detailed launch records.
    """)
    return


@app.cell
def _():
    COLOR_SUCCESS = "#009E73" 
    COLOR_FAILURE = "#D55E00" 

    COLOR_RESULT = {"Succeeded": COLOR_SUCCESS, "Failed": COLOR_FAILURE}

    COLOR_BARPLOT = "#2B5C8F"  
    COLOR_TRENDLINE = "#1F1F1F"  

    ALPHA_BARPLOT = 0.25  
    ALPHA_SCATTER = 0.70 
    ALPHA_TRENDLINE = 1.00 

    LINEWIDTH_TRENDLINE = 2.5
    return COLOR_BARPLOT, COLOR_RESULT, LINEWIDTH_TRENDLINE


@app.function
def base(
    width=1115,
    height=283,
    margin=dict(l=40, r=40, t=60, b=40),
    template="plotly_white",
) -> dict:
    return dict(
        width=width,
        height=height,
        margin=margin,
        template=template,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK 1: Visualize the relationship between Flight Number and Launch Site
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use the function <code>catplot</code> to plot <code>FlightNumber</code> vs <code>LaunchSite</code>, set the  parameter <code>x</code>  parameter to <code>FlightNumber</code>,set the  <code>y</code> to <code>Launch Site</code> and set the parameter <code>hue</code> to <code>'class'</code>
    """)
    return


@app.cell
def _(COLOR_BARPLOT, COLOR_RESULT, LINEWIDTH_TRENDLINE, df, go, px):
    _fig = px.scatter(
        df,
        x="FlightNumber",
        y="LaunchSite",
        color="Result",  # Mettre ici votre colonne de résultat (ex: "Class", "Outcome")
        title="<b>Launch site by flight number</b>",
        labels={"FlightNumber": "Flight number", "LaunchSite": "Launch site"},
        color_discrete_map=COLOR_RESULT,
    )

    # 2. Lignes reliant les points par site de lancement
    for _, _group in df.groupby("LaunchSite"):
        _fig.add_trace(
            go.Scatter(
                x=_group["FlightNumber"],
                y=_group["LaunchSite"],
                mode="lines",
                line=dict(color=COLOR_BARPLOT, width=LINEWIDTH_TRENDLINE),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # Passer les lignes en arrière-plan
    _fig.data = (
            _fig.data[len(df["Result"].unique()):]
            + _fig.data[: len(df["Result"].unique())]
    )

    _fig.update_traces(marker=dict(size=9), selector=dict(mode="markers"))
    _fig.update_layout(**base(), showlegend=False)
    _fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now try to explain the patterns you found in the Flight Number vs. Launch Site scatter point plots.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK 2: Visualize the relationship between Payload and Launch Site
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We also want to observe if there is any relationship between launch sites and their payload mass.
    """)
    return


@app.cell
def _(COLOR_BARPLOT, COLOR_RESULT, df, go, px):
    _fig_box = px.box(
        df,
        x="LaunchSite",
        y="PayloadMass",
        points=False,  # we'll add our own points below
        labels={
            "LaunchSite": "Launch site",
            "PayloadMass": "Payload mass (kg)",
        },
    )
    _fig_box.update_traces(marker_color=COLOR_BARPLOT)

    # 2. Jittered strip plot for points, colored by Result
    _fig_points = px.strip(
        df,
        x="LaunchSite",
        y="PayloadMass",
        color="Result",
        color_discrete_map=COLOR_RESULT,
        hover_data=["FlightNumber", "LaunchSite", "Class"],
        stripmode="overlay",  # points land on the same x position as the box, not offset
    )
    _fig_points.update_traces(
        marker=dict(size=9),
        jitter=1,  # étalement horizontal maximal, appliqué après la création
    )

    # 3. Merge: box traces first (background), then points on top
    _fig = go.Figure(data=_fig_box.data + _fig_points.data)

    _fig.update_layout(
        **base(),
        title="<b>Distribution of the payload mass per launch site</b>",
        xaxis_title="Launch site",
        yaxis_title="Payload mass (kg)",
        legend_title_text="Result",
        showlegend=True,
    )

    _fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now if you observe Payload Vs. Launch Site scatter point chart you will find for the VAFB-SLC  launchsite there are no  rockets  launched for  heavypayload mass(greater than 10000).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK  3: Visualize the relationship between success rate of each orbit type
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we want to visually check if there are any relationship between success rate and orbit type.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's create a `bar chart` for the sucess rate of each orbit
    """)
    return


@app.cell
def _(np, stats):
    def calculate_wilson_ci(row, confidence=0.95):
        n = row["Total"]
        k = row["Successes"]
        if n == 0:
            return 0.0, 0.0
        z = stats.norm.ppf(1 - (1 - confidence) / 2)
        p = k / n
        denom = 1 + z ** 2 / n
        center = (p + z ** 2 / (2 * n)) / denom
        spread = z * np.sqrt((p * (1 - p) + z ** 2 / (4 * n)) / n) / denom
        lower = max(0.0, center - spread)
        upper = min(1.0, center + spread)
        return lower, upper

    return (calculate_wilson_ci,)


@app.cell
def _(COLOR_BARPLOT, LINEWIDTH_TRENDLINE, calculate_wilson_ci, df, go):
    _df_orbit = (
        df.groupby("Orbit")
        .agg(
            Successes=("Class", lambda x: (x == 1).sum()),
            Failures=("Class", lambda x: (x == 0).sum()),
            Total=("Class", "count"),
            Success_Rate=("Class", "mean"),
        )
        .reset_index()
    )


    _df_orbit = _df_orbit.sort_values(by="Success_Rate", ascending=False)

    _df_orbit[["CI_Lower", "CI_Upper"]] = _df_orbit.apply(
        calculate_wilson_ci, axis=1, result_type="expand"
    )


    _df_orbit["Error_Minus"] = (
            _df_orbit["Success_Rate"] - _df_orbit["CI_Lower"]
    )
    _df_orbit["Error_Plus"] = _df_orbit["CI_Upper"] - _df_orbit["Success_Rate"]


    _df_orbit["Label"] = _df_orbit.apply(
        lambda r: f"{r['Orbit']}<br>(N={r['Total']})", axis=1
    )


    _min_size, _max_size = 10, 32
    _n_min, _n_max = _df_orbit["Total"].min(), _df_orbit["Total"].max()

    if _n_max > _n_min:
        _marker_sizes = _min_size + (
                (_df_orbit["Total"] - _n_min) / (_n_max - _n_min)
        ) * (_max_size - _min_size)
    else:
        _marker_sizes = [14] * len(_df_orbit)

    _df_orbit["Marker_Size"] = _marker_sizes


    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_df_orbit["Label"],
            y=_df_orbit["Success_Rate"],
            mode="markers",
            showlegend=False,
            xaxis="x",
            yaxis="y",
            marker=dict(
                size=_df_orbit["Marker_Size"],
                color=COLOR_BARPLOT,
                opacity=0.7,
                symbol="circle",
                line=dict(color=COLOR_BARPLOT, width=1.5),
            ),
            error_y=dict(
                type="data",
                symmetric=False,
                array=_df_orbit["Error_Plus"],
                arrayminus=_df_orbit["Error_Minus"],
                color=COLOR_BARPLOT,
                thickness=LINEWIDTH_TRENDLINE,
                width=6,
            ),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Taux de succès : %{y:.1%}<br>"
                "IC 95% : [%{customdata[2]:.1%} - %{customdata[3]:.1%}]<br>"
                "Volume : %{customdata[1]} vols<extra></extra>"
            ),
            customdata=_df_orbit[["Orbit", "Total", "CI_Lower", "CI_Upper"]],
        )
    )

    _legend_samples = [
        _n_min,
        int(round((_n_min + _n_max) / 2)),
        _n_max,
    ]
    _legend_samples = sorted(list(set(_legend_samples)))

    _legend_y_positions = [0.75, 0.55, 0.32]

    _legend_sizes = []
    _legend_y = []
    _legend_text = []

    for _idx, _sample in enumerate(_legend_samples):
        if _n_max > _n_min:
            _sz = _min_size + ((_sample - _n_min) / (_n_max - _n_min)) * (
                    _max_size - _min_size
            )
        else:
            _sz = 14
        _legend_sizes.append(_sz)
        _legend_y.append(_legend_y_positions[_idx])
        _legend_text.append(f"  N = {_sample}")

    _fig.add_trace(
        go.Scatter(
            x=[1] * len(_legend_samples),
            y=_legend_y,
            mode="markers+text",
            text=_legend_text,
            textposition="middle right",
            textfont=dict(size=12),
            showlegend=False,
            xaxis="x2",
            yaxis="y2",
            hoverinfo="skip",
            marker=dict(
                size=_legend_sizes,
                color=COLOR_BARPLOT,
                opacity=0.7,
                symbol="circle",
                line=dict(color=COLOR_BARPLOT, width=1.5),
            ),
        )
    )

    _fig.update_layout(
        **base(),
        title="<b>Success rate per orbit (95% CI)</b>",
        xaxis=dict(
            title="Orbit (sample size)",
            type="category",
            tickangle=0,
            domain=[0.0, 0.82],
        ),
        yaxis=dict(
            title="Success rate",
            tickformat=".0%",
            range=[-0.05, 1.05],
        ),
        xaxis2=dict(
            domain=[0.85, 1.0],
            range=[0.8, 2.5],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis2=dict(
            range=[-0.05, 1.05],
            showticklabels=False,
            showgrid=False,  
            zeroline=False,  
            overlaying="y",
        ),
        showlegend=False,
    )

    _fig.add_annotation(
        xref="x2 domain",
        yref="paper",
        x=0.0,
        y=0.92,
        text="<b>Sample size (N)</b>",
        showarrow=False,
        xanchor="left",
        font=dict(size=12),
    )

    _fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Analyze the ploted bar chart try to find which orbits have high sucess rate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK  4: Visualize the relationship between FlightNumber and Orbit type
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For each orbit, we want to see if there is any relationship between FlightNumber and Orbit type.
    """)
    return


@app.cell
def _(COLOR_BARPLOT, COLOR_RESULT, LINEWIDTH_TRENDLINE, df, go, px):
    # 2. Obtenir la liste des orbites ordonnées par le premier numéro de vol (min)
    _orbit_order = (
        df.groupby("Orbit")["FlightNumber"]
        .min()
        .sort_values(ascending=True)  # Du vol le plus ancien au plus récent
        .index.tolist()
    )

    # 3. Création du scatter plot Plotly Express
    _fig = px.scatter(
        df,
        x="FlightNumber",
        y="Orbit",
        color="Result",
        title="<b>Orbit by flight number</b>",
        labels={"FlightNumber": "Flight number", "Orbit": "Orbit"},
        color_discrete_map=COLOR_RESULT,
    )

    # 4. Ajout des lignes reliant les points par orbite
    for _, _group in df.groupby("Orbit"):
        _fig.add_trace(
            go.Scatter(
                x=_group["FlightNumber"],
                y=_group["Orbit"],
                mode="lines",
                line=dict(color=COLOR_BARPLOT, width=LINEWIDTH_TRENDLINE),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # 5. Re-ordonner les traces pour placer les lignes en arrière-plan
    _n_results = df["Result"].nunique()
    _fig.data = _fig.data[_n_results:] + _fig.data[:_n_results]

    # 6. Mise à jour des marqueurs et de l'ordre de l'axe Y
    _fig.update_traces(marker=dict(size=9), selector=dict(mode="markers"))

    _fig.update_layout(
        **base(),
        showlegend=False,
        yaxis=dict(
            categoryorder="array",
            categoryarray=_orbit_order,  # Applique le tri par premier vol
        ),
    )

    _fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You should see that in the LEO orbit the Success appears related to the number of flights; on the other hand, there seems to be no relationship between flight number when in GTO orbit.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK  5: Visualize the relationship between Payload and Orbit type
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Similarly, we can plot the Payload vs. Orbit scatter point charts to reveal the relationship between Payload and Orbit type
    """)
    return


@app.cell
def _(COLOR_BARPLOT, COLOR_RESULT, df, go, px):
    _orbit_order = (
        df.groupby("Orbit")["PayloadMass"]
        .median()
        .sort_values(ascending=True)
        .index.tolist()
    )

    # 1. Boxplot (en spécifying categoryorder via categoryarray ou en triant le df)
    _fig_box = px.box(
        df,
        x="Orbit",
        y="PayloadMass",
        points=False,
        labels={"Orbit": "Orbit", "PayloadMass": "Payload mass (kg)"},
        category_orders={
            "Orbit": _orbit_order
        },  # Applique le tri personnalisé
    )
    _fig_box.update_traces(marker_color=COLOR_BARPLOT)

    # 2. Jittered strip plot
    _fig_points = px.strip(
        df,
        x="Orbit",
        y="PayloadMass",
        color="Result",
        color_discrete_map=COLOR_RESULT,
        hover_data=["FlightNumber", "LaunchSite", "Class"],
        stripmode="overlay",
        category_orders={"Orbit": _orbit_order},
    )
    _fig_points.update_traces(
        marker=dict(size=9, opacity=1),
        jitter=1,
    )

    # 3. Fusion des traces
    _fig = go.Figure(data=_fig_box.data + _fig_points.data)

    _fig.update_layout(
        **base(),
        title="<b>Distribution of the payload mass per orbit</b>",
        xaxis=dict(
            title="Orbit",
            categoryorder="array",  # Force l'axe X à respecter l'ordre exact de la liste
            categoryarray=_orbit_order,
        ),
        yaxis_title="Payload mass (kg)",
        legend_title_text="Result",
        showlegend=True,
    )

    _fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With heavy payloads the successful landing or positive landing rate are more for Polar,LEO and ISS.

    However for GTO we cannot distinguish this well as both positive landing rate and negative landing(unsuccessful mission) are both there here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK  6: Visualize the launch success yearly trend
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can plot a line chart with x axis to be <code>Year</code> and y axis to be average success rate, to get the average launch success trend.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The function will help you get the year from the date:
    """)
    return


@app.cell
def _(COLOR_BARPLOT, LINEWIDTH_TRENDLINE, df, go, np, px):
    _df_yearly = df.groupby("Year", as_index=False)["Class"].mean()
    _df_yearly.rename(columns={"Class": "Year_Mean"}, inplace=True)

    _x_vals = _df_yearly["Year"].values
    _y_vals = _df_yearly["Year_Mean"].values

    _slope, _intercept = np.polyfit(_x_vals, _y_vals, deg=1)
    _df_yearly["Year_Trend"] = _slope * _x_vals + _intercept

    # 2. Barplot avec Plotly Express
    _fig_bar = px.bar(_df_yearly, x="Year", y="Year_Mean", opacity=0.55)
    _fig_bar.update_traces(
        marker_color=COLOR_BARPLOT,
        name="success rate",
        hovertemplate="<b>Année %{x}</b><br>Taux de succès: %{y:.2%}<extra></extra>",
    )

    # 3. Lineplot (Trendline) avec Plotly Express
    _fig_line = px.line(
        _df_yearly,
        x="Year",
        y="Year_Trend",
    )
    _fig_line.update_traces(
        line=dict(color=COLOR_BARPLOT, width=LINEWIDTH_TRENDLINE),
        name="Trend (OLS)",
        hovertemplate="<b>Année %{x}</b><br>Tendance: %{y:.2%}<extra></extra>",
    )

    # 4. Fusion des traces dans un Figure (exactement comme votre exemple box + strip)
    _fig = go.Figure(data=_fig_bar.data + _fig_line.data)

    _fig.update_layout(
        **base(),
        title="<b>Success rate per year, with trend</b>",
        xaxis=dict(title="Year", type="category"),
        yaxis=dict(title="Success rate", tickformat=".0%", range=[0, 1.15]),
        bargap=0.3,
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"),
        showlegend=False,
    )

    _fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can observe that the success rate since 2013 kept increasing till 2017 (stable in 2014) and after 2015 it started increasing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Features Engineering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    By now, you should obtain some preliminary insights about how each important variable would affect the success rate, we will select the features that will be used in success prediction in the future module.
    """)
    return


@app.cell
def _(df):
    features = df[['Date', 'PayloadMass', 'Orbit', 'LaunchSite', 'LandingPad']]
    features.head()
    return (features,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK  7: Create dummy variables to categorical columns
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use the function <code>get_dummies</code> and <code>features</code> dataframe to apply OneHotEncoder to the column <code>Orbits</code>, <code>LaunchSite</code>, <code>LandingPad</code>, and <code>Serial</code>. Assign the value to the variable <code>features_one_hot</code>, display the results using the method head. Your result dataframe must include all features including the encoded ones.
    """)
    return


@app.cell
def _(features, pd):
    features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad'])
    features_one_hot.head()
    return (features_one_hot,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TASK  8: Cast all numeric columns to `float64`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that our <code>features_one_hot</code> dataframe only contains numbers cast the entire dataframe to variable type <code>float64</code>
    """)
    return


@app.cell
def _(features_one_hot):
    features_one_hot_1 = features_one_hot.astype('float64')
    return (features_one_hot_1,)


@app.cell
def _(features_one_hot_1):
    len(features_one_hot_1.columns)
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
    <code>features_one_hot.to_csv('dataset_part_3.csv', index=False)</code>
    """)
    return


@app.cell
def _(features_one_hot_1):
    features_one_hot_1.to_csv('../data/dataset_part_3.csv', index=False)
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
    ## Change Log
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Date (YYYY-MM-DD) | Version | Changed By | Change Description      |
    | ----------------- | ------- | ---------- | ----------------------- |
    | 2021-10-12        | 1.1     | Lakshmi Holla     | Modified markdown |
    | 2020-09-20        | 1.0     | Joseph     | Modified Multiple Areas |
    | 2020-11-10       | 1.1    | Nayef      | updating the input data |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Copyright © 2020 IBM Corporation. All rights reserved.
    """)
    return


if __name__ == "__main__":
    app.run()
