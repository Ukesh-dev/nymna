import ReactPlayer from "react-player";

const products = [
  {
    id: 1,
    name: "Basic Tee",
    href: "#",
    imageSrc:
      "https://tailwindui.com/img/ecommerce-images/product-page-01-related-product-01.jpg",
    imageAlt: "Front of men's Basic Tee in black.",
    price: "$35",
    color: "Black",
  },
  // More products...
];

const IncidentDetails = () => {
  return (
    <div className="lg:pl-72">
      <div className="p-12">
        <div className=" sm:px-0">
          <h3 className="text-base font-semibold leading-7 text-white">
            Incident Information
          </h3>
          <p className="mt-1 max-w-2xl text-sm leading-6 text-gray-400">
            Details of Incidents
          </p>
        </div>
        <div className="mt-6 border-t border-white/10">
          <dl className="divide-y divide-white/10">
            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt className="text-sm font-medium leading-6 text-white">Name</dt>
              <dd className="mt-1 text-sm leading-6 text-gray-400 sm:col-span-2 sm:mt-0">
                Margot Foster
              </dd>
            </div>
            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt className="text-sm font-medium leading-6 text-white">
                About
              </dt>
              <dd className="mt-1 text-sm leading-6 text-gray-400 sm:col-span-2 sm:mt-0">
                Fugiat ipsum ipsum deserunt culpa aute sint do nostrud anim
                incididunt cillum culpa consequat. Excepteur qui ipsum aliquip
                consequat sint. Sit id mollit nulla mollit nostrud in ea officia
                proident. Irure nostrud pariatur mollit ad adipisicing
                reprehenderit deserunt qui eu.
              </dd>
            </div>
            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <ReactPlayer
                controls
                url="https://vz-e489fdd9-1a4.b-cdn.net/864b6eca-c46f-4e3e-9b64-22b15d7736d4/play_720p.mp4"
              />
            </div>

            <div className="">
              <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
                <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
                  <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
                    {products.map((product) => (
                      <div key={product.id} className="group relative">
                        <div className="min-h-80 aspect-h-1 aspect-w-1 w-full overflow-hidden rounded-md bg-gray-900 lg:aspect-none group-hover:opacity-75 lg:h-80">
                          {/* <img
                            src={product.imageSrc}
                            alt={product.imageAlt}
                            className="h-full w-full object-cover object-center lg:h-full lg:w-full"
                          /> */}
                        </div>
                        <div className="mt-4 flex justify-between">
                          <div>
                            <h3 className="text-sm text-gray-300">
                              <a href={product.href}>
                                <span
                                  aria-hidden="true"
                                  className="absolute inset-0"
                                />
                                {/* {product.name} */}
                              </a>
                            </h3>
                            <p className="mt-1 text-sm text-gray-300">
                              {/* {product.color} */}
                            </p>
                          </div>
                          <p className="text-sm font-medium text-gray-900">
                            {/* {product.price} */}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </dl>
        </div>
      </div>
    </div>
  );
};

export default IncidentDetails;
