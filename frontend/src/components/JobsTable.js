import React, {useEffect, useState} from 'react';
import './JobsTable.css';
const JobsTable = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8010/api/get_jobs')
        .then((response) => response.json())
        .then((data) => setJobs(data))
        .catch((error) => console.error(error));
  }, []);

  return (
    <table className="jobs-table">
      <thead>
        <tr>
          <th>Job ID</th>
          <th>Status</th>
          <th>Result</th>
          <th>Time Created</th>
        </tr>
      </thead>
      <tbody>
        {jobs.map((job) => (
          <tr key={job.id}>
            <td>{job.id}</td>
            <td>{job.status}</td>
            <td>{job.result}</td>
            <td>{job.date_done}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default JobsTable;
