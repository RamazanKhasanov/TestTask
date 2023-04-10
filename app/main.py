from fastapi import FastAPI
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, date


app = FastAPI(title="TestTask")


class Deposit(BaseModel):
    date: str = Field(description="Дата заявки")
    periods: int = Field(ge=1, le=60, description="Количество месяцев по вкладу")
    amount: int = Field(ge=10_000, le=3_000_000, description="Сумма вклада")
    rate: float = Field(ge=1, le=8, description="Процент по вкладу")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content=jsonable_encoder({"error": "Неверно введенные данные"}))


@app.post('/deposit')
def calc_deposit(item: Deposit):
    deposit = {}
    temp = 0
    january = {29: 30, 30: 29, 31: 28}
    initial_amount = item.amount
    try:
        start_date = datetime.strptime(item.date, "%d.%m.%Y").date()
    except ValueError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=jsonable_encoder({"error": "Неверно введенная дата заявки"}))
    if start_date.day == 31:
        for i in range(item.periods):
            initial_amount *= (1 + item.rate / 1200)
            year = start_date.year
            month = start_date.month
            if month == 12:
                days_in_month = 31
            elif month == 1 and start_date.day >= 29:
                days_in_month = january[start_date.day]
                temp = start_date.day
            elif month == 2 and temp >= 29:
                days_in_month = temp
            elif month in [3, 5, 8, 10] and start_date.day == 31:
                days_in_month = 30
            elif month in [4, 6, 9, 11] and start_date.day == 30:
                days_in_month = 31
            else:
                days_in_month = (date(year, month + 1, 1) - date(year, month, 1)).days
            key = start_date.strftime("%d.%m.%Y")
            deposit[key] = round(initial_amount, 2)
            start_date += timedelta(days=days_in_month)
    else:
        for i in range(item.periods):
            initial_amount *= (1 + item.rate / 1200)
            year = start_date.year
            month = start_date.month
            if month == 12:
                days_in_month = 31
            elif month == 1 and start_date.day >= 29:
                days_in_month = january[start_date.day]
                temp = start_date.day
            elif month == 2 and temp >= 29:
                days_in_month = temp
            else:
                days_in_month = (date(year, month + 1, 1) - date(year, month, 1)).days
            key = start_date.strftime("%d.%m.%Y")
            deposit[key] = round(initial_amount, 2)
            start_date += timedelta(days=days_in_month)
    return deposit
