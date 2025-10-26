import { Loader2, Search } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
  progress?: number;
}

export function LoadingState({ message = 'Searching...', progress }: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        <div className="absolute inset-0 flex items-center justify-center">
          <Search className="h-8 w-8 text-primary-500 opacity-30" />
        </div>
        <Loader2 className="h-16 w-16 text-primary-600 animate-spin" />
      </div>

      <p className="mt-6 text-gray-600 font-medium">{message}</p>

      {progress !== undefined && (
        <div className="mt-4 w-64">
          <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span>Progress</span>
            <span className="font-medium">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${Math.min(progress, 100)}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
