"""
Companies resource for the DGMax client.

This module provides the resource class for company operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dgmaxclient.models.companies import CompanyCreate, CompanyPublic, CompanyUpdate
from dgmaxclient.models.pagination import PaginatedResponse, PaginationParams
from dgmaxclient.resources.base import BaseResource

if TYPE_CHECKING:
    from dgmaxclient.client import DGMaxClient


class CompaniesResource(BaseResource[CompanyPublic]):
    """Resource for company management operations.

    Provides CRUD operations for companies including certificate
    management and configuration.

    Examples:
        >>> # List all companies
        >>> companies = client.companies.list()
        >>> for company in companies.results:
        ...     print(f"{company.name} ({company.rnc})")

        >>> # Get a specific company
        >>> company = client.companies.get("company-uuid")

        >>> # Create a new company
        >>> company = client.companies.create({
        ...     "name": "Mi Empresa SRL",
        ...     "trade_name": "Mi Empresa",
        ...     "rnc": "123456789",
        ...     "address": "Calle Principal #123"
        ... })

        >>> # Update a company
        >>> company = client.companies.update("company-uuid", {
        ...     "phone": "809-555-1234"
        ... })
    """

    def __init__(self, client: DGMaxClient) -> None:
        """Initialize the companies resource.

        Args:
            client: The DGMax client instance
        """
        super().__init__(
            client=client,
            endpoint=client.endpoints.companies,
            model_class=CompanyPublic,
        )

    def list(
        self,
        params: PaginationParams | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse[CompanyPublic]:
        """List all companies.

        Args:
            params: Pagination parameters
            **kwargs: Additional query parameters

        Returns:
            Paginated response with companies
        """
        return super().list(params=params, **kwargs)

    def create(
        self,
        data: dict[str, Any] | CompanyCreate,
    ) -> CompanyPublic:
        """Create a new company.

        Args:
            data: Company creation data

        Returns:
            The created company

        Examples:
            >>> company = client.companies.create(CompanyCreate(
            ...     name="Mi Empresa SRL",
            ...     trade_name="Mi Empresa",
            ...     rnc="123456789",
            ...     address="Calle Principal #123",
            ...     certificate=CertificateCreate(
            ...         name="certificate",
            ...         extension="p12",
            ...         content="base64-encoded-content",
            ...         password="certificate-password"
            ...     )
            ... ))
        """
        return super().create(data)

    def update(
        self,
        company_id: str,
        data: dict[str, Any] | CompanyUpdate,
    ) -> CompanyPublic:
        """Update an existing company.

        Note: RNC cannot be changed after creation.

        Args:
            company_id: The company identifier
            data: Update data (only non-None fields will be updated)

        Returns:
            The updated company

        Examples:
            >>> company = client.companies.update(
            ...     "company-uuid",
            ...     CompanyUpdate(
            ...         phone="809-555-1234",
            ...         email="info@miempresa.com"
            ...     )
            ... )
        """
        return super().update(company_id, data)
