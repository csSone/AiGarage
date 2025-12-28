/**
 * Common API response types for AiGarage frontend
 */

/**
 * Generic API response wrapper
 */
export interface ApiResponse<T = unknown> {
  data: T
  status: number
  message?: string
}

/**
 * API error response structure
 */
export interface ApiError {
  error: {
    code: string
    message: string
    details?: string
  }
  status: number
  path?: string
}

/**
 * Pagination metadata for list responses
 */
export interface Pagination {
  page: number
  pageSize: number
  totalCount: number
  totalPages: number
}

/**
 * Paginated API response
 */
export interface PaginatedApiResponse<T> {
  data: T[]
  pagination: Pagination
  status: number
}

/**
 * Common HTTP error codes
 */
export type ErrorCode =
  | 'VALIDATION_ERROR'
  | 'NOT_FOUND'
  | 'UNAUTHORIZED'
  | 'FORBIDDEN'
  | 'INTERNAL_ERROR'
  | 'UNSUPPORTED_MEDIA_TYPE'

/**
 * Error code constants
 */
export const ErrorCode = {
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  NOT_FOUND: 'NOT_FOUND',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  UNSUPPORTED_MEDIA_TYPE: 'UNSUPPORTED_MEDIA_TYPE',
} as const

/**
 * HTTP status codes
 */
export type HttpStatus =
  | 200
  | 201
  | 204
  | 400
  | 401
  | 403
  | 404
  | 409
  | 422
  | 500

/**
 * HTTP status constants
 */
export const HttpStatus = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
} as const
