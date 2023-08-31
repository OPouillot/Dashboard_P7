"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import requests
from PIL import Image

# Initialisation de la configuration de la page
st.set_page_config(
    page_title="Prêt à Dépenser - Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def submission():
    st.session_state.form_stat = True

def get_customer(id: int):
    """ Appel de l'API pour récupérer les informations et prédictions d'un client par son id """
    url = f"http://127.0.0.1:8000/customer/?id={id}"
    response = requests.get(url)
    return response


def get_group(target: int, arr_features: list[str]):
    """ Appel de l'API pour récupérer les features données en entrée pour 1500 clients aléatoire de chaque groupe de prédiction
    (3000 clients au total) """
    str_features = ""
    for feature in arr_features:
        str_features = str_features + f"&arr_features={feature}"
    url = f"http://127.0.0.1:8000/group/?{str_features}"
    response = requests.get(url)
    return response


def extract_info(sub_dict):
    """ Extrait la dernière partie du nom après "_" pour des features OneHotEncoder """
    for key in sub_dict:
        if sub_dict[key] == 1:
            return key.split("_")[-1]
    return None

def main():

    if 'form_stat' not in st.session_state:
        st.session_state.form_stat = False

    image = Image.open('pad.png')
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image(image)
        
    st.title("Dashboard client")

    # Formulaire simple pour récupération id client
    with st.form("custom_infos"):
        col1, col2 = st.columns(2)
        with col1:
            client_val = st.number_input(label="Numéro client", value=0, format='%d')
        with col2:
            st.write("")
            st.write("")
            st.form_submit_button("Charger données", on_click=submission())

    tab1, tab2, tab3 = st.tabs(["Informations prêt", "Informations Client", "Ensemble Clients"])

    # Si formulaire envoyé
    if st.session_state.form_stat:
        # Récupération des infos clients
        response = get_customer(client_val)

        if response.status_code == 200:
            prediction = response.json()['prediction']
            proba = {"labels": ["Solvable", "A risque"],
                    "values": response.json()['probability']}
            infos = response.json()['infos'] 

            proba_df = pd.DataFrame(proba)
            chart_proba = px.pie(proba_df,
                                 names="labels",
                                 values="values",
                                 hole=.3,
                                 color_discrete_sequence=["blue", "orange"],
                                 category_orders={"labels": ["Solvable", "A risque"]})

            mobile = ":heavy_check_mark:" if infos["FLAG_MOBIL"] == 1 or infos["FLAG_PHONE"] == 1 else ":x:"
            email = ":heavy_check_mark:" if infos["FLAG_EMAIL"] == 1 else ":x:"
            income = infos["AMT_INCOME_TOTAL"]
            childs = infos["CNT_CHILDREN"] 
            age = abs(infos["DAYS_BIRTH"]) / 365
            family_status = extract_info({key: value for key, value in infos.items() if "NAME_FAMILY_STATUS_" in key})
            work_org = extract_info({key: value for key, value in infos.items() if "ORGANIZATION_TYPE_" in key})
            work_years = abs(infos["DAYS_EMPLOYED"]) / 365

            # INFORMATIONS PRET
            with tab1:
                if prediction == 0:
                    st.markdown("Le client est considéré :blue[**fiable**].")
                else:
                    st.write("Le client est considéré :orange[**à risque**].")
                    
                st.subheader("Probabilité de remboursement du client :")
                col1, col2, col3, col4, col5= st.columns([1, 1, 2, 1, 1])
                with col3:
                    st.plotly_chart(chart_proba, use_container_width=True)
                    
            # INFORMATIONS CLIENT
            with tab2:
                st.write("Age : " + str(int(age)) + " ans")
                st.write("Numéro de téléphone " + mobile)
                st.write("Email " + email)
                st.write("Statut Familiale : " + family_status)
                st.write("Nombre d'enfants : " + str(int(childs)))
                st.write("Secteur d'activité : " + work_org)
                st.write("Années travaillées : " +  str(int(work_years)))
                st.write("Revenu : " + str(int(income)) +" €/an")

            # ENSEMBLE CLIENTS
            with tab3:
                # Récupération des 3000 clients échantillons
                group = get_group(0, ["DAYS_BIRTH", "DAYS_EMPLOYED", "AMT_INCOME_TOTAL", "y_pred"])

                if group.status_code == 200:
                    customers = pd.DataFrame(group.json())

                    # Conversion jours passés en années
                    customers['AGE'] = customers['DAYS_BIRTH'].abs() // 365
                    customers['WORK_YEARS'] = customers['DAYS_EMPLOYED'].abs() // 365
                    
                    feature = st.selectbox('Element à comparer', ('AGE', 'WORK_YEARS', 'AMT_INCOME_TOTAL'))
                    
                    # Mise en forme des données
                    data_chart = [customers[feature].loc[customers["y_pred"]==0], customers[feature].loc[customers["y_pred"]==1]]
                    group_labels = ['Solvable', 'A risque']

                    # Définition du nombre de bins en fonction du nombre de valeurs uniques
                    unique_values = len(customers[feature].unique())
                    bin_count = unique_values*100 if unique_values > 100 else 1

                    # Création du displot avec bin_size adaptatif
                    chart = ff.create_distplot(data_chart,
                                               group_labels,
                                               bin_size=bin_count)
                    chart.update_layout(title=f'Distribution des clients par "{feature}"',
                                        xaxis_title=feature, yaxis_title='Nombre de personnes')

                    st.write(f"Echantillon équilibré de {len(customers)} clients")
                    st.plotly_chart(chart, use_container_width=True)

                else:
                    st.warning(" Un problème est survenu !\n\nCode Erreur : "+ str(group.status_code), icon="🤖")
        else:
            st.warning(" Un problème est survenu !\n\nCode Erreur : "+ str(response.status_code), icon="🤖")


if __name__ == '__main__':
    main()
