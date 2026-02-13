from contextlib import closing
from datetime import datetime
from auth import connexion, inscription, reinitialiser_mot_de_passe
from bd import connexion_db

# OUTILS SAISIE
def saisir_texte(message):
    while True:
        valeur = input(message).strip()
        if valeur != "":
            return valeur
        print("Champ obligatoire.")

def saisir_entier(message):
    while True:
        try:
            return int(input(message))
        except:
            print("Veuillez entrer un nombre valide.")

def saisir_date(message):
    while True:
        try:
            return datetime.strptime(input(message), "%Y-%m-%d %H:%M")
        except:
            print("Format attendu : AAAA-MM-JJ HH:MM")

# CALCUL URGENCE
def calculer_niveau_urgence(date_max):
    difference = (date_max - datetime.now()).total_seconds() / 3600

    if difference < 72:
        return "Très urgent"
    elif difference < 168:
        return "Urgent"
    elif difference < 720:
        return "Moins urgent"
    else:
        return "Peut attendre"

# CREER TICKET (APPRENANT)
def creer_ticket(utilisateur):
    print("\n CREATION TICKET ")

    titre = saisir_texte("Titre : ")
    description = saisir_texte("Description : ")
    date_max = saisir_date("Date limite (AAAA-MM-JJ HH:MM) : ")

    connexion = connexion_db()

    with closing(connexion.cursor()) as curseur:

        curseur.execute("""
        SELECT id_role, nom_role FROM roles
        WHERE nom_role != 'apprenant'
        """)
        roles = curseur.fetchall()

        print("\nChoisir le rôle qui doit traiter votre demande :")
        for role in roles:
            print(f"{role[0]} - {role[1]}")

        role_id = saisir_entier("ID du rôle : ")

        curseur.execute("""
        SELECT id_utilisateur, username
        FROM utilisateurs
        WHERE role_id=%s
        """, (role_id,))
        utilisateurs = curseur.fetchall()

        print("\nChoisir la personne qui va traiter :")
        for u in utilisateurs:
            print(f"{u[0]} - {u[1]}")

        assigne_id = saisir_entier("ID utilisateur : ")

        curseur.execute("""
        INSERT INTO tickets
        (titre, description, dateheuremax_traitement, createur_id, assigne_id)
        VALUES (%s,%s,%s,%s,%s)
        """, (titre, description, date_max, utilisateur["id"], assigne_id))

        ticket_id = curseur.lastrowid

        curseur.execute("""
        INSERT INTO demandes(ticket_id, statut, createur_id, assigne_id)
        VALUES(%s,'en_attente',%s,%s)
        """, (ticket_id, utilisateur["id"], assigne_id))

        connexion.commit()

    connexion.close()

    niveau = calculer_niveau_urgence(date_max)
    print(f"\nTicket créé avec succès. Niveau d'urgence : {niveau}")

# MES TICKETS
def afficher_mes_tickets(utilisateur):
    connexion = connexion_db()

    with closing(connexion.cursor()) as curseur:
        curseur.execute("""
        SELECT t.id_ticket, t.titre, t.description,
               t.dateheuremax_traitement,
               d.statut, u.username
        FROM tickets t
        JOIN demandes d ON d.ticket_id=t.id_ticket
        LEFT JOIN utilisateurs u ON u.id_utilisateur=t.assigne_id
        WHERE t.createur_id=%s
        """, (utilisateur["id"],))

        lignes = curseur.fetchall()

        print("\n MES TICKETS ")

        for ligne in lignes:
            urgence = calculer_niveau_urgence(ligne[3])

            print("\n--------------------")
            print("ID :", ligne[0])
            print("Titre :", ligne[1])
            print("Description :", ligne[2])
            print("Assigné à :", ligne[5])
            print("Statut :", ligne[4])
            print("Urgence :", urgence)

    connexion.close()

# TICKETS ASSIGNES A MOI
def afficher_tickets_assignes(utilisateur):
    connexion = connexion_db()

    with closing(connexion.cursor()) as curseur:
        curseur.execute("""
        SELECT t.id_ticket, t.titre, t.description,
               u.username, u.email,
               t.dateheuremax_traitement,
               d.statut
        FROM tickets t
        JOIN utilisateurs u ON u.id_utilisateur=t.createur_id
        JOIN demandes d ON d.ticket_id=t.id_ticket
        WHERE t.assigne_id=%s
        """, (utilisateur["id"],))

        lignes = curseur.fetchall()

        print("\n TICKETS QUI VOUS SONT ASSIGNES ")

        for ligne in lignes:
            urgence = calculer_niveau_urgence(ligne[5])

            print("\n--------------------")
            print("ID :", ligne[0])
            print("Titre :", ligne[1])
            print("Apprenant :", ligne[3])
            print("Email :", ligne[4])
            print("Description :", ligne[2])
            print("Statut :", ligne[6])
            print("Urgence :", urgence)

    connexion.close()

# AJOUT PROMO
def ajouter_promo():
    nom = saisir_texte("Nom promo : ")
    connexion = connexion_db()

    with closing(connexion.cursor()) as curseur:
        curseur.execute("INSERT INTO promos(nom_promo) VALUES(%s)", (nom,))
        connexion.commit()

    connexion.close()
    print("Promo ajoutée.")

# AJOUT FORMATION
def ajouter_formation():
    nom = saisir_texte("Nom formation : ")
    connexion = connexion_db()

    with closing(connexion.cursor()) as curseur:
        curseur.execute("INSERT INTO formations(nom_formation) VALUES(%s)", (nom,))
        connexion.commit()

    connexion.close()
    print("Formation ajoutée.")

# ASSIGNER TICKET
def assigner_ticket_admin():
    connexion = connexion_db()

    with closing(connexion.cursor()) as curseur:

        curseur.execute("SELECT id_ticket,titre FROM tickets")
        tickets = curseur.fetchall()

        print("\nTickets :")
        for t in tickets:
            print(f"{t[0]} - {t[1]}")

        ticket_id = saisir_entier("ID ticket : ")

        curseur.execute("""
        SELECT id_role, nom_role FROM roles
        WHERE nom_role!='apprenant'
        """)
        roles = curseur.fetchall()

        for r in roles:
            print(f"{r[0]} - {r[1]}")

        role_id = saisir_entier("ID rôle : ")

        curseur.execute("""
        SELECT id_utilisateur, username
        FROM utilisateurs WHERE role_id=%s
        """, (role_id,))
        users = curseur.fetchall()

        for u in users:
            print(f"{u[0]} - {u[1]}")

        assigne_id = saisir_entier("ID utilisateur : ")

        curseur.execute("""
        UPDATE tickets SET assigne_id=%s
        WHERE id_ticket=%s
        """, (assigne_id, ticket_id))

        connexion.commit()

    connexion.close()
    print("Ticket assigné.")

def voir_tous_les_tickets():
    connexion = connexion_db()

    with closing(connexion.cursor()) as curseur:
        curseur.execute("""
        SELECT t.id_ticket, t.titre, u_createur.username AS createur,
               u_assigne.username AS assigne, d.statut, t.dateheure_creation
        FROM tickets t
        JOIN utilisateurs u_createur ON u_createur.id_utilisateur = t.createur_id
        LEFT JOIN utilisateurs u_assigne ON u_assigne.id_utilisateur = t.assigne_id
        JOIN demandes d ON d.ticket_id = t.id_ticket
        ORDER BY t.dateheure_creation DESC
        """)

        lignes = curseur.fetchall()

        print("\n TICKETS ")
        for l in lignes:
            print("\n--------------------")
            print("ID Ticket :", l[0])
            print("Titre :", l[1])
            print("Créé par :", l[2])
            print("Assigné à :", l[3] if l[3] else "Non assigné")
            print("Statut :", l[4])
            print("Date création :", l[5])
            print("--------------------")

    connexion.close()

# LOGS
def afficher_logs():
    connexion = connexion_db()

    with closing(connexion.cursor()) as curseur:
        curseur.execute("""
        SELECT l.dateheure,u.username,l.action_descr
        FROM logs_actions l
        JOIN utilisateurs u ON u.id_utilisateur=l.user_id
        ORDER BY l.dateheure DESC
        """)
        lignes = curseur.fetchall()

        print("\n HISTORIQUE ")
        for l in lignes:
            print(l[0], "|", l[1], "|", l[2])

    connexion.close()

# MENU
def menu(utilisateur):
    while True:

        print("\n MENU ")

        if utilisateur["role"] == "apprenant":
            print("1 Créer ticket")
            print("2 Mes tickets")
            print("0 Déconnexion")

            choix = input("Choix : ")

            if choix == "1":
                creer_ticket(utilisateur)
            elif choix == "2":
                afficher_mes_tickets(utilisateur)
            elif choix == "0":
                break

        else:
            print("1 Voir tickets assignés")
            print("3 Ajouter promo")
            print("4 Ajouter formation")
            print("5 Assigner ticket")
            print("6 Voir logs")
            print("7 Voir tous les tickets(qui a fait la demande & qui l'a traité)")
            print("0 Déconnexion")

            choix = input("Choix : ")

            if choix == "1":
                afficher_tickets_assignes(utilisateur)
            elif choix == "3":
                ajouter_promo()
            elif choix == "4":
                ajouter_formation()
            elif choix == "5":
                assigner_ticket_admin()
            elif choix == "6":
                afficher_logs()
            elif choix == "7":
                voir_tous_les_tickets()
            elif choix == "0":
                break

# DEMARRAGE
def demarrer():
    while True:
        print("\n1 Inscription")
        print("2 Connexion")

        choix = input("Choix : ")

        if choix == "1":
            email = saisir_texte("Email : ")
            username = saisir_texte("Username : ")
            mdp = saisir_texte("Mot de passe : ")
            role = saisir_texte("Role : ")

            promo = None
            formation = None

            if role == "apprenant":
                promo = saisir_entier("ID promo : ")
                formation = saisir_entier("ID formation : ")

            inscription(email, mdp, username, role, promo, formation)

        elif choix == "2":
            email = saisir_texte("Email : ")
            username = saisir_texte("Username : ")

            oubli = saisir_texte("Mot de passe oublié ? (oui/non) : ")

            if oubli == "oui":
                nouveau = saisir_texte("Nouveau mot de passe : ")
                reinitialiser_mot_de_passe(email, nouveau)
            else:
                mdp = saisir_texte("Mot de passe : ")
                utilisateur = connexion(email, username, mdp)

                if utilisateur:
                    menu(utilisateur)
                else:
                    print("Identifiants incorrects")

if __name__ == "__main__":
    demarrer()
