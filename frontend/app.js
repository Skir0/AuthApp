const API_BASE = "http://127.0.0.1:8000";

const tabs = document.querySelectorAll("[data-tab]");
const forms = {
  login: document.querySelector("#login-form"),
  register: document.querySelector("#register-form"),
};
const notice = document.querySelector("#notice");
const profile = document.querySelector("#profile");
const checkProfileButton = document.querySelector("#check-profile");
let accessToken = sessionStorage.getItem("access_token");

function showNotice(message, isError = false) {
  notice.textContent = message;
  notice.classList.toggle("error", isError);
}

function setActiveTab(tabName) {
  tabs.forEach((tab) => tab.classList.toggle("is-active", tab.dataset.tab === tabName));
  Object.entries(forms).forEach(([name, form]) => form.classList.toggle("is-hidden", name !== tabName));
  profile.classList.add("is-hidden");
  showNotice("");
}

function formDataToObject(form) {
  return Object.fromEntries(new FormData(form).entries());
}

async function request(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    credentials: "include",
    headers,
  });

  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = Array.isArray(body.detail)
      ? body.detail.map((item) => item.msg).join(", ")
      : body.detail;
    throw new Error(detail || "Не удалось выполнить запрос");
  }
  return body;
}

function showProfile(user) {
  document.querySelector("#profile-name").textContent =
    [user.first_name, user.last_name].filter(Boolean).join(" ") || "Пользователь";
  document.querySelector("#profile-email").textContent = user.email || "";
  Object.values(forms).forEach((form) => form.classList.add("is-hidden"));
  profile.classList.remove("is-hidden");
}

tabs.forEach((tab) => tab.addEventListener("click", () => setActiveTab(tab.dataset.tab)));

forms.login.addEventListener("submit", async (event) => {
  event.preventDefault();
  showNotice("Выполняется вход...");
  try {
    const loginResult = await request("/auth/login/", {
      method: "POST",
      body: JSON.stringify(formDataToObject(forms.login)),
    });
    accessToken = loginResult.access_token;
    sessionStorage.setItem("access_token", accessToken);
    const user = await request("/auth/me/");
    showProfile(user);
    showNotice("Вы успешно вошли и вас взломали. За ваш счет куплено 42 верблюда");
  } catch (error) {
    showNotice(error.message, true);
  }
});

forms.register.addEventListener("submit", async (event) => {
  event.preventDefault();
  showNotice("Создаём аккаунт...");
  try {
    await request("/auth/register/", {
      method: "POST",
      body: JSON.stringify(formDataToObject(forms.register)),
    });
    forms.register.reset();
    setActiveTab("login");
    showNotice("Вам на почту отправлена ссылка на регистрацию, перейдите в почту");
  } catch (error) {
    showNotice(error.message, true);
  }
});

checkProfileButton.addEventListener("click", async () => {
  showNotice("Проверяем сессию...");
  try {
    showProfile(await request("/auth/me/"));
    showNotice("Сессия активна.");
  } catch (error) {
    showNotice("Активная сессия не найдена.", true);
  }
});

document.querySelector("#logout-button").addEventListener("click", async () => {
  try {
    await request("/auth/logout/", { method: "POST" });
    accessToken = null;
    sessionStorage.removeItem("access_token");
    profile.classList.add("is-hidden");
    setActiveTab("login");
    showNotice("Вы вышли из аккаунта.");
  } catch (error) {
    showNotice(error.message, true);
  }
});
