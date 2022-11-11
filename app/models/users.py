from pydantic import BaseModel, EmailStr

from ._common import CommonBase, CommonBaseRead


# common (base, read, write)
class UserBase(BaseModel):
    username: str
    full_name: str | None
    email: EmailStr

# db-only overrides
class User(CommonBase, UserBase):
    password_hash: str | None

# create-only overrides
class UserCreate(UserBase):
    pass

# updatable fields
class UserUpdate(BaseModel):
    full_name: str | None
    email: EmailStr | None

# read-only overrides
class UserRead(CommonBaseRead, UserBase):
    pass
