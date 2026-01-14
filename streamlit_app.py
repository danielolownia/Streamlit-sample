import streamlit as st
import sqlite3

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("posts.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    text TEXT,
    likes INTEGER
)
""")
conn.commit()

# ---------------- SESSION STATE (USERS ONLY) ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

# ---------------- APP TITLE ----------------
st.title("Mini Social Media App")

menu = st.sidebar.selectbox(
    "Main Menu",
    [
        "Create a user",
        "Make a post",
        "View feed",
        "Like a post",
        "Edit your bio"
    ]
)

# ---------------- CREATE USER ----------------
if menu == "Create a user":
    st.header("Create a User")
    username = st.text_input("Username")
    bio = st.text_area("Bio")

    if st.button("Create User"):
        if username in st.session_state.users:
            st.error("User already exists")
        elif username == "":
            st.error("Username cannot be empty")
        else:
            st.session_state.users[username] = {
                "bio": bio,
                "followers": 0
            }
            st.success("User created!")
            st.write("**User:**", username)
            st.write("**Bio:**", bio)

# ---------------- MAKE A POST ----------------
elif menu == "Make a post":
    st.header("Make a Post")
    user = st.text_input("Your username")
    content = st.text_area("Post content")

    if st.button("Post"):
        if user not in st.session_state.users:
            st.error("User does not exist")
        elif content.strip() == "":
            st.error("Post cannot be empty")
        else:
            c.execute(
                "INSERT INTO posts (user, text, likes) VALUES (?, ?, ?)",
                (user, content, 0)
            )
            conn.commit()
            st.success("Post created!")

# ---------------- VIEW FEED ----------------
elif menu == "View feed":
    st.header("Feed")

    c.execute("SELECT id, user, text, likes FROM posts ORDER BY id DESC")
    posts = c.fetchall()

    if not posts:
        st.info("No posts yet")
    else:
        for post_id, user, text, likes in posts:
            st.subheader(f"Post #{post_id}")
            st.write("**User:**", user)
            st.write(text)
            st.write("❤️ Likes:", likes)
            st.divider()

# ---------------- LIKE A POST ----------------
elif menu == "Like a post":
    st.header("Like a Post")

    c.execute("SELECT id FROM posts")
    post_ids = [row[0] for row in c.fetchall()]

    if not post_ids:
        st.info("No posts to like")
    else:
        selected_id = st.selectbox("Choose a post ID", post_ids)

        if st.button("Like"):
            c.execute(
                "UPDATE posts SET likes = likes + 1 WHERE id = ?",
                (selected_id,)
            )
            conn.commit()
            st.success("Post liked!")

# ---------------- EDIT BIO ----------------
elif menu == "Edit your bio":
    st.header("Edit Bio")

    username = st.text_input("Username")
    new_bio = st.text_area("New bio")

    if st.button("Update Bio"):
        if username not in st.session_state.users:
            st.error("User does not exist")
        else:
            st.session_state.users[username]["bio"] = new_bio
            st.success("Bio updated!")
