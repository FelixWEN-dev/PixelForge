import { request } from './request';

const API_PREFIX = '/api/v1';

/**
 * 用户注册
 * @param {Object} data - { username, password }
 */
export function register(data) {
  return request(`${API_PREFIX}/auth/register`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * 用户登录
 * @param {Object} data - { username, password }
 */
export function login(data) {
  return request(`${API_PREFIX}/auth/login`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser() {
  return request(`${API_PREFIX}/auth/me`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
    },
  });
}

/**
 * 退出登录
 */
export function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
}

/**
 * 检查是否已登录
 */
export function isLoggedIn() {
  return !!localStorage.getItem('token');
}

/**
 * 获取本地存储的用户信息
 */
export function getUser() {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
}
