import React, { useEffect, useState } from "react";
import { Button, Icon, Label } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";
import { getSoapCountryApi } from "../../api/user";

const WEATHER_API_URL =
  "https://api.open-meteo.com/v1/forecast?latitude=32.4561&longitude=-114.7719&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=auto";
const QUOTE_API_URL = "https://dummyjson.com/quotes/random";

export function Dashboard() {
  const { logout, auth } = useAuth();
  const user = auth?.me || {};

  // Estado para API de terceros (Open-Meteo + DummyJSON Quotes usando fetch)
  const [weather, setWeather] = useState(null);
  const [quote, setQuote] = useState(null);
  const [loadingExternal, setLoadingExternal] = useState(true);

  // Estado para Web Service SOAP (consumido desde Django con zeep)
  const [soapCode, setSoapCode] = useState("MX");
  const [soapData, setSoapData] = useState(null);
  const [loadingSoap, setLoadingSoap] = useState(false);

  const fetchExternalApis = async () => {
    setLoadingExternal(true);
    try {
      const [weatherRes, quoteRes] = await Promise.all([
        fetch(WEATHER_API_URL),
        fetch(QUOTE_API_URL),
      ]);
      const weatherJson = await weatherRes.json();
      const quoteJson = await quoteRes.json();
      setWeather(weatherJson);
      setQuote(quoteJson);
    } catch (err) {
      console.error("Error al consultar API de terceros:", err);
    } finally {
      setLoadingExternal(false);
    }
  };

  const fetchSoapCountry = async (code) => {
    setSoapCode(code);
    setLoadingSoap(true);
    try {
      const data = await getSoapCountryApi(code);
      setSoapData(data);
    } catch (err) {
      console.error("Error SOAP:", err);
    } finally {
      setLoadingSoap(false);
    }
  };

  useEffect(() => {
    fetchExternalApis();
    fetchSoapCountry("MX");
  }, []);

  const fullName =
    [user.first_name, user.last_name].filter(Boolean).join(" ") ||
    user.username ||
    user.email;

  return (
    <div className="dashboard-page">
      {/* BARRA SUPERIOR INSTITUCIONAL */}
      <header className="dashboard-topbar">
        <div className="dashboard-topbar__brand">
          <span className="badge-ut">UTSLRC • IDGS 9-2</span>
          <div>
            <h2>Tienda Online — Panel de Control Protegido (JWT)</h2>
            <p>
              Desarrollo Web Integral • Sesión activa mediante{" "}
              <code>AuthContext</code> y <code>useAuth()</code>
            </p>
          </div>
        </div>

        <div className="dashboard-topbar__user">
          <div className="user-pill">
            <Icon name="user circle" size="large" />
            <div>
              <strong>Bienvenido, {fullName}</strong>
              <span>
                {user.email} • Matrícula: {user.matricula || "23304031"}
              </span>
            </div>
          </div>
          <Button
            color="red"
            icon="sign-out"
            content="Cerrar Sesión"
            onClick={logout}
          />
        </div>
      </header>

      <main className="dashboard-container">
        {/* SECCIÓN 1: DATOS DEL USUARIO AUTENTICADO (/api/v1/auth/me/) */}
        <section className="dash-card profile-card" id="section-auth-me">
          <div className="dash-card__header">
            <div>
              <Label color="teal" size="small">
                WEB SERVICE PROPIO (JWT)
              </Label>
              <h3>
                <Icon name="shield alternate" /> Datos del Usuario Logueado (
                <code>GET /api/v1/auth/me/</code>)
              </h3>
            </div>
            <span className="status-ok">
              <Icon name="check circle" /> 200 OK • Bearer Token Activo
            </span>
          </div>

          <div className="profile-grid">
            <div className="profile-item">
              <span className="lbl">Nombre Completo (AuthContext)</span>
              <strong>{fullName}</strong>
            </div>
            <div className="profile-item">
              <span className="lbl">Correo Electrónico (USERNAME_FIELD)</span>
              <strong>{user.email}</strong>
            </div>
            <div className="profile-item">
              <span className="lbl">Usuario (Username)</span>
              <strong>@{user.username}</strong>
            </div>
            <div className="profile-item">
              <span className="lbl">Matrícula / Carrera</span>
              <strong>
                {user.matricula || "23304031"} — {user.carrera || "IDGS 9-2"}
              </strong>
            </div>
            <div className="profile-item">
              <span className="lbl">Rol / Estado</span>
              <strong>
                {user.is_staff ? "Administrador (Staff)" : "Cliente Activo"}
              </strong>
            </div>
            <div className="profile-item">
              <span className="lbl">Seguridad Serializer</span>
              <strong style={{ color: "#059669" }}>
                password oculto (write_only=True)
              </strong>
            </div>
          </div>
        </section>

        {/* SECCIÓN 2: WIDGET DE API DE TERCEROS (FETCH) */}
        <section className="dash-card external-api-card" id="widget-third-party">
          <div className="dash-card__header">
            <div>
              <Label color="blue" size="small">
                PARTE 2: API DE TERCEROS (FETCH)
              </Label>
              <h3>
                <Icon name="cloud sun" /> Widget de Clima en Tiempo Real y Frase
                del Día (Open-Meteo API + DummyJSON API)
              </h3>
            </div>
            <Button
              size="tiny"
              basic
              color="blue"
              icon="refresh"
              content="Actualizar con fetch()"
              loading={loadingExternal}
              onClick={fetchExternalApis}
            />
          </div>

          <div className="external-widgets-grid">
            {/* Widget 1: Clima en San Luis Río Colorado */}
            <div className="ext-box weather-box">
              <div className="ext-box__top">
                <div>
                  <span className="ext-tag">
                    GET https://api.open-meteo.com/v1/forecast
                  </span>
                  <h4>Clima Actual — San Luis Río Colorado, Sonora</h4>
                </div>
                <div className="temp-badge">
                  {weather?.current
                    ? `${weather.current.temperature_2m} ${weather.current_units?.temperature_2m || "°C"}`
                    : "Cargando..."}
                </div>
              </div>

              {weather?.current && (
                <div className="weather-metrics">
                  <div className="metric">
                    <span>Humedad Relativa</span>
                    <strong>
                      {weather.current.relative_humidity_2m}
                      {weather.current_units?.relative_humidity_2m || "%"}
                    </strong>
                  </div>
                  <div className="metric">
                    <span>Velocidad del Viento</span>
                    <strong>
                      {weather.current.wind_speed_10m}{" "}
                      {weather.current_units?.wind_speed_10m || "km/h"}
                    </strong>
                  </div>
                  <div className="metric">
                    <span>Coordenadas / Elevación</span>
                    <strong>
                      {weather.latitude.toFixed(2)}°N,{" "}
                      {weather.longitude.toFixed(2)}°O ({weather.elevation}m)
                    </strong>
                  </div>
                  <div className="metric">
                    <span>Zona Horaria / Hora UTC</span>
                    <strong>{weather.current.time}</strong>
                  </div>
                </div>
              )}
            </div>

            {/* Widget 2: Frase Motivadora */}
            <div className="ext-box quote-box">
              <span className="ext-tag">
                GET https://dummyjson.com/quotes/random
              </span>
              <h4>Frase Inspiradora del Día (API Pública Externa)</h4>
              {quote ? (
                <blockquote>
                  “{quote.quote}”
                  <footer>
                    — <strong>{quote.author}</strong> (ID #{quote.id})
                  </footer>
                </blockquote>
              ) : (
                <p>Cargando frase desde API externa...</p>
              )}
            </div>
          </div>
        </section>

        {/* SECCIÓN 3: WEB SERVICE SOAP DESDE DJANGO CON ZEEP */}
        <section className="dash-card soap-card" id="section-soap-widget">
          <div className="dash-card__header">
            <div>
              <Label color="purple" size="small">
                PARTE 3: WEB SERVICE SOAP (ZEEP)
              </Label>
              <h3>
                <Icon name="globe" /> Consumo de Servicio SOAP Público desde
                Django (<code>GET /api/v1/soap/country/?code={soapCode}</code>)
              </h3>
            </div>
            <div className="soap-country-buttons">
              {["MX", "US", "ES", "CO", "JP"].map((c) => (
                <Button
                  key={c}
                  size="mini"
                  color={soapCode === c ? "purple" : undefined}
                  basic={soapCode !== c}
                  onClick={() => fetchSoapCountry(c)}
                  loading={loadingSoap && soapCode === c}
                >
                  {c}
                </Button>
              ))}
            </div>
          </div>

          {soapData && (
            <div className="soap-grid">
              <div className="soap-details">
                <div className="soap-row">
                  <span>Protocolo / Cliente:</span>
                  <strong>{soapData.protocol}</strong>
                </div>
                <div className="soap-row">
                  <span>WSDL Consumido:</span>
                  <code>{soapData.wsdl_url}</code>
                </div>
                <div className="soap-row">
                  <span>País ({soapData.iso_code}):</span>
                  <strong>{soapData.country_name}</strong>
                </div>
                <div className="soap-row">
                  <span>Capital Oficial:</span>
                  <strong>{soapData.capital_city}</strong>
                </div>
                <div className="soap-row">
                  <span>Divisa Oficial (ISO):</span>
                  <strong>
                    {soapData.currency_name} ({soapData.currency_iso})
                  </strong>
                </div>
                <div className="soap-row">
                  <span>Código Telefónico / Continente:</span>
                  <strong>
                    {soapData.phone_code} (Continente: {soapData.continent_code})
                  </strong>
                </div>
              </div>

              <div className="soap-json-preview">
                <div className="soap-json-preview__title">
                  Respuesta JSON del Endpoint Django SOAP
                </div>
                <pre>{JSON.stringify(soapData, null, 2)}</pre>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
