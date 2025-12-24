import React from "react";
import { Link } from "react-router-dom";

const CartItem = ({ item, onRemove, onUpdate }) => {
  return (
    <div className="cart-item">
      <img src={item.image} alt={item.name} />
      <div className="cart-info">
        <h4 title={item.name}>{item.name}</h4>
        <p>{item.price} ₽</p>

        <div className="quantity-controls">
          <button onClick={() => onUpdate(item.id, item.quantity - 1)}>-</button>
          <span>{item.quantity}</span>
          <button onClick={() => onUpdate(item.id, item.quantity + 1)}>+</button>
        </div>

        <p>Итого: {(item.price * item.quantity).toFixed(2)} ₽</p>

        <div className="cart-actions">
          <Link className="btn-secondary" to={`/products/${item.id}`}>Детали</Link>
          <button className="btn-remove" onClick={() => onRemove(item.id)}>Удалить</button>
        </div>
      </div>
    </div>
  );
};

export default CartItem;
