Proyecto Individual Parte 1 - Palacio Alexis (PI_Palacio)

Este repositorio contiene el desarrollo de un proyecto que abarca tareas de ETL, Análisis Exploratorio de Datos (EDA), y Machine Learning (ML). El proyecto se dividió en partes, y cada una de ellas se abordó en notebooks independientes.

Base de datos:
    User Reviews
    Steam Games
    User Items

Notebooks:
    
    PIparte1.ipynb:
        EDA (Análisis Exploratorio de Datos):
            En esta primera etapa, descargamos la información en formato JSON. Sin embargo, los archivos se encontraban con datos incompletos o desordenados. En este notebook, creamos una función para procesar los datos fila por fila. Este proceso nos permitió visualizar la información y realizar un análisis general para comprender los datos y su contenido. Cada función que creamos se formuló como una pregunta, y buscamos las respuestas dentro de las bases de datos.
    
    gamestratamiento.ipynb:
        EDA:
            En este notebook, descargamos la base de datos, realizamos correcciones necesarias y seleccionamos únicamente las columnas de interés.
    
    items.ipynb:
        EDA:
            Aquí identificamos una columna anidada que nos llevó a crear una función para organizar adecuadamente la base de datos.
    
    manipulacionreviews.ipynb:
        EDA:
            En este notebook nos encontramos con otra columna anidada. Gracias a la función previamente creada, pudimos ordenar la base de datos de manera efectiva. Además, se nos solicitó generar una nueva columna que involucra un análisis de sentimientos. Este análisis se llevó a cabo en la notebook "sentimentanalysis.ipynb", donde probamos tres modelos y seleccionamos el que mejor métricas proporcionó.
   
    PlaytimeGenre1.ipynb:
        EDA:
            Este notebook involucra la creación de una función para la que identificamos las columnas necesarias. Luego, realizamos un análisis más profundo de esas columnas para limpiar y transformar los datos, asegurando así una mayor calidad.
    
    def_UserForGenre2.ipynb:
        EDA:
            En este caso, seguimos una metodología similar a la etapa anterior. Sin embargo, nos encontramos con valores atípicos en la columna "Playtime_forever", expresados originalmente en minutos. Para cumplir con los requisitos de la función, los convertimos a horas. Además, implementamos el método del rango intercuartílico para abordar el problema de los valores atípicos.
    def_UsersRecommend3.ipynb:
       
        EDA:
            En esta notebook repetimos el proceso de selección de columnas y realizamos un análisis más detallado para depurar la base de datos.
    
    def_UsersNotRecommend4.ipynb:
        EDA:
            Aplicamos la misma metodología que en el paso anterior, con la salvedad de que tomamos los datos opuestos de algunas columnas, ya que esta función es prácticamente inversa a la anterior.
    
    def_sentiment_analysis5.ipynb:
            EDA:
            Seguimos la misma metodología, ya que teníamos la base de datos bien organizada. Utilizamos el análisis de sentimientos previamente creado en "manipulacionreviews.ipynb" para crear esta función.
    
    ml_sin_genres.ipynb:
        EDA:
            En esta etapa, decidimos crear una función de recomendación de usuarios. Seleccionamos las columnas necesarias para comprender los datos y elaborar la función de manera adecuada. La idea original era considerar los géneros de los juegos (como se hizo en "ml_con_genres.ipynb"), pero debido a limitaciones de memoria y practicidad, decidimos no incluirlos. A pesar de ello, logramos desarrollar un modelo con buenos resultados.

Enlaces:
        
        YouTube: https://youtu.be/mtsgqxSOVO0
        
        render: https://pi-palacioalexis.onrender.com/docs
        
        Gihub: https://github.com/soyalexis/pi_palacioalexis.git
