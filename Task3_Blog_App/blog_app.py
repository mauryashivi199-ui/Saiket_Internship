"""
Task 3: Simple Blog App with Local Storage (CLI Version)
Internship: Saiket Systems
Description: Complete CRUD Blog management system with local JSON file persistence.
"""

import json
import os
import sys
from datetime import datetime

# Windows UTF-8 encoding support
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATA_FILE = os.path.join(os.path.dirname(__file__), "blog_data.json")

INITIAL_SAMPLE_POSTS = [
    {
        "id": 1,
        "title": "Getting Started with Python & Modern Development",
        "author": "Shivangi Maurya",
        "category": "Technology",
        "content": "Python is one of the most versatile languages today, powering everything from AI models to web backends.",
        "date": "2026-09-15 10:30",
        "likes": 12
    },
    {
        "id": 2,
        "title": "Understanding REST APIs and Local Storage",
        "author": "Tech Explorer",
        "category": "Web Dev",
        "content": "Client-side storage like localStorage paired with REST APIs enables lightning-fast offline-first web apps.",
        "date": "2026-09-18 14:20",
        "likes": 8
    }
]


def load_posts() -> list[dict]:
    """Loads blog posts from local JSON storage, creates defaults if not exists."""
    if not os.path.exists(DATA_FILE):
        save_posts(INITIAL_SAMPLE_POSTS)
        return INITIAL_SAMPLE_POSTS
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Error reading local storage: {e}")
        return []


def save_posts(posts: list[dict]):
    """Persists blog posts array to local JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[!] Error saving to local storage: {e}")


def display_all_posts(posts: list[dict]):
    if not posts:
        print("\n📭 No blog posts found. Create one now!")
        return
    print("\n" + "=" * 70)
    print("                    📰 ALL BLOG POSTS")
    print("=" * 70)
    for p in posts:
        print(f"[{p['id']}] {p['title']}  ({p.get('category', 'General')})")
        print(f"    👤 By: {p['author']} | 📅 {p['date']} | ❤️ {p.get('likes', 0)} Likes")
        print(f"    📝 {p['content'][:80]}..." if len(p['content']) > 80 else f"    📝 {p['content']}")
        print("-" * 70)


def create_post():
    print("\n--- ✍️ Create New Blog Post ---")
    title = input("Enter post title: ").strip()
    if not title:
        print("[!] Title cannot be empty.")
        return
    author = input("Enter author name (default: Shivangi): ").strip() or "Shivangi"
    category = input("Enter category (e.g., Tech, Career, Life): ").strip() or "General"
    print("Enter post content (press Enter when done):")
    content = input("> ").strip()
    if not content:
        print("[!] Content cannot be empty.")
        return

    posts = load_posts()
    next_id = max([p["id"] for p in posts], default=0) + 1
    new_post = {
        "id": next_id,
        "title": title,
        "author": author,
        "category": category,
        "content": content,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "likes": 0
    }
    posts.append(new_post)
    save_posts(posts)
    print(f"\n✅ Blog post #{next_id} created and saved to local storage successfully!")


def view_single_post():
    posts = load_posts()
    try:
        post_id = int(input("\nEnter Post ID to read: ").strip())
        post = next((p for p in posts if p["id"] == post_id), None)
        if not post:
            print("[!] Post not found.")
            return
        print("\n" + "=" * 65)
        print(f"📖 {post['title'].upper()}")
        print(f"Category: {post.get('category', 'General')} | Author: {post['author']} | Date: {post['date']}")
        print("=" * 65)
        print(post["content"])
        print("=" * 65)
        print(f"Likes: ❤️ {post.get('likes', 0)}")
    except ValueError:
        print("[!] Please enter a valid numeric ID.")


def delete_post():
    posts = load_posts()
    try:
        post_id = int(input("\nEnter Post ID to delete: ").strip())
        post = next((p for p in posts if p["id"] == post_id), None)
        if not post:
            print("[!] Post not found.")
            return
        confirm = input(f"Are you sure you want to delete '{post['title']}'? (y/n): ").strip().lower()
        if confirm == 'y':
            posts = [p for p in posts if p["id"] != post_id]
            save_posts(posts)
            print("✅ Post deleted successfully from local storage.")
    except ValueError:
        print("[!] Please enter a valid numeric ID.")


def main():
    while True:
        print("\n" + "=" * 50)
        print("         📝 BLOG APP + LOCAL STORAGE        ")
        print("=" * 50)
        print(" 1. 📰 View All Posts")
        print(" 2. 📖 Read Single Post")
        print(" 3. ✍️ Create New Post")
        print(" 4. 🗑️ Delete Post")
        print(" 5. 🚪 Exit")
        print("=" * 50)

        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            display_all_posts(load_posts())
        elif choice == "2":
            view_single_post()
        elif choice == "3":
            create_post()
        elif choice == "4":
            delete_post()
        elif choice == "5":
            print("\nGoodbye! 👋\n")
            break
        else:
            print("[!] Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()
