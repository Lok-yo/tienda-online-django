import React from "react";
import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";

export function Error404() {
  return (
    <div className="login-admin">
      <div className="login-admin__content" style={{ textAlign: "center" }}>
        <h1>Error 404</h1>
        <p>La página solicitada no existe.</p>
        <Button as={Link} to="/dashboard" primary content="Ir al Dashboard" />
      </div>
    </div>
  );
}

export default Error404;
