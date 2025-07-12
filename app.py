import streamlit as st
from utils.llm_handler import call_llm
from utils.parser_utils import format_sql
import os

st.set_page_config(page_title="SQL Agent", layout="wide")
st.title("🧠 SQL Agent: NL ↔ SQL ↔ ORM ↔ DB")

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 NL → SQL", "🔁 SQL → ORM", "🗃️ Talk to DB"])

# --- Tab 1: Natural Language to SQL ---
with tab1:
    dialect = st.selectbox("Select SQL Dialect", ["PostgreSQL", "MySQL", "SQLite"])
    user_input = st.text_area("Enter your natural language instruction:", height=200)

    if st.button("🧠 Generate SQL", key="gen_sql"):
        if not user_input.strip():
            st.warning("Please enter a valid input.")
        else:
            with st.spinner("Generating SQL..."):
                with open("prompts/nl_to_sql.txt", "r", encoding="utf-8") as f:
                    prompt = f"-- Generate SQL compatible with {dialect}\n\n" + f.read()
                final_prompt = prompt.replace("{user_input}", user_input)
                result = call_llm(final_prompt)
                st.subheader("📝 Generated SQL")
                st.code(result, language='sql')
                st.subheader("📐 Formatted SQL")
                st.code(format_sql(result), language='sql')

# --- Tab 2: SQL to ORM ---
with tab2:
    sql_input = st.text_area("Paste your SQL below:", height=200)
    if st.button("🔁 Convert to ORM", key="sql_to_orm"):
        if not sql_input.strip():
            st.warning("Please enter a SQL query.")
        else:
            with st.spinner("Converting to ORM code..."):
                with open("prompts/sql_to_orm.txt", "r", encoding="utf-8") as f:
                    prompt = f.read()
                final_prompt = prompt.replace("{user_input}", sql_input)
                result = call_llm(final_prompt)
                st.subheader("📘 ORM Code (Django/SQLAlchemy)")
                st.code(result, language='python')

# --- Tab 3: Talk to DB ---
# --- Tab 3: Talk to DB ---
with tab3:
    st.markdown("### 🧠 Ask Questions in English → SQL → Query PostgreSQL")

    # DB settings input
    with st.expander("🔐 Database Connection Settings"):
        db_host = st.text_input("Host", value="localhost")
        db_port = st.text_input("Port", value="5433")  # updated to 5433 since you use that
        db_name = st.text_input("Database", value="sample")
        db_user = st.text_input("Username", value="postgres")
        db_pass = st.text_input("Password", type="password")

    nl_query = st.text_area("Ask a question in Natural Language:", height=150)

    # Helper: extract SQL code block only
    def extract_sql_block(text):
        import re
        matches = re.findall(r"```sql\n(.*?)```", text, re.DOTALL)
        return matches[0].strip() if matches else text.strip()

    if st.button("⚡ Run on Database"):
        if not nl_query.strip():
            st.warning("Please enter a natural language query.")
        elif not all([db_host, db_port, db_name, db_user, db_pass]):
            st.warning("Please fill in all database connection details.")
        else:
            with st.spinner("Generating SQL and querying database..."):
                try:
                    # Prepare prompt
                    with open("prompts/nl_to_sql.txt", "r", encoding="utf-8") as f:
                        base_prompt = f"-- Generate SQL compatible with PostgreSQL\n\n" + f.read()
                    final_prompt = base_prompt.replace("{user_input}", nl_query)

                    # Call LLM
                    raw_output = call_llm(final_prompt)
                    extracted_sql = extract_sql_block(raw_output)

                    # Display raw + parsed SQL
                    st.subheader("📝 Generated SQL")
                    st.code(extracted_sql, language="sql")

                    # Run query
                    from utils.db_connector import run_query
                    df = run_query(extracted_sql, db_host, db_port, db_name, db_user, db_pass)

                    st.success("✅ Query executed successfully!")
                    st.dataframe(df)

                except Exception as e:
                    st.error(f"❌ Failed to execute query: {e}")
