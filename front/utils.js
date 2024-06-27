import { jwtDecode } from "jwt-decode";

export const apiUrl = "http://localhost:5000";

export const updateToken = async () => {
  const decodedToken = jwtDecode(localStorage.getItem("access_token"));
  const currentTime = Date.now() / 1000;
  if (decodedToken.exp > currentTime) {
    const refreshResponse = await fetch("/auth/refresh", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        "Refresh-Token": localStorage.getItem("refresh_token"),
      },
    });

    if (refreshResponse.ok) {
      const { access_token: newAccessToken, refresh_token: newRefreshToken } =
        await refreshResponse.json();
      localStorage.setItem("access_token", newAccessToken);
      localStorage.setItem("refresh_token", newRefreshToken);
    }
  }
};
