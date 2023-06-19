-- SQL Datei um die benötigten Datenbanktabellen zu erstellen, die Tabellen müssen in einer Datenbank mit
-- dem Namen "Kunden_DB" angelegt werden.
Create table tblLogin (
	E_Mail Nvarchar(50),
	Pw Nvarchar(100) NOT NULL,
	Primary Key (E_Mail)
) Create table tblProfil (
	E_Mail Nvarchar(50),
	Nachname Nvarchar(50),
	Vorname Nvarchar(50),
	Strasse Nvarchar(50),
	PLZ Nvarchar(50),
	Stadt Nvarchar(50),
	Bundesland Nvarchar(50),
	PRIMARY KEY (E_Mail)
) Create table tblTest (
	voll_teilstationaere_Behandlung Nvarchar(10) NOT NULL,
	vor_nachstationaere_BehandlungPw Nvarchar(10) NOT NULL,
	ambulante_Behandlung Nvarchar(10) NOT NULL,
	anderer_Grund Nvarchar(10) NOT NULL,
	anderer_Grund_Kommentar Nvarchar(50)
) Create table tblFahrtenbuchung (
	ID int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
	email NVARCHAR(50) REFERENCES tblProfil(E_Mail) NOT NULL,
	datum datetime,
	Behandlungsstätte NVARCHAR(255),
	auf_rechnung NVARCHAR(25),
	voll_teilstationaere_Behandlung BIT NOT NULL,
	vor_nachstationaere_BehandlungPw BIT NOT NULL,
	ambulante_Behandlung BIT NOT NULL,
	anderer_Grund BIT NOT NULL,
	anderer_Grund_Kommentar NVARCHAR(255),
	hochfrequente_Behandlung BIT NOT NULL,
	vergleichbarer_Ausnahmefall BIT NOT NULL,
	dauerhafte_Mobilitätsbeeinträchtigung BIT NOT NULL,
	anderer_Grund_für_Fahrt BIT NOT NULL,
	Taxi BIT NOT NULL,
	KTW BIT NOT NULL,
	KTW_Begründung NVARCHAR(255),
	RTW BIT NOT NULL,
	NAW BIT NOT NULL,
	andere BIT NOT NULL,
	andere_Begründung NVARCHAR(255),
	Rollstuhl BIT NOT NULL,
	Tragestuhl BIT NOT NULL,
	liegend BIT NOT NULL,
	begruendung_sonstige NVARCHAR(255)
);