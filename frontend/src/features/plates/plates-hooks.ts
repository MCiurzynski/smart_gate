import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { type ListParams, platesApi } from './plates-api';
import { type PlateInput } from './plates-types';

export const platesKeys = {
  all: ['plates'] as const,
  list: (params: ListParams) => [...platesKeys.all, 'list', params] as const,
};

export const usePlates = (params: ListParams = {}) =>
  useQuery({
    queryKey: platesKeys.list(params),
    queryFn: () => platesApi.list(params),
  });

export const useCreatePlate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: PlateInput) => platesApi.create(input),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: platesKeys.all }),
  });
};

export const useUpdatePlate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ code, input }: { code: string; input: PlateInput }) =>
      platesApi.update(code, input),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: platesKeys.all }),
  });
};

export const useDeletePlate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (code: string) => platesApi.remove(code),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: platesKeys.all }),
  });
};
