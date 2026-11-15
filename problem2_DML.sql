USE library_db;

INSERT INTO AUTHOR (author_id, name, country, photo_url) VALUES 
(1, 'Naguib Mahfouz', 'Egypt', NULL),
(2, 'Taha Hussein', 'Egypt', NULL),
(3, 'William Shakespeare', 'UK', NULL),
(4, 'Haruki Murakami', 'Japan', NULL);

INSERT INTO PUBLISHER (publisher_id, name, country) VALUES 
(1, 'Dar El Shorouk', 'Egypt'),
(2, 'Penguin Books', 'UK'),
(3, 'O''Reilly Media', 'USA');

INSERT INTO CATEGORY (category_id, name) VALUES 
(1, 'Fiction'),
(2, 'History'),
(3, 'Drama');

INSERT INTO BOOK (book_id, title, price, publish_year, author_id, publisher_id, category_id, cover_url) VALUES 
(1, 'Palace Walk', 18.50, 1956, 1, 1, 1, NULL),
(2, 'Sugar Street', 16.00, 1957, 1, 1, 1, NULL),
(3, 'Midaq Alley', 22.00, 1947, 1, 1, 1, NULL),
(4, 'The Days', 12.00, 1929, 2, 1, 2, NULL),
(5, 'The Future of Culture in Egypt', 14.25, 1938, 2, 1, 2, NULL),
(6, 'Hamlet', 20.00, 1603, 3, 2, 3, NULL),
(7, 'Macbeth', 22.50, 1606, 3, 2, 3, NULL),
(8, 'Othello', 19.99, 1604, 3, 2, 3, NULL),
(9, 'Romeo and Juliet', 15.00, 1597, 3, 2, 3, NULL),
(10, 'King Lear', 25.00, 1606, 3, 2, 3, NULL);

INSERT INTO MEMBER (member_id, name, email, join_date) VALUES 
(1, 'Hamdy Mabrouk', 'hamdy@example.com', '2025-01-10'),
(2, 'Ahmed Ali', 'ahmed@example.com', '2025-02-15'),
(3, 'Sara Mohamed', 'sara@example.com', '2025-03-01'),
(4, 'Omar Hassan', 'omar@example.com', '2025-04-10'),
(5, 'Nour Ebrahim', 'nour@example.com', '2025-05-20');

INSERT INTO LOAN (loan_id, book_id, member_id, loan_date, return_date) VALUES 
(1, 1, 1, '2026-01-01', '2026-01-10'),
(2, 1, 2, '2026-01-12', '2026-01-20'),
(3, 1, 3, '2026-02-01', '2026-02-10'),
(4, 2, 1, '2026-02-05', '2026-02-15'),
(5, 2, 2, '2026-02-16', '2026-02-25'),
(6, 3, 1, '2026-03-01', '2026-03-10'),
(7, 4, 3, '2026-03-05', '2026-03-15'),
(8, 6, 1, '2026-03-12', '2026-03-22'),
(9, 6, 4, '2026-04-01', '2026-04-10'),
(10, 7, 2, '2026-04-05', '2026-04-15'),
(11, 8, 1, '2026-04-18', '2026-04-28'),
(12, 6, 1, '2026-05-01', NULL);