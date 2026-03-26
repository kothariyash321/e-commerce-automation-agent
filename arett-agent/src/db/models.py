from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class ItemMaster(Base):
    __tablename__ = 'item_master'
    item_number: Mapped[str] = mapped_column(String(30), primary_key=True)
    description: Mapped[str | None] = mapped_column(Text)
    upc: Mapped[str | None] = mapped_column(String(20))
    vendor_item_no: Mapped[str | None] = mapped_column(String(30))
    product_class: Mapped[str | None] = mapped_column(String(10))
    product_line: Mapped[str | None] = mapped_column(String(10))
    list_price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    std_cost: Mapped[float | None] = mapped_column(Numeric(10, 2))
    status: Mapped[str | None] = mapped_column(String(1))


class InventoryBalance(Base):
    __tablename__ = 'inventory_balances'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_number: Mapped[str | None] = mapped_column(String(30), ForeignKey('item_master.item_number'))
    warehouse_code: Mapped[str | None] = mapped_column(String(10))
    qty_on_hand: Mapped[int | None] = mapped_column(Integer)
    qty_available: Mapped[int | None] = mapped_column(Integer)
    snapshot_time: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


class AgentAuditLog(Base):
    __tablename__ = 'agent_audit_log'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tool_name: Mapped[str] = mapped_column(String(100))
    success: Mapped[bool] = mapped_column(Boolean)
    error_msg: Mapped[str | None] = mapped_column(Text)
