import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">Godamn Shop</Link>
      </div>
      <ul className="navbar-links">
        <li><Link to="/products">Каталог</Link></li>
        <li><Link to="/cart">Корзина</Link></li>
        <li><Link to="/checkout">Оформление</Link></li>
        <li><Link to="/admin">Админ</Link></li>
        {user ? (
          <>
            <li><button className="btn" onClick={logout}>Выйти</button></li>
          </>
        ) : (
          <>
            <li><Link to="/login">Войти</Link></li>
            <li><Link to="/register">Регистрация</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
