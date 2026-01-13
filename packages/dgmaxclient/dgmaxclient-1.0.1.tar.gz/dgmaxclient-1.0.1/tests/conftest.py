"""
Test fixtures for DGMaxClient tests.

This module provides pytest fixtures for unit and integration testing.
"""

from __future__ import annotations

import pytest

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

try:
    from dgmaxclient import DGMaxClient

    DGMAXCLIENT_AVAILABLE = True
except ImportError:
    DGMaxClient = None  # type: ignore
    DGMAXCLIENT_AVAILABLE = False


@pytest.fixture
def api_key() -> str:
    """Return a test API key."""
    return "dgmax_test_key_12345"


@pytest.fixture
def base_url() -> str:
    """Return the test base URL."""
    return "https://api.dgmax.do"


@pytest.fixture
def client(api_key: str, base_url: str) -> DGMaxClient:
    """Create a DGMax client for testing."""
    return DGMaxClient(api_key=api_key, base_url=base_url)


@pytest.fixture
def sample_company() -> dict:
    """Return sample company data."""
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Test Company SRL",
        "trade_name": "Test Company",
        "rnc": "123456789",
        "email": "test@example.com",
        "address": "Calle Test #123",
        "branch": None,
        "municipality": "Santo Domingo",
        "province": "Distrito Nacional",
        "phone": "809-555-1234",
        "website": "https://testcompany.com",
        "logo": None,
        "type": "primary",
        "certificate": None,
        "dgii_environment": "test",
        "certification_status": "not_started",
        "parent_company_id": None,
    }


@pytest.fixture
def sample_document() -> dict:
    """Return sample electronic document data."""
    return {
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "status": "COMPLETED",
        "rnc": "123456789",
        "encf": "E310000000001",
        "document_stamp_url": "https://dgii.gov.do/stamp/...",
        "security_code": "ABC123",
        "signature_date": "2024-01-15T10:30:00",
        "signed_xml": "documents/signed/E310000000001.xml",
        "resume_xml": None,
        "pdf": "documents/pdf/E310000000001.pdf",
        "queued_at": None,
        "referenced_document_id": None,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:35:00Z",
        "external_status": {
            "codigo": "1",
            "estado": "Aceptado",
            "rnc": "123456789",
            "encf": "E310000000001",
            "secuencia_utilizada": True,
            "fecha_recepcion": "2024-01-15T10:35:00",
            "mensajes": [],
        },
    }


@pytest.fixture
def sample_received_document() -> dict:
    """Return sample received document data."""
    return {
        "id": "789e0123-e89b-12d3-a456-426614174000",
        "company_id": "123e4567-e89b-12d3-a456-426614174000",
        "rnc_emisor": "987654321",
        "rnc_comprador": "123456789",
        "e_ncf": "E310000000099",
        "status": "PENDING",
        "received_at": "2024-01-15T10:30:00Z",
        "xml_url": "https://storage.example.com/signed-url",
        "arecf_xml_url": None,
    }


@pytest.fixture
def sample_commercial_approval() -> dict:
    """Return sample commercial approval data."""
    return {
        "id": "abc12345-e89b-12d3-a456-426614174000",
        "company_id": "123e4567-e89b-12d3-a456-426614174000",
        "direction": "SENT",
        "rnc_emisor": "987654321",
        "rnc_comprador": "123456789",
        "e_ncf": "E310000000099",
        "fecha_emision": "2024-01-15",
        "monto_total": "1000.00",
        "approval_action": "APPROVED",
        "rejection_reason": None,
        "fecha_hora_aprobacion_comercial": "2024-01-15T10:30:00",
        "submission_status": "COMPLETED",
        "dgii_track_id": "track-123",
        "created_at": "2024-01-15T10:30:00Z",
        "received_document_id": "789e0123-e89b-12d3-a456-426614174000",
        "electronic_document_id": None,
        "acecf_xml_url": "https://storage.example.com/acecf-signed-url",
    }


@pytest.fixture
def paginated_response(sample_document: dict) -> dict:
    """Return a sample paginated response."""
    return {
        "count": 1,
        "results": [sample_document],
    }


@pytest.fixture
def paginated_companies_response(sample_company: dict) -> dict:
    """Return a sample paginated companies response."""
    return {
        "count": 1,
        "results": [sample_company],
    }
