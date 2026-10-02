import unittest
from collections import Counter
import nlp_tools as n
from questions import QUESTIONS, FINAL_QUESTIONS, grade


class LogicTests(unittest.TestCase):
    def test_all_morphology_examples(self):
        expected = {'unhappiness':('un','happy','ness'), 'unhelpful':('un','help','ful'),
                    'played':('','play','ed'),'books':('','book','s'),
                    'unhappy':('un','happy',''),'teachers':('','teach','er + s'),
                    'replaying':('re','play','ing'),'careless':('','care','less'),
                    'unfriendliness':('un','friend','ly + ness')}
        for word, parts in expected.items():
            with self.subTest(word=word):
                result = n.analyze(word)
                self.assertEqual(tuple(result[k] for k in ['prefix','root','suffix']),parts)
        for word in ['cats','walking','replayed','happiness','teacher','useful','creation','cars']:
            self.assertIsNotNone(n.analyze(word))
        self.assertEqual(n.analyze(' BOOKS ')['root'],'book')
        for word in ['', 'unknownword', '<script>', 'two words', '123']:
            self.assertIsNone(n.analyze(word))

    def test_generation_and_irregulars(self):
        for root,forms in n.VERBS.items():
            for form,word in zip(n.FORMS,forms):
                self.assertEqual(n.generate(root,form),word)
                self.assertEqual(n.analyze(word)['root'],root)
        self.assertEqual(n.generate('book','plural'),'books')
        self.assertIsNone(n.generate('book','past'))
        self.assertIsNone(n.generate('unknown','past'))
        self.assertIsNone(n.generate('','past',True))
        self.assertEqual(n.generate('go','past',True),'goed')
        self.assertEqual(n.generate('go','past'),'went')
        self.assertIn('lexical',n.analyze('went')['info'])

    def test_fsm_and_data_learning(self):
        for suffix in ['','s','ed','ing']:
            self.assertEqual(n.fsm(suffix),'play'+suffix)
        self.assertIsNone(n.fsm('xyz'))
        counts,exceptions=n.discover_endings('play,played\nwalk,walked\nplay,playing\ngo,went\nbad line')
        self.assertEqual(counts,{'ed':2,'ing':1})
        self.assertEqual(len(exceptions),2)
        self.assertEqual(n.discover_endings(''),({},[]))

    def test_ner_all_slide_examples(self):
        for sentence in n.SENTENCES:
            result=n.ner(sentence)
            self.assertEqual([w for w,_ in result],n.tokenize(sentence))
        self.assertIn(('Jordan','LOC'),n.ner('I travelled to Jordan.'))
        self.assertIn(('Jordan','PER'),n.ner('Jordan submitted the assignment.'))
        self.assertIn(('Apple','ORG'),n.ner('Apple opened a new office.'))
        self.assertIn(('apple','O'),n.ner('I ate an apple.'))
        self.assertEqual([label for _,label in n.ner('Ahmed works at New York University.')],['PER','O','O','ORG','ORG','ORG','O'])
        self.assertEqual([label for _,label in n.ner('Ahmed works at ABC Bank in Dubai.')],['PER','O','O','ORG','ORG','O','LOC','O'])
        self.assertEqual(n.ner('Abu Dhabi'),[('Abu','LOC'),('Dhabi','LOC')])
        self.assertEqual(n.ner('NLP',True),[('NLP','TECH')])
        self.assertEqual(n.ner('NLP'),[('NLP','O')])
        self.assertEqual(n.ner(''),[])

    def test_chunks_and_features(self):
        for sentence,groups in n.CHUNKS.items():
            self.assertEqual(n.chunks(sentence)[0],groups)
        self.assertIn('Heuristic',n.chunks('A new test works.')[1])
        feats=n.features('Sara travelled to Dubai.',3)
        self.assertEqual(feats['Current word'],'Dubai')
        self.assertEqual(feats['Previous word'],'to')
        self.assertEqual(feats['Capitalized'],'Yes')
        self.assertIn('travelled',feats['Nearby words'])
        self.assertEqual(n.probabilities([5,5,90]),[.05,.05,.9])
        self.assertIsNone(n.probabilities([0,0,0]))

    def test_bank_and_scoring(self):
        self.assertEqual(Counter(q['kind'] for q in QUESTIONS),{'Multiple choice':15,'True / False':10,'Identify the Concept':10,'Practical scenario':5})
        self.assertEqual(len({q['id'] for q in QUESTIONS}),40)
        for q in QUESTIONS:
            self.assertIn(q['answer'],q['choices'])
            self.assertTrue(q['why'] and q['example'])
        self.assertEqual(len(FINAL_QUESTIONS),20)
        self.assertEqual(Counter(q['part'] for q in FINAL_QUESTIONS),{1:4,2:4,3:4,4:4,5:4})
        correct={q['id']:q['answer'] for q in FINAL_QUESTIONS}
        score,parts,review=grade(FINAL_QUESTIONS,correct)
        self.assertEqual(score,20)
        self.assertEqual(review,[])
        for q in FINAL_QUESTIONS[:4]:
            correct[q['id']]='wrong'
        score,parts,review=grade(FINAL_QUESTIONS,correct)
        self.assertEqual(score,16)
        self.assertEqual(parts[1]['correct'],0)
        self.assertTrue(all(part==1 for part,_ in review))
        self.assertEqual(grade(FINAL_QUESTIONS,{})[0],0)


if __name__=='__main__':
    unittest.main()
