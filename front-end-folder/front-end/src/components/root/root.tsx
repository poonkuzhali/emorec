import { Outlet } from "react-router-dom";

import Navbar from "../navbar/navbar";
import classes from "./root.module.css";

function RootLayout() {
  return (
    <>
      <Navbar />
      <main className={classes.content}>
        <Outlet />
      </main>
    </>
  );
}

export default RootLayout;
