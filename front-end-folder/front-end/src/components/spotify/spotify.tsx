// SpotifyComponent.jsx

import React, { useState, useEffect } from "react";
import axios from "axios";
import "./spotify.css"; // Import the CSS file

interface SpotifyComponentProps {
  username: string;
  password: string;
}
interface Artist {
  name: string;
}

const SpotifyComponent: React.FC<SpotifyComponentProps> = ({
  username,
  password,
}) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [songs, setSongs] = useState<any[]>([]);

  useEffect(() => {
    const fetchAccessToken = async () => {
      try {
        const response = await axios.post("YOUR_BACKEND_API_URL/token", {
          username,
          password,
        });

        const { access_token } = response.data;

        setAccessToken(access_token);
      } catch (error) {
        console.error("Error fetching access token:", error);
      }
    };

    if (!accessToken) {
      fetchAccessToken();
    }
  }, [accessToken, username, password]);

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await axios.get(
          "https://api.spotify.com/v1/me/top/tracks",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        setSongs(response.data.items);
      } catch (error) {
        console.error("Error fetching songs:", error);
      }
    };

    if (accessToken) {
      fetchSongs();
    }
  }, [accessToken]);

  return (
    <div className="container">
      <h2>Your Top Songs on Spotify</h2>
      <ul>
        {songs.map((song) => (
          <li key={song.id}>
            <img src={song.album.images[0].url} alt={song.name} />
            <p>{song.name}</p>
            <p className="artist">
              {song.artists.map((artist: Artist) => artist.name).join(", ")}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SpotifyComponent;
