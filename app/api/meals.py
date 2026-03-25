from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Meal
from app.schemas.meal import MealCreate, MealOut, MealUpdate

router = APIRouter(tags=["meals"])


@router.post("/meals", response_model=MealOut, status_code=status.HTTP_201_CREATED)
async def create_meal(payload: MealCreate, session: AsyncSession = Depends(get_session)):
    meal = Meal(**payload.model_dump())
    session.add(meal)
    await session.commit()
    await session.refresh(meal)
    return meal


@router.get("/meals", response_model=list[MealOut])
async def list_meals(session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(Meal).order_by(Meal.created_at.desc()))
    return result.all()


@router.get("/meals/{meal_id}", response_model=MealOut)
async def get_meal(meal_id: str, session: AsyncSession = Depends(get_session)):
    meal = await session.scalar(select(Meal).where(Meal.id == meal_id))
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    return meal


@router.put("/meals/{meal_id}", response_model=MealOut)
async def update_meal(meal_id: str, payload: MealUpdate, session: AsyncSession = Depends(get_session)):
    meal = await session.scalar(select(Meal).where(Meal.id == meal_id))
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")

    updated = payload.model_dump(exclude_none=True)
    for key, value in updated.items():
        setattr(meal, key, value)

    session.add(meal)
    await session.commit()
    await session.refresh(meal)
    return meal


@router.delete("/meals/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal(meal_id: str, session: AsyncSession = Depends(get_session)):
    meal = await session.scalar(select(Meal).where(Meal.id == meal_id))
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")

    await session.execute(delete(Meal).where(Meal.id == meal_id))
    await session.commit()
    return None
