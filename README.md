<h3>Invoice Management System </h3>

This project is a simple Invoice Management System built using Python’s Flask framework, the Peewee ORM, SQLite for storage, and Tailwind CSS for styling. It also uses WeasyPrint to generate professional-looking PDF invoices. The purpose of this project is to show how a small but complete web application can be built from scratch. It combines database models, CRUD operations, templates, and styling into one system.

The system is designed for small businesses, freelancers, or anyone who wants to manage invoices without depending on external software. The features are kept simple but still demonstrate many of the same principles used in larger, professional applications.

<h3>What the Project Does</h3>

The application allows users to:

Add customers with their name, email, and address.

Create invoices automatically when a new customer is added.

Add items to invoices, including description, quantity, and price.

Update totals for invoices whenever items are created, updated, or deleted.

Edit or delete both customers and items.

List invoices and view them either on the web or as downloadable PDF files.

Use a clean interface that works on different screen sizes and feels modern thanks to Tailwind CSS.

The end result is a small web-based invoice manager that you can run locally.

<h3>File Explanations</h3>

This project has a few key files and folders that each serve a clear purpose:

app.py
The main Python application. This file sets up the database, defines the models (Customer, Invoice, and Item), and creates the Flask routes for every action. Examples include the dashboard, invoice pages, and the routes to add, edit, or delete customers and items. It also handles the logic of keeping invoice totals up to date and generating PDFs.

templates/base.html
The base layout used by all other HTML pages. It includes the Tailwind CSS link and a navigation section, and defines a block called {% block content %}. Other templates extend this file, so the look and feel remain consistent across the whole application.

templates/dashboard.html
The homepage of the app. It shows a list of customers on one side, recent items on another, and also provides forms for adding new customers or items. This is the main “control center” of the app.

templates/edit_customer.html
A simple page for updating an existing customer’s information. It extends base.html and includes a form for name, email, and address.

templates/edit_item.html
Similar to the customer edit page, but for invoice items. Here you can update the description, quantity, and price of an item.

templates/invoice.html
A page that lists all invoices in the system. From here, you can view an invoice in your browser or download it as a PDF.

templates/invoice_pdf.html
A special template used to display a single invoice. It shows the customer, the list of items, quantities, and totals. This file is also used by WeasyPrint to generate the PDF version, meaning the browser and PDF versions look the same.

invoices.db
The SQLite database file. This is where all your customers, invoices, and items are stored. It is created automatically the first time you run the app.

Design Choices

While building this project, a few design decisions had to be made:

Database and ORM
I chose Peewee because it is much lighter and easier to read than something like SQLAlchemy. SQLite was chosen because it is built into Python, requires no setup, and is perfect for small projects.

PDF Generation
WeasyPrint was selected because it allows the use of normal HTML and CSS to design invoices. This is simpler than creating PDFs manually, and it guarantees that the on-screen and printed versions match.

UI with Tailwind CSS
Instead of writing custom CSS, I used Tailwind. It is included through a CDN, so there’s no need for a build process. Tailwind provides utility classes for spacing, colors, and responsiveness, which makes the app look modern with very little extra code.

Stored Totals
Invoice totals are saved in the database but recalculated every time items are added, edited, or deleted. This makes queries faster, while still ensuring totals stay correct.

Simplicity
The project avoids advanced features like user authentication or form validation libraries. This keeps the code short and easy for beginners to understand. In a production app, those features would definitely be required.
