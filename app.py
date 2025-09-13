from flask import Flask, render_template, request, redirect, url_for, send_file
from peewee import *
from datetime import date
from weasyprint import HTML
import io

# ---------------- DATABASE SETUP ----------------
db = SqliteDatabase("invoices.db")

class BaseModel(Model):
    class Meta:
        database = db

class Customer(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    address = CharField()

class Invoice(BaseModel):
    customer = ForeignKeyField(Customer, backref="invoices", on_delete="CASCADE")
    date = DateField()
    total = DecimalField(decimal_places=2, default=0)

class Item(BaseModel):
    invoice = ForeignKeyField(Invoice, backref="items", on_delete="CASCADE")
    description = CharField()
    quantity = IntegerField()
    price = DecimalField(decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price

# Create database tables
db.connect()
db.create_tables([Customer, Invoice, Item])

# ---------------- FLASK APP ----------------
app = Flask(__name__)

# ---------------- HOME / DASHBOARD ----------------
@app.route("/", methods=["GET", "POST"])
def dashboard():
    error = None

    if request.method == "POST":
        form_type = request.form.get("form_type")

        # ---- ADD CUSTOMER ----
        if form_type == "customer":
            name = request.form.get("name")
            email = request.form.get("email")
            address = request.form.get("address")

            if not (name and email and address):
                error = "Please fill all customer fields!"
            elif Customer.select().where(Customer.email == email).exists():
                error = "Email already exists!"
            else:
                customer = Customer.create(name=name, email=email, address=address)
                Invoice.create(customer=customer, date=date.today(), total=0)

        # ---- ADD ITEM ----
        elif form_type == "item":
            customer_id = request.form.get("customer_id")
            description = request.form.get("description")
            quantity = request.form.get("quantity")
            price = request.form.get("price")

            if not (customer_id and description and quantity and price):
                error = "Please fill all item fields!"
            else:
                try:
                    invoice = Invoice.get(Invoice.customer == int(customer_id))
                    Item.create(
                        invoice=invoice,
                        description=description,
                        quantity=int(quantity),
                        price=float(price)
                    )
                    invoice.total = sum(i.subtotal for i in invoice.items)
                    invoice.save()
                    return redirect(url_for("dashboard"))
                except Exception:
                    error = "Something went wrong when adding item."

        # ---- EDIT CUSTOMER ----
        elif form_type == "edit_customer":
            cid = request.form.get("customer_id")
            try:
                customer = Customer.get_by_id(int(cid))
                name = request.form.get("name")
                email = request.form.get("email")
                address = request.form.get("address")

                if Customer.select().where(
                    (Customer.email == email) & (Customer.id != customer.id)
                ).exists():
                    error = "Email already exists!"
                else:
                    customer.name = name
                    customer.email = email
                    customer.address = address
                    customer.save()
            except Exception:
                error = "Customer not found!"

        # ---- EDIT ITEM ----
        elif form_type == "edit_item":
            iid = request.form.get("item_id")
            try:
                item = Item.get_by_id(int(iid))
                item.description = request.form.get("description")
                item.quantity = int(request.form.get("quantity"))
                item.price = float(request.form.get("price"))
                item.save()

                # Update total
                invoice = item.invoice
                invoice.total = sum(i.subtotal for i in invoice.items)
                invoice.save()
            except Exception:
                error = "Item not found!"

    # Fetch all data for display
    customers = Customer.select()
    items = Item.select()
    return render_template("dashboard.html", customers=customers, items=items, error=error, date=date)


# ---------------- EDIT PAGES (MODAL STYLE MERGED) ----------------
@app.route("/edit/customer/<int:id>", methods=["GET", "POST"])
def edit_customer_page(id):
    customer = Customer.get_or_none(Customer.id == id)
    if not customer:
        return "Customer not found", 404
    if request.method == "POST":
        customer.name = request.form.get("name")
        customer.email = request.form.get("email")
        customer.address = request.form.get("address")
        customer.save()
        return redirect(url_for("dashboard"))
    return render_template("edit_customer.html", customer=customer)

@app.route("/edit/item/<int:id>", methods=["GET", "POST"])
def edit_item_page(id):
    item = Item.get_or_none(Item.id == id)
    if not item:
        return "Item not found", 404
    if request.method == "POST":
        item.description = request.form.get("description")
        item.quantity = int(request.form.get("quantity"))
        item.price = float(request.form.get("price"))
        item.save()
        invoice = item.invoice
        invoice.total = sum(i.subtotal for i in invoice.items)
        invoice.save()
        return redirect(url_for("dashboard"))
    return render_template("edit_item.html", item=item)


# ---------------- INVOICE LIST ----------------
@app.route("/invoice")
def invoice_page():
    invoices = Invoice.select()
    return render_template("invoice.html", invoices=invoices)

# ---------------- VIEW & DOWNLOAD PDF ----------------
@app.route("/invoice/view/<int:id>")
def invoice_view(id):
    try:
        invoice = Invoice.get_by_id(id)
        html = render_template("invoice_pdf.html", invoice=invoice, items=invoice.items)
        return html
    except Invoice.DoesNotExist:
        return "Invoice not found", 404

@app.route("/invoice/pdf/<int:id>")
def invoice_pdf(id):
    try:
        invoice = Invoice.get_by_id(id)
        html = render_template("invoice_pdf.html", invoice=invoice, items=invoice.items)
        pdf = HTML(string=html).write_pdf()
        return send_file(
            io.BytesIO(pdf),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"invoice_{id}.pdf"
        )
    except Invoice.DoesNotExist:
        return "Invoice not found", 404

# ---------------- DELETE ROUTES ----------------
@app.route("/customer/delete/<int:id>")
def delete_customer(id):
    try:
        customer = Customer.get_by_id(id)
        customer.delete_instance(recursive=True)
    except Customer.DoesNotExist:
        pass
    return redirect(url_for("dashboard"))

@app.route("/item/delete/<int:id>")
def delete_item(id):
    try:
        item = Item.get_by_id(id)
        invoice = item.invoice
        item.delete_instance()
        invoice.total = sum(i.subtotal for i in invoice.items)
        invoice.save()
    except Item.DoesNotExist:
        pass
    return redirect(url_for("dashboard"))

@app.route("/invoice/delete/<int:id>")
def delete_invoice(id):
    try:
        invoice = Invoice.get_by_id(id)
        invoice.delete_instance(recursive=True)
    except Invoice.DoesNotExist:
        pass
    return redirect(url_for("invoice_page"))

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
