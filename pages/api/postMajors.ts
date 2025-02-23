import { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const { major1, major2, math } = req.body;
      const pythonProcess = spawn('python', ['./scripts/select_course.py',(major1), (major2), (math)]);

      pythonProcess.stdout.on('data', (data) => {
        const result = JSON.parse(data.toString());
        res.status(200).json({ nextChoices: result });
      });

      pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        res.status(500).json({ error: 'An error occurred while executing the Python script' });
      });

      pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
      });
    } catch (error) {
      res.status(500).json({ error: 'Failed to select course' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}