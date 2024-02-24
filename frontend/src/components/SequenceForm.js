import React, { useState, useEffect } from 'react';
import axios from 'axios';

function SequenceForm() {
  const [jobId, setJobId] = useState('');
  const [value, setValue] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [retries, setRetries] = useState(10);
  useEffect(() => {
    const checkStatus = async () => {
      if (submitted === true && retries > 0 && jobId !== '') {
      setRetries(retries - 1);
      axios.get('http://localhost:8010/api/get_job_status/', {params: {"job_id": jobId}})
      .then( response => {
        setStatus(response.data.status);
      }).catch(error => {})
    }};
  const intervalId = setInterval(checkStatus, 1000);
  return () => clearInterval(intervalId);
  });
  const handleSubmit = (event) => {
    event.preventDefault();
    setError('');
    console.log('Form submitted with value: ', value);
    setSubmitted(true);
    axios.post('http://localhost:8010/api/align/', JSON.stringify({sequence: value}))
      .then(response => {
        setJobId(response.data.jobId);
        setStatus(response.data.status);
      })
      .catch(error => {
        setError(error.response.data.error);
      });  
    };

  const handleChange = (event) => {
    setValue(event.target.value);
  };
  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={value} onChange={handleChange} />
      <button type="submit">Submit</button>
      <p> {error} </p>
      <p id="job">{jobId} {status}</p>
    </form>
  );
};

export default SequenceForm;