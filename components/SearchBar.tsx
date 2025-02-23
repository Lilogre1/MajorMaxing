import { useState } from "react";

interface SearchBarProps {
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
  suggestions: string[];
  onSuggestionClick: (suggestion: string) => void;
}

export default function SearchBar({ placeholder, value, onChange, suggestions, onSuggestionClick }: SearchBarProps) {
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    onChange(value);
    if (value === "") {
      setFilteredSuggestions([]);
    } else {
      setFilteredSuggestions(suggestions.filter(suggestion => suggestion.toLowerCase().includes(value.toLowerCase())));
    }
    setShowSuggestions(true);
  };

  return (
    <div className="relative mt-4">
      <input
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={handleChange}
        onFocus={() => setShowSuggestions(true)}
        onBlur={() => setTimeout(() => setShowSuggestions(false), 100)}
        className="w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      {showSuggestions && filteredSuggestions.length > 0 && (
        <ul className="absolute z-20 w-full border rounded-lg bg-white mt-1">
          {filteredSuggestions.map((suggestion, index) => (
            <li
              key={index}
              onMouseDown={() => onSuggestionClick(suggestion)}
              className="p-2 cursor-pointer text-left hover:bg-gray-200"
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}