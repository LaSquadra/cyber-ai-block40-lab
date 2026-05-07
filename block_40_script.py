from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

ALERT_FILE = "/var/log/snort/alert"

def read_snort_alerts(path: str) -> str:
    """Read Snort alert file with basic error handling."""
    try:
        with open(path, "r") as f:
            data = f.read().strip()
    except FileNotFoundError:
        print(f"[Error] Alert file not found: {path}")
        print("Make sure Snort has run and generated alerts.")
        return ""
    except PermissionError:
        print(f"[Error] Permission denied when reading: {path}")
        print("Try fixing permissions with:")
        print("  sudo chmod 666 /var/log/snort/alert")
        return ""
    if not data:
        print("[Info] No alerts found in the file yet.")
        return ""
    return data

def extract_text_from_response(response) -> str:
    """Extract the model's text output from a Responses API response."""
    if hasattr(response, "output_text") and response.output_text:
        return str(response.output_text).strip()

    outputs = getattr(response, "output", None)
    if outputs:
        if isinstance(outputs, list) and outputs:
            first_output = outputs[0]
            if isinstance(first_output, dict):
                content = first_output.get("content")
                if isinstance(content, list) and content:
                    first_item = content[0]
                    text = first_item.get("text") if isinstance(first_item, dict) else None
                    if text:
                        return str(text).strip()
                text = first_output.get("text")
                if text:
                    return str(text).strip()
            else:
                content = getattr(first_output, "content", None)
                if isinstance(content, list) and content:
                    text = getattr(content[0], "text", None)
                    if text:
                        return str(text).strip()
                text = getattr(first_output, "text", None)
                if text:
                    return str(text).strip()

    if hasattr(response, "text") and response.text:
        return str(response.text).strip()

    return str(response).strip()


def analyze_alerts_with_genai(alerts: str) -> None:
    """Send Snort alerts to the GenAI model and print the explanation."""
    print("\n[GenAI Threat Analysis:]\n")
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Analyze this Snort alert log and explain what happened:\n\n{alerts}"
    )
    explanation = extract_text_from_response(response)
    if not explanation:
        print("[Warning] No text output was returned by the model.")
        return
    print(explanation)

def main():
    alerts = read_snort_alerts(ALERT_FILE)
    if not alerts:
          return
    analyze_alerts_with_genai(alerts)
if __name__ == "__main__":
    client = OpenAI()
    main()