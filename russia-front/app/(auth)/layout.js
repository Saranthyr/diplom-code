export default function AuthLayout({ children }) {
  return (
    <main className="flex flex-1 flex-col items-center justify-center bg-custom-bg bg-cover bg-center">
      {children}
    </main>
  );
}
