import api from ".";

export const getIncidents = async <T>(options: {
  pageIndex: number;
  pageSize: number;
}) => {
  return api.get<T>(`/reports/paged/${options.pageIndex + 1}/`);
};

export const getSingleIncidents = async <T>(incidentId: string) => {
  return api.get<T>(`/report/${incidentId}/`);
};
