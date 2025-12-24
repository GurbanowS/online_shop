import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import CartItem from "../components/CartItem";

const Cart = () => {
  const { cart, removeFromCart, updateQuantity, total, clearCart } = useCart();
  const navigate = useNavigate();

  const handleCheckout = () => {
    navigate("/checkout");
  };

  if (cart.length === 0) {
    return (
      <section className="cart">
        <h2>Корзина пуста 🛒</h2>
        <Link className="btn" to="/products">Перейти в каталог</Link>
      </section>
    );
  }

  return (
    <section className="cart">
      <h2>Ваша корзина</h2>
      {cart.map((item) => (
        <CartItem
          key={item.id}
          item={item}
          onRemove={removeFromCart}
          onUpdate={updateQuantity}
        />
      ))}

      <div className="cart-summary">
        <h3>Общая сумма: {total.toFixed(2)} ₽</h3>
        <div className="cart-buttons">
          <button className="btn" onClick={handleCheckout}>Оформить заказ</button>
          <button className="btn-secondary" onClick={clearCart}>Очистить корзину</button>
        </div>
      </div>
    </section>
  );
};

export default Cart;
