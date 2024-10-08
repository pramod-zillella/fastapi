# Social Media Platform RESTful API

This is a RESTful API built for a social media platform, developed using FastAPI, PostgreSQL, and SQLAlchemy. It supports CRUD operations for posts and users, along with JWT-based authentication. The API is deployed on Oracle Cloud Infrastructure (OCI) and includes HTTPS/SSL security with NGINX.

## Features

- **User Authentication**: JWT-based authentication with user registration and login.
- **CRUD Operations**: Full CRUD support for posts and users.
- **Post Voting**: Vote on posts to increase or decrease their score.
- **Data Validation**: Schema validation with Pydantic for robust request/response handling.
- **Deployed on OCI**: Deployed on Oracle Cloud Infrastructure with Ubuntu, NGINX, and Gunicorn.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **SQLAlchemy**: An ORM for Python that provides efficient and easy-to-use database management.
- **NGINX & Gunicorn**: For serving the application with SSL/HTTPS security.

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Oracle Cloud Infrastructure (optional, for deployment)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/pramod-zillella/fastapi-app-demo.git
   cd fastapi-app-demo
   ```

2. **Set Up Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Requirements:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file with the following details:

   ```plaintext
   DATABASE_URL=postgresql://username:password@localhost:5432/social_media_db
   SECRET_KEY=your_jwt_secret_key
   DATABASE_HOSTNAME=localhost
   DATABASE_USERNAME=set_your_username
   DATABASE_PASSWORD=set_your_password
   DATABASE_NAME=fastapi
   DATABASE_PORT=5433
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   SECRET_KEY=your_jwt_secret_key
   ALGORITHM=algorithm_for_decoding
    
   ```

5. **Run Database Migrations:**

   ```bash
   alembic upgrade head
   ```

6. **Run the API Locally:**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API should now be running locally on `http://127.0.0.1:8000/docs`, where you can test it using the interactive documentation.

## Deployment on OCI

1. **Configure Gunicorn and NGINX** for production settings.
2. **Install Certbot** to set up HTTPS using Let's Encrypt.

## API Endpoints

| Endpoint     | HTTP Method | Description                      |
|--------------|-------------|----------------------------------|
| `/users/`    | POST        | Create a new user                |
| `/authenticate/`    | POST        | Authenticate a user              |
| `/posts/`    | GET, POST   | Retrieve or create a post        |
| `/posts/{id}`| GET, PUT, DELETE | Retrieve, update, or delete a post |
| `/vote/`     | POST        | Vote on a post                   |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
