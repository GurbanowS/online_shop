import React, { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import ProductCard from "../components/ProductCard";
import useFetch from "../hooks/useFetch";
import { useCart } from "../context/CartContext";

const mapProduct = (p) => ({
  id: p.id,
  name: p.name,
  price: p.discount
    ? Math.round((p.price * (100 - p.discount)) / 100)
    : p.price,
  rawPrice: p.price,
  discount: p.discount,
  image: (p.images && p.images[0]) || "",
});

const ProductList = () => {
  const { addToCart } = useCart();
  const [q, setQ] = useState("");

  const url = useMemo(() => {
    const qs = q ? `?q=${encodeURIComponent(q)}` : "";
    return `/products${qs}`;
  }, [q]);

  const { data, loading, error } = useFetch(url, [q]);

  const products = useMemo(() => (Array.isArray(data) ? data.map(mapProduct) : []), [data]);

  return (
    <section className="product-list">
      <div className="product-list-header">
        <h2>Каталог товаров</h2>
        <input
          className="search"
          placeholder="Поиск..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
      </div>

      {loading && <p>Загрузка...</p>}
      {error && <p>Ошибка загрузки</p>}

      <div className="product-grid">
        {products.map((p) => (
          <div key={p.id} className="product-link">
            <ProductCard product={p} onAddToCart={addToCart} />
            <Link to={`/products/${p.id}`} className="btn-secondary details-link">
              Детали
            </Link>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ProductList;
