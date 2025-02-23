"use client"
import { useState, useEffect } from "react";
import { useRouter } from 'next/navigation';
import LoadingScreen from "@/components/LoadingScreen";
import { Course } from "@/components/course";

export default function LoadingPage({ searchParams }: { searchParams: { [key: string]: string | string[] | undefined } }) {
  const [loading, setLoading] = useState(true);
  const [options, setOptions] = useState<Course[]>([]);
  const [resolvedParams, setResolvedParams] = useState<{ [key: string]: string | string[] | undefined } | null>(null);
  const router = useRouter();

  useEffect(() => {
    const resolveParams = async () => {
      const params = await searchParams;
      setResolvedParams(params);
    };

    resolveParams();
  }, [searchParams]);

  useEffect(() => {
    if (!resolvedParams) return;

    const fetchData = async () => {
      const { major1, major2, math } = resolvedParams;

      const response = await fetch('/api/postMajors', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ major1, major2, math }),
      });
    };

    const fetchChoices = async () => {
      console.log("Fetching choices...");
      const response = await fetch('/api/getChoices', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      const data = await response.json();
      setOptions(data);
      setLoading(false);
    };

    const runFetches = async () => {
      console.log("Running fetches...");
      await fetchData();
      await fetchChoices();
    };

    runFetches();
  }, [resolvedParams]);

  const handleChoiceClick = async (course: Course) => {
    setLoading(true);
    const { major1, major2, math } = resolvedParams;
    try {
      const response = await fetch('/api/getChoices', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(course),
      });
      const data = await response.json();
      if (data.nextChoices.length === 0) {
        console.log("hi");
        router.push(`/results?major1=${encodeURIComponent(major1)}&major2=${encodeURIComponent(major2)}`);
        //router.push(`/results?major1=${encodeURIComponent(major1)}&major2=${encodeURIComponent(major2)}}`{/*&math=${encodeURIComponent(math)}`*/});
      } else {
        console.log("284793274932");
        setOptions(data.nextChoices);
      }
    } catch (error) {
      console.error('Error selecting course:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingScreen />;
  }

  console.log(options);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="mt-8 p-6 bg-white shadow-lg rounded-2xl w-96">
        <h2 className="text-xl font-bold text-gray-800">Which class do you prefer?</h2>
        <ul className="mt-4">
          {options.map((option, index) => (
            <li 
              key={index} 
              className="p-2 cursor-pointer text-left hover:bg-gray-200"
              onClick={() => handleChoiceClick(option)}
            >
              <span className="font-semibold">{option.course_name} </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}