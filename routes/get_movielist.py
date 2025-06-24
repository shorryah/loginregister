from fastapi import APIRouter, HTTPException, Depends
from models import Movie
from schemas import movie_format
from database import movie_collection
from bson import ObjectId
from jwttoken import verify_token, JWTBearer

router = APIRouter() #groups movie-related API routes

# endpoint to add movies
@router.post("/")
def add_movie(movie: Movie, user_id: str = Depends(JWTBearer())): #before allowing access to this endpoint, the JWT token is verified by verify_token, and the verified user’s ID is passed as user_id
    _ = user_id  #prevents warnings from editor (like Pylance) about an unused variable
    result = movie_collection.insert_one(movie.model_dump())   #movie data is inserted into the database.
    return {"message": "Movie added", "movie_id": str(result.inserted_id)} #returns a success message and the inserted movie’s id

#endpoint to get all the movies
@router.get("/")
def get_all_movies(user_id: str = Depends(JWTBearer())): #same as above, verification required
    _ = user_id
    movies = movie_collection.find() #finds all movie from database
    return [movie_format(movie) for movie in movies]

#updates movie based on movie_id
@router.put("/{movie_id}")
def update_movie(movie_id: str, updated: Movie, user_id: str = Depends(JWTBearer())):
    _ = user_id
    result = movie_collection.update_one(
        {"_id": ObjectId(movie_id)},
        {"$set": updated.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found") # if no movie was found to update, returns a 404 error
    return {"message": f"Movie {movie_id} updated", "updated": updated.model_dump()}

#deletes movie by movie_id
@router.delete("/{movie_id}")
def delete_movie(movie_id: str, user_id: str = Depends(JWTBearer())):
    _ = user_id
    result = movie_collection.delete_one({"_id": ObjectId(movie_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": f"Movie {movie_id} deleted"}
