## User Stories:

### Tietokantakaavioiden luomiset:

```sql
CREATE TABLE account (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	name VARCHAR(144) NOT NULL,
	username VARCHAR(144) NOT NULL,
	password VARCHAR(144) NOT NULL,
	role VARCHAR(144) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (username)
)

CREATE TABLE saliliike (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	nimi VARCHAR(144) NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE juoksu (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	pvm DATE NOT NULL,
	aika TIME NOT NULL,
	matka DECIMAL(6, 2) NOT NULL,
	account_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(account_id) REFERENCES account (id)
)

CREATE TABLE salikerta (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	pvm DATE NOT NULL,
	aika TIME NOT NULL,
	account_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(account_id) REFERENCES account (id)
)
```

### Käyttäjänä voin:

* Rekisteröityä
```sql
INSERT INTO account (date_created, date_modified, name, username, password, role) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, <name>, <username>, <password>, <role>)

```

* Kirjautua sisään
```sql
SELECT account.id AS account_id, account.date_created AS account_date_created, account.date_modified AS account_date_modified, account.name AS account_name, account.username AS account_username, account.password AS account_password, account.role AS account_role
FROM account
WHERE account.username = <username> AND account.password = <password>
```
* Nähdä tietokannan pisimmän juoksun sekä oman pisimmän juoksuni

```sql
SELECT MAX(Juoksu.matka) FROM Juoksu

SELECT MAX(Juoksu.matka) FROM Juoksu WHERE Juoksu.account_id = <user_id> GROUP BY Juoksu.matka

```


* Selata kaikkia lisäämiäni harjoituksia tietokannasta
```sql
SELECT Juoksu.id, Juoksu.pvm, Juoksu.matka, Juoksu.aika FROM Juoksu WHERE Juoksu.account_id = <user_id> GROUP BY Juoksu.id

SELECT Salikerta.id, Salikerta.pvm, Salikerta.aika FROM Salikerta WHERE Salikerta.account_id = <user_id> GROUP BY Salikerta.id

```


* Muokata harjoituksiani tai poistaa lisäämäni harjoituksen tietokannasta
```sql
UPDATE juoksu SET date_modified=CURRENT_TIMESTAMP, pvm=<pvm> WHERE juoksu.id = <juoksu.id>

DELETE FROM juoksu WHERE juoksu.id = <juoksu.id>
```



* Hakea harjoituksiani päivämäärän mukaan
```sql
SELECT Juoksu.id, Juoksu.pvm, Juoksu.matka, Juoksu.aika FROM Juoksu WHERE Juoksu.account_id = <account_id> AND Juoksu.pvm >= <pvm_1> AND Juoksu.pvm <= <pvm_2> GROUP BY Juoksu.id

```


* Lisätä juoksun tietokantaan
```sql
INSERT INTO juoksu (date_created, date_modified, pvm, aika, matka, account_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, <pvm>, <aika>, <matka>, <user_id>)
```


* Lisätä kuntosaliharjoituksen tietokantaan
```sql
INSERT INTO salikerta (date_created, date_modified, pvm, aika, account_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, <pvm>, <aika>, <user_id>)
```


* Lisätä kuntosaliliikkeen tietokantaan

```sql
INSERT INTO saliliike (date_created, date_modified, nimi) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, <nimi>)

```


### Adminina voin:

* Listata kaikki tietokannan harjoitukset
```sql
SELECT juoksu.id AS juoksu_id, juoksu.date_created AS juoksu_date_created, juoksu.date_modified AS juoksu_date_modified, juoksu.pvm AS juoksu_pvm, juoksu.aika AS juoksu_aika, juoksu.matka AS juoksu_matka, juoksu.account_id AS juoksu_account_id
FROM juoksu

SELECT salikerta.id AS salikerta_id, salikerta.date_created AS salikerta_date_created, salikerta.date_modified AS salikerta_date_modified, salikerta.pvm AS salikerta_pvm, salikerta.aika AS salikerta_aika, salikerta.account_id AS salikerta_account_id
FROM salikerta

```


* Poistaa tai muokata käyttäjien lisäämiä harjoituksia
```sql
UPDATE salikerta SET date_modified=CURRENT_TIMESTAMP, pvm=<pvm>, aika=<aika> WHERE salikerta.id = <salikerta.id>

DELETE FROM salikerta WHERE salikerta.id = <salikerta.id>

```

