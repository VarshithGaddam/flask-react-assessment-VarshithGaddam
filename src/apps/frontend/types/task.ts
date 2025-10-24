import { JsonObject } from 'frontend/types/common-types';

export class Task {
  id: string;
  title: string;
  description: string;
  accountId: string;

  constructor(json: JsonObject) {
    this.id = json.id as string;
    this.title = json.title as string;
    this.description = json.description as string;
    this.accountId = json.account_id as string;
  }

  toJson(): JsonObject {
    return {
      id: this.id,
      title: this.title,
      description: this.description,
      account_id: this.accountId,
    };
  }
}

export interface PaginationParams {
  page: number;
  size: number;
  offset: number;
}

export interface PaginatedTasks {
  items: Task[];
  totalCount: number;
  totalPages: number;
  paginationParams: PaginationParams;
}

export interface CreateTaskParams {
  title: string;
  description: string;
}

export interface UpdateTaskParams {
  id: string;
  title: string;
  description: string;
}

export interface DeleteTaskParams {
  id: string;
}

export interface GetTasksParams {
  page?: number;
  size?: number;
}