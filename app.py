import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=["/assets/styles.css", "/assets/animation.css"])
app.title = "Digital Colonization Narrative"

# ================= Load & Clean Data =================

df_dependency = pd.read_csv("data/youth_dependency_index.csv")
df_ownership = pd.read_csv("data/platform_ownership.csv")
df_ownership["Ownership_Percentage"] = df_ownership["Ownership_Percentage"].str.replace(r"[~><%]", "", regex=True).astype(float)

df_flow = pd.read_csv("data/data_flow_paths.csv")
nodes = list(set(df_flow["Origin_Country"].tolist() + df_flow["Destination_Country"].tolist()))
node_indices = {name: idx for idx, name in enumerate(nodes)}
df_flow["source_idx"] = df_flow["Origin_Country"].map(node_indices)
df_flow["target_idx"] = df_flow["Destination_Country"].map(node_indices)

df_local = pd.read_csv("data/local_apps_usage.csv")
df_laws = pd.read_csv("data/digital_laws_score.csv")
df_time = pd.read_csv("data/screen_time_stats.csv")
df_algo = pd.read_csv("data/ad_algo_exposure.csv")
df_attention = pd.merge(df_time, df_algo, on="Country")
df_attention["Attention_Index"] = df_attention["Avg_Screen_Time_Min"] * df_attention["Ad_Algo_Score"]

# ================== Visuals ==================

fig_donut = px.pie(df_dependency, names='Country', values='Youth_Dependency_Index_Percent', hole=0.45, title="Youth Dependency (%)")
fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')

fig_treemap = px.treemap(df_ownership, path=['Parent_Company', 'Platform'], values='Ownership_Percentage', color='Country_of_Origin', title="Platform Ownership Map")
fig_treemap.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')

fig_sankey = go.Figure(data=[go.Sankey(
    node=dict(pad=15, thickness=20, label=nodes, color="#30cfd0"),
    link=dict(source=df_flow["source_idx"], target=df_flow["target_idx"], value=[1]*len(df_flow), label=df_flow["Platform"] + " → " + df_flow["Company"]))])
fig_sankey.update_layout(title_text="Data Flow Across Borders", font_size=10, paper_bgcolor='rgba(0,0,0,0)', font_color='white')

fig_local = px.bar(df_local, x="App_Name", y="Youth_Adoption_Percent", color="Country", title="Local Alternatives Usage")
fig_local.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', family='Segoe UI'), title_font=dict(size=18, color='#ff6ec4', family='Segoe UI'), legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0)', bordercolor='rgba(255,255,255,0.2)'), xaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'))

fig_attention = px.bar(df_attention, x="Country", y="Attention_Index", title="Attention Exploitation Index", color="Attention_Index", color_continuous_scale="Plasma")
fig_attention.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')

policy_table = dash_table.DataTable(
    columns=[{"name": i, "id": i} for i in df_laws.columns],
    data=df_laws.to_dict('records'),
    style_table={'overflowX': 'auto'},
    style_cell={'textAlign': 'center', 'color': '#fff', 'backgroundColor': '#1f1f2e'},
    style_header={'backgroundColor': '#333', 'fontWeight': 'bold', 'color': '#f0f0f0'},
)

# ================= Layout ==================

app.layout = html.Div(className="dashboard", children=[
    html.Div(className="dashboard-header animate-fade", children=[
        html.H1("📱 Digital Colonization", className="title"),
        html.P("Uncovering the Global Grip Over Your Digital World", className="subtitle"),
    ]),

    html.Div(className="story-section animate-rise", children=[
        html.H2("🌍 Youth Dependency on Foreign Tech"),
        html.P("The future of any nation lies in its youth. Yet today, they rely heavily on platforms not made or governed by their own country."),
        dcc.Graph(figure=fig_donut, config={'displayModeBar': False})
    ]),

    html.Div(className="story-section animate-rise", children=[
        html.H2("🏢 Who Really Owns Your Digital Space?"),
        html.P("Tech platforms might feel local, but their ownership is concentrated in the hands of a few global corporations."),
        dcc.Graph(figure=fig_treemap, config={'displayModeBar': False})
    ]),

    html.Div(className="story-section animate-rise", children=[
        html.H2("📡 Cross-Border Data Flows"),
        html.P("Every click, every swipe—your data travels far. This visual shows where your information flows across borders."),
        dcc.Graph(figure=fig_sankey, config={'displayModeBar': False})
    ]),

    html.Div(className="story-section animate-rise", children=[
        html.H2("📲 Rise of Local Alternatives"),
        html.P("Despite the dominance of foreign apps, countries are building their own platforms. But are youth embracing them?"),
        dcc.Graph(figure=fig_local, config={'displayModeBar': False})
    ]),

    html.Div(className="story-section animate-rise", children=[
        html.H2("🛡️ Are We Protected Enough?"),
        html.P("How do digital laws across nations compare? Which countries offer better protection against tech overreach?"),
        html.Div(className="card", children=[
            html.H3("Policy Comparison", className="table-title"),
            policy_table
        ])
    ]),

    html.Div(className="story-section animate-rise", children=[
        html.H2("💥 Exploiting Attention in the Algorithm Age"),
        html.P("Platforms thrive on your attention. The more you stay, the more they profit. Here's how deeply different nations are being pulled into the algorithm trap."),
        dcc.Graph(figure=fig_attention, config={'displayModeBar': False})
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
