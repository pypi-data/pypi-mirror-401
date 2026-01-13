"""
Module principal pour l'extraction des données surf
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import os


def extract_surf_data(url, output_path='surf_data.csv'):
    """
    Extrait les données météo surf depuis une URL de surf-report.com
    et sauvegarde le DataFrame dans un fichier CSV.
    
    Parameters
    ----------
    url : str
        URL de la page surf-report.com
        Exemples:
        - https://www.surf-report.com/meteo-surf/lacanau-s1043.html
        - https://www.surf-report.com/meteo-surf/carcans-plage-s1013.html
        - https://www.surf-report.com/meteo-surf/moliets-plage-centrale-s102799.html
    
    output_path : str, optional
        Chemin complet où sauvegarder le fichier CSV (défaut: 'surf_data.csv')
        Exemples:
        - 'data/lacanau.csv'
        - 'C:/Users/nom/Documents/surf_data.csv'
        - '/home/user/data/surf.csv'
    
    Returns
    -------
    pandas.DataFrame
        DataFrame contenant les colonnes: day, hour, waves_size, wind_speed, wind_direction
    
    Raises
    ------
    ValueError
        Si l'URL n'est pas valide
    Exception
        Si aucune donnée n'a pu être extraite
    
    Examples
    --------
    >>> import surf_scrap
    >>> df = surf_scrap.extract_surf_data(
    ...     'https://www.surf-report.com/meteo-surf/lacanau-s1043.html',
    ...     'data/lacanau.csv'
    ... )
    >>> print(df.head())
    """
    
    # Validation de l'URL
    if not url.startswith('https://www.surf-report.com/meteo-surf/'):
        raise ValueError("URL invalide. Doit commencer par 'https://www.surf-report.com/meteo-surf/'")
    
    # Configuration des headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"🌊 Récupération des données depuis {url}...")
    
    # Récupération de la page web
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erreur lors de la récupération de la page: {e}")
    
    # Parser le HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    script_content = response.text
    
    # Pattern pour extraire les données forecast du code source
    pattern = r'\["(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"\]=>[\s\S]*?object\(stdClass\)#\d+ \(\d+\) \{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
    matches = re.finditer(pattern, script_content)
    
    data = []
    
    # Fonction pour extraire un champ spécifique
    def extract_field(field_name, text):
        """Extrait une valeur d'un champ dans le bloc forecast"""
        pattern = rf'\["{field_name}"\]=>\s*string\(\d+\)\s*"([^"]*)"'
        m = re.search(pattern, text)
        return m.group(1) if m else None
    
    # Fonction pour convertir les degrés en code de direction
    def degres_vers_code_direction(degres_str):
        """Convertit les degrés (0-360) en code de direction (N, S, E, O, etc.)"""
        if not degres_str:
            return "N/A"
        try:
            degres = float(degres_str)
            # 16 directions cardinales
            directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                         'S', 'SSO', 'SO', 'OSO', 'O', 'ONO', 'NO', 'NNO']
            index = round(degres / 22.5) % 16
            return directions[index]
        except:
            return "N/A"
    
    # Dictionnaire de traduction pour les jours
    jours_fr = {
        'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'Dimanche'
    }
    
    # Dictionnaire de traduction pour les mois
    mois_fr = {
        'January': 'Janvier', 'February': 'Février', 'March': 'Mars', 'April': 'Avril',
        'May': 'Mai', 'June': 'Juin', 'July': 'Juillet', 'August': 'Août',
        'September': 'Septembre', 'October': 'Octobre', 'November': 'Novembre', 'December': 'Décembre'
    }
    
    # Extraction des données pour chaque horaire
    for match in matches:
        try:
            date_time_str = match.group(1)
            forecast_block = match.group(2)
            
            # Parser la date et l'heure
            date_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            
            # Formater la date en français
            jour_en = date_obj.strftime('%A')
            mois_en = date_obj.strftime('%B')
            jour_num = date_obj.strftime('%d')
            
            day = f"{jours_fr[jour_en]} {jour_num} {mois_fr[mois_en]}"
            hour = date_obj.strftime('%H:%M')
            
            # Extraire les valeurs météo
            houle = extract_field('houle', forecast_block)
            houle_max = extract_field('houleMax', forecast_block)
            vent_moyen = extract_field('ventMoyen', forecast_block)
            direction_vent_deg = extract_field('directionVent', forecast_block)
            
            # Formater la taille des vagues : "0.8 - 1.3"
            if houle and houle_max:
                waves_size = f"{houle} - {houle_max}"
            else:
                waves_size = "N/A"
            
            # Formater la vitesse du vent : "\n3\n\n"
            if vent_moyen:
                wind_speed = f"\\n{vent_moyen}\\n\\n"
            else:
                wind_speed = "N/A"
            
            # Convertir les degrés en code de direction
            direction_code = degres_vers_code_direction(direction_vent_deg)
            
            # Ajouter les données
            data.append({
                'day': day,
                'hour': hour,
                'waves_size': waves_size,
                'wind_speed': wind_speed,
                'direction_vent_deg': direction_code
            })
            
        except Exception as e:
            # Ignorer les erreurs individuelles et continuer
            continue
    
    # Vérifier qu'on a bien des données
    if len(data) == 0:
        raise Exception("Aucune donnée extraite. Vérifiez l'URL ou la structure de la page.")
    
    # Créer le DataFrame
    df = pd.DataFrame(data)
    
    # Limiter à 7 jours
    dates_uniques = df['day'].unique()
    nb_jours = min(7, len(dates_uniques))
    df_7j = df[df['day'].isin(dates_uniques[:nb_jours])]
    
    # Dictionnaire pour les directions longues
    directions_longues = {
        'N': 'Orientation vent Nord',
        'NNE': 'Orientation vent Nord Est',
        'NE': 'Orientation vent Nord Est',
        'ENE': 'Orientation vent Est Nord Est',
        'E': 'Orientation vent Est',
        'ESE': 'Orientation vent Est Sud Est',
        'SE': 'Orientation vent Sud Est',
        'SSE': 'Orientation vent Sud Est',
        'S': 'Orientation vent Sud',
        'SSO': 'Orientation vent Sud Ouest',
        'SO': 'Orientation vent Sud Ouest',
        'OSO': 'Orientation vent Ouest Sud Ouest',
        'O': 'Orientation vent Ouest',
        'ONO': 'Orientation vent Ouest Nord Ouest',
        'NO': 'Orientation vent Nord Ouest',
        'NNO': 'Orientation vent Nord Ouest',
        'N/A': 'N/A'
    }
    
    # Appliquer le mapping pour wind_direction
    df_7j['wind_direction'] = df_7j['direction_vent_deg'].map(directions_longues)
    
    # Sélectionner et réorganiser les colonnes
    df_7j = df_7j[['day', 'hour', 'waves_size', 'wind_speed', 'wind_direction']]
    
    # Réinitialiser l'index
    df_7j = df_7j.reset_index(drop=True)
    
    # Créer le dossier de destination si nécessaire
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Dossier créé : {output_dir}")
    
    # Sauvegarder le DataFrame en CSV
    df_7j.to_csv(output_path, index=True, encoding='utf-8-sig')
    
    # Afficher les informations
    print(f"✅ Données extraites avec succès !")
    print(f"   - Nombre de prévisions : {len(df_7j)}")
    print(f"   - Nombre de jours : {nb_jours}")
    print(f"💾 Fichier sauvegardé : {output_path}")
    
    return df_7j