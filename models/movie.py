import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict


class Genre(BaseModel):
    name: str


class UserInReview(BaseModel):
    fullName: str


class Review(BaseModel):
    userId: str
    rating: float
    text: str
    createdAt: str
    user: UserInReview


class CreateMovieRequest(BaseModel):
    name: str
    imageUrl: str
    price: int = Field(..., ge=0)
    description: str
    location: str
    published: bool
    genreId: int


class CreateMovieResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: str
    location: str
    published: bool
    genreId: int
    genre: Genre
    createdAt: str
    rating: float


class UpdateMovieRequest(BaseModel):
    name: str
    imageUrl: str
    price: int = Field(..., ge=0)
    description: str
    location: str
    published: bool
    genreId: int


class UpdateMovieResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: str
    location: str
    published: bool
    genreId: int
    genre: Genre
    createdAt: str
    rating: float


class GetMovieResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: str | None = None
    location: str
    published: bool
    genreId: int
    genre: Genre
    createdAt: str
    rating: float
    reviews: List[Review] | None = None


class GetMoviesResponse(BaseModel):
    movies: List[GetMovieResponse]
    count: int
    page: int
    pageSize: int
    pageCount: int