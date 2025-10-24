import { useState, useCallback } from 'react';
import toast from 'react-hot-toast';
import {
  Task,
  PaginatedTasks,
  PaginationParams,
  CreateTaskParams,
  UpdateTaskParams,
  DeleteTaskParams,
  GetTasksParams,
  ApiError,
} from 'frontend/types';
import { TaskService } from 'frontend/services';
import { useAuthContext } from 'frontend/contexts';

interface UseTasksReturn {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  pagination: PaginationParams;
  totalPages: number;
  totalCount: number;
  createTask: (params: CreateTaskParams) => Promise<void>;
  updateTask: (params: UpdateTaskParams) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  loadTasks: (page?: number, size?: number) => Promise<void>;
  refreshTasks: () => Promise<void>;
}

export const useTasks = (): UseTasksReturn => {
  const { getAccessToken } = useAuthContext();
  const taskService = new TaskService();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState<PaginationParams>({
    page: 1,
    size: 9,
    offset: 0,
  });
  const [totalPages, setTotalPages] = useState(0);
  const [totalCount, setTotalCount] = useState(0);

  const handleError = useCallback((error: any, defaultMessage: string) => {
    console.error('Task operation error:', error);
    
    let errorMessage = defaultMessage;
    
    if (error?.response?.data?.message) {
      errorMessage = error.response.data.message;
    } else if (error?.message) {
      errorMessage = error.message;
    }
    
    setError(errorMessage);
    toast.error(errorMessage);
  }, []);

  const loadTasks = useCallback(async (page = 1, size = 9) => {
    try {
      setLoading(true);
      setError(null);
      
      const accessToken = getAccessToken();
      if (!accessToken) {
        throw new Error('No access token available');
      }

      const params: GetTasksParams = { page, size };
      const response = await taskService.getTasks(accessToken, params);
      
      if (response.error) {
        throw response.error;
      }

      if (response.data) {
        setTasks(response.data.items);
        setPagination(response.data.paginationParams);
        setTotalPages(response.data.totalPages);
        setTotalCount(response.data.totalCount);
      }
    } catch (error) {
      handleError(error, 'Failed to load tasks');
      setTasks([]);
      setTotalPages(0);
      setTotalCount(0);
    } finally {
      setLoading(false);
    }
  }, [getAccessToken, taskService, handleError]);

  const refreshTasks = useCallback(async () => {
    await loadTasks(pagination.page, pagination.size);
  }, [loadTasks, pagination.page, pagination.size]);

  const createTask = useCallback(async (params: CreateTaskParams) => {
    try {
      setError(null);
      
      const accessToken = getAccessToken();
      if (!accessToken) {
        throw new Error('No access token available');
      }

      const response = await taskService.createTask(accessToken, params);
      
      if (response.error) {
        throw response.error;
      }

      toast.success('Task created successfully!');
      
      // Refresh the task list
      await refreshTasks();
    } catch (error) {
      handleError(error, 'Failed to create task');
      throw error; // Re-throw so the component can handle it
    }
  }, [getAccessToken, taskService, handleError, refreshTasks]);

  const updateTask = useCallback(async (params: UpdateTaskParams) => {
    try {
      setError(null);
      
      const accessToken = getAccessToken();
      if (!accessToken) {
        throw new Error('No access token available');
      }

      const response = await taskService.updateTask(accessToken, params);
      
      if (response.error) {
        throw response.error;
      }

      toast.success('Task updated successfully!');
      
      // Update the task in the local state
      setTasks(prevTasks => 
        prevTasks.map(task => 
          task.id === params.id 
            ? { ...task, title: params.title, description: params.description }
            : task
        )
      );
    } catch (error) {
      handleError(error, 'Failed to update task');
      throw error; // Re-throw so the component can handle it
    }
  }, [getAccessToken, taskService, handleError]);

  const deleteTask = useCallback(async (id: string) => {
    try {
      setError(null);
      
      const accessToken = getAccessToken();
      if (!accessToken) {
        throw new Error('No access token available');
      }

      const params: DeleteTaskParams = { id };
      const response = await taskService.deleteTask(accessToken, params);
      
      if (response.error) {
        throw response.error;
      }

      toast.success('Task deleted successfully!');
      
      // Remove the task from local state
      setTasks(prevTasks => prevTasks.filter(task => task.id !== id));
      setTotalCount(prevCount => prevCount - 1);
      
      // If we deleted the last task on the current page and it's not the first page,
      // go back to the previous page
      if (tasks.length === 1 && pagination.page > 1) {
        await loadTasks(pagination.page - 1, pagination.size);
      }
    } catch (error) {
      handleError(error, 'Failed to delete task');
      throw error; // Re-throw so the component can handle it
    }
  }, [getAccessToken, taskService, handleError, tasks.length, pagination.page, pagination.size, loadTasks]);

  return {
    tasks,
    loading,
    error,
    pagination,
    totalPages,
    totalCount,
    createTask,
    updateTask,
    deleteTask,
    loadTasks,
    refreshTasks,
  };
};