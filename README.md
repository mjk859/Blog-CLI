# 📝 Blog CLI Application

A simple command-line interface (CLI) application to manage blog posts using Python and MySQL.  
Users can create posts with tags, view all post titles, view content by title, and search posts by tag.

---

## 📦 Features

- Create new blog posts with comma-separated tags  
- View all blog post titles  
- View a specific post’s content and its tags by title  
- Search blog posts by a specific tag  

---

## 🗃️ Database Schema

The application uses a MySQL database with the following tables:

### `posts`
| Field   | Type         | Description          |
|---------|--------------|----------------------|
| id      | INT (PK)     | Auto-incremented ID  |
| title   | VARCHAR(255) | Title of the post    |
| content | TEXT         | Content of the post  |

### `tags`
| Field | Type         | Description            |
|-------|--------------|------------------------|
| id    | INT (PK)     | Auto-incremented ID    |
| name  | VARCHAR(255) | Unique tag name        |

### `post_tags`
| Field    | Type | Description                        |
|----------|------|------------------------------------|
| post_id  | INT  | Foreign key referencing `posts.id` |
| tag_id   | INT  | Foreign key referencing `tags.id`  |
| PRIMARY  |      | Combined primary key (post_id, tag_id) |

> This schema allows a many-to-many relationship between posts and tags.

---

## 🛠️ How to Run

### ✅ Requirements

- Python 3.10+
- MySQL Server
- `mysql-connector-python` library (`pip install mysql-connector-python`)

### 🚀 Steps to Run

1. **Clone this repository**

    git clone https://github.com/yourusername/blog-cli  
    cd blog-cli

2. **Create the database and tables**

    Open MySQL and run the following:

    CREATE DATABASE IF NOT EXISTS blogdb;
    USE blogdb;

    CREATE TABLE posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL
    );

    CREATE TABLE tags (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE
    );

    CREATE TABLE post_tags (
        post_id INT,
        tag_id INT,
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (tag_id) REFERENCES tags(id),
        PRIMARY KEY (post_id, tag_id)
    );

3. **Run the application**

    python blog_cli.py

4. **Enter your MySQL credentials**

    You’ll be prompted to enter your MySQL password securely via `getpass`.

---

## 🔐 Security Note

The application uses Python’s `getpass` module to avoid hardcoding the MySQL password into the code.  
This provides a more secure way of handling credentials compared to plain strings.

---

## 🧠 Search by Tag

To find posts by a tag, the app performs a join between `posts`, `post_tags`, and `tags` where the tag name matches the user input.  
This fetches all matching post titles.

---

## 💡 Alternative Approach to Tagging

An alternative could be storing tags as a comma-separated string in the `posts` table.  
However, this approach violates database normalization rules and makes queries inefficient.  
Using a many-to-many linking table (`post_tags`) is the better and scalable solution.

---
