#
#  IN THIS VERSION THERE IS NO DATABASE - THERE ARE ONLY TWO USERS : ADMIN AND CUSTUMER
#  THE CUSTUMER DETAILS AR IN CONFIG FILE AND ADMIN DETAILS ARE IN .ENV FILE
#  ALSO ADMIN USERNAME IS ALWAYS "ADMIN"
#  PHOTOS ID ARE COMPOSED BY THEIR FOLDER NAME AND THEIR NAME SEPARATED BY '_'
#  TO GET USERS PHOTOS CHECK THE END OF FOLDER NAME (AS THERE IS NO DATABASE)
#  IN FURTHER UPDATE - CREATE A DATABASE on postrgres


from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from jose import JWTError, jwt

from multiprocessing import Process
import logging
import uvicorn 
from dotenv import load_dotenv
from config import config, env
from api.models import Token, SimpleUser, TokenData, ConfigDescriptor, DataExchange, \
    ExchangeType, ExchangeRequest, ExchangeResponse
from api.utility import ApiUtilities


SECRET_KEY = env.SECRET_KEY
ALGORITHM = env.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(env.ACCESS_TOKEN_EXPIRE_MINUTES)
ADMIN_PASSWORD = env.ADMIN_PASSWORD

app = FastAPI()
origins = [
    "http://localhost:5000",
    "https://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="(http|https)://(.*)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class FieboothApi():
    def __init__(self, connection): 
        self.IS_ADMIN = Annotated[bool, Depends(self.__is_user_admin)]
        self.USER = Annotated[SimpleUser, Depends(self.__get_current_user)]
        self.__utils = ApiUtilities(connection=connection) 
        self.__init__routes()
        self.__conn = connection
        self.logger = logging.getLogger("fiebooth")
        
        
    
    def __init__routes(self):
        # return the image by the id (the image is resized)
        @app.get("/image/{id}", responses = { 200: {
            "content": {"image/png": {}}
            },}, response_class=Response)
        async def get_image_by_id(id: str, user: self.USER):
            #verifier si l'image appartient à l'utilisateur
            try:
                fileName = self.__utils.get_image_path(id, user)
                return FileResponse(fileName)
            except:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Impossible to resolve id"
                )
            
        @app.get("/image/thumbnail/{id}", responses = { 200: {
            "content": {"image/png": {}}
            },}, response_class=Response)
        async def get_image_thumbnail_by_id(id: str, user: self.USER):
            try:
                fileName = self.__utils.get_image_thumbnail_path(id, user)
                return FileResponse(fileName)
            except:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Impossible to resolve id"
                )
        # get images list name by user
        @app.get("/images/user/{user_name}")
        async def get_user_photos(user_name, is_admin:self.IS_ADMIN):
            if is_admin:
                photos = self.__utils.get_all_user_photos(user_name)
                return {
                    "user" : user_name,
                    "photos" : photos
                }
        @app.get("/images/all")
        async def get_all_user_images(is_admin:self.IS_ADMIN):
            if is_admin:
                photos = self.__utils.get_all_photos()
                return {
                    "user" : "admin",
                    "photos" : photos
                }
        # get images id list by folder name
        @app.get("/images/folder/{folder_name}")
        async def get_folder_photos(folder_name, is_admin:self.IS_ADMIN):
            if is_admin:
                self.__utils.get_photos_in_folder(folder_name)

        # get folder list by user name
        @app.get("/images/folder/user/{user_name}")
        async def get_user_folders(user_name, is_admin:self.IS_ADMIN):
            if is_admin:
                folders = self.__utils.get_user_folder(user_name)
                return {
                    "user_name" : user_name,
                    "length" : len(folders),
                    "folders" : folders
                }
        
        # delete an image
        @app.delete("/image/delete/{id}")
        async def delete_image_by_id(id : str, is_admin:self.IS_ADMIN):
            if is_admin:
                self.__utils.delete_image(id)

        #delete folder
        @app.delete("/images/folder/delete/{folder_name}")
        async def delete_folder(folder_name: str, is_admin:self.IS_ADMIN):
            if is_admin:
                self.__utils.delete_folder(folder_name)
        
        # delete all user images
        @app.delete("/images/user/{user_name}")
        async def delete_user_photos(user_name: str,  is_admin:self.IS_ADMIN):
            if is_admin:
                self.__utils.delete_all_user_images(user_name)
        
        # edit settings
        @app.post("/setting/edit")
        async def edit_settings(conf: ConfigDescriptor, is_admin:self.IS_ADMIN):
            if is_admin:
                return self.__utils.set_config(conf)
        
        # get setting value
        @app.get("/setting/{param}")
        async def get_setting(param: str, is_admin:self.IS_ADMIN):
            if is_admin:
                return self.__utils.get_config(param)
            
         # print a photo
        @app.post("/print/{image_id}")
        async def print_photo(image_id: str, is_admin: self.IS_ADMIN):
            if is_admin:
                return self.__utils.print_photo(image_id)
        # 
        @app.post("/images/upload/{user}")
        async def send_all_in_cloud(new_user: SimpleUser, is_admin: self.IS_ADMIN):
            if is_admin:
                pass
        # 
        @app.post("/images/download/{user}")
        async def download_all_archive(new_user: SimpleUser, is_admin: self.IS_ADMIN):
            if is_admin:
                pass
        @app.delete("/images/all")
        async def delete_all_images(new_user: SimpleUser, is_admin: self.IS_ADMIN):
            if is_admin:
                pass
        # get the currrent user
        @app.get("/users/all")
        async def get_all_users(is_admin: self.IS_ADMIN):
            if is_admin:
                all_user_names = self.__utils.get_all_users()
                return {
                    "users" : all_user_names
                }
        # create new user
        @app.post("/users/new")
        async def create_new_user(new_user: SimpleUser, is_admin: self.IS_ADMIN):
            if is_admin:
                new_user.hashpassword = self.__get_password_hash(new_user.password)
                return self.__utils.create_new_user(new_user)
        # get the currrent user
        @app.get("/users/me")
        async def read_users_me(current_user: self.USER):
            return {
                "username" : current_user.username,
            }
            
        
        
        # identification
        @app.post("/token", response_model=Token)
        async def login_for_access_token(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
        ):
            user = self.__authenticate_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.__create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
        

    def __verify_password(self, plain_password, hashed_password):
        return plain_password == hashed_password


    def __get_password_hash(self, password):
        return password


    def __get_user(self, username: str):
        if username == "admin":
            return SimpleUser(username="admin", password=ADMIN_PASSWORD, 
                              hashpassword=ADMIN_PASSWORD)
        elif username == config.user_name:
            return SimpleUser(username=config.user_name, password=config.user_password, 
                              hashpassword=config.user_password)
        else:
            return None


    def __authenticate_user(self, username: str, password: str):
        user : SimpleUser = self.__get_user(username)
        if not user:
            return False
        if not self.__verify_password(password, user.hashpassword):
            return False
        return user
    
    def __create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def __is_user_admin(self, token: Annotated[str, Depends(oauth2_scheme)]):
        user : SimpleUser = await self.__get_current_user(token=token)
        not_admin_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized! content only for admins!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if user.username == "admin":
            return True
        else:
            raise not_admin_exception
            

    async def __get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.__get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def __server_process(self):
        uvicorn.run(app=app, host="0.0.0.0", port=5000,)

    def run_server(self):
        proc = Process(target=self.__server_process, args=(), daemon=True)
        proc.start()

        

