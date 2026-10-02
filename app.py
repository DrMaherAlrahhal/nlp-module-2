"""CSE447 Module 2 interactive teaching laboratory.

Run: streamlit run app.py
"""
import json
from html import escape
import streamlit as st
import activities as lab
import ui
from content import PARTS, CONCEPTS, CODING_TASKS
from questions import QUESTIONS, FINAL_QUESTIONS, grade

st.set_page_config(page_title='Module 2 · NLP Laboratory', page_icon='🔬', layout='wide')
ui.style()
PAGES = ['Home'] + [f'Part {p} – {v[1]}' for p,v in PARTS.items()] + ['Practice Lab','Quiz Center','Final Module Quiz']
SECTIONS = ['Learn','Examples','Try It Yourself','Interactive Demo','Quick Check','Quiz']
st.session_state.setdefault('completed', set())
st.session_state.setdefault('attempted', {})


def navigate(page):
    st.session_state['page'] = page


def home():
    ui.hero('CSE447 · Introduction to Natural Language Processing', 'From Words to Useful Information',
            'Module 2 · Words and Word Forms. Make a prediction. Test an idea. Discover how computers turn words into useful information.',
            ['5 connected parts','Learn by experimenting','Instructor + student workspace'])
    ui.path(['WORD','WORD STRUCTURE','WORD FORMS','COMPUTER PROCESSING','INFORMATION EXTRACTION','NLP DECISION'])
    left,right = st.columns([3,1])
    with left:
        st.subheader('Your learning journey')
        st.write('Begin with one word. Finish with a decision about a whole sentence.')
    with right:
        st.button('Start exploring →', type='primary', on_click=navigate, args=(PAGES[1],), width='stretch')
    for ids in [(1,2,3),(4,5)]:
        for col,p in zip(st.columns(len(ids)),ids):
            name, short, color, question, slides = PARTS[p]
            with col:
                st.markdown(f'<article class="learning-card" style="--accent:{color}"><div class="part-number">PART {p:02}</div><h3>{escape(name)}</h3><p>{escape(question)}</p></article>', unsafe_allow_html=True)
                st.button(f'Explore Part {p} →', key=f'home_{p}', on_click=navigate, args=(PAGES[p],), width='stretch')
        st.write('')
    st.divider()
    a,b,c = st.columns(3)
    with a:
        st.markdown('### Experiment')
        st.write('X-ray a word, break a rule, trace a machine, or label a sentence.')
        st.button('Open Practice Lab', on_click=navigate,args=('Practice Lab',))
    with b:
        st.markdown('### Check your understanding')
        st.write('40 practice questions and a balanced 20-question final quiz.')
        st.button('Open Quiz Center', on_click=navigate,args=('Quiz Center',))
    with c:
        st.markdown('### Teach one idea at a time')
        st.write('Turn on Teaching Mode in the sidebar for a question-first classroom flow.')
    with st.expander('Course source · all 46 slides and image summaries'):
        st.write('Main source: **NLP- Module 2.pptx**. All slide text and image-only diagrams were inspected. The activities reorganize that material into this learning journey.')
        slide = st.number_input('Original slide',1,46,1,key='source_slide')
        data = json.loads((ui.BASE/'source/slides.json').read_text(encoding='utf-8'))
        text = data[slide-1]['text']
        if text:
            st.text(text)
        images = {2:2,9:3,17:4,20:5,22:6,28:7,34:8,36:9,44:10,46:11}
        if slide in images:
            st.image(str(ui.BASE/f'source/image{images[slide]}.png'),caption=f'Original slide {slide} image',width='stretch')
        st.caption('Original images preserve their source wording. The lessons correct the plays/plural typo, explain German umlaut and Hindi case, and distinguish ing-forms from their contextual uses.')
        st.download_button('Download slide-to-activity map', (ui.BASE/'DEVELOPMENT_PLAN.md').read_text(encoding='utf-8'), 'Module2_Content_Map.md', 'text/markdown')


def lesson(part):
    name,short,color,question,slides = PARTS[part]
    ui.hero(f'Part {part:02} · Slides {slides}',name,question)
    section = st.radio('Learning workspace', SECTIONS, horizontal=True, key=f'section_{part}',label_visibility='collapsed')
    concepts = [c for c in CONCEPTS if c['part']==part]
    if section == 'Learn':
        names = [c['name'] for c in concepts]
        selected = st.selectbox('Choose a concept',names,key=f'concept_{part}')
        concept = concepts[names.index(selected)]
        ui.prompt(concept['question'])
        st.caption('THINK · '+concept['think'])
        st.text_input('Your prediction or discussion notes',key=f'prediction_{part}_{selected}')
        ui.reveal('Reveal Concept',f'reveal_{part}_{selected}',concept['explanation'])
        st.write('Use Examples or Interactive Demo to test the idea.')
    elif section == 'Examples':
        for c in concepts:
            with st.expander(c['name'],expanded=False):
                st.write(c['example'])
                st.caption(c['explanation'])
        if part == 2:
            st.table([{'Inflection':'Same basic word + grammatical change','Derivation':'New related word; category may change'},
                      {'Inflection':'play → played','Derivation':'teach → teacher'},
                      {'Inflection':'book → books','Derivation':'happy → happiness'}])
            lab.diversity('examples_languages')
        elif part == 4:
            st.table([{'Chunking':'Which words belong together?','NER':'What named things appear?'},
                      {'Chunking':'the smart student → NP','NER':'Sara → PERSON'},
                      {'Chunking':'Phrase structure','NER':'Entity categories'}])
            st.write('Also try: **The new AI system analyzed the medical report.** and **Prof. Ahmed presented his research in Abu Dhabi.** in the Sentence Analyzer.')
        elif part == 5:
            st.table([{'Maximum Entropy':'Features → probabilities → one label','CRF':'Features + neighboring labels → label sequence'},
                      {'Maximum Entropy':'Dubai → Location','CRF':'New York University → Organization'}])
    elif section == 'Try It Yourself':
        lab.try_it(part,f'try_{part}')
    elif section == 'Interactive Demo':
        lab.interactive(part,f'demo_{part}')
    elif section == 'Quick Check':
        q = next(q for q in QUESTIONS if q['part']==part and q['kind']=='Practical scenario')
        ui.question(q,f'quick_{part}')
    else:
        st.subheader(f'Part {part} practice quiz')
        bank = [q for q in QUESTIONS if q['part']==part]
        selected = st.selectbox('Question',range(len(bank)),format_func=lambda i:f'{i+1}. {bank[i]["kind"]}: {bank[i]["prompt"]}',key=f'part_quiz_{part}')
        ui.question(bank[selected],f'partquiz_{bank[selected]["id"]}')
        correct = sum(st.session_state['attempted'].get(q['id'],False) for q in bank)
        st.caption(f'{correct} / {len(bank)} questions answered correctly in this session.')
    st.divider()
    with st.expander(f'Build it yourself · coding activity from Part {part}'):
        st.write('Use a coding assistant such as Antigravity, or implement the change yourself. Keep extending the same project as the slides propose.')
        st.code(CODING_TASKS[part], language=None, wrap_lines=True)
        st.caption('After each upgrade: test a regular example, an irregular example, and an unknown input. Explain the new functions in your own words.')
    a,b = st.columns([2,1])
    with a:
        st.caption('Progress is self-confirmed and lasts for this browser session. Mark the part complete after trying its activities and checks.')
        if st.button('✓ Mark this part complete',key=f'complete_{part}'):
            st.session_state['completed'].add(part)
            st.rerun()
    with b:
        target = PAGES[part+1] if part < 5 else 'Final Module Quiz'
        st.button('Continue →',key=f'next_{part}',on_click=navigate,args=(target,),width='stretch')


def practice():
    ui.hero('Practice Lab','Try it. Break it. Explain it.','Return to any experiment and change the inputs. Every output has a method you can inspect.')
    experiments = {'Word X-Ray':lab.xray,'Word structure challenges':lab.structure_challenges,
                  'Search experiment':lab.search_demo,'Inflection or Derivation':lab.classify,
                  'Word Family Generator':lab.family_demo,'Missing forms':lab.missing_words,
                  'Language diversity':lab.diversity,'Finite-State Machine':lab.fsm_demo,
                  'Analysis and Generation':lab.morphology_modes,'Human word machine':lab.human_machine,
                  'Learn a pattern':lab.learning_demo,'Sentence Analyzer':lab.sentence_analyzer,
                  'Find the Entities':lab.find_entities,'Context and ambiguity':lab.ambiguity,
                  'Break the capitalization rule':lab.rule_failure,'Maximum Entropy simulation':lab.decision_demo,
                  'Sequence labeling':lab.sequence_demo}
    selected = st.selectbox('Choose an experiment',list(experiments),key='experiment')
    experiments[selected]('lab_'+str(list(experiments).index(selected)))


def quiz_center():
    ui.hero('Quiz Center','Make your prediction','40 questions across all five parts. Submit an answer to see the concept, explanation, and a small example.')
    a,b,c,d = st.columns(4)
    for col,value,label in [(a,15,'Multiple choice'),(b,10,'True / False'),(c,10,'Identify the Concept'),(d,5,'Practical scenarios')]:
        col.metric(label,value)
    a,b = st.columns(2)
    part = a.selectbox('Part',['All parts']+[str(p) for p in PARTS],key='quiz_part')
    kind = b.selectbox('Question type',['All types','Multiple choice','True / False','Identify the Concept','Practical scenario'],key='quiz_kind')
    bank = [q for q in QUESTIONS if (part=='All parts' or q['part']==int(part)) and (kind=='All types' or q['kind']==kind)]
    chosen = st.selectbox('Choose a question', [q['id'] for q in bank],format_func=lambda id:next(f'Part {q["part"]} · {q["prompt"]}' for q in bank if q['id']==id), key='quiz_question_'+part+kind)
    q = next(q for q in bank if q['id']==chosen)
    ui.question(q,'center_'+q['id'])
    correct = sum(st.session_state['attempted'].get(q['id'],False) for q in QUESTIONS)
    st.progress(correct/len(QUESTIONS),text=f'{correct} / 40 practice questions currently correct')
    st.caption('Practice allows retries. The final quiz records a separate submitted attempt.')


def final_quiz():
    ui.hero('Final Module Quiz','Bring the journey together','20 questions. Four from each part. Complete every question, then submit to see your score and topics to review.')
    with st.form('final_form'):
        answers = {}
        for part in PARTS:
            st.subheader(f'Part {part} · {PARTS[part][1]}')
            for q in [q for q in FINAL_QUESTIONS if q['part']==part]:
                answers[q['id']] = st.radio(q['prompt'],q['choices'],index=None,key='final_'+q['id'])
        submitted = st.form_submit_button('Submit final quiz',type='primary')
    if submitted:
        missing = sum(v is None for v in answers.values())
        if missing:
            st.warning(f'Answer all 20 questions before submitting. {missing} still unanswered.')
        else:
            st.session_state['final_result'] = answers.copy()
    if 'final_result' in st.session_state:
        recorded = st.session_state['final_result']
        score, breakdown, review = grade(FINAL_QUESTIONS,recorded)
        st.subheader('Your submitted result')
        st.caption('This report reflects the last submitted attempt. Editing choices does not change the score until you submit again.')
        a,b = st.columns(2)
        a.metric('Score',f'{score} / 20')
        b.metric('Percentage',f'{score/20:.0%}')
        for col,(part,result) in zip(st.columns(5),breakdown.items()):
            col.metric(f'Part {part}',f'{result["correct"]} / {result["total"]}')
        st.subheader('Topics to Review')
        if review:
            for part,concept in review:
                st.write(f'**Part {part}:** {concept}')
        else:
            st.success('All five parts answered correctly. Try explaining a failure case to someone else.')
        for q in FINAL_QUESTIONS:
            with st.expander(('✓ ' if recorded[q['id']]==q['answer'] else '↻ ')+q['prompt']):
                st.write('Your submitted answer: '+recorded[q['id']])
                ui.feedback(q,recorded[q['id']])
        report = {'score':score,'total':20,'percentage':score*5,'parts':breakdown,'topics_to_review':review}
        st.download_button('Download result',json.dumps(report,indent=2),'module2_result.json','application/json')


def teaching_demo(concept,key):
    name = concept['name']
    if name == 'Morphological generation':
        st.session_state.setdefault(key+'_mode', 'Morphological Generation')
    mapping = {
        'Why morphology matters':lab.search_demo,'Inflection':lab.classify,'Derivation':lab.classify,
        'Morphological diversity':lab.diversity,'Morphological paradigm':lab.family_demo,
        'Regular and irregular forms':lab.missing_words,'Finite-State Machine':lab.fsm_demo,
        'Finite-State Morphology':lab.fsm_demo,'Morphological analysis':lab.morphology_modes,
        'Morphological generation':lab.morphology_modes,'Automatic morphology learning':lab.learning_demo,
        'Rule-based vs automatic learning':lab.learning_demo,'Context and ambiguity':lab.ambiguity,
        'Limits of simple rules':lab.rule_failure,'Random fields':lab.sequence_demo,
        'CRF and sequence labeling':lab.sequence_demo,'Maximum Entropy vs CRF':lab.sequence_demo,
    }
    mapping.get(name,lab.DEMOS[concept['part']])(key)


def teaching():
    st.markdown('<div class="eyebrow">Instructor workspace · Teaching Mode</div>',unsafe_allow_html=True)
    part = st.selectbox('Teaching part',list(PARTS),format_func=lambda p:f'Part {p} – {PARTS[p][1]}',key='teach_part')
    concepts = [c for c in CONCEPTS if c['part']==part]
    index = st.selectbox('Discussion question',range(len(concepts)),format_func=lambda i:concepts[i]['question'],key=f'teach_concept_{part}')
    concept = concepts[index]
    key = f'teaching_{part}_{index}'
    step = st.session_state.get(key+'_step',0)
    stages = ['QUESTION','THINK','EXAMPLE','CONCEPT','INTERACTIVE DEMO','CHECK']
    st.progress((step+1)/6,text=f'Step {step+1} of 6 · {stages[step]}')
    st.markdown(f'<div class="stage">{stages[step]}</div>',unsafe_allow_html=True)
    ui.prompt(concept['question'])
    if step == 1:
        st.write(concept['think'])
        st.text_area('Class predictions',key=key+'_notes',placeholder='Discuss before moving on.')
    elif step == 2:
        # Reveal is deliberate; the step does not expose the example answer by itself.
        ui.reveal('Try Example',key+'_example',concept['example'])
    elif step == 3:
        ui.reveal('Reveal Concept',key+'_concept',concept['name']+' — '+concept['explanation'])
    elif step == 4:
        teaching_demo(concept,key+'_demo')
    elif step == 5:
        st.write('Explain this concept in your own words, then apply it to one new example.')
        st.text_area('Student explanation',key=key+'_explanation')
        ui.reveal('Show Answer',key+'_check',concept['explanation']+' Example: '+concept['example'])
    a,b,c = st.columns(3)
    if a.button('Previous Step',key=key+'_back',disabled=step==0):
        st.session_state[key+'_step'] = step-1
        st.rerun()
    if b.button('Next Step',key=key+'_next',disabled=step==5,type='primary'):
        st.session_state[key+'_step'] = step+1
        st.rerun()
    if c.button('Restart concept',key=key+'_restart'):
        for state_key in list(st.session_state):
            if state_key.startswith(key):
                del st.session_state[state_key]
        st.rerun()
    st.caption('Choose the next discussion question above when the class is ready. Earlier stages stay hidden on this screen.')


with st.sidebar:
    st.markdown('## NLP Laboratory')
    st.caption('CSE447 / MODULE 02')
    teaching_on = st.toggle('Teaching Mode',key='teaching_mode')
    page = st.radio('Navigate',PAGES,key='page')
    if teaching_on:
        st.caption('Teaching Mode takes over the main screen. Turn it off to return to normal navigation.')
    st.divider()
    st.markdown('**Module 2 Progress**')
    st.progress(len(st.session_state['completed'])/5)
    for part in PARTS:
        st.write(f'Part {part} '+('✓' if part in st.session_state['completed'] else '…'))
    st.caption('Session progress · self-confirmed completion')
    if st.button('Reset completion marks'):
        st.session_state['completed'] = set()
        st.rerun()

if teaching_on:
    teaching()
elif page == 'Home':
    home()
elif page.startswith('Part '):
    lesson(int(page[5]))
elif page == 'Practice Lab':
    practice()
elif page == 'Quiz Center':
    quiz_center()
else:
    final_quiz()

st.markdown('<div class="footer">CSE447 · Module 2 · Based on NLP- Module 2.pptx<br>Classroom demonstrations use small, transparent rules. No trained NLP model or external API is required.</div>',unsafe_allow_html=True)
