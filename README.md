# Clien Chat

This project is a simple chat system developed with Flask, which allows users to ask questions to different stores and receive responses. Additionally, it includes an admin panel for managing users and their access to the stores.

## Features

- Chat with stores.
- User authentication.
- Admin panel for creating and editing users.
- Role-based access control.

## API Used

The chat system interacts with an external API to send questions and receive responses from stores. The specification of the API is as follows:

- **API URL**: `http://zonaprub.xyz:8000/answer/`
- **Method**: POST
- **Request Parameters**:
    - `makequestion`: The question asked by the user.
    - `storeName`: The name of the store to which the question is addressed.
- **Response**:
    - The API returns a response in JSON format with the store's answer.


## Setup and Installation

To set up and run this project, follow these steps:

1. Clone the repository:
2. Create and activate a virtual environment:
3. Install the dependencies:
4. Run the application:
5.
<pre lang="no-highlight"><code>

git clone [repository URL]
cd ClientChat-Stores
pip install -r requirements.txt
python3 app.py
</code></pre>

## Usage

After starting the application, you can access the chat system and the admin panel through your web browser.

- Chat URL: `http://localhost:5000/`
- Admin Panel URL: `http://localhost:5000/admin`

## Technologies Used

- Python
- Flask
- HTML/CSS
- Bootstrap