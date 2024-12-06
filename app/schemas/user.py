from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    pass


class UserRead(schemas.BaseUser):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserDelete(schemas.BaseUser):
    pass
