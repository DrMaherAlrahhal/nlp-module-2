"""Interactive experiments reused by lessons, Practice Lab, and Teaching Mode."""
from html import escape
import streamlit as st
import nlp_tools as nlp
import ui
from questions import QUESTIONS


def xray(key):
    st.subheader('Word X-Ray')
    st.caption('Educational dictionary and rules. Try the slide examples; unknown words are not guessed.')
    word = st.text_input('Enter a word', 'unhelpful', key=key+'_word', max_chars=80)
    if st.button('X-ray this word', key=key+'_run', type='primary'):
        st.session_state[key+'_result'] = (word, nlp.analyze(word))
    if key+'_result' in st.session_state:
        original, result = st.session_state[key+'_result']
        if result:
            ui.decomposition(result)
        else:
            st.warning(f'No supported analysis for “{original}”. Try played, books, unhappiness, teachers, replaying, careless, or unfriendliness.')
    with st.expander('What can this small system analyze?'):
        st.write('Verb paradigms: ' + ', '.join(nlp.VERBS))
        st.write('Derived examples: ' + ', '.join(nlp.SPECIAL))
        st.write('Nouns and plurals: ' + ', '.join(sorted(nlp.NOUNS)))


def search_demo(key):
    st.subheader('Can the search engine find it?')
    st.write('Document: **Sara is playing football.**')
    st.write('Search: **play football**')
    mode = st.radio('Matching strategy', ['Exact words', 'Recognize word forms'], horizontal=True, key=key+'_mode')
    if st.button('Run search', key=key+'_run'):
        if mode == 'Exact words':
            st.error('Missed: play and playing are different character strings.')
        else:
            st.success('Found: playing → play + ing connects the document to the query.')
        st.caption('This miniature example matches words; it is not a full search engine.')


def structure_challenges(key):
    st.subheader('Your turn: look inside the word')
    for word in ['unhappy','teachers','replaying','careless','unfriendliness']:
        with st.expander(word):
            st.text_input('Your decomposition', key=key+'_'+word+'_guess', placeholder='prefix + root + suffix')
            if st.button('Show Answer', key=key+'_'+word+'_show'):
                st.session_state[key+'_'+word+'_shown'] = True
            if st.session_state.get(key+'_'+word+'_shown'):
                ui.decomposition(nlp.analyze(word))
    st.caption('A decomposition can contain both derivation and inflection, as in teach + er + s.')


def classify(key):
    st.subheader('Inflection or Derivation?')
    word = st.selectbox('Choose a word', ['played','teacher','books','happiness','playing','careless'], key=key+'_word')
    result = nlp.analyze(word)
    q = dict(prompt=f'{word}: which kind of change?', choices=['Inflection','Derivation'], answer=result['kind'],
             concept=result['kind'], why=result['info'], example=f"{result['root']} → {word}", id='classify_'+word)
    ui.question(q, key+'_'+word)


def family_demo(key):
    st.subheader('Word Family Generator')
    root = st.text_input('Base word', 'play', key=key+'_root', max_chars=60)
    if st.button('Generate family', key=key+'_run'):
        forms = nlp.family(root)
        if forms:
            ui.path(list(forms.values()))
            st.table([{'Form': k, 'Word': v} for k,v in forms.items()])
            if root.strip().lower() == 'go':
                st.info('went comes from our irregular-word lookup, not the add-ed rule.')
        else:
            st.warning('This small vocabulary supports play, walk, talk, work, jump, go, teach, create, use, and the lesson nouns such as book.')


def missing_words(key):
    st.subheader('Can you predict the missing form?')
    for i, (label, answer, reason) in enumerate([
        ('talk → talks → talked → ?', 'talking', 'The ing-form uses talk + ing.'),
        ('work → works → ? → working', 'worked', 'The regular past form uses work + ed.'),
        ('go → goes → ? → going', 'went', 'This irregular past form cannot be found by adding -ed.')]):
        ui.free_check(label, answer, reason, key+str(i))


def diversity(key):
    st.subheader('One language’s rule is not everyone’s rule')
    data = {
        'English': ('book → books', 'An ending -s marks this plural.'),
        'Arabic': ('kitāb → kutub', 'This broken plural changes the internal pattern.'),
        'German': ('ein Buch → zwei Bücher', 'One book → two books. Both an umlaut and the ending -er change the form.'),
        'Hindi': ('laṛkā → laṛke / laṛkõ', 'laṛke is the direct plural; laṛkõ is the oblique plural. The slide’s larka/larkon example also involves case, not just adding an ending.'),
        'Turkish': ('ev → evler', 'house → houses. This example adds -ler; other words can take -lar because of vowel harmony.'),
    }
    language = st.selectbox('Choose a language from the slides', list(data), key=key+'_language')
    ui.prompt('Would adding English -s give the correct form here?')
    ui.reveal('Show example', key+'_'+language, ' — '.join(data[language]))
    st.caption('These are individual examples, not complete descriptions of each language.')


def fsm_demo(key):
    st.subheader('The finite-state word machine')
    suffix = st.selectbox('Choose a transition', ['(none)','s','ed','ing','xyz'], key=key+'_suffix')
    chosen = '' if suffix == '(none)' else suffix
    branches = ''.join(f'<div class="branch {"active" if s == suffix else ""}">{escape(s)}<br>↓<br>FINAL</div>' for s in ['(none)','s','ed','ing'])
    st.markdown(f'<div class="fsm"><span class="state">START</span><div>↓</div><span class="state">play</span><div>↙ ↓ ↓ ↘</div><div class="branches">{branches}</div></div>', unsafe_allow_html=True)
    st.caption('States are stages in the machine; transitions are allowed moves. This is a simplified word-building diagram.')
    if st.button('Follow the path', key=key+'_run', type='primary'):
        value = nlp.fsm(chosen)
        ui.path(['START','play',suffix] + (['FINAL'] if value else ['REJECTED']))
        if value:
            st.success('Accepted · Output = ' + value)
        else:
            st.error('REJECTED: no xyz transition in this simplified machine.')


def morphology_modes(key):
    st.subheader('Word ↔ information')
    mode = st.radio('Mode', ['Morphological Analysis','Morphological Generation'], key=key+'_mode', horizontal=True)
    if mode == 'Morphological Analysis':
        ui.path(['WORD','INFORMATION'])
        word = st.text_input('Word to analyze', 'played', key=key+'_analysis', max_chars=80)
        if st.button('Analyze', key=key+'_analyze'):
            result = nlp.analyze(word)
            if result:
                ui.decomposition(result)
                st.write('**Information:** ' + result['info'])
            else:
                st.warning('No supported analysis. Our small rule system does not know every word.')
    else:
        ui.path(['INFORMATION','WORD'])
        root = st.text_input('Root', 'play', key=key+'_root', max_chars=60)
        form = st.selectbox('Form', nlp.FORMS + ['plural'], key=key+'_form')
        simple = st.toggle('Use only the simple append-a-suffix rule', key=key+'_simple')
        st.caption('Off: use the small vocabulary and irregular lookup. On: deliberately naive concatenation, to expose failures.')
        if st.button('Generate word', key=key+'_generate'):
            result = nlp.generate(root, form, simple)
            if result:
                ui.prompt(result)
                if simple:
                    correct = nlp.generate(root, form)
                    if correct and result != correct:
                        st.error(f'Something went wrong! The simple rule gives {result}; the supported form is {correct}.')
                    st.warning('Naive rule output: it may be wrong, including for unknown roots or inappropriate grammatical forms.')
                else:
                    st.caption('Educational rule system with a small lexical lookup; not a learned model.')
            else:
                st.warning('Unsupported root/form combination. Try play + past, go + past, or book + plural. A noun such as book has no verb past form in this lesson.')


def human_machine(key):
    st.subheader('Human word machine')
    items = {'walk + ed → ?': ('Generation','walked'), 'books → book + s': ('Analysis','book + s'),
             'playing → play + ing': ('Analysis','play + ing'), 'teach + er → ?': ('Generation','teacher'),
             'cars → car + s': ('Analysis','car + s'), 'happy + ness → ?': ('Generation','happiness')}
    selected = st.selectbox('Your input', list(items), key=key+'_item')
    answer, output = items[selected]
    ui.question(dict(prompt='Are we analyzing or generating?',choices=['Analysis','Generation'],answer=answer,
                     concept='Morphological '+answer.lower(),why='Analysis takes a word apart; generation builds a word from information.', example=selected+' · Output: '+output,id='human_'+selected),key+'_'+selected)


def learning_demo(key):
    st.subheader('Discover a pattern, then break it')
    a,b = st.columns(2)
    with a:
        st.markdown('**RULE-BASED**')
        ui.path(['Human gives rules','Computer applies rules'])
    with b:
        st.markdown('**AUTOMATIC LEARNING**')
        ui.path(['Human gives examples','Computer discovers patterns'])
    data = st.text_area('Training examples: one root,form pair per line', 'play,played\nwalk,walked\ntalk,talked\nwork,worked', key=key+'_data', height=130)
    st.text_input('What pattern can the computer discover?', key=key+'_prediction', placeholder='Write your hypothesis before revealing')
    if st.button('Discover repeated endings', key=key+'_discover'):
        endings, exceptions = nlp.discover_endings(data)
        if endings:
            st.table([{'Observed ending': k, 'Count': v} for k,v in endings.items()])
            st.info('A frequent ending is a candidate pattern, not proof that it works for every word. Add play,playing and walk,walking to discover -ing too.')
        else:
            st.warning('No appended endings found. Use root,form pairs such as play,played.')
        if exceptions:
            st.warning('Not explained by simple suffix addition, or not valid pairs: '+ '; '.join(exceptions))
        st.session_state[key+'_endings'] = endings
    if key+'_endings' in st.session_state and st.session_state[key+'_endings']:
        endings = st.session_state[key+'_endings']
        ending = st.selectbox('Choose a discovered ending', list(endings), key=key+'_ending')
        root = st.text_input('Try a new root', 'go', key=key+'_root', max_chars=60)
        if st.button('Test the learned pattern', key=key+'_test'):
            if not root.strip().isalpha() or not root.strip().isascii():
                st.warning('Enter one English word.')
            else:
                output = root.strip().lower() + ending
                ui.prompt(output)
                if root.strip().lower() == 'go' and ending == 'ed':
                    st.error('Something went wrong! go + past = went, not goed.')
                elif root.strip().lower() == 'jump' and ending == 'ed':
                    st.success('jumped works here. Success on one new example does not make the rule universal.')
                st.caption('This is a tiny data-driven suffix counter, not a general morphology learner. It cannot learn internal changes from these rules.')


def sentence_analyzer(key):
    st.subheader('Sentence Analyzer')
    preset = st.selectbox('Choose a slide example, or write your own below', nlp.SENTENCES, key=key+'_preset')
    # A separate text key per preset refreshes its default without overwriting user edits.
    sentence = st.text_area('Sentence', preset, key=key+'_text_'+str(nlp.SENTENCES.index(preset)), max_chars=1000)
    tech = st.checkbox('Include the overview’s optional TECH label for NLP', key=key+'_tech')
    if st.button('Analyze sentence', key=key+'_run', type='primary'):
        st.session_state[key+'_result'] = (sentence, tech)
    if key+'_result' in st.session_state:
        sentence, tech = st.session_state[key+'_result']
        if not sentence.strip():
            st.warning('Enter a sentence first.')
            return
        a,b = st.tabs(['Chunks · which words belong together?', 'Entities · what named things appear?'])
        with a:
            groups, method = nlp.chunks(sentence)
            st.caption(method)
            ui.entities(groups)
            st.write('**NP** = noun phrase. **VP** = verb phrase. **O** here = ungrouped token, not an entity judgment.')
        with b:
            ui.entities(nlp.ner(sentence, tech))
            st.write('**PER** Person · **ORG** Organization · **LOC** Location · **DATE** Date · **O** Outside an entity')
            st.caption('Educational dictionary + context rules, not a trained NER system. Unknown names can incorrectly receive O. Punctuation is shown too; honorifics Dr./Prof. are outside the name in this demo.')
        st.info('Chunking gives phrase groups. NER gives entity categories. These are different questions about the same text.')


def find_entities(key):
    st.subheader('Find the entities')
    st.write('**Dr. Sara joined Microsoft in Dubai on Monday.**')
    labels = [('WHO?', 'Sara'), ('ORGANIZATION?', 'Microsoft'), ('WHERE?', 'Dubai'), ('WHEN?', 'Monday')]
    options = ['Sara','joined','Microsoft','Dubai','Monday']
    with st.form(key):
        guesses = {label: st.selectbox(label,options,index=None,key=key+label) for label,_ in labels}
        submitted = st.form_submit_button('Check entities')
    if submitted:
        if any(v is None for v in guesses.values()):
            st.warning('Make all four predictions first.')
        else:
            for label, answer in labels:
                (st.success if guesses[label] == answer else st.error)(f'{label} '+ ('Correct' if guesses[label] == answer else 'Try Again'))
                st.write(f'**{answer}** answers {label.lower()} in this sentence.')
            st.caption('NER converts selected text into structured information. Example: Dubai → LOCATION.')


def ambiguity(key):
    st.subheader('Same word. Different context.')
    selected = st.radio('Ambiguous word', ['Jordan','Apple / apple'], horizontal=True, key=key+'_word')
    if selected == 'Jordan':
        ui.prompt('I travelled to Jordan. / Jordan submitted the assignment.')
        answer = 'Jordan → LOCATION in the first sentence; Jordan → PERSON in the second. The surrounding context changed.'
    else:
        ui.prompt('Apple opened a new office. / I ate an apple.')
        answer = 'Apple → ORGANIZATION in the first sentence; apple → O in the second, where it names ordinary fruit. Context changed the interpretation.'
    st.text_input('Same word. Why might the label change?', key=key+'_thought_'+selected)
    ui.reveal('Show Answer', key+'_answer_'+selected, answer)


def rule_failure(key):
    st.subheader('Break a one-rule classifier')
    st.code('if word[0].isupper():\n    label = "PERSON"', language='python')
    sentence = st.selectbox('Test sentence', ['Ahmed arrived.','Dubai is beautiful.','Microsoft released a product.'], key=key+'_sentence')
    st.text_input('Why might this rule fail?', key=key+'_thought')
    if st.button('Test capitalization rule', key=key+'_run'):
        word = sentence.split()[0]
        ui.entities([(word,'PER')])
        if word == 'Ahmed':
            st.success('Correct in this example. But one success is not enough.')
        else:
            st.error(f'Incorrect: {word} is a '+ ('LOCATION.' if word == 'Dubai' else 'ORGANIZATION.'))
        st.info('Capital letters occur in many entity types. Combine features and context.')


def decision_demo(key):
    st.subheader('Features → probabilities → one label')
    st.info('EDUCATIONAL SIMULATION: hand-set weights normalized into illustrative probabilities. No trained Maximum Entropy model is running.')
    sentence = st.text_input('Sentence for feature inspection', 'Sara travelled to Dubai.', key=key+'_sentence', max_chars=1000)
    tokens = nlp.tokenize(sentence)
    if not tokens:
        st.warning('Enter a sentence with a token to inspect.')
        return
    default = tokens.index('Dubai') if 'Dubai' in tokens else 0
    index = st.selectbox('Inspect a token', range(len(tokens)), index=default, format_func=lambda i:f'{i+1}: {tokens[i]}', key=key+'_token_'+sentence)
    st.table([{'Feature': k, 'Value': v} for k,v in nlp.features(sentence,index).items()])
    st.caption('Use the sliders to explore uncertainty. Changing the sentence changes features, not learned probabilities: you control the evidence weights below.')
    cols = st.columns(3)
    weights = []
    for col, label, default in zip(cols,['Person','Organization','Location'],[5,5,90]):
        with col:
            weights.append(st.slider(label+' weight', 0,100,default,key=key+'_'+label))
    values = nlp.probabilities(weights)
    if values is None:
        st.warning('At least one weight must be greater than zero.')
        return
    for label, value in zip(['Person','Organization','Location'],values):
        st.progress(value, text=f'{label} = {value:.2f}')
    st.text_input('Predict the argmax label before revealing', key=key+'_prediction')
    if st.button('Show argmax', key=key+'_argmax'):
        winners = [label for label,value in zip(['PERSON','ORGANIZATION','LOCATION'],values) if abs(value-max(values)) < 1e-9]
        ui.path(['ARGMAX', ' / '.join(winners)])
        if len(winners) > 1:
            st.warning('Tie: several labels share the maximum. A real application needs a tie-breaking policy.')
        else:
            st.success(f'{winners[0]} has the highest probability in this simulation.')
    st.caption('This three-class exercise assumes a candidate entity. General NER also needs O and often DATE and other labels.')


def sequence_demo(key):
    st.subheader('Why neighboring labels matter')
    sentence = st.selectbox('Sequence', ['Ahmed works at New York University.','Ahmed works at ABC Bank in Dubai.'], key=key+'_sentence')
    mode = st.radio('View', ['Independent decisions (illustrative failure)','Sequence-aware labels (illustrative result)'], key=key+'_mode')
    items = nlp.ner(sentence)
    if mode.startswith('Independent'):
        items = [(w, 'O' if w in {'New','York','University','ABC','Bank'} else label) for w,label in items]
    ui.entities(items)
    if mode.startswith('Sequence'):
        ui.path(['Features','Neighboring label relationships','Joint label sequence'])
        st.write('A linear-chain CRF scores labels together using input evidence and relationships between neighboring labels. New York University is one organization name.')
    else:
        st.write('These deliberately weak local decisions miss the multiword organization. A stronger local classifier can use context too; CRF additionally models label relationships.')
    st.caption('Illustration only: these are annotated/rule-based labels, not inference from a trained CRF. Repeated ORG labels do not encode full entity boundaries; real systems often add boundary tags.')


DEMOS = {1: xray, 2: family_demo, 3: morphology_modes, 4: sentence_analyzer, 5: decision_demo}


def try_it(part, key):
    if part == 1:
        structure_challenges(key)
    elif part == 2:
        classify(key+'_classify')
        missing_words(key+'_missing')
    elif part == 3:
        human_machine(key+'_human')
        learning_demo(key+'_learn')
    elif part == 4:
        find_entities(key+'_entities')
        ambiguity(key+'_ambiguity')
    else:
        rule_failure(key+'_rule')
        sequence_demo(key+'_sequence')


def interactive(part, key):
    DEMOS[part](key+'_main')
    if part == 1:
        search_demo(key+'_search')
    elif part == 2:
        diversity(key+'_diversity')
    elif part == 3:
        fsm_demo(key+'_fsm')
    elif part == 4:
        st.caption('Try the Jordan and Apple sentence presets to see the limited context rules at work.')
