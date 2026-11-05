import React, { useState } from "react";
import { Button, Form, Icon } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { loginApi } from "../../api/user";
import { useAuth } from "../../hooks/useAuth";
import { useNavigate, Link, useSearchParams } from "react-router-dom";

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const stayForConsole = searchParams.get("console") === "1";
  const [consoleLogs, setConsoleLogs] = useState([]);
  const [obtainedToken, setObtainedToken] = useState(null);

  const appendLog = (type, label, payload) => {
    const time = new Date().toLocaleTimeString("es-MX", { hour12: false });
    setConsoleLogs((prev) => [...prev, { time, type, label, payload }]);
  };

  const formik = useFormik({
    initialValues: initialValues(),
    validationSchema: validationSchema(),
    onSubmit: async (formValues) => {
      try {
        console.log("Valores enviados:", formValues);
        appendLog("info", "Valores enviados:", {
          email: formValues.email,
          password: "••••••••••••••",
        });

        const response = await loginApi(formValues);
        const { access, refresh } = response;

        // Requisito: Mostrar en consola el Token JWT obtenido
        console.log(access);
        console.log("JWT Token Response (/api/v1/auth/token/):", response);

        appendLog(
          "success",
          "POST http://127.0.0.1:8000/api/v1/auth/token/ [200 OK]",
          { access, refresh }
        );
        setObtainedToken(access);

        await login(access);
        toast.success("Autenticación JWT exitosa");

        if (!stayForConsole) {
          navigate("/dashboard");
        }
      } catch (error) {
        console.error(error.message);
        appendLog("error", "Error de autenticación:", error.message);
        toast.error(error.message);
      }
    },
  });

  return (
    <div className={`login-admin ${stayForConsole ? "with-console" : ""}`}>
      <div className="login-admin__content">
        <div className="login-admin__badge">UTSLRC • IDGS 9-2 • DWI</div>
        <h1>Iniciar Sesión</h1>
        <p className="login-admin__subtitle">
          Tienda Online — Autenticación JWT con Django REST Framework
        </p>

        <Form className="login-form-admin" onSubmit={formik.handleSubmit}>
          <label>Correo electrónico</label>
          <Form.Input
            name="email"
            icon="mail"
            iconPosition="left"
            placeholder="Correo electrónico (ej. luis.leon@utslrc.edu.mx)"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.errors.email}
          />

          <label>Contraseña</label>
          <Form.Input
            name="password"
            type="password"
            icon="lock"
            iconPosition="left"
            placeholder="Contraseña"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.errors.password}
            autoComplete="off"
          />

          <Button
            type="submit"
            content="Iniciar Sesión"
            icon="sign-in"
            primary
            fluid
            loading={formik.isSubmitting}
          />
        </Form>

        {obtainedToken && (
          <div className="token-success-banner">
            <div>
              <Icon name="check circle" color="green" />
              <strong>Token JWT guardado en localStorage (TOKEN)</strong>
            </div>
            <Button
              size="tiny"
              color="teal"
              content="Ir al Dashboard →"
              onClick={() => navigate("/dashboard")}
            />
          </div>
        )}

        <div className="auth-footer-links">
          ¿No tienes cuenta? <Link to="/register">Regístrate aquí</Link>
        </div>
      </div>

      {(stayForConsole || consoleLogs.length > 0) && (
        <div className="devtools-drawer" id="devtools-console">
          <div className="devtools-drawer__bar">
            <span className="tab">Elements</span>
            <span className="tab active">Console</span>
            <span className="tab">Network</span>
            <span className="tab">Application (localStorage: TOKEN)</span>
            <span className="right-meta">
              Firefox Web Console — http://127.0.0.1:5173/login
            </span>
          </div>
          <div className="devtools-drawer__body">
            {consoleLogs.map((entry, idx) => (
              <div key={idx} className={`console-line ${entry.type}`}>
                <span className="time">{entry.time}</span>
                <span className="label">{entry.label}</span>
                <pre className="payload">
                  {typeof entry.payload === "string"
                    ? entry.payload
                    : JSON.stringify(entry.payload, null, 2)}
                </pre>
                <span className="src">Login.jsx:39</span>
              </div>
            ))}
            {obtainedToken && (
              <div className="console-line raw-token">
                <span className="time">&gt; console.log(access)</span>
                <code className="token-val">{obtainedToken}</code>
                <span className="src">Login.jsx:40</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function initialValues() {
  return {
    email: "",
    password: "",
  };
}

function validationSchema() {
  return Yup.object({
    email: Yup.string()
      .email("Correo electrónico no válido")
      .required("El correo electrónico es obligatorio"),
    password: Yup.string().required("La contraseña es obligatoria"),
  });
}
