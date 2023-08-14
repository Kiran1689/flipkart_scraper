# Flipkart Scraper

The Flipkart Scraper is a Django REST framework application that allows users to scrape and save product details from Flipkart URLs. Users can sign up, log in, and use the API to scrape product information by providing a Flipkart URL.

## Features

- User Signup and Login: Users can sign up with an email and password, and log in to the application.
- JWT Authentication: The API uses JWT (JSON Web Token) based authentication for secure user sessions.
- Scrape Flipkart Product: Users can provide a Flipkart URL to scrape product details like title, price, ratings, and reviews.
- Database Storage: Scraped product details are stored in a PostgreSQL database associated with the user.

## Installation

1. Clone the repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the required dependencies by running: `pip install -r requirements.txt`
4. Set up your PostgreSQL database by updating the `DATABASES` configuration in `settings.py`.
5. Apply migrations to create the database schema by running: `python manage.py migrate`
6. Start the development server: `python manage.py runserver`


## API Endpoints

- **Signup:** `POST /api/signup/` - User registration.
- **Login:** `POST /api/login/` - User login to obtain JWT token.
- **Scrape Product:** `POST /api/scrape/` - Scrapes and saves product details from a Flipkart URL. Requires authentication.

## Usage

1. Sign up or log in to obtain an authentication token.
2. Use the authentication token to access the protected endpoints.
3. Scrape product details by sending a POST request to `/api/scrape/` with a Flipkart URL in the payload.

## Note

Ensure you have proper authentication before using protected endpoints. Invalid or expired tokens will result in authentication errors.

## Author

Kiran 



