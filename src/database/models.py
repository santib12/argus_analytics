"""
Argus Phase 2 — SQLAlchemy models
=================================

Source of truth for table shapes is still sql/schema.sql.
These models mirror that schema for typed Python access (FastAPI later).
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for Argus models."""


class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    recipient_uei: Mapped[Optional[str]] = mapped_column(String(12), unique=True)
    recipient_name: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_name: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(Text)
    state: Mapped[Optional[str]] = mapped_column(String(2))
    country: Mapped[Optional[str]] = mapped_column(Text)
    zip_code: Mapped[Optional[str]] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    awards: Mapped[list["Award"]] = relationship(back_populates="vendor")


class Agency(Base):
    __tablename__ = "agencies"
    __table_args__ = (
        UniqueConstraint(
            "agency_code",
            "agency_name",
            "subtier_agency_name",
            name="uq_agencies_code_name",
        ),
    )

    agency_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    agency_code: Mapped[Optional[str]] = mapped_column(String(20))
    agency_name: Mapped[str] = mapped_column(Text, nullable=False)
    subtier_agency_name: Mapped[Optional[str]] = mapped_column(Text)


class Award(Base):
    __tablename__ = "awards"

    award_id: Mapped[str] = mapped_column(Text, primary_key=True)
    usaspending_internal_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.vendor_id"), nullable=False)
    awarding_agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.agency_id"))
    funding_agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.agency_id"))
    award_type: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    naics_code: Mapped[Optional[str]] = mapped_column(String(10))
    product_service_code: Mapped[Optional[str]] = mapped_column(String(10))
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    initial_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    current_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    potential_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    place_of_performance_state: Mapped[Optional[str]] = mapped_column(String(2))
    set_aside_type: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    vendor: Mapped["Vendor"] = relationship(back_populates="awards")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="award")


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(Text, primary_key=True)
    award_id: Mapped[str] = mapped_column(ForeignKey("awards.award_id"), nullable=False)
    vendor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vendors.vendor_id"))
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.agency_id"))
    action_date: Mapped[date] = mapped_column(Date, nullable=False)
    federal_action_obligation: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    current_total_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    potential_total_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    modification_number: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    award: Mapped["Award"] = relationship(back_populates="transactions")


class Exclusion(Base):
    __tablename__ = "exclusions"

    exclusion_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uei: Mapped[Optional[str]] = mapped_column(String(12))
    entity_name: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_name: Mapped[Optional[str]] = mapped_column(Text)
    exclusion_type: Mapped[Optional[str]] = mapped_column(Text)
    excluding_agency: Mapped[Optional[str]] = mapped_column(Text)
    active_date: Mapped[Optional[date]] = mapped_column(Date)
    termination_date: Mapped[Optional[date]] = mapped_column(Date)
    address: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(Text)
    state: Mapped[Optional[str]] = mapped_column(String(2))
    country: Mapped[Optional[str]] = mapped_column(Text)
    source_system: Mapped[Optional[str]] = mapped_column(Text, server_default="SAM.gov")
    downloaded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class EntityMatch(Base):
    __tablename__ = "entity_matches"
    __table_args__ = (
        UniqueConstraint(
            "vendor_id",
            "exclusion_id",
            "match_type",
            name="uq_entity_matches_vendor_exclusion_type",
        ),
    )

    match_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.vendor_id"), nullable=False)
    exclusion_id: Mapped[int] = mapped_column(ForeignKey("exclusions.exclusion_id"), nullable=False)
    match_type: Mapped[str] = mapped_column(Text, nullable=False)
    similarity_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2))
    uei_match: Mapped[Optional[bool]] = mapped_column(Boolean)
    name_match: Mapped[Optional[bool]] = mapped_column(Boolean)
    address_match: Mapped[Optional[bool]] = mapped_column(Boolean)
    review_status: Mapped[str] = mapped_column(Text, nullable=False, server_default="pending")


class VendorFeature(Base):
    __tablename__ = "vendor_features"

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.vendor_id"), primary_key=True
    )
    analysis_date: Mapped[date] = mapped_column(Date, primary_key=True)
    total_award_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    award_count: Mapped[Optional[int]] = mapped_column(Integer)
    transaction_count: Mapped[Optional[int]] = mapped_column(Integer)
    average_award_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    median_award_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    award_value_std: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    award_growth_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 6))
    agency_count: Mapped[Optional[int]] = mapped_column(Integer)
    agency_concentration: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 6))
    modification_count: Mapped[Optional[int]] = mapped_column(Integer)
    average_modification_ratio: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 6))
    award_velocity: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 6))
    geographic_count: Mapped[Optional[int]] = mapped_column(Integer)
    set_aside_ratio: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 6))
    graph_degree: Mapped[Optional[int]] = mapped_column(Integer)
    graph_weighted_degree: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 2))
    anomaly_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 6))


class RiskFlag(Base):
    __tablename__ = "risk_flags"

    risk_flag_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.vendor_id"), nullable=False)
    award_id: Mapped[Optional[str]] = mapped_column(ForeignKey("awards.award_id"))
    flag_type: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    evidence: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB)


class RiskScore(Base):
    __tablename__ = "risk_scores"

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.vendor_id"), primary_key=True
    )
    analysis_date: Mapped[date] = mapped_column(Date, primary_key=True)
    rules_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2))
    statistical_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2))
    ml_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2))
    graph_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2))
    compliance_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2))
    overall_score: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    risk_level: Mapped[str] = mapped_column(Text, nullable=False)


class DojCase(Base):
    __tablename__ = "doj_cases"

    case_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    case_title: Mapped[str] = mapped_column(Text, nullable=False)
    defendant_or_entity_name: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_name: Mapped[Optional[str]] = mapped_column(Text)
    enforcement_date: Mapped[Optional[date]] = mapped_column(Date)
    agency_or_component: Mapped[Optional[str]] = mapped_column(Text)
    case_url: Mapped[Optional[str]] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
