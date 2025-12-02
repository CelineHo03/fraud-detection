import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.redis_client import redis_client

def submit_text(message: str):
    print("Submitting text message for fraud detection...")
    print(f"Message: {message[:50]}..." if len(message) > 50 else f"Message: {message}")
    
    app_id = redis_client.create_application(
        submission_type="text",
        content=message,
        metadata={"source": "cli"}
    )
    
    print(f"Submission successful!")
    print(f"Application ID: {app_id}")
    print(f"Your submission is now in the processing queue.")
    print(f"Check status with: python cli/check_status.py {app_id}")
    
    return app_id

def submit_screenshot(file_path: str):
    """Submit screenshot for fraud detection"""
    path = Path(file_path)
    
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return None
    
    print(f"Submitting screenshot for fraud detection...")
    print(f"File: {path.name}")
    
    app_id = redis_client.create_application(
        submission_type="screenshot",
        content=str(path.absolute()),
        metadata={"source": "cli", "filename": path.name}
    )
    
    print(f"Screenshot submitted!")
    print(f"Application ID: {app_id}")
    print(f"File: {path.name}")
    print(f"Check status with: python cli/check_status.py {app_id}")
    
    return app_id

def main():
    parser = argparse.ArgumentParser(
        description="Submit fraud detection request",
        epilog="Examples:\n"
               "  python cli/submit.py --text 'Suspicious message'\n"
               "  python cli/submit.py --screenshot screenshot.png",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--text",
        type=str,
        help="Submit text message for fraud detection"
    )
    
    parser.add_argument(
        "--screenshot",
        type=str,
        help="Submit screenshot file path for fraud detection"
    )
    
    args = parser.parse_args()
    
    if args.text:
        submit_text(args.text)
    elif args.screenshot:
        submit_screenshot(args.screenshot)
    else:
        parser.print_help()
        print("Error: Please provide either --text or --screenshot")
        sys.exit(1)

if __name__ == "__main__":
    main()