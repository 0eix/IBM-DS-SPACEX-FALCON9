import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. CHARGEMENT ET PRÉPARATION DES DONNÉES
# -----------------------------------------------------------------------------
block_type = pd.CategoricalDtype(categories=[1, 2, 3, 4, 5], ordered=True)

df = pd.read_csv(
    "../../data/dataset_part_2.csv",
    dtype={
        "FlightNumber": 'int64',
        "Class": 'int64',
        "Serial": 'category',
        "Orbit": "category",
        "LaunchSite": "category",
        "Flights": 'int64',
        "ReusedCount": 'int64',
        "PayloadMass": 'float64',
        "Block": block_type,
        "Outcome": 'category',
        "GridFins": 'bool',
        "Legs": 'bool'
    },
    parse_dates=["Date"],
    date_format="%Y-%m-%d",
)

# Traitement de la colonne LandingPad
df['LandingPad'] = df['LandingPad'].fillna('Aucune (NaN/Mer)')
df['LandingPad'] = df['LandingPad'].astype('category')

# Extraction de la première partie (action/tentative) et de la seconde (type de cible)
outcome_parts = df['Outcome'].astype(str).str.split(expand=True)
df['TriedLanding'] = outcome_parts[0] != 'None'
df['TargetDefined'] = outcome_parts[1] != 'None'
# df_cleaned = df[df['TargetDefined']].copy()

# Subsetting & création de la colonne résultat
df_payload = df.drop(columns=['Longitude', 'Latitude', 'BoosterVersion'], errors='ignore').copy()
df_payload['Resultat'] = df_payload['Class'].map({1: 'Succès', 0: 'Échec / Sacrifié'})

# Options pour les Dropdowns (LaunchSite, Orbit, LandingPad)
site_options = [{'label': 'Tous les sites', 'value': 'ALL'}] + [
    {'label': str(site), 'value': str(site)} for site in sorted(df_payload['LaunchSite'].unique())
]

orbit_options = [{'label': 'Toutes les orbites', 'value': 'ALL'}] + [
    {'label': str(orb), 'value': str(orb)} for orb in sorted(df_payload['Orbit'].unique())
]

pad_options = [{'label': 'Toutes les LandingPads', 'value': 'ALL'}] + [
    {'label': str(pad), 'value': str(pad)} for pad in sorted(df_payload['LandingPad'].unique())
]

block_options = [{'label': 'Tous les blocks', 'value': 'ALL'}] + [
    {'label': str(block), 'value': int(block)} for block in sorted(df_payload['Block'].unique())
]

# Options pour les Checkboxes (GridFins & Legs)
boolean_checklist_options = [
    {'label': ' Avec (True)', 'value': True},
    {'label': ' Sans (False)', 'value': False}
]

tried_options = [
    {'label': ' Tentative (True)', 'value': True},
    {'label': ' Sans tentative (False)', 'value': False}
]

target_options = [
    {'label': ' Cible définie (True)', 'value': True},
    {'label': ' Sans cible définie (False)', 'value': False}
]

class_options = [
    {'label': 'Succès', 'value': 1},
    {'label': 'Échec / Sacrifié', 'value': 0},
]

# -----------------------------------------------------------------------------
# 2. CONFIGURATION DE L'APPLICATION DASH
# -----------------------------------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f8f9fa'},
    children=[

        # En-tête
        html.H1(
            "SpaceX Falcon 9 - Analyse du PayloadMass",
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}
        ),

        # Panneau des filtres
        html.Div(
            style={
                'backgroundColor': '#ffffff',
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'marginBottom': '25px',
                'display': 'flex',
                'flexDirection': 'column',
                'gap': '20px'
            },
            children=[
                # LIGNE 1 : Class, TriedLanding, TargetDefined (Checkboxes)
                html.Div(
                    style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '15px'},
                    children=[
                        # Filtre 1 : Class Checkbox
                        html.Div(style={'width': '32%'}, children=[
                            html.Label("Classe :", style={'fontWeight': 'bold', 'color': '#34495e', 'marginBottom': '8px', 'display': 'block'}),
                            dcc.Checklist(
                                id='class-checklist',
                                options=class_options,
                                value=[0, 1], # Par défaut, tout est coché (équivalent de "Tous")
                                inline=True, # Alignement horizontal des cases
                                inputStyle={'marginRight': '5px', 'cursor': 'pointer'},
                                labelStyle={'marginRight': '20px', 'cursor': 'pointer'}
                            )
                        ]),

                        # Filtre 2 : TriedLanding Checkbox
                        html.Div(style={'width': '32%'}, children=[
                            html.Label("Tentative d'atterrissage :", style={'fontWeight': 'bold', 'color': '#34495e', 'marginBottom': '8px', 'display': 'block'}),
                            dcc.Checklist(
                                id='tried-checklist',
                                options=tried_options,
                                value=[True, False], # Par défaut, tout est coché (équivalent de "Tous")
                                inline=True, # Alignement horizontal des cases
                                inputStyle={'marginRight': '5px', 'cursor': 'pointer'},
                                labelStyle={'marginRight': '20px', 'cursor': 'pointer'}
                            )
                        ]),

                        # Filtre 3 : TargetDefined Checkbox
                        html.Div(style={'width': '32%'}, children=[
                            html.Label("Cible d'atterrissage définie :", style={'fontWeight': 'bold', 'color': '#34495e', 'marginBottom': '8px', 'display': 'block'}),
                            dcc.Checklist(
                                id='target-checklist',
                                options=target_options,
                                value=[True, False], # Par défaut, tout est coché (équivalent de "Tous")
                                inline=True,
                                inputStyle={'marginRight': '5px', 'cursor': 'pointer'},
                                labelStyle={'marginRight': '20px', 'cursor': 'pointer'}
                            )
                        ]),
                    ]
                ),


                # LIGNE 2 : LaunchSite, Orbit, LandingPad (Dropdowns)
                html.Div(
                    style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '15px'},
                    children=[
                        # Filtre 3 : LaunchSite
                        html.Div(style={'width': '32%'}, children=[
                            html.Label("Site de Lancement :", style={'fontWeight': 'bold', 'color': '#34495e'}),
                            dcc.Dropdown(
                                id='site-dropdown',
                                options=site_options,
                                value='ALL',
                                clearable=False
                            )
                        ]),

                        # Filtre 4 : Orbit
                        html.Div(style={'width': '32%'}, children=[
                            html.Label("Orbite :", style={'fontWeight': 'bold', 'color': '#34495e'}),
                            dcc.Dropdown(
                                id='orbit-dropdown',
                                options=orbit_options,
                                value='ALL',
                                clearable=False
                            )
                        ]),

                        # Filtre 5 : LandingPad
                        html.Div(style={'width': '32%'}, children=[
                            html.Label("Zone d'atterrissage (LandingPad) :", style={'fontWeight': 'bold', 'color': '#34495e'}),
                            dcc.Dropdown(
                                id='pad-dropdown',
                                options=pad_options,
                                value='ALL',
                                clearable=False
                            )
                        ]),
                    ]
                ),

                # LIGNE 3 : GridFins & Legs (Checkboxes)
                html.Div(
                    style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '15px'},
                    children=[
                        # Filtre 6 : Block
                        html.Div(style={'width': '32%'}, children=[
                            html.Label("Bloc (Block) :", style={'fontWeight': 'bold', 'color': '#34495e'}),
                            dcc.Dropdown(
                                id='block-dropdown',
                                options=block_options,
                                value='ALL',
                                clearable=False
                            )
                        ]),

                        # Filtre 7 : GridFins Checkbox
                        html.Div(style={'width': '32%'}, children=[
                            html.Label("Équipement GridFins :", style={'fontWeight': 'bold', 'color': '#34495e', 'marginBottom': '8px', 'display': 'block'}),
                            dcc.Checklist(
                                id='gridfins-checklist',
                                options=boolean_checklist_options,
                                value=[True, False], # Par défaut, tout est coché (équivalent de "Tous")
                                inline=True, # Alignement horizontal des cases
                                inputStyle={'marginRight': '5px', 'cursor': 'pointer'},
                                labelStyle={'marginRight': '20px', 'cursor': 'pointer'}
                            )
                        ]),

                        # Filtre 8 : Legs Checkbox
                        html.Div(style={'width': '32%'}, children=[
                            html.Label("Équipement Legs (Pieds) :", style={'fontWeight': 'bold', 'color': '#34495e', 'marginBottom': '8px', 'display': 'block'}),
                            dcc.Checklist(
                                id='legs-checklist',
                                options=boolean_checklist_options,
                                value=[True, False], # Par défaut, tout est coché (équivalent de "Tous")
                                inline=True,
                                inputStyle={'marginRight': '5px', 'cursor': 'pointer'},
                                labelStyle={'marginRight': '20px', 'cursor': 'pointer'}
                            )
                        ]),
                    ]
                )
            ]
        ),

        # Zone du Graphique
        html.Div(
            style={
                'backgroundColor': '#ffffff',
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            },
            children=[
                dcc.Graph(id='payload-scatter-chart')
            ]
        )
    ]
)


# -----------------------------------------------------------------------------
# 3. CALLBACK POUR LE FILTRAGE DYNAMIQUE ET CUMULATIF
# -----------------------------------------------------------------------------

# Limites fixes pour les axes
y_min = df_payload['PayloadMass'].min() - 500
y_max = df_payload['PayloadMass'].max() + 500

x_min = df_payload['FlightNumber'].min() - 1
x_max = df_payload['FlightNumber'].max() + 1


@app.callback(
    Output('payload-scatter-chart', 'figure'),
    [
        Input('class-checklist', 'value'),
        Input('tried-checklist', 'value'),
        Input('target-checklist', 'value'),
        Input('site-dropdown', 'value'),
        Input('orbit-dropdown', 'value'),
        Input('pad-dropdown', 'value'),
        Input('block-dropdown', 'value'),
        Input('gridfins-checklist', 'value'),
        Input('legs-checklist', 'value'),
    ]
)
def update_scatter_plot(
        selected_class,
        selected_tried,
        selected_target,
        selected_site,
        selected_orbit,
        selected_pad,
        selected_block,
        selected_gridfins,
        selected_legs,
):
    # 1. Copie locale du dataset
    filtered_df = df_payload.copy()

    # 2. Application séquentielle des filtres
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['LaunchSite'] == selected_site]

    if selected_orbit != 'ALL':
        filtered_df = filtered_df[filtered_df['Orbit'] == selected_orbit]

    if selected_pad != 'ALL':
        filtered_df = filtered_df[filtered_df['LandingPad'] == selected_pad]

    if selected_block != 'ALL':
        filtered_df = filtered_df[filtered_df['Block'] == selected_block]

    # Filtrage par Checkboxes (Utilisation de .isin() car selected_gridfins est une liste [True, False])
    filtered_df = filtered_df[filtered_df['Class'].isin(selected_class)]
    filtered_df = filtered_df[filtered_df['GridFins'].isin(selected_gridfins)]
    filtered_df = filtered_df[filtered_df['Legs'].isin(selected_legs)]
    filtered_df = filtered_df[filtered_df['TriedLanding'].isin(selected_tried)]
    filtered_df = filtered_df[filtered_df['TargetDefined'].isin(selected_target)]

    # 3. Traitement du cas où aucun vol ne correspond aux critères
    if filtered_df.empty:
        fig = px.scatter(title="<b>Aucun vol ne correspond à ces critères combinés.</b>")
        fig.update_layout(
            template="plotly_white",
            xaxis=dict(range=[x_min, x_max], title="Numéro de Vol (FlightNumber)"),
            yaxis=dict(range=[y_min, y_max], title="Masse de la charge utile (kg)")
        )
        return fig

    # 4. Génération du graphique Plotly Express
    fig = px.scatter(
        filtered_df,
        x='FlightNumber',
        y='PayloadMass',
        color='Resultat',
        symbol='Resultat',
        color_discrete_map={'Succès': '#2ecc71', 'Échec / Sacrifié': '#e74c3c'},
        symbol_map={'Succès': 'circle', 'Échec / Sacrifié': 'x'},
        hover_data={
            'FlightNumber': True,
            'PayloadMass': ':.1f',
            'LaunchSite': True,
            'Orbit': True,
            'LandingPad': True,
            'Date': '|%Y-%m-%d',
            'Resultat': False,
            'Outcome': True,
            'Flights': True,
            'Reused': True,
            'ReusedCount': True,
            'Block': True,
            'GridFins': True,
            'Legs': True,
        },
        labels={
            'FlightNumber': 'Numéro de Vol (FlightNumber)',
            'PayloadMass': 'Masse de la charge utile (kg)',
            'Resultat': 'Résultat'
        },
        title=f"<b>Évolution du PayloadMass par Vol</b> — <i>{len(filtered_df)} vol(s) trouvé(s)</i>"
    )

    # 5. Ajustements visuels et fixation des axes
    fig.update_traces(marker=dict(size=11, line=dict(width=1, color='black')))
    fig.update_layout(
        template='plotly_white',
        legend_title_text='Statut',
        hoverlabel=dict(bgcolor="white", font_size=12),
        xaxis=dict(
            range=[x_min, x_max],
            autorange=False,
            dtick=10
        ),
        yaxis=dict(
            range=[y_min, y_max],
            autorange=False
        )
    )

    return fig


# -----------------------------------------------------------------------------
# 4. LANCEMENT DU SERVEUR
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)