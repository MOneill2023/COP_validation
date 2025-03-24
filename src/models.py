from datetime import date, datetime
from typing import Literal, List
from decimal import Decimal

from pydantic import BaseModel, create_model, field_validator
from pydantic.fields import Field, AliasPath
from pydantic.types import NonNegativeInt, PastDate, NonNegativeFloat, constr
from pydantic.networks import HttpUrl

""""books dataset

bookid non-negative integer
title string
authors string
average_rating float? 
isbn string with mod checks
isbn13 string with mod checks
language string enumeration?
num pages integer
ratings_count integer
text_Reviews_count integer
publication_date date
publisher string"""


class Books(BaseModel):
    bookID: NonNegativeInt
    title: str
    authors: constr(strip_whitespace=True, min_length=1, max_length=700) 
    average_rating: NonNegativeFloat
    isbn: str
    isbn13: str
    language: str | None
    num_pages: NonNegativeInt
    ratings_count: NonNegativeInt
    text_reviews_count: NonNegativeInt
    publication_date: date
    publisher: str

    @field_validator("publication_date", mode="before")
    def parse_publication_date(cls, value):
        return datetime.strptime(value, "%m/%d/%Y")

    @field_validator("isbn")
    def isbn10_checksum(cls, value):
        *digits, check = value

        if check.lower() == "x":
            check = 10

        digits.append(check)

        weighted_sum = sum([int(digit) * (10 - i) for i, digit in enumerate(digits)])

        mod = weighted_sum % 11

        if mod == check:
            return value
        
        raise ValueError("Failed mod11 check")
        
    @field_validator("isbn13")
    def isbn13_checksum(cls, value):
        *digits, check = value
        if check.lower() == "x":
            check = 10

        weighted_sums = sum([int(digit) * ((3*(i%2)) or 1) for i, digit in enumerate(digits)])
        
        mod10 = 10 - (weighted_sums % 10)
        if mod10 == 10:
            mod10 = 0
        if mod10 == int(check):
            return value

        raise ValueError("Failed mod13 check")

def stringify_model(model): 
    
    string_annotations = {
        field: (str, Field(None, coerce_numbers_to_str=True))
        for field in model.__annotations__
    }
    stringified_model = create_model(
        "book_strings",
        __config__={"strict": False},
        __doc__=model.__doc__,
        **string_annotations
    )
    return stringified_model
"""
open4goods-isbn-dataset

isbn string with mod checks
title string
last_update timestamp (parsed from unixtime)
offers_count integer
min_price Decimal
min_pice_compensation Decimal
Currency string Enumeration?
url string valid url
editeur List of strings
Format ??? string?
nb_pages integer
french end columns String"
"""


class OpenGoods(BaseModel):
    isbn: str
    title: str
    last_update: datetime
    offers_count: int
    min_price: Decimal
    min_price_compensation: Decimal
    currency: Literal[enumerate]
    url: HttpUrl
    editeur: List[str]
    format: str
    nb_pages: int


"""BooksDataSet
Title          Authors Description           Category Publisher            Publish Date
<char>           <char>      <char>             <char>    <char>                  <char>

                     Price
                    <char>


"""


class BooksDataSet(BaseModel):
    Title: str
    Authors: str
    Description: str
    Category: str
    Publisher: str
    PublishDate: str = Field(validation_alias=AliasPath('Publish Date', 0))  # datetime.strptime("Friday, January 1, 1993", "%A, %B %d, %Y").strftime("%Y-%m-%d")
    Price: Decimal

