"""End-to-end Streamlit widget tests, without a browser or extra dependencies."""
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from content import PARTS,CONCEPTS
from questions import QUESTIONS,FINAL_QUESTIONS
from nlp_tools import SENTENCES

APP = str(Path(__file__).resolve().parents[1]/'app.py')
PAGES = ['Home']+[f'Part {p} – {v[1]}' for p,v in PARTS.items()]+['Practice Lab','Quiz Center','Final Module Quiz']


def click(app,label):
    return next(b for b in app.button if b.label==label).click().run()


class AppTests(unittest.TestCase):
    def setUp(self):
        self.a=AppTest.from_file(APP,default_timeout=15).run()

    def clean(self):
        self.assertEqual([e.message for e in self.a.exception],[])

    def page(self,page):
        self.a.radio(key='page').set_value(page).run()
        self.clean()

    def experiment(self,name):
        self.page('Practice Lab')
        self.a.selectbox(key='experiment').select(name).run()
        self.clean()

    def test_all_pages_sections_concepts_and_sources(self):
        for page in PAGES:
            self.page(page)
        for part in PARTS:
            self.page(PAGES[part])
            for section in ['Learn','Examples','Try It Yourself','Interactive Demo','Quick Check','Quiz']:
                self.a.radio(key=f'section_{part}').set_value(section).run()
                self.clean()
            self.a.radio(key=f'section_{part}').set_value('Learn').run()
            for c in [c for c in CONCEPTS if c['part']==part]:
                self.a.selectbox(key=f'concept_{part}').select(c['name']).run()
                self.assertFalse(self.a.info)
                click(self.a,'Reveal Concept')
                self.clean()
                self.assertTrue(self.a.info)
        self.page('Home')
        for slide in range(1,47):
            self.a.number_input(key='source_slide').set_value(slide).run()
            self.clean()

    def test_xray_search_structure_and_family(self):
        self.experiment('Word X-Ray')
        for word in ['unhelpful','unhappiness','teachers','replaying','unfriendliness','went','','<script>']:
            self.a.text_input(key='lab_0_word').set_value(word).run()
            click(self.a,'X-ray this word')
            self.clean()
        self.assertTrue(self.a.warning)
        self.experiment('Word structure challenges')
        for word in ['unhappy','teachers','replaying','careless','unfriendliness']:
            self.a.button(key=f'lab_1_{word}_show').click().run()
            self.clean()
        self.experiment('Search experiment')
        click(self.a,'Run search')
        self.assertTrue(self.a.error)
        self.a.radio(key='lab_2_mode').set_value('Recognize word forms').run()
        click(self.a,'Run search')
        self.assertTrue(self.a.success)
        self.experiment('Word Family Generator')
        for root in ['play','walk','go','book','unknown','']:
            self.a.text_input(key='lab_4_root').set_value(root).run()
            click(self.a,'Generate family')
            self.clean()

    def test_classification_missing_forms_and_languages(self):
        self.experiment('Inflection or Derivation')
        for word,answer in [('played','Inflection'),('teacher','Derivation'),('books','Inflection'),('happiness','Derivation'),('playing','Inflection'),('careless','Derivation')]:
            self.a.selectbox(key='lab_3_word').select(word).run()
            self.a.radio(key=f'lab_3_{word}_choice').set_value(answer)
            click(self.a,'Submit answer')
            self.assertTrue(self.a.success)
            self.clean()
        self.experiment('Missing forms')
        for i,answer in enumerate(['talking','worked','went']):
            self.a.text_input(key=f'lab_5{i}_value').set_value(answer)
            self.a.button(key=f'FormSubmitter:lab_5{i}-Check answer').click().run()
            self.clean()
        self.assertEqual(len(self.a.success),3)
        self.experiment('Language diversity')
        for language in ['English','Arabic','German','Hindi','Turkish']:
            self.a.selectbox(key='lab_6_language').select(language).run()
            click(self.a,'Show example')
            self.clean()
            self.assertTrue(self.a.info)

    def test_machine_analysis_generation_and_learning(self):
        self.experiment('Finite-State Machine')
        for suffix in ['(none)','s','ed','ing','xyz']:
            self.a.selectbox(key='lab_7_suffix').select(suffix).run()
            click(self.a,'Follow the path')
            self.clean()
            self.assertTrue(self.a.error if suffix=='xyz' else self.a.success)
        self.experiment('Analysis and Generation')
        for word in ['played','playing','books','went','']:
            self.a.text_input(key='lab_8_analysis').set_value(word).run()
            click(self.a,'Analyze')
            self.clean()
        self.a.radio(key='lab_8_mode').set_value('Morphological Generation').run()
        for root,form in [('play','past'),('play','ing-form'),('book','plural'),('go','past'),('book','past'),('','past')]:
            self.a.text_input(key='lab_8_root').set_value(root)
            self.a.selectbox(key='lab_8_form').select(form)
            click(self.a,'Generate word')
            self.clean()
        self.a.text_input(key='lab_8_root').set_value('go')
        self.a.toggle(key='lab_8_simple').set_value(True)
        click(self.a,'Generate word')
        self.assertTrue(self.a.error)
        self.experiment('Human word machine')
        for selected in self.a.selectbox(key='lab_9_item').options:
            self.a.selectbox(key='lab_9_item').select(selected).run()
            answer='Generation' if '?' in selected else 'Analysis'
            next(r for r in self.a.radio if r.label=='Are we analyzing or generating?').set_value(answer)
            click(self.a,'Submit answer')
            self.assertTrue(self.a.success)
        self.experiment('Learn a pattern')
        click(self.a,'Discover repeated endings')
        click(self.a,'Test the learned pattern')
        self.assertTrue(self.a.error)
        self.a.text_input(key='lab_10_root').set_value('jump')
        click(self.a,'Test the learned pattern')
        self.assertTrue(self.a.success)
        for data in ['', 'bad line','go,went','play,playing\nwalk,walking']:
            self.a.text_area(key='lab_10_data').set_value(data)
            click(self.a,'Discover repeated endings')
            self.clean()

    def test_sentences_entities_ambiguity_and_rule_failure(self):
        self.experiment('Sentence Analyzer')
        for sentence in SENTENCES:
            self.a.selectbox(key='lab_11_preset').select(sentence).run()
            click(self.a,'Analyze sentence')
            self.clean()
        self.a.text_area[0].set_value('')
        click(self.a,'Analyze sentence')
        self.assertTrue(self.a.warning)
        self.experiment('Find the Entities')
        click(self.a,'Check entities')
        self.assertTrue(self.a.warning)
        for label,value in [('WHO?','Sara'),('ORGANIZATION?','Microsoft'),('WHERE?','Dubai'),('WHEN?','Monday')]:
            self.a.selectbox(key='lab_12'+label).select(value)
        click(self.a,'Check entities')
        self.assertEqual(len(self.a.success),4)
        self.experiment('Context and ambiguity')
        for word in ['Jordan','Apple / apple']:
            self.a.radio(key='lab_13_word').set_value(word).run()
            self.assertFalse(self.a.info)
            click(self.a,'Show Answer')
            self.assertTrue(self.a.info)
        self.experiment('Break the capitalization rule')
        for sentence in ['Ahmed arrived.','Dubai is beautiful.','Microsoft released a product.']:
            self.a.selectbox(key='lab_14_sentence').select(sentence).run()
            click(self.a,'Test capitalization rule')
            self.clean()
            self.assertTrue(self.a.success if sentence.startswith('Ahmed') else self.a.error)

    def test_probabilities_sequence_and_edge_cases(self):
        self.experiment('Maximum Entropy simulation')
        click(self.a,'Show argmax')
        self.assertIn('LOCATION',self.a.success[0].value)
        for label in ['Person','Organization','Location']:
            self.a.slider(key='lab_15_'+label).set_value(0)
        self.a.run()
        self.assertTrue(self.a.warning)
        for label in ['Person','Organization','Location']:
            self.a.slider(key='lab_15_'+label).set_value(5)
        self.a.run()
        click(self.a,'Show argmax')
        self.assertTrue(any('Tie' in x.value for x in self.a.warning))
        for sentence in ['Ahmed works at Microsoft.','Dr. Sara joined Microsoft in Dubai on Monday.','','<script>alert(1)</script>']:
            self.a.text_input(key='lab_15_sentence').set_value(sentence).run()
            self.clean()
        self.experiment('Sequence labeling')
        for sentence in self.a.selectbox(key='lab_16_sentence').options:
            self.a.selectbox(key='lab_16_sentence').select(sentence).run()
            for mode in self.a.radio(key='lab_16_mode').options:
                self.a.radio(key='lab_16_mode').set_value(mode).run()
                self.clean()

    def test_all_quiz_answers_feedback_and_filters(self):
        self.page('Quiz Center')
        self.assertFalse(self.a.success)
        self.assertFalse(self.a.error)
        for q in QUESTIONS:
            self.a.selectbox(key='quiz_question_All partsAll types').select(q['id']).run()
            wrong=next(c for c in q['choices'] if c!=q['answer'])
            self.a.radio(key='center_'+q['id']+'_choice').set_value(wrong)
            click(self.a,'Submit answer')
            self.assertTrue(self.a.error)
            self.a.radio(key='center_'+q['id']+'_choice').set_value(q['answer'])
            click(self.a,'Submit answer')
            self.assertTrue(self.a.success)
            self.clean()
        for p in range(1,6):
            self.a.selectbox(key='quiz_part').select(str(p)).run()
            for kind in ['Multiple choice','True / False','Identify the Concept','Practical scenario']:
                self.a.selectbox(key='quiz_kind').select(kind).run()
                self.clean()

    def test_final_hidden_answers_incomplete_submission_and_scores(self):
        self.page('Final Module Quiz')
        self.assertEqual(len(self.a.radio),21)  # navigation + 20 questions
        self.assertFalse(self.a.metric)
        click(self.a,'Submit final quiz')
        self.assertTrue(self.a.warning)
        self.assertFalse(self.a.metric)
        for i,q in enumerate(FINAL_QUESTIONS):
            answer=q['answer'] if i>=4 else next(c for c in q['choices'] if c!=q['answer'])
            self.a.radio(key='final_'+q['id']).set_value(answer)
        click(self.a,'Submit final quiz')
        self.assertEqual(self.a.metric[0].value,'16 / 20')
        self.assertEqual(self.a.metric[1].value,'80%')
        self.assertEqual(self.a.metric[2].value,'0 / 4')
        self.page('Home')
        self.page('Final Module Quiz')
        self.assertEqual(self.a.metric[0].value,'16 / 20')
        for q in FINAL_QUESTIONS:
            self.a.radio(key='final_'+q['id']).set_value(q['answer'])
        click(self.a,'Submit final quiz')
        self.assertEqual(self.a.metric[0].value,'20 / 20')
        self.clean()

    def test_teaching_every_concept_and_stage(self):
        self.a.toggle(key='teaching_mode').set_value(True).run()
        for part in PARTS:
            self.a.selectbox(key='teach_part').select(part).run()
            for index,c in enumerate(x for x in CONCEPTS if x['part']==part):
                self.a.selectbox(key=f'teach_concept_{part}').select(index).run()
                self.assertFalse(self.a.info)
                for step in range(6):
                    self.clean()
                    if step==2:
                        click(self.a,'Try Example')
                    elif step==3:
                        click(self.a,'Reveal Concept')
                    elif step==5:
                        click(self.a,'Show Answer')
                    if step<5:
                        click(self.a,'Next Step')
                click(self.a,'Restart concept')
                self.assertFalse(self.a.info)
                self.clean()

    def test_navigation_and_progress(self):
        click(self.a,'Start exploring →')
        self.assertEqual(self.a.radio(key='page').value,PAGES[1])
        for part in PARTS:
            self.page(PAGES[part])
            click(self.a,'✓ Mark this part complete')
        self.assertEqual(self.a.session_state['completed'],{1,2,3,4,5})
        click(self.a,'Continue →')
        self.assertEqual(self.a.radio(key='page').value,'Final Module Quiz')
        click(self.a,'Reset completion marks')
        self.assertEqual(self.a.session_state['completed'],set())


if __name__=='__main__':
    unittest.main()
