import { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    const pythonProcess = spawn('python', ['./scripts/script.py']);

    pythonProcess.stdout.on('data', (data) => {
      const result = JSON.parse(data.toString());
      res.status(200).json(result);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      res.status(500).json({ error: 'An error occurred while executing the Python script' });
    });

    pythonProcess.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
    });
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}