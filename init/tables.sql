--table region
create table region (
	CodeReg VARCHAR(2) CONSTRAINT cle_region PRIMARY KEY,
	NomReg VARCHAR(50) CONSTRAINT region_not_null NOT NULL
);

--table departement
create table departement (
	CodeDep VARCHAR(3) CONSTRAINT cle_departement PRIMARY KEY,
	NomDep VARCHAR(50) CONSTRAINT departement_not_null NOT NULL,
	CodeReg VARCHAR(2) CONSTRAINT departement_foreign_region REFERENCES region (CodeReg) ON UPDATE CASCADE ON DELETE CASCADE
);

--table commune
create table commune (
	CodeCom VARCHAR(5) CONSTRAINT cle_commune PRIMARY KEY,
	NomCom VARCHAR(50) CONSTRAINT departement_not_null NOT NULL,
	CodeDep VARCHAR(3) CONSTRAINT commune_foreign_departement REFERENCES departement (CodeDep) ON UPDATE CASCADE ON DELETE CASCADE
);

-- table cheflieureg
create table cheflieureg (
	CodeReg VARCHAR(2) CONSTRAINT codereg_unique UNIQUE CONSTRAINT cheflieureg_foreign_region REFERENCES region (CodeReg) ON UPDATE CASCADE ON DELETE CASCADE,
	CodeCom VARCHAR(5) CONSTRAINT codecom_unique UNIQUE CONSTRAINT cheflieureg_foreign_commune REFERENCES commune (CodeCom) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (CodeReg, CodeCom)
);

-- table cheflieudep
create table cheflieudep (
	CodeDep VARCHAR(3) CONSTRAINT codedep_unique UNIQUE CONSTRAINT cheflieudep_foreign_departement REFERENCES departement (CodeDep) ON UPDATE CASCADE ON DELETE CASCADE,
	CodeCom VARCHAR(5) CONSTRAINT codecom_unique UNIQUE CONSTRAINT cheflieureg_foreign_commune REFERENCES commune (CodeCom) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (CodeDep, CodeCom)
);

-- table labelstats
create table labelstats (
	IdStat SERIAL CONSTRAINT cle_labelstats PRIMARY KEY,
	CodeStat VARCHAR(20) CONSTRAINT codestat_unique UNIQUE,
	Description TEXT CONSTRAINT description_not_null NOT NULL
);

-- table statsreg
create table statsreg (
	CodeReg VARCHAR(2) CONSTRAINT statsreg_foreign_region REFERENCES region (CodeReg) ON UPDATE CASCADE ON DELETE CASCADE,
	IdStat SERIAL CONSTRAINT statsreg_foreign_labelstats REFERENCES labelstats (IdStat) ON UPDATE CASCADE ON DELETE CASCADE,
	Valeur NUMERIC CONSTRAINT valeur_not_null NOT NULL,
	Annee NUMERIC(4) CONSTRAINT annee_not_null NOT NULL,
	PRIMARY KEY (CodeReg, IdStat, Annee),
	CONSTRAINT annee_possible CHECK (Annee BETWEEN 1800 and EXTRACT(YEAR FROM now()))
);

-- table statsdep 
create table statsdep (
	CodeDep VARCHAR(3) CONSTRAINT statsdep_foreign_departement REFERENCES departement (CodeDep) ON UPDATE CASCADE ON DELETE CASCADE,
	IdStat SERIAL CONSTRAINT statsreg_foreign_labelstats REFERENCES labelstats (IdStat) ON UPDATE CASCADE ON DELETE CASCADE,
	Valeur NUMERIC CONSTRAINT valeur_not_null NOT NULL,
	Annee NUMERIC(4) CONSTRAINT annee_not_null NOT NULL,
	PRIMARY KEY (CodeDep, IdStat, Annee),
	CONSTRAINT annee_possible CHECK (Annee BETWEEN 1800 and EXTRACT(YEAR FROM now()))
);

-- table statscom
create table statscom (
	CodeCom VARCHAR(5) CONSTRAINT statscom_foreign_commune REFERENCES commune (CodeCom) ON UPDATE CASCADE ON DELETE CASCADE,
	IdStat SERIAL CONSTRAINT statsreg_foreign_labelstats REFERENCES labelstats (IdStat) ON UPDATE CASCADE ON DELETE CASCADE,
	Valeur NUMERIC CONSTRAINT valeur_not_null NOT NULL,
	Annee NUMERIC(4) CONSTRAINT annee_not_null NOT NULL,
	PRIMARY KEY (CodeCom, IdStat, Annee),
	CONSTRAINT annee_possible CHECK (Annee BETWEEN 1800 and EXTRACT(YEAR FROM now()))
);
