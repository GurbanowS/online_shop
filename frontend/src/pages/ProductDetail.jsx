import React, { useMemo } from "react";
import { useParams, Link } from "react-router-dom";
import useFetch from "../hooks/useFetch";
import { useCart } from "../context/CartContext";

const ProductDetail = () => {
  const { id } = useParams();
  const { addToCart } = useCart();

  const url = useMemo(() => `/products/${id}`, [id]);
  const { data: p, loading, error } = useFetch(url, [id]);

  const mapped = p
    ? {
        id: p.id,
        name: p.name,
        price: p.discount
          ? Math.round((p.price * (100 - p.discount)) / 100)
          : p.price,
        image: (p.images && p.images[0]) || "",
        description: p.description,
        brand: p.brand,
        category: p.category,
      }
    : null;

  if (loading) {
    return (
      <section className="product-detail">
        <p>Загрузка...</p>
      </section>
    );
  }

  if (error || !mapped) {
    return (
      <section className="product-detail">
        <h2>Товар не найден</h2>
        <Link className="btn" to="/products">
          Вернуться в каталог
        </Link>
      </section>
    );
  }

  return (
    <section className="product-detail">
      <div className="product-detail-container">
        <img src={mapped.image} alt={mapped.name} className="detail-image" />
        <div className="detail-info">
          <h2>{mapped.name}</h2>
          <p className="detail-price">{mapped.price} ₽</p>
          {(mapped.brand || mapped.category) && (
            <p className="detail-meta">
              {mapped.brand ? `Бренд: ${mapped.brand.name}` : ""}
              {mapped.brand && mapped.category ? " · " : ""}
              {mapped.category ? `Категория: ${mapped.category.name}` : ""}
            </p>
          )}
          <p className="detail-desc">{mapped.description}</p>
          <div className="detail-buttons">
            <button className="btn" onClick={() => addToCart(mapped)}>
              Добавить в корзину
            </button>
            <Link className="btn-secondary" to="/products">
              Назад
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProductDetail;
