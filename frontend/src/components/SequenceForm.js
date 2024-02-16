import React, { useState, useEffect } from 'react';
import axios from 'axios';

function SequenceForm() {
  const [jobId, setJobId] = useState('');
  const [value, setValue] = useState('');
  const [status, setStatus] = useState('');


  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Form submitted with value: ', value);
    axios.post('http://localhost:8010/api/align/', JSON.stringify({sequence: value}))
      .then(response => {
        setJobId(response.data.jobId);
        setStatus(response.data.status);
      })
      .catch(error => {
        console.log(error);
      });  
    };

  const handleChange = (event) => {
    setValue(event.target.value);
  };
  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={value} onChange={handleChange} />
      <button type="submit">Submit</button>
      <p id="job">{jobId} {status}</p>
    </form>
  );
}

export default SequenceForm;