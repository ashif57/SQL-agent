import streamlit as st
from utils.llm_handler import call_llm
from utils.parser_utils import format_sql
import os

# UI Title
st.title("🧠 SQL Agent: NL ↔ SQL ↔ ORM")

# Task Selector
task = st.radio("Select Task", ["Natural Language → SQL", "SQL → ORM"], horizontal=True)

# Dialect Selector (only visible for NL → SQL task)
if task == "Natural Language → SQL":
    dialect = st.selectbox("Select SQL Dialect", ["PostgreSQL", "MySQL", "SQLite"])
else:
    dialect = None  # Not used in ORM conversion

# Text Input
user_input = st.text_area("Enter your input below:", height=200)

# Submit Button
if st.button("🔍 Generate"):
    if not user_input.strip():
        st.warning("Please enter a valid input.")
    else:
        with st.spinner("Processing with LLM..."):
            # Load prompt
            prompt_file = "prompts/nl_to_sql.txt" if task == "Natural Language → SQL" else "prompts/sql_to_orm.txt"
            with open(prompt_file, 'r', encoding='utf-8') as f:
                base_prompt = f.read()

            # Inject user input and optional dialect note
            if task == "Natural Language → SQL":
                dialect_note = f"-- Generate SQL compatible with {dialect}\n\n"
                final_prompt = dialect_note + base_prompt.replace("{user_input}", user_input)
            else:
                final_prompt = base_prompt.replace("{user_input}", user_input)

            # Call LLM
            result = call_llm(final_prompt)

            # Show result
            if task == "Natural Language → SQL":
                st.subheader("📝 Generated SQL")
                st.code(result, language='sql')
                st.subheader("📐 Formatted SQL")
                st.code(format_sql(result), language='sql')
            else:
                st.subheader("📘 ORM Code (Django/SQLAlchemy)")
                st.code(result, language='python')
