# Quadhexle

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16-red.svg)](https://www.django-rest-framework.org/)

A unique and challenging color-guessing puzzle game built with Django. Unlike traditional Wordle, **Quadhexle** challenges you to simultaneously guess **four 6-digit hexadecimal color codes** in 9 tries. Features two game modes: Classic mode for strategic color puzzle-solving, and Nightmare mode with random gameplay-altering challenges.

---

## Game Concept

### What is Quadhexle?

Quadhexle is a color-based puzzle game where you must deduce **four hidden hex color codes** (e.g., `#4285F4`, `#EA4335`, `#FBBC05`, `#34A853`). Each guess reveals feedback for all four colors simultaneously:

- **Each tile is divided into 4 quadrants** — one for each color
- **Full color** = Character in correct position for that color
- **Dimmed color (40% opacity)** = Character exists in that color but wrong position  
- **Black** = Character not in that color at all

### Example Gameplay

If the secret colors are:
- Color 1: `4285F4`
- Color 2: `EA4335`
- Color 3: `FBBC05`
- Color 4: `34A853`

And you guess `123456`:
- Position 1 (`1`): Color 3 shows dimmed (it contains `1` but wrong spot)
- Position 2 (`2`): Color 1 shows full color (correct position!)
- Position 3 (`3`): Colors 2 & 4 show dimmed
- Position 4 (`4`): Colors 1 & 2 show dimmed
- And so on...

---

## Key Features

### Two Game Modes

**Classic Mode**
- Guess four 6-digit hex colors in 9 attempts
- Clean, strategic puzzle-solving with consistent feedback
- Perfect for learning color theory and hex codes
- Progressive revelation of each color

**Nightmare Mode**
- All the challenge of Classic mode with added twist mechanics
- Random challenge selected each game from 5 devious types:
  - **LIAR** — Some feedback tiles are randomly flipped (probability increases each guess)
  - **BROKEN** — Three random hex keys are marked as "broken" (dark red on keyboard)
  - **AMNESIA** — All previous guess feedback erased when you find a correct color
  - **GLITCH** — One color's "present/absent" feedback is swapped
  - **VAMPIRE** — One color's feedback shows in gray (hidden color, replaced by `#666666`)

### Unique Visual Features

- **Quad-split tiles** showing simultaneous feedback for 4 colors
- **Progressive color revelation** at top of screen
- **Color preview column** showing your typed hex codes
- **Blend toggle mode** — Combines quadrant colors into single blended tile with hover tooltips
- **Glassmorphism UI** with frosted glass panels and smooth animations
- **Themed color palettes** — Guess colors from Google, Discord, Pokemon, Marvel themes, etc.

### Highly Configurable

- All game rules via environment variables (`.env` file)
- Customize word length (default: 6), max guesses (default: 9)
- Adjust animation timings, tile spacing, board dimensions
- No code changes needed to modify difficulty
- Easy to extend with new color palettes

### User Account System

- Complete registration and authentication
- Persistent game statistics tracking
- Win percentage and streak calculations  
- Guess distribution analytics (wins per attempt number)
- Profile page with detailed stats

### Competitive Leaderboard

- Global rankings by max streak and win percentage
- Paginated display (configurable page size)
- Compare your performance with other players
- Real-time statistics

### REST API

- Game creation and management endpoints
- Guess submission and validation
- User profile data access
- Separate endpoints for Classic and Nightmare modes
- Give-up functionality with answer reveal

### Modern Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10+, Django 5.2, Django REST Framework 3.16 |
| **Database** | SQLite (development), PostgreSQL-ready (production) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), jQuery 3.7 |
| **Styling** | Custom CSS with Glassmorphism effects |
| **Color Palettes** | JSON-based themed color sets (Google, Discord, Marvel, etc.) |

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.10 or newer** ([Download here](https://www.python.org/downloads/))
- **pip** (Python package installer)
- **Git** (for cloning the repository)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone -b quadhexle https://github.com/NgTHung/Wordling.git
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

4. **Configure environment variables:**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` with your preferred settings. See the [Environment Configuration](#environment-configuration) section below for details.

5. **Apply database migrations:**
   
   This will create the database schema and automatically load color palettes from `api/gamepallets.json`:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - **Web Interface:** [http://localhost:8000/](http://localhost:8000/)
   - **Classic Game:** [http://localhost:8000/game/](http://localhost:8000/game/)
   - **Nightmare Mode:** [http://localhost:8000/nightmare/](http://localhost:8000/nightmare/)
   - **API Root:** [http://localhost:8000/api/](http://localhost:8000/api/)
   - **Admin Panel:** [http://localhost:8000/admin/](http://localhost:8000/admin/) (requires superuser)

---

## Environment Configuration

Quadhexle uses environment variables to configure both Django settings and game parameters. This makes it easy to customize the game without modifying code.

### Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Generate a secure secret key** (for production):
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

3. **Edit `.env`** with your preferred values.

### Configuration Options

#### Django Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | (required) | Django secret key - **MUST be changed for production** |
| `DEBUG` | `True` | Enable debug mode - **MUST be False in production** |

#### Game Rules

Customize core gameplay mechanics:

| Variable | Default | Description |
|----------|---------|-------------|
| `GAME_WORD_LENGTH` | `6` | Length of each hex color code (hexadecimal digits) |
| `GAME_MAX_GUESSES` | `9` | Maximum number of guesses allowed |

**Note:** The game is designed for 6-character hex codes guessing 4 colors simultaneously. Changing `GAME_WORD_LENGTH` will require adjustments to game logic and UI.

#### Animation Timings (milliseconds)

Fine-tune the user experience by adjusting animation speeds:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANIMATION_SHAKE_MS` | `600` | Duration of the "not enough letters" shake |
| `ANIMATION_TILE_FLIP_STAGGER_MS` | `100` | Delay between each tile flip (4 quadrants per tile) |
| `ANIMATION_BOUNCE_STAGGER_MS` | `100` | Delay between each bounce on win |
| `ANIMATION_WIN_MODAL_DELAY_MS` | `1200` | Delay before showing the win modal |
| `ANIMATION_MODAL_DELAY_MS` | `200` | Delay before modal animates in |
| `ANIMATION_TOAST_TIMEOUT_MS` | `7000` | Auto-hide timeout for toast notifications |

**Example:** Faster animations for a snappier experience:
```bash
ANIMATION_TILE_FLIP_STAGGER_MS=50
ANIMATION_BOUNCE_STAGGER_MS=50
ANIMATION_WIN_MODAL_DELAY_MS=800
```

#### UI Dimensions

Control visual layout:

| Variable | Default | Description |
|----------|---------|-------------|
| `UI_TILE_GAP_PX` | `5` | Gap between tiles in pixels |
| `UI_BOARD_MAX_WIDTH_PX` | `350` | Maximum width of the game board |
| `UI_BOARD_COLUMNS` | `5` | Number of tile columns (adjust for aesthetics) |

#### Pagination

| Variable | Default | Description |
|----------|---------|-------------|
| `LEADERBOARD_PAGE_SIZE` | `50` | Number of players shown per leaderboard page |

### Example `.env` File

```bash
# Django Configuration
SECRET_KEY='your-super-secret-key-here'
DEBUG=True

# Game Rules
GAME_WORD_LENGTH=6
GAME_MAX_GUESSES=9

# Animation Timings (milliseconds)
ANIMATION_SHAKE_MS=600
ANIMATION_TILE_FLIP_STAGGER_MS=100
ANIMATION_BOUNCE_STAGGER_MS=100
ANIMATION_WIN_MODAL_DELAY_MS=1200
ANIMATION_MODAL_DELAY_MS=200
ANIMATION_TOAST_TIMEOUT_MS=7000

# UI Dimensions
UI_TILE_GAP_PX=5
UI_BOARD_MAX_WIDTH_PX=350
UI_BOARD_COLUMNS=5

# Pagination
LEADERBOARD_PAGE_SIZE=50
```

---

## API Documentation

The REST API provides programmatic access to game functionality for both Classic and Nightmare modes.

### Base URL
```
http://localhost:8000/api/
```

### Classic Mode Endpoints

| Endpoint | Methods | Authentication | Description |
|----------|---------|----------------|-------------|
| `/api/` | `GET` | None | API root with endpoint links |
| `/api/games/` | `GET` | Session | List all classic games |
| `/api/games/<id>/` | `GET`, `PATCH` | Session | Retrieve or update a specific game |
| `/api/guesses/` | `GET`, `POST` | Session | List guesses or submit a new guess |
| `/api/guesses/<id>/` | `GET` | Session | Retrieve a specific guess |
| `/api/giveup/` | `GET` | Session | Forfeit current game and reveal the solution |

### Nightmare Mode Endpoints

| Endpoint | Methods | Authentication | Description |
|----------|---------|----------------|-------------|
| `/api/nightmare/games/` | `GET` | Session | List all nightmare games |
| `/api/nightmare/games/<id>/` | `GET`, `PATCH` | Session | Retrieve or update a specific nightmare game |
| `/api/nightmare/guesses/` | `GET`, `POST` | Session | List guesses or submit a new guess |
| `/api/nightmare/guesses/<id>/` | `GET` | Session | Retrieve a specific guess |
| `/api/nightmare/giveup/` | `GET` | Session | Forfeit current game and reveal the solution |

### User Endpoints

| Endpoint | Methods | Authentication | Description |
|----------|---------|----------------|-------------|
| `/api/users/` | `GET` | None | List all registered users |
| `/api/users/<id>/` | `GET` | None | Retrieve a specific user's profile |

### Example API Requests

**Submit a guess (Classic mode):**
```bash
curl -X POST http://localhost:8000/api/guesses/ \
  -H "Content-Type: application/json" \
  -d '{"word": "4285F4"}' \
  --cookie "sessionid=YOUR_SESSION_ID"
```

**Response format for guess:**
```json
{
  "result": ["GGBBBB", "BYBBBB", "BBGBBB", "BBBBYB"]
}
```

Each string in the array represents feedback for one of the 4 colors:
- `G` = Green (correct letter, correct position)
- `Y` = Yellow (correct letter, wrong position)
- `B` = Black/Gray (letter not in this color)

**Nightmare mode response may include additional feedback characters:**
- `V` = Vampire correct (correct position, but color hidden)
- `M` = Vampire present (present, but color hidden)
- `S`, `T`, `U` = Broken keyboard indicators

**Give up (reveal solution):**
```bash
curl -X GET http://localhost:8000/api/giveup/ \
  --cookie "sessionid=YOUR_SESSION_ID"
```

**Response:**
```json
{
  "message": "Game marked as lost.",
  "colors": ["4285F4", "EA4335", "FBBC05", "34A853"]
}
```

---

## Project Structure

```
Wordling/
├── api/                      # REST API application
│   ├── models.py             # Game models (Game, NightmareGame, Guess, NightmareGuess, Pallet)
│   ├── serializers.py        # DRF serializers for API responses
│   ├── views.py              # API view classes for both game modes
│   ├── urls.py               # API URL routing
│   ├── utils.py              # Core game logic (color_word, nightmare_color_word)
│   ├── constants.py          # Game constants loaded from .env
│   ├── gamepallets.json      # Themed color palette definitions
│   └── migrations/           # Database migrations including pallet population
│
├── wordle/                   # Main web application
│   ├── views.py              # Game, Home, Leaderboard, and Nightmare views
│   ├── urls.py               # Web URL routing
│   ├── static/
│   │   ├── css/              # Stylesheets with glassmorphism effects
│   │   │   ├── base.css      # Global styles and navbar
│   │   │   ├── game.css      # Game board, keyboard, quad-split tiles
│   │   │   ├── home.css      # Landing page styles
│   │   │   ├── leaderboard.css  # Rankings display
│   │   │   ├── login.css     # Authentication pages
│   │   │   └── profile.css   # User statistics dashboard
│   │   ├── js/               # Client-side game logic
│   │   │   └── home.js       # Landing page interactions
│   │   ├── img/              # Images and assets
│   │   └── favicon/          # Site icons
│   └── templates/
│       ├── base.html         # Base template with navbar and help modal
│       ├── game.html         # Classic mode interface (4-quadrant tiles)
│       ├── nightmare.html    # Nightmare mode with challenge mechanics
│       ├── home.html         # Landing page
│       └── leaderboard.html  # Player rankings
│
├── accounts/                 # User authentication & profiles
│   ├── models.py             # UserProfile model with game statistics
│   ├── views.py              # Login, Signup, Profile views
│   ├── urls.py               # Account URL routing
│   └── templates/
│       ├── login.html        # Login page
│       ├── signup.html       # Registration page
│       └── profile.html      # User statistics dashboard
│
├── Wordling/                 # Django project settings
│   ├── settings.py           # Main configuration file
│   ├── context_processors.py # Makes game constants available in templates
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI application entry point
│
├── .env                      # Environment variables (create from .env.example)
├── .env.example              # Example environment configuration
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project metadata (uv/pip)
├── db.sqlite3                # SQLite database (generated)
└── README.md                 # This file
```

### Key Files Explained

- **`api/utils.py`** — Contains `color_word()` and `nightmare_color_word()` functions that implement the core guessing logic with support for challenge mechanics
- **`api/constants.py`** — Centralizes all game configuration loaded from environment variables
- **`api/gamepallets.json`** — Defines themed color palettes (Google, Discord, Pokemon, Marvel, etc.)
- **`wordle/templates/game.html`** — Classic mode with 4-quadrant tile system and progressive color revelation
- **`wordle/templates/nightmare.html`** — Extended game template with challenge-specific UI elements (broken keys, blend toggle, challenge indicators)
- **`Wordling/context_processors.py`** — Makes constants like `WORD_LENGTH`, `MAX_GUESSES`, animation timings available to all templates

---

## How to Play

### Classic Mode

1. **Start a game** — Visit [http://localhost:8000/game/](http://localhost:8000/game/)
2. **Type a 6-digit hex code** using keys 0-9 and A-F (e.g., `4285F4`)
3. **Press Enter** to submit your guess
4. **Observe the quad-split feedback:**
   - Each tile divides into **4 quadrants** (top-left, top-right, bottom-left, bottom-right)
   - Each quadrant represents one of the 4 hidden colors
   - **Full color** = Character is in the correct position for that color
   - **Dimmed color** = Character exists in that color but wrong position
   - **Black** = Character is not in that color
5. **Watch the color display** at the top reveal characters as you guess correctly
6. **Win by deducing all 4 colors** within 9 attempts!

### Nightmare Mode

1. **Start a nightmare game** — Visit [http://localhost:8000/nightmare/](http://localhost:8000/nightmare/)
2. **Same rules as Classic mode** BUT with a random challenge:
   - **LIAR** — Some feedback tiles lie to you (probability increases each guess)
   - **BROKEN** — Three random keys are marked as "broken" (shown in dark red)
   - **AMNESIA** — All previous feedback erases when you find a correct color
   - **GLITCH** — One color has swapped "present/absent" feedback
   - **VAMPIRE** — One color's feedback shown in gray (no color preview)
3. **Use Blend Toggle** — Combines the 4 quadrant colors into a single blended tile (hover for detailed tooltip)
4. **Adapt your strategy** based on the challenge type

### Tips & Strategies

- **Start with diverse characters** — Use guesses like `012345` or `ABCDEF` to test many different hex digits
- **Track partial revelations** — The color display shows `#??4?F?` style progress for each color
- **Use the keyboard feedback** — Each key button also has 4 quadrants showing its status across all colors
- **In Nightmare mode:**
  - **LIAR** — Look for inconsistencies across guesses
  - **BROKEN** — Avoid the marked keys or use them strategically  
  - **AMNESIA** — Screenshot your progress before solving colors
  - **GLITCH** — Focus on one color at a time to identify the glitched one
  - **VAMPIRE** — The drained color shows as `#666666` but feedback works normally (just gray)

---

## Color Palettes

The game includes themed color palettes from popular brands and franchises:

| Theme | Example Colors |
|-------|----------------|
| **Google** | Blue `#4285F4`, Red `#EA4335`, Yellow `#FBBC05`, Green `#34A853` |
| **Discord** | Blurple `#5865F2`, Yellow `#FEE75C`, Green `#57F287`, Red `#ED4245` |
| **Pokemon FireRed** | Red `#872214`, Blue `#2514C9`, Teal `#47B09D`, Yellow `#E6BF3E` |
| **Iron Man** | Red `#AA0404`, Gold `#F1C347`, Dark Gray `#353839`, Silver `#B3B6B7` |

You can add more palettes by editing `api/gamepallets.json` and running migrations.

---

## Troubleshooting

### Common Issues

**Issue:** `ImportError: No module named 'rest_framework'`
- **Solution:** Make sure you've activated your virtual environment and run `pip install -r requirements.txt`

**Issue:** `ImproperlyConfigured: Set the SECRET_KEY environment variable`
- **Solution:** Create a `.env` file by copying `.env.example` and ensure it contains a `SECRET_KEY` value

**Issue:** Environment variables not being loaded
- **Solution:** 
  - Verify `.env` file exists in the project root (same directory as `manage.py`)
  - Check `.env` file format - no quotes around values unless they contain spaces
  - Restart the development server after changing `.env`

**Issue:** Database migration errors
- **Solution:** Delete `db.sqlite3` and rerun `python manage.py migrate`

**Issue:** Color palettes not loading
- **Solution:** Ensure `api/gamepallets.json` exists and run migrations again

**Issue:** Game board looks broken or quadrants don't show
- **Solution:** 
  - Clear browser cache and hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
  - Check browser console for JavaScript errors
  - Ensure jQuery is loading from CDN

**Issue:** Nightmare mode challenges not working
- **Solution:** Check browser console for errors. The challenge type is passed from backend to frontend JavaScript.

**Issue:** CSRF verification failed
- **Solution:** Ensure cookies are enabled and you're using the same domain for API calls

**Issue:** Stats not tracking for authenticated users
- **Solution:** Verify you're logged in and check that migrations have created the UserProfile table

---

## Adding Custom Color Palettes

You can add your own themed color palettes:

1. **Edit `api/gamepallets.json`:**
   ```json
   [
     {
       "name": "My Custom Theme",
       "theme": "Custom",
       "codes": ["FF0000", "00FF00", "0000FF", "FFFF00"]
     }
   ]
   ```

2. **Run migrations to populate the database:**
   ```bash
   python manage.py migrate
   ```

3. **Restart the server:**
   ```bash
   python manage.py runserver
   ```

Your new palette will be randomly selected during game creation!

---

## Acknowledgments

- Inspired by the original [Wordle](https://www.nytimes.com/games/wordle/index.html) by Josh Wardle
- Color palette themes from popular brands and franchises
- Built with [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/)
- UI inspiration from modern glassmorphism design trends
- Hexadecimal color code gameplay concept: Original

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---