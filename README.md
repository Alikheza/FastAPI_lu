# Lightweight Student Site

This is a lightweight version of a student site built using the FastAPI framework and a PostgreSQL database. SQLAlchemy ORM is used to interact with PostgreSQL. JWT tokens are used for authentication.

## Getting Started

### Clone the Repository

To use this project locally, first clone the repository:

```bash
git clone <repository-link>
```

### Install Required Frameworks

Install the necessary frameworks using the following command:

```bash
pip install -r requirements.txt
```

### Configuration

Create a file named `.env` in the root directory and set the following values:

```env
DATABASE_HOST=localhost
DATABASE_USERNAME=your_database_username
DATABASE_PASSWORD=your_database_password
DATABASE_PORT=your_database_port
DATABASE_NAME=your_database_name
SECRET_KEY=DO NOT USE THIS STRING AS SECRET KEY THIS IS ONLY FOR DEV PURPOSES
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=your_token_expiry_minutes
```

### Run the Application

Finally, run the application with the following command:

```bash
uvicorn app.main:app --host "yourlocalhost" --port 8000
```

### Dockerize the Project

To dockerize the project, simply use the following command:

```bash
docker-compose up
```

This will automatically build an image and run the project.

### Access Swagger Documentation

To access the Swagger documentation, append `/docs` to the end of the URL.

## Note

Make sure to replace placeholders like `<repository-link>`, `your_database_username`, `your_database_password`, `your_database_port`, `your_database_name`, `your_token_expiry_minutes`, and `"yourlocalhost"` with actual values relevant to your setup.

## License

This project is licensed under the MIT License.
