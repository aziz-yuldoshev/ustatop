# 🛠️ USTATOP — Find Trusted Service Professionals

USTATOP is a Django-based service marketplace designed to help users find and connect with service professionals (*ustalar*) in their area.

The platform brings customers and professionals together in one place, making it easier to discover services and manage service requests.

## ✨ Features

- 🔎 Search and filter services
- 🧰 Browse service categories and professionals
- 👤 User and professional profiles
- 📍 Filter services by location
- 💰 Filter services by price range
- 📦 Service order management
- ⭐ Reviews and ratings
- ❤️ Favorites
- 🔔 Notifications
- 🛠️ Django administration panel

## 🛠️ Technologies

- Python
- Django
- SQLite
- HTML5
- CSS3
- Bootstrap
- JavaScript
- Git and GitHub

## 📁 Project Structure

```text
USTATOP/
├── config/
├── services/
├── orders/
├── reviews/
├── dashboard/
├── favorites/
├── notifications/
├── manage.py
└── .gitignore
```

*Note: The exact application folders may differ depending on the current project structure.*

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/aziz-yuldoshev/ustatop.git
cd ustatop
```

### 2. Create and activate a virtual environment

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

If a `requirements.txt` file exists:

```bash
pip install -r requirements.txt
```

Otherwise, install Django:

```bash
pip install django
```

### 4. Configure environment variables

Set the Django secret key using an environment variable. Never publish real secret keys or passwords.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## 🎯 Project Goal

The goal of USTATOP is to simplify the process of finding service professionals and managing customer requests through a convenient online marketplace.

## 👨‍💻 Author

**Aziz Yuldoshev**

GitHub: [@aziz-yuldoshev](https://github.com/aziz-yuldoshev)

## 🔐 Security

- Keep secret keys and passwords out of source code.
- Do not commit virtual environments or private databases.
- Use `DEBUG = False` for production deployment and configure allowed hosts appropriately.

## 📄 License

This repository is available for portfolio and educational demonstration. Add a formal license if you intend to distribute the project under specific reuse terms.
