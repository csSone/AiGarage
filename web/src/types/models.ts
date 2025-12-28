/**
 * Common data model types for AiGarage frontend
 */

/**
 * User model
 */
export interface User {
  id: string
  name: string
  email: string
  createdAt?: string
  updatedAt?: string
}

/**
 * Chat message for LLM interactions
 */
export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
}

/**
 * Chat completion request
 */
export interface ChatCompletionRequest {
  messages: ChatMessage[]
  model: string
  temperature?: number
  maxTokens?: number
  stream?: boolean
}

/**
 * Chat completion response
 */
export interface ChatCompletionResponse {
  content: string
  finishReason: 'stop' | 'length' | 'content_filter'
  usage: {
    promptTokens: number
    completionTokens: number
    totalTokens: number
  }
}

/**
 * Model information
 */
export interface ModelInfo {
  id: string
  name: string
  description?: string
  contextLength: number
  version: string
}

/**
 * Agent configuration
 */
export interface AgentConfig {
  id: string
  name: string
  description?: string
  model: string
  systemPrompt?: string
  temperature?: number
  maxTokens?: number
  enabled: boolean
}

/**
 * Task status
 */
export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed'

/**
 * Task status constants
 */
export const TaskStatus = {
  PENDING: 'pending',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
} as const

/**
 * Task status values array
 */
export const TaskStatusValues = ['pending', 'running', 'completed', 'failed'] as const

/**
 * Agent task
 */
export interface AgentTask {
  id: string
  agentId: string
  status: TaskStatus
  input: string
  output?: string
  error?: string
  createdAt: string
  updatedAt: string
}
