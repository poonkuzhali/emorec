import React, { useState } from "react";
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBIcon,
  MDBInput,
} from "mdb-react-ui-kit";

// Import your image

function App() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleInputChange = (e: any) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleLogin = () => {
    // Use formData.email and formData.password for login logic
    console.log("Email:", formData.email);
    console.log("Password:", formData.password);
    // Add your login logic here
  };

  return (
    <MDBContainer fluid>
      <MDBRow>
        <MDBCol sm="6">
          <div className="d-flex flex-row ps-5 pt-5">
            <MDBIcon fas icon="crow fa-3x me-3" style={{ color: "#709085" }} />
            <span className="h1 fw-bold mb-0">Emorec</span>
          </div>

          <div className="d-flex flex-column justify-content-center h-custom-2 w-75 pt-4">
            <h3
              className="fw-normal mb-3 ps-5 pb-3"
              style={{ letterSpacing: "1px" }}
            >
              Log in
            </h3>

            <MDBInput
              wrapperClass="mb-4 mx-5 w-100"
              label="Email address"
              id="formControlLg"
              type="email"
              size="lg"
              name="email"
              onChange={handleInputChange}
              value={formData.email}
            />
            <MDBInput
              wrapperClass="mb-4 mx-5 w-100"
              label="Password"
              id="formControlLg"
              type="password"
              size="lg"
              name="password"
              onChange={handleInputChange}
              value={formData.password}
            />

            <MDBBtn
              className="mb-4 px-5 mx-5 w-100"
              color="info"
              size="lg"
              onClick={handleLogin}
            >
              Login
            </MDBBtn>
            <p className="small mb-5 pb-lg-3 ms-5">
              <a className="text-muted" href="#!">
                Forgot password?
              </a>
            </p>
            <p className="ms-5">
              Don't have an account?{" "}
              <a href="#!" className="link-info">
                Register here
              </a>
            </p>
          </div>
        </MDBCol>

        <MDBCol sm="6" className="d-none d-sm-block px-0">
          <img
            src="https://image.winudf.com/v2/image1/Y29tLm1vYmlsZXVuaXZlcnNpdHkubXVzaWNfc2NyZWVuXzFfMTU0MzI5MzcwMF8wMTY/screen-1.webp?fakeurl=1&type=.webp"
            alt="Login"
            className="w-100"
            style={{ objectFit: "cover", objectPosition: "left" }}
          />
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
}

export default App;
