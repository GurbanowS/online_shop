import React from "react";

const ProductCard = ({ product, onAddToCart }) => {
  return (
    <div className="product-card" title={product.name}>
      <img
        src={product.image}
        alt={product.name}
        className="product-image"
      />
      <h3 className="product-title" title={product.name}>
        {product.name}
      </h3>
      <p className="product-price">{product.price} ₽</p>

      <div className="product-actions">
        <button className="btn" onClick={() => onAddToCart(product)}>
          Добавить в корзину
        </button>
      </div>
    </div>
  );
};

export default ProductCard;
