from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import get_db
from models.cocktail import Category
from schemas.cocktail import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    CategoryWithCocktails,
)

router = APIRouter(tags=["categories"])


@router.get(
    "",
    response_model=list[CategoryWithCocktails],
    summary="List all categories with their cocktails",
)
async def list_categories(
    search: str | None = Query(
        default=None,
        description="Filter categories by name substring",
    ),
    skip: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        default=100, ge=1, le=500, description="Max number of items to return"
    ),
    db: AsyncSession = Depends(get_db),
) -> list[Category]:
    stmt = (
        select(Category)
        .options(selectinload(Category.cocktails))
        .order_by(Category.id.asc())
    )

    if search is not None and search.strip():
        stmt = stmt.where(Category.name.ilike(f"%{search.strip()}%"))

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get(
    "/{category_id}",
    response_model=CategoryWithCocktails,
    summary="Get a category by ID with its cocktails",
)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
) -> Category:
    stmt = (
        select(Category)
        .options(selectinload(Category.cocktails))
        .where(Category.id == category_id)
    )
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found",
        )
    return category


@router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db),
) -> Category:
    name = category_in.name.strip()
    stmt = select(Category).where(Category.name.ilike(name))
    result = await db.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category with name '{name}' already exists",
        )

    category = Category(name=name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.put(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Update a category by ID",
)
@router.patch(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Partially update a category by ID",
)
async def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
) -> Category:
    stmt = select(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found",
        )

    if category_in.name is not None:
        new_name = category_in.name.strip()
        dup_stmt = select(Category).where(
            Category.name.ilike(new_name), Category.id != category_id
        )
        dup_result = await db.execute(dup_stmt)
        if dup_result.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category with name '{new_name}' already exists",
            )
        category.name = new_name

    await db.commit()
    await db.refresh(category)
    return category


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category by ID",
)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    stmt = (
        select(Category)
        .options(selectinload(Category.cocktails))
        .where(Category.id == category_id)
    )
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found",
        )

    await db.delete(category)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
