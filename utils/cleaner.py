import json
import csv
import sys
from urllib.parse import urlparse

def extract_domain(url):
    """Extrait le domaine principal d'une URL et ajoute www. si nécessaire"""
    # Ajouter le schéma si absent pour un parsing correct
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Parser l'URL
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path.split('/')[0]
    
    # Nettoyer le domaine (enlever le slash final si présent)
    domain = domain.rstrip('/')
    
    # Vérifier si c'est un sous-domaine (a plus de 2 parties avant le TLD)
    parts = domain.split('.')
    has_subdomain = len(parts) > 2
    
    # Ajouter www. seulement si le domaine ne commence pas déjà par www. et n'a pas de sous-domaine
    if domain and not domain.startswith('www.') and not has_subdomain:
        domain = 'www.' + domain
    
    return domain

def process_json_to_csv(input_file, output_file):
    """Lit le fichier JSON, modifie les URLs et sauvegarde en CSV"""
    try:
        # Lire le fichier d'entrée
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Modifier les URLs
        for item in data:
            if 'url' in item:
                item['url'] = extract_domain(item['url'])
        
        # Écrire dans le fichier CSV de sortie
        if data:
            # Récupérer les en-têtes (clés du premier élément)
            fieldnames = list(data[0].keys())
            
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"✓ Fichier CSV sauvegardé dans : {output_file}")
            print(f"✓ {len(data)} entrées traitées")
        else:
            print("✗ Attention : Le fichier JSON est vide")
        
    except FileNotFoundError:
        print(f"✗ Erreur : Le fichier '{input_file}' n'existe pas")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"✗ Erreur : Le fichier '{input_file}' n'est pas un JSON valide")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Erreur : {e}")
        sys.exit(1)

def main():
    """Fonction principale gérant les arguments"""
    if len(sys.argv) < 2:
        print("Usage : python script.py <fichier_entree.json> [fichier_sortie.csv]")
        print("\nExemples :")
        print("  python script.py input.json")
        print("  python script.py input.json output.csv")
        print("  python script.py /chemin/vers/data.json /chemin/vers/resultat.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Si pas de fichier de sortie spécifié, utiliser "output.csv"
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = "output.csv"
    
    process_json_to_csv(input_file, output_file)

if __name__ == "__main__":
    main()