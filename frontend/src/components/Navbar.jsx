import logo from "../assets/polarislogo.png";

function Navbar() {
  return (
    <header className="absolute top-0 left-0 z-20 w-full">
      <div className="flex items-center px-5 py-4 sm:px-8">
        <img
          src={logo}
          alt="Polaris"
          className="h-7 w-7 object-contain"
        />

        <h1 className="ml-2 text-2xl font-medium tracking-tight text-white">
          Polaris
        </h1>
      </div>
    </header>
  );
}

export default Navbar;