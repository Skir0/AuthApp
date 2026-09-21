from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.db.dao import UsersDAO
from app.models.user import User
from app.schemas.user import SUserAuth, SUserRegister
from app.services.auth import authenticate_user, create_access_token, get_password_hash
from app.services.send_email import send_verification_email

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/")
async def register_user(
    user_data: SUserRegister,
    background_tasks: BackgroundTasks,
) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует",
        )

    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)
    token = serializer.dumps(user_dict, salt="email-verification")
    verify_url = f"http://localhost:8000/auth/verify-email?token={token}"

    background_tasks.add_task(send_verification_email, user_data.email, verify_url)
    return {
        "message": (
            "Письмо для подтверждения отправлено. "
            "Пожалуйста, проверьте вашу почту."
        )
    }


@router.get("/verify-email/")
async def verify_email(token: str) -> dict:
    try:
        user_dict = serializer.loads(token, salt="email-verification", max_age=3600)
    except SignatureExpired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Срок действия ссылки истек. Зарегистрируйтесь заново.",
        )
    except BadSignature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недействительный токен.",
        )

    existing_user = await UsersDAO.find_one_or_none(email=user_dict["email"])
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже зарегистрирован.",
        )

    await UsersDAO.add(**user_dict)
    return {"response": "Вы успешно зарегистрированы. Войдите на сайте"}


@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(
        email=user_data.email,
        password=user_data.password,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверная почта или пароль",
        )

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}


@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}
