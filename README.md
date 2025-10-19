# Wordling

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16-red.svg)](https://www.django-rest-framework.org/)

A modern, full-featured implementation of the popular word-guessing game Wordle, built with Django. Features a polished animated web interface with glassmorphism effects, a comprehensive REST API, and a complete user account system for tracking statistics and competing on a global leaderboard.

---

## Key Features

- **Classic Wordle Gameplay**
  - Beautiful, responsive interface with smooth animations
  - Tile flip effects, win celebrations, and invalid guess feedback
  - Color-coded letter feedback (Green = correct position, Yellow = wrong position, Gray = not in word)
  - Support for duplicate letter handling

- **User Account System**
  - Complete registration and authentication flow
  - Persistent game statistics tracking
  - Win percentage and streak calculations
  - Guess distribution analytics

- **Competitive Leaderboard**
  - Public ranking system based on max streaks and win percentages
  - Real-time statistics display
  - Compare your performance with other players

- **REST API**
  - Game creation and management endpoints
  - Guess submission and validation
  - User profile data access

- **Modern UI/UX**
  - Glassmorphism design with frosted glass panels
  - Fully responsive layout for mobile and desktop
  - jQuery-powered interactivity
  - Clean, professional aesthetic

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10+, Django 5.2, Django REST Framework 3.16 |
| **Database** | SQLite (development), PostgreSQL-ready (production) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), jQuery 3.7 |
| **Styling** | Custom CSS with Glassmorphism effects |
| **Word List** | [dwyl/english-words](https://github.com/dwyl/english-words) (~370k words) |

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.10 or newer** ([Download here](https://www.python.org/downloads/))
- **pip** (Python package installer)
- **Git** (for cloning the repository)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/NgTHung/Wordling.git
    cd Wordling
    ```

2. **Create and activate a virtual environment:**
   
   **On macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   
   **On Windows:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   
   This will create the database schema and automatically load the word list from `words_alpha.txt`:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - **Web Interface:** [http://localhost:8000/](http://localhost:8000/)
   - **API Root:** [http://localhost:8000/api/](http://localhost:8000/api/)
   - **Admin Panel:** [http://localhost:8000/admin/](http://localhost:8000/admin/) (requires superuser)

---

## API Documentation

The REST API provides programmatic access to all game functionality.

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

| Endpoint | Methods | Authentication | Description |
|----------|---------|----------------|-------------|
| `/api/` | `GET` | None | API root with endpoint links |
| `/api/games/` | `GET`, `POST` | Session | List all games or create a new game |
| `/api/games/<id>/` | `GET`, `PATCH` | Session | Retrieve or update a specific game |
| `/api/guesses/` | `GET`, `POST` | Session | List guesses or submit a new guess |
| `/api/guesses/<id>/` | `GET` | Session | Retrieve a specific guess |
| `/api/users/` | `GET` | None | List all registered users |
| `/api/users/<id>/` | `GET` | None | Retrieve a specific user's profile |
| `/api/giveup/` | `GET` | Session | Forfeit current game and reveal the solution |

### Example API Requests

**Create a new game:**
```bash
curl -X POST http://localhost:8000/api/games/ \
  -H "Content-Type: application/json" \
  --cookie "sessionid=YOUR_SESSION_ID"
```

**Submit a guess:**
```bash
curl -X POST http://localhost:8000/api/guesses/ \
  -H "Content-Type: application/json" \
  -d '{"word": "hello"}' \
  --cookie "sessionid=YOUR_SESSION_ID"
```

**Response format for guess:**
```json
{
  "result": "GYBBB"
}
```
Where:
- `G` = Green (correct letter, correct position)
- `Y` = Yellow (correct letter, wrong position)
- `B` = Black/Gray (letter not in word)

---

## Project Structure

```
Wordling/
├── api/                      # REST API application
│   ├── models.py             # Game, Word, and Guess models
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # API view classes
│   ├── urls.py               # API URL routing
│   ├── utils.py              # Helper functions (color_word logic)
│   └── words_alpha.txt       # Word list source file
│
├── wordle/                   # Main web application
│   ├── views.py              # Game, Home, and Leaderboard views
│   ├── urls.py               # Web URL routing
│   ├── static/
│   │   ├── css/              # Stylesheets with glassmorphism
│   │   ├── js/               # jQuery game logic
│   │   └── img/              # Images and assets
│   └── templates/
│       ├── base.html         # Base template with navbar
│       ├── game.html         # Main game interface
│       ├── home.html         # Landing page
│       └── leaderboard.html  # Player rankings
│
├── accounts/                 # User authentication & profiles
│   ├── models.py             # UserProfile model with stats
│   ├── views.py              # Login, Signup, Profile views
│   ├── urls.py               # Account URL routing
│   └── templates/
│       ├── login.html        # Login page
│       ├── signup.html       # Registration page
│       └── profile.html      # User statistics dashboard
│
├── Wordling/                 # Django project settings
│   ├── settings.py           # Main configuration file
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI application entry point
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project metadata
├── db.sqlite3                # SQLite database (generated)
└── README.md                 # This file
```

---

## How to Play

1. **Visit the homepage** and click "Play" or register for an account to track your stats
2. **Guess the 5-letter word** in 6 tries or fewer
3. **Observe the color feedback:**
   - 🟩 **Green** = Letter is in the word and in the correct position
   - 🟨 **Yellow** = Letter is in the word but in the wrong position
   - ⬜ **Gray** = Letter is not in the word at all
4. **Use the feedback** to make more informed guesses
5. **Win by guessing the word** before running out of attempts!

---

## Troubleshooting

### Common Issues

**Issue:** `ImportError: No module named 'rest_framework'`
- **Solution:** Make sure you've activated your virtual environment and run `pip install -r requirements.txt`

**Issue:** Database migration errors
- **Solution:** Delete `db.sqlite3` and rerun `python manage.py migrate`

**Issue:** Words not loading
- **Solution:** Ensure `api/words_alpha.txt` exists and run the migration `0004_Populate_words.py`

**Issue:** CSRF verification failed
- **Solution:** Ensure cookies are enabled and you're using the same domain for API calls

---

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**!

### How to Contribute

1. **Fork the Project**
2. **Create your Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your Changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guidelines for Python code
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Word list provided by [dwyl/english-words](https://github.com/dwyl/english-words)
- Inspired by the original [Wordle](https://www.nytimes.com/games/wordle/index.html) by Josh Wardle
- Built with [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/)
- UI inspiration from modern glassmorphism design trends

---