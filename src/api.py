from typing import Union
from collections import Counter
from datetime import datetime

from database_stuff import sql_conn, connect
from fastapi import FastAPI, status, Response
from pydantic import ValidationError
import uvicorn
from models import Books, stringify_model
import json

app = FastAPI()



@app.post("/books/{submission_id}")
def post_book(books: list[stringify_model(Books)], submission_id: int):

    sql_conn = connect("database.db")
    with sql_conn as conn:
        conn.execute(f"""INSERT INTO job_start (submission_id, submitter, processing_Start_time)
                     Values ({submission_id}, 'X26', '{datetime.now()}')""")
    errors = []
    for row_id, book in enumerate(books):
        try:
            valid = Books(**book.dict())
            # write valid date to somewhere
        except ValidationError as err:
            errors.append({"index": row_id, "errors": err.errors()})
            # log errors to a table
    # aggregate up the errors
    aggregates = []
    for row in errors:
        raised_errors = row["errors"]
        for error in raised_errors:
            error_type = error["type"]
            field = error["loc"][-1]
            aggregates.append((error_type, field))
    counts = Counter(aggregates)
    for (type_, field), count in counts.items(): 
        with sql_conn as conn:
            conn.execute(f"""
                         INSERT INTO VALIDATIONS (submission_id, field_name, validation_type, number_failed)
                         Values ({submission_id}, '{field}', '{type_}', {count})
                         """)
    with sql_conn as conn:
        conn.execute(f"""INSERT INTO job_finish (submission_id, row_count, processing_end_time)
                    Values ({submission_id}, {row_id + 1}, '{datetime.now()}')""")

    
    if errors:
        errors = json.dumps(errors, default=str)
        return Response(errors, 
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, media_type="json"
                 )
    return Response("[]", status_code=200)

uvicorn.run(app)