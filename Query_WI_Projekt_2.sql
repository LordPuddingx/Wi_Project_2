Create table tblLogin (
	E_Mail Nvarchar(50),
	Pw Nvarchar(100) NOT NULL,
	Primary Key (E_Mail)
)

Insert into tblLogin (E_Mail, Pw) Values ('DomGOD@hotmail.com', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4')

Create table tblProfil (
	E_Mail Nvarchar(50),
	Nachname Nvarchar(50),
	Vorname Nvarchar(50),
	Strasse Nvarchar(50),
	PLZ Nvarchar(50),
	Stadt Nvarchar(50),
	Bundesland Nvarchar(50),
	PRIMARY KEY (E_Mail)	
)


Create table tblTest (
	voll_teilstationaere_Behandlung Nvarchar(10) NOT NULL,
	vor_nachstationaere_BehandlungPw Nvarchar(10) NOT NULL,
	ambulante_Behandlung Nvarchar(10) NOT NULL,
	anderer_Grund Nvarchar(10) NOT NULL,
	anderer_Grund_Kommentar Nvarchar(50)
)

Drop table tblTest

Delete from tblLogin where E_Mail like '%%'
Delete from tblProfil where E_Mail like '%%'
Delete from tblTest where voll_teilstationaere_Behandlung like '%%'