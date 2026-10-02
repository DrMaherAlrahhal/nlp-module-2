# From Words to Useful Information

Interactive Python + Streamlit laboratory for **CSE447 – Introduction to Natural Language Processing**, **Module 2 – Words and Word Forms**.

The main source is the instructor's **NLP- Module 2.pptx**. All 46 slides were inspected, including the 10 image-only diagrams/summaries. The application includes a source-slide viewer and a complete [slide-to-activity map](DEVELOPMENT_PLAN.md).

## Install and run

Use Python 3.11 or newer. Tested with Python 3.14.5 and Streamlit 1.64.0 on Windows.

Open a terminal in this project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, normally **http://localhost:8501**.

If PowerShell does not allow activation, use the environment's Python directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

If Streamlit is already installed but the `streamlit` command is not on PATH:

```powershell
python -m streamlit run app.py
```

On macOS/Linux, activate with `source .venv/bin/activate`, then use the same install and `streamlit run app.py` commands. Stop the server with **Ctrl+C**. No API key, model download, or paid service is needed. After installation, the lessons work without an Internet connection.

## Learning and teaching

- **Home:** connected learning journey and original-slide viewer.
- **Five parts:** each has Learn, Examples, Try It Yourself, Interactive Demo, Quick Check, and Quiz.
- **Practice Lab:** 17 experiments covering word decomposition, search, inflection/derivation, paradigms, languages, FSM paths, analysis/generation, pattern discovery, chunking, entities, context, features, probabilities, and sequences.
- **Quiz Center:** 15 multiple-choice, 10 true/false, 10 concept-identification, and 5 practical-scenario questions. Feedback appears after submission, with explanations and examples. Students can retry.
- **Final Module Quiz:** 20 questions, four per part. Answers remain hidden until a complete attempt is submitted. The report contains total score, percentage, part scores, topics to review, and a downloadable JSON result.
- **Teaching Mode:** sidebar switch. Select a part and a discussion question. Follow QUESTION → THINK → EXAMPLE → CONCEPT → INTERACTIVE DEMO → CHECK. Reveal buttons keep answers hidden until the instructor chooses to show them. Restart a concept before presenting it to a new group.
- **Coding activities:** each part retains the deck's incremental “extend the SAME Word X-Ray app” teaching task.

Suggested classroom flow: ask the opening question, collect predictions, try the example, reveal the concept, change an input to expose a limitation, then use the quick check. For example, learn `-ed` from four regular verbs, test `jump`, then test `go`.

Completion marks are **self-confirmed**. Marks, quiz feedback, and scores last for the current Streamlit session; there is no login, database, or permanent student record. A page refresh or new session may reset them. Download final results before leaving. The final report is a snapshot of the last submitted attempt; changing choices does not silently change that score.

## Honest limits of the demos

- **Word X-Ray:** a small explicit lexicon and rules. It supports the course examples, compounds of the taught affixes, nine verb paradigms, and selected nouns. Unknown inputs show an unsupported message. It is not a general morphological analyzer.
- **Word generation:** normal mode uses the small lexicon, including `go → went` and `teach → taught`. The deliberately naive mode appends a suffix and can produce `goed`, `gos`, or other bad forms. This is intentional and labeled.
- **Pattern discovery:** actually counts repeated appended endings in editable `root,form` pairs. It cannot learn internal changes or irregular forms through suffix counting alone.
- **Chunking:** three slide sentences have annotated chunks. Other sentences use a limited heuristic and display `NP?`/`VP?` as uncertain guesses. This is not a full parser.
- **NER:** a dictionary with multiword matching and small Jordan/Apple context rules. Unknown names may incorrectly receive O. This is not a trained NER model. The optional TECH label preserves the deck overview's domain-specific NLP example.
- **Maximum Entropy:** hand-set weights are normalized to illustrate probabilities and argmax. They are **not trained model predictions**, and do not automatically change when sentence features change. All-zero inputs and ties are explicitly handled.
- **CRF:** sequence labels illustrate the concept; no trained CRF runs. The example uses simple entity categories, not BIO boundary encoding.

## Source corrections

The source viewer preserves the original images. Teaching text corrects the slide 17 image's `plays = plural` typo to **third-person singular present**, notes the umlaut in German `Buch → Bücher`, and distinguishes Hindi direct plural `laṛke` from oblique plural `laṛkõ`. Word decomposition uses underlying morphemes, so `happy + ness` requires `y → i`. An isolated `-ing` form is not always a continuous verb; context matters. These adjustments are documented in [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md).

## Files to explore

| File | Purpose |
|---|---|
| `app.py` | Navigation, lessons, teaching stages, quizzes, results |
| `content.py` | 27 short concept cards and slide-derived coding tasks |
| `nlp_tools.py` | Plain Python processing functions, independent of the UI |
| `activities.py` | Reusable interactive experiments |
| `questions.py` | 40 questions, balanced final selection, scoring |
| `ui.py` | Escaped HTML display helpers and feedback controls |
| `assets/style.css` | Colors, responsive cards, diagrams, and typography |
| `.streamlit/config.toml` | Consistent light theme and disabled usage telemetry |
| `source/` | Extracted slide text and original diagram images |
| `tests/` | Functional and Streamlit widget tests |

To add an example, extend the relevant vocabulary/table in `nlp_tools.py`. To add a teaching concept, add a row to `content.py`. Keep predictions and reveals separate. To add a quiz question, supply its answer, explanation, concept, and a small example in `questions.py`.

## Test

```powershell
python -m unittest discover -s tests -v
```

Or produce a clean saved report:

```powershell
python run_tests.py
```

Tests cover all pages and sections, all 46 source slides, all 27 teaching concepts through six stages, the interactive activities, all 40 practice questions with incorrect and correct submissions, incomplete final submissions, 16/20 and 20/20 scoring, topic review, progress, navigation, and input edge cases. See [TEST_REPORT.md](TEST_REPORT.md) for validation and the visual-review limitation.

Streamlit's official references used during implementation: [AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest) and [forms](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form). Course content remains based on the supplied deck.
