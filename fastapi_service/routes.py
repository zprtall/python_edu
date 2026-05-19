from fastapi import HTTPException, APIRouter, Query

from models import Struct, datetime
from database import db

router = APIRouter()


@router.post("/struct")
def create_struct(struct: Struct):
    new_id = 1
    while new_id in db:
        new_id += 1
    db[new_id] = struct
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
        limit : int = Query(ge=1, le=100, description="number of elements"),
        offset : int = Query(ge=0, description="quantity we skip") | None,
        min_tooth: int | None = None,
        max_tooth: int | None = None,
        min_higth : float | None = None,
        max_higth : float | None = None,
        name: str | None = None,
        min_created_at : datetime.date | None = None,
        max_created_at : datetime.date | None = None,
        min_birth_at : datetime.date | None = None,
        max_birth_at : datetime.date | None = None
):
    if len(db) == 0:
        raise HTTPException(
            status_code=404,
            detail="No structures found"
        )
    struct_list = list(db.values())
    if min_tooth is not None:
        struct_list = [
            s for s in struct_list
            if s["number_of_tooth"] >= min_tooth
        ]
    if max_tooth is not None:
        struct_list = [
            s for s in struct_list
            if s["number_of_tooth"] <= max_tooth
        ]
    if min_higth:
        struct_list = [
            s for s in struct_list
            if s["hight"] >= min_higth
        ]
    if max_higth:
        struct_list = [
            s for s in struct_list
            if s["hight"] <= max_higth
        ]
    if name:
        struct_list = [s for s in struct_list if s["name"] == name]
    if min_created_at:
        struct_list = [
            s for s in struct_list
            if s["created_at"] >= min_created_at
        ]
    if max_created_at:
        struct_list = [
            s for s in struct_list
            if s["created_at"] <= max_created_at
        ]
    if min_birth_at:
        struct_list = [
            s for s in struct_list
            if s["birth_at"] >= min_birth_at
        ]
    if max_birth_at:
        struct_list = [
            s for s in struct_list
            if s["birth_at"] <= max_birth_at
        ]

    total = len(struct_list)
    paginated_struct = struct_list[offset:offset + limit]
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
    db[struct_id] = struct
    return {
        "message": "Structure updated",
        "data": db[struct_id]
    }


@router.patch("/struct/{struct_id}")
def patch_struct(struct_id: int, update_data: dict):
    if struct_id not in db:
        raise HTTPException(
            status_code=404,
            detail="Struct not found"
        )
    struct_obj = db[struct_id]
    struct_dict = struct_obj.dict()
    for field, value in update_data.items():
        if field not in struct_dict:
            raise HTTPException(
                status_code=400,
                detail=f"Field '{field}' does not exist"
            )
        if not isinstance(value, type(struct_dict[field])):
            raise HTTPException(
                status_code=400,
                detail=f"Field '{field}' has wrong type"
            )
        setattr(struct_obj, field, value)
    return {
        "message": "Structure changed",
        "data": struct_obj
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
