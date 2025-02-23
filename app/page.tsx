"use client"

import { useRouter } from "next/navigation";
import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import Dropdown from "@/components/Dropdown";

const suggestions = ["Computer Science", "Math", "Data Science", "Statistics", "Information Science"];
const dropdownOptions = ["MATH 221 - AP Calc AB", "MATH 222 - AP Calc BC"];

export default function Home() {
  const [major1, setMajor1] = useState("");
  const [major2, setMajor2] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const router = useRouter();

  const handleSearch = () => {
    console.log(major1, major2, selectedOption);
    router.push(`/generate?major1=${encodeURIComponent(major1)}&major2=${encodeURIComponent(major2)}`);//&math=${encodeURIComponent(selectedOption)}`);
  };

  const handleSuggestionClick1 = (suggestion: string) => {
    setMajor1(suggestion);
  };

  const handleSuggestionClick2 = (suggestion: string) => {
    setMajor2(suggestion);
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="text-center p-6 bg-white shadow-lg rounded-2xl w-96">
        <h1 className="text-3xl font-bold text-gray-800">Degree Optimizer</h1>
        <p className="text-gray-600 mt-2">
          Select two majors to find the optimal course plan that minimizes credit requirements.
        </p>
        <SearchBar
          placeholder="Enter first major"
          value={major1}
          onChange={setMajor1}
          suggestions={suggestions}
          onSuggestionClick={handleSuggestionClick1}
        />
        <SearchBar
          placeholder="Enter second major"
          value={major2}
          onChange={setMajor2}
          suggestions={suggestions}
          onSuggestionClick={handleSuggestionClick2}
        />
        <label className="block text-center font-bold text-gray-700 mt-4">Math Level</label>
        <Dropdown
          options={dropdownOptions}
          selectedOption={selectedOption}
          onOptionSelect={setSelectedOption}
        />
        <button 
          onClick={handleSearch}
          className="w-full bg-blue-500 text-white py-2 mt-4 rounded-lg hover:bg-blue-600"
        >
          Find Optimal Courses
        </button>
      </div>
    </div>
  );
}