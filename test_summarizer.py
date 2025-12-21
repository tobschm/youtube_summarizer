import sys
from Summarizer import summarize
from database import Database

def main():
    # Try to get API key from database
    try:
        db = Database()
        api_key = db.get_api_key("google_api_key")
        if not api_key:
            print("Error: No API key found in database. Please run the GUI app and save a key first.")
            return
    except Exception as e:
        print(f"Error accessing database: {e}")
        return

    # Default test video (short one) or user input
    default_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print(f"No URL provided, using default: {default_url}")
        url = default_url

    print(f"Summarizing: {url}")
    print("Scope: High level")
    print("Language: English")
    print("-" * 20)

    try:
        result = summarize(url, "High level", "English", api_key)
        print("\n--- Result ---")
        print(f"Type: {type(result)}")
        print(result)
        print("--------------")
    except Exception as e:
        print(f"\nError during summarization: {e}")

if __name__ == "__main__":
    main()
