import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")


@app.cell
def _():
    from __future__ import annotations

    import time
    import warnings
    from pathlib import Path

    return (time,)


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import pandas as pd
    import phik
    from phik import resources, report
    import numpy as np
    import scipy.stats as stats

    return np, pd, stats


@app.cell
def _():
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    return go, make_subplots, px


@app.cell
def _(pd):
    df_csv = pd.read_csv("../data/dataset_part_2.csv")

    df_csv = df_csv.dropna(subset=["Date"])
    df_csv["Date"] = pd.to_datetime(df_csv["Date"], format="%Y-%m-%d")

    df_csv
    return (df_csv,)


@app.cell
def _(pd):
    df_sql = pd.read_csv(
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
    )

    df_sql = df_sql.dropna(subset=["Date"])
    df_sql["Date"] = pd.to_datetime(df_sql["Date"], format="%Y-%m-%d")

    df_sql
    return (df_sql,)


@app.cell
def _(df_csv, df_sql, pd):
    df = pd.merge(
        df_csv,
        df_sql,
        on="Date",
        how="inner",
        validate="1:1",
        suffixes=("_csv", "_db"),
    )

    df["Year"] = df["Date"].dt.year

    df["Landing_Outcome"] = df["Landing_Outcome"].str.strip()
    df = df[df["Landing_Outcome"] != "No attempt"].copy()

    df["LandingPad"] = df["LandingPad"].fillna("Ocean")

    df["LandingPadGroup"] = df["LandingPad"].map({
        "5e9e3032383ecb6bb234e7ca": "5e9e3032383ecb6bb234e7ca",
        "5e9e3032383ecb267a34e7c7": "5e9e3032383ecb267a34e7c7",
        "5e9e3033383ecbb9e534e7cc": "5e9e3033383ecbb9e534e7cc",
        "Ocean": "Other",
        "5e9e3032383ecb554034e7c9": "Other",
        "5e9e3032383ecb761634e7cb": "Other",
    })


    df["OrbitGroup"] = df["Orbit_csv"].map({
        "VLEO": "VLEO",
        "ISS": "ISS",
        "LEO": "LEO",
        "SO": "SSO",
        "SSO": "SSO",
        "PO": "PO",
        "GTO": "GTO",
        "MEO": "Other",
        "GEO": "Other",
        "HEO": "Other",
        "ES-L1": "Other",
    })
    _orbit_group_order = ["VLEO", "ISS", "LEO", "SSO", "PO", "GTO", "Other"]
    df["OrbitGroup"] = pd.Categorical(
        df["OrbitGroup"], categories=_orbit_group_order, ordered=True
    )

    df["LandingMethod"] = (
        df["Outcome"].str.split().str[-1].replace("None", "Ocean")
    )

    df = df.drop(
        columns=[
            "Date",
            "Time (UTC)",
            "Serial",
            "Payload",
            "Latitude",
            "Longitude",
            "Launch_Site",
            "Customer",
            "Booster_Version",
            "BoosterVersion",
            "Block",
            "Mission_Outcome",
            "Legs",
            "GridFins",
            "Landing_Outcome",
            "Reused",
            "ReusedCount",
            "Flights",
            "PayloadMass",
            "Outcome",
            "Orbit_db",
            "Year",
        ]
    )

    df = df.rename(
        columns={"PAYLOAD_MASS__KG_": "PayloadMass", "Orbit_csv": "Orbit"}
    )

    df = df.astype(
        {
            "LandingMethod": "category",
            "LaunchSite": "category",
            "PayloadMass": "float64",
            "LandingPad": "category",
            "Orbit": "category",
        }
    )

    df = df[
        [
            "FlightNumber",
            "Orbit",
            "OrbitGroup",
            "LaunchSite",
            "LandingPad",
            "LandingPadGroup",
            "LandingMethod",
            "PayloadMass",
            "Class",
        ]
    ]
    df["Result"] = df["Class"].map({1: "Succeeded", 0: "Failed"})

    df = df.sort_values(
        by=["OrbitGroup", "Result"], ascending=[True, False], ignore_index=True
    )

    df
    return (df,)


@app.cell
def _(df):
    df['LandingPad'].value_counts()
    return


@app.cell
def _():

    COLOR_SUCCESS = "#009E73"  
    COLOR_FAILURE = "#D55E00"  

    COLOR_RESULTAT = {"Succeeded": COLOR_SUCCESS, "Failed": COLOR_FAILURE}

    COLOR_BARPLOT = "#2B5C8F"  
    COLOR_TRENDLINE = "#1F1F1F"  

    ALPHA_BARPLOT = 0.25  
    ALPHA_SCATTER = 0.70 
    ALPHA_TRENDLINE = 1.00

    LINEWIDTH_TRENDLINE = 2.5

    LAYOUT_DEFAULT = dict(
        width=1115,
        height=283,
        margin=dict(l=40, r=40, t=60, b=40),
        template="plotly_white",
    )
    return COLOR_BARPLOT, COLOR_RESULTAT, LAYOUT_DEFAULT, LINEWIDTH_TRENDLINE


@app.cell(hide_code=True)
def _(
    COLOR_BARPLOT,
    COLOR_RESULTAT,
    LAYOUT_DEFAULT,
    LINEWIDTH_TRENDLINE,
    df,
    go,
    px,
):
    _orbit_order = (
        df.groupby("OrbitGroup")["FlightNumber"]
        .min()
        .sort_values(ascending=True)  
        .index.tolist()
    )

    _fig = px.scatter(
        df,
        x="FlightNumber",
        y="OrbitGroup",
        color="Result",
        title="<b>OrbitGroup by flight number</b>",
        labels={"FlightNumber": "Flight number", "OrbitGroup": "Orbit"},
        color_discrete_map=COLOR_RESULTAT,
    )

    for _, _group in df.groupby("OrbitGroup"):
        _fig.add_trace(
            go.Scatter(
                x=_group["FlightNumber"],
                y=_group["OrbitGroup"],
                mode="lines",
                line=dict(color=COLOR_BARPLOT, width=LINEWIDTH_TRENDLINE),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    _n_results = df["Result"].nunique()
    _fig.data = _fig.data[_n_results:] + _fig.data[:_n_results]

    _fig.update_traces(marker=dict(size=9), selector=dict(mode="markers"))

    _fig.update_layout(
        **LAYOUT_DEFAULT,
        showlegend=False,
        yaxis=dict(
            categoryorder="array",
            categoryarray=_orbit_order, 
        ),
    )

    _fig.show()
    return


@app.cell(hide_code=True)
def _(COLOR_BARPLOT, COLOR_RESULTAT, LAYOUT_DEFAULT, df, go, px):
    _orbit_order = (
        df.groupby("OrbitGroup")["PayloadMass"]
        .median()
        .sort_values(ascending=True)
        .index.tolist()
    )

    _fig_box = px.box(
        df,
        x="OrbitGroup",
        y="PayloadMass",
        points=False,
        labels={"OrbitGroup": "Orbit", "PayloadMass": "Payload mass (kg)"},
    )
    _fig_box.update_traces(marker_color=COLOR_BARPLOT)

    _fig_points = px.strip(
        df,
        x="OrbitGroup",
        y="PayloadMass",
        color="Result",
        color_discrete_map=COLOR_RESULTAT,
        hover_data=["FlightNumber", "LaunchSite", "Class"],
        stripmode="overlay",
    )
    _fig_points.update_traces(
        marker=dict(size=9, opacity=1),
        jitter=1,
    )

    _fig = go.Figure(data=_fig_box.data + _fig_points.data)

    _fig.update_layout(
        **LAYOUT_DEFAULT,
        title="<b>Distribution of the payload mass per orbit</b>",
        xaxis=dict(
            title="Orbit",
            categoryorder="array",
            categoryarray=_orbit_order,
        ),
        yaxis_title="Payload mass (kg)",
        legend_title_text="Result",
        showlegend=True,
    )

    _fig.show()
    return


@app.cell(hide_code=True)
def _(COLOR_RESULTAT, LAYOUT_DEFAULT, df, px):
    _df_counts = (
        df.groupby(["LaunchSite", "OrbitGroup", "Result"])
        .size()
        .reset_index(name="Count")
    )

    _fig_faceted = px.bar(
        _df_counts,
        x="OrbitGroup",
        y="Count",
        color="Result",
        facet_col="LaunchSite",
        color_discrete_map=COLOR_RESULTAT,
        barmode="stack",
        labels={
            "OrbitGroup": "Orbit",
            "Count": "Number of Launches",
            "Result": "Result",
        },
    )

    _fig_faceted.for_each_annotation(
        lambda a: a.update(text=f"<b>{a.text.split('=')[-1]}</b>")
    )

    _fig_faceted.update_layout(
        **LAYOUT_DEFAULT,
        title="<b>Launch Outcomes per Orbit (Faceted by Launch Site)</b>",
        yaxis_title="Total Launches",
        legend_title_text="Result",
    )

    _fig_faceted.show()
    return


@app.cell(hide_code=True)
def _(COLOR_RESULTAT, LAYOUT_DEFAULT, df, px):
    _df_counts = (
        df.groupby(["LandingMethod", "OrbitGroup", "Result"])
        .size()
        .reset_index(name="Count")
    )

    _fig_faceted = px.bar(
        _df_counts,
        x="OrbitGroup",
        y="Count",
        color="Result",
        facet_col="LandingMethod",
        color_discrete_map=COLOR_RESULTAT,
        barmode="stack",
        labels={
            "OrbitGroup": "Orbit",
            "Count": "Number of Launches",
            "Result": "Result",
        },
    )

    _fig_faceted.for_each_annotation(
        lambda a: a.update(text=f"<b>{a.text.split('=')[-1]}</b>")
    )

    _fig_faceted.update_layout(
        **LAYOUT_DEFAULT,
        title="<b>Launch Outcomes per Orbit (Faceted by LandingMethod)</b>",
        yaxis_title="Total Launches",
        legend_title_text="Result",
    )

    _fig_faceted.show()
    return


@app.cell(hide_code=True)
def _(COLOR_RESULTAT, LAYOUT_DEFAULT, df, px):
    _df_counts = (
        df.groupby(["LandingPad", "OrbitGroup", "Result"])
        .size()
        .reset_index(name="Count")
    )

    _fig_faceted = px.bar(
        _df_counts,
        x="OrbitGroup",
        y="Count",
        color="Result",
        facet_col="LandingPad",
        facet_col_wrap=3,
        color_discrete_map=COLOR_RESULTAT,
        barmode="stack",
        labels={
            "OrbitGroup": "Orbit",
            "Count": "Number of Launches",
            "Result": "Result",
        },
    )

    _fig_faceted.for_each_annotation(
        lambda a: a.update(text=f"<b>{a.text.split('=')[-1]}</b>")
    )

    LAYOUT_FACETED = {**LAYOUT_DEFAULT, "height": 550}

    _fig_faceted.update_layout(
        **LAYOUT_FACETED,
        title="<b>Launch Outcomes per Orbit (Faceted by LandingPad)</b>",
        legend_title_text="Result",
    )

    _fig_faceted.update_yaxes(matches="y", title_text="Total Launches")

    _fig_faceted.show()
    return


@app.cell(hide_code=True)
def _(np, pd, stats):
    def calculate_cramers_v(x, y):
        tbl = pd.crosstab(x, y)
        chi2 = stats.chi2_contingency(tbl)[0]
        n = tbl.sum().sum()
        r, c = tbl.shape
        return np.sqrt(chi2 / (n * (min(r, c) - 1)))

    def calculate_eta_squared(cat_col, num_col):
        df_clean = pd.DataFrame({"cat": cat_col, "num": num_col}).dropna()
        groups = [group["num"].values for _, group in df_clean.groupby("cat")]
        if len(groups) < 2:
            return 0
        H, _ = stats.kruskal(*groups)
        n = len(df_clean)
        k = len(groups)
        return max(0, (H - k + 1) / (n - k))

    def matrice_dependance_globale(df, columns):
        n_cols = len(columns)
        matrix = pd.DataFrame(
            np.zeros((n_cols, n_cols)), index=columns, columns=columns
        )

        for c1 in columns:
            for c2 in columns:
                if c1 == c2:
                    matrix.loc[c1, c2] = 1.0
                    continue

                s1, s2 = df[c1], df[c2]
                type1 = (
                    "num"
                    if pd.api.types.is_numeric_dtype(s1) and s1.nunique() > 10
                    else "cat"
                )
                type2 = (
                    "num"
                    if pd.api.types.is_numeric_dtype(s2) and s2.nunique() > 10
                    else "cat"
                )

                # Catégoriel vs Catégoriel -> V de Cramér
                if type1 == "cat" and type2 == "cat":
                    matrix.loc[c1, c2] = calculate_cramers_v(s1, s2)

                # Catégoriel vs Numérique -> Eta-carré
                elif type1 == "cat" and type2 == "num":
                    matrix.loc[c1, c2] = calculate_eta_squared(s1, s2)
                elif type1 == "num" and type2 == "cat":
                    matrix.loc[c1, c2] = calculate_eta_squared(s2, s1)

                # Numérique vs Numérique -> Corrélation de Spearman (valeur absolue)
                else:
                    corr, _ = stats.spearmanr(s1, s2, nan_policy="omit")
                    matrix.loc[c1, c2] = abs(corr)

        return matrix

    return (matrice_dependance_globale,)


@app.cell(hide_code=True)
def _(df, matrice_dependance_globale, px):
    _cols_to_test = df.columns.to_list()
    _matrice = matrice_dependance_globale(df, _cols_to_test)

    _fig = px.imshow(
        _matrice,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=0,
        zmax=1,
        title=r"Matrice de dépendance synthétique (<i>V</i>, eta<sup>2</sup>, Spearman)",
        aspect="auto",
    )

    _fig.update_layout(
        xaxis_title="",
        yaxis_title="",
    )

    _fig.show()
    return


@app.cell(hide_code=True)
def _(df, px):
    interval_columns = ["PayloadMass"]
    _phik_matrix = df.phik_matrix(interval_cols=interval_columns)

    _fig = px.imshow(
        _phik_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=0,
        zmax=1,
        title="Matrice de dépendance globale (Coefficients phi<sub>K</sub>)",
        aspect="auto",
    )

    _fig.update_layout(
        xaxis_title="",
        yaxis_title="",
    )

    _fig.show()
    return (interval_columns,)


@app.cell
def _(df, interval_columns):
    p_values = df.significance_matrix(interval_cols=interval_columns)
    p_values
    return


@app.cell
def _(df):
    y = df["Class"].astype(int).reset_index(drop=True)
    X = df[
        ["PayloadMass", "Orbit", "OrbitGroup", "LandingPad", "LaunchSite"]
    ].copy()
    X
    return X, y


@app.cell
def _():
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import (
        StandardScaler,
        OneHotEncoder,
        OrdinalEncoder,
        FunctionTransformer,
    )

    from sklearn.base import BaseEstimator
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import GradientBoostingClassifier

    from sklearn.model_selection import (
        train_test_split,
        GridSearchCV,
        StratifiedKFold,
        RepeatedStratifiedKFold,
        LeaveOneOut,
        cross_val_score,
        cross_val_predict,
    )
    from sklearn.metrics import (
        accuracy_score,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
        roc_curve,
        confusion_matrix,
        classification_report,
    )

    return (
        BaseEstimator,
        CalibratedClassifierCV,
        ColumnTransformer,
        FunctionTransformer,
        KNeighborsClassifier,
        LogisticRegression,
        OneHotEncoder,
        OrdinalEncoder,
        Pipeline,
        RandomForestClassifier,
        SVC,
        SimpleImputer,
        StandardScaler,
        StratifiedKFold,
        accuracy_score,
        confusion_matrix,
        cross_val_predict,
        cross_val_score,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
        roc_curve,
    )


@app.cell
def _():
    import optuna

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    return (optuna,)


@app.cell
def _():
    RANDOM_STATE = 42
    N_TRIALS = 60
    CV_FOLDS = 5
    return CV_FOLDS, N_TRIALS, RANDOM_STATE


@app.cell
def _(
    BaseEstimator,
    CalibratedClassifierCV,
    ColumnTransformer,
    FunctionTransformer,
    KNeighborsClassifier,
    LogisticRegression,
    OneHotEncoder,
    OrdinalEncoder,
    Pipeline,
    RANDOM_STATE,
    RandomForestClassifier,
    SVC,
    SimpleImputer,
    StandardScaler,
    XGBClassifier,
    pd,
):
    def _reduce_orbits(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["OrbitGroup"] = df["Orbit"].map(
            {
                "VLEO": "VLEO",
                "ISS": "ISS",
                "LEO": "LEO",
                "SO": "SSO",
                "SSO": "SSO",
                "PO": "PO",
                "GTO": "GTO",
                "MEO": "Other",
                "GEO": "Other",
                "HEO": "Other",
                "ES-L1": "Other",
            }
        )

        df["OrbitGroup"] = df["OrbitGroup"].fillna("Other")

        return df

    def _reduce_landing_pads(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["LandingPadGroup"] = df["LandingPad"].map({
            "5e9e3032383ecb6bb234e7ca": "5e9e3032383ecb6bb234e7ca",
            "5e9e3032383ecb267a34e7c7": "5e9e3032383ecb267a34e7c7",
            "5e9e3033383ecbb9e534e7cc": "5e9e3033383ecbb9e534e7cc",
            "Ocean": "Other",
            "5e9e3032383ecb554034e7c9": "Other",
            "5e9e3032383ecb761634e7cb": "Other",
        })
        df["LandingPadGroup"] = df["LandingPadGroup"].fillna("Other")

        return df


    def _get_feature_engineer() -> Pipeline:
        return Pipeline(
            steps=[
                ("reduce_orbits", FunctionTransformer(_reduce_orbits)),
                ("reduce_landing_pads", FunctionTransformer(_reduce_landing_pads)),
            ]
        )

    def _get_processor(config) -> ColumnTransformer:
        num_features = config.get("num", {}).get("features", [])
        cat_features = config.get("cat", {}).get("features", [])
        ord_features = config.get("ord", {}).get("features", [])
        ord_features_orders = config.get("ord", {}).get("orders", [])

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "num",
                    Pipeline(
                        [
                            ("imputer", SimpleImputer(strategy="median")),
                            ("scaler", StandardScaler()),
                        ]
                    ),
                    num_features,
                ),
                (
                    "cat",
                    Pipeline(
                        [
                            (
                                "imputer",
                                SimpleImputer(strategy="most_frequent"),
                            ),
                            (
                                "onehot",
                                OneHotEncoder(
                                    drop="if_binary",
                                    sparse_output=False,
                                    handle_unknown="ignore",
                                ),
                            ),
                        ]
                    ),
                    cat_features,
                ),
                (
                    "orbits",
                    Pipeline(
                        [
                            (
                                "imputer",
                                SimpleImputer(strategy="most_frequent"),
                            ),
                            (
                                "ordinal",
                                OrdinalEncoder(
                                    categories=ord_features_orders,
                                    handle_unknown="use_encoded_value",
                                    unknown_value=-1,
                                ),
                            ),
                        ]
                    ),
                    ord_features,
                ),
            ],
            remainder="drop",
        )

        return preprocessor

    def _get_model(model_name: str, params: dict) -> BaseEstimator:
        if model_name == "SVM":
            base_svc = SVC(
                class_weight="balanced", random_state=RANDOM_STATE, **params
            )
            return CalibratedClassifierCV(base_svc, ensemble=False)

        elif model_name == "LogisticRegression":
            return LogisticRegression(
                class_weight="balanced",
                max_iter=2000,
                random_state=RANDOM_STATE,
                **params,
            )

        elif model_name == "KNN":
            return KNeighborsClassifier(**params)

        elif model_name == "RandomForest":
            return RandomForestClassifier(
                class_weight="balanced", random_state=RANDOM_STATE, **params
            )

        elif model_name == "XGBoost":
            return XGBClassifier(
                eval_metric="logloss",
                verbosity=0,
                random_state=RANDOM_STATE,
                **params,
            )
        else:
            raise ValueError(f"Unknown model: {model_name}")

    def build_pipeline(
        processor_conf: dict, model_name: str, params: dict
    ) -> Pipeline:
        feature_engineer = _get_feature_engineer()
        preprocessor = _get_processor(processor_conf)
        model = _get_model(model_name, params)

        base_pipeline = Pipeline(
            steps=[
                ("feature_engineer", feature_engineer),
                ("preprocessor", preprocessor),
                ("classifier", model),
            ]
        )

        return base_pipeline

    return (build_pipeline,)


@app.cell
def _(
    N_TRIALS,
    RANDOM_STATE,
    accuracy_score,
    build_pipeline,
    confusion_matrix,
    cross_val_predict,
    cross_val_score,
    f1_score,
    optuna,
    precision_score,
    recall_score,
    roc_auc_score,
    time,
):
    def _make_objective(transformer_config, model_name, X_train, y_train, cv):
        neg_pos = max((y_train == 0).sum() / max((y_train == 1).sum(), 1), 0.1)

        def objective(trial):
            if model_name == "SVM":
                params = {
                    "C": trial.suggest_float("C", 0.01, 100, log=True),
                    "kernel": trial.suggest_categorical(
                        "kernel", ["rbf", "linear", "poly"]
                    ),
                    "gamma": trial.suggest_categorical(
                        "gamma", ["scale", "auto"]
                    ),
                }

            elif model_name == "LogisticRegression":
                solver = trial.suggest_categorical("solver", ["lbfgs", "saga"])
                if solver == "lbfgs":
                    l1_ratio = 0.0
                else:
                    l1_ratio = trial.suggest_categorical(
                        "l1_ratio", [0.0, 1.0]
                    )

                params = {
                    "C": trial.suggest_float("C", 0.001, 100, log=True),
                    "solver": solver,
                    "l1_ratio": l1_ratio,
                }

            elif model_name == "KNN":
                params = {
                    "n_neighbors": trial.suggest_int(
                        "n_neighbors", 2, min(20, len(X_train) - 1)
                    ),
                    "weights": trial.suggest_categorical(
                        "weights", ["uniform", "distance"]
                    ),
                    "metric": trial.suggest_categorical(
                        "metric", ["euclidean", "manhattan"]
                    ),
                }

            elif model_name == "RandomForest":
                params = {
                    "n_estimators": trial.suggest_int("n_estimators", 10, 50),
                    "max_depth": trial.suggest_int("max_depth", 1, 15),
                    "min_samples_split": trial.suggest_int(
                        "min_samples_split", 2, 12
                    ),
                    "min_samples_leaf": trial.suggest_int(
                        "min_samples_leaf", 1, 8
                    ),
                    "max_features": trial.suggest_categorical(
                        "max_features", ["sqrt", "log2"]
                    ),
                }

            elif model_name == "XGBoost":
                params = {
                    "n_estimators": trial.suggest_int("n_estimators", 10, 50),
                    "max_depth": trial.suggest_int("max_depth", 1, 8),
                    "learning_rate": trial.suggest_float(
                        "learning_rate", 0.001, 0.3, log=True
                    ),
                    "subsample": trial.suggest_float("subsample", 0.5, 1.0),
                    "colsample_bytree": trial.suggest_float(
                        "colsample_bytree", 0.5, 1.0
                    ),
                    "reg_alpha": trial.suggest_float(
                        "reg_alpha", 1e-8, 1.0, log=True
                    ),
                    "reg_lambda": trial.suggest_float(
                        "reg_lambda", 1e-8, 1.0, log=True
                    ),
                    "scale_pos_weight": trial.suggest_float(
                        "scale_pos_weight",
                        max(0.3, neg_pos * 0.5),
                        neg_pos * 3.0,
                    ),
                }
            pipe = build_pipeline(transformer_config, model_name, params)
            scores = cross_val_score(
                pipe, X_train, y_train, cv=cv, scoring="roc_auc", n_jobs=-1
            )
            return float(scores.mean())

        return objective

    def train_and_evaluate(
        transformer_config, model_name, X_train, X_test, y_train, y_test, cv
    ):
        print(f"  ┌── {model_name} — Optuna {N_TRIALS} trials")
        t0 = time.perf_counter()

        study = optuna.create_study(
            direction="maximize",
            sampler=optuna.samplers.TPESampler(
                seed=RANDOM_STATE, n_startup_trials=15
            ),
        )
        study.optimize(
            _make_objective(
                transformer_config, model_name, X_train, y_train, cv
            ),
            n_trials=N_TRIALS,
            show_progress_bar=False,
            gc_after_trial=True,
        )

        best_params = study.best_params
        best_cv_roc_auc = study.best_value
        elapsed = time.perf_counter() - t0

        print(
            f"  │   CV roc_auc best : {best_cv_roc_auc:.4f}  ({elapsed:.0f}s)"
        )
        print(f"  └── Params     : {best_params}")

        pipe = build_pipeline(transformer_config, model_name, best_params)

        # Détection automatique du mode d'évaluation
        is_same_dataset = (X_train is X_test) or (
            len(X_train) == len(X_test)
            and hasattr(X_train, "index")
            and X_train.index.equals(X_test.index)
        )

        if is_same_dataset:
            # Mode 1 : Dataset unique sans split (~70 samples) -> Out-Of-Fold avec CV
            y_pred = cross_val_predict(
                pipe, X_train, y_train, cv=cv, n_jobs=-1
            )
            y_prob = cross_val_predict(
                pipe,
                X_train,
                y_train,
                cv=cv,
                method="predict_proba",
                n_jobs=-1,
            )[:, 1]
            pipe.fit(
                X_train, y_train
            )  # Réentraînement sur 100% des données pour export
        else:
            # Mode 2 : Train/Test Split classique (Grand dataset futur)
            pipe.fit(X_train, y_train)
            y_pred = pipe.predict(X_test)
            y_prob = pipe.predict_proba(X_test)[:, 1]

        return {
            "model": model_name,
            "best_cv_roc_auc": round(best_cv_roc_auc, 6),
            "f1": round(f1_score(y_test, y_pred, zero_division=0), 6),
            "roc_auc": round(roc_auc_score(y_test, y_prob), 6),
            "precision": round(
                precision_score(y_test, y_pred, zero_division=0), 6
            ),
            "recall": round(recall_score(y_test, y_pred, zero_division=0), 6),
            "accuracy": round(accuracy_score(y_test, y_pred), 6),
            "elapsed_s": round(elapsed, 1),
            "best_params": best_params,
            "_y_pred": y_pred,
            "_y_prob": y_prob,
            "_cm": confusion_matrix(y_test, y_pred),
            "_study": study,
            "_pipe": pipe,
        }

    return (train_and_evaluate,)


@app.cell(hide_code=True)
def _(LINEWIDTH_TRENDLINE, go, make_subplots, np, pd, roc_curve):
    MODEL_COLORS = {
        "SVM": "#818cf8",
        "LogisticRegression": "#34d399",
        "RandomForest": "#fbbf24",
        "KNN": "#f87171",
        "XGBoost": "#60a5fa",
    }

    def _base(title, height=283, **kw):
        return dict(
            height=height,
            width=1115,
            margin=dict(l=40, r=40, t=60, b=40),
            template="plotly_white",
            **kw,
        )

    def chart_metric_comparison(rdf):
        metrics = [
            ("roc_auc", "ROC-AUC", "#34d399"),
            ("f1", "F1-Score", "#818cf8"),
            ("precision", "Precision", "#fbbf24"),
            ("recall", "Recall", "#f87171"),
            ("accuracy", "Accuracy", "#94a3b8"),
        ]

        fig = go.Figure()
        for key, label, color in metrics:
            vals = rdf[key].round(4)
            fig.add_trace(
                go.Bar(
                    name=label,
                    x=rdf["model"],
                    y=vals,
                    text=vals.map("{:.3f}".format),
                    textposition="outside",
                    marker=dict(color=color, opacity=0.88),
                )
            )

        fig.update_layout(
            **_base("Model Comparison - All Metrics", height=560),
            barmode="group",
            yaxis=dict(range=[0, 1.15], title="Score"),
            xaxis=dict(title="Modèle"),
            legend=dict(orientation="h", y=-0.18),
        )
        return fig

    def chart_roc_curves(all_results, y_test):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode="lines",
                line=dict(
                    dash="dash", color="#475569", width=LINEWIDTH_TRENDLINE
                ),
                name="Random (AUC=0.500)",
            )
        )

        for r in all_results:
            fpr, tpr, _ = roc_curve(y_test, r["_y_prob"])
            fig.add_trace(
                go.Scatter(
                    x=fpr,
                    y=tpr,
                    mode="lines",
                    name=f"{r['model']}  (AUC={r['roc_auc']:.3f})",
                    line=dict(color=MODEL_COLORS[r["model"]], width=2.5),
                )
            )

        fig.update_layout(
            **_base("ROC Curves — Test Set"),
            xaxis=dict(title="False Positive Rate", range=[-0.02, 1.02]),
            yaxis=dict(title="True Positive Rate", range=[-0.02, 1.02]),
        )
        return fig

    def chart_confusion_matrices(all_results):
        n = len(all_results)
        labels = ["Failure (0)", "Success (1)"]

        fig = make_subplots(
            rows=1,
            cols=n,
            subplot_titles=[r["model"] for r in all_results],
            horizontal_spacing=0.06,
        )

        for i, r in enumerate(all_results, 1):
            cm = r["_cm"]
            cmf = cm[::-1]
            lf = labels[::-1]
            tot = cm.sum()
            ann = [
                [
                    f"<b>{cmf[row, col]}</b><br>{cmf[row, col] / tot * 100:.0f}%"
                    for col in range(2)
                ]
                for row in range(2)
            ]

            fig.add_trace(
                go.Heatmap(
                    z=cmf,
                    x=labels,
                    y=lf,
                    text=ann,
                    texttemplate="%{text}",
                    showscale=(i == n),
                    zmin=0,
                    zmax=max(cm.max(), 1),
                ),
                row=1,
                col=i,
            )
            fig.update_xaxes(title_text="Predicted", row=1, col=i)
            fig.update_yaxes(
                title_text="Actual" if i == 1 else "", row=1, col=i
            )
        fig.update_layout(**_base("Confusion Matrices — Test Set", height=380))
        return fig

    def chart_optuna_history(all_results):
        n = len(all_results)

        fig = make_subplots(
            rows=1,
            cols=n,
            subplot_titles=[r["model"] for r in all_results],
            shared_yaxes=True,
            horizontal_spacing=0.05,
        )

        for i, r in enumerate(all_results, 1):
            dft = r["_study"].trials_dataframe()
            dft["value"] = (
                pd.to_numeric(dft["value"], errors="coerce").ffill().fillna(0)
            )
            dft["best"] = dft["value"].cummax()
            color = MODEL_COLORS[r["model"]]

            fig.add_trace(
                go.Scatter(
                    x=dft["number"],
                    y=dft["value"],
                    mode="markers",
                    marker=dict(color=color, size=4, opacity=0.3),
                    showlegend=False,
                ),
                row=1,
                col=i,
            )

            fig.add_trace(
                go.Scatter(
                    x=dft["number"],
                    y=dft["best"],
                    mode="lines",
                    line=dict(color=color, width=2.5),
                    name=f"{r['model']}  best={r['best_cv_roc_auc']:.3f}",
                ),
                row=1,
                col=i,
            )

            fig.update_xaxes(title_text="Trial #", row=1, col=i)
            fig.update_yaxes(
                title_text="CV ROC_AUC" if i == 1 else "", row=1, col=i
            )
        fig.update_layout(
            **_base("Optimization History (Optuna)", height=420),
            legend=dict(orientation="h", y=-0.28),
        )
        return fig

    def chart_radar(rdf):
        metrics = ["roc_auc", "f1", "precision", "recall", "accuracy"]
        labels = ["ROC-AUC", "F1-Score", "Precision", "Recall", "Accuracy"]
        fig = go.Figure()

        for _, row in rdf.iterrows():
            vals = [row[m] for m in metrics] + [row[metrics[0]]]
            color = MODEL_COLORS[row["model"]]

            fig.add_trace(
                go.Scatterpolar(
                    r=vals,
                    theta=labels + [labels[0]],
                    fill="toself",
                    name=row["model"],
                    line=dict(color=color, width=2.5),
                    fillcolor=color,
                    # opacity=0.15
                )
            )

        fig.update_layout(
            **_base("Multi-Metric Comparison", height=520),
            polar=dict(radialaxis=dict(range=[0, 1])),
        )
        return fig

    def chart_feature_importance(all_results):
        tree_res = [
            r for r in all_results if r["model"] in ("RandomForest", "XGBoost")
        ]
        if not tree_res:
            return None
        n = len(tree_res)

        fig = make_subplots(
            rows=1,
            cols=n,
            subplot_titles=[r["model"] for r in tree_res],
            horizontal_spacing=0.14,
        )

        for i, r in enumerate(tree_res, 1):
            pipe = r["_pipe"]
            imp = pipe.named_steps["classifier"].feature_importances_

            # 1. Extraction dynamique des noms de variables après prétraitement
            raw_names = pipe.named_steps[
                "preprocessor"
            ].get_feature_names_out()

            # 2. Nettoyage des préfixes générés par ColumnTransformer (ex: 'num__PayloadMass' -> 'PayloadMass')
            feature_names_out = [name.split("__")[-1] for name in raw_names]

            idx = np.argsort(imp)
            color = MODEL_COLORS[r["model"]]

            fig.add_trace(
                go.Bar(
                    x=imp[idx],
                    y=[feature_names_out[j] for j in idx],
                    orientation="h",
                    marker=dict(color=imp[idx], showscale=False),
                    text=[f"{v:.3f}" for v in imp[idx]],
                    textposition="outside",
                    showlegend=False,
                ),
                row=1,
                col=i,
            )
            fig.update_xaxes(title_text="Importance", row=1, col=i)

        fig.update_layout(
            **_base("Feature Importances — Tree Models", height=380)
        )
        return fig

    def chart_timing(rdf):
        df_s = rdf.sort_values("elapsed_s")
        colors = [MODEL_COLORS[m] for m in df_s["model"]]

        fig = go.Figure(
            go.Bar(
                x=df_s["elapsed_s"],
                y=df_s["model"],
                orientation="h",
                text=df_s["elapsed_s"].map("{:.0f}s".format),
                textposition="outside",
                marker=dict(color=colors, opacity=0.85),
            )
        )

        fig.update_layout(
            **_base("Optuna Tuning Time per Model", height=360),
            xaxis=dict(title="Seconds"),
            yaxis=dict(title=""),
        )
        return fig

    return (
        chart_confusion_matrices,
        chart_feature_importance,
        chart_metric_comparison,
        chart_optuna_history,
        chart_radar,
        chart_roc_curves,
        chart_timing,
    )


@app.cell
def _(
    CV_FOLDS,
    RANDOM_STATE,
    StratifiedKFold,
    X,
    df,
    pd,
    train_and_evaluate,
    y,
):
    reduced_orbit_order = ["VLEO", "ISS", "LEO", "SSO", "PO", "GTO", "Other"]

    transformer_config = {
        "num": {
            "features": ["PayloadMass"],
        },
        "cat": {
            "features": ["LandingPadGroup"],
        },
        "ord": {"features": ["OrbitGroup"], "orders": [reduced_orbit_order]},
    }

    print(f"Dataset : {len(df)} rows  |  {X.shape[1]} features")
    print(f"   Features       : {list(X.columns)}")
    print(
        f"   Class balance  : {y.sum()} succès ({y.mean():.1%})  /  {(y == 0).sum()} échecs"
    )

    X_train = X.copy()
    X_test = X.copy()
    y_train = y.copy()
    y_test = y.copy()

    cv = StratifiedKFold(
        n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE
    )

    print("=" * 65)
    print("Optuna Hyperparameter Search")
    print("=" * 65)
    model_names = ["SVM", "LogisticRegression", "KNN", "RandomForest"]
    all_results: list[dict] = []
    for name in model_names:
        r = train_and_evaluate(
            transformer_config, name, X_train, X_test, y_train, y_test, cv
        )
        all_results.append(r)

    scalar_keys = [k for k in all_results[0] if not k.startswith("_")]
    results_df = pd.DataFrame(
        [{k: r[k] for k in scalar_keys} for r in all_results]
    )

    print("=" * 65)
    print("  RESULTS SUMMARY")
    print("=" * 65)
    cols = [
        "model",
        "f1",
        "roc_auc",
        "precision",
        "recall",
        "accuracy",
        "best_cv_roc_auc",
    ]
    print(
        results_df[cols].to_string(index=False, float_format="{:.4f}".format)
    )

    best = results_df.loc[results_df["roc_auc"].idxmax()]
    print(
        f"  Best (roc_auc): {best['model']}  AUC={best['roc_auc']:.4f}  F1={best['f1']:.4f}"
    )

    csv_path = "../model_results.csv"
    results_df.drop(columns=["best_params"]).to_csv(csv_path, index=False)
    print(f" CSV -> {csv_path}")
    return all_results, results_df, y_test


@app.cell
def _(
    all_results: list[dict],
    chart_confusion_matrices,
    chart_feature_importance,
    chart_metric_comparison,
    chart_optuna_history,
    chart_radar,
    chart_roc_curves,
    chart_timing,
    results_df,
    y_test,
):
    charts = {
        "1_metric_comparison": chart_metric_comparison(results_df),
        "2_roc_curves": chart_roc_curves(all_results, y_test),
        "3_confusion_matrices": chart_confusion_matrices(all_results),
        "4_optuna_history": chart_optuna_history(all_results),
        "5_radar": chart_radar(results_df),
        "6_feature_importance": chart_feature_importance(all_results),
        "7_timing": chart_timing(results_df),
    }
    for _name, _fig in charts.items():
        if _fig is None:
            continue
        _fig.show()
    return


@app.cell
def _(all_results: list[dict], np):
    import matplotlib.pyplot as plt
    from sklearn.tree import plot_tree

    # 1. Extraction du modèle et du préprocesseur
    best_model = all_results[-1]["_pipe"]
    forest = best_model.named_steps["classifier"]
    preprocessor_fitted = best_model.named_steps["preprocessor"]

    # 2. Récupération des noms de colonnes après Feature Engineering
    try:
        feature_names = preprocessor_fitted.get_feature_names_out()
    except AttributeError:
        # Si le préprocesseur ne supporte pas get_feature_names_out
        feature_names = None

    # 3. Sélection du nombre d'arbres à afficher (ex: les 3 premiers)
    num_trees_to_plot = min(3, len(forest.estimators_))

    fig, axes = plt.subplots(num_trees_to_plot, 1, figsize=(18, 8 * num_trees_to_plot))
    if num_trees_to_plot == 1:
        axes = [axes]

    for i in range(num_trees_to_plot):
        # Pour RandomForest: accès direct à l'arbre via forest.estimators_[i]
        # Si c'est un GradientBoosting binary: remplacer par forest.estimators_[i][0]
        tree = forest.estimators_[i]
        if isinstance(tree, (list, tuple, np.ndarray)):
            tree = tree[0]

        plot_tree(
            tree,
            feature_names=feature_names,
            filled=True,
            rounded=True,
            max_depth=3,  # Limite la profondeur affichée pour garder l'image lisible
            ax=axes[i],
            fontsize=10,
        )
        axes[i].set_title(
            f"Arbre {i+1} / {len(forest.estimators_)}", fontsize=14, fontweight="bold"
        )

    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
