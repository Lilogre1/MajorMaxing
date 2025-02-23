"use client"
import { useState } from "react";
import { Course } from "./course";
interface AccordionProps {
  title: string;
  data: { id: string, category: string, courses: Course[] }[];
}
export default function Accordion({ title, data }: AccordionProps ) {
  const [selected, setSelected] = useState<number[]>([]);

  function handleClick(ind: number): void {
    setSelected(prevArr => prevArr.includes(ind) ? prevArr.filter(val => val !== ind) : [...prevArr, ind]);
  }

  return (
    <div className="w-full max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl">
    <h2 className="text-xl font-bold p-4 bg-gray-200">{title}</h2>
      <div className="accordion">
        {data && data.length > 0 ? data.map((ele, ind) => (
          <div className="accordion-item border-b" key={ind}>
            <div
              className="accordion-header flex justify-between items-center p-4 cursor-pointer hover:bg-gray-100"
              onClick={() => handleClick(ind)}
            >
              <span className="text-lg font-medium">{ele.category}</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className={`transform transition-transform duration-200 ${selected.includes(ind) ? 'rotate-180' : ''}`}
              >
                <path d="m6 9 6 6 6-6"></path>
              </svg>
            </div>
            {selected.includes(ind) && (
              <div className="accordion-collapse p-4 bg-gray-50">
                {ele.courses.map(course => (
                  <div key={course.id} className="p-2">
                    <span className="font-semibold">{course.courseCode}: </span>
                    <span>{course.courseName}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )) : "No data"}
      </div>
    </div>
  );
}