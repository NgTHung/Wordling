# Wordling

Wordling is a Django-based implementation of the Wordle game. It uses a word list sourced from [dwyl/english-words](https://github.com/dwyl/english-words) and provides both a web interface and a REST API for gameplay.

## Features

- Play Wordle in your browser.
- REST API for games, guesses, and users.
- User authentication and session management.
- Game logic with win/loss tracking and guess feedback (green/yellow/black).
- Word list loaded from `words_alpha.txt`.

## Project Structure

- `Wordling/` - Django project settings and URLs.
- `api/` - REST API for games, guesses, and users.
- `wordle/` - Web interface, templates, and static files.
- `db.sqlite3` - SQLite database.

## Requirements

- Python >= 3.14
- Django >= 5.2.7
- djangorestframework >= 3.16.1

## Installation

1. **Clone the repository:**
	```bash
	git clone https://github.com/NgTHung/Wordling.git
	cd Wordling
	```

2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```

3. **Apply migrations:**
	```bash
	python manage.py migrate
	```

4. **Run the development server:**
	```bash
	python manage.py runserver
	```

5. **Access the app:**
	- Web: [http://localhost:8000/](http://localhost:8000/)
	- API: [http://localhost:8000/api/](http://localhost:8000/api/)

## API Endpoints

- `/api/games/` - List and create games
- `/api/games/<id>/` - Retrieve/update a game
- `/api/guesses/` - List and create guesses
- `/api/guesses/<id>/` - Retrieve/update a guess
- `/api/users/` - List users
- `/api/users/<id>/` - Retrieve a user
- `/api/giveup/` - Mark current game as lost

## How to Play

- Start a new game from the homepage.
- Enter guesses; feedback is given for each letter (G=Green, Y=Yellow, B=Black).
- You have 6 attempts to guess the word.
- Give up to reveal the answer.

## License

This project is licensed under the MIT License.