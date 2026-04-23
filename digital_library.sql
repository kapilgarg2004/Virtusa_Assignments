-- Digital Library Audit


-- TABLE CREATION

CREATE TABLE Books (
    book_id     INT PRIMARY KEY,
    title       VARCHAR(100),
    author      VARCHAR(100),
    category    VARCHAR(50)
);

CREATE TABLE Students (
    student_id  INT PRIMARY KEY,
    name        VARCHAR(100),
    email       VARCHAR(100),
    joined_date DATE
);

CREATE TABLE IssuedBooks (
    issue_id    INT PRIMARY KEY,
    book_id     INT,
    student_id  INT,
    issue_date  DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);


-- SAMPLE DATA

INSERT INTO Books VALUES (1, 'The Great Gatsby',         'F. Scott Fitzgerald', 'Fiction');
INSERT INTO Books VALUES (2, 'A Brief History of Time',  'Stephen Hawking',     'Science');
INSERT INTO Books VALUES (3, 'Sapiens',                  'Yuval Noah Harari',   'History');
INSERT INTO Books VALUES (4, 'Clean Code',               'Robert C. Martin',    'Technology');
INSERT INTO Books VALUES (5, 'To Kill a Mockingbird',    'Harper Lee',          'Fiction');
INSERT INTO Books VALUES (6, 'Cosmos',                   'Carl Sagan',          'Science');
INSERT INTO Books VALUES (7, 'The Art of War',           'Sun Tzu',             'History');
INSERT INTO Books VALUES (8, 'Harry Potter',             'J.K. Rowling',        'Fiction');

INSERT INTO Students VALUES (1, 'Aryan Mehta',   'aryan@college.edu',   '2022-06-01');
INSERT INTO Students VALUES (2, 'Priya Sharma',  'priya@college.edu',   '2021-03-15');
INSERT INTO Students VALUES (3, 'Rohan Verma',   'rohan@college.edu',   '2020-01-10');
INSERT INTO Students VALUES (4, 'Sneha Patil',   'sneha@college.edu',   '2023-07-20');
INSERT INTO Students VALUES (5, 'Karan Joshi',   'karan@college.edu',   '2019-08-05');
INSERT INTO Students VALUES (6, 'Divya Nair',    'divya@college.edu',   '2022-11-30');

INSERT INTO IssuedBooks VALUES (1,  1, 1, CURRENT_DATE - 20, NULL);
INSERT INTO IssuedBooks VALUES (2,  2, 2, CURRENT_DATE - 10, CURRENT_DATE - 2);
INSERT INTO IssuedBooks VALUES (3,  3, 3, CURRENT_DATE - 16, NULL);
INSERT INTO IssuedBooks VALUES (4,  4, 4, CURRENT_DATE - 5,  NULL);
INSERT INTO IssuedBooks VALUES (5,  5, 1, CURRENT_DATE - 30, NULL);
INSERT INTO IssuedBooks VALUES (6,  6, 5, CURRENT_DATE - 3,  CURRENT_DATE - 1);
INSERT INTO IssuedBooks VALUES (7,  1, 6, CURRENT_DATE - 18, NULL);
INSERT INTO IssuedBooks VALUES (8,  8, 2, CURRENT_DATE - 7,  NULL);
INSERT INTO IssuedBooks VALUES (9,  3, 3, '2021-05-01',       '2021-05-10');
INSERT INTO IssuedBooks VALUES (10, 7, 5, '2020-03-01',       '2020-03-12');


-- QUERY 1: OVERDUE BOOKS
-- Students who have not returned a book issued more than 14 days ago

SELECT
    s.student_id,
    s.name,
    s.email,
    b.title,
    b.category,
    ib.issue_date,
    (CURRENT_DATE - ib.issue_date) AS days_overdue
FROM IssuedBooks ib
JOIN Students s ON ib.student_id = s.student_id
JOIN Books b    ON ib.book_id    = b.book_id
WHERE ib.return_date IS NULL
  AND ib.issue_date < CURRENT_DATE - 14
ORDER BY days_overdue DESC;


-- QUERY 2: POPULARITY INDEX
-- Which category of books is borrowed the most

SELECT
    b.category,
    COUNT(ib.issue_id) AS total_borrows
FROM IssuedBooks ib
JOIN Books b ON ib.book_id = b.book_id
GROUP BY b.category
ORDER BY total_borrows DESC;


-- QUERY 3: PENALTY REPORT
-- Fine of $1 per day for every day overdue beyond 14 days

SELECT
    s.name,
    s.email,
    b.title,
    ib.issue_date,
    (CURRENT_DATE - ib.issue_date)        AS days_held,
    (CURRENT_DATE - ib.issue_date) - 14   AS days_overdue,
    ((CURRENT_DATE - ib.issue_date) - 14) AS penalty_amount
FROM IssuedBooks ib
JOIN Students s ON ib.student_id = s.student_id
JOIN Books b    ON ib.book_id    = b.book_id
WHERE ib.return_date IS NULL
  AND ib.issue_date < CURRENT_DATE - 14
ORDER BY penalty_amount DESC;


-- QUERY 4: INACTIVE ACCOUNTS
-- Students who have not borrowed any book in over 3 years

SELECT
    s.student_id,
    s.name,
    s.email,
    MAX(ib.issue_date) AS last_borrow_date
FROM Students s
LEFT JOIN IssuedBooks ib ON s.student_id = ib.student_id
GROUP BY s.student_id, s.name, s.email
HAVING MAX(ib.issue_date) < CURRENT_DATE - (3 * 365)
    OR MAX(ib.issue_date) IS NULL
ORDER BY last_borrow_date ASC;


-- CLEANUP: Remove inactive student records

DELETE FROM Students
WHERE student_id IN (
    SELECT s.student_id
    FROM Students s
    LEFT JOIN IssuedBooks ib ON s.student_id = ib.student_id
    GROUP BY s.student_id
    HAVING MAX(ib.issue_date) < CURRENT_DATE - (3 * 365)
        OR MAX(ib.issue_date) IS NULL
);
