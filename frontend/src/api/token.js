const TOKEN = import.meta.env.VITE_LOCAL_STORAGE_ITEM_NAME || "TOKEN";

export function setToken(token) {
  window.localStorage.setItem(TOKEN, token);
}

export function getToken() {
  return window.localStorage.getItem(TOKEN);
}

export function removeToken() {
  window.localStorage.removeItem(TOKEN);
}
