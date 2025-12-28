/**
 * Central type exports for AiGarage frontend
 *
 * Usage:
 * import type { User, ApiResponse } from '@/types'
 * or
 * import { ApiResponse, User } from '@/types'
 */

// Export all API-related types
export type {
  ApiResponse,
  ApiError,
  Pagination,
  PaginatedApiResponse,
  ErrorCode,
  HttpStatus,
} from './api'

export { ErrorCode as ErrorCodeConst, HttpStatus as HttpStatusConst } from './api'

// Export all model types
export type {
  User,
  ChatMessage,
  ChatCompletionRequest,
  ChatCompletionResponse,
  ModelInfo,
  AgentConfig,
  AgentTask,
  TaskStatus,
} from './models'

export { TaskStatus as TaskStatusConst, TaskStatusValues } from './models'

/**
 * Common utility types
 */

/**
 * Make specific properties optional
 */
export type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>

/**
 * Make specific properties required
 */
export type RequiredBy<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>

/**
 * Deep partial type
 */
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends Array<infer U>
    ? Array<DeepPartial<U>>
    : T[P] extends ReadonlyArray<infer U>
    ? ReadonlyArray<DeepPartial<U>>
    : T[P] extends object
    ? DeepPartial<T[P]>
    : T[P]
}

/**
 * Extract promise return type
 */
export type AsyncReturnType<T extends (...args: unknown[]) => Promise<unknown>> =
  T extends (...args: unknown[]) => Promise<infer R> ? R : never
