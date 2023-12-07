// src/UserInput.tsx

// import Chat from "./components/chat/chat";
// import Login from "./components/login/login";
import "mdb-react-ui-kit/dist/css/mdb.min.css";
import Home from "./components/home/home";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
// import AppRoutes from "./Routes";
// import Navbar from "./components/navbar/navbar";
import Chatbot from "./components/chat/chat";
import RootLayout from "./components/root/root";
import Login from "./components/login/login";
import SpotifyComponent from "./components/spotify/spotify";
import MovieList from "./components/movies/movies";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { path: "/", element: <Home /> },
      { path: "/chat", element: <Chatbot /> },
      { path: "/login", element: <Login /> },
      {
        path: "/spotify",
        element: (
          <SpotifyComponent username="yourUsername" password="yourPassword" />
        ),
      },
      {
        path: "/movies",
        element: <MovieList movies={[]} />,
      },
    ],
  },
]);

function App(): JSX.Element {
  // return <Chat></Chat>;d
  return (
    // <Router>
    //   <Navbar /> {/* Render the navigation bar */}
    // </Router>
    <RouterProvider router={router} />
  );
  // <Login></Login>;
}

export default App;
