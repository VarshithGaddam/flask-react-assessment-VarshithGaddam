import APIService from 'frontend/services/api.service';
import {
  AccessToken,
  ApiResponse,
  CreateTaskParams,
  DeleteTaskParams,
  GetTasksParams,
  PaginatedTasks,
  Task,
  UpdateTaskParams,
} from 'frontend/types';

export default class TaskService extends APIService {
  getTasks = async (
    userAccessToken: AccessToken,
    params: GetTasksParams = {}
  ): Promise<ApiResponse<PaginatedTasks>> => {
    const { page = 1, size = 10 } = params;
    const queryParams = new URLSearchParams({
      page: page.toString(),
      size: size.toString(),
    });

    const response = await this.apiClient.get(
      `/accounts/${userAccessToken.accountId}/tasks?${queryParams}`,
      {
        headers: {
          Authorization: `Bearer ${userAccessToken.token}`,
        },
      }
    );

    // Transform the response to match our PaginatedTasks interface
    const data = response.data;
    const paginatedTasks: PaginatedTasks = {
      items: data.items.map((item: any) => new Task(item)),
      totalCount: data.total_count,
      totalPages: data.total_pages,
      paginationParams: {
        page: data.pagination_params.page,
        size: data.pagination_params.size,
        offset: data.pagination_params.offset,
      },
    };

    return new ApiResponse(paginatedTasks);
  };

  createTask = async (
    userAccessToken: AccessToken,
    params: CreateTaskParams
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.post(
      `/accounts/${userAccessToken.accountId}/tasks`,
      {
        title: params.title,
        description: params.description,
      },
      {
        headers: {
          Authorization: `Bearer ${userAccessToken.token}`,
        },
      }
    );

    const task = new Task(response.data);
    return new ApiResponse(task);
  };

  updateTask = async (
    userAccessToken: AccessToken,
    params: UpdateTaskParams
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.patch(
      `/accounts/${userAccessToken.accountId}/tasks/${params.id}`,
      {
        title: params.title,
        description: params.description,
      },
      {
        headers: {
          Authorization: `Bearer ${userAccessToken.token}`,
        },
      }
    );

    const task = new Task(response.data);
    return new ApiResponse(task);
  };

  deleteTask = async (
    userAccessToken: AccessToken,
    params: DeleteTaskParams
  ): Promise<ApiResponse<void>> => {
    await this.apiClient.delete(
      `/accounts/${userAccessToken.accountId}/tasks/${params.id}`,
      {
        headers: {
          Authorization: `Bearer ${userAccessToken.token}`,
        },
      }
    );

    return new ApiResponse();
  };
}