import React from 'react';
import { Task } from 'frontend/types';

interface TaskItemProps {
  task: Task;
  onEdit: () => void;
  onDelete: () => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onEdit, onDelete }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold text-gray-900 truncate pr-2">
          {task.title}
        </h3>
        <div className="flex space-x-2 flex-shrink-0">
          <button
            onClick={onEdit}
            className="text-blue-600 hover:text-blue-800 transition-colors p-1 rounded hover:bg-blue-50"
            title="Edit task"
            aria-label={`Edit task: ${task.title}`}
          >
            <svg
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
          <button
            onClick={onDelete}
            className="text-red-600 hover:text-red-800 transition-colors p-1 rounded hover:bg-red-50"
            title="Delete task"
            aria-label={`Delete task: ${task.title}`}
          >
            <svg
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
      
      <p className="text-gray-600 text-sm mb-4 break-words">
        {task.description}
      </p>
      
      <div className="flex justify-between items-center text-xs text-gray-400">
        <span>ID: {task.id.slice(-8)}</span>
        <span>Account: {task.accountId.slice(-8)}</span>
      </div>
    </div>
  );
};

export default TaskItem;