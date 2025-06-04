from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from markdown_texts import markdown_texts

# Cargar datos
df = pd.read_csv("HRDataset_v14.csv")
df["DOB"] = pd.to_datetime(df["DOB"], errors="coerce")
today = pd.to_datetime("today")
df = df[df["DOB"].notna() & (df["DOB"] < today)]
df["Edad"] = ((today - df["DOB"]).dt.days // 365).astype(int)
df = df[(df["Edad"] > 17) & (df["Edad"] < 100)]

# Gráficos
fig1 = px.scatter(
    df,
    x="Edad",
    y="Salary",
    color="Sex",
    title="Edad vs Salario",
    hover_data=["Employee_Name", "Department", "Position"],
    labels={"Edad": "Edad", "Salary": "Salario"},
)

fig2 = px.box(
    df,
    x="Department",
    y="Salary",
    color="Department",
    points="all",
    title="Salarios por Departamento",
)
fig2.update_layout(showlegend=False)

fig3 = px.histogram(
    df,
    x="DOB",
    color="Sex",
    nbins=30,
    marginal="rug",
    title="Edades por Género",
    labels={"DOB": "Fecha de nacimiento"},
    hover_data=df.columns,
)
fig3.update_layout(bargap=0.1)

fig4 = px.box(
    df,
    x="Sex",
    y="Absences",
    color="Sex",
    points="all",
    title="Ausencias por Género",
    labels={"Sex": "Género", "Absences": "Ausencias"},
)

satisfaccion_promedio = (
    df.groupby("RecruitmentSource")["EmpSatisfaction"].mean().reset_index()
)
fig5 = px.bar(
    satisfaccion_promedio,
    x="RecruitmentSource",
    y="EmpSatisfaction",
    color="EmpSatisfaction",
    color_continuous_scale="Blues",
    title="Satisfacción por Fuente de Reclutamiento",
    labels={"RecruitmentSource": "Fuente", "EmpSatisfaction": "Satisfacción"},
)
fig5.update_layout(xaxis_tickangle=-45)

fig6 = px.histogram(
    df,
    x="Salary",
    nbins=30,
    title="Distribución de Salarios",
    labels={"Salary": "Salario"},
)
fig6.update_layout(bargap=0.1)

fig7 = px.pie(
    df,
    names="PerformanceScore",
    title="Puntajes de Desempeño",
    color="PerformanceScore",
    hole=0.3,
)
fig7.update_traces(
    textinfo="percent+label", pull=[0.05] * df["PerformanceScore"].nunique()
)

despedidos = df[df["Termd"] == 1]
despedidos_por_departamento = despedidos["Department"].value_counts().reset_index()
despedidos_por_departamento.columns = ["Department", "NumDespedidos"]
fig8 = px.bar(
    despedidos_por_departamento,
    x="Department",
    y="NumDespedidos",
    color="NumDespedidos",
    color_continuous_scale="Reds",
    title="Despidos por Departamento",
    labels={"Department": "Departamento", "NumDespedidos": "Despedidos"},
)
fig8.update_layout(xaxis_tickangle=-45)

df["DateofHire"] = pd.to_datetime(df["DateofHire"])
df["Antiguedad_Anios"] = (today - df["DateofHire"]).dt.days / 365
fig9 = px.scatter(
    df,
    x="Antiguedad_Anios",
    y="Salary",
    trendline="ols",
    labels={"Antiguedad_Anios": "Antigüedad (Años)", "Salary": "Salario"},
    title="Antigüedad vs Salario",
)

fig10 = px.histogram(
    df,
    x="Position",
    color="Sex",
    barmode="group",
    title="Puestos por Género",
    labels={"Position": "Puesto", "Sex": "Género"},
)
fig10.update_layout(xaxis_tickangle=-45)

# App
app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Dashboard de HRDataset", className="titulo"),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Gráfica 1: Edad vs Salario"),
                        dcc.Graph(figure=fig1, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica1"]),
                        html.H2("Gráfica 2: Salarios por Departamento"),
                        dcc.Graph(figure=fig2, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica2"]),
                    ],
                    className="graph-section",
                ),
                html.Div(
                    [
                        html.H2("Gráfica 3: Distribución de Edades"),
                        dcc.Graph(figure=fig3, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica3"]),
                        html.H2("Gráfica 4: Ausencias por Género"),
                        dcc.Graph(figure=fig4, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica4"]),
                    ],
                    className="graph-section",
                ),
            ],
            className="flex-container",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Gráfica 5: Satisfacción por Fuente"),
                        dcc.Graph(figure=fig5, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica5"]),
                        html.H2("Gráfica 6: Distribución de Salarios"),
                        dcc.Graph(figure=fig6, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica6"]),
                    ],
                    className="graph-section",
                ),
                html.Div(
                    [
                        html.H2("Gráfica 7: Puntajes de Desempeño"),
                        dcc.Graph(figure=fig7, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica7"]),
                        html.H2("Gráfica 8: Despidos por Departamento"),
                        dcc.Graph(figure=fig8, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica8"]),
                    ],
                    className="graph-section",
                ),
            ],
            className="flex-container",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Gráfica 9: Antigüedad vs Salario"),
                        dcc.Graph(figure=fig9, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica9"]),
                    ],
                    className="graph-section",
                ),
                html.Div(
                    [
                        html.H2("Gráfica 10: Puestos por Género"),
                        dcc.Graph(figure=fig10, className="dash-graph"),
                        dcc.Markdown(markdown_texts["grafica10"]),
                    ],
                    className="graph-section",
                ),
            ],
            className="flex-container",
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
