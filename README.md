# 🕵️ CTF Web Hackademy — site d'intégration

Site du club **Hackademy** transformé en petit CTF web très guidé pour les nouveaux.
Parcours : **code d'accès → login (SQL injection) → dashboard → code source (F12) → robots.txt → coffre final**.

Deux versions sont fournies :

---

## 🟢 Version STATIQUE (recommandée pour l'événement)

Rien à installer. Injection SQL **simulée** en JavaScript.

**Tester en local :** ouvre `index.html` dans un navigateur.
> ⚠️ Le mieux est de passer par un petit serveur local (sinon `robots.txt` et les sous-dossiers marchent moins bien) :
> ```
> python -m http.server 8000
> ```
> puis ouvre `http://localhost:8000/`

**Mettre en ligne (URL publique gratuite) :**
- **GitHub Pages** : pousse le dossier dans un repo → Settings → Pages → branche `main`.
- ou **Netlify / Vercel** : glisse-dépose le dossier, tu as une URL en 30 s.

Tous les téléphones ouvrent la même URL. Zéro serveur à gérer.

---

## 🔵 Version FLASK (vraie injection SQL)

Injection SQL **réelle** contre une base SQLite.

```
pip install flask
python app.py
```
Puis, sur le **wifi de l'école**, les participants ouvrent `http://<IP-DE-CE-PC>:5000/`
(ton IP : `ipconfig` sous Windows / `ip a` sous Linux).

---

## ⚙️ À personnaliser avant l'événement

| Quoi | Où |
|---|---|
| **Code d'accès** (sortie du quiz du club dev) | `index.html` → variable `CODE_ACCES` (statique) |
| Les **flags** | `admin.html`, `documentation.html`, `robots.txt`, `galerie-s3cr3t3/index.html` |
| Le **lien robots.txt** montré dans le code source | commentaire en haut de `documentation.html` |

## 🚩 Les flags du parcours

| Étape | Flag |
|---|---|
| 1 — SQL Injection (login) | `HKM{SQL_1NJ3CT10N_R3USS13}` |
| 2 — Code source / F12 (dans `documentation.html`) | `HKM{V13W_S0URC3_D3T3CT1V3}` |
| 3 — robots.txt | `HKM{R0B0TS_TXT_R3V3L4T10N}` |
| 4 — Coffre final | `HKM{Image<x>}` — **x = le numéro de l'indice de départ de l'équipe** |

## 🎫 L'indice de départ (à remettre, 1 par équipe)

Chaque équipe reçoit au départ un indice affichant :
```
        HKM{Image_ }        ← un numéro d'image (ex. HKM{Image3}), DIFFÉRENT par équipe

   YOU ARE CAPTURING THE FLAG RIGHT NOW !
```
À la fin, la page `galerie-s3cr3t3/` affiche « YOU WERE CAPTURING THE FLAG ALL THE TIME! ».
Ils retapent leur numéro → le site affiche **l'image correspondante** : c'est l'indice de leur
**PROCHAINE STATION** de la chasse au trésor.

### 🖼️ Mapping numéro → image (dans `galerie-s3cr3t3/index.html`, objet `IMAGES`)
| Numéro | Fichier |
|---|---|
| Image1 | `assets/image1.jpg` |
| Image2 | `assets/image2.jpg` |
| Image3 | `assets/image3.jpg` |
| Image4 | `assets/image4.jpg` |
| Image5 | `assets/image5.jpg` |
> Les 5 images actuelles sont des **placeholders** — remplace-les par tes vraies photos de stations (garde les mêmes noms de fichiers).

## 🗺️ Parcours complet

1. `index.html` — entre le code d'accès du club dev
2. `site.html` — vitrine du club (cellules, activités, bureau) → bouton **Espace membres**
3. `login.html` — taper `password` échoue → note rouge SQLi → payload `' OR '1'='1' -- ` → admin
4. `admin.html` — dashboard + 1er flag → lien **Documentation**
5. `documentation.html` — F12 / code source → flag caché + va sur `/robots.txt`
6. `robots.txt` — un `Disallow` révèle `/galerie-s3cr3t3/`
7. `galerie-s3cr3t3/` — le twist final + champ `HKM{...}`
