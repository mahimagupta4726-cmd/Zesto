# 🛍️ Zesto — E-Commerce Store
### CodeAlpha Internship | Task 1 | Mahima Gupta

---

## 🚀 Quick Start (VS Code / Any Terminal)

```bash
# Step 1 — Open the zesto/ folder in VS Code terminal

# Step 2 — Create a virtual environment (recommended)
python -m venv venv

# Step 3 — Activate it
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# Step 4 — Run the setup script (does everything)
python setup.py

# Step 5 — Start the server
python manage.py runserver
```

Open browser → **http://127.0.0.1:8000/**

---

## 🔑 Default Login
| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | `admin`  | `admin123` |

Admin panel: http://127.0.0.1:8000/admin/

---

## ✅ Features
- Product listings with category filter & search
- Product detail page with related products  
- Shopping cart (add / update qty / remove)
- Checkout with shipping form
- Order processing & order history (My Orders)
- User registration & login / logout
- SQLite database (products, users, orders)
- Django Admin panel for full management
- 12 pre-loaded sample products across 4 categories
- Responsive design — works on mobile & desktop
- Premium UI with Unsplash product images

---

## 🛠️ Tech Stack
| Layer    | Tech                    |
|----------|-------------------------|
| Backend  | Django 4.2+ (Python)    |
| Database | SQLite 3                |
| Frontend | HTML5, CSS3, JavaScript |
| Fonts    | Google Fonts (Inter + Playfair Display) |
| Images   | Unsplash (via URL)      |

---

## 📁 Project Structure
```
zesto/
├── zesto/                  ← Django config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                  ← Main app
│   ├── models.py           ← Category, Product, Order, OrderItem
│   ├── views.py            ← All logic
│   ├── urls.py             ← Routes
│   ├── admin.py
│   ├── context_processors.py
│   └── fixtures/
│       └── sample_data.json
├── templates/store/        ← All HTML pages
│   ├── base.html
│   ├── home.html
│   ├── product_list.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_success.html
│   ├── my_orders.html
│   ├── login.html
│   └── register.html
├── static/
│   ├── css/style.css       ← All styles
│   └── js/main.js
├── media/                  ← Uploaded images
├── db.sqlite3              ← Auto-created on setup
├── manage.py
├── requirements.txt
└── setup.py                ← Run this first!
```

---

*Built by Mahima Gupta | B.Tech CSE | SRMU | CodeAlpha 2024*
