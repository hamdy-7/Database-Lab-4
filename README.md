# Lab 4 - Database Systems (Part II Solution)

This repository contains the complete implementation for Lab 4 - Part II, including multi-table DDL schemas, complex seeded DML scripts, SQL query analytics, and a Premium Glassmorphic Web Dashboard built with Flask and MySQL.

## Structure
- `problem2_DDL.sql` - Database schema (6 Tables with ON DELETE CASCADE)
- `problem2_DML.sql` - Seed data (Authors, Publishers, Categories, Books, Members, Loans)
- `problem2_Queries.sql` - Standalone SQL queries for F2.1 to F2.6
- `website/` - Flask Web Application
  - `app.py` - Flask server with parameterized queries (Bonus)
  - `templates/` - Glassmorphic UI templates

## Setup & Execution
1. Execute `problem2_DDL.sql` and `problem2_DML.sql` in DBeaver / MySQL Client.
2. Navigate to the website folder:
   ```bash
   cd website