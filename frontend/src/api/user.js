const API_URL = import.meta.env.VITE_BASE_API_URL || "http://127.0.0.1:8000";

export async function loginApi(formData) {
  const url = `${API_URL}/api/v1/auth/token/`;
  console.log("POST JWT URL:", url);
  const params = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  };

  const response = await fetch(url, params);

  if (response.status !== 200) {
    throw new Error("Usuario o contraseña incorrecta");
  }

  const result = await response.json();
  return result;
}

export async function registerApi(formData) {
  const url = `${API_URL}/api/v1/auth/register/`;
  console.log("POST Register URL:", url);
  const params = {
    method: "POST",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  };

  const response = await fetch(url, params);

  if (response.status !== 201) {
    const errData = await response.json().catch(() => ({}));
    const firstMsg = Object.values(errData)?.[0];
    throw new Error(
      Array.isArray(firstMsg) ? firstMsg[0] : "No se puede crear el usuario"
    );
  }

  const result = await response.json();
  return result;
}

export async function getMeApi(token) {
  const url = `${API_URL}/api/v1/auth/me/`;
  const params = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await fetch(url, params);
  if (response.status !== 200) {
    throw new Error("Sesión expirada o token inválido");
  }
  const result = await response.json();
  return result;
}

export async function getSoapCountryApi(countryCode = "MX") {
  const url = `${API_URL}/api/v1/soap/country/?code=${encodeURIComponent(
    countryCode
  )}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("No se pudo consultar el servicio SOAP");
  }
  return await response.json();
}
