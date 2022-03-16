import pandas as pd
import pymongo
import nltk
import os
import re
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
#Descarga de stopwords actualizadas
nltk.download('stopwords')
#Abrir archivo y guardarlo en variable BUSQUEDA
ubicacion = "C:\meliv2\coleccion_2022\\"      
procesado = "C:/meliv2/procesado/"
procesado_csv = "C:/meliv2/procesado_csv/"
#filtrar texto
for file in os.listdir(ubicacion):    
    with open(os.path.join(ubicacion,file), encoding="utf8") as busqueda, open((procesado+file), "w", encoding='utf-8') as datoprocesado:
        archivo=busqueda.read()       
        #Remover guion_bajo 
        guion_bajo=archivo.replace("_", " ")
        #Remover acentos
        acentos= (unidecode(guion_bajo))
        #Poner en minusculas
        lower_string = acentos.lower()   
        #Quitar numeros
        no_number_string = re.sub(r'\d+','',lower_string)   
        #Quitar signos de puntuacion
        no_punc_string = re.sub(r'[^\w\s]','', no_number_string)
        #Quitar espacios
        no_wspace_string = no_punc_string.strip()
        no_wspace_string.split(';')
        #Se tokeniza por palabra
        word_tokenize(no_wspace_string)
        stop_words = set(stopwords.words('spanish')) 
        word_tokens = word_tokenize(no_wspace_string) 
        #Se quitan STOPWORDS
        filtered_sentence = [w for w in word_tokens if not w in stop_words] 
        filtered_sentence = [] 
        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.append(w)
        final=(filtered_sentence)
        datoprocesado.write('\n'.join(final))               
    datoprocesado.close
    data= {'Archivo': file, "Palabra": final}  
    df=pd.DataFrame(data)
    #df['archivo'] = file
    
    #convertir texto en csv
    csv_data=df.to_csv(os.path.join(procesado_csv,file.rsplit('.',1)[0]+'.csv'), encoding='utf-8')
    
#print(df)
#enviar a mongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
for filename in os.listdir(procesado_csv):
    mydb= myclient["MELIDB"]
    os.path.splitext(procesado_csv)[0]
    mycol=mydb["Coleccion_2022"]
    PATH = (procesado_csv) + (filename)
    #data = pd.read_csv('temp.csv', index_col=[0])
    data = pd.read_csv((PATH), index_col=[0])
    data_json = json.loads(data.to_json(orient='records'))
    mycol.insert_many(data_json)
