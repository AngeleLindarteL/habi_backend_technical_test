from .module import PropertyModule
from .service import PropertyService
from lib.dtos.property_dto import GetPropertyListParams

import asyncio
import pytest

pytest_plugins = ("pytest_asyncio",)


service: PropertyService


def test_initialize_service():
    service = PropertyModule().service

    return service is not None


@pytest.mark.asyncio
async def test_normal_find() -> None:
    """Test normal find with no filters"""
    service = PropertyModule().service
    params = GetPropertyListParams(page=1, pageSize=10)

    paged_res = await service.get_property_list(params)

    assert paged_res.length == params.pageSize
    assert paged_res.page == params.page
    assert paged_res.page_size == params.pageSize
    assert paged_res.has_next == True


@pytest.mark.asyncio
async def test_city_filter_find() -> None:
    """Test normal find with city filter"""
    service = PropertyModule().service
    params = GetPropertyListParams(page=1, pageSize=10, city="medellin")

    paged_res = await service.get_property_list(params)
    all_from_medellin = True

    for result in paged_res.data:
        if result.city != "medellin":
            all_from_medellin = False

    assert all_from_medellin is True


@pytest.mark.asyncio
async def test_status_filter_find() -> None:
    """Test normal find with status filter"""
    service = PropertyModule().service
    params = GetPropertyListParams(page=1, pageSize=10, status="pre_venta")

    paged_res = await service.get_property_list(params)
    all_same_status = True

    for result in paged_res.data:
        if result.status != "pre_venta":
            all_same_status = False

    assert all_same_status is True


@pytest.mark.asyncio
async def test_status_filter_find() -> None:
    """Test normal find with year filter"""
    service = PropertyModule().service
    params = GetPropertyListParams(page=1, pageSize=10, builtYearStart=2002)

    paged_res = await service.get_property_list(params)
    all_gt_year = True

    for result in paged_res.data:
        if result.year < 2002:
            all_gt_year = False

    assert all_gt_year is True


@pytest.mark.asyncio
async def test_status_filter_find() -> None:
    """Test normal find with year filter"""
    service = PropertyModule().service
    params = GetPropertyListParams(page=1, pageSize=10, builtYearEnd=2002)

    paged_res = await service.get_property_list(params)
    all_lt_year = True

    for result in paged_res.data:
        if result.year > 2002:
            all_lt_year = False

    assert all_lt_year is True


@pytest.mark.asyncio
async def test_combined_filters() -> None:
    """Test normal find with city filter"""
    service = PropertyModule().service
    params = GetPropertyListParams(
        page=1, pageSize=10, city="medellin", status="pre_venta"
    )

    paged_res = await service.get_property_list(params)
    all_filtered = True

    for result in paged_res.data:
        if result.city != "medellin" or result.status != "pre_venta":
            all_filtered = False

    assert all_filtered is True
