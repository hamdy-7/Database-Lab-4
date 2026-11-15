import os
from flask import Flask, render_template, request, redirect, url_for
import pymysql
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mysecretkey123')

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'library_db'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return redirect(url_for('search_books'))

@app.route('/search', methods=['GET'])
def search_books():
    title_query = request.args.get('title', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    category_id = request.args.get('category_id', '')

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM CATEGORY")
        categories = cursor.fetchall()

        sql = """
            SELECT B.book_id, B.title, B.price, B.publish_year, A.name AS author_name, C.name AS category_name
            FROM BOOK B
            JOIN AUTHOR A ON B.author_id = A.author_id
            JOIN CATEGORY C ON B.category_id = C.category_id
            WHERE 1=1
        """
        params = []

        if title_query:
            sql += " AND B.title LIKE %s"
            params.append(f"%{title_query}%")
        if min_price and max_price:
            sql += " AND B.price BETWEEN %s AND %s"
            params.append(float(min_price))
            params.append(float(max_price))
        elif min_price:
            sql += " AND B.price >= %s"
            params.append(float(min_price))
        elif max_price:
            sql += " AND B.price <= %s"
            params.append(float(max_price))
        if category_id:
            sql += " AND B.category_id = %s"
            params.append(int(category_id))

        sql += " ORDER BY B.price ASC"
        cursor.execute(sql, tuple(params))
        books = cursor.fetchall()
    conn.close()
    return render_template('search.html', books=books, categories=categories, 
                           title_query=title_query, min_price=min_price, 
                           max_price=max_price, category_id=category_id)

@app.route('/catalogue')
def catalogue():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT B.book_id, B.title, B.price, B.publish_year, A.name AS author_name, P.name AS publisher_name, C.name AS category_name
            FROM BOOK B
            JOIN AUTHOR A ON B.author_id = A.author_id
            JOIN PUBLISHER P ON B.publisher_id = P.publisher_id
            JOIN CATEGORY C ON B.category_id = C.category_id
            ORDER BY B.book_id ASC
        """)
        books = cursor.fetchall()
    conn.close()
    return render_template('catalogue.html', books=books)

@app.route('/reports')
def reports():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT C.name AS category_name, COUNT(B.book_id) AS total_books, IFNULL(AVG(B.price), 0) AS avg_price
            FROM CATEGORY C
            LEFT JOIN BOOK B ON C.category_id = B.category_id
            GROUP BY C.category_id, C.name
        """)
        category_stats = cursor.fetchall()

        cursor.execute("""
            SELECT A.name AS author_name, COUNT(B.book_id) AS books_written
            FROM AUTHOR A
            JOIN BOOK B ON A.author_id = B.author_id
            GROUP BY A.author_id, A.name
            HAVING COUNT(B.book_id) >= 2
        """)
        prolific_authors = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS total_books, IFNULL(SUM(price), 0) AS total_library_value, 
                   IFNULL(MIN(price), 0) AS min_price, IFNULL(MAX(price), 0) AS max_price
            FROM BOOK
        """)
        overall_stats = cursor.fetchone()
    conn.close()
    return render_template('reports.html', category_stats=category_stats, 
                           prolific_authors=prolific_authors, overall_stats=overall_stats)

@app.route('/loans')
def loans():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT L.loan_id, B.title AS book_title, M.name AS member_name, L.loan_date
            FROM LOAN L
            JOIN BOOK B ON L.book_id = B.book_id
            JOIN MEMBER M ON L.member_id = M.member_id
            WHERE L.return_date IS NULL
        """)
        active_loans = cursor.fetchall()

        cursor.execute("""
            SELECT M.member_id, M.name, M.email
            FROM MEMBER M
            LEFT JOIN LOAN L ON M.member_id = L.member_id
            WHERE L.loan_id IS NULL
        """)
        inactive_members = cursor.fetchall()

        cursor.execute("""
            SELECT B.book_id, B.title, B.price
            FROM BOOK B
            LEFT JOIN LOAN L ON B.book_id = L.book_id
            WHERE L.loan_id IS NULL
        """)
        unborrowed_books = cursor.fetchall()
    conn.close()
    return render_template('loans.html', active_loans=active_loans, 
                           inactive_members=inactive_members, unborrowed_books=unborrowed_books)

@app.route('/most-borrowed')
def most_borrowed():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT B.title AS book_title, COUNT(L.loan_id) AS times_borrowed
            FROM BOOK B
            JOIN LOAN L ON B.book_id = L.book_id
            GROUP BY B.book_id, B.title
            ORDER BY times_borrowed DESC
            LIMIT 3
        """)
        top_books = cursor.fetchall()

        cursor.execute("""
            SELECT M.name AS member_name, COUNT(L.loan_id) AS total_loans
            FROM MEMBER M
            JOIN LOAN L ON M.member_id = L.member_id
            GROUP BY M.member_id, M.name
            ORDER BY total_loans DESC
            LIMIT 1
        """)
        top_member = cursor.fetchone()
    conn.close()
    return render_template('most_borrowed.html', top_books=top_books, top_member=top_member)

@app.route('/authors-books')
def authors_books():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT A.name AS author_name, COUNT(B.book_id) AS books_count
            FROM AUTHOR A
            LEFT JOIN BOOK B ON A.author_id = B.author_id
            GROUP BY A.author_id, A.name
        """)
        authors_count = cursor.fetchall()

        cursor.execute("""
            SELECT B.title AS book_title, A.name AS author_name, A.country AS author_country, P.name AS publisher_name, P.country AS publisher_country
            FROM BOOK B
            JOIN AUTHOR A ON B.author_id = A.author_id
            JOIN PUBLISHER P ON B.publisher_id = P.publisher_id
            WHERE A.country = P.country
        """)
        same_country_books = cursor.fetchall()
    conn.close()
    return render_template('authors_books.html', authors_count=authors_count, 
                           same_country_books=same_country_books)

if __name__ == '__main__':
    app.run(debug=True)