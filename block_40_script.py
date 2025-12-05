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

def analyze_alerts_with_genai(alerts: str) -> None:
    """Send Snort alerts to the GenAI model and print the explanation."""
    print("\n[GenAI Threat Analysis:]\n")
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Analyze this Snort alert log and explain what happened:\n\n{alerts}"
    )
    explanation = response.output[0].content[0].text
    print(explanation)

def main():
    alerts = read_snort_alerts(ALERT_FILE)
    if not alerts:
          return
    analyze_alerts_with_genai(alerts)
if __name__ == "__main__":
    client = OpenAI()
    main()