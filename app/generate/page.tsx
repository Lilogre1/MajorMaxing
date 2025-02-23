"use client"
import { useState, useEffect } from "react";
import { useRouter } from 'next/router';
import LoadingScreen from "@/components/LoadingScreen";
import { Course } from "@/components/course";

export default function LoadingPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const { major1, major2, math } = await searchParams; 
  const [loading, setLoading] = useState(true);
  const [options, setOptions] = useState<Course[]>([]);
  const router = useRouter();

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/api/postMajors', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({major1: major1,major2: major2,math: math }),
      });
      const data = await response.json();
      setOptions(data.courses);
      setLoading(false);
    };

    fetchData();
  }, []);

  const handleChoiceClick = async (course: Course) => {
    setLoading(true);
    try {
      const response = await fetch('/api/postChoices', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ course: course }),
      });
      const data = await response.json();
      if (data.nextChoices.length === 0) {

        router.push(`/results?major1=${encodeURIComponent(major1)}&major2=${encodeURIComponent(major2)}&math=${encodeURIComponent(selectedOption)}`);
      } else {
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
              <span className="font-semibold">{option.courseCode}: </span>
              <span>{option.courseName}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}