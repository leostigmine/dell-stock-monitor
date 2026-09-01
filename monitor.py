import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
URL = "https://www.dell.com/fr-fr/shop/ordinateurs-portables-dell/ordinateur-portable-dell-14-plus/spd/dell-db14250-laptop/cndb1425003sc"
EMAIL_TO = "leo.heinon.pro@gmail.com"
EMAIL_FROM = os.environ.get("GMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

def check_stock():
    # Headers pour simuler un vrai navigateur et éviter d'être bloqué par Dell
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        # On passe tout le code HTML en minuscules pour faciliter la recherche
        content = response.text.lower()
        
        # Condition : "ajouter au panier" est présent ET "rupture de stock" n'y est plus
        if "ajouter au panier" in content and "rupture de stock" not in content:
            print("Le produit est EN STOCK !")
            send_email()
        else:
            print("Le produit est toujours en rupture de stock.")
            
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page : {e}")

def send_email():
    subject = "⚠️ ALERTE STOCK : Le Dell 14 Plus est DISPONIBLE !"
    body = f"Bonne nouvelle !\n\nL'ordinateur Dell est maintenant en stock (le bouton 'Ajouter au panier' a été détecté).\n\nVous pouvez l'acheter ici :\n{URL}"
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        # Connexion au serveur SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("E-mail d'alerte envoyé avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")

if __name__ == "__main__":
    if not EMAIL_FROM or not EMAIL_PASSWORD:
        print("Erreur : Les variables d'environnement GMAIL_ADDRESS et GMAIL_APP_PASSWORD ne sont pas définies.")
    else:
        check_stock()
