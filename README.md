# Quiz Application

This is a simple quiz application developed using Flask, a Python web framework. The application allows users to create and manage quiz questions, add categories, and play quizzes based on different categories and the number of questions. The application stores quiz data in a SQLite database.

## API Endpoints

### 1. Get Quiz Questions

- **Endpoint:** `/api/quiz`
- **Method:** `GET`
- **Parameters:**
  - `category` (optional): Filter questions by category.
  - `count` (optional): Limit the number of questions returned.
- **Response:** Returns a JSON array of quiz questions.

### 2. Add Category

- **Endpoint:** `/add_category`
- **Method:** `POST`
- **Parameters:**
  - `category`: The name of the new category to add.
- **Response:** Displays a result message indicating success or failure.

### 3. Add Question

- **Endpoint:** `/add_question`
- **Method:** `POST`
- **Parameters:**
  - `category`: Category of the question.
  - `question`: The text of the question.
  - `correct_answer`: The correct answer to the question.
  - `incorrect_answers`: A list of incorrect answers.
- **Response:** Displays a result message indicating success or failure.

### 4. Delete Question

- **Endpoint:** `/delete_question_from_db`
- **Method:** `POST` or `DELETE`
- **Parameters:**
  - `id`: ID of the question to delete.
- **Response:** Displays a result message indicating success or failure.

### 5. Generate API URL

- **Endpoint:** `/generate_url`
- **Method:** `GET`
- **Parameters:**
  - `category` (optional): Filter questions by category.
  - `count` (optional): Limit the number of questions returned.
- **Response:** Displays a generated API URL based on the specified parameters.


## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/jojogmattam/Pyhton_Flask_MiniProject.git
    cd quiz-app
    ```

2. **Run the application:**

    ```bash
    python3 alta3research-flask01.py
    ```

   The application will be accessible at [http://localhost:5000](http://localhost:5000).

## Usage

1. Access the landing page at [http://localhost:5000](http://localhost:5000).

2. Use the navigation links to add new questions, add categories, generate API URLs, delete questions, and play quizzes.

## Database

The application uses SQLite to store quiz questions and categories. Two tables are created:

- `question_bank`: Stores quiz questions with columns for ID, category, question, correct answer, and incorrect answers.

- `category`: Stores categories for quiz questions.

## Notes

- Ensure that the `base_url` variable in the `alta3research-flask01.py` file matches the base URL where the API is hosted.

- Use caution when deleting questions, as it permanently removes them from the question bank.


