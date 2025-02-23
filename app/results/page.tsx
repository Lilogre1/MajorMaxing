"use client"
import { useEffect, useState } from 'react';
import Accordion from "@/components/Accordion";

export default function ResultsPage({ searchParams }: { searchParams: { [key: string]: string | string[] | undefined } }) {
  const [data1, setData1] = useState([]);
  const [data2, setData2] = useState([]);
  const [resolvedParams, setResolvedParams] = useState<{ [key: string]: string | string[] | undefined } | null>(null);

  useEffect(() => {
    const resolveParams = async () => {
      const params = await searchParams;
      setResolvedParams(params);
    };

    resolveParams();
  }, [searchParams]);

  useEffect(() => {
    console.log(resolvedParams);
    if (!resolvedParams) return;

    const fetchData = async () => {
      const response = await fetch('/api/getCourses');
      const data = await response.json();
      console.log(data.courses1);
      setData1(data.courses1);
      setData2(data.courses2);
    };

    fetchData();
  }, [resolvedParams]);

  if (!resolvedParams) {
    return <div>Loading...</div>;
  }

  const { major1, major2 } = resolvedParams;

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h1 className="text-3xl font-bold text-gray-800">Optimal Course Plan</h1>
      <p className="text-gray-600 mt-2">
       Showing courses for: <strong>{major1}</strong> and <strong>{major2}</strong>
      </p>
      <div className="flex space-x-4 mt-4 w-full max-w-5xl">
        <Accordion title={`Courses for ${major1}`} data={data1} />
        <Accordion title={`Courses for ${major2}`} data={data2} />
      </div>
    </div>
  );
}
