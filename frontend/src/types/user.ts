import { z } from 'zod';

export const UserSchema = z.object({
  id: z.number(),
  email: z.string().email(),
  first_name: z.string(),
  last_name: z.string(),
  avatar: z.string().url(),
});

export const UserResponseSchema = z.object({
  data: UserSchema,
});

export const ApiErrorSchema = z.object({
  detail: z.string(),
  status_code: z.number().optional(),
});

export type User = z.infer<typeof UserSchema>;
export type UserResponse = z.infer<typeof UserResponseSchema>;
export type ApiError = z.infer<typeof ApiErrorSchema>;