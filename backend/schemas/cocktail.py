from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------
# Category Schemas
# ---------------------------------------------------------


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the liquor category (e.g., Vodka, Gin, Rum)",
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Updated name of the category",
    )


class CategoryRead(CategoryBase):
    id: int = Field(..., description="Unique category identifier")

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Cocktail Schemas
# ---------------------------------------------------------


class CocktailBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the cocktail",
    )
    description: str = Field(
        ...,
        description="Detailed description or tagline for the cocktail",
    )
    thumbnail_url: str | None = Field(
        default=None,
        description="Path or URL to the cocktail thumbnail image",
    )
    hero_url: str | None = Field(
        default=None,
        description="Path or URL to the full-size hero/modal image",
    )
    ingredients: list[str] = Field(
        default_factory=list,
        description="List of ingredients required for the cocktail",
    )
    instructions: list[str] = Field(
        default_factory=list,
        description="Step-by-step preparation and serving instructions",
    )
    is_under_construction: bool = Field(
        default=False,
        description="Flag indicating whether this cocktail card is under construction",
    )


class CocktailCreate(CocktailBase):
    category_id: int = Field(
        ...,
        description="ID of the category this cocktail belongs to",
    )


class CocktailUpdate(BaseModel):
    category_id: int | None = Field(
        default=None,
        description="Updated parent category ID",
    )
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated cocktail name",
    )
    description: str | None = Field(
        default=None,
        description="Updated description",
    )
    thumbnail_url: str | None = Field(
        default=None,
        description="Updated thumbnail image URL or path",
    )
    hero_url: str | None = Field(
        default=None,
        description="Updated hero image URL or path",
    )
    ingredients: list[str] | None = Field(
        default=None,
        description="Updated list of ingredients",
    )
    instructions: list[str] | None = Field(
        default=None,
        description="Updated list of instructions",
    )
    is_under_construction: bool | None = Field(
        default=None,
        description="Updated under construction status",
    )


class CocktailRead(CocktailBase):
    id: int = Field(..., description="Unique cocktail identifier")
    category_id: int = Field(
        ..., description="ID of the category this cocktail belongs to"
    )

    model_config = ConfigDict(from_attributes=True)


class CocktailDetail(CocktailRead):
    category: CategoryRead | None = Field(
        default=None,
        description="Parent category details",
    )

    model_config = ConfigDict(from_attributes=True)


class CategoryWithCocktails(CategoryRead):
    cocktails: list[CocktailRead] = Field(
        default_factory=list,
        description="List of cocktails belonging to this category",
    )

    model_config = ConfigDict(from_attributes=True)
