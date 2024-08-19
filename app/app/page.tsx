
export default function Home() {
  return (
    <div>
      <div className="flex items-center justify-center min-h-screen">
        <div>
          <h1 className="mb-5">Enter Parameters</h1>
          <div>
            <input type="text" className="mb-5 text-black pl-1.5" />
          </div>
          <input type="file" />
        </div>
      </div>
    </div>
  );
}
