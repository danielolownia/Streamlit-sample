import streamlit as st

# Initialize session state
if "users" not in st.session_state:
    st.session_state.users = {}

if "posts" not in st.session_state:
    st.session_state.posts = []

if "post_id" not in st.session_state:
    st.session_state.post_id = 1


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
        else:
            post = {
                "id": st.session_state.post_id,
                "user": user,
                "text": content,
                "likes": 0
            }
            st.session_state.posts.append(post)
            st.session_state.post_id += 1
            st.success("Post created!")

# ---------------- VIEW FEED ----------------
elif menu == "View feed":
    st.header("Feed")

    if not st.session_state.posts:
        st.info("No posts yet")
    else:
        for post in st.session_state.posts:
            st.subheader(f"Post #{post['id']}")
            st.write("**User:**", post["user"])
            st.write(post["text"])
            st.write("❤️ Likes:", post["likes"])
            st.divider()

# ---------------- LIKE A POST ----------------
elif menu == "Like a post":
    st.header("Like a Post")

    post_ids = [post["id"] for post in st.session_state.posts]

    if not post_ids:
        st.info("No posts to like")
    else:
        selected_id = st.selectbox("Choose a post ID", post_ids)

        if st.button("Like"):
            for post in st.session_state.posts:
                if post["id"] == selected_id:
                    post["likes"] += 1
                    st.success("Post liked!")
                    break

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
