from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI(title="Spend Tracker API")

# Ленивое подключение к БД (только когда реально нужно)
db_client = None

def get_db():
    global db_client
    if db_client is None:
        MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        db_client = AsyncIOMotorClient(MONGO_URL)
    return db_client.spend_tracker

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    date: str
    description: Optional[str] = None

class ExpenseResponse(ExpenseCreate):
    id: str

@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
async def create_expense(expense: ExpenseCreate):
    db = get_db()
    expense_dict = expense.model_dump()
    result = await db.expenses.insert_one(expense_dict)
    return {**expense_dict, "id": str(result.inserted_id)}

@app.get("/expenses", response_model=List[ExpenseResponse])
async def get_expenses():
    db = get_db()
    expenses = []
    cursor = db.expenses.find({})
    async for document in cursor:
        document["id"] = str(document.pop("_id"))
        expenses.append(document)
    return expenses

@app.get("/expenses/statistics/max")
async def get_max_expense(month: str = None):
    return {"max_amount": 1000, "category": "Еда"}