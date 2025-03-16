from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import erdantic as erd
import json

# Define models with SQLAlchemy-style relationships
class User(BaseModel):
    user_id: int = Field(primary_key=True)
    email: str
    password_hash: str
    first_name: str
    last_name: str
    created_at: datetime
    last_login: Optional[datetime] = None
    sustainability_preferences: Dict[str, Any]

    # Relationships
    sessions: List["UserSession"] = Field(default_factory=list)
    activities: List["UserActivity"] = Field(default_factory=list)
    orders: List["Order"] = Field(default_factory=list)
    reviews: List["ProductReview"] = Field(default_factory=list)
    audit_logs: List["DatabaseAuditLog"] = Field(default_factory=list)

class UserSession(BaseModel):
    session_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="User.user_id")
    login_time: datetime
    last_activity: datetime
    ip_address: str
    device_info: str

    # Relationships
    user: User = Field(None, back_populates="sessions")

class UserActivity(BaseModel):
    activity_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="User.user_id")
    activity_type: str
    timestamp: datetime
    details: Dict[str, Any]

    # Relationships
    user: User = Field(None, back_populates="activities")

class Country(BaseModel):
    country_id: int = Field(primary_key=True)
    name: str

    # Relationships
    brands: List["Brand"] = Field(default_factory=list)

class Brand(BaseModel):
    brand_id: int = Field(primary_key=True)
    name: str
    description: str
    founded_year: int
    sustainability_statement: str
    headquarters_country_id: int = Field(foreign_key="Country.country_id")

    # Relationships
    products: List["Product"] = Field(default_factory=list)
    certifications: List["BrandCertification"] = Field(default_factory=list)
    country: Country = Field(None, back_populates="brands")

class ProductCategory(BaseModel):
    category_id: int = Field(primary_key=True)
    parent_category_id: Optional[int] = Field(None, foreign_key="ProductCategory.category_id")
    name: str
    description: str

    # Relationships
    products: List["Product"] = Field(default_factory=list)
    subcategories: List["ProductCategory"] = Field(default_factory=list)
    parent_category: Optional["ProductCategory"] = Field(None, back_populates="subcategories")

class Certification(BaseModel):
    certification_id: int = Field(primary_key=True)
    name: str
    issuing_organization: str
    description: str
    verification_process: str
    website_url: str

    # Relationships
    product_certifications: List["ProductCertification"] = Field(default_factory=list)
    brand_certifications: List["BrandCertification"] = Field(default_factory=list)

class Product(BaseModel):
    product_id: int = Field(primary_key=True)
    brand_id: int = Field(foreign_key="Brand.brand_id")
    category_id: int = Field(foreign_key="ProductCategory.category_id")
    name: str
    description: str
    price: Decimal
    cost: Decimal
    stock_quantity: int
    carbon_footprint: Decimal
    created_at: datetime
    updated_at: datetime

    # Relationships
    brand: Brand = Field(None, back_populates="products")
    category: ProductCategory = Field(None, back_populates="products")
    certifications: List["ProductCertification"] = Field(default_factory=list)
    order_items: List["OrderItem"] = Field(default_factory=list)
    reviews: List["ProductReview"] = Field(default_factory=list)

class ProductCertification(BaseModel):
    product_certification_id: int = Field(primary_key=True)
    product_id: int = Field(foreign_key="Product.product_id")
    certification_id: int = Field(foreign_key="Certification.certification_id")
    issue_date: datetime
    expiration_date: datetime
    verification_document_url: str
    verification_status: str

    # Relationships
    product: Product = Field(None, back_populates="certifications")
    certification: Certification = Field(None, back_populates="product_certifications")

class BrandCertification(BaseModel):
    brand_certification_id: int = Field(primary_key=True)
    brand_id: int = Field(foreign_key="Brand.brand_id")
    certification_id: int = Field(foreign_key="Certification.certification_id")
    issue_date: datetime
    expiration_date: datetime
    verification_document_url: str
    verification_status: str

    # Relationships
    brand: Brand = Field(None, back_populates="certifications")
    certification: Certification = Field(None, back_populates="brand_certifications")

class Address(BaseModel):
    address_id: int = Field(primary_key=True)
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country_id: int = Field(foreign_key="Country.country_id")

    # Relationships
    orders: List["Order"] = Field(default_factory=list)

class PaymentMethod(BaseModel):
    payment_method_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="User.user_id")
    method_type: str
    details: Dict[str, Any]

    # Relationships
    orders: List["Order"] = Field(default_factory=list)

class Order(BaseModel):
    order_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="User.user_id")
    order_date: datetime
    shipping_address_id: int = Field(foreign_key="Address.address_id")
    payment_method_id: int = Field(foreign_key="PaymentMethod.payment_method_id")
    status: str
    total_amount: Decimal
    carbon_offset_amount: Decimal

    # Relationships
    user: User = Field(None, back_populates="orders")
    shipping_address: Address = Field(None, back_populates="orders")
    payment_method: PaymentMethod = Field(None, back_populates="orders")
    items: List["OrderItem"] = Field(default_factory=list)

class OrderItem(BaseModel):
    order_item_id: int = Field(primary_key=True)
    order_id: int = Field(foreign_key="Order.order_id")
    product_id: int = Field(foreign_key="Product.product_id")
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    # Relationships
    order: Order = Field(None, back_populates="items")
    product: Product = Field(None, back_populates="order_items")

class ProductReview(BaseModel):
    review_id: int = Field(primary_key=True)
    product_id: int = Field(foreign_key="Product.product_id")
    user_id: int = Field(foreign_key="User.user_id")
    rating: int
    sustainability_rating: int
    review_text: str
    created_at: datetime
    helpful_votes: int

    # Relationships
    product: Product = Field(None, back_populates="reviews")
    user: User = Field(None, back_populates="reviews")

class DatabaseAuditLog(BaseModel):
    log_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="User.user_id")
    action_type: str
    table_affected: str
    record_id: int
    timestamp: datetime
    ip_address: str

    # Relationships
    user: User = Field(None, back_populates="audit_logs")

class PerformanceMetric(BaseModel):
    metric_id: int = Field(primary_key=True)
    metric_type: str
    value: Decimal
    timestamp: datetime
    details: Dict[str, Any]

def main():
    # Create the diagram
    diagram = erd.create(
        User,
        UserSession,
        UserActivity,
        Country,
        Brand,
        ProductCategory,
        Certification,
        Product,
        ProductCertification,
        BrandCertification,
        Address,
        PaymentMethod,
        Order,
        OrderItem,
        ProductReview,
        DatabaseAuditLog,
        PerformanceMetric
    )

    # Save the diagram to various formats
    diagram.draw("sustainable_ecommerce_erd.png")
    diagram.draw("sustainable_ecommerce_erd.pdf")

    # You can also generate a dot file for further customization
    diagram.write_dot("sustainable_ecommerce_erd.dot")

    print("ERD diagram has been generated successfully!")

if __name__ == "__main__":
    main()
