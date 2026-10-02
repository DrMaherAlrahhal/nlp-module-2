"""Small reusable visual components; escape all dynamic HTML."""
from html import escape
from pathlib import Path
import streamlit as st

BASE = Path(__file__).resolve().parent


def style():
    st.markdown('<style>' + (BASE/'assets/style.css').read_text(encoding='utf-8') + '</style>', unsafe_allow_html=True)


def hero(kicker, title, subtitle, tags=()):
    badges = ''.join(f'<span class="hero-tag">{escape(t)}</span>' for t in tags)
    st.markdown(f'<section class="hero"><div class="eyebrow">{escape(kicker)}</div><h1>{escape(title)}</h1><p>{escape(subtitle)}</p>{badges}</section>', unsafe_allow_html=True)


def prompt(text):
    st.markdown(f'<div class="prompt">{escape(text)}</div>', unsafe_allow_html=True)


def path(items):
    st.markdown('<div class="path">' + '<span class="path-arrow">→</span>'.join(f'<span class="path-node">{escape(s)}</span>' for s in items) + '</div>', unsafe_allow_html=True)


def entities(items):
    st.markdown('<div class="entity-row">' + ''.join(f'<span class="entity {escape(label, quote=True)}">{escape(word)}<small>{escape(label)}</small></span>' for word,label in items) + '</div>', unsafe_allow_html=True)


def decomposition(result):
    st.subheader(result['word'])
    st.write('↓')
    st.markdown('<div class="word-row">' + ''.join(f'<div class="word-piece"><small>{name}</small><strong>{escape(result[key] or "∅")}</strong></div>' for name,key in [('PREFIX','prefix'),('ROOT','root'),('SUFFIX / SUFFIXES','suffix')]) + '</div>', unsafe_allow_html=True)
    st.write(f"**{result['kind']}** · {result['info']}")
    st.caption('∅ = no affix here. Underlying morphemes may require a spelling change when joined.')


def reveal(label, key, text):
    if st.button(label, key=key):
        st.session_state[key+'_shown'] = True
    if st.session_state.get(key+'_shown'):
        st.info(text)


def feedback(q, answer):
    if answer == q['answer']:
        st.success('Correct')
    else:
        st.error('Try Again')
    st.write(f"**Correct concept: {q['concept']}**")
    st.write(f"**Answer:** {q['answer']}. {q['why']}")
    st.caption('Example: ' + q['example'])


def question(q, key):
    """Store the submitted answer separately from the currently edited choice."""
    with st.form(key):
        choice = st.radio(q['prompt'], q['choices'], index=None, key=key+'_choice')
        submitted = st.form_submit_button('Submit answer')
    if submitted:
        if choice is None:
            st.warning('Choose an answer first.')
        else:
            st.session_state[key+'_answer'] = choice
            st.session_state.setdefault('attempted', {})[q['id']] = choice == q['answer']
    if key+'_answer' in st.session_state:
        feedback(q, st.session_state[key+'_answer'])


def free_check(label, answer, explanation, key):
    with st.form(key):
        value = st.text_input(label, key=key+'_value')
        sent = st.form_submit_button('Check answer')
    if sent:
        if not value.strip():
            st.warning('Make a prediction first.')
        else:
            st.session_state[key+'_submitted'] = value
    if key+'_submitted' in st.session_state:
        value = st.session_state[key+'_submitted']
        (st.success if value.strip().casefold() == answer.casefold() else st.error)('Correct' if value.strip().casefold() == answer.casefold() else 'Try Again')
        st.write(f'**Answer: {answer}.** {explanation}')
