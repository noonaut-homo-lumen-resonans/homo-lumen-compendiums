/**
 * Ubuntu Playground Client - TypeScript Wrapper
 *
 * Provides a simple, type-safe interface for agents to interact with the
 * Ubuntu Playground shared workspace API.
 *
 * @example
 * ```typescript
 * const client = new PlaygroundClient('code', 'code-api-key');
 *
 * // Read Manus' synthesis
 * const content = await client.read('manus/synthesis.md');
 *
 * // Write implementation notes
 * await client.write('code/implementation.md', 'My notes...');
 *
 * // Commit changes
 * await client.commit('Add implementation notes', ['code/implementation.md']);
 * ```
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

// ===========================
// TYPES
// ===========================

export interface PlaygroundConfig {
  agentName: string;
  apiKey: string;
  baseURL?: string;
  timeout?: number;
}

export interface ReadResponse {
  content: string;
  path: string;
}

export interface WriteResponse {
  success: boolean;
  path: string;
  size: number;
}

export interface FileInfo {
  path: string;
  type: 'file' | 'directory';
  size?: number;
}

export interface ListResponse {
  files: FileInfo[];
  count: number;
}

export interface CommitResponse {
  success: boolean;
  message: string;
  agent: string;
  files: string[];
}

export interface HealthResponse {
  status: 'healthy' | 'degraded';
  redis: string;
  database: string;
  workspace: string;
  timestamp: string;
}

export interface AgentEvent {
  agent: string;
  action: string;
  path?: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

// ===========================
// ERRORS
// ===========================

export class PlaygroundError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public response?: any
  ) {
    super(message);
    this.name = 'PlaygroundError';
  }
}

export class AuthenticationError extends PlaygroundError {
  constructor(message: string = 'Invalid API key') {
    super(message, 401);
    this.name = 'AuthenticationError';
  }
}

export class PermissionError extends PlaygroundError {
  constructor(message: string = 'Permission denied') {
    super(message, 403);
    this.name = 'PermissionError';
  }
}

export class NotFoundError extends PlaygroundError {
  constructor(message: string = 'File not found') {
    super(message, 404);
    this.name = 'NotFoundError';
  }
}

// ===========================
// PLAYGROUND CLIENT
// ===========================

export class PlaygroundClient {
  private api: AxiosInstance;
  private agentName: string;

  constructor(config: PlaygroundConfig | string, apiKey?: string) {
    // Support both object and string constructor
    if (typeof config === 'string') {
      this.agentName = config;
      if (!apiKey) {
        throw new Error('API key required when using string constructor');
      }
      config = {
        agentName: config,
        apiKey,
      };
    } else {
      this.agentName = config.agentName;
    }

    this.api = axios.create({
      baseURL: config.baseURL || 'http://localhost:8000',
      headers: {
        'X-API-Key': config.apiKey,
        'Content-Type': 'application/json',
      },
      timeout: config.timeout || 30000,
    });

    // Add error interceptor
    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        return Promise.reject(this.handleError(error));
      }
    );
  }

  /**
   * Read a file from the shared workspace
   *
   * @param path - Relative path to file (e.g., 'manus/synthesis.md')
   * @returns File content
   * @throws {NotFoundError} If file doesn't exist
   * @throws {PermissionError} If agent lacks read permission
   */
  async read(path: string): Promise<string> {
    const response = await this.api.post<ReadResponse>('/api/workspace/read', { path });
    return response.data.content;
  }

  /**
   * Write a file to the shared workspace
   *
   * @param path - Relative path to file (e.g., 'code/notes.md')
   * @param content - File content
   * @returns True if successful
   * @throws {PermissionError} If agent lacks write permission for this path
   */
  async write(path: string, content: string): Promise<boolean> {
    const response = await this.api.post<WriteResponse>('/api/workspace/write', {
      path,
      content,
    });
    return response.data.success;
  }

  /**
   * List files in a directory
   *
   * @param path - Relative path to directory (default: root)
   * @returns Array of file information
   * @throws {NotFoundError} If directory doesn't exist
   */
  async list(path: string = ''): Promise<FileInfo[]> {
    const response = await this.api.post<ListResponse>('/api/workspace/list', { path });
    return response.data.files;
  }

  /**
   * Commit files to Git
   *
   * @param message - Commit message
   * @param files - Array of file paths to commit
   * @returns True if successful
   * @throws {PermissionError} If agent lacks commit permission
   */
  async commit(message: string, files: string[]): Promise<boolean> {
    const response = await this.api.post<CommitResponse>('/api/git/commit', {
      message,
      files,
      agent_name: this.agentName,
    });
    return response.data.success;
  }

  /**
   * Check API health status
   *
   * @returns Health status information
   */
  async health(): Promise<HealthResponse> {
    const response = await this.api.get<HealthResponse>('/health');
    return response.data;
  }

  /**
   * Subscribe to real-time workspace events
   *
   * NOTE: This requires WebSocket or Server-Sent Events implementation on the server.
   * Currently a placeholder for Phase 2.
   *
   * @param channel - Event channel to subscribe to
   * @param callback - Function to call when event is received
   */
  async subscribe(channel: string, callback: (event: AgentEvent) => void): Promise<void> {
    throw new Error('Subscribe not yet implemented (Phase 2 feature)');
    // TODO: Implement WebSocket or SSE subscription to Redis pub/sub
  }

  /**
   * Get the current agent name
   */
  getAgentName(): string {
    return this.agentName;
  }

  /**
   * Handle Axios errors and convert to Playground-specific errors
   */
  private handleError(error: AxiosError): PlaygroundError {
    if (!error.response) {
      return new PlaygroundError(
        `Network error: ${error.message}`,
        undefined,
        error
      );
    }

    const status = error.response.status;
    const message = (error.response.data as any)?.detail || error.message;

    switch (status) {
      case 401:
        return new AuthenticationError(message);
      case 403:
        return new PermissionError(message);
      case 404:
        return new NotFoundError(message);
      default:
        return new PlaygroundError(message, status, error.response.data);
    }
  }
}

// ===========================
// UTILITY FUNCTIONS
// ===========================

/**
 * Create a PlaygroundClient instance with environment variables
 *
 * Expects the following environment variables:
 * - AGENT_NAME: Name of the agent
 * - PLAYGROUND_API_KEY: API key for authentication
 * - PLAYGROUND_BASE_URL: Base URL of the Playground API (optional, defaults to localhost:8000)
 *
 * @returns Configured PlaygroundClient instance
 */
export function createClientFromEnv(): PlaygroundClient {
  const agentName = process.env.AGENT_NAME;
  const apiKey = process.env.PLAYGROUND_API_KEY;
  const baseURL = process.env.PLAYGROUND_BASE_URL;

  if (!agentName || !apiKey) {
    throw new Error('Missing required environment variables: AGENT_NAME, PLAYGROUND_API_KEY');
  }

  return new PlaygroundClient({
    agentName,
    apiKey,
    baseURL,
  });
}

/**
 * Check if a path is within an agent's writable workspace
 *
 * @param agentName - Name of the agent
 * @param path - Path to check
 * @returns True if agent can write to this path
 */
export function canAgentWrite(agentName: string, path: string): boolean {
  // Agents can write to:
  // 1. Their own workspace (e.g., 'code/' for agent 'code')
  // 2. The shared workspace ('shared/')
  // 3. Experiments workspace ('experiments/')

  const writable = [
    `${agentName}/`,
    'shared/',
    'experiments/',
  ];

  return writable.some(prefix => path.startsWith(prefix));
}

// ===========================
// EXPORTS
// ===========================

export default PlaygroundClient;
