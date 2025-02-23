import { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    const pythonProcess = spawn('python', ['./get_courses.py']);

    let responseData = '';

    pythonProcess.stdout.on('data', (data) => {
      responseData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      res.status(500).json({ error: 'An error occurred while executing the Python script' });
    });

    pythonProcess.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
      console.log(`Raw output: ${responseData}`);
      try {
        const result = JSON.parse(responseData);
        res.status(200).json(result);
      } catch (error) {
        console.error('Error parsing JSON:', error);
        res.status(500).json({ error: 'Failed to parse JSON response from Python script' });
      }
    });
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}
