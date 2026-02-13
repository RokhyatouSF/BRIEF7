import bcrypt
import re
from bd import connexion_db
from contextlib import closing

# VALIDATION EMAIL
def email_valide(email):
    """
    Vérifie si l'email respecte le format valide
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)

# INSCRIPTION
def inscription(email, mot_de_passe, username=None, role_nom='apprenant', promo_id=None, formation_id=None):
    """
    Inscription d'un utilisateur avec email, mot de passe, username, rôle, promo et formation.
    """
    # Vérifier format email
    if not email_valide(email):
        print("Email invalide")
        return False

    # Connexion à la base
    conn = connexion_db()
    if not conn:
        return False

    try:
        with closing(conn.cursor()) as cursor:

            # Vérifier email unique
            cursor.execute("SELECT id_utilisateur FROM utilisateurs WHERE email=%s", (email,))
            if cursor.fetchone():
                print("Email déjà utilisé.")
                return False

            # Vérifier rôle existant
            cursor.execute("SELECT id_role FROM roles WHERE nom_role=%s", (role_nom,))
            role = cursor.fetchone()
            if not role:
                print("Rôle inexistant")
                return False

            role_id = role[0]

            # Hash du mot de passe
            hash_pw = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt())

            # Insérer l'utilisateur
            if role_nom.lower() == "apprenant":
                cursor.execute("""
                    INSERT INTO utilisateurs(email, username, password_hash, role_id, promo_id, formation_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (email, username, hash_pw, role_id, promo_id, formation_id))
            else:
                cursor.execute("""
                    INSERT INTO utilisateurs(email, username, password_hash, role_id)
                    VALUES (%s, %s, %s, %s)
                """, (email, username, hash_pw, role_id))

            conn.commit()
            print("Inscription réussie ")
            return True

    except Exception as e:
        print("Erreur inscription :", e)
        return False
    finally:
        conn.close()

# CONNEXION
def connexion(email, username, mot_de_passe):
    """
    Connexion avec email + username + mot de passe.
    Retourne un dict avec id et rôle pour la session.
    """
    conn = connexion_db()
    if not conn:
        return None

    try:
        with closing(conn.cursor()) as cursor:
            cursor.execute("""
                SELECT u.id_utilisateur, u.password_hash, r.nom_role
                FROM utilisateurs u
                JOIN roles r ON u.role_id = r.id_role
                WHERE u.email=%s AND u.username=%s
            """, (email, username))

            user = cursor.fetchone()
            if not user:
                return None

            user_id, hash_pw, role = user

            # Vérifier mot de passe
            if isinstance(hash_pw, str):
                hash_pw = hash_pw.encode()
            if not bcrypt.checkpw(mot_de_passe.encode(), hash_pw):
                return None

            return {"id": user_id, "role": role}

    except Exception as e:
        print("Erreur connexion :", e)
        return None
    finally:
        conn.close()

# REINITIALISATION MOT DE PASSE
def reinitialiser_mot_de_passe(email, nouveau_mdp):
    """
    Réinitialiser le mot de passe d'un utilisateur à partir de son email.
    """
    conn = connexion_db()
    if not conn:
        return False

    try:
        with closing(conn.cursor()) as cursor:

            # Vérifier que l'utilisateur existe
            cursor.execute("SELECT id_utilisateur FROM utilisateurs WHERE email=%s", (email,))
            if not cursor.fetchone():
                print("Email non trouvé.")
                return False

            # Hash du nouveau mot de passe
            hash_pw = bcrypt.hashpw(nouveau_mdp.encode(), bcrypt.gensalt())

            cursor.execute("""
                UPDATE utilisateurs
                SET password_hash=%s
                WHERE email=%s
            """, (hash_pw, email))

            conn.commit()
            print("Mot de passe modifié ")
            return True

    except Exception as e:
        print("Erreur reset mot de passe :", e)
        return False
    finally:
        conn.close()
