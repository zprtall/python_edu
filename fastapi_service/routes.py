from fastapi import HTTPException, APIRouter, Query
from fastapi import Body

from models import Struct
from database import db

router = APIRouter()


@router.post("/struct")
def create_struct(struct: Struct):
    new_id = 1
    while new_id in db:
        new_id += 1
    db[new_id] = struct.dict()
    return {
        "message": "Struct created",
        "id": new_id,
        "data": db[new_id]
    }


@router.get("/struct/{struct_id}")
def get_struct(struct_id: int):
    if struct_id not in db:
        raise HTTPException(
            status_code=404,
            detail="Struct not found"
        )
    return db[struct_id]


@router.get("/struct")
def get_all_structs(
        limit : int = Query(10, ge=1, le=100, description="number of elements"),
        offset : int = Query(0, ge=0, le=100, description="quantity we skip")
):
    if len(db) == 0:
        raise HTTPException(
            status_code=404,
            detail="No structures found"
        )
    struct_list = list(db.values())
    paginated_struct = struct_list[offset:offset + limit]
    total = len(db)
    return {
        "data": paginated_struct,
        "total": total,
        "limit": limit,
        "offset": offset,
        "next_offset": offset + limit if offset + limit < total else None
    }


@router.put("/struct/{struct_id}")
def put_struct(struct_id: int, struct: Struct):
    if struct_id not in db:
        raise HTTPException(
            status_code=404,
            detail="Struct not found"
        )
    db[struct_id] = struct.dict()
    return {
        "message": "Structure updated",
        "data": db[struct_id]
    }


@router.patch("/struct/{struct_id}")
def patch_struct(struct_id: int, update_data: dict = Body(...)):
    if struct_id not in db:
        raise HTTPException(
            status_code=404,
            detail="Struct not found"
        )
    for field, value in update_data.items():
        if field not in db[struct_id]:
            raise HTTPException(
                status_code=400,
                detail = f"Field '{field}' does not exist"
            )
        if not isinstance(db[struct_id][field], type(value)):
            raise HTTPException(
                status_code=400,
                detail=f"Field '{field}' has wrong type"
            )
        db[struct_id][field] = value
    return {
        "message": "Structure changed",
        "data": db[struct_id]
    }


@router.delete("/struct/{struct_id}")
def delete_struct(struct_id: int):
    if struct_id not in db:
        raise HTTPException(
            status_code=404,
            detail="Struct not found"
        )
    deleted = db.pop(struct_id)
    return {
        "message": "Structure deleted",
        "data": deleted
    }
