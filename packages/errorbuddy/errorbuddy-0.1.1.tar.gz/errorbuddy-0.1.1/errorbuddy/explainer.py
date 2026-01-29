from .rules import ERROR_RULES
import traceback

def explain(error: Exception):
    error_name = type(error).__name__
    message = str(error)

    rule = ERROR_RULES.get(error_name)

    print(f"\n🚨 ERROR: {error_name}")
    print(f"📍 Message: {message}")

    if rule:
        print("\n🧠 What happened?")
        print(rule["explanation"])

        print("\n🛠️ How to fix it?")
        print(rule["fix"])

        print("\n✅ Example:")
        print(rule["example"])
    else:
        print("\n🤔 This error is uncommon.")
        print("📌 Suggestion:")
        print("Check the traceback carefully or search the exact message.")