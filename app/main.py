from fastapi import FastAPI, Depends, HTTPException, status, Query
from typing import Optional, List
from datetime import datetime, timedelta
from bson import ObjectId

from .db import get_db
from .deps import get_current_user_id
from .schemas import ExpenseCreate, ExpenseUpdate, ExpenseOut
from .models import Category

app = FastAPI(title="Expenses API", version="1.0.0")

# Routers
from .auth import router as auth_router
app.include_router(auth_router)

# Helpers

def to_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

async def serialize_expense(doc) -> ExpenseOut:
    return ExpenseOut(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        amount=doc["amount"],
        category=doc["category"],
        description=doc.get("description"),
        date=doc["date"],
    )

# CRUD Gastos
@app.post("/expenses", response_model=ExpenseOut, status_code=201)
async def create_expense(payload: ExpenseCreate, db = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    expenses = db["expenses"]
    doc = {
        "user_id": ObjectId(user_id),
        "amount": payload.amount,
        "category": payload.category.value,
        "description": payload.description,
        "date": payload.date,
    }
    res = await expenses.insert_one(doc)
    doc["_id"] = res.inserted_id
    return await serialize_expense(doc)

@app.get("/expenses", response_model=List[ExpenseOut])
async def list_expenses(
    db = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
    rango: Optional[str] = Query(default=None, description="past_week | past_month | last_3_months | custom"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[Category] = Query(default=None),
):
    expenses = db["expenses"]
    q = {"user_id": ObjectId(user_id)}

    # Filtros de fecha
    now = datetime.utcnow()
    if rango == "past_week":
        q["date"] = {"$gte": now - timedelta(days=7), "$lte": now}
    elif rango == "past_month":
        q["date"] = {"$gte": now - timedelta(days=30), "$lte": now}
    elif rango == "last_3_months":
        q["date"] = {"$gte": now - timedelta(days=90), "$lte": now}
    elif rango == "custom":
        if not start_date or not end_date:
            raise HTTPException(status_code=400, detail="Para 'custom' debe indicar start_date y end_date")
        q["date"] = {"$gte": start_date, "$lte": end_date}

    # Filtro por categoría
    if category:
        q["category"] = category.value

    cursor = expenses.find(q).sort("date", -1)
    results = [await serialize_expense(doc) async for doc in cursor]
    return results

@app.patch("/expenses/{expense_id}", response_model=ExpenseOut)
async def update_expense(expense_id: str, payload: ExpenseUpdate, db = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    expenses = db["expenses"]
    oid = to_object_id(expense_id)

    updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if "category" in updates and updates["category"] is not None:
        updates["category"] = updates["category"].value

    if not updates:
        raise HTTPException(status_code=400, detail="Nada que actualizar")

    res = await expenses.find_one_and_update(
        {"_id": oid, "user_id": ObjectId(user_id)},
        {"$set": updates},
        return_document=True,
    )
    if not res:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return await serialize_expense(res)

@app.delete("/expenses/{expense_id}", status_code=204)
async def delete_expense(expense_id: str, db = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    expenses = db["expenses"]
    oid = to_object_id(expense_id)
    res = await expenses.delete_one({"_id": oid, "user_id": ObjectId(user_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return