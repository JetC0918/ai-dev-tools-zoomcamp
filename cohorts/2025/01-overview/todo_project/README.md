# TODO Application

This is a simple TODO application built with Django. It allows users to create, edit, delete, and manage TODO items with due dates and resolution status.

## Features

- Create new TODO items
- Edit existing TODO items
- Delete TODO items
- Assign due dates to TODO items
- Mark TODO items as resolved

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd todo_project
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```
   python manage.py migrate
   ```

5. **Run the development server:**
   ```
   python manage.py runserver
   ```

6. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

- Navigate to the TODO list to view all TODO items.
- Use the provided forms to create or edit TODO items.
- Confirm deletion when removing TODO items.

## License

This project is licensed under the MIT License.