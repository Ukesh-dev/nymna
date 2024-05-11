import { create } from "zustand";
import { IncidentType } from "../views/Incidents/components/IncidentTable";

export const useIncident = create<{
  open: boolean;
  setOpen: (open: boolean) => void;
  data: null | IncidentType;
  setData: (data: IncidentType) => void;
  currentData: IncidentType["data"];
  setCurrentData: (currentData: IncidentType["data"]) => void;
  message: { id: number; status: string } | null;
  setMessage: (message: { id: number; status: string }) => void;
}>((set) => ({
  open: false,
  setOpen: (open) => {
    set((state) => ({
      ...state,
      open,
    }));
  },
  data: null,
  setData: (data) => {
    set((state) => ({
      ...state,
      data,
    }));
  },
  currentData: [],
  setCurrentData: (currentData) => {
    set((state) => ({
      ...state,
      currentData,
    }));
  },
  message: null,
  setMessage: (message) => {
    set((state) => ({
      ...state,
      message,
    }));
  },
}));
