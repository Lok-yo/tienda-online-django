import React from "react";
import { Link } from "react-router-dom";
import { Button, Icon } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";

export function Home() {
  const { auth } = useAuth();

  return (
    <div className="login-admin">
      <div className="login-admin__content" style={{ textAlign: "center" }}>
        <div className="login-admin__badge">UTSLRC • IDGS 9-2 • DWI</div>
        <h1>Tienda Online</h1>
        <p className="login-admin__subtitle">
          Plataforma Full Stack con Django REST Framework, JWT, React, API Externa y SOAP
        </p>
        <div style={{ display: "flex", gap: "12px", justifyContent: "center", marginTop: "24px" }}>
          {auth ? (
            <Button as={Link} to="/dashboard" primary size="large">
              <Icon name="dashboard" /> Ir al Dashboard Protegido
            </Button>
          ) : (
            <>
              <Button as={Link} to="/login" primary size="large">
                <Icon name="sign-in" /> Iniciar Sesión
              </Button>
              <Button as={Link} to="/register" secondary size="large">
                <Icon name="signup" /> Registrarse
              </Button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
