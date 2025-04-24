import os
import openai
from notion_client import Client

openai.api_key = os.environ["OPENAI_API_KEY"]
notion = Client(auth=os.environ["NOTION_TOKEN"])
DATABASE_ID = os.environ["DATABASE_ID"]

def run_compliance():
    try:
        results = notion.databases.query(database_id=DATABASE_ID)
        for page in results["results"]:
            props = page["properties"]
            english = props.get("English Script", {}).get("rich_text", [])
            spanish = props.get("Spanish Script", {}).get("rich_text", [])

            if english:
                text = english[0]["text"]["content"]
                prompt = f"Make this TikTok-compliant, keep it aggressive and grammatically perfect: {text}"
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You rewrite TikTok scripts to be compliant, not salesy, and aggressive on pain points."},
                        {"role": "user", "content": prompt}
                    ]
                )
                new_text = response.choices[0].message.content.strip()
                notion.pages.update(
                    page_id=page["id"],
                    properties={
                        "Compliant English Script": {
                            "rich_text": [{"text": {"content": new_text}}]
                        }
                    }
                )

            if spanish:
                text = spanish[0]["text"]["content"]
                prompt = f"Haz este guión compatible con TikTok, manteniéndolo impactante pero sin sonar como una venta dura: {text}"
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Reescribes guiones en español para TikTok, haciéndolos compatibles y naturales."},
                        {"role": "user", "content": prompt}
                    ]
                )
                new_text = response.choices[0].message.content.strip()
                notion.pages.update(
                    page_id=page["id"],
                    properties={
                        "Compliant Spanish Script": {
                            "rich_text": [{"text": {"content": new_text}}]
                        }
                    }
                )
        return True
    except Exception as e:
        import traceback
        print("=== ERROR DETAILS ===")
        traceback.print_exc()
        print("Error object:", e)
        return False

