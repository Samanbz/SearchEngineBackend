import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import HTTPException
load_dotenv()


client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

model = "gpt-3.5-turbo"
initail_prompt = f"You are an assistant at a new company, and your boss has asked you to summarize the headlines of the day into one single short line. The headlines are as follows:"


# Generates a summary of a list of headlines given the related topic and langugae)
def generate_summary(headlines: list[str], topic: str, language: str = "ens") -> str:
    try:
        summary = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": initail_prompt + " ".join(headlines) + f"\n concerning the topic {topic}, your response should be in {language}"},],
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=e, detail="Failed to generate summary")
    return summary.choices[0].message.content
