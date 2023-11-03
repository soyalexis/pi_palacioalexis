from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
#http://127.0.0.1:8000
app = FastAPI()


df1 = pd.read_parquet("df_1redu.parquet")
@app.get("/PlayTimeGenre/")
async def PlayTimeGenre(genero: str):
        # Filtra las filas donde el género coincide
        df_filtered = df1[df1['genres'] == genero]

        if df_filtered.empty:
         return f"No se encontraron datos para el género '{genero}', ingresar genero en miniscula ej: action"

        # Encuentra el año con más horas jugadas para ese género
        year_with_most_playtime = int(df_filtered.groupby('Año')['playtime_forever'].sum().idxmax())


        return {f"Año de lanzamiento con más horas jugadas para el género '{genero}'": year_with_most_playtime}
    
    
df2 = pd.read_parquet('df_2reducidov2.parquet')
@app.get("/UserForGenre")
def UserForGenre(genero:str):
    # Filtrar el DataFrame por genero
    df_genre = df2[df2['genres'] == genero]

    if df_genre.empty:
        return {"Usuario con más horas jugadas para " + genero: "Ninguno, ingresar genero en miniscula ej: action", "Horas jugadas": []}

    df_genre['Año'] = pd.to_datetime(df_genre['Año'], format='%Y')
    # Encontrar el usuario con más horas jugadas para ese género
    max_playtime_user = df_genre.loc[df_genre['playtime_hours'].idxmax()]['user_id']

    # Calcular la acumulación de horas jugadas por año
    playtime_by_year = df_genre.groupby(df_genre['Año'].dt.year)['playtime_hours'].sum().reset_index()

    # Crear una lista de diccionarios para la acumulación de horas por año
    playtime_list = [{"Año": year, "Horas": hours} for year, hours in zip(playtime_by_year['Año'], playtime_by_year['playtime_hours'])]

    return {"Usuario con más horas jugadas para " + genero: max_playtime_user, "Horas jugadas": playtime_list}


df3 = pd.read_parquet('df_3reducido.parquet')
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


df4 = pd.read_parquet('df_4reducido.parquet')
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



df5 = pd.read_parquet('df_5sinreduccion.parquet')
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

df_reducido_num = pd.read_parquet('df_numerico_recomendacion_reducido.parquet')
df_reducido_user = pd.read_parquet('df_user_recomendacion_reducido.parquet')
@app.post("/recomendacion_usuario")
def recomendacion_usuario(user_id):
    user_similarity = cosine_similarity(df_reducido_num)
    user_similarity_df = pd.DataFrame(user_similarity, index=df_reducido_user['user_id'], columns=df_reducido_user['user_id'])
    if user_id not in user_similarity_df.index:
        return "Usuario no encontrado, ingresar algundos de los siguientes: 76561198045476116,ChipBae,mwanan,topkekhehe,dynamoburrito,76561198094044284"

    # Obtiene la fila de similitud del usuario
    user_similarity = user_similarity_df.loc[user_id]

    # Ordena los usuarios por similitud en orden descendente
    similar_users = user_similarity.sort_values(ascending=False)[1:]  # Excluye al propio usuario

    # Filtra los juegos jugados por usuarios similares
    user_data = df_reducido_user[df_reducido_user['user_id'] == user_id]
    games_played = user_data['item_name'].unique()

    # Genera una lista de juegos recomendados
    recommendations = []
    unique_recommendations = set()  # Conjunto para asegurar recomendaciones únicas

    for similar_user_id, similarity_score in similar_users.items():
        similar_user_data = df_reducido_user[df_reducido_user['user_id'] == similar_user_id]
        for game in similar_user_data['item_name']:
            if game not in games_played and game not in unique_recommendations:
                recommendations.append(game)
                unique_recommendations.add(game)
            if len(recommendations) >= 10:  # Recolecta 10 recomendaciones, ajusta según sea necesario
                break

    return recommendations[:5]  # Devuelve las primeras 5 recomendaciones únicas