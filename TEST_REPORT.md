# Validation

Environment: Windows, Python 3.14.5, Streamlit 1.64.0.

## Automated verification

All 16 test methods passed on the final implementation. They exercise many inputs and UI states, using Python unittest and Streamlit AppTest. The latest full output is in `test-results.txt`:

- All nine navigation destinations and all six sections in each of five parts.
- All 46 original slide entries, including image-only slides.
- All 27 concept reveals and all 27 Teaching Mode flows through six stages, including restart and hidden-answer checks.
- All 17 Practice Lab experiments, including every predefined sentence and all five language examples.
- Word decomposition, spelling changes, irregular lookup, unsupported words, blank inputs, and HTML-like text.
- FSM acceptance for empty/s/ed/ing endings and rejection for xyz.
- Both morphological modes, supported generation forms, deliberately wrong goed, and unsupported root/form combinations.
- Editable suffix discovery, malformed pairs, irregular pairs, successful jumped and failing goed.
- Entity identification, multiword entities, optional TECH label, Jordan and Apple ambiguity, and chunking method disclosures.
- Capitalization-rule successes/failures, probability argmax, zero weights, ties, and sequence views.
- All 40 practice questions: wrong answer feedback followed by correct answer feedback. All part/type filters.
- Final quiz: no result before submission, incomplete submission handling, 16/20 = 80%, correct per-part breakdown, saved result across navigation, and 20/20.
- Review-topic calculation, session completion marks, reset, and continuation navigation.

The server started successfully at `http://127.0.0.1:8501`. The page returned HTTP 200 and `/_stcore/health` returned HTTP 200 with body `ok`. The installed Streamlit CLI reported version 1.64.0. Its executable directory was added only to the verification shell's PATH; the README explains normal virtual-environment installation and the Python-module fallback.

## Visual inspection limitation

The computer/browser tool reported no available browsers or applications. Opening an in-app browser returned “Browser is not available: iab”. Therefore **browser screenshot review was not completed**. AppTest verifies rendered widget structure and interactions, not pixel-level layout. Responsive CSS and a consistent theme are supplied, but a manual desktop/mobile visual pass remains advisable before classroom projection.

## Content fidelity

The complete 46-slide text extraction and all referenced images were inspected before implementation. `DEVELOPMENT_PLAN.md` maps every slide to its lesson/activity, and records the source corrections. No trained-model outputs are claimed.
