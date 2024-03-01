-- Initial creation of the SQL database written in SQL
-- Initial creation of database tables and preinputted
-- information for testing.

drop database if exists russLangTool;
CREATE DATABASE IF NOT EXISTS russLangTool;

USE russLangTool;



CREATE TABLE IF NOT EXISTS englishWords (
  id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
  engWord VARCHAR(100) NOT NULL, 
  gramType VARCHAR(100), def VARCHAR(100));

 -- ALTER TABLE englishWords AUTO_INCREMENT = 1;
 -- alter table englishwords add primary key (id, engWord);
 
CREATE TABLE IF NOT EXISTS russianWords (
  id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  russWord VARCHAR(100) not NULL, 
  gramType VARCHAR(100));
 
CREATE TABLE IF NOT EXISTS proNouns (
  id INT NOT NULL,
  russWord VARCHAR(90) NOT NULL, 
  gramType VARCHAR(100),
  gramCase VARCHAR(100) NOT NULL,
  PRIMARY KEY (id, gramCase)
);
 
CREATE TABLE IF NOT EXISTS verbs (
  id INT not NULL ,
  russWord VARCHAR(100) NOT NULL, 
  gramType VARCHAR(100),
  verbType VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
);
 
CREATE TABLE IF NOT EXISTS prep_conj (
  id INT NOT NULL,
  russWord VARCHAR(100) NOT NULL, 
  gramType VARCHAR(100),
  gramCase VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
);



INSERT INTO englishWords (engWord,gramType,def) 
VALUES('apple','noun','a fruit'), 
      ('ice cream','noun','a dessert'), ('water','noun','a drink'),  
      ('grape','noun','a fruit'), ('Beer','noun','an alcoholic drink'), 
      ('banana','noun','fruit'), ('bread','noun','a carbohydrate'),('I', 'pronoun', 'yourself'),
     ('you', 'pronoun','direct someone else'),('we','pronoun','a colllective us'),('in','prep', 'inside something'),
    ('on','prep','on top of something'),('about','prep','the information describing something'),
   ('to go','verb','to travel somewhere'), ('to see','verb','to look at something'),
  ('to read','verb','to comprehend words'), ('without','prep','not having something'), ('if','conj','idk'),
 ('and','conj','add another sentence'), ('but','conj','idk'), ('usually', 'adv', 'happens often'), 
 ('quickly', 'adv', 'move at a fast pace'), ('slowly', 'adv', 'move at a slow pace'), 
('big', 'adj', 'enormous in size'), ('small', 'adj', 'meniscule size'), ('heavey', 'adj', 'a lot of weigh');
     
 -- describe englishWords;
     
INSERT INTO russianWords (russWord,gramType) 
values
	  ('яблоко','noun'), 
      ('мороженое','noun'), ('вода','noun'),  
      ('виноград','noun'), ('пиво','noun'), 
      ('банан','noun'), ('хлеб','noun'), ('я', 'pronoun'),
     ('ты','pronoun'),('мы','pronoun'),('в','prep'),('на','prep'),('о','prep'),
    ('ходить','verb'), ('видить','verb'), ('читать','verb'), ('без','prep'), ('если','conj'), ('и','conj'),
   ('но','conj'), ('обычно','adv'), ('выстро','adv'), ('медленно','adv'), ('большой','adj'), ('маленький','adj'), 
  ('тяжёлый','adj');
     
INSERT INTO proNouns (id,russWord,gramType,gramCase) 
VALUES
('8','я', 'pronoun','nom'), 
('9','ты','pronoun','nom'), 
('10','мы','pronoun','nom');

INSERT INTO prep_conj (id,russWord,gramType,gramCase) 
values
	  ('11','в','prep','prep'), 
      ('12','на','prep','prep'), ('13','о','prep','prep'), ('17','без','prep','gen'),
     ('18','если','conj','nom'), ('19','и','conj','nom'), ('20','но','conj','nom') ;
INSERT INTO verbs (id,russWord,gramType,verbType) 
values
	  ('14','ходить','verb','imperf'), 
      ('15','видить','verb','imperf'), ('16','читать','verb','imperf');
     
-- alter table proNouns 
-- add constraint fk_id1
-- 	foreign key (id) references russianWords(id)
-- 	on update cascade on delete cascade;
-- 
-- alter table prep_conj 
-- add constraint fk_id2
-- 	foreign key (id) references russianWords(id)
-- 	on update cascade on delete cascade;
-- 
-- alter table verbs
-- add constraint fk_id3
-- 	foreign key (id) references russianWords(id)
-- 	on update cascade on delete cascade;
-- SELECT englishWords.engWord, russianWords.russWord, verbs.russWord
-- FROM englishWords
-- INNER JOIN russianWords ON englishWords.id = russianWords.id
-- inner join verbs on russianWords.id = verbs.id
-- WHERE russianWords.gramType = 'verb' ;

-- SELECT englishWords.engWord, russianWords.russWord AS russConjunction, prep_conj.gramCase AS gramCase
--         FROM englishWords
--         INNER JOIN russianWords ON englishWords.id = russianWords.id
--         INNER JOIN prep_conj ON russianWords.id = prep_conj.id
--         WHERE russianWords.gramType = 'conj';
       
--  DELETE russianWords, englishWords
--         FROM russianWords 
--         INNER JOIN englishWords ON englishWords.id = russianWords.id 
--         WHERE englishWords.engWord = 'water' ;     
     
-- create view translateview as
-- 	select id, engWord, russWord, gramType 
-- 	from englishWords natural join russianWords;
-- 
-- select * from translateview;

-- SELECT englishWords.engWord, russianWords.russWord, prep_conj.russWord
-- FROM englishWords
--  INNER JOIN russianWords ON englishWords.id=russianWords.id
--  INNER JOIN prep_conj ON englishWords.id=prep_conj.id;


     

     
-- SELECT * FROM englishWords;
-- SELECT * FROM russianWords;
-- SELECT * FROM proNouns;
-- SELECT * FROM verbs;
-- SELECT * FROM prep_conj;

/*
-- SQL Operation examples

SELECT englishWords.engWord, russianWords.russWord
FROM englishWords
 INNER JOIN russianWords ON englishWords.id=russianWords.id;



create view translateview as
	select id, engWord, russWord
	from englishWords natural join russianWords;

select * from translateview;
	
create view nounview as
	select id, engWord, russWord
	from englishWords natural join russianWords
	where gramType = 'noun';

select * from nounview;

select englishWords.engWord, proNouns.russWord, proNouns.proCase  
from englishWords
inner join proNouns on englishWords.id=proNouns.id;

-- Delete operation
DELETE russianWords, englishWords
FROM russianWords
INNER JOIN englishWords
ON russianWords.id = englishWords.id
WHERE russianWords.id = 1;

SELECT englishWords.engWord, russianWords.russWord
FROM englishWords
INNER JOIN russianWords ON englishWords.id=russianWords.id;

select * from translateview;



-- create view verbview as
-- 	select engWord, russWord, verbType
-- 	from englishWords natural join russianWords
-- 	where gramType = 'verb';

-- select * from nounview;

*/

/*
-- Add operation
INSERT INTO englishWords (engWord,eGramType,def)
VALUES ('they', 'pronoun','direct to a group of people');

INSERT INTO russianWords (russWord,rGramType)
VALUES ('они', 'pronoun');

-- INSERT INTO proNouns SELECT * FROM russianWords where russianWords.rGramType = 'pronoun';
INSERT INTO proNouns (id, russWord, rGramType, proCase)
SELECT id, russWord, rGramType, 'nominative' AS proCase
FROM russianWords
WHERE rGramType = 'pronoun'
  AND id = (SELECT MAX(id) FROM russianWords);

 SELECT * FROM russianWords;
 SELECT * FROM proNouns;

-- Delete operation
DELETE russianWords, englishWords
FROM russianWords
INNER JOIN englishWords
ON russianWords.id = englishWords.id
WHERE russianWords.id = 1;

-- SELECT * FROM englishWords;
-- SELECT * FROM russianWords;

-- update operation
UPDATE russianWords AS r
INNER JOIN englishWords AS e
ON r.id = e.id
SET r.russWord = 'водка', e.engWord = 'vodka'
WHERE r.id = 5;

SELECT * FROM englishWords;
 SELECT * FROM russianWords;*/



