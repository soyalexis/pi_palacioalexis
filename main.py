from fastapi import FastAPI
import pandas as pd
import fastparquet
import numpy as np
#http://127.0.0.1:8000
app = FastAPI()


@app.get("/")
async def ruta_prueba():
    return "Hola"


df1 = pd.read_parquet('df_primerafuncionv4.parquet')
@app.get("/PlayTimeGenre/")
async def PlayTimeGenre(genero: str):
        # Filtra las filas donde el género coincide
        df_filtered = df1[df1['genres'] == genero]

        if df_filtered.empty:
         return f"No se encontraron datos para el género '{genero}'"

        # Encuentra el año con más horas jugadas para ese género
        year_with_most_playtime = int(df_filtered.groupby('Año')['playtime_forever'].sum().idxmax())


        return {f"Año de lanzamiento con más horas jugadas para el género '{genero}'": year_with_most_playtime}
    
    
df2 = pd.read_parquet('C:\\Users\W10\Desktop\\Entorno virtual 7\\data\\df_segundafuncionv2.parquet')
@app.get("/UserForGenre")
def UserForGenre(genero:str):
    # Filtrar el DataFrame por genero
    df_genre = df2[df2['genres'] == genero]

    if df_genre.empty:
        return {"Usuario con más horas jugadas para " + genero: "Ninguno", "Horas jugadas": []}

    df_genre['Año'] = pd.to_datetime(df_genre['Año'], format='%Y')
    # Encontrar el usuario con más horas jugadas para ese género
    max_playtime_user = df_genre.loc[df_genre['playtime_hours'].idxmax()]['user_id']

    # Calcular la acumulación de horas jugadas por año
    playtime_by_year = df_genre.groupby(df_genre['Año'].dt.year)['playtime_hours'].sum().reset_index()

    # Crear una lista de diccionarios para la acumulación de horas por año
    playtime_list = [{"Año": year, "Horas": hours} for year, hours in zip(playtime_by_year['Año'], playtime_by_year['playtime_hours'])]

    return {"Usuario con más horas jugadas para " + genero: max_playtime_user, "Horas jugadas": playtime_list}


df3 = pd.read_parquet('C:\\Users\W10\Desktop\\Entorno virtual 7\\Data\\df_tercerafuncionv1.parquet')
@app.get("/UsersRecommend")
def UsersRecommend(year:int):
    # Filtra el DataFrame para el año especificado y donde 'recommend' es True
    juegos_recomendados = df3[(df3['Fecha_posteo'] == year) & (df3['recommend'] == True)]

    # Verifica si no hay datos para ese año
    if juegos_recomendados.empty:
        return ("No hay datos para ese año", year)

    # Agrupa por el nombre del juego y cuenta las recomendaciones
    juegos_agrupados = juegos_recomendados['item_name'].value_counts().reset_index()
    juegos_agrupados.columns = ['Juego', 'Recomendaciones']

    # Ordena los juegos por número de recomendaciones de mayor a menor
    juegos_ordenados = juegos_agrupados.sort_values(by='Recomendaciones', ascending=False)

    # Toma los 3 juegos con más recomendaciones
    top_3_juegos = juegos_ordenados.head(3)

    # Formatea los resultados en la estructura deseada
    resultado = []
    for i, row in top_3_juegos.iterrows():
        resultado.append({"Puesto " + str(i + 1): row['Juego']})

    return resultado


df4 = pd.read_parquet('C:\\Users\W10\Desktop\\Entorno virtual 7\\Data\\df_cuartafuncionv1.parquet')
@app.get("/UsersNotRecommend")
def UsersNotRecommend(year:int):
    # Filtra el DataFrame para el año especificado y donde 'recommend' es True
    juegos_recomendados = df4[(df4['Fecha_posteo'] == year) & (df4['recommend'] == False)]

    # Verifica si no hay datos para ese año
    if juegos_recomendados.empty:
        return ("No hay datos para ese año", year)

    # Agrupa por el nombre del juego y cuenta las recomendaciones
    juegos_agrupados = juegos_recomendados['item_name'].value_counts().reset_index()
    juegos_agrupados.columns = ['Juego', 'Recomendaciones']

    # Ordena los juegos por número de recomendaciones de mayor a menor
    juegos_ordenados = juegos_agrupados.sort_values(by='Recomendaciones', ascending=False)

    # Toma los 3 juegos con más recomendaciones
    top_3_juegos = juegos_ordenados.head(3)

    # Formatea los resultados en la estructura deseada
    resultado = []
    for i, row in top_3_juegos.iterrows():
        resultado.append({"Puesto " + str(i + 1): row['Juego']})

    return resultado



df5 = pd.read_parquet('C:\\Users\W10\Desktop\\Entorno virtual 7\\data\\df_quintafuncionv1.parquet')
@app.get("/sentiment_analysis")
def sentiment_analysis(año: int):
    # Filtra el DataFrame para el año especificado
    df_filtrado = df5[df5['release_year'] == año]

    # Cuenta la cantidad de registros para cada categoría de sentimiento
    conteo_sentimiento = df_filtrado['sentiment_analysis'].value_counts()

    # Convierte los valores de tipo numpy.int64 a int
    resultado = {
        "Negative": conteo_sentimiento.get(0, 0).item(),
        "Neutral": conteo_sentimiento.get(1, 0).item(),
        "Positive": conteo_sentimiento.get(2, 0).item()
    }

    return resultado
