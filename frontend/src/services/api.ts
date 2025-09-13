import type { UserResponse } from '../types/user';

const API_BASE_URL = 'http://localhost:8000';

export const fetchUser = async (userId: number): Promise<UserResponse> => {
  const response = await fetch(`${API_BASE_URL}/user/${userId}`);
  
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch user data');
    } catch (parseError) {
      if (response.status === 404) {
        throw new Error('User not found');
      } else if (response.status === 503) {
        throw new Error('Service temporarily unavailable. Please try again later.');
      }
      throw new Error('Failed to fetch user data');
    }
  }
  
  return response.json();
};