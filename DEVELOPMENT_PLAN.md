# Module 2 development plan

Main source: `../NLP- Module 2.pptx`, inspected in full before implementation (46 slides, including all 10 slide images). No speaker notes were present.

1. Extract the slide text and preserve the source diagrams; map every slide to learning activities.
2. Build small, readable morphology and sentence-processing functions. Explicitly disclose their limited vocabulary and educational status.
3. Build the home learning path and five parts with Learn, Examples, Try It Yourself, Interactive Demo, Quick Check, and Quiz.
4. Add Practice Lab, 40-question practice bank, balanced 20-question final quiz, session progress, and concept-by-concept Teaching Mode.
5. Test logic, every page, interactive activities, hidden answers, quiz scoring, review recommendations, teaching stages, and input edge cases. Run the server and inspect the browser layout.
6. Deliver installation instructions, coverage map, source notes, and test results.

## Content map

| Slides | Content | Website destination |
|---|---|---|
| 1–2 | Five-part journey; applications; overview examples | Home, five-part path, source gallery |
| 3–7 | happy family; morphology; search play/playing; morphemes; roots/affixes | Part 1 concepts, X-Ray, search experiment |
| 8–9 | Word X-Ray coding prompt; cats/walking/replayed; five challenges; applications | Part 1 activities, coding studio, source summary |
| 10–12 | Inflection vs derivation; play/book/teach/happy; prediction questions | Part 2 concepts, classification activity |
| 13–14 | Diversity and paradigms | Part 2 language comparison, family generator |
| 15–17 | Missing forms, went, upgrade task; care/use/create; multilingual examples | Part 2 challenges, coding studio, source summary |
| 18–22 | States, transitions, FSM acceptance/rejection; finite-state morphology | Part 3 FSM, analysis/generation |
| 23 | Human word machine: walk+ed, books, playing, teach+er, cars, happy+ness | Part 3 direction challenge |
| 24–25 | Cost of manual rules; learning ed/ing from examples | Part 3 pattern discovery lab |
| 26–28 | Incremental coding task; irregular failure; jump/jumped | Part 3 generation and pattern experiments, coding studio |
| 29–32 | Chunks vs entities; NP/VP; 10,000 news articles | Part 4 sentence analyzer and concepts |
| 33–36 | Jordan context; comparison; Apple/apple; AI system/medical report; Prof. Ahmed/Abu Dhabi | Part 4 ambiguity activity, example presets, coding studio |
| 37–41 | Bad capitalization rule; features; Microsoft clues; MaxEnt; probabilities/argmax | Part 5 failure experiment and decision simulator |
| 42–44 | Independent decisions; random fields; CRF; NYU/ABC Bank; comparison | Part 5 sequence demonstration |
| 45–46 | Feature/illustrative probability upgrade; extended features; complete NER decision | Part 5 simulator, coding studio, source summary |

## Accuracy notes

- Slide 17's image labels verb `plays` as plural in one row. The paradigm correctly calls it third-person singular. Use third-person singular consistently.
- German `Buch → Bücher` includes an umlaut and an ending, not just addition of `-er`.
- The Hindi `larka → larkon` image is a simplified transliteration of a singular/direct to plural/oblique contrast. Show `laṛkā → laṛke` (direct plural), and explain `laṛkõ` (oblique plural).
- `happy + ness → happiness` and `friendly + ness → friendliness` require spelling changes. Morpheme displays represent underlying pieces, not always literal character slices.
- `-ing` identifies an ing-form; sentence context determines its exact use. `-ed` may also mark a participle. Avoid claiming isolated forms have only one grammatical use.
- The overview has an optional TECH label for NLP. Preserve this as a domain-specific extension; the core NER exercise uses PER/ORG/LOC/DATE/O.
- Simulated MaxEnt scores and illustrative sequence labels are not outputs of trained MaxEnt or CRF models. Finite-state methods can handle irregulars with appropriate lexical information.

## Architecture

`app.py`: navigation and page composition. `content.py`: course concepts and teaching prompts. `nlp_tools.py`: inspectable educational rules. `activities.py`: reusable interactive experiments. `questions.py`: question bank. `ui.py` + `assets/style.css`: visual presentation. `tests/`: standard-library unittest and Streamlit AppTest checks. `source/`: extracted source evidence.
