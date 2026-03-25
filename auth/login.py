import hashlib


# AJOUT : Import des éléments de security.py
from security import verifications_connexion, traitement_mdp, PEPPER


def mdp_conform(mdp):
    if len(mdp) < 6:
        return False
    a_majuscule = a_minuscule = a_chiffre = a_special = False
    for caractere in mdp:
        if caractere.isupper():
            a_majuscule = True
        elif caractere.islower():
            a_minuscule = True
        elif caractere.isdigit():
            a_chiffre = True
        elif not caractere.isalnum():
            a_special = True
    return a_majuscule and a_minuscule and a_chiffre and a_special


def inscription(nom, prenom, email, mdp):
    h_mdp = traitement_mdp(mdp, email)

    if h_mdp and role != "erreur_code":
        conn = get_connection()
        if conn:
            try:
                curseur = conn.cursor()

                requete = """
                    INSERT INTO User (Nom, Prenom, Email, Adresse, MDP, Role, ID_banquier)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                role_sql = role.capitalize()
                valeurs = (nom, prenom, email, adresse, h_mdp, role_sql, id_banquier)

                curseur.execute(requete, valeurs)
                conn.commit()
                return True
            except Exception as e:
                print(f"Erreur lors de l'inscription : {e}")
                conn.rollback()
            finally:
                curseur.close()
                conn.close()
    return False


def login(email, mdp):
    cnx = get_connection()
    if cnx:
        cur = cnx.cursor()
        # MODIFICATION : On sélectionne ID, Nom, Prenom pour pouvoir les utiliser dans app.py
        cur.execute(
            "SELECT ID, Nom, Prenom, MDP, Role FROM User WHERE Email = %s", (email,)
        )
        res = cur.fetchone()
        cur.close()
        cnx.close()

        # res[3] correspond au MDP haché dans la BDD
        if res and verifications_connexion(mdp, res[3], email):
            # MODIFICATION : On retourne un dictionnaire complet pour la session de l'app
            return {
                "id": res[0],
                "nom": res[1],
                "prenom": res[2],
                "role": res[4],
                "email": email,
            }
    return None
