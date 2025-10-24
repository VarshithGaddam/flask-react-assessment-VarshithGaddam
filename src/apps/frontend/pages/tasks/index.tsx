import React, { useState, useEffect } from 'react';
import { Task, CreateTaskParams, UpdateTaskParams } from 'frontend/types';
import { useTasks } from 'frontend/hooks/use-tasks.hook';
import TaskList from 'frontend/components/task/task-list';
import TaskModal from 'frontend/components/task/task-modal';
import DeleteConfirmationModal from 'frontend/components/task/delete-confirmation-modal';
import Pagination from 'frontend/components/task/pagination';

const TasksPage: React.FC = () => {
  const {
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
  } = useTasks();

  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | undefined>(undefined);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);
  const [operationLoading, setOperationLoading] = useState(false);

  // Load tasks on component mount
  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  const handleCreateTask = () => {
    setEditingTask(undefined);
    setIsTaskModalOpen(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsTaskModalOpen(true);
  };

  const handleDeleteTask = (taskId: string) => {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
      setDeletingTask(task);
      setIsDeleteModalOpen(true);
    }
  };

  const handleTaskSubmit = async (params: CreateTaskParams | UpdateTaskParams) => {
    try {
      setOperationLoading(true);
      
      if ('id' in params) {
        // Update existing task
        await updateTask(params);
      } else {
        // Create new task
        await createTask(params);
      }
      
      setIsTaskModalOpen(false);
      setEditingTask(undefined);
    } catch (error) {
      // Error is already handled in the hook
      console.error('Task operation failed:', error);
    } finally {
      setOperationLoading(false);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deletingTask) return;
    
    try {
      setOperationLoading(true);
      await deleteTask(deletingTask.id);
      setIsDeleteModalOpen(false);
      setDeletingTask(null);
    } catch (error) {
      // Error is already handled in the hook
      console.error('Delete operation failed:', error);
    } finally {
      setOperationLoading(false);
    }
  };

  const handleModalClose = () => {
    if (!operationLoading) {
      setIsTaskModalOpen(false);
      setEditingTask(undefined);
    }
  };

  const handleDeleteCancel = () => {
    if (!operationLoading) {
      setIsDeleteModalOpen(false);
      setDeletingTask(null);
    }
  };

  const handlePageChange = (page: number) => {
    loadTasks(page, pagination.size);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
              <p className="mt-2 text-gray-600">
                Manage your tasks and stay organized
              </p>
            </div>
            <button
              onClick={handleCreateTask}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg
                className="-ml-1 mr-2 h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clipRule="evenodd"
                />
              </svg>
              Add Task
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-red-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Task List */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4">
            <TaskList
              tasks={tasks}
              loading={loading}
              onEdit={handleEditTask}
              onDelete={handleDeleteTask}
            />
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <Pagination
              pagination={pagination}
              totalPages={totalPages}
              totalCount={totalCount}
              onPageChange={handlePageChange}
              loading={loading}
            />
          )}
        </div>

        {/* Task Modal */}
        <TaskModal
          isOpen={isTaskModalOpen}
          task={editingTask}
          onSubmit={handleTaskSubmit}
          onClose={handleModalClose}
          loading={operationLoading}
        />

        {/* Delete Confirmation Modal */}
        <DeleteConfirmationModal
          isOpen={isDeleteModalOpen}
          task={deletingTask}
          onConfirm={handleDeleteConfirm}
          onCancel={handleDeleteCancel}
          loading={operationLoading}
        />
      </div>
    </div>
  );
};

export default TasksPage;