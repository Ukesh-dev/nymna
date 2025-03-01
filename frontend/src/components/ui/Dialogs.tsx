import { Fragment, useRef } from "react";
import { Button, Dialog, Transition } from "@headlessui/react";
import { ExclamationTriangleIcon } from "@heroicons/react/24/outline";
import { useNavigate } from "react-router-dom";
import { cn } from "../../lib/utils";

export default function Dialogs({
  open,
  setOpen,
  message,
}: {
  open: boolean;
  message: { id: number; status: string } | null;
  setOpen: (e: boolean) => void;
}) {
  const cancelButtonRef = useRef(null);

  const navigate = useNavigate();
  return (
    <Transition.Root show={open} as={Fragment}>
      <Dialog
        as="div"
        className="relative z-10"
        initialFocus={cancelButtonRef}
        onClose={setOpen}
        // onClose={(e) => setOpen(e)}
      >
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              {/* w-full max-w-md rounded-xl bg-white/5 p-6 backdrop-blur-2xl */}
              <Dialog.Panel className="relative transform overflow-hidden  rounded-lg  text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                <div className="bg-gray-900/75 px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                  <div className="sm:flex sm:items-start">
                    <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                      <ExclamationTriangleIcon
                        className="h-6 w-6 text-red-600"
                        aria-hidden="true"
                      />
                    </div>
                    <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                      <Dialog.Title
                        as="h3"
                        className="text-base font-semibold leading-6 text-white"
                      >
                        Incident Alert
                      </Dialog.Title>
                      <div className="mt-2">
                        <p className="text-[1rem] text-white/85">
                          There has been an incident!!!{" "}
                        </p>

                        <p
                          className={cn(
                            " p-0 inline-flex mt-4 items-center rounded-[.5rem] bg-green-50 px-2 py-1 text-[14px] font-medium capitalize text-green-700 ring-1 ring-inset ring-green-600/20",
                            message?.status === "minor"
                              ? "text-green-700 ring-green-600/20 bg-green-100 "
                              : message?.status === "mediocre"
                                ? "text-amber-700 ring-amber-600/20 bg-amber-100 "
                                : "text-red-700 ring-red-600/20 bg-red-100 ",
                          )}
                        >
                          Status: {message?.status}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
                <div className=" px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6 bg-gray-900/75 backdrop-blur-2xl ">
                  <Button
                    type="button"
                    className="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto"
                    onClick={() => {
                      navigate(`/incidents/${message?.id}`);
                      setOpen(false);
                    }}
                  >
                    View Details
                  </Button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
}
