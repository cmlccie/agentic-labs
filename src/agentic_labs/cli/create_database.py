"""Create database command — generates a sample SQLite database with fake data for the database agent lab."""

import logging
import random
import sqlite3
from pathlib import Path
from typing import Annotated

import click
import typer
from faker import Faker

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = Path("labs/pydantic-ai/database.db")
NUM_CUSTOMERS = 50
NUM_PRODUCTS = 20
NUM_PURCHASES = 200


def create_database(
    path: Annotated[
        Path,
        typer.Option(
            "--path",
            "-p",
            help="Path where the SQLite database file will be created.",
        ),
    ] = DEFAULT_DB_PATH,
) -> None:
    """Create a sample SQLite database with fake customers, products, and purchases data.

    Generates and populates three tables:
    - customers: personal and contact information for fake customers.
    - products: product catalog with SKUs, descriptions, and pricing.
    - purchases: purchase history linking customers to products.

    Args:
        path: Filesystem path for the output SQLite database file. Parent directories
            are created automatically if they do not already exist. Any existing file
            at the given path is removed before the new database is written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        path.unlink()
        click.echo(f"Removed existing database at {path}")

    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    conn = sqlite3.connect(path)
    try:
        conn.executescript("""
            CREATE TABLE customers (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name      TEXT NOT NULL,
                last_name       TEXT NOT NULL,
                birth_date      TEXT NOT NULL,
                street_address  TEXT NOT NULL,
                city            TEXT NOT NULL,
                state           TEXT NOT NULL,
                zip_code        TEXT NOT NULL,
                email           TEXT NOT NULL UNIQUE,
                phone_number    TEXT NOT NULL
            );

            CREATE TABLE products (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                sku             TEXT NOT NULL UNIQUE,
                name            TEXT NOT NULL,
                description     TEXT NOT NULL,
                cost            REAL NOT NULL,
                in_stock_qty    INTEGER NOT NULL
            );

            CREATE TABLE purchases (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id     INTEGER NOT NULL REFERENCES customers(id),
                product_id      INTEGER NOT NULL REFERENCES products(id),
                qty_purchased   INTEGER NOT NULL,
                purchase_date   TEXT NOT NULL
            );
        """)

        customers = [
            (
                fake.first_name(),
                fake.last_name(),
                fake.date_of_birth(minimum_age=18, maximum_age=85).isoformat(),
                fake.street_address(),
                fake.city(),
                fake.state_abbr(),
                fake.zipcode(),
                fake.unique.email(),
                fake.phone_number(),
            )
            for _ in range(NUM_CUSTOMERS)
        ]
        conn.executemany(
            """INSERT INTO customers
               (first_name, last_name, birth_date, street_address, city, state, zip_code, email, phone_number)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            customers,
        )

        products = [
            (
                fake.bothify(text="SKU-####-???").upper(),
                fake.catch_phrase(),
                fake.sentence(nb_words=12),
                round(random.uniform(4.99, 299.99), 2),
                random.randint(0, 500),
            )
            for _ in range(NUM_PRODUCTS)
        ]
        conn.executemany(
            "INSERT INTO products (sku, name, description, cost, in_stock_qty) VALUES (?, ?, ?, ?, ?)",
            products,
        )

        purchases = [
            (
                random.randint(1, NUM_CUSTOMERS),
                random.randint(1, NUM_PRODUCTS),
                random.randint(1, 5),
                fake.date_between(start_date="-2y", end_date="today").isoformat(),
            )
            for _ in range(NUM_PURCHASES)
        ]
        conn.executemany(
            "INSERT INTO purchases (customer_id, product_id, qty_purchased, purchase_date) VALUES (?, ?, ?, ?)",
            purchases,
        )

        conn.commit()
        logger.info("Created database at %s", path)

    except Exception as e:
        logger.error("Failed to create database: %s", e)
        click.echo(f"Error: Failed to create database: {e}", err=True)
        raise typer.Exit(1) from e
    finally:
        conn.close()

    click.echo(f"Created database at {path}")
    click.echo(f"  {NUM_CUSTOMERS} customers")
    click.echo(f"  {NUM_PRODUCTS} products")
    click.echo(f"  {NUM_PURCHASES} purchases")
