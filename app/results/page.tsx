import Accordion from "@/components/Accordion";
const data1 = [
    { id: '1', category: 'Category 1', courses: [{ id: '1', courseCode: 'CS101', courseName: 'Intro to Computer Science' }] },
    { id: '2', category: 'Category 2', courses: [{ id: '2', courseCode: 'CS102', courseName: 'Data Structures' }] },
  ];

  const data2 = [
    { id: '3', category: 'Category 3', courses: [{ id: '3', courseCode: 'CS201', courseName: 'Algorithms' }] },
    { id: '4', category: 'Category 4', courses: [{ id: '4', courseCode: 'CS202', courseName: 'Operating Systems' }] },
  ];
export default async function ResultsPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const { major1, major2 } = await searchParams;

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
