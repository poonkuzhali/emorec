import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import "./MoviesList.css";

interface Movie {
  id: number;
  title: string;
  overview: string;
  rating: number;
  release_date: string;
  image: string;
}

interface MovieListProps {
  movies: Movie[];
}

const MovieList: React.FC<MovieListProps> = ({ movies }) => {
  const location = useLocation();
  const locationMovies = location.state && location.state.movies;
  const displayedMovies = locationMovies || movies;

  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [isModalOpen, setModalOpen] = useState<boolean>(false);

  const handleCardClick = (movie: Movie) => {
    setSelectedMovie(movie);
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedMovie(null);
    setModalOpen(false);
  };

  return (
    <div className="movie-list-container">
      {displayedMovies.map((movie: Movie) => (
        <div
          key={movie.id}
          className="movie-card"
          onClick={() => handleCardClick(movie)}
        >
          <img src={movie.image} alt={movie.title} className="movie-image" />
          <div className="movie-details">
            <h2 className="movie-title">{movie.title}</h2>
            {/* <p className="movie-info">Rating: {movie.rating}</p>
            <p className="movie-info">Release Date: {movie.release_date}</p> */}
          </div>
        </div>
      ))}

      {isModalOpen && selectedMovie && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={handleCloseModal}>
              &times;
            </span>
            <h2 className="movie-title">{selectedMovie.title}</h2>
            <p className="movie-info">Rating: {selectedMovie.rating}</p>
            <p className="movie-info">
              Release Date: {selectedMovie.release_date}
            </p>
            <p className="movie-info">Overview: {selectedMovie.overview}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default MovieList;
