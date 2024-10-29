
import nltk
from nltk.tokenize import word_tokenize


def extraer_comision(df):
    """
    Separa la columna 'MATERIA' en 'MATERIA' (sin cambios) y 'COMISION' (última palabra del token).

    Args:
        df (pandas.DataFrame): El DataFrame con la columna 'MATERIA'.

    Returns:
        pandas.DataFrame: El DataFrame modificado.
    """

    # Tokenizar la columna 'MATERIA'
    df['tokens'] = df['MATERIA'].apply(word_tokenize)

    # Función para extraer la última palabra del token
    def extraer_ultima_palabra(tokens):
        return tokens[-1] if tokens else None

    # Aplicar la función y crear la columna 'COMISION'
    df['COMISION'] = df['tokens'].apply(extraer_ultima_palabra)
    df.drop('tokens', axis=1, inplace=True)

    return df



















#GEMINI#######



def separar_materia_y_comision(df):
    # Tokenizar las materias
    df['tokens'] = df['MATERIA'].apply(word_tokenize)

    # Función para comparar prefijos y extraer comisión
    def comparar_prefijos(row):
        tokens = row['tokens']
        for index, row_inner in df.iterrows():
            if index != row.name and tokens[:2] == row_inner['tokens'][:2]:
                return ' '.join(tokens[:2]), ' '.join(tokens[2:])
        return ' '.join(tokens), None

    # Aplicar la función y crear las nuevas columnas
    df[['MATERIA', 'COMISION']] = df.apply(comparar_prefijos, axis=1, result_type='expand')
    df.drop('tokens', axis=1, inplace=True)

    return df

# Ejemplo de uso

#df_limpio = separar_materia_y_comision(df_limpio)

#valores_unicos = df_limpio['COMISION'].unique().tolist()

# Imprimir los valores únicos
#print(valores_unicos)

#df_muestra = df_limpio[['MATERIA', 'COMISION']].sample(n=50)

# Imprimir el DataFrame resultante
#print(df_muestra)

