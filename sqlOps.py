# Written by Calla Robison
# # 4/24/2023
# This file's purpose was to define classes that would hold the SQL CRUD operations queries that 
# would be called in as objects in the dbIMP.py file to implement the operation in python.

class AddingOperations:
   # def sqlAddOps():
        #Add to Russian table
        pop_russianWords = """

        INSERT INTO russianWords(russWord,gramType) 
        VALUES (%s, %s);

        """

        #Add to english table
        pop_englishWords = """

            -- Add operation
            INSERT INTO englishWords (engWord,gramType,def)
            VALUES (%s, %s, 'N/A');

        """
        
        #Add to verb table
        pop_verb = """
            INSERT INTO verbs (id,russWord,gramType,verbType)
            VALUES ('0',%s, %s, %s);
        """

        #Update verb id with matching russian word id
        update_verbId = """
            UPDATE verbs
            JOIN russianWords
            ON russianWords.russWord = verbs.russWord
            SET verbs.id = russianWords.id;
        """

        #Add to pronoun table
        pop_pronoun = """
            INSERT INTO proNouns (id,russWord,gramType,gramCase)
            VALUES ('0',%s, %s, %s);
        """

        #Update pronoun id with matching russian word id
        update_pronounId = """
            UPDATE proNouns
            JOIN russianWords
            ON russianWords.russWord = proNouns.russWord
            SET proNouns.id = russianWords.id;
        """

        #Add to prep_conj table
        pop_prep_conj = """
            INSERT INTO prep_conj (id,russWord,gramType,gramCase)
            VALUES ('0', %s, %s, %s);
        """

        #Update prep_conj id with matching russian word id
        update_prepConjId = """
            UPDATE prep_conj
            JOIN russianWords
            ON russianWords.russWord = prep_conj.russWord
            SET prep_conj.id = russianWords.id;
        """

class DeletingOperations:

    #Delete from english and russian tables
    delete_query_reg = """
        DELETE russianWords, englishWords
        FROM russianWords 
        INNER JOIN englishWords ON russianWords.id = englishWords.id 
        WHERE englishWords.engWord = %s ;
     """

    #reset id incrementation on russian and english tables
    reset_auto_incrementEng = """
        ALTER TABLE englishWords AUTO_INCREMENT = 1;
        
    """
    reset_auto_incrementRuss = """
        ALTER TABLE russianWords AUTO_INCREMENT = 1;
        
    """
    fk1 = """
        alter table proNouns 
        add constraint fk_id1
	        foreign key (id) references russianWords(id)
	        on update cascade on delete cascade;

    """
    fk2 = """
        alter table prep_conj 
        add constraint fk_id2
	        foreign key (id) references russianWords(id)
	        on update cascade on delete cascade;

    """

    fk3 = """
        alter table verbs
        add constraint fk_id3
	        foreign key (id) references russianWords(id)
	        on update cascade on delete cascade;

    """
    dropFk1 = """
        alter table proNouns drop foreign key fk_id1;
    """
    dropFk2 = """
        alter table prep_conj drop foreign key fk_id2;
    """
    dropFk3 = """
        alter table verbs drop foreign key fk_id3;
    """

class EditingOperations:

    #Update russian table for russWord
    update_russWord = """
        UPDATE russianWords
        SET russianWords.russWord = %s 
        WHERE id = %s;
    """
    #Update english table for engWord
    update_engWord = """
        UPDATE englishWords
        SET englishWords.engWord = %s
        WHERE id = %s;
    """
    #update prep_conj table for russWord
    update_russWordPrepConj = """
        UPDATE prep_conj
        SET prep_conj.russWord = %s 
        WHERE id = %s;

    """
    #update verb table table for russWord
    update_russWordVerb = """
        UPDATE verbs
        SET verbs.russWord = %s
        WHERE id = %s; ;

    """
    #update proNouns table for russWord
    update_russWordProNouns = """
        UPDATE proNouns
        SET proNouns.russWord = %s 
        WHERE id = %s;;

    """
    #Update verb table for verbType
    update_verbType = """
        UPDATE verbs
        JOIN russianWords
        ON verbs.id = russianWords.id
        SET verbs.gramType = %s ;
    """

    #Update grammar query
    update_gramTypeRuss = """
        UPDATE russianWords
        JOIN englishWords
        ON russianWords.id = englishWords.id
        SET russianWords.gramType = %s ;
    """
    update_gramTypeEng = """
        UPDATE englishWords
        JOIN russianWords
        ON englishWords.id = russianWords.id
        SET englishWords.gramType = %s ;
    """

class RetrieveOperations:
     
     #Essentially a home view to view all words in database with enligsh to russian translation
     create_translateView = """
        CREATE VIEW IF NOT EXISTS translateview AS
	    SELECT id, engWord, russWord, gramType 
	    FROM englishWords NATURAL JOIN russianWords; 
     """
     show_translateView = """
        select * from translateview;
     """
    #Show only the noun - russian and english pair

     select_nouns = """
        SELECT englishWords.engWord, russianWords.russWord
        FROM englishWords
        INNER JOIN russianWords ON englishWords.id = russianWords.id
        WHERE englishWords.gramType = 'noun';
    """

    #Show only the adjectives - russian and english pair
     select_adj = """
        SELECT englishWords.engWord, russianWords.russWord
        FROM englishWords
        INNER JOIN russianWords ON englishWords.id = russianWords.id
        WHERE englishWords.gramType = 'adj';
    """

    #show only the adverbs - russian and english pair
     select_adv = """
        SELECT englishWords.engWord, russianWords.russWord
        FROM englishWords
        INNER JOIN russianWords ON englishWords.id = russianWords.id
        WHERE englishWords.gramType = 'adv';
    """
    #Show only the verbs - russian, english, and verb tuple
     select_verbs = """
        SELECT englishWords.engWord, russianWords.russWord as russVerb, verbs.gramType AS verbType
        FROM englishWords
        INNER JOIN russianWords ON englishWords.id = russianWords.id
        INNER JOIN verbs ON russianWords.id = verbs.id
        WHERE russianWords.gramType = 'verb';
    """

    #Show only the pronouns - russian, english, pronoun pair
     select_pronouns = """
        SELECT englishWords.engWord, russianWords.russWord AS russPronoun, proNouns.gramCase AS gramCase
        FROM englishWords
        INNER JOIN russianWords ON englishWords.id = russianWords.id
        INNER JOIN proNouns ON russianWords.id = proNouns.id
        WHERE russianWords.gramType = 'pronoun';
    """

    #show only the prepositions - russian, english, prep_conj - conj tuple
     select_prep = """
        SELECT englishWords.engWord, russianWords.russWord AS russPreposition, prep_conj.gramCase AS gramCase
        FROM englishWords
        INNER JOIN russianWords ON englishWords.id = russianWords.id
        INNER JOIN prep_conj ON russianWords.id = prep_conj.id
        WHERE russianWords.gramType = 'prep';
    """

    #show only the conjunctions - russian, english, prep_conj - preptuple
     select_conj = """
        SELECT englishWords.engWord, russianWords.russWord AS russConjunction, prep_conj.gramCase AS gramCase
        FROM englishWords
        INNER JOIN russianWords ON englishWords.id = russianWords.id
        INNER JOIN prep_conj ON russianWords.id = prep_conj.id
        WHERE russianWords.gramType = 'conj';
    """
     


    