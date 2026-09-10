"""
Task 2: Public API Data Fetcher (CLI & Core Logic)
Internship: Saiket Systems
Description: Fetches data from Public REST APIs, parses JSON, handles errors, and displays formatted records with search & filter.
"""

import json
import urllib.request
import urllib.error
import sys

# Ensure UTF-8 output on Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Free, reliable public API endpoints
API_PRODUCTS = "https://dummyjson.com/products"
API_USERS = "https://jsonplaceholder.typicode.com/users"


def fetch_data_from_api(url: str, timeout: int = 10) -> dict | list | None:
    """
    Fetches raw JSON data from a given REST API URL with timeout and error handling.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) SaiketInternship/1.0'
    }

    req = urllib.request.Request(url, headers=headers)
    
    try:
        print(f"Connecting to API: {url.split('?')[0]} ...")
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.status
            print(f"[SUCCESS] Response Status: {status_code} OK")

            raw_bytes = response.read()
            json_text = raw_bytes.decode('utf-8')
            data = json.loads(json_text)
            return data

    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP Error encountered: Code {e.code} - {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"[ERROR] Network/Connection Error: {e.reason}")
        print("Tip: Check your internet connection and try again.")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON response: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected Error: {e}")
        return None


def display_products():
    """Fetches and displays live Product Catalog with search & price sorting."""
    data = fetch_data_from_api(API_PRODUCTS)
    if not data or 'products' not in data:
        print("[ERROR] Could not retrieve product data.")
        return

    products = data['products']
    print(f"\nSuccessfully loaded {len(products)} products!\n")
    print(f"{'ID':<4} | {'Title':<30} | {'Category':<15} | {'Price ($)':<10} | {'Rating':<6}")
    print("-" * 75)

    for p in products[:15]:  # Display first 15 items
        title = p.get('title', 'N/A')[:28]
        category = p.get('category', 'N/A')[:14]
        price = f"${p.get('price', 0):.2f}"
        rating = f"* {p.get('rating', 0)}"
        print(f"{p.get('id', 0):<4} | {title:<30} | {category:<15} | {price:<10} | {rating:<6}")

    print("-" * 75)


def display_users():
    """Fetches and displays user directory from JSONPlaceholder API."""
    users = fetch_data_from_api(API_USERS)
    if not users or not isinstance(users, list):
        print("[ERROR] Could not retrieve user directory data.")
        return

    print(f"\nSuccessfully loaded {len(users)} user profiles!\n")
    print(f"{'ID':<4} | {'Name':<22} | {'Email':<25} | {'City':<15} | {'Company'}")
    print("-" * 85)

    for u in users:
        uid = u.get('id', 0)
        name = u.get('name', 'N/A')[:20]
        email = u.get('email', 'N/A')[:23]
        city = u.get('address', {}).get('city', 'N/A')[:13]
        company = u.get('company', {}).get('name', 'N/A')
        print(f"{uid:<4} | {name:<22} | {email:<25} | {city:<15} | {company}")

    print("-" * 85)


def main():
    while True:
        print("\n" + "=" * 55)
        print("        PUBLIC API DATA FETCHER & EXPLORER       ")
        print("=" * 55)
        print(" 1. Fetch & View Products (DummyJSON API)")
        print(" 2. Fetch & View User Profiles (JSONPlaceholder API)")
        print(" 3. Custom API Endpoint Explorer")
        print(" 4. Exit")
        print("=" * 55)

        choice = input("Select an option (1-4): ").strip()

        if choice == '1':
            display_products()
        elif choice == '2':
            display_users()
        elif choice == '3':
            custom_url = input("\nEnter full REST API URL (GET): ").strip()
            if custom_url:
                result = fetch_data_from_api(custom_url)
                if result is not None:
                    print("\n--- Parsed JSON Response Preview ---")
                    formatted_preview = json.dumps(result, indent=2)[:500]
                    print(formatted_preview)
                    if len(json.dumps(result)) > 500:
                        print("\n... [Output truncated for preview] ...")
        elif choice == '4':
            print("\nExiting Public API Data Fetcher. Goodbye! 👋\n")
            break
        else:
            print("[!] Invalid selection. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
