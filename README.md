Postgresql Connection over IntelliJ:
Host: localhost
Port: 5432
Authentication: User & Password
User: keycloak
Password: password
Database: keycloak
URL: jdbc:postgresql://localhost:5432/keycloak



POSTGRES SQL Konfiguration:
grant all privileges on database keycloak to keycloak;

Create TABLE user_table(
    ID SERIAL,
    FIRSTNAME TEXT NOT NULL,
    LASTNAME TEXT NOT NULL,
    MAIL TEXT PRIMARY KEY NOT NULL,
    PASSWORD TEXT NOT NULL,
    MAIL_SERVICE BOOLEAN NOT NULL
);


Create TABLE user_stocks(
    ID SERIAL,
    MAIL TEXT NOT NULL,
    STOCK_SYMBOL TEXT NOT NULL,
    CONSTRAINT FK_MAIL
                        FOREIGN KEY(mail)
                        REFERENCES user_table(mail)
);