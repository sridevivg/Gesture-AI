import { useQuery } from '@tanstack/react-query';
import { apiService } from '@/services/api';

export function useSystemStatus() {
  return useQuery({
    queryKey: ['system-health'],
    queryFn: () => apiService.getHealth(),
    refetchInterval: 10000,
    retry: 1,
  });
}
