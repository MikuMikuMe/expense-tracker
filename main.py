Creating a full-fledged full-stack application within a single Python script is quite complex, so I'll write a simplified version for the backend using Flask and SQLite. This Python code will serve as an API, which a front-end application can use to perform CRUD operations and basic analytics on user expenses.

Here's a minimalistic version of such an application:

### Backend: Python Flask Application

```python
from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

DATABASE = 'expense_tracker.db'

# Create the database and table if they do not exist
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                      id INTEGER PRIMARY KEY,
                      date TEXT NOT NULL,
                      category TEXT NOT NULL,
                      amount REAL NOT NULL,
                      description TEXT)''')
    conn.commit()
    conn.close()

# Utility function to connect to the database
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    return conn

@app.route('/expenses', methods=['GET'])
def get_expenses():
    conn = db_connection()
    cursor = conn.cursor()
    
    cursor = conn.execute("SELECT * FROM expenses")
    expenses = [
        dict(id=row[0], date=row[1], category=row[2], amount=row[3], description=row[4])
        for row in cursor.fetchall()
    ]
    
    conn.close()
    return jsonify(expenses)

@app.route('/expenses', methods=['POST'])
def add_expense():
    new_expense = request.json
    conn = db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''INSERT INTO expenses (date, category, amount, description)
                          VALUES (?, ?, ?, ?)''',
                       (new_expense['date'], new_expense['category'], 
                        new_expense['amount'], new_expense.get('description')))
        conn.commit()
        conn.close()
        return jsonify(new_expense), 201
    except KeyError as e:
        return f"Missing field {str(e)}", 400
    except Error as e:
        return str(e), 500

@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    conn = db_connection()
    cursor = conn.cursor()
    
    try:
        update_data = request.json
        cursor.execute('''UPDATE expenses 
                          SET date = ?, category = ?, amount = ?, description = ?
                          WHERE id = ?''',
                       (update_data['date'], update_data['category'],
                        update_data['amount'], update_data.get('description'), id))
        conn.commit()
        success = cursor.rowcount
        conn.close()
        if success:
            return jsonify(update_data), 200
        else:
            return "Expense not found", 404
    except KeyError as e:
        return f"Missing field {str(e)}", 400
    except Error as e:
        return str(e), 500

@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
        conn.commit()
        success = cursor.rowcount
        conn.close()
        if success:
            return "Expense deleted successfully", 204
        else:
            return "Expense not found", 404
    except Error as e:
        return str(e), 500

@app.route('/analytics/total', methods=['GET'])
def get_total_expense():
    conn = db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({"total_expense": total_expense or 0}), 200

@app.route('/analytics/category', methods=['GET'])
def get_expense_by_category():
    conn = db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    expenses_by_category = [
        dict(category=row[0], total=row[1])
        for row in cursor.fetchall()
    ]
    
    conn.close()
    return jsonify(expenses_by_category), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
```

### Explanation
- **Flask**: Used to create a RESTful API for managing expenses.
- **SQLite**: An embedded database that's easy to set up and use for small to medium applications.
- **Endpoints**:
  - `/expenses` (GET): Retrieve list of all expenses.
  - `/expenses` (POST): Add a new expense.
  - `/expenses/<id>` (PUT): Update an existing expense by ID.
  - `/expenses/<id>` (DELETE): Delete an expense by ID.
  - `/analytics/total` (GET): Calculate and return the total expenses.
  - `/analytics/category` (GET): Get expenses summarized by category.

### Error Handling
- Handles common errors such as missing fields in the request and database connection errors.

### Usage
Run the script, and it will start a server that you can interact with using tools like Postman or CURL, or by integrating with a front-end framework.

This backend is kept basic for illustration and would need to be expanded for a complete solution, including user authentication, more robust data validation, and potentially more sophisticated analytics.