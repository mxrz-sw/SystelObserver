# 📱Jobagent für Benachrichtigungen bei DB Systel Jobanzeigen (SystelObserver)

**Benachrichtigungen bei neuen Stellenanzeigen via EMail & PushNotification - läuft vollautomatisch auf einem Raspberry Pi**

---

## 🧠 Projektidee

Das Python Projekt dient für mich als **automatischer Jobagent** für Stellenanzeigen der **DB Systel GmbH**. Es durchsucht jede 5 Minuten die offizielle Karriereseite der Deutschen Bahn ([db.jobs](https://db.jobs)) und prüft, ob neue Stellenanzeigen veröffentlicht wurden. Wenn sich die Anzahl der Anzeigen ändert, werde ich sofort über Mail und über eine Push Notification auf meinem Handy informiert.

---

## ⚙️ Features

- 🔄 Automatisches Monitoring alle 5 Minuten
- 📧 E Mail Benachrichtigung bei Neuen Stellenanzeigen
- 📲 Push Benachrichtigung über [Pushover](https://pushover.net)
- 🌐 Webscraping mit BeautifulSoup
- 🔹 Läuft automatisiert auf einem Raspberry Pi

---

## 🧰 Verwendete Technologien

| Zweck                 | Technologie                |
| --------------------- | -------------------------- |
| HTML Scraping         | `BeautifulSoup`            |
| HTTP Anfragen         | `requests`                 |
| EMail Versand         | `smtplib`, `MIMEText`      |
| Push Benachrichtigung | `Pushover API`             |
| Automatischer Start   | `systemd` auf Raspberry Pi |
| Scheduler             | `time.sleep()`             |

---

## 💻 So läuft das Ganze auf einem Raspberry Pi

Das Script läuft dauerhaft auf einem Raspberry Pi mit Raspbian. Es wird dort als \`\`**-Service** eingerichtet, sodass es automatisch beim Hochfahren startet und im Hintergrund läuft ohne manuelles Starten.

### 🔧 Einrichtung auf dem Raspberry Pi

1. **Python Abhängigkeiten installieren**:

   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install beautifulsoup4 requests
   ```

2. **Skript speichern.**

3. **Systemd Service Datei anlegen**:

   ```ini
   # /etc/systemd/system/jobagent.service

   [Unit]
   Description=DB Systel Jobagent
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /home/pi/jobagent/SystelObserver.py
   WorkingDirectory=/home/pi/jobagent
   Restart=always
   User=pi

   [Install]
   WantedBy=multi-user.target
   ```

4. **Service aktivieren und starten**:

   ```bash
   sudo systemctl daemon-reexec
   sudo systemctl enable jobagent
   sudo systemctl start jobagent
   ```

5. **Status prüfen**:

   ```bash
   systemctl status jobagent
   ```

---

## 📷 Beispielausgabe

```
[START] Tracking DB Systel listings on https://db.jobs/...
[JobAgent] Hat 25 Stellenanzeigen gefunden.
[CHANGE] Anzahl Endlich!!: 2 jetzt 3
[EMAIL] Gesendet: db.jobs Anzahl Changed!
[PUSHOVER] Nachricht gesendet.
```

---

## ⚠️ Sicherheits Wahrnung

🔐 Zugangsdaten wie EMail Passwörter und API Tokens sollten nicht im Quelltextoder in Repositories gespeichert werden:

- Deswegen nutze ich demonstrativ  .env-Dateien + dotenv-Bibliothek (


## 📬 Kontakt

**Maximilian Andrzejczak**\
📧 [andrzejczak.max@gmail.com](mailto\:andrzejczak.max@gmail.com)\
💼 IT-Stundent & Werkstudent im 2nd Level IT Support – Fokus auf Systemintegration, Automatisierung und Problemlösung.

---

## 💡 Erweiterungsideen

- 🔎 Filter nach bestimmten Schlüsselwörtern (Ausbildung, Fachinformatiker)
- 🔁 Unterstützung für andere Jobportale
- 📊 Historie der Veränderungen speichern und grafisch darstellen
- 🧑‍💻 Webinterface zur Steuerung und Konfiguration


---

## ✅ Status

Bis jetzt ist das Projekt vollständig funktionsfähig, erfüllt sein Zweck gut und ist bereits auf einem Raspberry Pi im Einsatz. Es läuft zuverlässig seit mehreren Wochen und hat mir schon mehrfach neue DB Systel Stellenangebote gemeldet.

---

