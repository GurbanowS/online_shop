import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";

/**
 * Minimal fetch hook used across pages.
 *
 * @param {string|null} url - relative API path, e.g. "/products"
 * @param {any[]} deps - additional deps that trigger refetch
 */
export default function useFetch(url, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(Boolean(url));
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    async function run() {
      if (!url) return;
      setLoading(true);
      setError(null);
      try {
        const res = await axiosClient.get(url);
        if (!cancelled) setData(res.data);
      } catch (e) {
        if (!cancelled) setError(e);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    run();
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url, ...deps]);

  return { data, loading, error, setData };
}
