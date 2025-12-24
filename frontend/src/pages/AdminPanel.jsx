import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import axiosClient from "../api/axiosClient";
import useFetch from "../hooks/useFetch";

const apiBase = process.env.REACT_APP_API_URL || "http://localhost:5000/api";

const AdminPanel = () => {
  const [adminToken, setAdminToken] = useState(
    () => localStorage.getItem("admin_token") || ""
  );
  const [loginForm, setLoginForm] = useState({ username: "", password: "" });
  const [loginError, setLoginError] = useState("");

  const adminClient = useMemo(() => {
    return axios.create({
      baseURL: apiBase,
      headers: {
        "Content-Type": "application/json",
        ...(adminToken ? { Authorization: `Bearer ${adminToken}` } : {}),
      },
    });
  }, [adminToken]);

  const { data: products, loading, error, setData } = useFetch("/products", []);
  const { data: categories } = useFetch("/categories", []);
  const { data: brands } = useFetch("/brands", []);

  const [form, setForm] = useState({
    name: "",
    price: "",
    discount: "0",
    stock: "1",
    colors: "black",
    description: "",
    category_id: "",
    brand_id: "",
    image_1: "image.jpg",
  });
  const [actionError, setActionError] = useState("");

  useEffect(() => {
    if (!form.category_id && Array.isArray(categories) && categories[0]) {
      setForm((p) => ({ ...p, category_id: String(categories[0].id) }));
    }
  }, [categories, form.category_id]);

  useEffect(() => {
    if (!form.brand_id && Array.isArray(brands) && brands[0]) {
      setForm((p) => ({ ...p, brand_id: String(brands[0].id) }));
    }
  }, [brands, form.brand_id]);

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    setLoginError("");
    try {
      const res = await axiosClient.post("/admin/login", loginForm);
      const token = res.data.access_token;
      localStorage.setItem("admin_token", token);
      setAdminToken(token);
    } catch (e2) {
      setLoginError("Неверный логин или пароль администратора");
    }
  };

  const logoutAdmin = () => {
    localStorage.removeItem("admin_token");
    setAdminToken("");
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setActionError("");
    try {
      const payload = {
        ...form,
        price: Number(form.price),
        discount: Number(form.discount || 0),
        stock: Number(form.stock),
        category_id: Number(form.category_id),
        brand_id: Number(form.brand_id),
      };
      const res = await adminClient.post("/admin/products", payload);
      alert(`Товар добавлен: ${res.data.name}`);
      setForm((p) => ({ ...p, name: "", price: "", description: "" }));
      // update visible list without refetching
      if (Array.isArray(products)) setData([res.data, ...products]);
    } catch (e2) {
      setActionError("Не удалось добавить товар. Проверьте вход администратора.");
    }
  };

  return (
    <section className="admin-panel">
      <div className="admin-head">
        <h2>Админ-панель</h2>
        {adminToken && (
          <button className="btn-secondary" onClick={logoutAdmin}>
            Выйти
          </button>
        )}
      </div>

      {!adminToken ? (
        <form className="admin-form" onSubmit={handleAdminLogin}>
          <h3>Вход администратора</h3>
          <input
            placeholder="Username"
            value={loginForm.username}
            onChange={(e) =>
              setLoginForm((p) => ({ ...p, username: e.target.value }))
            }
            required
          />
          <input
            type="password"
            placeholder="Пароль"
            value={loginForm.password}
            onChange={(e) =>
              setLoginForm((p) => ({ ...p, password: e.target.value }))
            }
            required
          />
          {loginError && <p className="error">{loginError}</p>}
          <button type="submit" className="btn">
            Войти
          </button>
          <p className="hint">
            Подсказка: в базе должен существовать админ-пользователь.
          </p>
        </form>
      ) : (
        <form onSubmit={handleCreate} className="admin-form">
          <h3>Добавить товар</h3>
          <input
            type="text"
            placeholder="Название"
            value={form.name}
            onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))}
            required
          />
          <input
            type="number"
            placeholder="Цена"
            value={form.price}
            onChange={(e) => setForm((p) => ({ ...p, price: e.target.value }))}
            required
          />
          <input
            type="number"
            placeholder="Скидка (%)"
            value={form.discount}
            onChange={(e) =>
              setForm((p) => ({ ...p, discount: e.target.value }))
            }
          />
          <input
            type="number"
            placeholder="Остаток"
            value={form.stock}
            onChange={(e) => setForm((p) => ({ ...p, stock: e.target.value }))}
            required
          />
          <input
            type="text"
            placeholder="Цвета (строка)"
            value={form.colors}
            onChange={(e) => setForm((p) => ({ ...p, colors: e.target.value }))}
            required
          />
          <textarea
            placeholder="Описание"
            value={form.description}
            onChange={(e) =>
              setForm((p) => ({ ...p, description: e.target.value }))
            }
            required
          />
          <div className="row">
            <select
              value={form.category_id}
              onChange={(e) =>
                setForm((p) => ({ ...p, category_id: e.target.value }))
              }
            >
              {Array.isArray(categories) &&
                categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
            </select>
            <select
              value={form.brand_id}
              onChange={(e) =>
                setForm((p) => ({ ...p, brand_id: e.target.value }))
              }
            >
              {Array.isArray(brands) &&
                brands.map((b) => (
                  <option key={b.id} value={b.id}>
                    {b.name}
                  </option>
                ))}
            </select>
          </div>
          {actionError && <p className="error">{actionError}</p>}
          <button type="submit" className="btn">
            Добавить
          </button>
        </form>
      )}

      <hr />
      <h3>Товары</h3>
      {loading && <p>Загрузка...</p>}
      {error && <p>Ошибка загрузки</p>}
      <div className="admin-products">
        {Array.isArray(products) &&
          products.slice(0, 20).map((p) => (
            <div key={p.id} className="admin-product">
              <strong>{p.name}</strong>
              <span>{p.price} ₽</span>
            </div>
          ))}
      </div>
    </section>
  );
};

export default AdminPanel;
