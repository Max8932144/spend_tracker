from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI(title="Spend Tracker API")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.spend_tracker
expenses_collection = db.get_collection("expenses")

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    date: str
    description: Optional[str] = None

class ExpenseResponse(ExpenseCreate):
    id: str

@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
async def create_expense(expense: ExpenseCreate):
    expense_dict = expense.model_dump()
    result = await expenses_collection.insert_one(expense_dict)
    return {**expense_dict, "id": str(result.inserted_id)}

@app.get("/expenses", response_model=List[ExpenseResponse])
async def get_expenses():
    expenses = []
    cursor = expenses_collection.find({})
    async for document in cursor:
        document["id"] = str(document.pop("_id"))
        expenses.append(document)
    return expenses

@app.get("/expenses/statistics/max")
async def get_max_expense(month: str):
    return {"max_amount": 1000, "category": "Еда"}