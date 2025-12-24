"""Initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2025-12-24

This project originally shipped without a `migrations/versions` folder.
This migration creates the initial tables.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "brand",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=30), nullable=False, unique=True),
    )

    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=30), nullable=False, unique=True),
    )

    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False, unique=True),
        sa.Column("email", sa.String(length=120)),
        sa.Column("password", sa.String(length=180), nullable=False),
    )

    op.create_table(
        "register",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False, unique=True),
        sa.Column("email", sa.String(length=120), unique=True),
        sa.Column("password", sa.String(length=180), nullable=False),
        sa.Column("country", sa.String(length=20)),
        sa.Column("city", sa.String(length=20)),
        sa.Column("contact", sa.Integer()),
        sa.Column("address", sa.String(length=40)),
        sa.Column("zipcode", sa.Integer()),
        sa.Column("profile", sa.String(length=200), server_default="profile.jpg"),
        sa.Column("date_create", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "addproduct",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("discount", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.Column("colors", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("pub_date", sa.DateTime(), nullable=False),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("category.id"), nullable=False),
        sa.Column("brand_id", sa.Integer(), sa.ForeignKey("brand.id"), nullable=False),
        sa.Column("image_1", sa.String(length=180), nullable=False, server_default="image.jpg"),
        sa.Column("image_2", sa.String(length=180), nullable=False, server_default="image.jpg"),
        sa.Column("image_3", sa.String(length=180), nullable=False, server_default="image.jpg"),
    )

    op.create_index("ix_addproduct_name", "addproduct", ["name"])

    op.create_table(
        "customer_order",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("invoice", sa.String(length=20), nullable=False, unique=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="Pending"),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.Column("orders", sa.Text()),
    )


def downgrade():
    op.drop_table("customer_order")
    op.drop_index("ix_addproduct_name", table_name="addproduct")
    op.drop_table("addproduct")
    op.drop_table("register")
    op.drop_table("user")
    op.drop_table("category")
    op.drop_table("brand")
