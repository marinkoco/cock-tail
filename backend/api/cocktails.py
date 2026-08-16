from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import get_db
from models.cocktail import Category, Cocktail
from schemas.cocktail import (
    CocktailCreate,
    CocktailDetail,
    CocktailRead,
    CocktailUpdate,
)

router = APIRouter(tags=["cocktails"])


@router.get(
    "",
    response_model=list[CocktailDetail],
    summary="List all cocktails with optional filtering",
)
async def list_cocktails(
    category_id: int | None = Query(
        default=None, description="Filter cocktails by category ID"
    ),
    category_name: str | None = Query(
        default=None,
        description="Filter cocktails by category name (case-insensitive)",
    ),
    search: str | None = Query(
        default=None,
        description="Search cocktails by name or description substring",
    ),
    is_under_construction: bool | None = Query(
        default=None,
        description="Filter by construction status (True/False)",
    ),
    skip: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        default=100, ge=1, le=500, description="Max number of items to return"
    ),
    db: AsyncSession = Depends(get_db),
) -> list[Cocktail]:
    stmt = select(Cocktail).options(selectinload(Cocktail.category))

    if category_id is not None:
        stmt = stmt.where(Cocktail.category_id == category_id)

    if category_name is not None:
        stmt = stmt.join(Cocktail.category).where(
            Category.name.ilike(category_name.strip())
        )

    if search is not None and search.strip():
        term = f"%{search.strip()}%"
        stmt = stmt.where(
            Cocktail.name.ilike(term) | Cocktail.description.ilike(term)
        )

    if is_under_construction is not None:
        stmt = stmt.where(Cocktail.is_under_construction == is_under_construction)

    stmt = stmt.order_by(Cocktail.id.asc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get(
    "/{cocktail_id}",
    response_model=CocktailDetail,
    summary="Get a cocktail by ID",
)
async def get_cocktail(
    cocktail_id: int,
    db: AsyncSession = Depends(get_db),
) -> Cocktail:
    stmt = (
        select(Cocktail)
        .options(selectinload(Cocktail.category))
        .where(Cocktail.id == cocktail_id)
    )
    result = await db.execute(stmt)
    cocktail = result.scalar_one_or_none()

    if cocktail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cocktail with ID {cocktail_id} not found",
        )
    return cocktail


@router.post(
    "",
    response_model=CocktailDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new cocktail",
)
async def create_cocktail(
    cocktail_in: CocktailCreate,
    db: AsyncSession = Depends(get_db),
) -> Cocktail:
    # Verify parent category exists
    cat_stmt = select(Category).where(Category.id == cocktail_in.category_id)
    cat_result = await db.execute(cat_stmt)
    category = cat_result.scalar_one_or_none()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with ID {cocktail_in.category_id} does not exist",
        )

    # Check for duplicate cocktail name
    name_stmt = select(Cocktail).where(
        Cocktail.name.ilike(cocktail_in.name.strip())
    )
    name_result = await db.execute(name_stmt)
    if name_result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cocktail with name '{cocktail_in.name}' already exists",
        )

    cocktail = Cocktail(
        category_id=cocktail_in.category_id,
        name=cocktail_in.name.strip(),
        description=cocktail_in.description,
        thumbnail_url=cocktail_in.thumbnail_url,
        hero_url=cocktail_in.hero_url,
        ingredients=cocktail_in.ingredients,
        instructions=cocktail_in.instructions,
        is_under_construction=cocktail_in.is_under_construction,
    )
    db.add(cocktail)
    await db.commit()

    # Re-fetch with eager loaded relationships
    return await get_cocktail(cocktail_id=cocktail.id, db=db)


@router.put(
    "/{cocktail_id}",
    response_model=CocktailDetail,
    summary="Update a cocktail by ID",
)
@router.patch(
    "/{cocktail_id}",
    response_model=CocktailDetail,
    summary="Partially update a cocktail by ID",
)
async def update_cocktail(
    cocktail_id: int,
    cocktail_in: CocktailUpdate,
    db: AsyncSession = Depends(get_db),
) -> Cocktail:
    cocktail = await get_cocktail(cocktail_id=cocktail_id, db=db)

    update_data = cocktail_in.model_dump(exclude_unset=True)

    # If updating category_id, verify existence
    if "category_id" in update_data and update_data["category_id"] is not None:
        new_cat_id = update_data["category_id"]
        cat_stmt = select(Category).where(Category.id == new_cat_id)
        cat_result = await db.execute(cat_stmt)
        if cat_result.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with ID {new_cat_id} does not exist",
            )

    # If updating name, check uniqueness against other cocktails
    if "name" in update_data and update_data["name"] is not None:
        new_name = update_data["name"].strip()
        name_stmt = select(Cocktail).where(
            Cocktail.name.ilike(new_name), Cocktail.id != cocktail_id
        )
        name_result = await db.execute(name_stmt)
        if name_result.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cocktail with name '{new_name}' already exists",
            )
        update_data["name"] = new_name

    for field, value in update_data.items():
        setattr(cocktail, field, value)

    await db.commit()
    return await get_cocktail(cocktail_id=cocktail.id, db=db)


@router.delete(
    "/{cocktail_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a cocktail by ID",
)
async def delete_cocktail(
    cocktail_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    stmt = select(Cocktail).where(Cocktail.id == cocktail_id)
    result = await db.execute(stmt)
    cocktail = result.scalar_one_or_none()

    if cocktail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cocktail with ID {cocktail_id} not found",
        )

    await db.delete(cocktail)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
