import { UserResponseSchema, ApiErrorSchema, type UserResponse } from '../types/user';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export class ApiError extends Error {
  public statusCode?: number;

  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
  }
}

export const fetchUser = async (userId: number): Promise<UserResponse> => {
  const response = await fetch(`${API_BASE_URL}/user/${userId}`);

  if (!response.ok) {
    try {
      const errorData = await response.json();
      const validatedError = ApiErrorSchema.safeParse(errorData);

      if (validatedError.success) {
        throw new ApiError(
          validatedError.data.detail,
          validatedError.data.status_code || response.status
        );
      }
    } catch (parseError) {
      if (parseError instanceof ApiError) {
        throw parseError;
      }
    }

    // Fallback error messages
    if (response.status === 404) {
      throw new ApiError('User not found', 404);
    } else if (response.status === 503) {
      throw new ApiError('Service temporarily unavailable. Please try again later.', 503);
    }

    throw new ApiError('Failed to fetch user data', response.status);
  }

  const data = await response.json();
  const validatedData = UserResponseSchema.safeParse(data);

  if (!validatedData.success) {
    throw new ApiError('Invalid response format from server');
  }

  return validatedData.data;
};