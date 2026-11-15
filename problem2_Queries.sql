USE library_db;

SELECT B.book_id, B.title, B.price, B.publish_year, A.name AS author_name, C.name AS category_name
FROM BOOK B
JOIN AUTHOR A ON B.author_id = A.author_id
JOIN CATEGORY C ON B.category_id = C.category_id
WHERE B.title LIKE '%Palace%' AND B.price BETWEEN 10 AND 25 AND B.category_id = 1
ORDER BY B.price ASC;

SELECT B.book_id, B.title, B.price, B.publish_year, A.name AS author_name, P.name AS publisher_name, C.name AS category_name
FROM BOOK B
JOIN AUTHOR A ON B.author_id = A.author_id
JOIN PUBLISHER P ON B.publisher_id = P.publisher_id
JOIN CATEGORY C ON B.category_id = C.category_id
ORDER BY B.book_id ASC;

SELECT C.name AS category_name, COUNT(B.book_id) AS total_books, AVG(B.price) AS avg_price
FROM CATEGORY C
LEFT JOIN BOOK B ON C.category_id = B.category_id
GROUP BY C.category_id, C.name;

SELECT A.name AS author_name, COUNT(B.book_id) AS books_written
FROM AUTHOR A
JOIN BOOK B ON A.author_id = B.author_id
GROUP BY A.author_id, A.name
HAVING COUNT(B.book_id) >= 2;

SELECT COUNT(*) AS total_books, SUM(price) AS total_library_value, MIN(price) AS min_price, MAX(price) AS max_price
FROM BOOK;

SELECT L.loan_id, B.title AS book_title, M.name AS member_name, L.loan_date
FROM LOAN L
JOIN BOOK B ON L.book_id = B.book_id
JOIN MEMBER M ON L.member_id = M.member_id
WHERE L.return_date IS NULL;

SELECT M.member_id, M.name, M.email
FROM MEMBER M
LEFT JOIN LOAN L ON M.member_id = L.member_id
WHERE L.loan_id IS NULL;

SELECT B.book_id, B.title, B.price
FROM BOOK B
LEFT JOIN LOAN L ON B.book_id = L.book_id
WHERE L.loan_id IS NULL;

SELECT B.title AS book_title, COUNT(L.loan_id) AS times_borrowed
FROM BOOK B
JOIN LOAN L ON B.book_id = L.book_id
GROUP BY B.book_id, B.title
ORDER BY times_borrowed DESC
LIMIT 3;

SELECT M.name AS member_name, COUNT(L.loan_id) AS total_loans
FROM MEMBER M
JOIN LOAN L ON M.member_id = L.member_id
GROUP BY M.member_id, M.name
ORDER BY total_loans DESC
LIMIT 1;

SELECT A.name AS author_name, COUNT(B.book_id) AS books_count
FROM AUTHOR A
LEFT JOIN BOOK B ON A.author_id = B.author_id
GROUP BY A.author_id, A.name;

SELECT B.title AS book_title, A.name AS author_name, A.country AS author_country, P.name AS publisher_name, P.country AS publisher_country
FROM BOOK B
JOIN AUTHOR A ON B.author_id = A.author_id
JOIN PUBLISHER P ON B.publisher_id = P.publisher_id
WHERE A.country = P.country;