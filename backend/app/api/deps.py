from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from bson import ObjectId

from app.core.config import settings
from app.schemas.user import TokenPayload
from app.db.connection import db_client

# Define the OAuth2 scheme for extracting the token from the Authorization header
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/login"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(token: TokenDep) -> dict:
    """
    Dependency to extract and validate the JWT token, then retrieve the user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    # Fetch user from database
    db = db_client.database
    user = await db["users"].find_one({"_id": ObjectId(token_data.sub)})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )
    
    return user
