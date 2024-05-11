import { Button, Description, Field, Input, Label } from "@headlessui/react";
import { cn } from "../../lib/utils";
import ReactPlayer from "react-player";
import { useMutation, useQuery } from "@tanstack/react-query";
import api from "../../api";
import { useState } from "react";

const Analyze = () => {
  const [url, setUrl] = useState("");
  const [currrentUrl, setCurrentUrl] = useState("");
  const submitMutation = useMutation({
    mutationFn: async (url: string) => {
      return api.post(url, {});
    },
    onSuccess: (data) => {
      // setUrl(data);
      setCurrentUrl(null);
    },
  });
  /* const {data} = useQuery({
    queryKey: ['url'],
    queryFn: () => api
  }) */
  return (
    <div className="lg:pl-72 py-12">
      <div className="w-full mx-auto max-w-2xl px-4">
        <Field>
          <div>
            <Label className="text-sm/6 font-medium text-white">Analyze</Label>
            <Description className="text-sm/6 text-white/50">
              Analyze the video
            </Description>
          </div>
          <div className="flex gap-4 items-center">
            <Input
              onChange={(e) => setCurrentUrl(e.target.value)}
              className={cn(
                "mt-3 block w-full rounded-lg border-none bg-white/5 py-1.5 px-3 text-sm/6 text-white",
                "focus:outline-none data-[focus]:outline-2 data-[focus]:-outline-offset-2 data-[focus]:outline-white/25",
              )}
            />
            <Button
              onClick={() => {
                if (currrentUrl) {
                  submitMutation.mutate(currrentUrl);
                }
              }}
              className="inline-flex items-center gap-2 rounded-md bg-gray-700 py-1.5 px-3 text-sm/6 font-semibold text-white shadow-inner shadow-white/10 focus:outline-none data-[hover]:bg-gray-600 data-[open]:bg-gray-700 data-[focus]:outline-1 data-[focus]:outline-white"
            >
              Analyze
            </Button>
          </div>
        </Field>
        <ReactPlayer controls url="http://localhost:8000/video" />
      </div>
    </div>
  );
};

export default Analyze;
