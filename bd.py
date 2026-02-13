import os
from dotenv import load_dotenv

# Charge le fichier .env
load_dotenv()

# Récupère les variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

import mysql.connector

def connexion_db():
    try:
        connexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connexion
    except mysql.connector.Error as err:
        print("Erreur de connexion MySQL :", err)
        return None
