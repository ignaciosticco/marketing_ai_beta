'''
Este script le pega a la api de fb, y formatea los datos para que consuma el chatbot.

IMPORTANTE: cambiar el token y el campaing_id segun sea necesario

'''
import requests
import pandas as pd

def bring_fataframe(token, campaing_id, breakdown):

    ''' 
    Le pega a la api de facebook y devuelve los datos pedidos en un dataframe
    '''

    url = "https://graph.facebook.com/v20.0/{}/insights".format(campaing_id)
    params = {

    "date_preset": "this_year",
    "access_token": token,    
    "fields": "campaign_name,impressions,reach,inline_link_clicks,actions,spend",
    "breakdowns": breakdown,
    "limit":"50000000",
    }

    response = requests.get(url, params=params)
    json_data  = response.json()
    data = json_data['data']

    processed_data = []
    # Process each campaign's data
    for campaign in data:
        base_info = {key: campaign[key] for key in campaign if key != 'actions'}
        # Initialize 'onsite_conversion.lead_grouped' to 0
        lead_grouped_value = 0
        if 'actions' in campaign:
            for action in campaign['actions']:
                if action['action_type'] == 'onsite_conversion.lead_grouped':
                    lead_grouped_value = int(action['value'])
        base_info['onsite_conversion.lead_grouped'] = lead_grouped_value
        processed_data.append(base_info)

    df = pd.DataFrame(processed_data)
    return df


def limpia_csv(df):

    # Casteo las columnas
    df['impressions'] = df['impressions'].astype(int)
    df['reach'] = df['reach'].astype(int)
    df['inline_link_clicks'] = df['inline_link_clicks'].astype(float)
    df['spend'] = df['spend'].astype(float)
    df['onsite_conversion.lead_grouped'] = df['onsite_conversion.lead_grouped'].astype(int)

    # Renombro las columnas
    df.rename(columns={'inline_link_clicks':'link_clicks', 'onsite_conversion.lead_grouped':'conversions'}, inplace = True)

    # Elimino las columnas que no necesito
    df.drop(['date_start', 'date_stop', 'reach'], axis=1, inplace = True)

    return df
    
def crea_nuevas_metricas(df):

    # Calculo el ctr y cpc (al enlace) calculado por definicion (a partir de la data agregada)
    df['ctr'] = round((df['link_clicks']/df['impressions'])*100,2)
    df['cost_per_link_click'] = round(df['spend']/df['link_clicks'],2)

    return df



def main():

    # PARAMETERS
    token =  "EAAbcF9JKPTkBO0rcYg2BnS4zRe2ZBwShkuiMqoXKgLRYUZBEeW1QSGfkvInuU8j7rWZBbjr8LVOPo4sT3vPwditm7dC3pXaNtDiZCL7JmaSCchqEJ9NJbPZB2T5lix1nhF5o9sF5zwjQWKTKljBB7oJxwT6UJBmCcZCp71yUfwfhYFL7ykIIO9CvsB35hWXvvkRJlfh1iylrKTC8oZD"
    campaing_id = "120207306882740766"

    ################### Desglose por genero ###################
    breakdown = "gender"
    # Traigo los datos, los limpio y creo nuevas metricas
    df_gender = bring_fataframe(token, campaing_id, breakdown)
    df_gender = limpia_csv(df_gender)
    df_gender = crea_nuevas_metricas(df_gender)

    # Redondeo la columna de gastos
    df_gender['spend'] = df_gender['spend'].round(2)
    # Elimino sexo unknown
    df_gender = df_gender [df_gender['gender']!='unknown']
    # Reorganizo las columnas
    column_order = ['campaign_name', 'gender', 'link_clicks', 'conversions','spend', 'cost_per_link_click', 'ctr', 'impressions']
    df_gender = df_gender.reindex(columns=column_order)
    # Imprimo el dataframe
    df_gender.to_csv('data_gender.txt',sep = ',')


    ################### Desglose por edad ###################
    breakdown = "age"
    # Traigo los datos, los limpio y creo nuevas metricas
    df_age = bring_fataframe(token, campaing_id, breakdown)
    df_age = limpia_csv(df_age)
    df_age = crea_nuevas_metricas(df_age)

    # Redondeo la columna de gastos
    df_age['spend'] = df_age['spend'].round(2)
    # Reorganizo las columnas
    column_order = ['campaign_name', 'age', 'link_clicks', 'conversions','spend', 'cost_per_link_click', 'ctr', 'impressions']
    df_age = df_age.reindex(columns=column_order)
    # Imprimo el dataframe
    df_age.to_csv('data_age.txt',sep = ',')


    ################### Desglose por region ###################
    breakdown = "region"

    # Traigo los datos, los limpio y creo nuevas metricas
    df_region = bring_fataframe(token, campaing_id, breakdown)
    df_region = limpia_csv(df_region)
    df_region = crea_nuevas_metricas(df_region)

    # Redondeo la columna de gastos
    df_region['spend'] = df_region['spend'].round(2)
    # Reorganizo las columnas
    column_order = ['campaign_name', 'region', 'link_clicks', 'conversions','spend', 'cost_per_link_click', 'ctr', 'impressions']
    df_region = df_region.reindex(columns=column_order)
    # Imprimo el dataframe
    df_region.to_csv('data_region.txt',sep = ',')


if __name__ == "__main__":
    main()