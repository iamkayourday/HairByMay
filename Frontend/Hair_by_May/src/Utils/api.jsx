// src/utils/api.js
const API_BASE_URL = 'http://localhost:8000/api/v1';

export const fetchCategories = async () => {
  const response = await fetch(`${API_BASE_URL}/categories/`);
  if (!response.ok) throw new Error('Failed to fetch categories');
  return await response.json();
};

export const fetchCategoryDetails = async (id) => {
  const response = await fetch(`${API_BASE_URL}/categories/${id}/`);
  if (!response.ok) throw new Error('Failed to fetch category details');
  return await response.json();
};

export const fetchServiceDetails = async (id) => {
  const response = await fetch(`${API_BASE_URL}/services/${id}/`);
  if (!response.ok) throw new Error('Failed to fetch service details');
  return await response.json();
};

export const createAppointment = async (appointmentData) => {
  const response = await fetch(`${API_BASE_URL}/appointments/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(appointmentData),
  });
  if (!response.ok) throw new Error('Failed to create appointment');
  return await response.json();
};