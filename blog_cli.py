import mysql.connector
import getpass

db_config = {
    'host': 'localhost',
    'user': 'root',           
    'password': getpass.getpass("Enter MySQL password: "),         
    'database': 'blogdb'
}

def connect():
    return mysql.connector.connect(**db_config)

def create_post():
    title = input("Enter post title: ").strip()
    content = input("Enter post content: ").strip()
    tags_input = input("Enter comma-separated tags: ").strip()

    tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]

    conn = connect()
    cursor = conn.cursor()

    try:
        # Insert into posts
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        post_id = cursor.lastrowid

        # Insert tags and associate with post
        for tag in tags:
            cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
            result = cursor.fetchone()
            if result:
                tag_id = result[0]
            else:
                cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,))
                tag_id = cursor.lastrowid

            # Link post and tag
            cursor.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s)", (post_id, tag_id))

        conn.commit()
        print("✅ Post created successfully.")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def view_all_titles():
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT title FROM posts")
        results = cursor.fetchall()

        if results:
            print("\n📚 All Post Titles:")
            for idx, (title,) in enumerate(results, start=1):
                print(f"{idx}. {title}")
        else:
            print("No posts found.")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()

def view_post_by_title():
    title = input("Enter post title: ").strip()

    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, content FROM posts WHERE title = %s", (title,))
        result = cursor.fetchone()

        if result:
            post_id, content = result
            print(f"\n📝 Post Content:\n{content}")

            # Get tags
            cursor.execute("""
                SELECT t.name FROM tags t
                JOIN post_tags pt ON t.id = pt.tag_id
                WHERE pt.post_id = %s
            """, (post_id,))
            tags = [row[0] for row in cursor.fetchall()]
            print(f"\n🏷️ Tags: {', '.join(tags)}")
        else:
            print("Post not found.")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()

def search_posts_by_tag():
    tag = input("Enter tag to search: ").strip().lower()

    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT p.title FROM posts p
            JOIN post_tags pt ON p.id = pt.post_id
            JOIN tags t ON pt.tag_id = t.id
            WHERE t.name = %s
        """, (tag,))
        results = cursor.fetchall()

        if results:
            print("\n🔍 Posts with tag:", tag)
            for idx, (title,) in enumerate(results, start=1):
                print(f"{idx}. {title}")
        else:
            print("No posts found with that tag.")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()

def main():
    while True:
        print("\n📘 Blog Post Manager")
        print("1. Create a new post")
        print("2. View all post titles")
        print("3. View post content by title")
        print("4. Search posts by tag")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            create_post()
        elif choice == '2':
            view_all_titles()
        elif choice == '3':
            view_post_by_title()
        elif choice == '4':
            search_posts_by_tag()
        elif choice == '5':
            print("👋 Exiting. Bye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
