# Pharmacy E-Commerce Backend

This is the backend API for the pharmacy e-commerce platform, built using **Express.js** and **MySQL**. It provides authentication, product management, and order processing functionalities.

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

-   Node.js (v16+ recommended)
-   MySQL

### Installation Steps

1. Install dependencies:

    ```bash
    npm install
    ```

2. Create database:

    ```bash
    npx sequelize-cli db:create
    ```

3. Run database migrations:

    ```bash
    npx sequelize-cli db:migrate
    ```

4. Start the development server:
    ```bash
    node index.js
    ```
    The server will run on `http://localhost:3000`.

## Authentication Endpoints

### Register a new user

```
POST /api/auth/register
```

-   **Request Body:**
    ```json
    {
        "first_name": "string",
        "last_name": "string",
        "email": "string",
        "password": "string",
        "role": "string"
    }
    ```
-   **Response:**
    ```json
    {
        "message": "User registered successfully"
    }
    ```

### Login

```
POST /api/auth/login
```

-   **Request Body:**
    ```json
    {
        "email": "string",
        "password": "string"
    }
    ```
-   **Response:**
    ```json
    {
        "token": "JWT token"
    }
    ```

## Notes

-   The backend expects JSON requests for most operations.
-   Authentication requires sending a JWT token in the `Authorization` header (`Bearer <token>`).
-   When making requests, always check the response structure to correctly handle success and error messages.
