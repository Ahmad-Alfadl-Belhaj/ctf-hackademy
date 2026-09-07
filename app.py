#!/usr/bin/env python3
# =====================================================================
#  HACKADEMY — CTF d'intégration — VERSION FLASK (vraie injection SQL)
# ---------------------------------------------------------------------
#  Sert le même site que la version statique, MAIS le login /login.html
#  exécute une VRAIE requête SQL volontairement vulnérable (sqlite).
#
#  Lancer :
#     pip install flask
#     python app.py
#  Puis, sur le wifi de l'école, tout le monde ouvre :
#     http://<IP-DE-CE-PC>:5000/
#  (trouve ton IP avec `ipconfig` sous Windows ou `ip a` sous Linux)
# =====================================================================
import os, sqlite3
from flask import Flask, request, send_from_directory, render_template_string, redirect

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# --- petite base de données du club (en mémoire, recréée à chaque requête) ---
def make_db():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE users(username TEXT, password TEXT, role TEXT)")
    db.executemany("INSERT INTO users VALUES(?,?,?)", [
        ("admin",       "S3cr3t_ENSAJ_2026!", "super-admin"),
        ("a.belhaj",    "pres2026",           "président"),
        ("guest",       "guest",              "invité"),
    ])
    db.commit()
    return db

LOGIN_HTML = """<!DOCTYPE html><html lang="fr"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hackademy — Espace membres</title><link rel="stylesheet" href="/styles.css"></head><body>
<div class="auth-wrap"><div class="auth-card">
  <img src="/assets/logo.jpg" class="logo-sm" alt="Hackademy">
  <h2>Espace membres / Admin</h2>
  <p class="hint">Connecte-toi pour accéder au panneau d'administration.</p>
  <form method="POST" action="/login.html">
    <label>Utilisateur</label>
    <input type="text" name="username" placeholder="admin" autocomplete="off" value="{{u}}">
    <label>Mot de passe</label>
    <input type="password" name="password" placeholder="••••••••" autocomplete="off">
    <button class="btn" type="submit">Se connecter</button>
  </form>
  {% if failed %}<div class="msg err">❌ Utilisateur ou mot de passe incorrect.</div>{% endif %}
  <div class="tip">💡 Astuce sécurité : parfois les admins sont paresseux… il paraît que le mot de passe est juste <b>password</b>.</div>
  {% if failed %}
  <div class="sqli-note">
    <div class="head">🟥 SQL INJECTION</div>
    <div class="body">
      <h5>C'est quoi ?</h5>
      <p>Une faille où on trompe la base de données en glissant un bout de code dans un champ de texte, au lieu d'un vrai mot de passe.</p>
      <h5>Analogie 🧠</h5>
      <p class="analogy">Imagine un videur : sa règle est « je laisse entrer si le nom est sur la liste ET le mot de passe est bon ».
        La SQL injection, c'est lui souffler « mon nom… <b>OU</b> alors laisse entrer tout le monde ». Il ouvre la porte à tous.</p>
      <h5>Exemple à essayer ⚙️</h5>
      <p>Copie ceci dans le champ <b>Utilisateur</b> (mets n'importe quoi dans Mot de passe) :</p>
      <code class="code-box">' OR '1'='1' -- </code>
      <p style="color:var(--muted);font-size:.85rem">Le <span class="mono">' OR '1'='1'</span> rend la condition <b>toujours vraie</b>,
        et le <span class="mono">-- </span> dit à la base « ignore le reste » → elle ne vérifie plus le mot de passe.</p>
    </div>
  </div>{% endif %}
</div></div></body></html>"""

@app.route("/login.html", methods=["GET", "POST"])
@app.route("/login",      methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string(LOGIN_HTML, failed=False, u="")
    u = request.form.get("username", "")
    p = request.form.get("password", "")
    # !!! REQUÊTE VOLONTAIREMENT VULNÉRABLE (ne JAMAIS faire ça en vrai) !!!
    query = "SELECT username, role FROM users WHERE username = '%s' AND password = '%s'" % (u, p)
    db = make_db()
    try:
        row = db.execute(query).fetchone()   # une injection fait renvoyer une ligne
    except Exception:
        row = None
    db.close()
    if row:
        return redirect("/admin.html")
    return render_template_string(LOGIN_HTML, failed=True, u=u)

# --- tout le reste = fichiers statiques du site ---
@app.route("/")
def home():
    return send_from_directory(SITE_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    full = os.path.join(SITE_DIR, path)
    if os.path.isdir(full):
        return send_from_directory(full, "index.html")
    return send_from_directory(SITE_DIR, path)

if __name__ == "__main__":
    print("HACKADEMY CTF — http://0.0.0.0:5000  (partage l'IP de ce PC aux participants)")
    app.run(host="0.0.0.0", port=5000, debug=False)
