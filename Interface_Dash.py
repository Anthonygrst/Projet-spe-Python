import dash
import dash_html_components as html
import pandas as pd

#fonction qui permet de generer sur dash une dataframe

def generate_table(df, max_rows=20):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ])

df = pd.read_csv('corpus.csv', on_bad_lines='skip')

app = dash.Dash()
app.title = "Documents Reddit Arxiv"
app.layout = html.Div(children=[
    html.H1(children='Voici les données de notre Corpus sur les articles Reddit et Arxiv', style={"fontSize": "48px", "color": "black", "text-align": "center"}),

    html.Br(),
    generate_table(df),
    html.Div([
        
        
        html.Div(id='container-button-basic',)     
        ]
        
        ),
        
        html.Div('M1 Informatique Spécialité Python Celia Maurin et Anthony Graissot',style={"font-weight":"bold","position":'relative', "bottom":0, 
                                                                                "left":-400, "right":0, "padding": "1rem", "fontSize": "17px", 
                                                                                "color": "black", "text-align": "center"})
    
    ], style={'padding': '2rem', 'flex': 1},
    )



             
             
             
if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
