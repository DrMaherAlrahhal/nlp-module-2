"""40 practice questions: 15 MCQ, 10 true/false, 10 concept, 5 scenarios."""

QUESTIONS = []


def add(part, kind, prompt, answer, others, concept, why, example):
    # Rotate answers so their position never reveals the correct choice.
    choices = [answer] + others
    offset = len(QUESTIONS) % len(choices)
    choices = choices[offset:] + choices[:offset]
    QUESTIONS.append(dict(id=f'q{len(QUESTIONS)+1:02}', part=part, kind=kind,
                          prompt=prompt, answer=answer, choices=choices,
                          concept=concept, why=why, example=example))


add(1,'Multiple choice','What does morphology study?','Internal structure and formation of words',['Only sentence order','Only sound volume','Only named people'],'Morphology','Morphology looks at meaningful word structure.','unhappiness → un + happy + ness')
add(1,'Multiple choice','What is the root of unhelpful?','help',['un','ful','unhelp'],'Root, prefix, and suffix','help carries the central meaning; un- and -ful modify it.','un | help | ful')
add(1,'Multiple choice','Which part of books expresses plural number?','s',['book','boo','The whole sentence'],'Morpheme','The suffix -s adds grammatical information meaning more than one.','cat + s → cats')
add(1,'True / False','A morpheme can carry grammatical information.','True',['False'],'Morpheme','A morpheme need not name an object; it can mark grammar.','-ed in played marks a past/participle form.')
add(1,'True / False','Every word has both a prefix and a suffix.','False',['True'],'Root, prefix, and suffix','A word can consist of a root alone or only one kind of affix.','book has no prefix; books has a suffix.')
add(1,'Identify the Concept','Name the meaningful piece added before a root.','Prefix',['Suffix','Paradigm','Chunk'],'Root, prefix, and suffix','Prefixes occur before the root.','re- in replaying means again.')
add(1,'Identify the Concept','Name the smallest unit carrying meaning or grammar.','Morpheme',['Sentence','Probability','State'],'Morpheme','Morphemes are meaningful or grammatical building blocks.','book and -s are morphemes in books.')
add(1,'Practical scenario','A search for play football misses Sara is playing football. What helps?','Recognize related word forms',['Treat every spelling as unrelated','Label football as a date','Use capitalization only'],'Why morphology matters','Morphological analysis can connect playing with play.','playing → play + ing')

add(2,'Multiple choice','Which change is inflection?','play → played',['teach → teacher','happy → happiness','care → careless'],'Inflection','The same basic verb receives grammatical information.','book → books is another inflection.')
add(2,'Multiple choice','Which change creates a noun from an adjective?','happy → happiness',['book → books','play → playing','walk → walked'],'Derivation','-ness creates a related noun naming a state.','happy is an adjective; happiness is a noun.')
add(2,'Multiple choice','What is the missing form: go, goes, __, going?','went',['goed','goinged','gos'],'Regular and irregular forms','go has an irregular past form.','walk → walked follows a regular pattern; go → went does not.')
add(2,'True / False','Derivation must always change grammatical category.','False',['True'],'Derivation','Derivation may change category, but does not have to.','happy → unhappy: both are adjectives.')
add(2,'True / False','All languages form plurals by adding English -s.','False',['True'],'Morphological diversity','Languages use different endings or internal patterns.','Arabic kitāb → kutub changes the internal pattern.')
add(2,'Identify the Concept','Name an organized set such as play, plays, played, playing.','Morphological paradigm',['Named entity','Random field','Prefix'],'Morphological paradigm','The forms are organized by their grammatical functions.','walk, walks, walked, walking form another paradigm.')
add(2,'Identify the Concept','Name the idea that languages express word information differently.','Morphological diversity',['Argmax','Shallow parsing','Generation'],'Morphological diversity','One language’s word rules do not cover every language.','English book/books; German Buch/Bücher.')
add(2,'Practical scenario','A program treats teacher as just the past form of teach. What should you explain?','Teacher is a derived noun',['Teacher is a plural verb','All suffixes mean past','Teacher has no relationship to teach'],'Derivation','teach → teacher creates a related lexical item and changes verb to noun.','play → played keeps the same basic verb.')

add(3,'Multiple choice','Which path does the tiny play FSM reject?','START → play → xyz',['START → play → s → FINAL','START → play → ed → FINAL','START → play → ing → FINAL'],'Finite-State Machine','xyz is not an allowed transition in this machine.','play + ed is accepted as played.')
add(3,'Multiple choice','What is morphological analysis?','Word → information',['Information → word','Labels → news articles','A capital → a person'],'Morphological analysis','Analysis starts with a surface word and finds its structure or features.','books → book + s, plural')
add(3,'Multiple choice','What does automatic morphology learning use to find patterns?','Examples and data',['Only hand-written rules','Only one capitalization rule','Random answers'],'Automatic morphology learning','Repeated patterns in data can suggest word-building rules.','play/played and walk/walked suggest -ed.')
add(3,'True / False','An FSM has a finite set of states and allowed transitions.','True',['False'],'Finite-State Machine','Its structure limits which paths are accepted.','A final state accepts play + ing.')
add(3,'True / False','Finite-state methods can never handle irregular words.','False',['True'],'Finite-State Morphology','Suitable lexical information and rules can represent irregular mappings.','A lexicon can map go + past to went.')
add(3,'Identify the Concept','Name the task that turns root play plus past into played.','Morphological generation',['Morphological analysis','NER','Chunking'],'Morphological generation','Generation builds a word from supplied information.','book + plural → books')
add(3,'Identify the Concept','Name a permitted move from one FSM state to another.','Transition',['Entity','Probability','Corpus'],'Finite-State Machine','A transition is an allowed step in the machine.','The -ed transition leads toward acceptance.')
add(3,'Practical scenario','Your learned add-ed pattern produces goed. What should you conclude?','The pattern needs irregular lexical information or richer data',['All past forms are wrong','went has the suffix ed','Learning guarantees correctness'],'Rule-based vs automatic learning','A pattern learned from regular examples can overgeneralize.','go → went is an exception to simple concatenation.')

add(4,'Multiple choice','Which phrase is an NP in the slide sentence?','The smart student',['completed','on','quickly'],'Shallow parsing / chunking','The group acts as a noun phrase.','the difficult project is the other NP.')
add(4,'Multiple choice','What label fits Monday in Sara joined Microsoft on Monday?','DATE',['PERSON','ORGANIZATION','LOCATION'],'Named Entity Recognition','Monday names a day and provides temporal information.','Dubai is a LOCATION in the course example.')
add(4,'Multiple choice','What does O mean in entity labeling?','Outside an entity',['Organization','Object noun','Only a person'],'O and entity sequences','O labels tokens outside the chosen entity categories.','works and at receive O in Ahmed works at ABC Bank.')
add(4,'True / False','Shallow parsing requires a full deep grammatical analysis.','False',['True'],'Shallow parsing / chunking','Chunking finds useful groups without building a complete deep parse.','[The smart student] [completed] [the difficult project]')
add(4,'True / False','The same spelling can receive different NER labels in different contexts.','True',['False'],'Context and ambiguity','Context helps distinguish the meaning of an ambiguous name.','Jordan is a location after travelled to, a person before submitted.')
add(4,'Identify the Concept','Name the task that labels Sara as PERSON and Microsoft as ORGANIZATION.','Named Entity Recognition',['Inflection','Generation','Argmax'],'Named Entity Recognition','NER extracts and categorizes named information.','Dubai → LOCATION')
add(4,'Identify the Concept','Name the task that groups words into NP and VP chunks.','Shallow parsing',['Morphological diversity','Maximum Entropy','Derivation'],'Shallow parsing / chunking','Chunking groups related words by phrase type.','completed is the VP in the slide example.')
add(4,'Practical scenario','Apple opened an office. I ate an apple. Why do labels differ?','Context distinguishes the company from fruit',['Every apple is an organization','Only word length matters','O means organization'],'Context and ambiguity','A company name is an entity; an ordinary fruit mention is not a named entity here.','Jordan can similarly name a person or country.')

add(5,'Multiple choice','Why does capitalized word → PERSON fail on Dubai?','Capitalization does not determine entity type',['Dubai is not capitalized','Every place is a person','Rules cannot be executed'],'Limits of simple rules','Many places and organizations are capitalized too.','Microsoft is an organization, not a person.')
add(5,'Multiple choice','Person .05, Organization .05, Location .90: what does argmax return?','Location',['0.05','Person','All labels equally'],'Argmax','Location has the greatest probability; argmax selects its label.','With ORG .90, argmax would select Organization.')
add(5,'Multiple choice','What does a CRF add to this lesson’s standalone local classifier?','Relationships between neighboring labels',['A guarantee of perfect labels','Only capitalization','Removal of all features'],'CRF and sequence labeling','A CRF selects a sequence using input features and label dependencies.','New York University can be labeled as one organization.')
add(5,'True / False','Displayed probabilities in this website come from a trained Maximum Entropy model.','False',['True'],'Maximum Entropy model','The probability controls are explicitly an educational simulation.','0.05, 0.05, 0.90 illustrates uncertainty and selection.')
add(5,'True / False','A random field models relationships among variables.','True',['False'],'Random fields','Variables can be connected rather than treated independently.','Neighboring entity-label variables in a sequence can interact.')
add(5,'Identify the Concept','Name an input clue such as previous word = to.','Feature',['Suffix','Final state','Paradigm'],'Features','A feature supplies evidence for a model decision.','Capitalized = Yes is another feature for Dubai.')
add(5,'Identify the Concept','Name the classifier that combines weighted features to produce label probabilities.','Maximum Entropy model',['FSM recognizer','Morpheme','Noun phrase'],'Maximum Entropy model','The classifier uses evidence to estimate probabilities over labels.','Dubai can have a high illustrative Location probability.')
add(5,'Practical scenario','A local system labels New, York, University as unrelated O tokens. What can help?','Joint sequence labeling with context and label relationships',['Always label every capitalized token PERSON','Delete neighboring words','Use only the last letter'],'CRF and sequence labeling','The words together name an organization; sequence modeling can use that relationship.','Ahmed/PER works/O at/O New/ORG York/ORG University/ORG')

# Four questions per part: two MCQ, one T/F, one practical scenario.
FINAL_QUESTIONS = []
for part in range(1, 6):
    part_questions = [q for q in QUESTIONS if q['part'] == part]
    multiple_choice = [q for q in part_questions if q['kind'] == 'Multiple choice']
    true_false = next(q for q in part_questions if q['kind'] == 'True / False')
    scenario = next(q for q in part_questions if q['kind'] == 'Practical scenario')
    FINAL_QUESTIONS.extend(multiple_choice[:2] + [true_false, scenario])


def grade(questions, answers):
    results = {p: {'correct': 0, 'total': 0} for p in range(1,6)}
    review = set()
    score = 0
    for q in questions:
        correct = answers.get(q['id']) == q['answer']
        score += int(correct)
        results[q['part']]['total'] += 1
        results[q['part']]['correct'] += int(correct)
        if not correct:
            review.add((q['part'], q['concept']))
    return score, results, sorted(review)
