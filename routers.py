from asyncio import gather
from fastapi import APIRouter, Path, Query
from converter import convert_currency
from schemas import ConverterInput, ConverterOutput

router = APIRouter()

@router.get('/converter/{from_currency}', response_model=ConverterOutput)
async def converter_router(
    body: ConverterInput,
    from_currency: str = Path(max_length=3, regex='^[A-Z]{3}$'), 
):
    to_currencies = body.to_currencies
    price = body.price

    cororoutines = []

    for currency in to_currencies:
        coro = convert_currency(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )

        cororoutines.append(coro)

    result = await gather(*cororoutines)
    return ConverterOutput(
        message= 'Success',
        data=result
    )