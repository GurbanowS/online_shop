import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <section className="home">
      <h1>Добро пожаловать в MyShop!</h1>
      <p>Лучшие товары по отличным ценам.</p>
      <Link className="btn" to="/products">Перейти в каталог</Link>
    </section>
  );
};

export default Home;
