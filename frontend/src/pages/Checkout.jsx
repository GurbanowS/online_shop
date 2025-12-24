import React, { useState } from "react";
import { useCart } from "../context/CartContext";
import { Link, useNavigate } from "react-router-dom";
import axiosClient from "../api/axiosClient";
import { useAuth } from "../context/AuthContext";

const Checkout = () => {
  const { cart, total, clearCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", address: "", phone: "" });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      navigate("/login");
      return;
    }
    setSubmitting(true);
    setError("");
    try {
      const items = cart.map((item) => ({
        product_id: item.id,
        quantity: item.quantity || 1,
      }));
      const res = await axiosClient.post("/orders", {
        items,
        shipping: form,
      });
      alert(`Заказ оформлен! Номер счета: ${res.data.invoice}`);
      clearCart();
      navigate("/products");
    } catch (e2) {
      setError("Не удалось оформить заказ. Проверьте вход в систему и повторите попытку.");
    } finally {
      setSubmitting(false);
    }
  };

  if (cart.length === 0) {
    return (
      <section className="checkout">
        <h2>Корзина пуста</h2>
        <Link className="btn" to="/products">Вернуться в каталог</Link>
      </section>
    );
  }

  return (
    <section className="checkout">
      <h2>Оформление заказа</h2>
      {!user && (
        <p className="hint">
          Для оформления заказа нужно <Link to="/login">войти</Link>.
        </p>
      )}
      <form onSubmit={handleSubmit} className="checkout-form">
        <input
          name="name"
          placeholder="Ваше имя"
          value={form.name}
          onChange={handleChange}
          required
        />
        <input
          name="address"
          placeholder="Адрес доставки"
          value={form.address}
          onChange={handleChange}
          required
        />
        <input
          name="phone"
          placeholder="Телефон"
          value={form.phone}
          onChange={handleChange}
          required
        />
        <p>Сумма заказа: {total.toFixed(2)} ₽</p>
        {error && <p className="error">{error}</p>}
        <button type="submit" className="btn" disabled={submitting}>
          {submitting ? "Оформляем..." : "Подтвердить заказ"}
        </button>
      </form>
    </section>
  );
};

export default Checkout;
