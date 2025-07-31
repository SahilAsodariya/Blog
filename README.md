# 📝 Flask Blog API

This is a simple RESTful Blog API built with Flask. It supports user authentication, blog post management, and comment functionality. Admin users can view and delete users.

---

## 📁 Project Structure

BLOG/
│
├── app/
│ ├── models.py
│ ├── routes/
│ ├── templates/
│ ├── static/
│ ├── init.py
│ └── extensions.py
│
├── migrations/
├── .env
├── requirements.txt
├── run..py
├── config.py
├── blog-api.postman_collection.json
└── README.md


---

## ⚙️ Setup Instructions

### 1. 🔧 Clone the Repository

git clone https://github.com/SahilAsodariya/Blog.git
cd blog 

## 2. 🐍 Create and Activate Virtual Environment

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


## 3. 📦 Install Dependencies

pip install -r requirements.txt


##  4. 🔐 Create .env File

SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///blog.db
JWT_SECRET_KEY=your-jwt-secret


## 5. 🛠️ Database Migrations

flask db init  # only once
flask db migrate -m "Your massage"
flask db upgrade

## 6. 🚀 Run the Application

flask run
or
python run.py
or
flask --app run(fileName,ex:run.py) run


## 7. 🔐 Authentication

==> JWT is used for secure access.
==> After logging in, include this header in all protected routes:
    Authorization: Bearer <your_token>

## 8. 🧪 API Endpoints

Method	          Endpoint	                              Description

POST	          /auth/register	                      Register a new user
POST	          /auth/login	                          Login user
GET	              /post/	                              Get all posts
POST	          /post/create	                          Create a new post
PUT               /post/update/<Post_ID>                  Update post
DELETE            /post/delete/<Post_id>                  Delete post
POST	          /add_comment/<Post_id>                  Create comment
DELETE            /admin/comment_delete/<Comment_id>      Admin: Delete comment
GET	              /admin/users	                          Admin: Get all users
DELETE	          /admin/delete_user/<userID>             Admin: Delete a user

## 9. 📬 Postman Collection

blog.postman_collection.json

To use:
       ==> Open Postman
       ==> Click "Import"
       ==> Select the .json file
       ==> Start testing your endpoints


## 10. ✍️ Author

Sahil - [github.com/SahilAsodariya]
