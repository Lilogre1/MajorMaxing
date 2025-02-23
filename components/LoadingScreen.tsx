export default function LoadingScreen() {
  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="text-center p-6 bg-white shadow-lg rounded-2xl w-96">
        <h1 className="text-3xl font-bold text-gray-800">Loading...</h1>
        <p className="text-gray-600 mt-2">Please wait while we fetch the data.</p>
      </div>
    </div>
  );
}