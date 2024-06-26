import Link from "next/link";

export const HeaderLink = ({ href, children }) => {
  return (
    <Link href={href} className="text-gray-700 hover:text-blue-500">
      {children}
    </Link>
  );
};
