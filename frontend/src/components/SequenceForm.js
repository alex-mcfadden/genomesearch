import React, {useState} from 'react';
import axios from 'axios';

function SequenceForm() {
  const [value, setValue] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    setError('');
    setSubmitted(true);

    axios.post('http://localhost:8010/api/align/', JSON.stringify({sequence: value}))
        .then((response) => {
          setTaskId(response.data.task_id);
          setStatus(response.data.status);
        })
        .catch((error) => {
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
      <p id="job">{ status ? 'Job submitted! Status is ' + status : ''}</p>
    </form>
  );
};

export default SequenceForm;
