from fastapi import HTTPException


def get_or_404(obj, detail: str = "Object not found"):
    if obj is None:
        raise HTTPException(status_code=404, detail=detail)
    else:
        return obj
