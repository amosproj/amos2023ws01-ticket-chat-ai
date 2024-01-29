from fastapi import APIRouter
from starlette import status
from fastapi.params import Depends
from app.util.logger import logger

from app.dependency.repository import get_service_repository
from app.repository.service_repository import ServiceRepository
from app.dependency.repository import get_category_repository
from app.repository.category_repository import CategoryRepository

router = APIRouter()


@router.get("/services", status_code=status.HTTP_200_OK, response_model=list[str])
async def get_services(service_repository: ServiceRepository = Depends(get_service_repository)):
    """
    Retrieve all services from the database

    Returns:
    - List[Str]: A response containing a list of service information.
    """
    logger.info("Fetching all services from the database...")
    services = service_repository.read_services()
    service_names = [service['service_name'] for service in services]

    return service_names


@router.get("/categories", status_code=status.HTTP_200_OK, response_model=list[str])
async def get_categories(category_repository: CategoryRepository = Depends(get_category_repository)):
    """
    Retrieve all categories from the database

    Returns:
    - List[Str]: A response containing a list of category information.
    """
    logger.info("Fetching all categories from the database...")
    categories = category_repository.read_categories()
    categories_names = [category['name'] for category in categories]

    return categories_names
