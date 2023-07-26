# NBA Data Analysis Project

## Description
In this project, we leverage SQL queries to derive interesting insights from an NBA dataset, including answers to some hot debates such as the real GOAT in NBA. The project involves creating a MySQL database from multiple CSV files, creating tables based on an ER diagram, and executing complex SQL queries to uncover meaningful patterns.

## Installation
Ensure you have a Python environment with MySQL connector installed. You'll also need access to MySQL Workbench. The Python script provided in the repository uses MySQL connector to interact with the MySQL database.

## Project Motivation
We aim to demonstrate the power of SQL in extracting meaningful information from a seemingly simple dataset. This project is a testament to how relational databases can serve as powerful tools for data analysts and sports enthusiasts alike.

## File Description
The project contains a Python script (`main.py`), several SQL scripts (`Queries.sql` and `SQLCODE.sql`), and a collection of CSV files representing different entities in the NBA dataset. There are also two versions of an ER diagram, one with all attributes and a simplified one for better readability.

## How To Interact With This Project
Here are the instructions on how to interact with the project:
1. Clone the repository and navigate to the folder named `NBA_project`.
2. Open the file `main.py` and enter your MySQL password at lines 31 and 41.
3. Run the `main.py` script.
4. View the output of the queries in the Python terminal.
  
**Alternative Method 1:**
You can also directly run the `Queries.sql` in MySQL Workbench after executing `main.py` with lines 256 onwards commented out.

**Alternative Method 2:**
For the entire SQL process except for inserting CSV values, use the `SQLCODE.sql` script. Before running this script, comment out line 36 and lines 53 to 148 in `main.py`. 

## Licensing, Authors, Acknowledgements
This project is licensed under the MIT license. All contributions to this project are acknowledged in the Contributors section of the repository.

## Acknowledgements
The CSV files used in this project can be found in the `NBA_data` folder.

Please remember to drop the schema in MySQL Workbench before testing the next method if you're testing all methods. Enjoy diving into the world of NBA data analysis!

