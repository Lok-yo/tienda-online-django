import React from "react";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { registerApi } from "../../api/user";
import { useNavigate, Link } from "react-router-dom";

export function Register() {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: initialValues(),
    validationSchema: validationSchema(),
    onSubmit: async (formValues) => {
      try {
        const payload = {
          username: formValues.username,
          email: formValues.email,
          first_name: formValues.first_name,
          last_name: formValues.last_name,
          matricula: formValues.matricula,
          carrera: formValues.carrera || "IDGS 9-2",
          password: formValues.password,
        };
        const response = await registerApi(payload);
        console.log("Usuario registrado:", response);
        toast.success(`Usuario ${response.username} registrado exitosamente`);
        navigate("/login");
      } catch (error) {
        toast.error(error.message);
      }
    },
  });

  return (
    <div className="register-admin">
      <div className="register-admin__content">
        <div className="login-admin__badge">UTSLRC • IDGS 9-2 • DWI</div>
        <h1>Registro de Usuario</h1>
        <p className="login-admin__subtitle">
          Crea una nueva cuenta conectada a POST /api/v1/auth/register/
        </p>

        <Form className="register-form-admin" onSubmit={formik.handleSubmit}>
          <Form.Group widths="equal">
            <Form.Field>
              <label>Username</label>
              <Form.Input
                name="username"
                placeholder="Username (sin espacios)"
                value={formik.values.username}
                onChange={(e) => {
                  const value = e.target.value.replace(/\s+/g, "");
                  formik.setFieldValue("username", value);
                }}
                onBlur={formik.handleBlur}
                error={formik.errors.username}
              />
            </Form.Field>
            <Form.Field>
              <label>Matrícula</label>
              <Form.Input
                name="matricula"
                placeholder="Ej. 23304031"
                value={formik.values.matricula}
                onChange={formik.handleChange}
                error={formik.errors.matricula}
              />
            </Form.Field>
          </Form.Group>

          <Form.Group widths="equal">
            <Form.Field>
              <label>Nombre(s)</label>
              <Form.Input
                name="first_name"
                placeholder="Nombre"
                value={formik.values.first_name}
                onChange={formik.handleChange}
              />
            </Form.Field>
            <Form.Field>
              <label>Apellidos</label>
              <Form.Input
                name="last_name"
                placeholder="Apellidos"
                value={formik.values.last_name}
                onChange={formik.handleChange}
              />
            </Form.Field>
          </Form.Group>

          <label>Correo electrónico</label>
          <Form.Input
            name="email"
            placeholder="Correo electrónico institucional"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.errors.email}
          />

          <Form.Group widths="equal">
            <Form.Field>
              <label>Contraseña</label>
              <Form.Input
                name="password"
                type="password"
                placeholder="Contraseña segura"
                value={formik.values.password}
                onChange={formik.handleChange}
                error={formik.errors.password}
                autoComplete="off"
              />
            </Form.Field>
            <Form.Field>
              <label>Confirmar Contraseña</label>
              <Form.Input
                name="password_confirm"
                type="password"
                placeholder="Confirmar Contraseña"
                value={formik.values.password_confirm}
                onChange={formik.handleChange}
                error={formik.errors.password_confirm}
                autoComplete="off"
              />
            </Form.Field>
          </Form.Group>

          <Button
            type="submit"
            content="Registrar Cuenta"
            icon="user plus"
            primary
            fluid
            loading={formik.isSubmitting}
          />
        </Form>

        <div className="auth-footer-links">
          ¿Ya tienes una cuenta? <Link to="/login">Inicia sesión aquí</Link>
        </div>
      </div>
    </div>
  );
}

function initialValues() {
  return {
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    matricula: "",
    carrera: "IDGS 9-2",
    password: "",
    password_confirm: "",
  };
}

function validationSchema() {
  return Yup.object({
    username: Yup.string()
      .required("El username es obligatorio")
      .matches(/^\S*$/, "El username no debe contener espacios"),
    email: Yup.string()
      .email("Correo electrónico no válido")
      .required("El correo electrónico es obligatorio"),
    password: Yup.string()
      .required("La contraseña es obligatoria")
      .min(8, "La contraseña debe tener al menos 8 caracteres")
      .matches(/[A-Z]/, "Debe contener al menos una letra mayúscula")
      .matches(/\d/, "Debe contener al menos un número")
      .matches(
        /[@$!%*?&#]/,
        "Debe contener al menos un carácter especial (@$!%*?&#)"
      ),
    password_confirm: Yup.string()
      .required("La confirmación de contraseña es obligatoria")
      .oneOf([Yup.ref("password"), null], "Las contraseñas no coinciden"),
  });
}
