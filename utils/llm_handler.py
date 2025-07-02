import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["API_KEY"],
)

def call_llm(prompt, model="deepseek/deepseek-r1-0528-qwen3-8b:free", temperature=0.3):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error from LLM: {e}"
