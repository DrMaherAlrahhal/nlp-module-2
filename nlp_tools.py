"""Small educational rules, deliberately independent of Streamlit.

These are transparent classroom demonstrations, not trained NLP models.
Unknown words are reported instead of inventing confident analyses.
"""
import re
from collections import Counter


VERBS = {
    'play': ['play', 'plays', 'played', 'playing'],
    'walk': ['walk', 'walks', 'walked', 'walking'],
    'talk': ['talk', 'talks', 'talked', 'talking'],
    'work': ['work', 'works', 'worked', 'working'],
    'jump': ['jump', 'jumps', 'jumped', 'jumping'],
    'go': ['go', 'goes', 'went', 'going'],
    'teach': ['teach', 'teaches', 'taught', 'teaching'],
    'create': ['create', 'creates', 'created', 'creating'],
    'use': ['use', 'uses', 'used', 'using'],
}
NOUNS = {'book', 'car', 'cat', 'student', 'project', 'teacher'}
FORMS = ['base', 'third-person singular', 'past', 'ing-form']
SPECIAL = {
    'unhappy': ('un', 'happy', '', 'Derivation', 'un- means not; happy supplies the central meaning.'),
    'happiness': ('', 'happy', 'ness', 'Derivation', '-ness forms a noun naming a state; y changes to i.'),
    'unhappiness': ('un', 'happy', 'ness', 'Derivation', 'un- means not; -ness names a state; happy becomes happi before -ness.'),
    'unhelpful': ('un', 'help', 'ful', 'Derivation', 'helpful means giving help; un- reverses that meaning.'),
    'helpful': ('', 'help', 'ful', 'Derivation', '-ful forms an adjective: giving help.'),
    'teacher': ('', 'teach', 'er', 'Derivation', '-er names a person who teaches. Verb → noun.'),
    'teachers': ('', 'teach', 'er + s', 'Derivation + Inflection', 'teach → teacher creates a noun; teacher → teachers adds plural information.'),
    'replaying': ('re', 'play', 'ing', 'Derivation + Inflection', 're- means again; -ing marks the ing-form.'),
    'replayed': ('re', 'play', 'ed', 'Derivation + Inflection', 're- means again; -ed marks a past/participle form.'),
    'careless': ('', 'care', 'less', 'Derivation', '-less means without; careless is an adjective.'),
    'useful': ('', 'use', 'ful', 'Derivation', '-ful forms an adjective meaning having a use.'),
    'creation': ('', 'create', 'ion', 'Derivation', 'create → creation forms a noun with a spelling change.'),
    'unfriendliness': ('un', 'friend', 'ly + ness', 'Derivation', 'friend → friendly → unfriendly → unfriendliness; -ly forms an adjective here, -ness a noun. y changes to i.'),
}


def analyze(word):
    word = word.strip().lower()
    if not re.fullmatch(r'[a-z]+', word):
        return None
    if word in SPECIAL:
        prefix, root, suffix, kind, info = SPECIAL[word]
        return dict(word=word, prefix=prefix, root=root, suffix=suffix, kind=kind, info=info)
    for root, forms in VERBS.items():
        if word in forms:
            index = forms.index(word)
            suffix = ['', 's', 'ed', 'ing'][index]
            if word in {'went', 'taught'}:
                suffix = 'no separable suffix'
            elif index == 1 and word.endswith('es') and root in {'go', 'teach'}:
                suffix = 'es'
            info = ['base form', 'third-person singular present', 'past form (some forms can also be participles)', 'ing-form; its use depends on context'][index]
            if word in {'went', 'taught'}:
                info = 'irregular past form; found using a small lexical lookup'
            return dict(word=word, prefix='', root=root, suffix=suffix,
                        kind='Base' if index == 0 else 'Inflection', info=info)
    for root in NOUNS:
        if word in {root, root + 's'}:
            plural = word.endswith('s')
            return dict(word=word, prefix='', root=root, suffix='s' if plural else '',
                        kind='Inflection' if plural else 'Base', info='plural: more than one' if plural else 'base noun')
    if word in {'happy', 'help', 'care', 'friend'}:
        return dict(word=word, prefix='', root=word, suffix='', kind='Base', info='central meaning')
    return None


def family(root):
    root = root.strip().lower()
    if root in VERBS:
        return dict(zip(FORMS, VERBS[root]))
    if root in NOUNS:
        return {'base': root, 'plural': root + 's'}
    return None


def generate(root, form, simple=False):
    root = root.strip().lower()
    if not re.fullmatch(r'[a-z]+', root):
        return None
    if simple:
        endings = {'base': '', 'third-person singular': 's', 'past': 'ed', 'ing-form': 'ing', 'plural': 's'}
        return root + endings[form]
    forms = family(root)
    return forms.get(form) if forms else None


def fsm(suffix):
    """A recognizer for this lesson's tiny play paradigm."""
    return 'play' + suffix if suffix in {'', 's', 'ed', 'ing'} else None


def discover_endings(text):
    """Count suffixes in root,form pairs where form starts with root."""
    endings = Counter()
    exceptions = []
    for line in text.splitlines():
        if not line.strip():
            continue
        pieces = [piece.strip().lower() for piece in line.split(',')]
        if len(pieces) != 2 or not all(re.fullmatch('[a-z]+', p) for p in pieces):
            exceptions.append(line.strip())
        elif pieces[1].startswith(pieces[0]) and pieces[1] != pieces[0]:
            endings[pieces[1][len(pieces[0]):]] += 1
        else:
            exceptions.append(line.strip())
    return dict(endings), exceptions


def tokenize(sentence):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+|[^\w\s]", sentence)


PHRASES = {'new york university': 'ORG', 'abc bank': 'ORG',
           'amity university': 'ORG', 'abu dhabi': 'LOC', 'new york': 'LOC'}
LEXICON = {'sara': 'PER', 'ahmed': 'PER', 'microsoft': 'ORG', 'dubai': 'LOC',
           'monday': 'DATE', 'tuesday': 'DATE', 'friday': 'DATE'}
SENTENCES = [
    'The smart student completed the difficult project.',
    'Dr. Sara joined Microsoft in Dubai on Monday.',
    'Ahmed works at ABC Bank in Dubai.',
    'I travelled to Jordan.',
    'Jordan submitted the assignment.',
    'Apple opened a new office.',
    'I ate an apple.',
    'The new AI system analyzed the medical report.',
    'Prof. Ahmed presented his research in Abu Dhabi.',
    'The young researcher presented the new paper.',
    'Dr. Sara is teaching NLP at Amity University in Dubai.',
    'Ahmed works at New York University.',
    'Sara travelled to Dubai.',
    'Ahmed works at Microsoft.',
    'She lives in Dubai.',
]
CHUNKS = {
    SENTENCES[0]: [('The smart student', 'NP'), ('completed', 'VP'), ('the difficult project', 'NP'), ('.', 'O')],
    SENTENCES[7]: [('The new AI system', 'NP'), ('analyzed', 'VP'), ('the medical report', 'NP'), ('.', 'O')],
    SENTENCES[9]: [('The young researcher', 'NP'), ('presented', 'VP'), ('the new paper', 'NP'), ('.', 'O')],
}


def ner(sentence, domain_terms=False):
    """Dictionary + two context rules. O means unrecognized by this demo."""
    tokens = tokenize(sentence)
    lower = [t.lower() for t in tokens]
    labels = ['O'] * len(tokens)
    for phrase, label in sorted(PHRASES.items(), key=lambda x: -len(x[0])):
        words = phrase.split()
        for i in range(len(tokens) - len(words) + 1):
            if lower[i:i + len(words)] == words and all(x == 'O' for x in labels[i:i + len(words)]):
                labels[i:i + len(words)] = [label] * len(words)
    for i, token in enumerate(tokens):
        if labels[i] != 'O':
            continue
        word = lower[i]
        if word == 'jordan':
            labels[i] = 'LOC' if i > 0 and lower[i - 1] in {'to', 'in', 'from'} else 'PER'
        elif word == 'apple':
            labels[i] = 'ORG' if token == 'Apple' and any(t in lower for t in ['opened', 'released', 'joined']) else 'O'
        elif word == 'nlp' and domain_terms:
            labels[i] = 'TECH'
        else:
            labels[i] = LEXICON.get(word, 'O')
    return list(zip(tokens, labels))


def chunks(sentence):
    """Annotated slide examples, then a deliberately small phrase heuristic."""
    sentence = sentence.strip()
    if sentence in CHUNKS:
        return CHUNKS[sentence], 'Annotated example from the slides'
    tokens = tokenize(sentence)
    verbs = {'joined', 'works', 'travelled', 'submitted', 'opened', 'ate', 'presented', 'is', 'teaching', 'lives', 'released', 'arrived'}
    boundaries = {'in', 'on', 'at', 'to', 'from'}
    result, group = [], []
    def flush():
        if group:
            result.append((' '.join(group), 'NP?'))
            group.clear()
    for token in tokens:
        if token.lower() in verbs:
            flush()
            result.append((token, 'VP?'))
        elif token.lower() in boundaries or not token.isalpha():
            flush()
            result.append((token, 'O'))
        else:
            group.append(token)
    flush()
    return result, 'Heuristic guess: ? means uncertain, not a full parser'


def features(sentence, index):
    tokens = tokenize(sentence)
    word = tokens[index]
    return {'Current word': word, 'Previous word': tokens[index - 1] if index else '(start)',
            'Next word': tokens[index + 1] if index + 1 < len(tokens) else '(end)',
            'Capitalized': 'Yes' if word[0].isupper() else 'No',
            'Word shape': 'ALL CAPS' if word.isupper() else 'Title case' if word.istitle() else 'Other',
            'Nearby words': ' '.join(tokens[max(0, index - 3):index] + tokens[index + 1:index + 4])}


def probabilities(weights):
    total = sum(weights)
    return [w / total for w in weights] if total > 0 else None
