# Thailand Recommendation API

This project is django-based api for travel locations ratings and automated routing optimization with provided features:
1. JWT authentication using username and password
2. Adding new locations
3. Remove new locations
4. Finding optimal travel route by minimizing travelling distance

## Installation

1. Clone the repository
`git clone https://github.com/Narawish/thailand-recommendations.git`
`cd thailand-recommendations`
2. Install the requirements
`pip install -r requirements.txt`
3. Setting up environments variables
`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, and `SECRET_KEY`
4. Run the migration to set up database
`python manage.py migrate`
5. Start server
`python manage.py runserver`

## Endpoints
