#Asennusohjeet (Mac OS X)

Sovellus vaatii toimiakseen python3 sekä sqlite3. Python tarvitsee lisäksi lisäosat pip ja venv.

## Paikallinen versio:

1. Lataa repository koneellesi githubista. 
2. Avaa komentorivi, ja luo projektille virtuaaliympäristö komennoilla:
* python3 -m venv venv
* source venv/bin/activate
* Huom! Sinun pitää olla projektin kansiossa luodessasi ympäristön
3. Virtuaaliympäristön luomisen jälkeen voit ladata projektissa käytettävät riippuvuudet komennolla:
* pip install -r requirements.txt
4. Käynnistä sovellus paikallisesti komennolla:
* python3 run.py
5. Siirry komentorivisi ilmoittamaan osoitteeseen selaimessa. Voit halutessasi luoda käyttäjän sivun kautta, tai käyttämällä sqliteä.

Admin-tunnukset voi luoda vain sqliten kautta komennoilla:
* sqlite3 harjoitukset.db
* INSERT INTO account(name, username, password, role) VALUES('admin', 'admin', '*salasanasi*', 'ADMIN')

## Heroku:

1. Lataa ja asenna heroku. Terminaalista tämä onnistuu komennolla:
* brew install heroku/brew/heroku
2. heroku create StayBisi
3. Lisää paikalliseen versionhallintaan tieto Herokusta komennolla:
* git remote add heroku https://git.heroku.com/StayBusy.git
4. Siirretään projekti Herokuun:
* git add .
* git commit -m "*viestisi*"
* git push heroku master
5. Vaihdetaan herokun tietokanta Postgresql:ksi, jotta tieto pysyy tallennettuna:
* heroku config:set HEROKU=1
* heroku addons:add heroku-postgresql:hobby-dev
6. Admin-tunnusten luominen herokussa:
* heroku pg:psql
* INSERT INTO account (name, username, password, role) VALUES ('admin', 'admin', 'salasanasi', 'ADMIN');

